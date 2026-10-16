"""Regression coverage for routine pilots and recorded human decisions."""
import unittest
from pathlib import Path
import tempfile

import research_state as rs


class AuthorityTests(unittest.TestCase):
    def test_local_pilot_does_not_require_reapproval(self):
        rs._require_human_gate('pilot', 'passed', actor_kind='automation', human_approved=False, tty=False)

    def test_actual_human_gates_remain_protected(self):
        for gate in ['adopted', 'ethics', 'publication', 'release']:
            with self.subTest(gate=gate), self.assertRaises(rs.ValidationError):
                rs._require_human_gate(gate, 'passed', actor_kind='automation', human_approved=False, tty=True)

    def test_approval_flag_alone_is_not_human_authority(self):
        with self.assertRaises(rs.ValidationError):
            rs._require_human_gate('adopted', 'waived', actor_kind='automation', human_approved=True, tty=True)

    def test_recorded_human_decision_does_not_require_terminal(self):
        rs._require_human_gate('adopted', 'passed', actor_kind='human', human_approved=True, tty=False)

    def test_human_actor_without_approval_is_rejected(self):
        with self.assertRaises(rs.ValidationError):
            rs._require_human_gate('release', 'passed', actor_kind='human', human_approved=False, tty=True)

    def test_recording_failure_never_needs_approval(self):
        rs._require_human_gate('release', 'failed', actor_kind='automation', human_approved=False, tty=False)

    def project_with_evidence(self, path):
        rs.init_project(path, title='Synthetic pilot', question='Does the local fixture run?')
        evidence = Path(path) / 'decision.txt'
        evidence.write_text('Synthetic user decision: permit this local pilot and adopt its fixture result.', encoding='utf-8')
        rs.add_evidence(path, kind='fixture', locator='decision.txt', is_file=True,
                        independence_key='synthetic-test', evidence_id='fixture-evidence')

    def test_pilot_decision_persists_and_replays_without_human_gate(self):
        with tempfile.TemporaryDirectory() as path:
            self.project_with_evidence(path)
            rs.record_gate(path, gate='pilot', decision='passed', evidence_ids=['fixture-evidence'], tty=False)
            rs.validate_project(path)
            self.assertEqual(rs.replay_project(path)['state']['gates']['pilot']['decision'], 'passed')

    def test_prior_human_decision_can_be_recorded_without_terminal(self):
        with tempfile.TemporaryDirectory() as path:
            self.project_with_evidence(path)
            rs.record_gate(path, gate='adopted', decision='passed', evidence_ids=['fixture-evidence'],
                           actor='synthetic-user', actor_kind='human', human_approved=True, tty=False)
            rs.validate_project(path)

    def test_pilot_still_requires_evidence(self):
        with tempfile.TemporaryDirectory() as path:
            self.project_with_evidence(path)
            with self.assertRaises(rs.ValidationError):
                rs.record_gate(path, gate='pilot', decision='passed', tty=False)


if __name__ == '__main__':
    unittest.main()
