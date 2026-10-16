"""Public launcher boundaries: no model calls and no real login required."""

import os
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import run_agent


SCRIPT = Path(__file__).resolve().with_name('run_agent.py')


class ReconfigurableStringIO(io.StringIO):
    def reconfigure(self, **kwargs):
        pass


class LauncherTests(unittest.TestCase):
    def invoke(self, *args):
        return subprocess.run([sys.executable, '-B', str(SCRIPT), *args],
                              input='Synthetic task', capture_output=True, text=True, timeout=5)

    def test_only_native_roles_are_accepted(self):
        for role in ('simple', 'complex', 'unknown'):
            self.assertEqual(self.invoke(role, '--context-class', 'synthetic').returncode, 2)

    def test_context_declaration_and_role_options_are_enforced(self):
        for args in (('grok',),
                     ('grok', '--context-class', 'synthetic', '--allow-write'),
                     ('antigravity', '--context-class', 'synthetic', '--task-mode', 'implement'),
                     ('antigravity', '--context-class', 'synthetic', '--timeout', '0')):
            self.assertEqual(self.invoke(*args).returncode, 2)
        missing = self.invoke('grok', '--context-class', 'synthetic', '--output',
                              str(Path('missing-output-dir') / 'review.json'))
        self.assertEqual(missing.returncode, 2, missing.stderr)
        finite_without_budget = self.invoke('grok', '--context-class', 'synthetic', '--revision',
                                             'sha256:synthetic', '--timeout', '120')
        self.assertEqual(finite_without_budget.returncode, 2, finite_without_budget.stderr)

    def test_grok_launcher_defaults_to_unlimited_total_and_idle_timeouts(self):
        stdin = ReconfigurableStringIO('Synthetic task')
        stdout = ReconfigurableStringIO()
        with patch.object(run_agent.sys, 'argv', [str(SCRIPT), 'grok', '--context-class', 'synthetic',
                                                  '--revision', 'sha256:synthetic']), \
             patch.object(run_agent.sys, 'stdin', stdin), patch.object(run_agent.sys, 'stdout', stdout), \
             patch('grok_worker.run', return_value=({'status': 'error', 'role': 'grok'}, 1)) as run:
            self.assertEqual(run_agent.main(), 1)
        self.assertIsNone(run.call_args.args[1])
        self.assertIsNone(run.call_args.args[4])
        receipt = json.loads(stdout.getvalue())
        self.assertEqual(receipt['requested_reasoning_effort'], 'xhigh')
        self.assertIsNone(receipt['launch_reasoning_effort'])
        self.assertEqual(receipt['effort_evidence'], 'not_launched')

    def test_relocated_package_without_login_fails_before_inference(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / 'relocated skill/scripts'
            shutil.copytree(SCRIPT.parent, package, ignore=shutil.ignore_patterns('__pycache__'))
            env = dict(os.environ, HOME=str(root / 'new-home'), PATH=str(root / 'empty-bin'))
            for role in ('antigravity', 'grok'):
                role_args = [role, '--context-class', 'synthetic']
                if role == 'grok':
                    role_args.extend(['--revision', 'sha256:synthetic'])
                result = subprocess.run(
                    [sys.executable, '-B', str(package / SCRIPT.name), *role_args], input='Synthetic task',
                    env=env, cwd=root, capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn('CLI is unavailable', result.stdout)


if __name__ == '__main__':
    unittest.main()
