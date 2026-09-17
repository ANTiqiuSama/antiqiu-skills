"""Public launcher boundaries: no model calls and no real login required."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().with_name('run_agent.py')


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

    def test_relocated_package_without_login_fails_before_inference(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / 'relocated skill/scripts'
            shutil.copytree(SCRIPT.parent, package, ignore=shutil.ignore_patterns('__pycache__'))
            env = dict(os.environ, HOME=str(root / 'new-home'), PATH=str(root / 'empty-bin'))
            for role in ('antigravity', 'grok'):
                result = subprocess.run(
                    [sys.executable, '-B', str(package / SCRIPT.name), role,
                     '--context-class', 'synthetic'], input='Synthetic task',
                    env=env, cwd=root, capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn('CLI is unavailable', result.stdout)


if __name__ == '__main__':
    unittest.main()
