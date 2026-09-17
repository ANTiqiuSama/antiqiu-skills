"""Offline tests for the prompt gate and disposable native configuration."""

import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

import antigravity_worker as worker


class RetainedBytes(io.BytesIO):
    def close(self):
        self.closed_value = self.getvalue()
        super().close()


class AntigravityWorkerTests(unittest.TestCase):
    def event(self, work):
        return {'event': 'init', 'init': {
            'cwd': str(work), 'model': worker.MODEL, 'agent': worker.AGENT_NAME,
            'tools': ['view_file'], 'permission_mode': 'strict'}}

    def test_valid_init_sends_exactly_one_stdin_prompt(self):
        pipe = RetainedBytes()
        work = Path('/tmp')
        gate = worker.InputGate(Mock(stdin=pipe), 'Synthetic material', work, True)
        gate(self.event(work))
        self.assertTrue(gate.initialized)
        self.assertEqual(json.loads(pipe.closed_value)['message']['content'], 'Synthetic material')
        with self.assertRaises(ValueError):
            gate(self.event(work))

    def test_unexpected_permissions_identity_or_workspace_prevents_prompt(self):
        for changed in ({'tools': None}, {'permission_mode': 'always-proceed'}, {'model': 'other'},
                        {'agent': 'other'}, {'cwd': '/'}):
            with self.subTest(changed=changed):
                pipe = io.BytesIO()
                work = Path('/tmp')
                gate = worker.InputGate(Mock(stdin=pipe), 'Synthetic material', work, True)
                event = self.event(work)
                event['init'].update(changed)
                with self.assertRaises(ValueError):
                    gate(event)
                self.assertEqual(pipe.getvalue(), b'')

    def test_unverified_policy_prevents_prompt(self):
        pipe = io.BytesIO()
        work = Path('/tmp')
        gate = worker.InputGate(Mock(stdin=pipe), 'Synthetic material', work)
        with self.assertRaises(ValueError):
            gate(self.event(work))
        self.assertEqual(pipe.getvalue(), b'')

    def test_tools_and_subagent_results_are_rejected(self):
        gate = worker.InputGate(Mock(), 'Synthetic material', Path('/tmp'))
        for step in ({'step_type': 'tool'}, {'tool_info': {'name': 'read_file'}},
                     {'subagent_info': {'subagents': [{}]}}):
            with self.assertRaises(ValueError):
                gate({'event': 'step_update', 'step_update': step})

    def test_disposable_profile_and_credentials_not_in_prompt_or_command(self):
        with tempfile.TemporaryDirectory() as directory:
            auth = Path(directory) / 'auth'
            auth.write_text('synthetic-credential')
            with patch.object(worker, 'AUTH', auth), patch.object(worker, 'AGY', auth), \
                 patch.dict(os.environ, {'GOOGLE_API_KEY': 'synthetic-secret'}):
                with worker.isolated_run() as (command, env, work):
                    root = work.parent
                    self.assertEqual(list(work.iterdir()), [])
                    self.assertNotIn('GOOGLE_API_KEY', env)
                    self.assertNotIn('synthetic-credential', str(command))
                    self.assertEqual(env.get('HOME'), os.environ.get('HOME'))
                    self.assertEqual((root / 'profile/antigravity-cli/antigravity-oauth-token').resolve(), auth.resolve())
                    settings = json.loads((root / 'profile/antigravity-cli/settings.json').read_text())
                    self.assertFalse(settings['allowNonWorkspaceAccess'])
                    self.assertEqual(settings['permissions']['allow'], [])
                self.assertFalse(root.exists())
                self.assertEqual(auth.read_text(), 'synthetic-credential')


if __name__ == '__main__':
    unittest.main()
