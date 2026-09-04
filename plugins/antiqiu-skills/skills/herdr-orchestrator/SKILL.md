---
name: herdr-orchestrator
description: Coordinate cross-vendor coding and research agents through Herdr with explicit roles, isolated write scopes, artifact-based acceptance, and bounded recovery. Use when the user explicitly asks to operate Herdr, coordinate Codex, Claude Code, Antigravity or Gemini across Herdr tabs, inspect a Herdr fleet, or build a multi-agent debate and execution workflow. Do not trigger for ordinary in-process delegation or a single small task that does not need Herdr.
---

# Herdr Orchestrator

Use Herdr as the terminal and lifecycle control plane. Keep model routing,
task ownership, and delivery evidence explicit.

## Choose the operating mode

- For an explanation or tutorial, answer without controlling a live session.
- For live inspection or control, first run:

```bash
test "${HERDR_ENV:-}" = 1
```

If the check fails, stop live control. Tell the user to start or resume the
coordinator inside a Herdr-managed pane. Do not target the focused Herdr
session from an unrelated terminal.

Before composing commands from memory, run `herdr --skill`. The installed
binary is authoritative for CLI syntax and lifecycle semantics.

## Keep the coordinator independent

The coordinator owns the task graph, assignments, status, evidence gates, and
user-facing report. By default it does not edit the same deliverable that it
later accepts, and it does not review its own implementation.

Honor user-selected agents and models. Explain a material loss of independence
or higher cost once, then follow the choice unless it would cross an approval,
permission, or destructive-action boundary.

Do not create a fleet for one small action that the current agent can complete
more safely and quickly.

## Select the topology

- One independent writable task gets one Git worktree and one Herdr workspace.
- One long-lived worker gets one tab. Do not divide a narrow pane among agents.
- Read-only investigation can share a project workspace and needs no worktree.
- Workers that share a worktree must write serially or have disjoint write sets.
- Mobile builds, signing, simulators, and attached devices are shared resources;
  serialize them unless isolation is proven.
- Use the project root as `cwd`. Do not use filesystem `/` as a shortcut for
  broad access.

Always pass an explicit workspace and `cwd` when creating background tabs.
Read pane and workspace IDs from command JSON. Never infer them from sidebar
order or an earlier session.

## Run the orchestration loop

1. Confirm the outcome, source of truth, allowed writes, acceptance command,
   and actions that require the user.
2. Inspect `herdr agent list`, the current workspace, and installed
   integrations. Reuse a suitable idle worker instead of creating a duplicate.
3. Create all independent tabs before waiting. Start one named agent in each
   new root pane.
4. Send every independent assignment, then wait. Do not prompt one worker and
   block before dispatching the rest.
5. Track task progress by artifact and acceptance signals. Lifecycle state is
   supporting evidence, not delivery evidence.
6. Present disagreements without erasing them. Route the accepted decision to
   one writer or implementer.
7. Run the acceptance command from the task worktree. Add independent review
   when the user requested debate, the change is high risk, or evidence conflicts.
8. Report results and unresolved decisions. Clean up only resources created for
   this task and only after the user no longer needs them.

Use this assignment shape for every worker:

```markdown
**Outcome** <one observable result>
**Read first** `<brief or source paths>`
**Allowed reads** `<paths or systems>`
**Allowed writes** only `<paths>`
**Constraints**
- Do not delegate again.
- Do not change unrelated files or external systems.
- Separate facts, inference, and proposals.
**Acceptance** `<executable check or review criterion>`
**Return** Write the complete artifact to `<path>`; reply with the path and done/blocked.
```

Put long shared context in one brief file. Keep prompts small enough to inspect
in the tab. Require durable file output when terminal alternate-screen history
may be lost.

## Treat state and delivery separately

Interpret states narrowly:

- `idle`: ready for input.
- `done`: background work settled and has not been viewed.
- `blocked`: waiting for a human decision or approval.
- `unknown`: Herdr cannot classify the agent; it is not completion.

A task passes only when its expected artifact exists, is non-empty and fresh,
and the acceptance command or review criterion passes. If the task changes a
repository, inspect the actual diff or delegate that inspection to an
independent reviewer.

If `agent prompt --wait` times out, do not resend the prompt. Inspect
`agent get`, `agent read`, state changes, and the artifact. The worker may still
be running.

Never answer an approval dialog with `send-keys` on the user's behalf. Surface
the exact question and its workspace/tab location.

## Bound recovery

Classify failures before retrying:

- Transient transport, rate-limit, or backend failures: retry twice with
  increasing delay, then try one equivalent configured route.
- Deterministic authentication, model, parameter, context, or permission
  failures: fix the configuration before retrying.
- Task-quality failures: issue one focused correction, then report the gap.

Stop and report when the same non-transient failure repeats, two correction
rounds make no substantive progress, ten minutes pass with no artifact or state
change, or an unattended worker needs approval.

Read [references/recovery.md](references/recovery.md) when a worker times out,
disappears, becomes `unknown`, or returns to idle without its artifact.

## Load only relevant details

- Read [references/providers.md](references/providers.md) before configuring a
  model, a custom Claude-compatible endpoint, Codex environment inheritance, or
  Antigravity.
- Read [references/paper-workflow.md](references/paper-workflow.md) for paper
  review, cross-model debate, manuscript editing, figures, or experiment gaps.

The human-facing tutorial is published separately in the repository `docs/`
directory; it is not required at runtime.
