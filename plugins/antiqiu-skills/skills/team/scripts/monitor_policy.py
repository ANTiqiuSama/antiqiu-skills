"""One observation -> a proposed schedule or handoff. Standard library only."""
import argparse
import copy
import json
import math
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


DEFAULTS = {"min_minutes": 15, "initial_minutes": 60, "max_minutes": 240}
WAKE_SOURCE = "wake_observations"
MAX_POINTS = 32


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError("observed_at must be an ISO timestamp")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("observed_at must include a timezone")
    return parsed.timestamp()


def utc(value):
    return datetime.fromtimestamp(value, timezone.utc).isoformat().replace("+00:00", "Z")


def finite_number(value):
    return type(value) in (int, float) and math.isfinite(value)


def validate(snapshot):
    if not isinstance(snapshot, dict):
        raise ValueError("snapshot must be an object")
    if not isinstance(snapshot.get("job_id"), str) or not snapshot["job_id"].strip():
        raise ValueError("job_id is required")
    timestamp(snapshot.get("observed_at"))
    if snapshot.get("status") not in {"running", "unknown", "succeeded", "failed", "needs_decision"}:
        raise ValueError("invalid status")
    for key in ("identity_verified", "progress_comparable"):
        if key in snapshot and type(snapshot[key]) is not bool:
            raise ValueError(f"{key} must be a boolean")
    if snapshot.get("alive") is not None and type(snapshot["alive"]) is not bool:
        raise ValueError("alive must be boolean or null")
    for key in ("phase", "execution_id", "event_key", "detail"):
        if key in snapshot and not isinstance(snapshot[key], str):
            raise ValueError(f"{key} must be a string")
    completed, total = snapshot.get("completed"), snapshot.get("total")
    if completed is None and total is None:
        return
    if not all(finite_number(v) and v >= 0 for v in (completed, total)):
        raise ValueError("completed and total must both be finite nonnegative numbers")
    if completed > total:
        raise ValueError("completed cannot exceed total")


def supplied_progress(snapshot):
    supplied = snapshot.get("progress_samples")
    if supplied is None:
        return None
    if not isinstance(supplied, dict):
        raise ValueError("progress_samples must be an object")
    for key in ("job_id", "phase", "total", "execution_id"):
        if supplied.get(key) != snapshot.get(key):
            raise ValueError(f"progress samples must match current {key}")
    source, points = supplied.get("source"), supplied.get("points")
    if not isinstance(source, str) or not source.strip() or source == WAKE_SOURCE:
        raise ValueError("producer samples require a distinct, nonempty source")
    if not isinstance(points, list) or not 3 <= len(points) <= 64:
        raise ValueError("progress samples require 3 to 64 points")
    now, previous = timestamp(snapshot["observed_at"]), None
    for point in points:
        if not isinstance(point, dict):
            raise ValueError("progress point must be an object")
        at, count = point.get("at"), point.get("completed")
        if not all(finite_number(v) for v in (at, count)):
            raise ValueError("progress point must contain finite time and count")
        if at > now or count < 0 or snapshot.get("completed") is None or count > snapshot["completed"]:
            raise ValueError("progress point cannot exceed current time or count")
        if previous and (at <= previous["at"] or count <= previous["completed"]):
            raise ValueError("progress samples must increase in time and count")
        previous = point
    return supplied


def prepare_state(snapshot, previous, overrides):
    state = copy.deepcopy(previous or {})
    if state and state.get("version") != 1:
        raise ValueError("unsupported state version; inspect existing monitor")
    if state and state.get("job_id") != snapshot["job_id"]:
        raise ValueError("job_id changed; use a separate state for a verified new job")
    policy = {**DEFAULTS, **state.get("policy", {}), **(overrides or {})}
    if set(policy) != set(DEFAULTS) or any(type(v) is not int or v <= 0 for v in policy.values()):
        raise ValueError("policy requires min_minutes, initial_minutes and max_minutes as positive integers")
    if not policy["min_minutes"] <= policy["initial_minutes"] <= policy["max_minutes"]:
        raise ValueError("require min_minutes <= initial_minutes <= max_minutes")
    last = state.get("last_snapshot")
    if last and timestamp(snapshot["observed_at"]) <= timestamp(last["observed_at"]):
        raise ValueError("observation must be newer; repeated input is not a new check")
    return state, policy


