import unittest

from route_task import EXECUTION_FIELDS, canonical_execution_revision, quota_zone, route


def packet():
        return {field: ("not_applicable" if field == "scientific_predicate" else {"declared": f"synthetic details for {field}"})
            for field in EXECUTION_FIELDS}


def receipt(revision="r1"):
    return {"status": "success", "exit_code": 0, "isolation_verified": True,
            "tools_used": [], "tools_available": [], "requested_model": "grok-4.7",
            "model": "grok-4.7", "requested_reasoning_effort": "xhigh",
            "launch_reasoning_effort": "xhigh", "actual_reported_reasoning_effort": None,
            "effort_evidence": "launch_argument", "revision": revision,
            "result": "review findings"}


def reviewed(**changes):
    execution_packet = packet()
    revision = canonical_execution_revision(execution_packet)
    review_receipt = receipt(revision)
    request = {"task_kind": "implementation", "revision": revision, "reviewed_revision": revision,
               "review_receipt": review_receipt, "adjudication": {"revision": revision, "status": "accepted"},
               "execution_packet": execution_packet, "current_model": "gpt-6-astra",
               "current_step_authorized": True, "fixed_luna_thread_id": "luna-thread-1",
               "executor_authorized": True,
               "executor_binding": {"thread_id": "luna-thread-1", "model": "gpt-6-luna", "reasoning_effort": "low"}}
    request.update(changes)
    return route(request)


