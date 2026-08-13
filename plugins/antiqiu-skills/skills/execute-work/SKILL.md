---
name: execute-work
description: Carry an accepted plan or known multi-step checklist through verified completion. Use when the direction is settled and the user wants implementation to continue without repeated approval; skip planning, diagnosis-only requests, and routine single-step answers.
---

# Execute Work

Complete the requested outcome, keep the plan current, and verify what materially changed.

## Execute

1. Inspect the current state and first dependency.
2. Track the real steps, with at most one item in progress.
3. Work sequentially unless steps are genuinely independent and parallel work is authorized.
4. After a meaningful change, run the smallest check that can catch its likely failure.
5. Revise the plan when evidence invalidates an assumption; do not follow stale steps mechanically.
6. Continue until the outcome is complete or genuinely blocked.

Do not pause between routine plan items. Do not require worktrees, subagents, separate reviewers, per-step commits, or full-suite tests unless scope or risk supports them.

## Verify completion

Before claiming completion:

1. Identify the user-visible outcome and most likely remaining failure.
2. Choose the smallest fresh check that can detect it.
3. Run the check and inspect its exit status and relevant output.
4. Use a native validator for generated artifacts.
5. Broaden testing only for shared contracts, unknown consumers, destructive changes, releases, or high-impact risk.

Do not rerun settled checks against unchanged evidence. If no practical verification exists, state the limitation and strongest available evidence.

## Pause only when needed

Pause for a missing decision that materially changes the result, unauthorized destructive or external work, missing access or data, or repeated failure showing the approach is unsound.

Report the outcome, verification evidence, and material remaining risk. Merge, push, publish, communicate externally, or clean branches only when requested.
