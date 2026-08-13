# Root-cause tracing

Use this reference when the visible failure is several calls or transformations away from the value that first became wrong. Skip it when the cause and safe correction are already explicit.

## Trace the first divergence

1. Record the exact bad output, state, error, and the operation that produced it.
2. Identify the direct inputs to that operation and compare them with a working path when one exists.
3. Follow the incorrect value backward through callers, conversions, defaults, and persistence boundaries.
4. Stop at the earliest point where actual state diverges from required state.
5. Test one observation that distinguishes this cause from the nearest alternative.

For each step, keep a compact chain:

```text
observed failure
  <- direct operation and bad input
  <- caller or transformation
  <- first unsupported value or state transition
```

Temporary instrumentation may help when the chain is hidden. Capture only decision-relevant values, location, and call context; avoid broad logging or credentials. Remove temporary output after diagnosis unless an operational consumer will use it.

## Choose the correction point

Prefer the earliest point the project controls where one small change restores the required invariant. A containment fix nearer the symptom can still be correct when the upstream source is external, risky to change, or intentionally variable; state that constraint instead of pretending the symptom layer is always wrong.

After an authorized fix, rerun the smallest reproduction and one check covering the affected path. Add more validation layers only if a demonstrated alternate path can recreate material harm.

If the trace cannot reach a confirmed cause, report the leading hypothesis, evidence, missing observation, and cheapest next check. Do not stack speculative fixes.
