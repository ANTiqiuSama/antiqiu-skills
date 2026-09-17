"""Offline regression tests for the Grok dispatch boundary; no model calls."""

import copy
from contextlib import nullcontext
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import grok_worker
from run_agent import stop_process


class GrokWorkerTests(unittest.TestCase):
    def setUp(self):
        self.events = [
            {'type': 'system', 'subtype': 'init', 'model': 'grok-4.6', 'tools': [],
             'skills': [], 'mcp_servers': [{'name': 'configured-only', 'status': 'connected'}]},
            {'type': 'result', 'subtype': 'success', 'is_error': False,
             'stop_reason': 'end_turn', 'result': 'Synthetic counterexample.',
             'modelUsage': {'grok-4.6-build': {'outputTokens': 10}}},
        ]

    def parse(self, events, code=0, verified=True):
        return grok_worker.parse_response('\n'.join(map(json.dumps, events)),
                                          code, 'grok-4.6', verified)

    def test_complete_response_and_config_metadata(self):
        self.assertEqual(self.parse(self.events)['status'], 'success')

    def test_incomplete_unverified_or_wrong_model_is_not_success(self):
        for index, changes in (
            (0, {'model': 'another-model'}), (0, {'tools': ['read_file']}),
            (0, {'skills': ['external-context']}), (1, {'result': ''}),
            (1, {'stop_reason': 'max_tokens'}), (1, {'is_error': True}),
            (1, {'modelUsage': {}}), (1, {'modelUsage': {'another-model': {}}}),
        ):
            with self.subTest(changes=changes):
                events = copy.deepcopy(self.events)
                events[index].update(changes)
                self.assertEqual(self.parse(events)['status'], 'error')
        self.assertEqual(self.parse(self.events, code=1)['status'], 'error')
        self.assertEqual(self.parse(self.events, verified=False)['status'], 'error')
        self.assertEqual(self.parse(self.events[1:])['status'], 'error')

    def test_client_and_server_tool_calls_are_rejected(self):
        for kind in ('tool_use', 'server_tool_use'):
            tool = {'type': 'assistant', 'message': {'content': [{'type': kind, 'name': 'read_file'}]}}
            self.assertEqual(self.parse(self.events + [tool])['status'], 'error')

    def test_isolated_files_environment_and_cleanup(self):
        with tempfile.TemporaryDirectory() as auth_dir:
            auth = Path(auth_dir)
            (auth / 'auth.json').write_text('{}')
            (auth / 'requirements.toml').write_text('[features]\nweb_fetch = false\n')
            with patch.object(grok_worker, 'GROK', auth / 'auth.json'), \
                 patch.object(grok_worker, 'GROK_AUTH_HOME', auth), patch.dict(os.environ, {
                'GROK_CONFIG': '{"features":{"web_fetch":true}}',
                'ANTHROPIC_API_KEY': 'synthetic-secret',
            }):
                with grok_worker.isolated_run('Synthetic prompt') as (command, env, work, _):
                    root = work.parent
                    self.assertEqual(list(work.iterdir()), [])
                    self.assertNotIn('GROK_CONFIG', env)
                    self.assertNotIn('ANTHROPIC_API_KEY', env)
                    self.assertEqual(env.get('HOME'), os.environ.get('HOME'))
                    self.assertNotIn('Synthetic prompt', command)
                    policy = (root / 'grok-home/requirements.toml').read_text()
                    self.assertIn('allowed_mcp_servers = []', policy)
                    self.assertIn('web_fetch = false', policy)
                    self.assertEqual((root / 'grok-home/auth.json').resolve(), (auth / 'auth.json').resolve())
                self.assertFalse(root.exists())
                self.assertEqual((auth / 'auth.json').read_text(), '{}')

    def test_active_context_prevents_inference(self):
        with tempfile.TemporaryDirectory() as auth_dir:
            auth = Path(auth_dir)
            (auth / 'auth.json').write_text('{}')
            with patch.object(grok_worker, 'GROK', auth / 'auth.json'), \
                 patch.object(grok_worker, 'GROK_AUTH_HOME', auth), \
                 patch.object(grok_worker, 'check_isolation', side_effect=ValueError('active context')), \
                 patch.object(grok_worker.subprocess, 'Popen') as spawn:
                output, code = grok_worker.run('Synthetic prompt', 5, 'synthetic', lambda p: None)
                self.assertEqual(output['status'], 'error')
                self.assertNotEqual(code, 0)
                spawn.assert_not_called()


