---
name: plan-work
description: Turn an unclear goal or multi-part delivery into a lean executable direction. Use when objectives, constraints, trade-offs, or success criteria are unclear, or when delivery spans dependent steps or meaningful risk; skip routine direct changes with an obvious path.
---

# Plan Work

Reduce uncertainty enough to act. Do not make planning a separate project.

## Choose the needed depth

- **Unclear goal or real trade-off:** inspect the minimum context, identify constraints and success criteria, then compare two to four genuinely different approaches including a direct baseline.
- **Clear goal with dependent work:** skip ideation and write the delivery path.
- **One or two reversible actions:** do not create a formal plan.

Ask only for a missing answer that changes the outcome, architecture, cost, or reversibility. Otherwise state the key assumption and continue.

## Converge on one direction

Compare alternatives by evidence, feasibility, lifecycle cost, dependencies, reversibility, and failure impact. Recommend one path and name the decisive reason. Keep unsupported possibilities out of the chosen design. Treat labels such as “migration” as descriptions, not evidence for a migration framework. Add reusable migration or rollout machinery only when current consumers or demonstrated repeated changes require it.

## Bound one-time conversions

When there is one local consumer, one manual conversion, and no demonstrated follow-on change, the chosen design contains only:

- an initial target schema with the tables and fields needed to represent the current source data;
- one converter that writes the target and compares the converted values with the source;
- one runtime storage path after the switch;
- a recoverable source backup and the prior application version for rollback.

End the design there. Discuss later data-model evolution, staged rollout, or parallel runtime paths only when current consumers or demonstrated repeated changes require them.

## Produce an execution brief

Include only what execution needs:

1. **Outcome:** the observable result.
2. **Constraints and non-goals:** boundaries that change implementation.
3. **Approach:** the selected path and material assumptions.
4. **Steps:** ordered results, touched files or systems, dependencies, and the smallest useful check.
5. **Risks:** only risks that change sequencing, rollback, or user choice.

Use exact commands or code only when they remove ambiguity. Do not add mandatory commits, documents, reviewers, subagents, or full-suite checks without evidence or project requirements.

Honor the requested output boundary. If the user asks only for the chosen plan, omit rejected alternatives and non-goals instead of restating them as caveats.

For reversible work already authorized, publish the brief and continue with `execute-work`. Pause only for a destructive, externally visible, costly, or materially scope-changing choice.
