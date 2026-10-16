#!/usr/bin/env python3
"""Run a local Antigravity or Grok Build CLI with an isolated text task."""

import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import sys


def stop_process(process):
    if process.poll() is not None:
        return
    if os.name == 'nt':
        subprocess.run([os.path.join(os.environ['SYSTEMROOT'], 'System32', 'taskkill.exe'),
                        '/PID', str(process.pid), '/T', '/F'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       timeout=3, creationflags=subprocess.CREATE_NO_WINDOW)
        if process.poll() is None:
            process.kill()
        process.wait(timeout=2)
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        process.wait()
    except ProcessLookupError:
        pass


def main():
    if os.name == 'nt':
        sys.stdin.reconfigure(encoding='utf-8')
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('role', choices=('antigravity', 'grok'))
    parser.add_argument('--context-class', required=True,
                        choices=('public', 'sanitized', 'synthetic'),
                        help='Caller has checked that this input may be shared externally.')
    parser.add_argument('--timeout', type=int,
                        help='Total seconds; default is unlimited for Grok and 300 for Antigravity.')
    parser.add_argument('--budget',
                        help='Explicit task budget authorizing any finite Grok timeout.')
    parser.add_argument('--idle-timeout', type=int, default=0,
                        help='Grok only: seconds without stream progress; 0 disables the limit.')
    parser.add_argument('--task-mode', choices=('debate', 'implement'),
                        help='Grok only: debate (default) or implementation output.')
    parser.add_argument('--output', type=Path,
                        help='Write the JSON result to this file. Its parent directory must exist.')
    parser.add_argument('--revision',
                        help='Immutable review-packet revision; required for Grok review receipts.')
    args = parser.parse_args()
    if args.timeout is None:
        args.timeout = 0 if args.role == 'grok' else 300
    if args.timeout < 0 or (args.role == 'antigravity' and args.timeout == 0):
        parser.error('--timeout must be positive; Grok also accepts 0 for unlimited')
    if args.idle_timeout < 0:
        parser.error('--idle-timeout must be nonnegative')
    if args.role == 'antigravity' and (args.task_mode or args.idle_timeout):
        parser.error('--task-mode and --idle-timeout apply only to Grok')
    if args.role == 'antigravity' and args.budget:
        parser.error('--budget applies only to a finite Grok timeout')
    if args.role == 'grok' and ((args.timeout is not None and args.timeout > 0) or args.idle_timeout > 0) and not args.budget:
        parser.error('finite Grok timeouts require an explicit --budget')
    if args.role == 'grok' and (not args.revision or not args.revision.strip()):
        parser.error('--revision is required for a revision-bound Grok review')
    if args.role == 'antigravity' and args.revision:
        parser.error('--revision applies only to Grok review receipts')
    if sys.stdin.isatty():
        parser.error('Pass the task through standard input')
    prompt = sys.stdin.read().strip()
    if not prompt:
        parser.error('The task is empty')
    if args.output and not args.output.parent.is_dir():
        parser.error('--output directory does not exist')
    try:
        if args.role == 'antigravity':
            from antigravity_worker import run
            output, code = run(prompt, args.timeout, args.context_class, stop_process)
        else:
            from grok_worker import run
            output, code = run(prompt, args.timeout or None, args.context_class,
                               stop_process, args.idle_timeout or None, args.task_mode or 'debate')
            output['revision'] = args.revision
            output['exit_code'] = code
            output.setdefault('requested_reasoning_effort', 'xhigh')
            output.setdefault('launch_reasoning_effort', None)
            output.setdefault('effort_evidence', 'not_launched')
            output['task_budget'] = args.budget
    except KeyboardInterrupt:
        return 130
    rendered = json.dumps(output, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(rendered + '\n', encoding='utf-8')
    print(rendered)
    return code


if __name__ == '__main__':
    raise SystemExit(main())
