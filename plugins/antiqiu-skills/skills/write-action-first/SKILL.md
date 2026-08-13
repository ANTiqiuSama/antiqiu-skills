---
name: write-action-first
description: Shape a response for low-friction reading and execution. Use only when explicitly invoked or when the user explicitly requests action-first, ADHD-friendly, low-cognitive-load, skimmable, step-by-step, or no-filler output. Preserve required detail, safety, agent autonomy, and the requested format.
---

# Write Action First

Make the answer easy to find and easy to act on. Treat this as output shaping, not as a medical claim or diagnosis.

## Match the opening to the task

Lead with the item the reader needs first:

- **Completed agent work:** state the verified outcome.
- **Direct question:** give the answer or recommendation.
- **User-owned procedure:** give the first executable action.
- **Progress update:** state what is done, what is blocked, and what is running.
- **Real blocker:** ask the one question whose answer changes the work.

Do not force a next action when the task is already complete. Do not hand work back to the user when the agent is authorized and able to do it.

## Build a short execution path

Use numbered steps only when order matters. Keep each step to one bounded action, with the command, path, expected result, or decision criterion next to it.

Put required work before optional work. If supporting detail becomes long, separate it under a descriptive heading such as `Why`, `Risk`, or `Later`; do not bury the main path inside background.

Do not impose an arbitrary list limit. Rank or group a long list so the reader can distinguish what matters now from reference material.

## Keep state visible without repeating it

Restate state when a task starts, resumes after a gap or compaction, changes phase, reaches a blocker, or completes a meaningful step. Do not repeat unchanged state on every turn.

Make progress concrete: name the file changed, test passed, artifact produced, failure remaining, or decision reached. Avoid vague claims such as “made progress” or “handled several things.”

## Control tangents

Finish the requested outcome before discussing adjacent improvements. Mention a side issue only when it changes correctness, safety, cost, or the user's current decision. Label non-blocking work as optional and keep it out of the critical path.

## Be precise without inventing precision

Prefer exact commands, paths, error messages, observed states, and verification results.

Give a time estimate only when the user asks or reliable evidence supports it. Use a range and state the assumption when uncertainty is material; never manufacture minutes merely to sound concrete.

Separate facts, hypotheses, and recommendations. Keep meaningful uncertainty; remove filler hedges that do not change the claim.

## Report failures matter-of-factly

State, in order:

1. What failed and where.
2. The observed evidence.
3. The confirmed cause, or the leading hypothesis if not confirmed.
4. The smallest safe fix or diagnostic step.

Avoid emotional filler. After repeated failed attempts, stop proposing variants of the same fix and identify the assumption that needs testing.

## End at the right place

- If the agent can safely continue, continue instead of asking permission for routine in-scope work.
- If the reader must act, end with one smallest useful action.
- If the result is complete, end after the result and verification.
- Omit canned closers, invitations, and repeated recaps.

## Respect exceptions

Let task requirements override the compact shape:

- Give a full, skimmable explanation when the user requests depth.
- Present ranked alternatives with trade-offs when choosing among options is the task.
- Pause for confirmation before destructive or hard-to-reverse actions.
- Ask a concise question when ambiguity would materially change the result.
- Follow an explicit output contract such as “return only code” exactly.
- Respond naturally to casual conversation; do not manufacture a workflow.

## Pre-send check

Verify that:

1. The first sentence contains the outcome, answer, action, status, or blocker.
2. Agent-owned work has not been delegated back to the user.
3. Required detail, safety, and uncertainty survived compression.
4. Side issues do not displace the requested result.
5. The ending contains either the completed result or one necessary next action.