def progress_context(snapshot, last):
    completed = snapshot.get("completed")
    reset = not last or any(snapshot.get(k) != last.get(k) for k in ("phase", "total", "execution_id"))
    advancing = False
    if last and completed is not None and last.get("completed") is not None:
        reset = reset or completed < last["completed"]
        advancing = completed > last["completed"]
    comparable = (snapshot["status"] == "running" and snapshot.get("identity_verified")
                  and snapshot.get("alive") is True and bool(snapshot.get("phase"))
                  and snapshot.get("progress_comparable", False) and completed is not None)
    return bool(comparable), bool(reset), advancing


def estimate_progress(snapshot, state, supplied):
    """Use producer history immediately; never mix completion times with wake times."""
    last, now = state.get("last_snapshot"), timestamp(snapshot["observed_at"])
    comparable, reset, advancing = progress_context(snapshot, last)
    completed = snapshot.get("completed")
    producer = supplied if supplied and supplied["points"][-1]["completed"] == completed else None
    source = producer["source"] if producer else WAKE_SOURCE
    old_source = state.get("history_source", WAKE_SOURCE)
    previous_comparable = progress_context(last, None)[0] if last else False
    if not comparable:
        history = []
    elif producer:
        history = copy.deepcopy(producer["points"][-MAX_POINTS:])
    else:
        history = [] if reset or not previous_comparable or old_source != WAKE_SOURCE else state.get("history", [])
        if not history or completed != history[-1]["completed"]:
            history = (history + [{"at": now, "completed": completed}])[-6:]

    eta, costs, reason = None, [], "insufficient_progress"
    if not comparable:
        reason = "progress_not_comparable"
    elif snapshot["total"] == completed:
        reason = "await_explicit_terminal"
    elif len(history) >= 3 and (advancing or producer):
        costs = [(b["at"] - a["at"]) / (b["completed"] - a["completed"])
                 for a, b in zip(history, history[1:])]
        age = now - history[-1]["at"] if producer else 0
        if min(costs) <= 0 or max(costs) > min(costs) * 3:
            reason = "variable_rate"
        elif age > max(costs) * 3:
            reason = "stale_progress"
        else:
            remaining = snapshot["total"] - completed
            eta = [max(0, math.floor((min(costs) * remaining - age) / 60) * 60),
                   max(0, math.ceil((max(costs) * remaining - age) / 60) * 60)]
            reason = "measured_phase_progress"
    elif not advancing and not producer and last:
        reason = "no_new_progress"
    return {"history": history, "source": source, "eta": eta, "costs": costs,
            "reason": reason, "reset": reset, "advancing": advancing, "comparable": comparable}


def choose_interval(snapshot, state, policy, progress):
    eta, completed = progress["eta"], snapshot.get("completed")
    last = state.get("last_snapshot")
    if eta is not None:
        interval, basis = math.ceil(eta[0] / 60 / 3 / 5) * 5, "remaining_work_eta"
    elif completed is not None and completed == snapshot["total"] and completed > 0:
        was_full = last and not progress["reset"] and last.get("completed") == last.get("total")
        interval = state.get("interval_minutes", policy["min_minutes"]) * 2 if was_full else policy["min_minutes"]
        basis = "await_explicit_terminal"
    elif progress["reset"] or (progress["advancing"] and progress["comparable"]):
        interval, basis = policy["initial_minutes"], "collect_progress_samples"
    else:
        interval = state.get("interval_minutes", policy["initial_minutes"]) * 2
        basis = "no_usable_progress_backoff"
    return max(policy["min_minutes"], min(policy["max_minutes"], interval)), basis