class GrokStreamTests(unittest.TestCase):
    """Exercise real pipe timing without network calls or model responses."""

    def collect(self, script, timeout=4, idle_timeout=.8, cleanup_timeout=.2):
        with subprocess.Popen([sys.executable, '-u', '-c', script],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              start_new_session=True) as process:
            try:
                stdout, timing = grok_worker.collect_response(
                    process, timeout, idle_timeout, stop_process, cleanup_timeout)
                self.assertIsNotNone(process.poll())
                return stdout, timing
            finally:
                stop_process(process)

    def test_progress_keeps_inference_alive(self):
        stdout, timing = self.collect('''
import json, time
for _ in range(12):
    print(json.dumps({'type': 'stream_event'}), flush=True)
    time.sleep(.1)
print(json.dumps({'type': 'result'}), flush=True)
''')
        self.assertIsNone(timing['timeout_kind'])
        self.assertGreater(timing['response_seconds'], 1)
        self.assertFalse(timing['shutdown_terminated'])
        self.assertEqual(timing['process_exit_code'], 0)
        self.assertIn('result', stdout)

    def test_missing_startup_or_stalled_progress_has_distinct_timeout(self):
        for script, expected in (
            ('import time; time.sleep(10)', 'startup'),
            ('import time; print(\'{"type":"stream_event"}\', flush=True); time.sleep(10)', 'idle'),
        ):
            with self.subTest(expected=expected):
                _, timing = self.collect(script)
                self.assertEqual(timing['timeout_kind'], expected)
                self.assertIsNone(timing['response_seconds'])

    def test_total_deadline_stops_continuing_stream(self):
        _, timing = self.collect('''
import time
while True:
    print('{"type":"stream_event"}', flush=True)
    time.sleep(.05)
''', timeout=.5, idle_timeout=2)
        self.assertEqual(timing['timeout_kind'], 'total')
        self.assertIsNone(timing['response_seconds'])

    def test_no_deadlines_allows_quiet_inference_to_complete(self):
        _, timing = self.collect('''
import time
print('{"type":"stream_event"}', flush=True)
time.sleep(1)
print('{"type":"result"}', flush=True)
''', timeout=None, idle_timeout=None)
        self.assertIsNone(timing['timeout_kind'])
        self.assertGreaterEqual(timing['response_seconds'], 1)
        self.assertEqual(timing['process_exit_code'], 0)

    def test_partial_lines_and_stderr_do_not_hide_progress(self):
        stdout, timing = self.collect('''
import os, time
os.write(2, b'diagnostic' * 10000)
os.write(1, b'{"type":')
time.sleep(.1)
os.write(1, b'"result"}\\n')
''')
        self.assertIsNone(timing['timeout_kind'])
        self.assertIsNotNone(timing['response_seconds'])
        self.assertNotIn('diagnostic', stdout)

    def test_completed_result_survives_hanging_cli_shutdown(self):
        events = [
            {'type': 'system', 'subtype': 'init', 'model': 'grok-4.6',
             'apiKeySource': 'oauth', 'tools': [], 'skills': []},
            {'type': 'result', 'subtype': 'success', 'is_error': False,
             'stop_reason': 'end_turn', 'result': 'Synthetic result.',
             'modelUsage': {'grok-4.6-build': {'outputTokens': 5}}},
        ]
        script = 'import time\n' + '\n'.join(
            f'print({json.dumps(event)!r}, flush=True)' for event in events) + '\ntime.sleep(10)'
        command = [sys.executable, '-u', '-c', script]
        with tempfile.TemporaryDirectory() as work, \
             patch.object(grok_worker, 'isolated_run', return_value=nullcontext(
                 (command, os.environ.copy(), Path(work), 'grok-4.6'))), \
             patch.object(grok_worker, 'check_isolation'):
            output, code = grok_worker.run('Synthetic check', 5, 'synthetic', stop_process)
        timing = output['timing']
        self.assertTrue(timing['shutdown_terminated'])
        self.assertIsNone(timing['timeout_kind'])
        self.assertIsNotNone(timing['response_seconds'])
        self.assertNotEqual(timing['process_exit_code'], 0)
        self.assertEqual(code, 0)
        self.assertEqual(output['status'], 'success')
        self.assertEqual(output['auth_source'], 'oauth')


if __name__ == '__main__':
    unittest.main()
