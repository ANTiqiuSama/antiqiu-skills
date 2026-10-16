"""Exercise research continuation separately from release authorization."""
import tempfile
import unittest
from pathlib import Path

import research_state as rs


class ResearchProgressTests(unittest.TestCase):
    def completed_trial(self, path, stage='experimentation'):
        rs.init_project(path, title='Exploratory comparison', question='Does the candidate alter the measured quantity?')
        rs.add_task(path, task_id='TRIAL', title='Run one comparison', stage=stage,
                    gap_key='candidate-comparison', acceptance=['Comparison result is retained.'])
        rs.start_task(path, task_id='TRIAL')
        (Path(path) / 'result.txt').write_text('Synthetic fixture result; no scientific claim.', encoding='utf-8')
        rs.complete_task(path, task_id='TRIAL', artifacts=['result.txt'])

    def test_completed_diagnostic_is_checkpoint_without_release_request(self):
        with tempfile.TemporaryDirectory() as path:
            self.completed_trial(path)
            self.assertEqual(rs.next_action(path)['status'], 'checkpoint')
            state = rs.replay_project(path)['state']
            self.assertFalse(state['project']['completed'])
            self.assertEqual(state['gates'], {})
            rs.validate_project(path)

    def test_actual_release_request_still_awaits_its_decision(self):
        with tempfile.TemporaryDirectory() as path:
            self.completed_trial(path, stage='release')
            self.assertEqual(rs.next_action(path)['status'], 'awaiting_gate')
            with self.assertRaises(rs.ValidationError):
                rs.record_gate(path, gate='release', decision='passed',
                               actor_kind='automation', human_approved=False)
            self.assertFalse(rs.replay_project(path)['state']['project']['completed'])

    def test_next_scientific_task_can_follow_diagnostic_checkpoint(self):
        with tempfile.TemporaryDirectory() as path:
            self.completed_trial(path)
            rs.add_task(path, task_id='REFIT', title='Fit the changed feature model',
                        stage='experimentation', gap_key='changed-feature-refit',
                        dependencies=['TRIAL'], acceptance=['Both fitted variants and outcomes are retained.'])
            self.assertEqual(rs.next_action(path)['tasks'][0]['id'], 'REFIT')
            self.assertEqual(rs.start_task(path, task_id='REFIT')['status'], 'in_progress')
            rs.validate_project(path)

    def test_unrelated_old_protocol_is_not_a_pilot_dependency(self):
        with tempfile.TemporaryDirectory() as path:
            rs.init_project(path, title='Research', question='Compare a new idea.')
            rs.add_task(path, task_id='OLD-DRAFT', title='Older confirmation draft',
                        stage='protocol', gap_key='old-protocol', acceptance=['Original draft remains recorded.'])
            rs.add_task(path, task_id='PILOT', title='Independent exploratory implementation',
                        stage='implementation', gap_key='new-pilot', priority=90,
                        acceptance=['Minimal working implementation exists.'])
            self.assertEqual(rs.next_action(path)['tasks'][0]['id'], 'PILOT')
            self.assertEqual(rs.start_task(path, task_id='PILOT')['status'], 'in_progress')
            state = rs.replay_project(path)['state']
            self.assertEqual(state['tasks']['OLD-DRAFT']['status'], 'ready')
            rs.validate_project(path)

    def test_priority_cannot_bypass_a_real_dependency(self):
        with tempfile.TemporaryDirectory() as path:
            rs.init_project(path, title='Research', question='Run a dependent comparison.')
            rs.add_task(path, task_id='INPUTS', title='Prepare required input',
                        stage='implementation', gap_key='required-input',
                        acceptance=['Required input exists.'])
            rs.add_task(path, task_id='RUN', title='Run the comparison',
                        stage='experimentation', gap_key='dependent-run', priority=100,
                        dependencies=['INPUTS'], acceptance=['Comparison exists.'])
            self.assertEqual(rs.next_action(path)['tasks'][0]['id'], 'INPUTS')
            with self.assertRaises(rs.ConflictError):
                rs.start_task(path, task_id='RUN')
            self.assertEqual(rs.replay_project(path)['state']['tasks']['RUN']['status'], 'pending')


if __name__ == '__main__':
    unittest.main()
