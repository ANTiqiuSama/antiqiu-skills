#!/usr/bin/env python3
"""Run a local Antigravity or Grok Build CLI with an isolated text task."""

import argparse
import json
import os
import signal
import subprocess
import sys


def stop_process(process):
    if process.poll() is not None:
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('role', choices=('antigravity', 'grok'))
    parser.add_argument('--context-class', required=True,
                        choices=('public', 'sanitized', 'synthetic'),
                        help='Caller has checked that this input may be shared externally.')
    parser.add_argument('--timeout', type=int,
                        help='Total seconds: Antigravity defaults to 300; Grok to 0 (unlimited).')
    parser.add_argument('--idle-timeout', type=int, default=0,
                        help='Grok only: seconds without stream progress; 0 disables the limit.')
    parser.add_argument('--task-mode', choices=('debate', 'implement'),
                        help='Grok only: debate (default) or implementation output.')
    args = parser.parse_args()
    if args.timeout is None:
        args.timeout = 0 if args.role == 'grok' else 300
    if args.timeout < 0 or (args.role == 'antigravity' and args.timeout == 0):
        parser.error('--timeout must be positive; Grok also accepts 0 for unlimited')
    if args.idle_timeout < 0:
        parser.error('--idle-timeout must be nonnegative')
    if args.role == 'antigravity' and (args.task_mode or args.idle_timeout):
        parser.error('--task-mode and --idle-timeout apply only to Grok')
    if sys.stdin.isatty():
        parser.error('Pass the task through standard input')
    prompt = sys.stdin.read().strip()
    if not prompt:
        parser.error('The task is empty')
    try:
        if args.role == 'antigravity':
            from antigravity_worker import run
            output, code = run(prompt, args.timeout, args.context_class, stop_process)
        else:
            from grok_worker import run
            output, code = run(prompt, args.timeout or None, args.context_class,
                               stop_process, args.idle_timeout or None, args.task_mode or 'debate')
    except KeyboardInterrupt:
        return 130
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
