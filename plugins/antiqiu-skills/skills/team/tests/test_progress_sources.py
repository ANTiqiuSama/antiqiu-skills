import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import monitor_policy as policy
from completion_history import completed_file_samples
import test_monitor_policy as fixtures

shot = fixtures.shot


class SourceTests(unittest.TestCase):
    def producer(self, *args, **kwargs):
        return fixtures.MonitorTests().producer_shot(*args, **kwargs)

    def test_missing_or_incomplete_producer_does_not_mix_clocks(self):
        baseline, _ = policy.observe(self.producer(0, 30))
        for sample in (shot(1, 31, progress_comparable=True), self.producer(1, 31)):
            if "progress_samples" in sample:
                for point in sample["progress_samples"]["points"]:
                    point["completed"] -= 1
            state, decision = policy.observe(sample, baseline)
            self.assertIsNone(decision["eta_seconds_range"])
            self.assertEqual(state["history_source"], "wake_observations")
            self.assertEqual(len(state["history"]), 1)

    def test_execution_identity_change_resets_only_rate_history(self):
        state = None
        for hour in range(3):
            state, _ = policy.observe(shot(hour, hour * 10, progress_comparable=True, execution_id="boot:1:100"), state)
        _, decision = policy.observe(shot(3, 30, progress_comparable=True, execution_id="boot:1:200"), state)
        self.assertIsNone(decision["eta_seconds_range"])
        sample = self.producer(3, 30)
        sample["execution_id"] = sample["progress_samples"]["execution_id"] = "boot:1:200"
        _, decision = policy.observe(sample, state)
        self.assertEqual(decision["interval_minutes"], 50)
        with self.assertRaises(ValueError):
            sample["progress_samples"]["execution_id"] = "boot:1:100"
            policy.observe(sample, state)

    def test_terminal_or_unverified_process_has_no_throughput_forecast(self):
        for changes in ({"status": "succeeded"}, {"status": "unknown"},
                        {"alive": False}, {"identity_verified": False}):
            sample = self.producer(0, 30)
            sample.update(changes)
            _, decision = policy.observe(sample)
            self.assertIsNone(decision["eta_seconds_range"])

    def test_phase_change_at_full_count_uses_new_phase_finish_check(self):
        state, _ = policy.observe(shot(0, 100))
        state, _ = policy.observe(shot(1, 100), state)
        _, decision = policy.observe(shot(2, 100, phase="new-phase"), state)
        self.assertEqual(decision["interval_minutes"], 15)
        self.assertEqual(decision["action"], "wait")

    def test_source_required_and_state_is_not_scheduler(self):
        for source in ("", " ", "wake_observations"):
            sample = self.producer(0, 30)
            sample["progress_samples"]["source"] = source
            with self.assertRaises(ValueError):
                policy.observe(sample)
        _, decision = policy.observe(self.producer(0, 30))
        self.assertFalse(decision["scheduled"])

    def test_handoff_survives_new_execution_and_skips_probe(self):
        state, decision = policy.observe(shot(0, status="failed", event_key="failure"))
        event = decision["event_id"]
        state, _ = policy.observe(shot(1, execution_id="new-execution"), state)
        self.assertEqual(policy.pending_decision(state)["action"], "escalate")
        self.assertEqual(state["handoff"]["trigger_snapshot"]["event_key"], "failure")
        state = policy.acknowledge(state, event, "dispatched", "real-worker")
        self.assertEqual(policy.pending_decision(state)["action"], "wait_for_worker")
        finished = policy.acknowledge(state, event, "handled")
        self.assertEqual(policy.pending_decision(finished)["action"], "stop")
        state = policy.acknowledge(state, event, "resume")
        self.assertIsNone(policy.pending_decision(state))
        with self.assertRaises(ValueError):
            policy.acknowledge(state, event, "dispatched", "new-worker")

    def test_new_instance_failure_rearms_without_a_healthy_intermediate_probe(self):
        state, decision = policy.observe(shot(0, status="failed", event_key="oom", execution_id="boot:1:100"))
        first = decision["event_id"]
        state = policy.acknowledge(state, first, "dispatched", "worker-1")
        state = policy.acknowledge(state, first, "resume")
        _, missing = policy.observe(shot(1, status="failed", event_key="oom"), state)
        self.assertEqual(missing["action"], "wait")
        _, same = policy.observe(shot(1, status="failed", event_key="oom", execution_id="boot:1:100"), state)
        self.assertEqual(same["action"], "wait")
        state, decision = policy.observe(shot(1, status="failed", event_key="oom", execution_id="boot:1:200"), state)
        self.assertEqual(decision["action"], "escalate")
        self.assertNotEqual(first, decision["event_id"])
        self.assertIsNone(state["handoff"]["worker_id"])


class MetadataTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.arguments = dict(job_id="job", phase="evaluation", total=10, completed=4,
                              execution_id="boot:1:100", started_at=1000, observed_at=1500,
                              name_pattern=r"(?P<position>\d{4})_.+\.json")

    def tearDown(self):
        self.temp.cleanup()

    def shard(self, position, at, suffix="event"):
        path = self.root / f"{position:04d}_{suffix}.json"
        path.write_text("payload must not be read", encoding="utf-8")
        os.utime(path, (at, at))

    def history(self):
        return completed_file_samples(self.root, **self.arguments)

    def test_collects_current_serial_completions_without_payload_reads(self):
        for position in range(4):
            self.shard(position, 1050 + 100 * position)
        with mock.patch.object(Path, "read_text", side_effect=AssertionError("read payload")), \
             mock.patch.object(Path, "read_bytes", side_effect=AssertionError("read payload")):
            samples = self.history()
        self.assertEqual([point["completed"] for point in samples["points"]], [1, 2, 3, 4])
        self.assertEqual(samples["execution_id"], "boot:1:100")

    def test_absent_history_is_optional(self):
        self.assertIsNone(completed_file_samples(self.root / "missing", **self.arguments))
        self.assertIsNone(self.history())

    def test_gap_duplicate_and_nonmonotonic_times_reject_history(self):
        for position in (0, 2, 3):
            self.shard(position, 1050 + 100 * position)
        self.assertIsNone(self.history())
        self.shard(1, 1150)
        self.assertIsNotNone(self.history())
        self.shard(2, 1300, "duplicate")
        self.assertIsNone(self.history())
        (self.root / "0002_duplicate.json").unlink()
        self.shard(2, 1100)
        self.assertIsNone(self.history())

    def test_old_or_future_completion_cannot_supply_current_rate(self):
        for position in range(4):
            self.shard(position, 1050 + 100 * position)
        self.arguments["started_at"] = 1200
        self.assertIsNone(self.history())
        self.arguments["started_at"] = 1000
        self.shard(3, 1600)
        self.assertIsNone(self.history())


if __name__ == "__main__":
    unittest.main()