def detect_event(snapshot, previous_unknown_count):
    status = snapshot["status"]
    unknown = status == "unknown" or (status == "running" and not
              (snapshot.get("identity_verified") and snapshot.get("alive") is not None))
    unknown_count = previous_unknown_count + 1 if unknown else 0
    reason = status if status in {"failed", "needs_decision", "succeeded"} else None
    if not reason and status == "running" and snapshot.get("alive") is False and snapshot.get("identity_verified"):
        reason = "process_missing"
    elif not reason and unknown_count >= 3:
        reason = "observation_unavailable"
    # No changing timestamp in the event identity: repeated probes reuse the worker.
    identity = [snapshot["job_id"], reason, snapshot.get("event_key", "")]
    if snapshot.get("execution_id"):
        identity.append(snapshot["execution_id"])
    event_id = json.dumps(identity, ensure_ascii=False, separators=(",", ":")) if reason else None
    return event_id, reason, unknown_count


def route_handoff(snapshot, handoff, event_id, reason):
    action, model = "wait", "luna"
    if handoff and handoff["status"] == "handled":
        return handoff, "stop", "none", handoff["event_id"], "monitoring_finished"
    if handoff and handoff["status"] in {"pending", "dispatched"}:
        if event_id and event_id != handoff["event_id"]:
            handoff["latest_incident"] = {"event_id": event_id, "reason": reason, "snapshot": snapshot}
        action, model = ("wait_for_worker", "none") if handoff["status"] == "dispatched" else ("escalate", "large")
        return handoff, action, model, handoff["event_id"], handoff["reason"]
    trigger = handoff.get("trigger_snapshot", {}) if handoff else {}
    old_execution, new_execution = trigger.get("execution_id"), snapshot.get("execution_id")
    new_instance = bool(old_execution and new_execution and old_execution != new_execution)
    same_incident = (handoff and handoff.get("reason") == reason
                     and trigger.get("event_key", "") == snapshot.get("event_key", "") and not new_instance)
    if event_id and handoff and same_incident and handoff["status"] == "released":
        # Missing execution identity is not proof of a restart; keep legacy handoffs valid.
        reason = "reviewed_continue_waiting"
    elif event_id:
        handoff = {"event_id": event_id, "status": "pending", "worker_id": None,
                   "reason": reason, "trigger_snapshot": snapshot}
        action, model = "escalate", "large"
    elif (handoff and handoff["status"] == "released" and snapshot["status"] == "running"
          and snapshot.get("identity_verified") and snapshot.get("alive") is True):
        handoff = None  # Real recovery rearms a later recurrence; unknown does not.
    return handoff, action, model, event_id, reason


def pending_decision(state):
    """Handle an existing handoff before spending another probe or model run."""
    handoff = (state or {}).get("handoff")
    if not handoff or handoff.get("status") == "released":
        return None
    action, model = {"pending": ("escalate", "large"),
                     "dispatched": ("wait_for_worker", "none"),
                     "handled": ("stop", "none")}[handoff["status"]]
    return {"action": action, "model_tier": model, "event_id": handoff["event_id"],
            "reason": handoff["reason"], "worker_id": handoff.get("worker_id"),
            "interval_minutes": None, "scheduled": False}