class RouteTaskTests(unittest.TestCase):
    def test_quota_zones_preserved(self):
        self.assertEqual([quota_zone(v) for v in (80, 26, 15, 5, None)],
                         ["green", "yellow", "red", "emergency", "unknown"])

    def test_review_precedes_luna_low_execution(self):
        first = route({"revision": "r1", "externalizable": True, "current_model": "gpt-6-luna"})
        self.assertEqual((first["route"], first["model"], first["reasoning_effort"]),
                         ("grok_review", "grok-4.7", "xhigh"))
        result = reviewed()
        self.assertEqual((result["route"], result["model"], result["reasoning_effort"]),
                         ("luna_execute", "gpt-6-luna", "low"))

    def test_review_completion_requires_real_matching_receipt_and_adjudication(self):
        self.assertEqual(reviewed(review_receipt={"status": "success", "exit_code": 0, "accepted": True}, externalizable=True)["route"], "grok_review")
        self.assertEqual(reviewed(reviewed_revision="r0", externalizable=True)["route"], "grok_review")
        revision = reviewed()["revision"]
        self.assertEqual(reviewed(adjudication={"revision": revision, "status": "pending"})["route"], "coordinator_decide")
        self.assertEqual(reviewed(adjudication={"revision": "sha256:other", "status": "accepted"})["route"], "coordinator_decide")

    def test_historical_high_receipt_does_not_authorize_current_review(self):
        revision = canonical_execution_revision(packet())
        old = receipt(revision)
        old.update(requested_reasoning_effort="high", launch_reasoning_effort="high")
        result = reviewed(review_receipt=old, externalizable=True)
        self.assertEqual(result["route"], "grok_review")
        self.assertEqual(result["reasoning_effort"], "xhigh")

    def test_echoed_effort_mismatch_is_not_accepted(self):
        revision = canonical_execution_revision(packet())
        self.assertEqual(reviewed(review_receipt=receipt(revision) | {"actual_reported_reasoning_effort": "high"},
                                  externalizable=True)["route"], "grok_review")
        echoed = receipt(revision) | {"actual_reported_reasoning_effort": "xhigh", "effort_evidence": "server_echo"}
        self.assertEqual(reviewed(review_receipt=echoed)["route"], "luna_execute")

    def test_missing_packet_fields_fail_closed_exactly(self):
        result = reviewed(execution_packet={"attempt_protocol": "synthetic attempt and protocol"})
        self.assertEqual(result["route"], "blocked")
        self.assertEqual(result["missing_fields"], [f for f in EXECUTION_FIELDS if f != "attempt_protocol"])

    def test_legacy_coordinator_flag_does_not_change_route(self):
        a = route({"revision": "r1", "externalizable": True, "coordinator_is_astra": True})
        b = route({"revision": "r1", "externalizable": True, "coordinator_is_astra": False})
        self.assertEqual(a, b)
        self.assertIsNone(a["coordinator_model"])

    def test_unavailable_model_is_blocked_without_substitution(self):
        result = reviewed(luna_available=False)
        self.assertEqual(result["route"], "blocked")
        self.assertIsNone(result["model"])
        self.assertIn("no model substitution", result["reason"])

    def test_plan_mode_never_implements(self):
        result = route({"revision": "r1", "plan_mode": True, "current_model": "gpt-6-luna"})
        self.assertEqual(result["route"], "coordinator_decide")
        self.assertFalse(result["implementation_started"])

    def test_wait_requires_real_verified_job_and_uses_attached_luna_heartbeat(self):
        self.assertEqual(route({"task_kind": "wait"})["route"], "blocked")
        job = {"job_id": "synthetic-1", "identity_verified": True, "status": "running", "alive": True, "execution_id": "run-1"}
        binding = {"thread_id": "luna-1", "model": "gpt-6-luna", "reasoning_effort": "low", "heartbeat": "attached"}
        result = route({"task_kind": "wait", "actual_job": job, "current_model": "gpt-6-luna",
                        "fixed_luna_thread_id": "luna-1", "executor_authorized": True, "executor_binding": binding})
        self.assertEqual((result["route"], result["model"], result["reasoning_effort"], result["heartbeat"]),
                         ("luna_monitor", "gpt-6-luna", "low", "attached"))
        for changed in ({"alive": False}, {"status": "unknown"}, {"execution_id": ""}):
            bad = dict(job, **changed)
            self.assertEqual(route({"task_kind": "wait", "actual_job": bad, "fixed_luna_thread_id": "luna-1", "executor_authorized": True, "executor_binding": binding})["route"], "coordinator_decide")

    def test_explicit_gemini_and_mimo_remain_behind_gates(self):
        self.assertEqual(reviewed(explicit_model="gemini")["route"], "blocked")
        self.assertEqual(reviewed(explicit_model="gemini", externalizable=True)["route"], "gemini_execute")
        self.assertEqual(reviewed(explicit_model="mimo")["route"], "mimo_execute")

    def test_execution_packet_hash_change_invalidates_prior_review(self):
        p = packet()
        p["objective_claims"] = {"changed": "different semantic claim"}
        result = reviewed(execution_packet=p, externalizable=True)
        self.assertEqual(result["route"], "blocked")
        self.assertEqual(result["reason"], "revision does not match canonical execution packet hash")

    def test_judgment_and_review_never_dispatch_implementation(self):
        self.assertEqual(reviewed(task_kind="judgment")["route"], "coordinator_decide")
        self.assertEqual(reviewed(task_kind="review", operation="implementation")["route"], "coordinator_decide")
        self.assertEqual(reviewed(task_kind="review", operation="review")["route"], "coordinator_decide")
        self.assertEqual(route({"task_kind": "review", "revision": "sha256:readonly", "externalizable": True})["route"], "grok_review")

    def test_step_authorization_and_stop_gate_luna_execution(self):
        self.assertEqual(reviewed(current_step_authorized=False)["route"], "coordinator_decide")
        self.assertEqual(reviewed(stop_requested=True)["route"], "coordinator_decide")
        self.assertEqual(reviewed(explicit_model="gemini", externalizable=True, current_step_authorized=False)["route"], "coordinator_decide")
        self.assertEqual(reviewed(explicit_model="mimo", scientific_failed=True)["route"], "coordinator_decide")

    def test_low_quota_is_not_a_hard_limit_and_gemini_model_is_explicit(self):
        result = reviewed(explicit_model="gemini", externalizable=True, gemini_remaining_percent=5)
        self.assertEqual(result["route"], "gemini_execute")
        self.assertEqual(result["model"], "gemini-3.8-flash-high")

    def test_nested_boolean_metadata_is_allowed_but_field_boolean_is_not(self):
        p = packet()
        p["inputs_identity"] = {"gpu_training": False, "no_download": True, "source": "synthetic-inputs-v1"}
        self.assertEqual(reviewed(execution_packet=p)["route"], "blocked")  # package hash changed
        p["inputs_identity"] = {"gpu_training": False, "no_download": True, "source": "synthetic-inputs-v1"}
        from route_task import missing_execution_fields
        self.assertNotIn("inputs_identity", missing_execution_fields(p))
        p["inputs_identity"] = True
        self.assertIn("inputs_identity", missing_execution_fields(p))

    def test_grok_unavailable_does_not_fall_back(self):
        result = route({"revision": "r1", "externalizable": True, "grok_available": False})
        self.assertEqual(result["route"], "blocked")
        self.assertIsNone(result["model"])

    def test_not_applicable_science_is_explicit(self):
        p = packet()
        p["scientific_predicate"] = ""
        self.assertEqual(reviewed(execution_packet=p)["route"], "blocked")
        p["scientific_predicate"] = "not_applicable"
        self.assertEqual(reviewed(execution_packet=p)["route"], "luna_execute")


if __name__ == "__main__":
    unittest.main()
