---
name: diagnose-work
description: Locate the cause of a non-obvious failure or evaluate code-review feedback against current evidence before changing behavior. Use for bugs, regressions, performance problems, flaky tests, or review comments that are ambiguous, conflicting, or technically uncertain; skip errors whose cause and safe correction are already explicit.
---

# Diagnose Work

Treat errors and review comments as hypotheses. Diagnose only when the user asks for diagnosis; implement a fix only when the request includes it.

## Establish the evidence

Capture the exact failure or complete feedback, affected behavior, environment, recent changes, requirements, and relevant tests. Prefer the smallest reliable reproduction; when it is unsafe or expensive, gather logs or state instead.

## Follow the matching path

For a failure:

1. Trace inputs and outputs until the first divergence.
2. State one concrete cause hypothesis and its evidence.
3. Run the cheapest observation that distinguishes it from alternatives.
4. After two unsupported hypotheses, stop stacking fixes and re-check assumptions or compare a known-good path.

For review feedback:

1. Group related comments and clarify only meaning that changes implementation.
2. Check each claim against code, requirements, compatibility, and tests.
3. Classify it as `accept`, `adapt`, `defer`, or `reject`.
4. Explain technical pushback with evidence, not agreement or defensiveness.

## Correct only when authorized

Make the smallest root-cause change, then rerun the reproduction and a proportionate regression check. Add a regression test when recurrence risk justifies it, not as automatic ceremony.

Use `root-cause-tracing.md` for deep call chains and `condition-based-waiting.md` for timing-sensitive behavior. Treat extra guards as a separate hardening decision: add them only when an observed bypass path, real consumer, or material failure impact justifies the additional layer. Do not automatically validate every layer.
