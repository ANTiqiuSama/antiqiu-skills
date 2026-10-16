#!/usr/bin/env python3
"""Read-only structural audit for a research release candidate.

This program deliberately has no dependency on the research state writer.  It
only opens files for reading, which makes it suitable as an independent check
and lets it report on incomplete or damaged projects without trying to repair
them implicitly.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence
from urllib.parse import urlparse


HEX_SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")
PASS_DECISIONS = {"approved", "complete", "completed", "pass", "passed", "success", "succeeded"}
TASK_COMPLETE = {"complete", "completed", "superseded"}
TASK_KNOWN = TASK_COMPLETE | {"blocked", "failed", "in_progress", "pending", "ready", "running"}
RELEASE_GATE_NAMES = {"release", "release_approval", "release_decision", "human_release", "human_release_decision"}
HUMAN_ONLY_GATE_NAMES = RELEASE_GATE_NAMES | {"adopted", "adoption"}
INDEPENDENT_REVIEW_GATE_NAMES = {"independent_review", "release_audit", "research_release_audit"}
INDEPENDENT_REVIEW_EVIDENCE_KINDS = {"independent_review", "release_audit", "review", "review_report"}
RUN_MANIFEST_NAMES = {"run-manifest.json", "run_manifest.json"}


@dataclass(frozen=True)
class Issue:
    code: str
    severity: str
    message: str
    location: str
    remediation: str


@dataclass(frozen=True)
class AuditResult:
    status: str
    project: str
    issues: tuple[Issue, ...]
    stats: Mapping[str, int]

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "project": self.project,
            "issues": [asdict(issue) for issue in self.issues],
            "stats": dict(self.stats),
        }


class Auditor:
    """Accumulates findings while never writing to the project being checked."""

    def __init__(self, project: Path):
        self.project = project.expanduser().resolve()
        self.state_dir = self.project / ".research-program"
        self.issues: list[Issue] = []
        self._issue_keys: set[tuple[str, str]] = set()
        self.stats: dict[str, int] = {
            "events": 0,
            "tasks": 0,
            "claims": 0,
            "evidence": 0,
            "artifacts": 0,
            "run_manifests": 0,
            "reviews": 0,
            "gates": 0,
        }
        self.snapshot: dict[str, Any] = {}
        self.state: dict[str, Any] = {}
        self.events: list[dict[str, Any]] = []
        self.artifacts: dict[str, dict[str, Any]] = {}
        self.evidence: dict[str, dict[str, Any]] = {}
        self._checked_artifacts: set[str] = set()
        self.canonical_state = False

    def add(
        self,
        code: str,
        severity: str,
        message: str,
        location: str,
        remediation: str,
    ) -> None:
        key = (code, location)
        if key in self._issue_keys:
            return
        self._issue_keys.add(key)
        self.issues.append(Issue(code, severity, message, location, remediation))

    def run(self) -> AuditResult:
        if not self.project.exists() or not self.project.is_dir():
            self.add(
                "PROJECT_DIRECTORY_MISSING",
                "error",
                "The project directory does not exist or is not a directory.",
                str(self.project),
                "Pass the research project root to --project.",
            )
            return self.result()

        snapshot_path = self.state_dir / "project.json"
        snapshot = self.read_json(snapshot_path, "PROJECT_STATE")
        if not isinstance(snapshot, dict):
            if snapshot is None and not any(i.code.startswith("PROJECT_STATE_") for i in self.issues):
                self.add(
                    "PROJECT_STATE_MISSING",
                    "error",
                    "The durable project snapshot is missing.",
                    self.relative(snapshot_path),
                    "Initialize the research program and checkpoint it before requesting release.",
                )
            return self.result()

        self.snapshot = snapshot
        format_version = snapshot.get("format_version")
        if format_version is None:
            self.add(
                "PROJECT_FORMAT_VERSION_MISSING",
                "warning",
                "The durable snapshot has no format_version.",
                self.relative(snapshot_path),
                "Replay and checkpoint the project with the current state engine.",
            )
        elif format_version != 1:
            self.add(
                "PROJECT_FORMAT_VERSION_UNSUPPORTED",
                "error",
                f"Snapshot format_version {format_version!r} is not supported by this auditor.",
                self.relative(snapshot_path),
                "Use a matching auditor or migrate the snapshot through a documented state transition.",
            )
        nested_state = snapshot.get("state")
        self.canonical_state = isinstance(nested_state, dict)
        self.state = nested_state if self.canonical_state else snapshot

        if self.canonical_state:
            self.audit_snapshot_state_hash()
            project_record = self.state.get("project")
            if not isinstance(project_record, dict) or project_record.get("completed") is not True:
                self.add(
                    "PROJECT_INCOMPLETE",
                    "error",
                    "The canonical research project is not marked complete by a human release gate.",
                    ".research-program/project.json#state/project/completed",
                    "Complete required research and independent audit tasks, then record the human release decision.",
                )

        self.audit_events()
        if self.canonical_state:
            self.audit_replay_consistency()
        self.load_artifacts()
        tasks = self.audit_tasks()
        if self.canonical_state:
            self.audit_required_stage_coverage(tasks)
        evidence = self.audit_claims()
        self.audit_declared_artifacts(tasks)
        self.audit_run_manifests(tasks)
        self.audit_reviews()
        self.audit_gates()

        self.stats["evidence"] = len(evidence)
        self.stats["artifacts"] = len(self._checked_artifacts)
        if not tasks:
            self.add(
                "TASK_SET_EMPTY",
                "error" if self.canonical_state else "warning",
                "The release has no recorded research tasks.",
                ".research-program/project.json#state/tasks",
                "Record the completed research work and its acceptance artifacts before release.",
            )
        if self.stats["claims"] == 0:
            self.add(
                "CLAIM_LEDGER_EMPTY",
                "error" if self.canonical_state else "warning",
                "The release has no claim ledger to audit.",
                ".research-program/project.json#state/claims",
                "Map manuscript claims to independently checkable evidence before release.",
            )
        if not self._checked_artifacts:
            self.add(
                "RELEASE_ARTIFACT_MISSING",
                "error" if self.canonical_state else "warning",
                "No durable local release artifact was available for existence and hash checks.",
                ".research-program/project.json#state/artifacts",
                "Attach the manuscript, reports, and other release outputs with project-relative paths and SHA-256 values.",
            )
        return self.result()

    def result(self) -> AuditResult:
        if any(issue.severity == "error" for issue in self.issues):
            status = "fail"
        elif any(issue.severity == "warning" for issue in self.issues):
            status = "partial"
        else:
            status = "pass"
        ordered = tuple(sorted(self.issues, key=lambda i: ({"error": 0, "warning": 1}.get(i.severity, 2), i.code, i.location)))
        return AuditResult(status, str(self.project), ordered, dict(self.stats))

    def read_json(self, path: Path, prefix: str) -> Any | None:
        if not path.is_file():
            return None
        try:
            with path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except UnicodeDecodeError as exc:
            self.add(
                f"{prefix}_ENCODING_INVALID",
                "error",
                f"JSON is not valid UTF-8: {exc}.",
                self.relative(path),
                "Rewrite the file as UTF-8 from a trusted source, then rerun the audit.",
            )
        except (json.JSONDecodeError, OSError) as exc:
            self.add(
                f"{prefix}_INVALID",
                "error",
                f"JSON could not be read: {exc}.",
                self.relative(path),
                "Restore a valid JSON file from the immutable record or rerun the producing task.",
            )
        return None

    def audit_snapshot_state_hash(self) -> None:
        recorded = self.snapshot.get("state_hash")
        location = ".research-program/project.json#state_hash"
        if not isinstance(recorded, str) or not HEX_SHA256.fullmatch(recorded):
            self.add(
                "SNAPSHOT_STATE_HASH_MISSING",
                "error",
                "The canonical snapshot has no valid SHA-256 state_hash.",
                location,
                "Replay the immutable event ledger with the state engine and checkpoint a new snapshot.",
            )
            return
        calculated = hashlib.sha256(
            json.dumps(
                self.state,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        if calculated != recorded.lower():
            self.add(
                "SNAPSHOT_STATE_HASH_MISMATCH",
                "error",
                "The canonical snapshot state does not match its recorded state_hash.",
                location,
                "Treat the snapshot as corrupted and rebuild it from the trusted event ledger.",
            )

    def relative(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(self.project).as_posix()
        except (OSError, ValueError):
            return str(path)

    # -- Immutable event chain -------------------------------------------------

    def audit_events(self) -> None:
        event_dir = self.state_dir / "events"
        if not event_dir.is_dir():
            self.add(
                "EVENT_LOG_MISSING",
                "error",
                "The immutable event directory is missing.",
                self.relative(event_dir),
                "Restore the event log; a snapshot alone is insufficient provenance.",
            )
            return

        event_paths = sorted(event_dir.glob("*.json"), key=self.event_sort_key)
        if not event_paths:
            self.add(
                "EVENT_LOG_EMPTY",
                "error",
                "The immutable event directory contains no events.",
                self.relative(event_dir),
                "Initialize the project through the state engine so the first event is recorded.",
            )
            return

        previous_hash: str | None = None
        previous_sequence: int | None = None
        for index, path in enumerate(event_paths):
            event = self.read_json(path, "EVENT")
            location = self.relative(path)
            if not isinstance(event, dict):
                if event is not None:
                    self.add(
                        "EVENT_NOT_OBJECT",
                        "error",
                        "An event record is not a JSON object.",
                        location,
                        "Restore the event from a trusted append-only backup.",
                    )
                continue

            self.events.append(event)
            schema_version = event.get("schema_version")
            if schema_version is None:
                self.add(
                    "EVENT_SCHEMA_VERSION_MISSING",
                    "warning",
                    "Event has no schema_version.",
                    location,
                    "Use the current state engine for future events and migrate only through a documented append-only process.",
                )
            elif schema_version != 1:
                self.add(
                    "EVENT_SCHEMA_VERSION_UNSUPPORTED",
                    "error",
                    f"Event schema_version {schema_version!r} is unsupported.",
                    location,
                    "Use an auditor matching this event schema before relying on the release decision.",
                )
            recorded_hash = self.pick(event, "event_hash", "hash")
            if not isinstance(recorded_hash, str) or not HEX_SHA256.fullmatch(recorded_hash):
                self.add(
                    "EVENT_HASH_MISSING",
                    "error",
                    "The event has no valid SHA-256 event_hash.",
                    location,
                    "Regenerate the project from the last trusted event; do not patch history in place.",
                )
                recorded_hash = None
            else:
                computed_hash = self.event_digest(event)
                if computed_hash != recorded_hash.lower():
                    self.add(
                        "EVENT_HASH_MISMATCH",
                        "error",
                        "The event content does not match its recorded hash.",
                        location,
                        "Treat the chain as corrupted and recover from a trusted immutable copy.",
                    )

            recorded_previous = self.pick(event, "previous_hash", "prev_hash")
            if index == 0:
                if recorded_previous not in (None, "", "0" * 64):
                    self.add(
                        "EVENT_CHAIN_GENESIS_INVALID",
                        "error",
                        "The first event points to a predecessor.",
                        location,
                        "Restore the original genesis event and its following chain.",
                    )
            elif previous_hash is not None and recorded_previous != previous_hash:
                self.add(
                    "EVENT_CHAIN_LINK_BROKEN",
                    "error",
                    "The event previous_hash does not match the preceding event.",
                    location,
                    "Recover the missing or altered event sequence from a trusted copy.",
                )

            sequence = self.event_sequence(event, path)
            if sequence is None:
                self.add(
                    "EVENT_SEQUENCE_MISSING",
                    "error",
                    "The event has no usable sequence number.",
                    location,
                    "Record monotonically increasing sequence values in every event.",
                )
            elif previous_sequence is not None and sequence != previous_sequence + 1:
                self.add(
                    "EVENT_SEQUENCE_GAP",
                    "error",
                    f"Expected event sequence {previous_sequence + 1}, found {sequence}.",
                    location,
                    "Recover the missing event or restore the complete chain.",
                )
            previous_sequence = sequence if sequence is not None else previous_sequence
            previous_hash = recorded_hash.lower() if isinstance(recorded_hash, str) else None

        self.stats["events"] = len(self.events)
        if not self.events:
            return

        final_hash = self.pick(self.events[-1], "event_hash", "hash")
        snapshot_head = self.deep_pick(
            self.snapshot,
            "last_event_hash",
            "event_head",
            "head_hash",
            "events_head",
        )
        if snapshot_head is None:
            self.add(
                "SNAPSHOT_EVENT_HEAD_MISSING",
                "error",
                "The snapshot does not declare the event hash it was reduced from.",
                self.relative(self.state_dir / "project.json"),
                "Checkpoint the state with last_event_hash (or event_head) from the reducer.",
            )
        elif isinstance(final_hash, str) and snapshot_head != final_hash:
            self.add(
                "SNAPSHOT_EVENT_HEAD_MISMATCH",
                "error",
                "The snapshot head does not match the immutable event log head.",
                self.relative(self.state_dir / "project.json"),
                "Replay the event log with the trusted state engine and replace the derived snapshot atomically.",
            )

        declared_count = self.deep_pick(self.snapshot, "event_count")
        if declared_count is not None and declared_count != len(self.events):
            self.add(
                "SNAPSHOT_EVENT_COUNT_MISMATCH",
                "error",
                f"Snapshot declares {declared_count!r} events but {len(self.events)} were found.",
                self.relative(self.state_dir / "project.json"),
                "Replay the complete event log to regenerate the snapshot.",
            )
        declared_sequence = self.deep_pick(self.snapshot, "last_sequence")
        final_sequence = self.event_sequence(self.events[-1], event_paths[-1])
        if declared_sequence is not None and declared_sequence != final_sequence:
            self.add(
                "SNAPSHOT_EVENT_SEQUENCE_MISMATCH",
                "error",
                f"Snapshot declares last_sequence {declared_sequence!r}, but the log ends at {final_sequence!r}.",
                self.relative(self.state_dir / "project.json"),
                "Replay the complete immutable event log to regenerate the snapshot.",
            )

    @staticmethod
    def event_sort_key(path: Path) -> tuple[int, str]:
        match = re.match(r"^(\d+)", path.stem)
        return (int(match.group(1)) if match else sys.maxsize, path.name)

    @staticmethod
    def event_sequence(event: Mapping[str, Any], path: Path) -> int | None:
        value = event.get("sequence", event.get("seq"))
        if isinstance(value, int) and not isinstance(value, bool):
            return value
        match = re.match(r"^(\d+)", path.stem)
        return int(match.group(1)) if match else None

    @staticmethod
    def event_digest(event: Mapping[str, Any]) -> str:
        unsigned = {key: value for key, value in event.items() if key not in {"event_hash", "hash"}}
        payload = json.dumps(unsigned, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def audit_replay_consistency(self) -> None:
        """Independently reduce version-1 events and compare with canonical state."""

        state: dict[str, Any] = {
            "_last_sequence": 0,
            "project": None,
            "tasks": {},
            "claims": {},
            "evidence": {},
            "gates": {},
            "request_ids": {},
        }

        def refresh() -> None:
            tasks = state["tasks"]
            for task in tasks.values():
                if task["status"] not in {"pending", "ready"}:
                    continue
                ready = all(
                    tasks.get(dependency, {}).get("status") == "completed"
                    for dependency in task["dependencies"]
                )
                task["status"] = "ready" if ready else "pending"

        try:
            for event in self.events:
                event_type = event["event_type"]
                payload = event["payload"]
                occurred_at = event["occurred_at"]
                sequence = event["sequence"]
                actor = event["actor"]

                if event_type == "project_initialized":
                    if state["project"] is not None:
                        raise ValueError("multiple project initialization events")
                    state["project"] = copy.deepcopy(payload["project"])
                elif state["project"] is None:
                    raise ValueError("first event does not initialize the project")
                elif event_type == "task_added":
                    task = copy.deepcopy(payload["task"])
                    if task["id"] in state["tasks"]:
                        raise ValueError(f"duplicate task {task['id']}")
                    task.setdefault("gap_key", f"legacy:{task['id']}")
                    task.setdefault("priority", 50)
                    state["tasks"][task["id"]] = task
                elif event_type == "task_started":
                    task = state["tasks"][payload["task_id"]]
                    if payload["resume"] and task["status"] == "in_progress":
                        if not task["attempts"] or task["attempts"][-1]["ended_at"] is not None:
                            raise ValueError("in-progress task has no resumable attempt")
                        task["attempts"][-1].setdefault("resumes", []).append(
                            {
                                "recorded_at": occurred_at,
                                "actor": copy.deepcopy(actor),
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
                                "actor": copy.deepcopy(actor),
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
                    task["negative_findings"].append(
                        {
                            "kind": "blocked_attempt",
                            "reason": payload["reason"],
                            "recorded_at": occurred_at,
                            "actor": copy.deepcopy(actor),
                            "event_sequence": sequence,
                        }
                    )
                elif event_type == "claim_added":
                    claim = copy.deepcopy(payload["claim"])
                    if claim["id"] in state["claims"]:
                        raise ValueError(f"duplicate claim {claim['id']}")
                    claim.setdefault("epistemic_state", "active")
                    claim.setdefault("contradiction_ids", [])
                    state["claims"][claim["id"]] = claim
                elif event_type == "evidence_added":
                    evidence = copy.deepcopy(payload["evidence"])
                    if evidence["id"] in state["evidence"]:
                        raise ValueError(f"duplicate evidence {evidence['id']}")
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
                            "actor": copy.deepcopy(actor),
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
                        "actor": copy.deepcopy(actor),
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
                        self.normalize_name(name) in RELEASE_GATE_NAMES
                        and payload["decision"] == "passed"
                        and actor["kind"] == "human"
                        and payload["human_approved"]
                    ):
                        state["project"]["completed"] = True
                        state["project"]["completed_at"] = occurred_at
                else:
                    raise ValueError(f"unsupported event type {event_type!r}")

                request = event.get("request")
                if request is not None:
                    request_id = request["id"]
                    if request_id in state["request_ids"]:
                        raise ValueError(f"duplicate request id {request_id!r}")
                    state["request_ids"][request_id] = {
                        "command": request["command"],
                        "fingerprint": request["fingerprint"],
                        "result": copy.deepcopy(event["result"]),
                        "event_sequence": sequence,
                        "event_hash": event["event_hash"],
                    }
                state["_last_sequence"] = sequence
                refresh()
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            self.add(
                "EVENT_REPLAY_FAILED",
                "error",
                f"Independent event reduction failed: {exc}.",
                ".research-program/events",
                "Repair the event chain from a trusted source or use a matching versioned auditor.",
            )
            return

        if state != self.state:
            self.add(
                "SNAPSHOT_REPLAY_MISMATCH",
                "error",
                "Independent reduction of the immutable events does not equal snapshot state.",
                ".research-program/project.json#state",
                "Discard the snapshot and rebuild it from the trusted ledger before release.",
            )

    # -- State collections -----------------------------------------------------

    def state_location(self, suffix: str = "") -> str:
        base = (
            ".research-program/project.json#state"
            if self.canonical_state
            else ".research-program/project.json"
        )
        return f"{base}/{suffix}" if suffix else base

    def state_collection(self, name: str, identity: str) -> list[dict[str, Any]]:
        value = self.state.get(name)
        location = self.state_location(name)
        if value is None:
            return []
        if isinstance(value, list):
            result = []
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    result.append(dict(item))
                else:
                    self.add(
                        "STATE_COLLECTION_ENTRY_INVALID",
                        "error",
                        f"Collection {name!r} contains a non-object entry.",
                        f"{location}/{index}",
                        "Restore a valid state snapshot by replaying the event log.",
                    )
            return result
        if isinstance(value, dict):
            result: list[dict[str, Any]] = []
            for key, item in value.items():
                if isinstance(item, dict):
                    normalized = dict(item)
                    normalized.setdefault(identity, str(key))
                    result.append(normalized)
                else:
                    self.add(
                        "STATE_COLLECTION_ENTRY_INVALID",
                        "error",
                        f"Collection {name!r} contains a non-object entry.",
                        f"{location}/{key}",
                        "Restore a valid state snapshot by replaying the event log.",
                    )
            return result
        self.add(
            "STATE_COLLECTION_INVALID",
            "error",
            f"State collection {name!r} is neither an object nor a list.",
            location,
            "Restore a valid state snapshot by replaying the event log.",
        )
        return []

    @staticmethod
    def identity(item: Mapping[str, Any], fallback: str, *names: str) -> str:
        for name in names:
            value = item.get(name)
            if value not in (None, ""):
                return str(value)
        return fallback

    @staticmethod
    def pick(item: Mapping[str, Any], *names: str) -> Any:
        for name in names:
            if name in item:
                return item[name]
        return None

    @staticmethod
    def deep_pick(item: Mapping[str, Any], *names: str) -> Any:
        for container in (item, item.get("meta"), item.get("_meta"), item.get("state")):
            if not isinstance(container, Mapping):
                continue
            for name in names:
                if name in container:
                    return container[name]
        return None

    def load_artifacts(self) -> None:
        artifacts = self.state_collection("artifacts", "id")
        for index, artifact in enumerate(artifacts):
            artifact_id = self.identity(artifact, f"artifact-{index + 1}", "id", "artifact_id", "name")
            artifact.setdefault("id", artifact_id)
            self.artifacts[artifact_id] = artifact
        self.stats["artifacts"] = len(self.artifacts)

    # -- Tasks -----------------------------------------------------------------

    def audit_tasks(self) -> list[dict[str, Any]]:
        tasks = self.state_collection("tasks", "id")
        self.stats["tasks"] = len(tasks)
        by_id: dict[str, dict[str, Any]] = {}
        for index, task in enumerate(tasks):
            task_id = self.identity(task, f"task-{index + 1}", "id", "task_id")
            task.setdefault("id", task_id)
            by_id[task_id] = task

        dependencies: dict[str, list[str]] = {}
        for task_id, task in by_id.items():
            location = self.state_location(f"tasks/{task_id}")
            status = str(self.pick(task, "status", "state") or "pending").lower()
            if status not in TASK_KNOWN:
                self.add(
                    "TASK_STATUS_INVALID",
                    "error",
                    f"Task has unknown status {status!r}.",
                    location,
                    "Use a state-engine task status and replay the snapshot.",
                )
            required = bool(task.get("required", task.get("mandatory", True)))
            if required and status not in TASK_COMPLETE:
                code = {
                    "blocked": "TASK_REQUIRED_BLOCKED",
                    "failed": "TASK_REQUIRED_FAILED",
                }.get(status, "TASK_REQUIRED_INCOMPLETE")
                self.add(
                    code,
                    "error",
                    f"Required task is {status}, so the release is not ready.",
                    location,
                    "Resolve, explicitly supersede, or complete the task with its acceptance evidence.",
                )

            refs = self.as_strings(self.pick(task, "depends_on", "dependencies", "requires"))
            dependencies[task_id] = refs
            for dependency in refs:
                if dependency not in by_id:
                    self.add(
                        "TASK_DEPENDENCY_MISSING",
                        "error",
                        f"Task references unknown dependency {dependency!r}.",
                        location,
                        "Restore the dependency task or correct the task through a new state event.",
                    )
                elif status in {"ready", "running", "in_progress", "completed", "complete"}:
                    dependency_status = str(self.pick(by_id[dependency], "status", "state") or "pending").lower()
                    if dependency_status not in TASK_COMPLETE:
                        self.add(
                            "TASK_DEPENDENCY_UNSATISFIED",
                            "error",
                            f"Task is {status} while dependency {dependency!r} is {dependency_status}.",
                            location,
                            "Recompute readiness by replaying the event log before continuing.",
                        )

            if status in {"completed", "complete"} and not self.artifact_refs(task):
                self.add(
                    "TASK_OUTPUT_ARTIFACT_MISSING",
                    "error" if self.canonical_state else "warning",
                    "Completed task declares no durable output artifact.",
                    location,
                    "Attach the produced artifact and its SHA-256 through a new event.",
                )

        self.detect_task_cycles(dependencies)
        return tasks

    def detect_task_cycles(self, graph: Mapping[str, Sequence[str]]) -> None:
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(node: str, trail: list[str]) -> None:
            if node in visiting:
                cycle = trail[trail.index(node) :] + [node] if node in trail else trail + [node]
                self.add(
                    "TASK_DEPENDENCY_CYCLE",
                    "error",
                    "Task dependency cycle: " + " -> ".join(cycle),
                    self.state_location(f"tasks/{node}"),
                    "Supersede or replace a dependency edge through the state engine.",
                )
                return
            if node in visited:
                return
            visiting.add(node)
            for dependency in graph.get(node, ()):
                if dependency in graph:
                    visit(dependency, trail + [node])
            visiting.remove(node)
            visited.add(node)

        for node in graph:
            visit(node, [])

    def audit_required_stage_coverage(self, tasks: Sequence[Mapping[str, Any]]) -> None:
        present = {
            self.normalize_name(str(task.get("stage", "")))
            for task in tasks
        }
        required = {
            "framing": "FRAMING_STAGE_MISSING",
            "literature": "LITERATURE_STAGE_MISSING",
            "protocol": "PROTOCOL_STAGE_MISSING",
            "analysis": "ANALYSIS_STAGE_MISSING",
            "manuscript": "MANUSCRIPT_STAGE_MISSING",
            "audit": "AUDIT_STAGE_MISSING",
        }
        for stage, code in required.items():
            if stage not in present:
                self.add(
                    code,
                    "error",
                    f"No {stage} task is recorded in the canonical release package.",
                    self.state_location("tasks"),
                    f"Add and complete a scoped {stage} task with durable acceptance artifacts before release.",
                )

    # -- Claims and evidence ---------------------------------------------------

    def audit_claims(self) -> dict[str, dict[str, Any]]:
        evidence_items = self.state_collection("evidence", "id")
        evidence: dict[str, dict[str, Any]] = {}
        reverse_refs: dict[str, list[str]] = {}
        for index, item in enumerate(evidence_items):
            evidence_id = self.identity(item, f"evidence-{index + 1}", "id", "evidence_id")
            item.setdefault("id", evidence_id)
            evidence[evidence_id] = item
            for claim_id in self.as_strings(self.pick(item, "claims", "claim_ids", "supports")):
                reverse_refs.setdefault(claim_id, []).append(evidence_id)
        self.evidence = evidence

        claims = self.state_collection("claims", "id")
        self.stats["claims"] = len(claims)
        for index, claim in enumerate(claims):
            claim_id = self.identity(claim, f"claim-{index + 1}", "id", "claim_id")
            location = self.state_location(f"claims/{claim_id}")
            stage = str(self.pick(claim, "maturity", "status", "state") or "candidate").lower()
            manuscript = bool(claim.get("in_manuscript")) or str(claim.get("stage", "")).lower() == "manuscript"
            mandatory = bool(claim.get("required", claim.get("mandatory", manuscript or "required" not in claim)))
            if mandatory and stage != "verified":
                self.add(
                    "CLAIM_NOT_VERIFIED",
                    "error",
                    f"Release claim is {stage!r}, not verified.",
                    location,
                    "Add independent evidence or a rerun, then advance the claim through the state engine.",
                )

            refs = self.as_strings(self.pick(claim, "evidence_ids", "evidence", "supported_by"))
            refs.extend(ref for ref in reverse_refs.get(claim_id, []) if ref not in refs)
            resolved: list[dict[str, Any]] = []
            for ref in refs:
                item = evidence.get(ref)
                if item is None:
                    self.add(
                        "CLAIM_EVIDENCE_REFERENCE_MISSING",
                        "error",
                        f"Claim references unknown evidence {ref!r}.",
                        location,
                        "Restore or replace the evidence through an append-only state event.",
                    )
                else:
                    resolved.append(item)

            if stage == "verified" and not resolved:
                self.add(
                    "CLAIM_VERIFICATION_EVIDENCE_MISSING",
                    "error",
                    "A verified claim has no resolvable evidence.",
                    location,
                    "Attach the independent source, test, or rerun that justifies verification.",
                )
            for item in resolved:
                evidence_id = self.identity(item, "unknown", "id", "evidence_id")
                if not self.pick(item, "locator", "url", "doi", "path", "file", "artifact_id"):
                    self.add(
                        "EVIDENCE_LOCATOR_MISSING",
                        "error",
                        "Evidence has no auditable locator.",
                        f"project.json#evidence/{evidence_id}",
                        "Record a DOI, canonical URL, file path, or artifact identifier.",
                    )
                evidence_file = self.pick(item, "file", "path")
                if isinstance(evidence_file, str):
                    self.check_artifact(
                        {
                            "id": f"evidence:{evidence_id}",
                            "path": evidence_file,
                            "sha256": self.pick(item, "sha256", "content_hash", "digest", "hash"),
                        },
                        f"project.json#evidence/{evidence_id}/file",
                    )

            if stage == "verified" and resolved and not self.independence_proven(claim, resolved):
                self.add(
                    "CLAIM_INDEPENDENCE_UNPROVEN",
                    "error",
                    "Verification evidence does not demonstrate independence from the claim producer.",
                    location,
                    "Record distinct independence_key values or mark independently produced evidence explicitly.",
                )

        return evidence

    def independence_proven(self, claim: Mapping[str, Any], evidence: Sequence[Mapping[str, Any]]) -> bool:
        if any(item.get("independent") is True for item in evidence):
            return True
        origin = self.pick(claim, "independence_key", "origin_independence_key", "producer_key")
        evidence_keys = {
            str(self.pick(item, "independence_key", "producer_key", "source_key"))
            for item in evidence
            if self.pick(item, "independence_key", "producer_key", "source_key") not in (None, "")
        }
        if origin not in (None, ""):
            return any(key != str(origin) for key in evidence_keys)
        return len(evidence_keys) >= 1

    # -- Artifacts -------------------------------------------------------------

    def audit_declared_artifacts(self, tasks: Sequence[Mapping[str, Any]]) -> None:
        for artifact_id, artifact in self.artifacts.items():
            self.check_artifact(artifact, f"project.json#artifacts/{artifact_id}")
        for task in tasks:
            task_id = self.identity(task, "unknown", "id", "task_id")
            for index, ref in enumerate(self.artifact_refs(task)):
                self.check_artifact_ref(ref, f"project.json#tasks/{task_id}/artifacts/{index}")
        self.stats["artifacts"] = len(self._checked_artifacts)

    def artifact_refs(self, item: Mapping[str, Any]) -> list[Any]:
        value = self.pick(item, "artifacts", "artifact_ids", "outputs")
        if value is None:
            singular = self.pick(item, "artifact", "output")
            return [] if singular is None else [singular]
        if isinstance(value, list):
            return value
        if isinstance(value, dict):
            return list(value.values())
        return [value]

    def check_artifact_ref(self, ref: Any, location: str) -> None:
        if isinstance(ref, str) and ref in self.artifacts:
            self.check_artifact(self.artifacts[ref], f"project.json#artifacts/{ref}")
        elif isinstance(ref, str):
            self.check_artifact({"path": ref}, location)
        elif isinstance(ref, dict):
            self.check_artifact(ref, location)
        else:
            self.add(
                "ARTIFACT_REFERENCE_INVALID",
                "error",
                "Artifact reference is neither an identifier, path, nor object.",
                location,
                "Record a valid artifact identifier or a path-plus-SHA-256 object.",
            )

    def check_artifact(self, artifact: Mapping[str, Any], location: str) -> None:
        artifact_id = self.identity(artifact, location, "id", "artifact_id", "path", "file", "locator")
        if artifact_id in self._checked_artifacts:
            return
        self._checked_artifacts.add(artifact_id)

        locator = self.pick(artifact, "path", "file", "locator", "uri")
        if not isinstance(locator, str) or not locator.strip():
            self.add(
                "ARTIFACT_PATH_MISSING",
                "error",
                "Artifact has no local path.",
                location,
                "Record the durable project-relative file path and SHA-256.",
            )
            return
        if self.is_url(locator):
            kind = str(self.pick(artifact, "kind", "type") or "").lower()
            if kind not in {"citation", "reference", "source", "web_source"}:
                self.add(
                    "ARTIFACT_REMOTE_UNVERIFIED",
                    "warning",
                    "A release artifact is remote and cannot be existence- or hash-checked locally.",
                    location,
                    "Materialize the release artifact locally and record its SHA-256.",
                )
            return

        raw_path = Path(locator)
        path = raw_path if raw_path.is_absolute() else self.project / raw_path
        resolved = path.resolve()
        try:
            resolved.relative_to(self.project)
        except ValueError:
            self.add(
                "ARTIFACT_OUTSIDE_PROJECT",
                "error",
                "Artifact path resolves outside the project root.",
                location,
                "Copy the immutable artifact into the project and record a project-relative path.",
            )
            return
        if not resolved.is_file():
            self.add(
                "ARTIFACT_FILE_MISSING",
                "error",
                f"Artifact file does not exist: {self.relative(resolved)}.",
                location,
                "Restore or regenerate the artifact, then record it through the state engine.",
            )
            return

        expected = self.normalize_hash(self.pick(artifact, "sha256", "content_hash", "digest", "hash"))
        if expected is None:
            self.add(
                "ARTIFACT_HASH_MISSING",
                "warning",
                "Artifact has no valid recorded SHA-256.",
                location,
                "Record the file SHA-256 in a new immutable event.",
            )
            return
        actual = self.file_digest(resolved)
        if actual != expected:
            self.add(
                "ARTIFACT_HASH_MISMATCH",
                "error",
                f"Artifact SHA-256 mismatch for {self.relative(resolved)}.",
                location,
                "Quarantine the changed file and restore the immutable artifact or rerun its producing task.",
            )

    @staticmethod
    def normalize_hash(value: Any) -> str | None:
        if not isinstance(value, str):
            return None
        candidate = value.split(":", 1)[1] if value.lower().startswith("sha256:") else value
        return candidate.lower() if HEX_SHA256.fullmatch(candidate) else None

    @staticmethod
    def file_digest(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    @staticmethod
    def is_url(value: str) -> bool:
        return urlparse(value).scheme.lower() in {"http", "https"}

    # -- Reproducible run manifests -------------------------------------------

    def audit_run_manifests(self, tasks: Sequence[Mapping[str, Any]]) -> None:
        manifests: dict[str, tuple[dict[str, Any], str]] = {}
        runs = self.state_collection("runs", "id")
        for index, run in enumerate(runs):
            run_id = self.identity(run, f"run-{index + 1}", "id", "run_id")
            path_value = self.pick(run, "manifest", "manifest_path", "path")
            if isinstance(path_value, dict):
                manifests[f"inline:{run_id}"] = (path_value, f"project.json#runs/{run_id}/manifest")
            elif isinstance(path_value, str):
                loaded = self.read_project_json_path(path_value, "RUN_MANIFEST")
                if isinstance(loaded, dict):
                    manifests[path_value] = (loaded, path_value)
            elif self.looks_like_manifest(run):
                manifests[f"inline:{run_id}"] = (run, f"project.json#runs/{run_id}")
            else:
                self.add(
                    "RUN_MANIFEST_MISSING",
                    "warning",
                    "Declared run has no readable manifest.",
                    f"project.json#runs/{run_id}",
                    "Attach a run manifest containing code, data, environment, parameters, seed, I/O hashes, logs, and status.",
                )

        for artifact_id, artifact in self.artifacts.items():
            kind = str(self.pick(artifact, "kind", "type") or "").lower().replace("-", "_")
            locator = self.pick(artifact, "path", "file", "locator")
            if kind == "run_manifest" and isinstance(locator, str) and not self.is_url(locator):
                loaded = self.read_project_json_path(locator, "RUN_MANIFEST")
                if isinstance(loaded, dict):
                    manifests.setdefault(locator, (loaded, locator))

        for task in tasks:
            task_id = self.identity(task, "unknown", "id", "task_id")
            for index, ref in enumerate(self.artifact_refs(task)):
                candidate = self.artifacts.get(ref) if isinstance(ref, str) and ref in self.artifacts else ref
                locator = self.pick(candidate, "path", "file", "locator") if isinstance(candidate, Mapping) else candidate
                if not isinstance(locator, str) or self.is_url(locator) or Path(locator).name not in RUN_MANIFEST_NAMES:
                    continue
                loaded = self.read_project_json_path(locator, "RUN_MANIFEST")
                if isinstance(loaded, dict):
                    manifests.setdefault(locator, (loaded, f"project.json#tasks/{task_id}/artifacts/{index}"))

        experiments = self.project / "research" / "experiments"
        if experiments.is_dir():
            for path in experiments.rglob("*.json"):
                if path.name not in RUN_MANIFEST_NAMES:
                    continue
                key = self.relative(path)
                if key in manifests:
                    continue
                loaded = self.read_json(path, "RUN_MANIFEST")
                if isinstance(loaded, dict):
                    manifests[key] = (loaded, key)

        experimental_tasks = [
            task
            for task in tasks
            if str(task.get("stage", "")).lower() in {"experiment", "experimentation", "implementation"}
            and str(self.pick(task, "status", "state") or "").lower() in {"complete", "completed"}
        ]
        if experimental_tasks and not manifests:
            self.add(
                "RUN_MANIFEST_MISSING",
                "warning",
                "Completed experimental work has no reproducibility manifest.",
                "research/experiments",
                "Record a manifest for each run with code, data, environment, parameters, seed, I/O hashes, logs, and status.",
            )

        for manifest, location in manifests.values():
            self.audit_run_manifest(manifest, location)
        self.stats["run_manifests"] = len(manifests)

    def read_project_json_path(self, value: str, prefix: str) -> Any | None:
        path = Path(value)
        resolved = (path if path.is_absolute() else self.project / path).resolve()
        try:
            resolved.relative_to(self.project)
        except ValueError:
            self.add(
                f"{prefix}_OUTSIDE_PROJECT",
                "error",
                "Manifest path resolves outside the project.",
                value,
                "Place the immutable manifest inside the project.",
            )
            return None
        if not resolved.is_file():
            self.add(
                f"{prefix}_MISSING",
                "error",
                "Manifest file does not exist.",
                value,
                "Restore or regenerate the declared manifest.",
            )
            return None
        return self.read_json(resolved, prefix)

    @staticmethod
    def looks_like_manifest(value: Mapping[str, Any]) -> bool:
        return any(key in value for key in ("code_commit", "git_commit", "data_version", "parameters", "seed"))

    def audit_run_manifest(self, manifest: Mapping[str, Any], location: str) -> None:
        aliases = {
            "code_commit": ("code_commit", "git_commit", "commit"),
            "data_version": ("data_version", "dataset_version", "data"),
            "environment": ("environment", "environment_lock", "runtime"),
            "parameters": ("parameters", "params", "configuration"),
            "seed": ("seed", "seeds", "random_seed"),
            "inputs": ("inputs", "input_artifacts"),
            "outputs": ("outputs", "output_artifacts"),
            "stdout": ("stdout", "stdout_log"),
            "stderr": ("stderr", "stderr_log"),
            "status": ("status", "result_status"),
        }
        values: dict[str, Any] = {}
        for canonical, names in aliases.items():
            present = next((name for name in names if name in manifest), None)
            if present is None:
                self.add(
                    "RUN_MANIFEST_FIELD_MISSING",
                    "warning",
                    f"Run manifest is missing required field {canonical!r}.",
                    f"{location}#{canonical}",
                    f"Regenerate the manifest with an explicit {canonical} field.",
                )
            else:
                values[canonical] = manifest[present]

        for field in ("code_commit", "data_version", "environment", "status"):
            if field in values and values[field] in (None, "", [], {}):
                self.add(
                    "RUN_MANIFEST_FIELD_EMPTY",
                    "warning",
                    f"Run manifest field {field!r} is empty.",
                    f"{location}#{field}",
                    f"Record the actual {field}; never infer or fabricate it.",
                )
        if "seed" in values and values["seed"] in (None, ""):
            self.add(
                "RUN_MANIFEST_SEED_EMPTY",
                "warning",
                "Run manifest seed is empty.",
                f"{location}#seed",
                "Record the actual seed, or an explicit deterministic/non-applicable rationale.",
            )
        if "status" in values and str(values["status"]).lower() not in PASS_DECISIONS:
            self.add(
                "RUN_NOT_SUCCESSFUL",
                "warning",
                f"Run status is {values['status']!r}.",
                f"{location}#status",
                "Resolve or retain the failed run and add a successful superseding run before release.",
            )

        for field in ("inputs", "outputs"):
            if field in values:
                self.audit_manifest_hashes(values[field], location, field)
        for field in ("stdout", "stderr"):
            if field not in values:
                continue
            log = values[field]
            if log in (None, "", {}):
                self.add(
                    "RUN_MANIFEST_LOG_EMPTY",
                    "warning",
                    f"Run manifest {field} log is empty.",
                    f"{location}#{field}",
                    "Record the captured log artifact and its SHA-256, even when the stream is empty.",
                )
            elif isinstance(log, (str, dict)):
                self.check_artifact_ref(log, f"{location}#{field}")
            else:
                self.add(
                    "RUN_MANIFEST_LOG_INVALID",
                    "warning",
                    f"Run manifest {field} log is not an artifact reference.",
                    f"{location}#{field}",
                    "Record a project-relative log path or artifact object with SHA-256.",
                )

    def audit_manifest_hashes(self, value: Any, location: str, field: str) -> None:
        entries: list[Any]
        if isinstance(value, list):
            entries = value
        elif isinstance(value, dict):
            entries = [{"path": key, "sha256": item} if isinstance(item, str) else item for key, item in value.items()]
        else:
            self.add(
                "RUN_MANIFEST_IO_INVALID",
                "warning",
                f"Run manifest {field} must be a list or object with hashes.",
                f"{location}#{field}",
                "Record each input/output with a locator and SHA-256.",
            )
            return
        if not entries:
            self.add(
                "RUN_MANIFEST_IO_EMPTY",
                "warning",
                f"Run manifest {field} is empty.",
                f"{location}#{field}",
                "Record the actual inputs and outputs, or an explicit non-applicable record.",
            )
            return
        for index, entry in enumerate(entries):
            valid = False
            if isinstance(entry, dict):
                valid = self.normalize_hash(self.pick(entry, "sha256", "content_hash", "digest", "hash")) is not None
            if not valid:
                self.add(
                    "RUN_MANIFEST_IO_HASH_MISSING",
                    "warning",
                    f"Run manifest {field} entry has no valid SHA-256.",
                    f"{location}#{field}/{index}",
                    "Record the exact content hash for this run input/output.",
                )
            if isinstance(entry, dict):
                artifact_id = self.pick(entry, "artifact_id", "artifact")
                locator = self.pick(entry, "path", "file", "locator", "uri")
                if isinstance(artifact_id, str):
                    self.check_artifact_ref(artifact_id, f"{location}#{field}/{index}")
                elif isinstance(locator, str):
                    self.check_artifact(entry, f"{location}#{field}/{index}")

    # -- Independent review and human gates -----------------------------------

    def audit_reviews(self) -> None:
        reviews = self.state_collection("reviews", "id")
        self.stats["reviews"] = len(reviews)
        qualifying: list[dict[str, Any]] = []
        for index, review in enumerate(reviews):
            review_id = self.identity(review, f"review-{index + 1}", "id", "review_id")
            status = str(self.pick(review, "status", "decision", "state") or "pending").lower()
            independent = review.get("independent") is True or bool(review.get("independence_key"))
            if independent and status in PASS_DECISIONS:
                qualifying.append(review)
                refs = self.artifact_refs(review)
                if not refs:
                    self.add(
                        "INDEPENDENT_REVIEW_ARTIFACT_MISSING",
                        "error" if self.canonical_state else "warning",
                        "Independent review has no durable report artifact.",
                        f"project.json#reviews/{review_id}",
                        "Attach the review report and SHA-256 before release.",
                    )
                for ref_index, ref in enumerate(refs):
                    self.check_artifact_ref(ref, f"project.json#reviews/{review_id}/artifacts/{ref_index}")

        gates = self.state_collection("gates", "id")
        for gate in gates:
            gate_id = self.identity(gate, "", "id", "gate_id", "name", "slug")
            decision = str(self.pick(gate, "decision", "status", "state") or "pending").lower()
            if self.normalize_name(gate_id) not in INDEPENDENT_REVIEW_GATE_NAMES or decision not in PASS_DECISIONS:
                continue
            refs = self.as_strings(self.pick(gate, "evidence_ids", "evidence", "artifacts"))
            resolved = [self.evidence[ref] for ref in refs if ref in self.evidence]
            gate_actor_kind = self.normalize_name(str(self.pick(gate, "actor_kind", "reviewer_kind") or ""))
            independent = (
                gate.get("independent") is True
                or bool(gate.get("independence_key"))
                or gate_actor_kind in {"human", "independent_agent", "reviewer"}
                or any(item.get("independent") is True or bool(item.get("independence_key")) for item in resolved)
            )
            if not refs:
                self.add(
                    "INDEPENDENT_REVIEW_ARTIFACT_MISSING",
                    "warning",
                    "Independent-review gate has no evidence report.",
                    f"project.json#gates/{gate_id}",
                    "Attach an independently produced review report to the gate.",
                )
            elif len(resolved) != len(refs):
                self.add(
                    "INDEPENDENT_REVIEW_EVIDENCE_MISSING",
                    "error",
                    "Independent-review gate references missing evidence.",
                    f"project.json#gates/{gate_id}",
                    "Restore or replace every referenced review-evidence record.",
                )
            elif not independent:
                self.add(
                    "INDEPENDENT_REVIEW_INDEPENDENCE_UNPROVEN",
                    "error",
                    "Independent-review gate does not record an independent actor or evidence lineage.",
                    f"project.json#gates/{gate_id}",
                    "Record a reviewer/agent independence key distinct from the research producer.",
                )
            else:
                qualifying.append(gate)
            for item in resolved:
                evidence_id = self.identity(item, "unknown", "id", "evidence_id")
                evidence_file = self.pick(item, "file", "path")
                if isinstance(evidence_file, str):
                    self.check_artifact(
                        {
                            "id": f"review-evidence:{evidence_id}",
                            "path": evidence_file,
                            "sha256": self.pick(item, "sha256", "content_hash", "digest", "hash"),
                        },
                        f"project.json#evidence/{evidence_id}/file",
                    )

        if not qualifying:
            for evidence_id, item in self.evidence.items():
                kind = self.normalize_name(str(self.pick(item, "kind", "type") or ""))
                actor_kind = self.normalize_name(str(self.pick(item, "actor_kind", "producer_kind") or ""))
                if kind not in INDEPENDENT_REVIEW_EVIDENCE_KINDS:
                    continue
                if item.get("independent") is not True and not item.get("independence_key") and actor_kind not in {"human", "independent_agent", "reviewer"}:
                    continue
                qualifying.append(item)
                evidence_file = self.pick(item, "file", "path")
                if isinstance(evidence_file, str):
                    self.check_artifact(
                        {
                            "id": f"review-evidence:{evidence_id}",
                            "path": evidence_file,
                            "sha256": self.pick(item, "sha256", "content_hash", "digest", "hash"),
                        },
                        f"project.json#evidence/{evidence_id}/file",
                    )
                elif isinstance(evidence_file, Mapping):
                    descriptor = dict(evidence_file)
                    descriptor.setdefault("id", f"review-evidence:{evidence_id}")
                    self.check_artifact(
                        descriptor,
                        self.state_location(f"evidence/{evidence_id}/file"),
                    )
                else:
                    self.add(
                        "INDEPENDENT_REVIEW_ARTIFACT_MISSING",
                        "error" if self.canonical_state else "warning",
                        "Independent review evidence has no durable local report.",
                        self.state_location(f"evidence/{evidence_id}"),
                        "Attach the review report file and its SHA-256.",
                    )

        if not qualifying:
            self.add(
                "INDEPENDENT_REVIEW_MISSING",
                "error",
                "No completed independent release review is recorded.",
                self.state_location("reviews"),
                "Freeze the package snapshot, have an independent reviewer audit it, and attach the report with dispositions.",
            )

    def audit_gates(self) -> None:
        gates = self.state_collection("gates", "id")
        self.stats["gates"] = len(gates)
        release_gates: list[dict[str, Any]] = []
        for index, gate in enumerate(gates):
            gate_id = self.identity(gate, f"gate-{index + 1}", "id", "gate_id", "name", "slug")
            normalized_id = self.normalize_name(gate_id)
            decision = str(self.pick(gate, "decision", "status", "state") or "pending").lower()
            required = bool(gate.get("required", gate.get("mandatory", True)))
            location = f"project.json#gates/{gate_id}"
            if required and decision not in PASS_DECISIONS:
                self.add(
                    "GATE_REQUIRED_NOT_PASSED",
                    "error",
                    f"Required gate decision is {decision!r}.",
                    location,
                    "Resolve the gate with supporting evidence and, where required, explicit human approval.",
                )
            if normalized_id in HUMAN_ONLY_GATE_NAMES and decision in PASS_DECISIONS and not self.human_approved(gate):
                self.add(
                    "GATE_HUMAN_APPROVAL_MISSING",
                    "error",
                    "A human-only gate is marked passed without explicit human approval.",
                    location,
                    "Record human_approved=true and the accountable approver through a new event.",
                )
            if normalized_id in RELEASE_GATE_NAMES:
                release_gates.append(gate)

        if not release_gates:
            release_gates = self.release_gates_from_events()
        if not release_gates:
            self.add(
                "HUMAN_RELEASE_DECISION_MISSING",
                "error",
                "No explicit human release decision is recorded.",
                self.state_location("gates/release"),
                "After all research and independent-audit gates pass, a human must approve release with supporting evidence.",
            )
        elif not any(
            str(self.pick(gate, "decision", "status", "state") or "").lower() in PASS_DECISIONS
            and self.human_approved(gate)
            for gate in release_gates
        ):
            self.add(
                "HUMAN_RELEASE_DECISION_MISSING",
                "error",
                "The release gate lacks a passed, explicit human decision.",
                self.state_location("gates/release"),
                "A human must approve the release gate after reviewing the independent audit.",
            )

    def release_gates_from_events(self) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for event in self.events:
            kind = str(self.pick(event, "event_type", "type") or "").lower()
            payload = event.get("payload") if isinstance(event.get("payload"), dict) else event
            gate_name = self.identity(payload, "", "gate", "gate_id", "id", "name", "slug")
            if kind in {"gate_decided", "gate_decision", "gate_resolved"} and self.normalize_name(gate_name) in RELEASE_GATE_NAMES:
                results.append(dict(payload))
        return results

    @staticmethod
    def human_approved(gate: Mapping[str, Any]) -> bool:
        actor = gate.get("actor")
        actor_kind = str(gate.get("actor_kind", "")).lower()
        if isinstance(actor, Mapping):
            actor_kind = str(actor.get("kind", actor.get("type", actor.get("actor_type", actor_kind)))).lower()
        identity = gate.get("approved_by") or actor or gate.get("approver")
        if gate.get("human_approved") is True:
            return bool(identity) and actor_kind == "human"
        approval = gate.get("approval")
        if isinstance(approval, Mapping) and approval.get("human") is True:
            approval_actor = approval.get("actor")
            approval_kind = str(approval.get("actor_kind", "")).lower()
            if isinstance(approval_actor, Mapping):
                approval_kind = str(approval_actor.get("kind", approval_actor.get("type", approval_kind))).lower()
            return bool(approval.get("approved_by") or approval_actor or approval.get("approver")) and approval_kind == "human"
        if isinstance(actor, Mapping):
            return str(actor.get("kind", actor.get("type", actor.get("actor_type", "")))).lower() == "human"
        return str(gate.get("actor_type", gate.get("actor_kind", ""))).lower() == "human" and bool(actor)

    @staticmethod
    def normalize_name(value: str) -> str:
        return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")

    @staticmethod
    def as_strings(value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [value]
        if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
            return [str(item) for item in value]
        return [str(value)]


def audit_project(project: str | Path) -> AuditResult:
    """Audit *project* without modifying it or acquiring a writer lock."""

    return Auditor(Path(project)).run()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read-only audit of a research release candidate")
    parser.add_argument("--project", required=True, help="research project root")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    return parser


def render_text(result: AuditResult) -> str:
    lines = [f"release audit: {result.status.upper()}", f"project: {result.project}"]
    if result.issues:
        for issue in result.issues:
            lines.append(f"[{issue.severity.upper()}] {issue.code} at {issue.location}: {issue.message}")
            lines.append(f"  next: {issue.remediation}")
    else:
        lines.append("No structural release-readiness issues found.")
    lines.append("stats: " + ", ".join(f"{key}={value}" for key, value in sorted(result.stats.items())))
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = audit_project(args.project)
    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(result))
    return {"pass": 0, "fail": 1, "partial": 2}[result.status]


if __name__ == "__main__":
    raise SystemExit(main())
