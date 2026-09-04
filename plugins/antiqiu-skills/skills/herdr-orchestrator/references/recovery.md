# Runtime recovery

Use the lowest-cost signal that can answer the question.

## Observation order

1. Read all agent names, states, and `state_change_seq` values with
   `herdr agent list`.
2. Check whether the expected artifact exists and is changing.
3. Use `herdr agent explain <name> --format text` when the state is unclear.
4. Use `herdr agent read <name> --source recent-unwrapped --lines 40` for the
   final screen evidence.

Do not poll without a trigger. Inspect after a wait timeout, `unknown`, a
missing agent, an exceeded estimate, or a settled state without its artifact.

## Common cases

| Signal | Meaning | Action |
| --- | --- | --- |
| `agent prompt --wait` timed out | The observer timed out; the turn may still run | Check state and artifact; wait again without resending |
| `blocked` | Human approval or question | Read and surface the exact prompt; user answers in that tab |
| `unknown` | Detection is obscured or inconclusive | Run `agent explain`; close only a harmless viewer overlay when confirmed |
| Agent returned to idle, artifact missing | Early exit, wrong prompt target, or transport truncation | Read recent output; continue from partial work rather than restarting |
| Agent disappeared | Process exited | Inspect the pane; rebuild only that worker and pass existing artifact paths |
| Context remains at zero after a request | Often a rejected runtime parameter | Check endpoint/model/effort configuration before retrying |
| Model label is not the configured route | Tab environment did not apply | Recreate the tab with the complete environment |

## Retry and stop rules

For transient errors, try the same route twice with increasing delay. Then try
one equivalent route if the user configured one. Report every route change.

Do not retry unchanged authentication, permission, model-not-found, invalid
parameter, or context-limit failures. Correct the cause first.

For a poor or off-scope artifact, give one correction that identifies the failed
acceptance criterion. A second full rewrite is not an independent review.

Stop the orchestration when:

- the same non-transient failure happens twice;
- two correction rounds produce no substantive change;
- ten minutes pass with no artifact and no state transition;
- an unattended agent is waiting for approval.

Stopping the observer does not stop the worker. To cancel work, use an explicit
agent interruption only when the user asked to stop that task.

## Acceptance after recovery

Recovery is complete only when the expected artifact is fresh and non-empty and
the original acceptance command passes. Do not downgrade acceptance because a
provider was unstable. If a route change weakens review independence, state it.
