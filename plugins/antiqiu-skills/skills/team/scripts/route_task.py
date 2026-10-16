"""Fail-closed routing for the explicitly invoked team skill.

Input is one JSON object on stdin or --input. External review receipts are
verified from caller-read raw receipts, never from truthy summary flags.
"""
import argparse
import hashlib
import json
import sys


KINDS = {"mechanical", "implementation", "judgment", "review", "wait"}
RISKS = {"low", "medium", "high"}
EXPLICIT_MODELS = {None, "gemini", "grok", "mimo", "luna"}

EXECUTION_FIELDS = (
    "attempt_protocol", "objective_claims", "inputs_identity", "write_scope",
    "command_environment", "budget_stop", "metrics_aggregation",
    "engineering_completion", "scientific_predicate", "evidence_recovery_escalation",
)
NOT_APPLICABLE = {"scientific_predicate"}


def quota_zone(remaining):
    if remaining is None:
        return "unknown"
    if isinstance(remaining, bool) or not isinstance(remaining, (int, float)) or not 0 <= remaining <= 100:
        raise ValueError("remaining percent must be null or a number from 0 to 100")
    if remaining >= 50:
        return "green"
    if remaining >= 20:
        return "yellow"
    if remaining >= 10:
        return "red"
    return "emergency"


def _present(value):
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        if isinstance(value, dict):
            return bool(value) and all(_present(v) for v in value.values())
        return bool(value) and all(_present(v) for v in value)
    return True


def missing_execution_fields(packet):
    if not isinstance(packet, dict):
        return list(EXECUTION_FIELDS)
    missing = []
    for field in EXECUTION_FIELDS:
        value = packet.get(field)
        if field in NOT_APPLICABLE and isinstance(value, str) and value.strip().lower() in {"not_applicable", "n/a"}:
            continue
        if isinstance(value, bool) or not _present(value):
            missing.append(field)
    return list(dict.fromkeys(missing))


