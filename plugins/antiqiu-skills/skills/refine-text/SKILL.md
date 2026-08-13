---
name: refine-text
description: Refine existing text while preserving intent, facts, constraints, citations, and uncertainty. Use for 炼化、打磨、润色、提炼、压缩、扩写、改写、总结、重组, or synthesis of drafts, notes, transcripts, proposals, reports, and research summaries; skip ordinary coding and natural-Chinese authorship requests handled by human-writing.
---

# Refine Text

Transform raw or existing text into the clearest useful form without silently changing its meaning.

Use `human-writing` after the meaning and structure passes only when the requested deliverable is natural Chinese prose. Use `write-action-first` only to shape the surrounding chat response, not to rewrite the source artifact unless the user asks.

## Core contract

1. Preserve the source's intent, facts, constraints, uncertainty, and important nuance.
2. Improve structure before polishing sentences.
3. Separate sourced facts from interpretation, recommendation, and newly inferred material.
4. Optimize for the reader's decision, understanding, or next action rather than for decorative prose.
5. Return a usable result, not merely editorial commentary.

Never invent evidence, citations, numbers, names, dates, commitments, or certainty. Preserve links and citations unless the user asks to change them. Surface contradictions instead of resolving them by guesswork.

## Workflow

### 1. Establish the transformation contract

Infer the following from the request and source:

- purpose: what the text must accomplish;
- audience: who will read it and what they already know;
- output form: message, memo, plan, article, report, specification, summary, or another form;
- fidelity: how much wording and structure may change;
- success condition: what a successful reader should understand, decide, feel, or do.

Ask a question only when a missing answer would materially change the result. Otherwise choose the least risky interpretation and proceed.

### 2. Diagnose before rewriting

Build a compact internal map of:

- central thesis or intended outcome;
- essential facts, constraints, decisions, and requests;
- supporting evidence and examples;
- assumptions, ambiguities, contradictions, and gaps;
- repetition, weak ordering, vague wording, and unnecessary detail.

Do not expose this diagnostic unless the user asks for critique, rationale, or tracked changes.

### 3. Select the refinement mode

Use one primary mode and combine secondary modes only when useful:

- **Polish** — improve correctness, flow, tone, and wording with minimal structural change.
- **Distill** — reduce length while retaining the decision-relevant or meaning-bearing content.
- **Restructure** — rebuild hierarchy, ordering, headings, and progression.
- **Challenge** — test logic, assumptions, evidence, risks, and alternatives, then strengthen the text.
- **Adapt** — tailor language, depth, tone, and format to a reader or channel.
- **Synthesize** — combine multiple sources without hiding disagreement or provenance.

For an unspecified request such as "refine this" or "polish this," default to balanced refinement: preserve the purpose, remove redundancy, clarify logic, strengthen structure, and avoid adding new claims.

Read [references/modes-and-patterns.md](references/modes-and-patterns.md) when the requested mode or document type materially affects the output structure.

### 4. Refine in passes

Apply these passes in order:

1. **Meaning pass** — identify what must survive unchanged.
2. **Logic pass** — repair ordering, missing transitions, unsupported jumps, and mixed levels of abstraction.
3. **Structure pass** — group related ideas and choose a reader-friendly hierarchy.
4. **Expression pass** — tighten sentences, replace vague wording, remove repetition, and align tone.
5. **Reader pass** — foreground the conclusion, request, decision, or next action.

For challenge mode, label new reasoning as analysis or recommendation. For synthesis mode, retain source distinctions where they matter.

### 5. Validate

Check the result against [references/quality-rubric.md](references/quality-rubric.md). At minimum verify:

- no material fact, qualifier, constraint, or requested action was lost;
- no unsupported claim was introduced;
- the organization matches the reader's likely questions;
- the conclusion and next action are easy to find;
- tone and terminology are consistent;
- unresolved ambiguity remains visible.

If the source is too incomplete to support a polished final, produce the strongest faithful version and list only the blocking gaps.

### 6. Deliver

Lead with the refined text.

- If the user asks for final copy only, return only final copy.
- If changes are substantial or reasoning is requested, follow with a short change summary.
- If unresolved issues affect correctness, add a concise "Open questions" section.
- If the user requests variants, make each variant meaningfully different in audience, tone, compression, or strategy.
- If editing a file, preserve the file format and avoid unrelated changes.

Do not upload, publish, message, or share the text unless the user explicitly asks. Treat sensitive source material as sensitive in every output form.

## Output principles

- Preserve the source language unless translation is requested.
- Prefer plain, precise wording over jargon and ornamental phrasing.
- Put conclusions before background when the text is decision-oriented.
- Use headings, lists, tables, or diagrams only when they materially improve comprehension.
- Keep technical terms that carry exact meaning; define them when the audience may not know them.
- Preserve productive nuance. Concision must not erase caveats, ownership, dependencies, or conditions.
- Use placeholders such as `[owner needed]` or `[evidence needed]` only when the gap must remain explicit; never fabricate the missing value.

## Bundled references

- [references/modes-and-patterns.md](references/modes-and-patterns.md) — mode-specific procedures and document patterns.
- [references/quality-rubric.md](references/quality-rubric.md) — final fidelity, clarity, logic, and usability checks.
