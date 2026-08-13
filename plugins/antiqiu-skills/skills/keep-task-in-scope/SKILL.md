---
name: keep-task-in-scope
description: Keep long-running or scope-ambiguous work on the requested critical path. Use for open-ended improvement loops, SOTA or publication goals, or decisions about hashes, freezes, audits, migrations, compatibility, hardening, broad tests, dependencies, abstractions, and infrastructure when optional process may delay delivery; skip routine direct changes.
---

# Keep Task in Scope

Apply this workflow silently. Surface it only when a real scope decision or tradeoff affects the user.

## Anchor the task

Identify the requested deliverable and the smallest check that would prove it complete. Do not turn this into a required status template.

Treat the user's latest explicit correction, prohibition, resource limit, or phase instruction as an active constraint. When it conflicts with an older broad goal, apply the newer and more specific instruction for the current phase. Do not comply with one literal detail while preserving the same displaced workflow under a different name.

## Bound open-ended improvement

Treat "continue improving", "reach SOTA", and "meet top-tier standards" as directions, not terminal conditions. Before an experiment cycle, identify:

- the hypothesis being tested;
- the metric or observation that would support or reject it;
- a resource or attempt boundary for this cycle;
- the keep, roll-back, or stop decision that follows.

Do not increment a version merely to keep the loop alive. If a cycle produces no decision-relevant evidence, stop that line of iteration instead of wrapping it in another protocol.

## Classify the phase

- **Exploration:** change mechanisms and test hypotheses quickly. Reuse one experiment ledger and lightweight checks; do not create a freeze package for every attempt.
- **Confirmation:** lock a selected candidate before independent or held-out evaluation. Statistical checks, provenance, and a single candidate freeze can be necessary here.
- **Release:** package the accepted result for another person or system. Manifests, checksums, compatibility notes, and reproducibility artifacts belong here when a real consumer needs them.

Do not import release discipline into every exploratory iteration. Do not use this rule to weaken valid leakage controls or reproducibility at an actual confirmation or release boundary.

## Gate auxiliary work

Before adding work outside the direct path, establish:

- **Evidence:** a supported input can reach it, a real consumer or threat exists, the user or project requires it, or an observed change creates it.
- **Consequence:** the concrete failure or cost being prevented.
- **Decision impact:** what implementation, release, rollback, or follow-up changes if the result differs.
- **Proportion:** why this is the lowest-lifecycle-cost response to that evidence.

If the first three are absent, keep the work out of the current implementation. Mention it only when the option would materially help the user decide.

## Sequence work

Keep evidence-backed critical risks on the main path. Otherwise complete the smallest end-to-end requested slice before optional hardening, refactoring, research, or process work. Ask only when the missing choice would materially change the result or make an action hard to reverse.

Treat repeated governance artifacts, version changes without a new hypothesis, and verification of unchanged evidence as drift signals. A signal triggers a scope check, not an automatic verdict: the work may still be required by the current phase.

At completion, use `execute-work` for proportionate verification. When a formal delivery plan is needed, use `plan-work` only after this Skill has bounded the current phase and optional work.

## Re-anchor sparingly

Re-anchor on a new task, a changed deliverable or correction, resumed or compacted context, a phase transition, or when auxiliary work begins to displace the requested outcome. Do not repeat the rules on a timer or in routine progress updates. For the same unchanged decision, run the scope gate once; reopen it only when evidence, phase, or user intent changes.