def canonical_execution_revision(packet):
    """SHA-256 of canonical JSON, binding every execution-packet value."""
    if not isinstance(packet, dict):
        raise ValueError("execution_packet must be an object")
    missing = missing_execution_fields(packet)
    if missing:
        raise ValueError("execution_packet missing fields: " + ", ".join(missing))
    canonical = json.dumps(packet, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def verify_review_receipt(receipt, revision):
    """Validate observed raw CLI receipt fields; booleans/summary cannot suffice."""
    if not isinstance(receipt, dict):
        return False
    model = receipt.get("actual_model") or receipt.get("model")
    requested = receipt.get("requested_model")
    result = receipt.get("result")
    requested_effort = receipt.get("requested_reasoning_effort")
    launch_effort = receipt.get("launch_reasoning_effort")
    actual_effort = receipt.get("actual_reported_reasoning_effort")
    return (receipt.get("status") == "success" and type(receipt.get("exit_code")) is int and receipt.get("exit_code") == 0
            and receipt.get("isolation_verified") is True
            and receipt.get("tools_used") == [] and receipt.get("tools_available") == []
            and _present(receipt.get("result")) and model == "grok-4.7"
            and requested == "grok-4.7" and receipt.get("revision") == revision
            and requested_effort == "xhigh" and launch_effort == "xhigh"
            and ((receipt.get("effort_evidence") == "launch_argument" and actual_effort is None)
                 or (receipt.get("effort_evidence") == "server_echo" and actual_effort == "xhigh"))
            and isinstance(result, str) and bool(result.strip())
            and not (receipt.get("model") and receipt.get("actual_model")
                     and receipt.get("model") != receipt.get("actual_model")))


def decision(route_name, model, effort, execution, reason, *, zone="unknown", attempts=None, **extra):
    result = {"route": route_name, "model": model, "reasoning_effort": effort,
              "quota_zone": zone, "execution": execution,
              "max_worker_attempts": attempts, "reason": reason}
    result.update(extra)
    return result


def route(request):
    kind = request.get("task_kind", "implementation")
    risk = request.get("risk", "medium")
    explicit = request.get("explicit_model")
    if kind not in KINDS:
        raise ValueError(f"unsupported task_kind: {kind}")
    if risk not in RISKS:
        raise ValueError(f"unsupported risk: {risk}")
    if explicit not in EXPLICIT_MODELS:
        raise ValueError(f"unsupported explicit_model: {explicit}")
    codex_zone = quota_zone(request.get("codex_remaining_percent"))
    grok_zone = quota_zone(request.get("grok_remaining_percent"))
    current_model = request.get("current_model")
    plan_mode = request.get("plan_mode") is True
    actual_job = request.get("actual_job")

    operation = request.get("operation", "review" if kind == "review" else "implementation")
    if operation not in {"review", "implementation"}:
        raise ValueError(f"unsupported operation: {operation}")
    if kind == "wait":
        if (not isinstance(actual_job, dict) or not _present(actual_job.get("job_id"))
                or actual_job.get("identity_verified") is not True
                or actual_job.get("status") != "running" or actual_job.get("alive") is not True
                or not _present(actual_job.get("execution_id"))):
            route_name = "blocked" if actual_job is None else "coordinator_decide"
            return decision(route_name, current_model, None, "root", "job is absent, inactive, or identity is incomplete",
                            coordinator_model=current_model)
        if request.get("stop_requested") is True:
            return decision("coordinator_decide", current_model, None, "root", "stop was requested",
                            coordinator_model=current_model)
        if request.get("luna_available") is False or request.get("luna_hard_limited") is True:
            return decision("blocked", None, None, "root", "GPT-6 Luna unavailable or hard-limited; no substitution",
                            coordinator_model=current_model)
        executor = request.get("executor_binding")
        if request.get("executor_authorized") is not True:
            return decision("coordinator_decide", current_model, None, "root", "user authorization is required before creating or attaching the fixed Luna task",
                            coordinator_model=current_model)
        if not isinstance(executor, dict) or executor.get("thread_id") != request.get("fixed_luna_thread_id") or not _present(request.get("fixed_luna_thread_id")):
            return decision("coordinator_decide", current_model, None, "root", "bind the fixed Luna executor task before monitoring",
                            coordinator_model=current_model)
        if executor.get("model") != "gpt-6-luna" or executor.get("reasoning_effort") != "low" or executor.get("heartbeat") != "attached":
            return decision("blocked", None, None, "root", "Luna executor model, effort, or attached heartbeat binding is invalid",
                            coordinator_model=current_model)
        return decision("luna_monitor", "gpt-6-luna", "low", "fixed_task_attached_heartbeat",
                        "the authorized fixed Luna task owns monitoring for this verified job",
                        job_id=actual_job["job_id"], thread_id=executor["thread_id"], heartbeat="attached",
                        coordinator_model=current_model)

    if plan_mode and operation != "review":
        return decision("coordinator_decide", current_model, None, "root",
                        "plan mode returns a coordinator plan and starts no implementation",
                        coordinator_model=current_model, implementation_started=False)

    revision = request.get("revision")
    packet = request.get("execution_packet")
    packet_hash = None
    if isinstance(packet, dict) and not missing_execution_fields(packet):
        packet_hash = canonical_execution_revision(packet)
    if not isinstance(revision, str) or not revision.strip():
        return decision("blocked", None, None, "root", "revision is required to bind review and execution",
                        coordinator_model=current_model)
    if kind in {"judgment", "review"} and operation == "implementation":
        return decision("coordinator_decide", current_model, None, "root", "judgment and review requests do not authorize implementation",
                        coordinator_model=current_model, revision=revision)
    if packet_hash is not None and revision != packet_hash:
        return decision("blocked", None, None, "root", "revision does not match canonical execution packet hash",
                        coordinator_model=current_model, revision=revision, expected_revision=packet_hash)
    reviewed_revision = request.get("reviewed_revision")
    receipt = request.get("review_receipt")
    receipt_ok = verify_review_receipt(receipt, revision)
    if reviewed_revision != revision or not receipt_ok:
        if request.get("externalizable") is not True:
            return decision("blocked", None, None, "root", "review material is not authorized for external review",
                            coordinator_model=current_model, revision=revision)
        if request.get("grok_available") is False or request.get("grok_hard_limited") is True:
            return decision("blocked", None, None, "root", "Grok unavailable or hard-limited; no model substitution",
                            coordinator_model=current_model, revision=revision)
        return decision("grok_review", "grok-4.7", "xhigh", "isolated_cli",
                        "first review this exact revision; completion alone is not acceptance",
                        zone=grok_zone, attempts=1, revision=revision, coordinator_model=current_model,
                        write_access=False)

    adjudication = request.get("adjudication")
    if not isinstance(adjudication, dict) or adjudication.get("revision") != revision or adjudication.get("status") != "accepted":
        return decision("coordinator_decide", current_model, None, "root",
                        "coordinator must adjudicate the verified review for this revision",
                        coordinator_model=current_model, revision=revision)

    if operation == "review":
        return decision("coordinator_decide", current_model, None, "root",
                        "read-only review completed; coordinator records its disposition without implementation",
                        coordinator_model=current_model, revision=revision)

    missing = missing_execution_fields(packet)
    if missing:
        return decision("blocked", None, None, "root", "execution packet is incomplete",
                        coordinator_model=current_model, revision=revision, missing_fields=missing)

    if request.get("current_step_authorized") is not True:
        return decision("coordinator_decide", current_model, None, "root", "current implementation step is not explicitly authorized",
                        coordinator_model=current_model, revision=revision)
    if request.get("stop_requested") is True or request.get("scientific_failed") is True:
        return decision("coordinator_decide", current_model, None, "root", "stop or scientific failure prevents automatic re-execution",
                        coordinator_model=current_model, revision=revision)

    requested_model = explicit or "luna"
    configured = {"luna": "gpt-6-luna", "gemini": "gemini-3.8-flash-high", "mimo": "mimo-v2.6"}
    model = configured.get(requested_model)
    effort = "low" if requested_model == "luna" else ("medium" if requested_model == "mimo" else "high")
    if model is None:
        return decision("blocked", None, None, "root", "Grok is review-only and cannot execute repository changes",
                        coordinator_model=current_model, revision=revision)
    available_key = requested_model + "_available"
    hard_key = requested_model + "_hard_limited"
    remaining = request.get(requested_model + "_remaining_percent") if requested_model in {"gemini", "mimo"} else request.get("codex_remaining_percent")
    zone = quota_zone(remaining) if requested_model != "luna" else codex_zone
    if request.get(available_key) is False or request.get(hard_key) is True:
        return decision("blocked", None, None, "root", f"{model} unavailable or hard-limited; no model substitution",
                        coordinator_model=current_model, revision=revision)
    if requested_model == "gemini" and request.get("externalizable") is not True:
        return decision("blocked", None, None, "root", "Gemini execution requires explicitly externalizable material",
                        coordinator_model=current_model, revision=revision)
    if requested_model == "luna":
        executor = request.get("executor_binding")
        if request.get("executor_authorized") is not True:
            return decision("coordinator_decide", current_model, None, "root", "user authorization is required before dispatching to the fixed Luna task",
                            coordinator_model=current_model, revision=revision)
        if not isinstance(executor, dict) or executor.get("thread_id") != request.get("fixed_luna_thread_id") or not _present(request.get("fixed_luna_thread_id")):
            return decision("coordinator_decide", current_model, None, "root", "bind the fixed Luna execution task before dispatch",
                            coordinator_model=current_model, revision=revision)
        if executor.get("model") != model or executor.get("reasoning_effort") != effort:
            return decision("blocked", None, None, "root", "Luna executor model or effort binding is invalid",
                            coordinator_model=current_model, revision=revision)
        execution = "fixed_codex_task"
    else:
        execution = "codex_collaboration" if requested_model == "mimo" else "isolated_cli"
        if operation == "review":
            return decision("coordinator_decide", current_model, None, "root", "review-only request is not an implementation dispatch",
                            coordinator_model=current_model, revision=revision)
    return decision("luna_execute" if requested_model == "luna" else requested_model + "_execute",
                    model, effort, execution,
                    "review receipt, adjudication, and complete execution packet match this revision",
                    zone=zone, attempts=1, revision=revision, coordinator_model=current_model,
                    execution_packet_hash=packet_hash,
                    execution_packet_fields=list(EXECUTION_FIELDS))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="JSON string; defaults to stdin")
    args = parser.parse_args()
    request = json.loads(args.input if args.input is not None else sys.stdin.read())
    print(json.dumps(route(request), ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False))
        raise SystemExit(2)
