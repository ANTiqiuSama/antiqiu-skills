"""Pure one-shot restart gate for an already registered project attempt."""


IDENTITY_FIELDS = ("attempt_id", "protocol_version", "code_identity", "inputs_identity", "config_identity", "weights_identity")


def recovery_decision(*, original, candidate, checkpoint_valid, old_process_exited,
                      registered, same_incident, recovery_count, user_stopped=False,
                      scientific_failed=False):
    """Return whether this exact attempt may recover once; never starts a process."""
    if user_stopped or scientific_failed:
        return {"recover": False, "reason": "explicit_stop_or_scientific_failure"}
    if not isinstance(original, dict) or not isinstance(candidate, dict):
        return {"recover": False, "reason": "identity_missing"}
    if any(not original.get(key) or candidate.get(key) != original.get(key) for key in IDENTITY_FIELDS):
        return {"recover": False, "reason": "identity_mismatch"}
    if not checkpoint_valid:
        return {"recover": False, "reason": "checkpoint_invalid"}
    if not old_process_exited:
        return {"recover": False, "reason": "old_process_not_confirmed_exited"}
    if not registered:
        return {"recover": False, "reason": "attempt_not_registered"}
    if not same_incident:
        return {"recover": False, "reason": "incident_mismatch"}
    if type(recovery_count) is not int or recovery_count != 0:
        return {"recover": False, "reason": "recovery_already_used_or_unknown"}
    return {"recover": True, "reason": "verified_same_attempt", "next_recovery_count": 1}
