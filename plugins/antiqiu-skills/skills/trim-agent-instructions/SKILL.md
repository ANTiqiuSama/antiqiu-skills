---
name: trim-agent-instructions
description: Audit and simplify an existing hierarchy of AGENTS.md, AGENTS.override.md, CLAUDE.md, or similar agent-instruction files. Use when removing duplicate, stale, vague, conflicting, or overly procedural rules; preserving directory-specific constraints; or deciding whether an instruction should be kept, shortened, rewritten, or deleted. Skip greenfield instruction design and unrelated routine edits.
---

# Trim Agent Instructions

Improve behavioral signal, not line count. Keep a rule when it changes a useful decision or prevents a demonstrated failure; remove or rewrite it when it only restates defaults, describes vanished machinery, or adds process without changing behavior.

## Resolve the effective instruction chain

Determine how the current agent product discovers and prioritizes instruction files. Do not assume every product uses the same filenames or precedence.

Read only the chain that can affect the requested scope:

1. Start with the highest applicable parent instruction.
2. Follow inherited files down to the target directory.
3. Include child files only when their inherited behavior is part of the audit.
4. Record which rule wins when parent, current, child, user, or system instructions conflict.

Do not scan unrelated trees merely to make the audit look complete.

## Build decision candidates

For each rule or coherent rule group, identify the behavior it is meant to change and the evidence that behavior matters. Useful evidence includes a live path or command, a current consumer, an observed failure, a real project constraint, or a specific decision that would differ without the rule.

Classify each candidate into one outcome:

- **Keep:** specific, current, non-duplicated, and behavior-changing.
- **Delete as obvious:** merely repeats a reliable default or says nothing actionable.
- **Delete as stale:** references removed tools, paths, workflows, or risks.
- **Shorten:** useful behavior is buried in history, examples, or repeated explanation.
- **Improve:** intent matters, but the trigger, action, precedence, or verification is ambiguous.

Treat classifications as decisions, not a mandatory scoring table. Separate observed facts from assumptions and inferences.

## Match evidence depth to uncertainty

Static inspection is enough for a clearly missing path, exact duplicate, empty slogan, or rule contradicted by current project structure.

Use one matched behavior comparison only when all of these are true:

- the rule is high impact;
- static evidence leaves a real keep-or-change ambiguity;
- the result would change the edit decision;
- an isolated fresh session is practical.

Compare the same task and environment with and without the candidate rule. Prevent the supposedly blind run from automatically loading that rule; otherwise describe the result as a qualitative check, not independent evidence. Do not require a subagent, a fixed drill count, or a formal report for every rule.

## Separate authority from evidence

Inspection permission does not authorize edits. A user request to trim or update the instructions authorizes the in-scope change unless they explicitly requested analysis only.

Do not repeatedly ask for confirmation after the user has authorized the edit. Ask only when a choice would materially change behavior, affect a wider scope than requested, or be difficult to reverse. Independently of permission, delete a rule only when the evidence supports deletion.

## Apply the smallest complete change

- Preserve the most specific effective constraint when it still matches reality.
- Remove true duplicates from the narrowest unnecessary layer.
- Turn a vague rule into a concrete trigger, action, and check only when each part has a real purpose.
- Remove incident history after its durable lesson is expressed directly.
- Keep user, system, safety, legal, and repository constraints above stylistic preferences.
- Do not add aliases, tombstones, migration scaffolding, hashes, or versioning without a real consumer.
- Preserve unrelated user edits and the existing file style.

When the audit grows into broad governance or repeated auxiliary work, use `keep-task-in-scope`. When the edit direction is accepted and implementation spans several verified steps, use `execute-work`.

## Verify and stop

Run the cheapest checks that can catch a plausible regression:

- reread the effective instruction chain after editing;
- verify referenced files, paths, and commands that remain;
- run formatting or repository checks that already exist;
- use one fresh-session loading or routing check when precedence or discoverability changed materially.

Report the scope, important keep/change decisions, and verification result. Provide a detailed rule matrix only when the number or risk of decisions makes it useful.

Stop when every remaining rule has a current behavioral purpose or encodes a real constraint. Do not chase an arbitrary reduction percentage, word count, or perfectly uniform style.
