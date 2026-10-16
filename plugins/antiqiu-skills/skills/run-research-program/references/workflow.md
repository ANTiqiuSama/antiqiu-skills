# Durable Research Workflow

The current objective owns intent and acceptance; the append-only ledger records events and evidence. Reuse state and meaningful checkpoints rather than reinitializing on each question or wakeup.

## Exploration and confirmation

Exploration follows a scientific question, useful baseline, small implementation/analysis, bounded run and interpretation. Retain configuration, data exposure and all outcomes, then continue the next useful trial. A new hypothesis does not require a new release pipeline.

For confirmation and manuscript release, use the applicable dependencies: question/scope/budget; competing hypotheses and prior work; traceable literature/evidence; registered metrics, controls, exclusions and analysis; fair baseline reproduction; pilot instrumentation; planned runs/seeds; primary and labeled exploratory analysis; source-linked manuscript; independent review; authorized release/archive. Apply only the stages required by the requested deliverable. Pilot execution uses existing local authorization; publication requirements constrain publication.

## Scheduler

`next` returns `ready`, `resume`, `checkpoint`, `awaiting_gate`, `blocked`, `complete` or `invalid`, with a reason. Ready ordering is priority, stage, creation order and task ID; explicit dependencies determine readiness, so priority never bypasses a required input.

`checkpoint` means registered tasks finished: consult the current objective for further scientific work. `awaiting_gate` requires a recorded release-stage task or release gate. An unrelated old draft, independent replication or release review is not an automatic dependency of exploration.

A running attempt is not stale merely because time passed. Resume or explicitly replace it while preserving its outputs/logs. Each task uses a unique scientific-question/evidence-gap key; add work for useful hypotheses, contradictions, missing comparisons or other concrete gaps, not to consume a quota.

Update affected objective facts, actions and completion conditions before dependent work. Replace superseded instructions in the current body, keep historical evidence links, and recheck only affected evidence.

## Recovery

Immutable events are authoritative records and `project.json` is their replayable snapshot; neither replaces latest user intent. Mutations lock, append an atomic event, then atomically update the snapshot. Recovery replays committed events. Identical request IDs are idempotent; reuse with changed payload is an error.
