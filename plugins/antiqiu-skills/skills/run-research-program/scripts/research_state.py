#!/usr/bin/env python3
"""Durable, replayable state for evidence-gated research programs.

The event ledger is authoritative.  ``project.json`` is only an atomic,
rebuildable snapshot.  Every mutation is serialized by an exclusive lock and
recorded as one immutable JSON event whose SHA-256 includes the preceding event
hash.  The module intentionally uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import socket
import sys
import tempfile
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Optional, Sequence
from urllib.parse import urlparse


FORMAT_VERSION = 1
STATE_DIR_NAME = ".research-program"
EVENT_DIR_NAME = "events"
SNAPSHOT_NAME = "project.json"
LOCK_NAME = ".lock"

STAGES = (
    "framing",
    "literature",
    "protocol",
    "implementation",
    "experimentation",
    "analysis",
    "manuscript",
    "audit",
    "release",
)
STAGE_INDEX = {stage: index for index, stage in enumerate(STAGES)}
TASK_STATUSES = {
    "pending",
    "ready",
    "in_progress",
    "completed",
    "blocked",
    "failed",
    "superseded",
}
MATURITIES = ("candidate", "sourced", "verified")
ACTOR_KINDS = ("automation", "human", "independent")
GATE_DECISIONS = ("passed", "failed", "waived")
# A routine pilot is an execution stage, not automatically a human decision.
HUMAN_GATES = {"adopted"}
HUMAN_GATES |= {
    "ethics",
    "authorship",
    "submission",
    "publication",
    "release",
    "release_approval",
    "release_decision",
    "human_release",
    "human_release_decision",
}
RELEASE_GATES = {
    "release",
    "release_approval",
    "release_decision",
    "human_release",
    "human_release_decision",
}
RELEASE_REQUIRED_STAGES = {
    "framing",
    "literature",
    "protocol",
    "analysis",
    "manuscript",
    "audit",
}
INDEPENDENT_REVIEW_KINDS = {
    "independent-review",
    "release-audit",
    "review",
    "review-report",
}
ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


class ResearchStateError(RuntimeError):
    """Base class for expected state-engine failures."""


class ValidationError(ResearchStateError):
    """An input or stored-state invariant was violated."""


class ConflictError(ResearchStateError):
    """A request or state transition conflicts with prior state."""


class NotFoundError(ResearchStateError):
    """A requested entity does not exist."""


class LockError(ResearchStateError):
    """Another process owns the project mutation lock."""


class LedgerError(ResearchStateError):
    """The immutable event ledger is missing, malformed, or corrupted."""


@dataclass(frozen=True)
class ProjectPaths:
    root: Path
    state_dir: Path
    events_dir: Path
    snapshot: Path
    lock: Path


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:16]}"


def _project_paths(project: os.PathLike[str] | str, *, must_exist: bool) -> ProjectPaths:
    raw = Path(project).expanduser()
    if must_exist and not raw.exists():
        raise NotFoundError(f"project directory does not exist: {raw}")
    root = raw.resolve()
    if must_exist and not root.is_dir():
        raise ValidationError(f"project path is not a directory: {root}")
    state_dir = root / STATE_DIR_NAME
    paths = ProjectPaths(
        root=root,
        state_dir=state_dir,
        events_dir=state_dir / EVENT_DIR_NAME,
        snapshot=state_dir / SNAPSHOT_NAME,
        lock=state_dir / LOCK_NAME,
    )
    for label, candidate in (
        ("state directory", paths.state_dir),
        ("event directory", paths.events_dir),
        ("snapshot", paths.snapshot),
        ("lock", paths.lock),
    ):
        if candidate.is_symlink():
            raise ValidationError(f"{label} must not be a symbolic link: {candidate}")
    if paths.state_dir.exists() and not paths.state_dir.is_dir():
        raise ValidationError(f"state path is not a directory: {paths.state_dir}")
    if paths.events_dir.exists() and not paths.events_dir.is_dir():
        raise ValidationError(f"event path is not a directory: {paths.events_dir}")
    return paths


def _is_within(root: Path, candidate: Path) -> bool:
    try:
        common = os.path.commonpath(
            [os.path.normcase(str(root)), os.path.normcase(str(candidate))]
        )
    except ValueError:
        return False
    return common == os.path.normcase(str(root))


def _validate_id(value: str, label: str) -> str:
    value = value.strip()
    if not ID_PATTERN.fullmatch(value):
        raise ValidationError(
            f"{label} must start with an alphanumeric character and contain only "
            "letters, numbers, '.', '_' or '-' (maximum 128 characters)"
        )
    return value


def _nonempty(value: str, label: str) -> str:
    value = value.strip()
    if not value:
        raise ValidationError(f"{label} must not be empty")
    return value


def _normalize_actor(name: str, kind: str) -> dict[str, str]:
    name = _nonempty(name, "actor")
    if kind not in ACTOR_KINDS:
        raise ValidationError(f"actor kind must be one of: {', '.join(ACTOR_KINDS)}")
    return {"name": name, "kind": kind}


def _normalize_request_id(request_id: Optional[str]) -> Optional[str]:
    if request_id is None:
        return None
    return _validate_id(request_id, "request id")


def _file_descriptor(root: Path, value: os.PathLike[str] | str) -> dict[str, Any]:
    raw = Path(value).expanduser()
    candidate = raw if raw.is_absolute() else root / raw
    try:
        resolved = candidate.resolve(strict=True)
    except FileNotFoundError as exc:
        raise ValidationError(f"artifact file does not exist: {value}") from exc
    if not _is_within(root, resolved):
        raise ValidationError(f"file escapes project root: {value}")
    if not resolved.is_file():
        raise ValidationError(f"artifact must be a regular file: {value}")
    relative = resolved.relative_to(root).as_posix()
    return {
        "path": relative,
        "sha256": _sha256_file(resolved),
        "size": resolved.stat().st_size,
    }


def _validate_locator(locator: str) -> str:
    locator = _nonempty(locator, "evidence locator")
    parsed = urlparse(locator)
    if parsed.scheme and parsed.scheme.lower() in {"http", "https", "doi", "urn"}:
        return locator
    # Opaque identifiers and citations are accepted. Filesystem access is only
    # enabled by the explicit --file flag, where containment is enforced.
    return locator


def _atomic_write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
    )
    temp_path = Path(temp_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, ensure_ascii=False, sort_keys=True, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
        if os.name != "nt":
            directory_fd = os.open(str(path.parent), os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
    finally:
        if temp_path.exists():
            temp_path.unlink()


class ProjectLock:
    """A fail-fast OS advisory lock released automatically on process exit."""

    def __init__(self, path: Path):
        self.path = path
        self._descriptor: Optional[int] = None

    @staticmethod
    def _lock(descriptor: int) -> None:
        if os.name == "nt":
            import msvcrt

            os.lseek(descriptor, 0, os.SEEK_SET)
            msvcrt.locking(descriptor, msvcrt.LK_NBLCK, 1)
        else:
            import fcntl

            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)

    @staticmethod
    def _unlock(descriptor: int) -> None:
        if os.name == "nt":
            import msvcrt

            os.lseek(descriptor, 0, os.SEEK_SET)
            msvcrt.locking(descriptor, msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(descriptor, fcntl.LOCK_UN)

    def __enter__(self) -> "ProjectLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        flags = os.O_CREAT | os.O_RDWR
        descriptor = os.open(str(self.path), flags, 0o600)
        try:
            if os.fstat(descriptor).st_size == 0:
                os.write(descriptor, b"\0")
                os.fsync(descriptor)
            self._lock(descriptor)
        except OSError as exc:
            owner = "unknown"
            try:
                owner_data = json.loads(self.path.read_text(encoding="utf-8"))
                owner = f"pid={owner_data.get('pid', 'unknown')} host={owner_data.get('host', 'unknown')}"
            except (OSError, ValueError):
                pass
            os.close(descriptor)
            raise LockError(
                f"project is locked ({owner}); retry after the owning process exits"
            ) from exc
        try:
            record = {
                "pid": os.getpid(),
                "host": socket.gethostname(),
                "acquired_at": _utc_now(),
            }
            encoded = _canonical_bytes(record) + b"\n"
            os.lseek(descriptor, 0, os.SEEK_SET)
            os.write(descriptor, encoded)
            os.ftruncate(descriptor, len(encoded))
            os.fsync(descriptor)
            os.lseek(descriptor, 0, os.SEEK_SET)
        except BaseException:
            try:
                self._unlock(descriptor)
            except OSError:
                pass
            os.close(descriptor)
            raise
        self._descriptor = descriptor
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        if self._descriptor is not None:
            descriptor = self._descriptor
            self._descriptor = None
            try:
                self._unlock(descriptor)
            finally:
                os.close(descriptor)


def _blank_state() -> dict[str, Any]:
    return {
        "_last_sequence": 0,
        "project": None,
        "tasks": {},
        "claims": {},
        "evidence": {},
        "gates": {},
        "request_ids": {},
    }


def _refresh_task_readiness(state: dict[str, Any]) -> None:
    tasks = state["tasks"]
    for task in tasks.values():
        if task["status"] not in {"pending", "ready"}:
            continue
        dependencies_complete = all(
            tasks.get(dependency, {}).get("status") == "completed"
            for dependency in task["dependencies"]
        )
        task["status"] = "ready" if dependencies_complete else "pending"


def _apply_event(state: dict[str, Any], event: Mapping[str, Any]) -> None:
    event_type = event["event_type"]
    payload = event["payload"]
    occurred_at = event["occurred_at"]
    sequence = event["sequence"]

    if event_type == "project_initialized":
        if state["project"] is not None:
            raise LedgerError("ledger contains more than one project initialization")
        state["project"] = copy.deepcopy(payload["project"])
    elif state["project"] is None:
        raise LedgerError("first ledger event must initialize the project")
    elif event_type == "task_added":
        task = copy.deepcopy(payload["task"])
        if task["id"] in state["tasks"]:
            raise LedgerError(f"duplicate task id in ledger: {task['id']}")
        task.setdefault("gap_key", f"legacy:{task['id']}")
        task.setdefault("priority", 50)
        state["tasks"][task["id"]] = task
    elif event_type == "task_started":
        task = state["tasks"][payload["task_id"]]
        if payload["resume"] and task["status"] == "in_progress":
            if not task["attempts"] or task["attempts"][-1]["ended_at"] is not None:
                raise LedgerError("in-progress task has no resumable attempt")
            task["attempts"][-1].setdefault("resumes", []).append(
                {
                    "recorded_at": occurred_at,
                    "actor": copy.deepcopy(event["actor"]),
                    "reason": payload.get("reason"),
                    "event_sequence": sequence,
                }
            )
        else:
            task["attempts"].append(
                {
                    "id": payload.get("attempt_id", f"attempt_{sequence:012d}"),
                    "started_at": occurred_at,
                    "ended_at": None,
                    "outcome": None,
                    "actor": copy.deepcopy(event["actor"]),
                    "resume": payload["resume"],
                    "reason": payload.get("reason"),
                    "resumes": [],
                    "event_sequence": sequence,
                }
            )
        task["status"] = "in_progress"
    elif event_type == "task_completed":
        task = state["tasks"][payload["task_id"]]
        if task["attempts"] and task["attempts"][-1]["ended_at"] is None:
            task["attempts"][-1]["ended_at"] = occurred_at
            task["attempts"][-1]["outcome"] = "completed"
        task["status"] = "completed"
        task["completed_at"] = occurred_at
        task["artifacts"] = copy.deepcopy(payload["artifacts"])
        task["evidence_ids"] = list(payload["evidence_ids"])
    elif event_type == "task_blocked":
        task = state["tasks"][payload["task_id"]]
        if task["attempts"] and task["attempts"][-1]["ended_at"] is None:
            task["attempts"][-1]["ended_at"] = occurred_at
            task["attempts"][-1]["outcome"] = "blocked"
        task["status"] = "blocked"
        finding = {
            "kind": "blocked_attempt",
            "reason": payload["reason"],
            "recorded_at": occurred_at,
            "actor": copy.deepcopy(event["actor"]),
            "event_sequence": sequence,
        }
        task["negative_findings"].append(finding)
    elif event_type == "claim_added":
        claim = copy.deepcopy(payload["claim"])
        if claim["id"] in state["claims"]:
            raise LedgerError(f"duplicate claim id in ledger: {claim['id']}")
        claim.setdefault("epistemic_state", "active")
        claim.setdefault("contradiction_ids", [])
        state["claims"][claim["id"]] = claim
    elif event_type == "evidence_added":
        evidence = copy.deepcopy(payload["evidence"])
        if evidence["id"] in state["evidence"]:
            raise LedgerError(f"duplicate evidence id in ledger: {evidence['id']}")
        state["evidence"][evidence["id"]] = evidence
        for claim_id in evidence["claim_ids"]:
            claim = state["claims"][claim_id]
            if evidence["id"] not in claim["evidence_ids"]:
                claim["evidence_ids"].append(evidence["id"])
            if evidence["negative"]:
                claim.setdefault("contradiction_ids", []).append(evidence["id"])
                claim["epistemic_state"] = "contested"
    elif event_type == "claim_advanced":
        claim = state["claims"][payload["claim_id"]]
        claim["maturity"] = payload["to"]
        claim["transitions"].append(
            {
                "from": payload["from"],
                "to": payload["to"],
                "evidence_ids": list(payload["evidence_ids"]),
                "actor": copy.deepcopy(event["actor"]),
                "recorded_at": occurred_at,
                "event_sequence": sequence,
            }
        )
    elif event_type == "gate_decided":
        name = payload["gate"]
        prior = state["gates"].get(name)
        history = [] if prior is None else list(prior["history"])
        decision_record = {
            "decision": payload["decision"],
            "actor": copy.deepcopy(event["actor"]),
            "human_approved": payload["human_approved"],
            "evidence_ids": list(payload["evidence_ids"]),
            "reason": payload.get("reason"),
            "recorded_at": occurred_at,
            "event_sequence": sequence,
        }
        history.append(copy.deepcopy(decision_record))
        state["gates"][name] = {
            "name": name,
            **decision_record,
            "history": history,
        }
        if (
            name.casefold() in RELEASE_GATES
            and payload["decision"] == "passed"
            and event["actor"]["kind"] == "human"
            and payload["human_approved"]
        ):
            state["project"]["completed"] = True
            state["project"]["completed_at"] = occurred_at
    else:
        raise LedgerError(f"unknown event type: {event_type}")

    request = event.get("request")
    if request is not None:
        request_id = request["id"]
        if request_id in state["request_ids"]:
            raise LedgerError(f"request id appears in more than one event: {request_id}")
        state["request_ids"][request_id] = {
            "command": request["command"],
            "fingerprint": request["fingerprint"],
            "result": copy.deepcopy(event["result"]),
            "event_sequence": sequence,
            "event_hash": event["event_hash"],
        }

    state["_last_sequence"] = sequence
    _refresh_task_readiness(state)


def _event_files(paths: ProjectPaths) -> list[Path]:
    if not paths.events_dir.exists():
        return []
    return sorted(paths.events_dir.glob("*.json"), key=lambda path: path.name)


def _replay(paths: ProjectPaths) -> tuple[dict[str, Any], int, Optional[str]]:
    state = _blank_state()
    previous_hash: Optional[str] = None
    expected_sequence = 1
    for path in _event_files(paths):
        expected_name = f"{expected_sequence:012d}.json"
        if path.name != expected_name:
            raise LedgerError(
                f"event sequence is not contiguous: expected {expected_name}, found {path.name}"
            )
        try:
            event = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise LedgerError(f"cannot read event {path.name}: {exc}") from exc
        if not isinstance(event, dict):
            raise LedgerError(f"event {path.name} is not a JSON object")
        required = {
            "schema_version",
            "sequence",
            "event_id",
            "event_type",
            "occurred_at",
            "actor",
            "request",
            "payload",
            "result",
            "previous_hash",
            "event_hash",
        }
        missing = sorted(required - set(event))
        if missing:
            raise LedgerError(f"event {path.name} is missing: {', '.join(missing)}")
        if event["schema_version"] != FORMAT_VERSION:
            raise LedgerError(f"unsupported event schema in {path.name}")
        if event["sequence"] != expected_sequence:
            raise LedgerError(f"event sequence mismatch in {path.name}")
        if event["previous_hash"] != previous_hash:
            raise LedgerError(f"previous hash mismatch in {path.name}")
        unhashed = dict(event)
        recorded_hash = unhashed.pop("event_hash")
        calculated_hash = _sha256_bytes(_canonical_bytes(unhashed))
        if recorded_hash != calculated_hash:
            raise LedgerError(f"event hash mismatch in {path.name}")
        _apply_event(state, event)
        previous_hash = recorded_hash
        expected_sequence += 1
    return state, expected_sequence - 1, previous_hash


def _snapshot_document(
    state: Mapping[str, Any], sequence: int, event_hash: Optional[str]
) -> dict[str, Any]:
    return {
        "format_version": FORMAT_VERSION,
        "last_sequence": sequence,
        "last_event_hash": event_hash,
        "state_hash": _sha256_bytes(_canonical_bytes(state)),
        "state": copy.deepcopy(state),
    }


def _read_snapshot(path: Path) -> Optional[dict[str, Any]]:
    if not path.exists():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return value if isinstance(value, dict) else None


def _load_locked(
    paths: ProjectPaths, *, repair_snapshot: bool = True
) -> tuple[dict[str, Any], int, Optional[str], bool]:
    state, sequence, event_hash = _replay(paths)
    if sequence == 0:
        raise NotFoundError(f"research state is not initialized in {paths.root}")
    expected = _snapshot_document(state, sequence, event_hash)
    recorded = _read_snapshot(paths.snapshot)
    recovered = recorded != expected
    if recovered and repair_snapshot:
        _atomic_write_json(paths.snapshot, expected)
    return state, sequence, event_hash, recovered


def _request_fingerprint(command: str, arguments: Mapping[str, Any]) -> str:
    return _sha256_bytes(_canonical_bytes({"command": command, "arguments": arguments}))


def _existing_request(
    state: Mapping[str, Any], request_id: Optional[str], fingerprint: str
) -> Optional[dict[str, Any]]:
    if request_id is None:
        return None
    recorded = state["request_ids"].get(request_id)
    if recorded is None:
        return None
    if recorded["fingerprint"] != fingerprint:
        raise ConflictError(
            f"request id {request_id!r} was already used with different arguments"
        )
    return copy.deepcopy(recorded["result"])


def _append_event(
    paths: ProjectPaths,
    state: dict[str, Any],
    sequence: int,
    previous_hash: Optional[str],
    *,
    event_type: str,
    payload: Mapping[str, Any],
    result: Mapping[str, Any],
    actor: Mapping[str, str],
    command: str,
    request_id: Optional[str],
    fingerprint: str,
) -> dict[str, Any]:
    next_sequence = sequence + 1
    request = None
    if request_id is not None:
        request = {
            "id": request_id,
            "command": command,
            "fingerprint": fingerprint,
        }
    event: dict[str, Any] = {
        "schema_version": FORMAT_VERSION,
        "sequence": next_sequence,
        "event_id": _new_id("evt"),
        "event_type": event_type,
        "occurred_at": _utc_now(),
        "actor": dict(actor),
        "request": request,
        "payload": copy.deepcopy(payload),
        "result": copy.deepcopy(result),
        "previous_hash": previous_hash,
    }
    event["event_hash"] = _sha256_bytes(_canonical_bytes(event))
    target = paths.events_dir / f"{next_sequence:012d}.json"
    if target.exists():
        raise LedgerError(f"refusing to overwrite immutable event: {target.name}")
    _atomic_write_json(target, event)
    _apply_event(state, event)
    _atomic_write_json(
        paths.snapshot,
        _snapshot_document(state, next_sequence, event["event_hash"]),
    )
    return copy.deepcopy(dict(result))


MutationBuilder = Callable[
    [dict[str, Any]], tuple[str, Mapping[str, Any], Mapping[str, Any]]
]


def _mutate(
    project: os.PathLike[str] | str,
    *,
    command: str,
    request_id: Optional[str],
    fingerprint_arguments: Mapping[str, Any],
    actor_name: str,
    actor_kind: str,
    builder: MutationBuilder,
) -> dict[str, Any]:
    paths = _project_paths(project, must_exist=True)
    if not paths.state_dir.exists():
        raise NotFoundError(f"research state is not initialized in {paths.root}")
    actor = _normalize_actor(actor_name, actor_kind)
    request_id = _normalize_request_id(request_id)
    fingerprint = _request_fingerprint(
        command, {**copy.deepcopy(dict(fingerprint_arguments)), "actor": actor}
    )
    with ProjectLock(paths.lock):
        state, sequence, previous_hash, _ = _load_locked(paths)
        duplicate = _existing_request(state, request_id, fingerprint)
        if duplicate is not None:
            return duplicate
        event_type, payload, result = builder(state)
        return _append_event(
            paths,
            state,
            sequence,
            previous_hash,
            event_type=event_type,
            payload=payload,
            result=result,
            actor=actor,
            command=command,
            request_id=request_id,
            fingerprint=fingerprint,
        )


def init_project(
    project: os.PathLike[str] | str,
    *,
    title: str,
    question: str,
    request_id: Optional[str] = None,
    actor: str = "codex",
    actor_kind: str = "automation",
) -> dict[str, Any]:
    title = _nonempty(title, "title")
    question = _nonempty(question, "question")
    actor_record = _normalize_actor(actor, actor_kind)
    request_id = _normalize_request_id(request_id)
    paths = _project_paths(project, must_exist=False)
    paths.root.mkdir(parents=True, exist_ok=True)
    paths.events_dir.mkdir(parents=True, exist_ok=True)
    fingerprint = _request_fingerprint(
        "init", {"title": title, "question": question, "actor": actor_record}
    )
    with ProjectLock(paths.lock):
        state, sequence, previous_hash = _replay(paths)
        if sequence:
            duplicate = _existing_request(state, request_id, fingerprint)
            if duplicate is not None:
                # Also repairs a missing/stale snapshot after a committed init.
                expected = _snapshot_document(state, sequence, previous_hash)
                if _read_snapshot(paths.snapshot) != expected:
                    _atomic_write_json(paths.snapshot, expected)
                return duplicate
            raise ConflictError(f"research state is already initialized in {paths.root}")
        project_id = _new_id("project")
        project_record = {
            "id": project_id,
            "title": title,
            "question": question,
            "created_at": _utc_now(),
            "completed": False,
        }
        result = {"project_id": project_id, "initialized": True}
        return _append_event(
            paths,
            state,
            sequence,
            previous_hash,
            event_type="project_initialized",
            payload={"project": project_record},
            result=result,
            actor=actor_record,
            command="init",
            request_id=request_id,
            fingerprint=fingerprint,
        )


def get_status(project: os.PathLike[str] | str) -> dict[str, Any]:
    paths = _project_paths(project, must_exist=True)
    with ProjectLock(paths.lock):
        state, sequence, event_hash, recovered = _load_locked(paths)
        document = _snapshot_document(state, sequence, event_hash)
        document["snapshot_recovered"] = recovered
        return document


def replay_project(project: os.PathLike[str] | str) -> dict[str, Any]:
    """Replay the authoritative ledger and repair the snapshot if necessary."""

    return get_status(project)


def next_tasks(
    project: os.PathLike[str] | str, *, limit: int = 1
) -> list[dict[str, Any]]:
    if limit < 1:
        raise ValidationError("limit must be positive")
    document = get_status(project)
    ready = [
        copy.deepcopy(task)
        for task in document["state"]["tasks"].values()
        if task["status"] == "ready"
    ]
    ready.sort(
        key=lambda task: (
            -int(task.get("priority", 50)),
            STAGE_INDEX.get(task["stage"], len(STAGES)),
            task["created_sequence"],
            task["id"],
        )
    )
    return ready[:limit]


def next_action(
    project: os.PathLike[str] | str, *, limit: int = 1
) -> dict[str, Any]:
    """Explain whether a worker should start, resume, wait, or stop."""

    if limit < 1:
        raise ValidationError("limit must be positive")
    document = get_status(project)
    state = document["state"]
    tasks = list(state["tasks"].values())
    in_progress = sorted(
        (copy.deepcopy(item) for item in tasks if item["status"] == "in_progress"),
        key=lambda item: (item["created_sequence"], item["id"]),
    )
    if in_progress:
        return {
            "status": "resume",
            "reason": "an attempt is already in progress and must be explicitly resumed or blocked",
            "tasks": in_progress[:limit],
            "snapshot_recovered": document["snapshot_recovered"],
        }
    ready = next_tasks(project, limit=limit)
    if ready:
        withheld = [
            {
                "id": item["id"],
                "status": item["status"],
                "waiting_on": [
                    dependency
                    for dependency in item["dependencies"]
                    if state["tasks"][dependency]["status"] != "completed"
                ],
            }
            for item in tasks
            if item["status"] == "pending"
        ]
        return {
            "status": "ready",
            "reason": "the task's explicit dependencies are satisfied",
            "tasks": ready,
            "withheld": withheld,
            "snapshot_recovered": document["snapshot_recovered"],
        }
    release = next(
        (
            gate
            for name, gate in state["gates"].items()
            if name.casefold() in RELEASE_GATES and gate["decision"] == "passed"
        ),
        None,
    )
    if state["project"].get("completed") and release is not None:
        release_errors = _release_readiness_errors(
            state, release.get("evidence_ids", [])
        )
        if release_errors:
            return {
                "status": "invalid",
                "reason": "release state violates readiness gates: "
                + "; ".join(release_errors),
                "tasks": [],
                "snapshot_recovered": document["snapshot_recovered"],
            }
        return {
            "status": "complete",
            "reason": "all work is complete and a human release gate is recorded",
            "tasks": [],
            "snapshot_recovered": document["snapshot_recovered"],
        }
    if not tasks:
        return {
            "status": "ready",
            "reason": "task_graph_empty; seed scoped evidence-gap tasks before execution",
            "tasks": [],
            "snapshot_recovered": document["snapshot_recovered"],
        }
    if all(item["status"] == "completed" for item in tasks):
        release_requested = any(item["stage"] == "release" for item in tasks) or any(
            name.casefold() in RELEASE_GATES for name in state["gates"]
        )
        return {
            "status": "awaiting_gate" if release_requested else "checkpoint",
            "reason": (
                "recorded release work is complete; the applicable release decision remains"
                if release_requested
                else "registered research tasks are complete; consult the current objective for the next scientific work"
            ),
            "tasks": [],
            "snapshot_recovered": document["snapshot_recovered"],
        }
    blocked = [
        copy.deepcopy(item)
        for item in tasks
        if item["status"] in {"blocked", "failed"}
    ]
    return {
        "status": "blocked",
        "reason": "no task is ready; resolve the recorded blockers or failed dependencies",
        "tasks": blocked[:limit],
        "snapshot_recovered": document["snapshot_recovered"],
    }


def _assert_acyclic(tasks: Mapping[str, Mapping[str, Any]]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(task_id: str) -> None:
        if task_id in visiting:
            raise ValidationError(f"task dependency cycle includes {task_id}")
        if task_id in visited:
            return
        visiting.add(task_id)
        task = tasks[task_id]
        for dependency in task["dependencies"]:
            if dependency not in tasks:
                raise ValidationError(
                    f"task {task_id} depends on unknown task {dependency}"
                )
            visit(dependency)
        visiting.remove(task_id)
        visited.add(task_id)

    for candidate in tasks:
        visit(candidate)


def add_task(
    project: os.PathLike[str] | str,
    *,
    title: str,
    stage: str,
    acceptance: Sequence[str],
    gap_key: str,
    priority: int = 50,
    dependencies: Sequence[str] = (),
    task_id: Optional[str] = None,
    request_id: Optional[str] = None,
    actor: str = "codex",
    actor_kind: str = "automation",
) -> dict[str, Any]:
    title = _nonempty(title, "task title")
    gap_key = _nonempty(gap_key, "evidence gap key")
    if len(gap_key) > 256:
        raise ValidationError("evidence gap key must not exceed 256 characters")
    if isinstance(priority, bool) or not isinstance(priority, int) or not 0 <= priority <= 100:
        raise ValidationError("task priority must be an integer from 0 through 100")
    if stage not in STAGES:
        raise ValidationError(f"stage must be one of: {', '.join(STAGES)}")
    acceptance_values = [_nonempty(item, "acceptance criterion") for item in acceptance]
    if not acceptance_values:
        raise ValidationError("at least one acceptance criterion is required")
    dependency_values = sorted(
        {_validate_id(item, "dependency task id") for item in dependencies}
    )
    if task_id is not None:
        task_id = _validate_id(task_id, "task id")
    fingerprint_arguments = {
        "title": title,
        "stage": stage,
        "acceptance": acceptance_values,
        "dependencies": dependency_values,
        "task_id": task_id,
        "gap_key": gap_key,
        "priority": priority,
    }

    def build(state: dict[str, Any]) -> tuple[str, Mapping[str, Any], Mapping[str, Any]]:
        actual_id = task_id or _new_id("task")
        if actual_id in state["tasks"]:
            raise ConflictError(f"task already exists: {actual_id}")
        if any(item.get("gap_key") == gap_key for item in state["tasks"].values()):
            raise ConflictError(f"evidence gap key already exists: {gap_key}")
        missing = [item for item in dependency_values if item not in state["tasks"]]
        if missing:
            raise NotFoundError(f"unknown dependency tasks: {', '.join(missing)}")
        if actual_id in dependency_values:
            raise ValidationError("task cannot depend on itself")
        task = {
            "id": actual_id,
            "title": title,
            "stage": stage,
            "acceptance": list(acceptance_values),
            "gap_key": gap_key,
            "priority": priority,
            "dependencies": list(dependency_values),
            "status": "pending",
            "created_sequence": _current_sequence(state) + 1,
            "attempts": [],
            "artifacts": [],
            "evidence_ids": [],
            "negative_findings": [],
            "completed_at": None,
        }
        prospective = dict(state["tasks"])
        prospective[actual_id] = task
        _assert_acyclic(prospective)
        return "task_added", {"task": task}, {"task_id": actual_id}

    return _mutate(
        project,
        command="add-task",
        request_id=request_id,
        fingerprint_arguments=fingerprint_arguments,
        actor_name=actor,
        actor_kind=actor_kind,
        builder=build,
    )


def _current_sequence(state: Mapping[str, Any]) -> int:
    # Event sequence is stored on every request and entity creation.  Builders
    # only need a stable ordering hint; the exact event number is filled by the
    # maximum known sequence plus one.
    if "_last_sequence" in state:
        return int(state["_last_sequence"])
    sequences = [entry["event_sequence"] for entry in state["request_ids"].values()]
    for task in state["tasks"].values():
        sequences.append(int(task.get("created_sequence", 0)))
        sequences.extend(
            int(attempt.get("event_sequence", 0)) for attempt in task["attempts"]
        )
    for claim in state["claims"].values():
        sequences.append(int(claim.get("created_sequence", 0)))
        sequences.extend(
            int(transition.get("event_sequence", 0))
            for transition in claim["transitions"]
        )
    for evidence in state["evidence"].values():
        sequences.append(int(evidence.get("created_sequence", 0)))
    for gate in state["gates"].values():
        sequences.extend(int(item["event_sequence"]) for item in gate["history"])
    return max(sequences, default=1)


def start_task(
    project: os.PathLike[str] | str,
    *,
    task_id: str,
    resume: bool = False,
    reason: Optional[str] = None,
    request_id: Optional[str] = None,
    actor: str = "codex",
    actor_kind: str = "automation",
) -> dict[str, Any]:
    task_id = _validate_id(task_id, "task id")
    reason = reason.strip() if reason is not None else None
    if resume and not reason:
        raise ValidationError("resuming a blocked task requires a reason")

    def build(state: dict[str, Any]) -> tuple[str, Mapping[str, Any], Mapping[str, Any]]:
        task = state["tasks"].get(task_id)
        if task is None:
            raise NotFoundError(f"unknown task: {task_id}")
        allowed = {"blocked", "in_progress"} if resume else {"ready"}
        if task["status"] not in allowed:
            raise ConflictError(
                f"task {task_id} is {task['status']}; expected one of {', '.join(sorted(allowed))}"
            )
        if resume and not all(
            state["tasks"][dependency]["status"] == "completed"
            for dependency in task["dependencies"]
        ):
            raise ConflictError("blocked task dependencies are no longer complete")
        continuing = resume and task["status"] == "in_progress"
        attempt_id = (
            task["attempts"][-1]["id"]
            if continuing
            else _new_id("attempt")
        )
        payload = {
            "task_id": task_id,
            "resume": resume,
            "reason": reason,
            "attempt_id": attempt_id,
        }
        return "task_started", payload, {
            "task_id": task_id,
            "attempt_id": attempt_id,
            "status": "in_progress",
            "resumed": continuing,
        }

    return _mutate(
        project,
        command="start",
        request_id=request_id,
        fingerprint_arguments={"task_id": task_id, "resume": resume, "reason": reason},
        actor_name=actor,
        actor_kind=actor_kind,
        builder=build,
    )


def complete_task(
    project: os.PathLike[str] | str,
    *,
    task_id: str,
    artifacts: Sequence[os.PathLike[str] | str],
    evidence_ids: Sequence[str] = (),
    request_id: Optional[str] = None,
    actor: str = "codex",
    actor_kind: str = "automation",
) -> dict[str, Any]:
    task_id = _validate_id(task_id, "task id")
    paths = _project_paths(project, must_exist=True)
    artifact_records = sorted(
        (_file_descriptor(paths.root, item) for item in artifacts),
        key=lambda item: item["path"],
    )
    if not artifact_records:
        raise ValidationError("completing a task requires at least one artifact")
    evidence_values = sorted(
        {_validate_id(item, "evidence id") for item in evidence_ids}
    )

    def build(state: dict[str, Any]) -> tuple[str, Mapping[str, Any], Mapping[str, Any]]:
        task = state["tasks"].get(task_id)
        if task is None:
            raise NotFoundError(f"unknown task: {task_id}")
        if task["status"] != "in_progress":
            raise ConflictError(
                f"task {task_id} is {task['status']}; expected in_progress"
            )
        missing = [item for item in evidence_values if item not in state["evidence"]]
        if missing:
            raise NotFoundError(f"unknown evidence: {', '.join(missing)}")
        payload = {
            "task_id": task_id,
            "artifacts": artifact_records,
            "evidence_ids": evidence_values,
        }
        return "task_completed", payload, {"task_id": task_id, "status": "completed"}

    return _mutate(
        project,
        command="complete",
        request_id=request_id,
        fingerprint_arguments={
            "task_id": task_id,
            "artifacts": artifact_records,
            "evidence_ids": evidence_values,
        },
        actor_name=actor,
        actor_kind=actor_kind,
        builder=build,
    )


def block_task(
    project: os.PathLike[str] | str,
    *,
    task_id: str,
    reason: str,
    request_id: Optional[str] = None,
    actor: str = "codex",
    actor_kind: str = "automation",
) -> dict[str, Any]:
    task_id = _validate_id(task_id, "task id")
    reason = _nonempty(reason, "block reason")

    def build(state: dict[str, Any]) -> tuple[str, Mapping[str, Any], Mapping[str, Any]]:
        task = state["tasks"].get(task_id)
        if task is None:
            raise NotFoundError(f"unknown task: {task_id}")
        if task["status"] not in {"ready", "in_progress"}:
            raise ConflictError(
                f"task {task_id} is {task['status']}; only ready or in-progress tasks can be blocked"
            )
        payload = {"task_id": task_id, "reason": reason}
        return "task_blocked", payload, {"task_id": task_id, "status": "blocked"}

    return _mutate(
        project,
        command="block",
        request_id=request_id,
        fingerprint_arguments={"task_id": task_id, "reason": reason},
        actor_name=actor,
        actor_kind=actor_kind,
        builder=build,
    )


def add_claim(
    project: os.PathLike[str] | str,
    *,
    text: str,
    independence_key: str,
    mandatory: bool = True,
    claim_id: Optional[str] = None,
    request_id: Optional[str] = None,
    actor: str = "codex",
    actor_kind: str = "automation",
) -> dict[str, Any]:
    text = _nonempty(text, "claim text")
    independence_key = _nonempty(independence_key, "independence key")
    if claim_id is not None:
        claim_id = _validate_id(claim_id, "claim id")

    def build(state: dict[str, Any]) -> tuple[str, Mapping[str, Any], Mapping[str, Any]]:
        actual_id = claim_id or _new_id("claim")
        if actual_id in state["claims"]:
            raise ConflictError(f"claim already exists: {actual_id}")
        claim = {
            "id": actual_id,
            "text": text,
            "mandatory": bool(mandatory),
            "maturity": "candidate",
            "epistemic_state": "active",
            "origin_actor": {"name": actor, "kind": actor_kind},
            "origin_independence_key": independence_key,
            "evidence_ids": [],
            "contradiction_ids": [],
            "transitions": [],
            "created_sequence": _current_sequence(state) + 1,
        }
        return "claim_added", {"claim": claim}, {"claim_id": actual_id}

    return _mutate(
        project,
        command="add-claim",
        request_id=request_id,
        fingerprint_arguments={
            "text": text,
            "independence_key": independence_key,
            "mandatory": bool(mandatory),
            "claim_id": claim_id,
        },
        actor_name=actor,
        actor_kind=actor_kind,
        builder=build,
    )


def add_evidence(
    project: os.PathLike[str] | str,
    *,
    kind: str,
    locator: str,
    independence_key: str,
    claim_ids: Sequence[str] = (),
    is_file: bool = False,
    negative: bool = False,
    finding: Optional[str] = None,
    evidence_id: Optional[str] = None,
    request_id: Optional[str] = None,
    actor: str = "codex",
    actor_kind: str = "automation",
) -> dict[str, Any]:
    kind = _nonempty(kind, "evidence kind")
    independence_key = _nonempty(independence_key, "independence key")
    finding = finding.strip() if finding is not None else None
    if negative and not finding:
        raise ValidationError("negative evidence requires a finding")
    claim_values = sorted({_validate_id(item, "claim id") for item in claim_ids})
    if evidence_id is not None:
        evidence_id = _validate_id(evidence_id, "evidence id")
    file_record: Optional[dict[str, Any]] = None
    if is_file:
        paths = _project_paths(project, must_exist=True)
        file_record = _file_descriptor(paths.root, locator)
        normalized_locator = file_record["path"]
    else:
        normalized_locator = _validate_locator(locator)

    def build(state: dict[str, Any]) -> tuple[str, Mapping[str, Any], Mapping[str, Any]]:
        actual_id = evidence_id or _new_id("evidence")
        if actual_id in state["evidence"]:
            raise ConflictError(f"evidence already exists: {actual_id}")
        missing = [item for item in claim_values if item not in state["claims"]]
        if missing:
            raise NotFoundError(f"unknown claims: {', '.join(missing)}")
        evidence = {
            "id": actual_id,
            "kind": kind,
            "locator": normalized_locator,
            "file": copy.deepcopy(file_record),
            "claim_ids": claim_values,
            "actor": {"name": actor, "kind": actor_kind},
            "actor_kind": actor_kind,
            "independence_key": independence_key,
            "negative": bool(negative),
            "finding": finding,
            "created_sequence": _current_sequence(state) + 1,
        }
        return "evidence_added", {"evidence": evidence}, {"evidence_id": actual_id}

    return _mutate(
        project,
        command="add-evidence",
        request_id=request_id,
        fingerprint_arguments={
            "kind": kind,
            "locator": normalized_locator,
            "file": file_record,
            "claim_ids": claim_values,
            "independence_key": independence_key,
            "negative": bool(negative),
            "finding": finding,
            "evidence_id": evidence_id,
        },
        actor_name=actor,
        actor_kind=actor_kind,
        builder=build,
    )


def _positive_claim_evidence(
    state: Mapping[str, Any], claim: Mapping[str, Any], evidence_ids: Iterable[str]
) -> list[Mapping[str, Any]]:
    attached = set(claim["evidence_ids"])
    selected = []
    for evidence_id in evidence_ids:
        if evidence_id not in state["evidence"]:
            raise NotFoundError(f"unknown evidence: {evidence_id}")
        if evidence_id not in attached:
            raise ValidationError(
                f"evidence {evidence_id} is not attached to claim {claim['id']}"
            )
        evidence = state["evidence"][evidence_id]
        if not evidence["negative"]:
            selected.append(evidence)
    return selected


def advance_claim(
    project: os.PathLike[str] | str,
    *,
    claim_id: str,
    to_maturity: str,
    evidence_ids: Sequence[str],
    request_id: Optional[str] = None,
    actor: str = "codex",
    actor_kind: str = "automation",
) -> dict[str, Any]:
    claim_id = _validate_id(claim_id, "claim id")
    if to_maturity not in MATURITIES[1:]:
        raise ValidationError("target maturity must be sourced or verified")
    evidence_values = sorted(
        {_validate_id(item, "evidence id") for item in evidence_ids}
    )
    if not evidence_values:
        raise ValidationError("advancing a claim requires evidence")
    if actor_kind == "automation" and to_maturity == "verified":
        raise ValidationError("automation may not advance claims beyond sourced")

    def build(state: dict[str, Any]) -> tuple[str, Mapping[str, Any], Mapping[str, Any]]:
        claim = state["claims"].get(claim_id)
        if claim is None:
            raise NotFoundError(f"unknown claim: {claim_id}")
        current_index = MATURITIES.index(claim["maturity"])
        target_index = MATURITIES.index(to_maturity)
        if target_index != current_index + 1:
            raise ConflictError(
                f"claim transition must advance one step; {claim['maturity']} -> {to_maturity} is invalid"
            )
        positive = _positive_claim_evidence(state, claim, evidence_values)
        if not positive:
            raise ValidationError("negative findings cannot support claim advancement")
        if to_maturity == "verified":
            contradictions = [
                evidence_id
                for evidence_id in claim.get("contradiction_ids", [])
                if evidence_id in state["evidence"]
            ]
            if contradictions:
                raise ValidationError(
                    "verified requires every attached contradiction to be resolved; "
                    f"unresolved: {', '.join(contradictions)}"
                )
            independent = [
                evidence
                for evidence in positive
                if evidence["actor_kind"] == "independent"
                and evidence["independence_key"]
                != claim["origin_independence_key"]
            ]
            if not independent:
                raise ValidationError(
                    "verified requires positive evidence from an independent actor "
                    "with a distinct independence key"
                )
            if actor_kind not in {"human", "independent"}:
                raise ValidationError("only a human or independent actor may record verified")
        payload = {
            "claim_id": claim_id,
            "from": claim["maturity"],
            "to": to_maturity,
            "evidence_ids": evidence_values,
        }
        return "claim_advanced", payload, {"claim_id": claim_id, "maturity": to_maturity}

    return _mutate(
        project,
        command="advance-claim",
        request_id=request_id,
        fingerprint_arguments={
            "claim_id": claim_id,
            "to_maturity": to_maturity,
            "evidence_ids": evidence_values,
        },
        actor_name=actor,
        actor_kind=actor_kind,
        builder=build,
    )


def _require_human_gate(
    gate: str,
    decision: str,
    *,
    actor_kind: str,
    human_approved: bool,
    tty: Optional[bool],
) -> None:
    if gate.casefold() not in HUMAN_GATES or decision == "failed":
        return
    # TTY presence is not evidence of consent. Callers may record a real
    # existing human decision from chat or another authorized interface.
    # record_gate still requires evidence; never invent a human decision.
    # Keep tty as a compatibility argument for existing callers.
    if actor_kind != "human" or not human_approved:
        raise ValidationError(
            f"{gate} may pass or be waived only with a recorded human decision "
            "and explicit approval"
        )


def record_gate(
    project: os.PathLike[str] | str,
    *,
    gate: str,
    decision: str,
    evidence_ids: Sequence[str] = (),
    reason: Optional[str] = None,
    human_approved: bool = False,
    tty: Optional[bool] = None,
    request_id: Optional[str] = None,
    actor: str = "codex",
    actor_kind: str = "automation",
) -> dict[str, Any]:
    gate = _validate_id(gate, "gate")
    if decision not in GATE_DECISIONS:
        raise ValidationError(
            f"gate decision must be one of: {', '.join(GATE_DECISIONS)}"
        )
    evidence_values = sorted(
        {_validate_id(item, "evidence id") for item in evidence_ids}
    )
    reason = reason.strip() if reason is not None else None
    _require_human_gate(
        gate,
        decision,
        actor_kind=actor_kind,
        human_approved=human_approved,
        tty=tty,
    )
    if decision in {"passed", "waived"} and not evidence_values:
        raise ValidationError("passing or waiving a gate requires evidence")

    def build(state: dict[str, Any]) -> tuple[str, Mapping[str, Any], Mapping[str, Any]]:
        missing = [item for item in evidence_values if item not in state["evidence"]]
        if missing:
            raise NotFoundError(f"unknown evidence: {', '.join(missing)}")
        if gate.casefold() in RELEASE_GATES and decision == "passed":
            readiness_errors = _release_readiness_errors(state, evidence_values)
            if readiness_errors:
                raise ValidationError(
                    "release gate is not ready: " + "; ".join(readiness_errors)
                )
        payload = {
            "gate": gate,
            "decision": decision,
            "evidence_ids": evidence_values,
            "reason": reason,
            "human_approved": bool(human_approved),
        }
        return "gate_decided", payload, {"gate": gate, "decision": decision}

    return _mutate(
        project,
        command="gate",
        request_id=request_id,
        fingerprint_arguments={
            "gate": gate,
            "decision": decision,
            "evidence_ids": evidence_values,
            "reason": reason,
            "human_approved": bool(human_approved),
        },
        actor_name=actor,
        actor_kind=actor_kind,
        builder=build,
    )


def _release_readiness_errors(
    state: Mapping[str, Any], evidence_ids: Sequence[str]
) -> list[str]:
    errors: list[str] = []
    tasks = state["tasks"]
    if not tasks:
        errors.append("no research tasks are recorded")
    incomplete = sorted(
        task_id for task_id, task in tasks.items() if task["status"] != "completed"
    )
    if incomplete:
        errors.append("incomplete tasks: " + ", ".join(incomplete))
    present_stages = {task["stage"] for task in tasks.values()}
    missing_stages = sorted(RELEASE_REQUIRED_STAGES - present_stages)
    if missing_stages:
        errors.append("missing required stages: " + ", ".join(missing_stages))
    mandatory_claims = [
        claim for claim in state["claims"].values() if claim.get("mandatory", True)
    ]
    if not mandatory_claims:
        errors.append("no mandatory claims are recorded")
    unready_claims = sorted(
        claim["id"]
        for claim in mandatory_claims
        if claim["maturity"] != "verified"
        or claim.get("epistemic_state", "active") != "active"
    )
    if unready_claims:
        errors.append("unverified or contested claims: " + ", ".join(unready_claims))
    review_evidence = [
        state["evidence"][evidence_id]
        for evidence_id in evidence_ids
        if evidence_id in state["evidence"]
        and state["evidence"][evidence_id]["actor_kind"] == "independent"
        and state["evidence"][evidence_id]["kind"].casefold().replace("_", "-")
        in INDEPENDENT_REVIEW_KINDS
    ]
    if not review_evidence:
        errors.append("selected evidence lacks an independent review")
    return errors


def _validate_file_record(root: Path, record: Mapping[str, Any], label: str) -> None:
    path_value = record.get("path")
    if not isinstance(path_value, str) or not path_value:
        raise ValidationError(f"{label} has no relative path")
    candidate = (root / Path(path_value)).resolve()
    if not _is_within(root, candidate):
        raise ValidationError(f"{label} escapes project root")
    if not candidate.is_file():
        raise ValidationError(f"{label} is missing: {path_value}")
    if record.get("sha256") != _sha256_file(candidate):
        raise ValidationError(f"{label} hash changed: {path_value}")
    if record.get("size") != candidate.stat().st_size:
        raise ValidationError(f"{label} size changed: {path_value}")


def _validate_semantics(root: Path, state: Mapping[str, Any]) -> None:
    project = state.get("project")
    if not isinstance(project, dict) or not project.get("id"):
        raise ValidationError("project metadata is missing")
    tasks = state.get("tasks")
    claims = state.get("claims")
    evidence_map = state.get("evidence")
    gates = state.get("gates")
    if not all(isinstance(item, dict) for item in (tasks, claims, evidence_map, gates)):
        raise ValidationError("state collections must be objects")
    _assert_acyclic(tasks)
    gap_keys: set[str] = set()
    for task_id, task in tasks.items():
        if task.get("id") != task_id:
            raise ValidationError(f"task map key mismatch: {task_id}")
        if task.get("stage") not in STAGES:
            raise ValidationError(f"task {task_id} has an unknown stage")
        if task.get("status") not in TASK_STATUSES:
            raise ValidationError(f"task {task_id} has an unknown status")
        gap_key = task.get("gap_key")
        if not isinstance(gap_key, str) or not gap_key.strip():
            raise ValidationError(f"task {task_id} has no evidence gap key")
        if gap_key in gap_keys:
            raise ValidationError(f"duplicate evidence gap key: {gap_key}")
        gap_keys.add(gap_key)
        priority = task.get("priority")
        if isinstance(priority, bool) or not isinstance(priority, int) or not 0 <= priority <= 100:
            raise ValidationError(f"task {task_id} has an invalid priority")
        open_attempts = [
            attempt for attempt in task.get("attempts", []) if attempt.get("ended_at") is None
        ]
        if len(open_attempts) > 1:
            raise ValidationError(f"task {task_id} has more than one active attempt")
        if task["status"] == "in_progress" and len(open_attempts) != 1:
            raise ValidationError(f"task {task_id} has no active attempt")
        if task["status"] != "in_progress" and open_attempts:
            raise ValidationError(f"task {task_id} retains an active attempt while {task['status']}")
        for evidence_id in task.get("evidence_ids", []):
            if evidence_id not in evidence_map:
                raise ValidationError(
                    f"task {task_id} references unknown evidence {evidence_id}"
                )
        if task["status"] == "completed":
            if not task.get("artifacts"):
                raise ValidationError(f"completed task {task_id} has no artifacts")
            for index, artifact in enumerate(task["artifacts"]):
                _validate_file_record(root, artifact, f"task {task_id} artifact {index}")
        if task["status"] == "ready" and not all(
            tasks[dependency]["status"] == "completed"
            for dependency in task["dependencies"]
        ):
            raise ValidationError(f"task {task_id} is ready before its dependencies")
        if task["status"] == "pending" and all(
            tasks[dependency]["status"] == "completed"
            for dependency in task["dependencies"]
        ):
            raise ValidationError(f"task {task_id} should be ready")
    for evidence_id, evidence in evidence_map.items():
        if evidence.get("id") != evidence_id:
            raise ValidationError(f"evidence map key mismatch: {evidence_id}")
        for claim_id in evidence.get("claim_ids", []):
            if claim_id not in claims:
                raise ValidationError(
                    f"evidence {evidence_id} references unknown claim {claim_id}"
                )
            if evidence_id not in claims[claim_id].get("evidence_ids", []):
                raise ValidationError(
                    f"claim {claim_id} does not link back to evidence {evidence_id}"
                )
        if evidence.get("negative") and not evidence.get("finding"):
            raise ValidationError(f"negative evidence {evidence_id} has no finding")
        if evidence.get("file") is not None:
            _validate_file_record(root, evidence["file"], f"evidence {evidence_id}")
    for claim_id, claim in claims.items():
        if claim.get("id") != claim_id:
            raise ValidationError(f"claim map key mismatch: {claim_id}")
        maturity = claim.get("maturity")
        if maturity not in MATURITIES:
            raise ValidationError(f"claim {claim_id} has an unknown maturity")
        epistemic_state = claim.get("epistemic_state", "active")
        if epistemic_state not in {"active", "contested", "retracted"}:
            raise ValidationError(f"claim {claim_id} has an unknown epistemic state")
        contradictions = claim.get("contradiction_ids", [])
        for evidence_id in contradictions:
            if evidence_id not in evidence_map or not evidence_map[evidence_id]["negative"]:
                raise ValidationError(
                    f"claim {claim_id} has an invalid contradiction {evidence_id}"
                )
        if contradictions and epistemic_state != "contested":
            raise ValidationError(f"claim {claim_id} hides unresolved contradictions")
        positive = [
            evidence_map[item]
            for item in claim.get("evidence_ids", [])
            if item in evidence_map and not evidence_map[item]["negative"]
        ]
        if maturity in {"sourced", "verified"} and not positive:
            raise ValidationError(f"{maturity} claim {claim_id} has no positive evidence")
        if maturity == "verified" and not any(
            item["actor_kind"] == "independent"
            and item["independence_key"] != claim["origin_independence_key"]
            for item in positive
        ):
            raise ValidationError(f"verified claim {claim_id} lacks independent evidence")
        expected_from = "candidate"
        for transition in claim.get("transitions", []):
            if transition["from"] != expected_from:
                raise ValidationError(f"claim {claim_id} has a discontinuous transition")
            target = transition["to"]
            if MATURITIES.index(target) != MATURITIES.index(expected_from) + 1:
                raise ValidationError(f"claim {claim_id} skipped a maturity state")
            if target == "verified" and transition["actor"]["kind"] == "automation":
                raise ValidationError(f"automation marked claim {claim_id} verified")
            expected_from = target
        if expected_from != maturity:
            raise ValidationError(f"claim {claim_id} maturity disagrees with transitions")
    for gate_name, gate in gates.items():
        if gate_name.casefold() in HUMAN_GATES and gate["decision"] in {
            "passed",
            "waived",
        }:
            if gate["actor"]["kind"] != "human" or not gate["human_approved"]:
                raise ValidationError(f"gate {gate_name} lacks explicit human approval")
        for evidence_id in gate.get("evidence_ids", []):
            if evidence_id not in evidence_map:
                raise ValidationError(
                    f"gate {gate_name} references unknown evidence {evidence_id}"
                )
    if project.get("completed"):
        release_gates = [
            gate
            for name, gate in gates.items()
            if name.casefold() in RELEASE_GATES and gate["decision"] == "passed"
        ]
        if not release_gates:
            raise ValidationError("completed project lacks a passed release gate")
        release_errors = _release_readiness_errors(
            state, release_gates[-1].get("evidence_ids", [])
        )
        if release_errors:
            raise ValidationError(
                "completed project violates release readiness: "
                + "; ".join(release_errors)
            )


def validate_project(project: os.PathLike[str] | str) -> dict[str, Any]:
    paths = _project_paths(project, must_exist=True)
    with ProjectLock(paths.lock):
        state, sequence, event_hash, recovered = _load_locked(paths)
        _validate_semantics(paths.root, state)
        return {
            "valid": True,
            "snapshot_recovered": recovered,
            "event_count": sequence,
            "last_event_hash": event_hash,
            "state_hash": _sha256_bytes(_canonical_bytes(state)),
            "counts": {
                "tasks": len(state["tasks"]),
                "claims": len(state["claims"]),
                "evidence": len(state["evidence"]),
                "gates": len(state["gates"]),
                "negative_findings": sum(
                    len(task["negative_findings"])
                    for task in state["tasks"].values()
                )
                + sum(
                    1 for evidence in state["evidence"].values() if evidence["negative"]
                ),
            },
        }


def _add_actor_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--actor", default="codex")
    parser.add_argument("--actor-kind", choices=ACTOR_KINDS, default="automation")


def _add_request_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--request-id")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage a resumable, evidence-gated research program"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="initialize an event ledger")
    init.add_argument("--project", required=True)
    init.add_argument("--title", required=True)
    init.add_argument("--question", required=True)
    _add_request_argument(init)
    _add_actor_arguments(init)

    status = subparsers.add_parser("status", help="replay and show project state")
    status.add_argument("--project", required=True)
    status.add_argument("--json", action="store_true")

    next_parser = subparsers.add_parser(
        "next", help="explain whether to start, resume, wait, or stop"
    )
    next_parser.add_argument("--project", required=True)
    next_parser.add_argument("--limit", type=int, default=1)
    next_parser.add_argument("--json", action="store_true")

    add_task_parser = subparsers.add_parser("add-task", help="add a task to the DAG")
    add_task_parser.add_argument("--project", required=True)
    add_task_parser.add_argument("--task-id")
    add_task_parser.add_argument("--title", required=True)
    add_task_parser.add_argument("--stage", choices=STAGES, required=True)
    add_task_parser.add_argument(
        "--gap-key",
        required=True,
        help="unique evidence-gap key that prevents duplicate expansion",
    )
    add_task_parser.add_argument(
        "--priority", type=int, default=50, help="value from 0 through 100"
    )
    add_task_parser.add_argument("--depends-on", action="append", default=[])
    add_task_parser.add_argument("--acceptance", action="append", required=True)
    _add_request_argument(add_task_parser)
    _add_actor_arguments(add_task_parser)

    start = subparsers.add_parser("start", help="start or explicitly resume a task")
    start.add_argument("--project", required=True)
    start.add_argument("--task", required=True)
    start.add_argument(
        "--resume",
        action="store_true",
        help="explicitly resume the active attempt or start a new attempt for a blocked task",
    )
    start.add_argument("--reason", help="required for every explicit resume")
    _add_request_argument(start)
    _add_actor_arguments(start)

    complete = subparsers.add_parser("complete", help="complete a task with artifacts")
    complete.add_argument("--project", required=True)
    complete.add_argument("--task", required=True)
    complete.add_argument("--artifact", action="append", required=True)
    complete.add_argument(
        "--evidence",
        action="append",
        default=[],
        help="existing evidence ID to attach; repeat for multiple IDs",
    )
    _add_request_argument(complete)
    _add_actor_arguments(complete)

    block = subparsers.add_parser("block", help="retain a blocked attempt and reason")
    block.add_argument("--project", required=True)
    block.add_argument("--task", required=True)
    block.add_argument("--reason", required=True)
    _add_request_argument(block)
    _add_actor_arguments(block)

    add_claim_parser = subparsers.add_parser("add-claim", help="add a candidate claim")
    add_claim_parser.add_argument("--project", required=True)
    add_claim_parser.add_argument("--claim-id")
    add_claim_parser.add_argument("--text", required=True)
    add_claim_parser.add_argument("--independence-key", required=True)
    add_claim_parser.add_argument("--optional", action="store_true")
    _add_request_argument(add_claim_parser)
    _add_actor_arguments(add_claim_parser)

    add_evidence_parser = subparsers.add_parser(
        "add-evidence", help="attach positive or negative evidence"
    )
    add_evidence_parser.add_argument("--project", required=True)
    add_evidence_parser.add_argument("--evidence-id")
    add_evidence_parser.add_argument("--kind", required=True)
    add_evidence_parser.add_argument("--locator", required=True)
    add_evidence_parser.add_argument("--file", action="store_true")
    add_evidence_parser.add_argument("--claim", action="append", default=[])
    add_evidence_parser.add_argument("--independence-key", required=True)
    add_evidence_parser.add_argument("--negative", action="store_true")
    add_evidence_parser.add_argument("--finding")
    _add_request_argument(add_evidence_parser)
    _add_actor_arguments(add_evidence_parser)

    advance = subparsers.add_parser(
        "advance-claim", help="advance candidate -> sourced -> verified"
    )
    advance.add_argument("--project", required=True)
    advance.add_argument("--claim", required=True)
    advance.add_argument("--to", dest="to_maturity", choices=MATURITIES[1:], required=True)
    advance.add_argument("--evidence", action="append", required=True)
    _add_request_argument(advance)
    _add_actor_arguments(advance)

    gate = subparsers.add_parser("gate", help="record an evidence-backed gate decision")
    gate.add_argument("--project", required=True)
    gate.add_argument("--gate", required=True)
    gate.add_argument("--decision", choices=GATE_DECISIONS, required=True)
    gate.add_argument("--evidence", action="append", default=[])
    gate.add_argument("--reason")
    gate.add_argument("--human-approved", action="store_true")
    _add_request_argument(gate)
    _add_actor_arguments(gate)

    validate = subparsers.add_parser("validate", help="verify ledger and state invariants")
    validate.add_argument("--project", required=True)
    validate.add_argument("--json", action="store_true")
    return parser


def _print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2))


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            result = init_project(
                args.project,
                title=args.title,
                question=args.question,
                request_id=args.request_id,
                actor=args.actor,
                actor_kind=args.actor_kind,
            )
        elif args.command == "status":
            document = get_status(args.project)
            if args.json:
                _print_json(document)
            else:
                state = document["state"]
                _print_json(
                    {
                        "project": state["project"],
                        "last_sequence": document["last_sequence"],
                        "snapshot_recovered": document["snapshot_recovered"],
                        "counts": {
                            "tasks": len(state["tasks"]),
                            "claims": len(state["claims"]),
                            "evidence": len(state["evidence"]),
                            "gates": len(state["gates"]),
                        },
                    }
                )
            return 0
        elif args.command == "next":
            action = next_action(args.project, limit=args.limit)
            _print_json(action)
            return 0
        elif args.command == "add-task":
            result = add_task(
                args.project,
                task_id=args.task_id,
                title=args.title,
                stage=args.stage,
                gap_key=args.gap_key,
                priority=args.priority,
                dependencies=args.depends_on,
                acceptance=args.acceptance,
                request_id=args.request_id,
                actor=args.actor,
                actor_kind=args.actor_kind,
            )
        elif args.command == "start":
            result = start_task(
                args.project,
                task_id=args.task,
                resume=args.resume,
                reason=args.reason,
                request_id=args.request_id,
                actor=args.actor,
                actor_kind=args.actor_kind,
            )
        elif args.command == "complete":
            result = complete_task(
                args.project,
                task_id=args.task,
                artifacts=args.artifact,
                evidence_ids=args.evidence,
                request_id=args.request_id,
                actor=args.actor,
                actor_kind=args.actor_kind,
            )
        elif args.command == "block":
            result = block_task(
                args.project,
                task_id=args.task,
                reason=args.reason,
                request_id=args.request_id,
                actor=args.actor,
                actor_kind=args.actor_kind,
            )
        elif args.command == "add-claim":
            result = add_claim(
                args.project,
                claim_id=args.claim_id,
                text=args.text,
                independence_key=args.independence_key,
                mandatory=not args.optional,
                request_id=args.request_id,
                actor=args.actor,
                actor_kind=args.actor_kind,
            )
        elif args.command == "add-evidence":
            result = add_evidence(
                args.project,
                evidence_id=args.evidence_id,
                kind=args.kind,
                locator=args.locator,
                is_file=args.file,
                claim_ids=args.claim,
                independence_key=args.independence_key,
                negative=args.negative,
                finding=args.finding,
                request_id=args.request_id,
                actor=args.actor,
                actor_kind=args.actor_kind,
            )
        elif args.command == "advance-claim":
            result = advance_claim(
                args.project,
                claim_id=args.claim,
                to_maturity=args.to_maturity,
                evidence_ids=args.evidence,
                request_id=args.request_id,
                actor=args.actor,
                actor_kind=args.actor_kind,
            )
        elif args.command == "gate":
            result = record_gate(
                args.project,
                gate=args.gate,
                decision=args.decision,
                evidence_ids=args.evidence,
                reason=args.reason,
                human_approved=args.human_approved,
                request_id=args.request_id,
                actor=args.actor,
                actor_kind=args.actor_kind,
            )
        elif args.command == "validate":
            result = validate_project(args.project)
            _print_json(result)
            return 0
        else:  # pragma: no cover - argparse prevents this branch.
            parser.error(f"unknown command: {args.command}")
            return 2
        _print_json(result)
        return 0
    except ResearchStateError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