def observe(snapshot, previous=None, overrides=None):
    validate(snapshot)
    supplied = supplied_progress(snapshot)
    state, policy = prepare_state(snapshot, previous, overrides)
    progress = estimate_progress(snapshot, state, supplied)
    interval, basis = choose_interval(snapshot, state, policy, progress)
    observed_event, reason, unknown_count = detect_event(snapshot, state.get("unknown_count", 0))
    handoff, action, model, event_id, reason = route_handoff(snapshot, state.get("handoff"), observed_event, reason)
    now, eta, costs = timestamp(snapshot["observed_at"]), progress["eta"], progress["costs"]
    decision = {
        "action": action, "model_tier": model, "reason": reason or progress["reason"],
        "interval_minutes": interval if action == "wait" else None,
        "proposed_next_check_at": utc(now + interval * 60) if action == "wait" else None,
        "eta_seconds_range": eta,
        "estimated_phase_completion_at_range": [utc(now + t) for t in eta] if eta is not None else None,
        "eta_source": progress["source"] if eta is not None else None,
        "eta_unavailable_reason": progress["reason"] if eta is None else None,
        "seconds_per_unit_range": [min(costs), max(costs)] if eta is not None else None,
        "rate_interval_count": len(costs) if eta is not None else 0,
        "remaining_units": snapshot["total"] - snapshot["completed"] if snapshot.get("completed") is not None else None,
        "schedule_basis": basis, "scheduled": False,
        "event_id": event_id, "observed_event_id": observed_event,
        "worker_id": handoff.get("worker_id") if handoff else None,
    }
    state.update(version=1, job_id=snapshot["job_id"], policy=policy, last_snapshot=snapshot,
                 history=progress["history"], history_source=progress["source"], interval_minutes=interval,
                 unknown_count=unknown_count, handoff=handoff, decision=decision)
    return state, decision


def acknowledge(state, event_id, command, worker_id=None):
    result = copy.deepcopy(state)
    handoff = result.get("handoff")
    if not handoff or handoff.get("event_id") != event_id:
        raise ValueError("event_id does not match the pending handoff")
    if command == "dispatched":
        if not isinstance(worker_id, str) or not worker_id.strip():
            raise ValueError("actual worker_id is required")
        if handoff["status"] not in {"pending", "dispatched"}:
            raise ValueError("only a pending incident can be dispatched")
        if handoff["status"] == "dispatched" and handoff["worker_id"] != worker_id:
            raise ValueError("event already assigned to another worker")
        handoff.update(status="dispatched", worker_id=worker_id)
    elif command == "handled":
        if handoff["status"] not in {"dispatched", "handled"}:
            raise ValueError("cannot finish an undispatched handoff")
        handoff["status"] = "handled"
    elif command == "resume":
        if handoff["status"] not in {"dispatched", "released"}:
            raise ValueError("only a completed worker handoff can resume monitoring")
        handoff["status"] = "released"
    else:
        raise ValueError("unknown acknowledgement command")
    result["decision"] = {"action": {"dispatched": "wait_for_worker", "handled": "stop", "resume": "rearm"}[command],
                          "event_id": event_id, "worker_id": handoff.get("worker_id"), "scheduled": False}
    return result


def load_json(path):
    with Path(path).open(encoding="utf-8-sig") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError("JSON must be an object")
    return value


def save_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + f".tmp-{os.getpid()}")
    try:
        temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    obs = sub.add_parser("observe")
    obs.add_argument("--snapshot", required=True)
    obs.add_argument("--state", required=True)
    for key in DEFAULTS:
        obs.add_argument("--" + key.replace("_", "-"), type=int)
    for command in ("dispatched", "handled", "resume"):
        ack = sub.add_parser(command)
        ack.add_argument("--state", required=True)
        ack.add_argument("--event-id", required=True)
        if command == "dispatched":
            ack.add_argument("--worker-id", required=True)
    args = parser.parse_args()
    state_path = Path(args.state)
    try:
        if args.command == "observe":
            if state_path.resolve() == Path(args.snapshot).resolve():
                raise ValueError("snapshot and state must be different files")
            previous = load_json(state_path) if state_path.exists() else None
            overrides = {k: getattr(args, k) for k in DEFAULTS if getattr(args, k) is not None}
            state, output = observe(load_json(args.snapshot), previous, overrides)
        else:
            state = acknowledge(load_json(state_path), args.event_id, args.command, getattr(args, "worker_id", None))
            output = state["handoff"]
        save_json(state_path, state)
        print(json.dumps(output, ensure_ascii=False))
        return 0
    except (KeyError, ValueError, TypeError, AttributeError, OSError) as exc:
        print(json.dumps({"error": str(exc), "scheduled": False}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
