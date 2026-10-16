"""Synthetic behavior drill; does not call external models or live services."""
import tempfile
import subprocess
import sys
import unittest
from pathlib import Path

from recovery_policy import recovery_decision
from route_task import EXECUTION_FIELDS, canonical_execution_revision, route
from monitor_policy import observe


def good_packet():
    return {field: ("not_applicable" if field == "scientific_predicate" else f"synthetic declared {field} details")
            for field in EXECUTION_FIELDS}


def valid_request():
    packet = good_packet()
    revision = canonical_execution_revision(packet)
    return {"revision": revision, "reviewed_revision": revision,
            "review_receipt": {"status": "success", "exit_code": 0, "isolation_verified": True,
                               "tools_used": [], "tools_available": [], "requested_model": "grok-4.7",
                               "requested_reasoning_effort": "xhigh", "launch_reasoning_effort": "xhigh",
                               "actual_reported_reasoning_effort": None, "effort_evidence": "launch_argument",
                               "actual_model": "grok-4.7", "revision": revision,
                               "result": "synthetic adversarial findings"},
            "adjudication": {"revision": revision, "status": "accepted"},
            "execution_packet": packet, "current_step_authorized": True,
            "fixed_luna_thread_id": "synthetic-luna", "executor_authorized": True, "executor_binding": {
                "thread_id": "synthetic-luna", "model": "gpt-6-luna", "reasoning_effort": "low"}}


def rebind_packet(request):
    revision = canonical_execution_revision(request["execution_packet"])
    request["revision"] = revision
    request["reviewed_revision"] = revision
    request["review_receipt"]["revision"] = revision
    request["adjudication"]["revision"] = revision


class TeamDrill(unittest.TestCase):
    def test_exit_zero_is_not_scientific_success(self):
        request = valid_request()
        request["execution_packet"]["scientific_predicate"] = "pass iff preregistered CI excludes null"
        rebind_packet(request)
        self.assertEqual(route(request)["route"], "luna_execute")
        # A zero process code proves engineering termination only; no scientific evidence means inconclusive.
        with tempfile.TemporaryDirectory(prefix="team-drill-") as work:
            process = subprocess.run([sys.executable, "-c", "raise SystemExit(0)"], cwd=work,
                                     capture_output=True, text=True, timeout=5)
            scientific_outcome = "inconclusive" if process.returncode == 0 else "fail"
            self.assertEqual(process.returncode, 0)
            self.assertEqual(scientific_outcome, "inconclusive")

    def test_monitor_no_change_reuses_event_and_interval(self):
        first = {"job_id": "synthetic", "execution_id": "run-1", "observed_at": "2026-09-26T00:00:00Z",
                 "status": "failed", "event_key": "incident-1", "identity_verified": True, "alive": False}
        state, decision = observe(first)
        second = dict(first, observed_at="2026-09-26T00:01:00Z")
        state2, decision2 = observe(second, state)
        self.assertEqual(decision["event_id"], decision2["event_id"])
        self.assertEqual(decision2["action"], "escalate")
        self.assertEqual(state2["handoff"]["event_id"], state["handoff"]["event_id"])

    def test_recovery_requires_every_gate_and_only_once(self):
        identity = {"attempt_id": "a1", "protocol_version": "p1", "code_identity": "code1", "inputs_identity": "i1",
                    "config_identity": "c1", "weights_identity": "w1"}
        valid = dict(original=identity, candidate=dict(identity), checkpoint_valid=True,
                     old_process_exited=True, registered=True, same_incident=True, recovery_count=0)
        self.assertTrue(recovery_decision(**valid)["recover"])
        self.assertFalse(recovery_decision(**dict(valid, recovery_count=1))["recover"])
        self.assertFalse(recovery_decision(**dict(valid, old_process_exited=False))["recover"])
        self.assertFalse(recovery_decision(**dict(valid, candidate=dict(identity, code_identity="code2")))["recover"])
        self.assertFalse(recovery_decision(**dict(valid, candidate=dict(identity, inputs_identity="other")))["recover"])
        self.assertFalse(recovery_decision(**dict(valid, user_stopped=True))["recover"])
        self.assertFalse(recovery_decision(**dict(valid, scientific_failed=True))["recover"])

    def test_synthetic_filesystem_does_not_launch_a_job(self):
        with tempfile.TemporaryDirectory(prefix="team-drill-") as work:
            path = Path(work) / "synthetic_result.txt"
            path.write_text("exit code 0; science inconclusive", encoding="utf-8")
            self.assertIn("inconclusive", path.read_text(encoding="utf-8"))
            self.assertFalse((Path(work) / "process_started").exists())


if __name__ == "__main__":
    unittest.main()
