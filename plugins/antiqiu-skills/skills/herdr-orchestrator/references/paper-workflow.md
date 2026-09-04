# Paper debate, writing, figures, and experiments

Use this workflow when the user wants several model families to improve a paper.
“Top-journal quality” is a direction for gap analysis, not a guaranteed outcome.

## Recommended roles

| Role | Default responsibility | Must not do |
| --- | --- | --- |
| Codex coordinator | Scope, task contract, evidence ledger, acceptance, status | Edit the manuscript it will accept |
| Codex reviewer | Methods, reproducibility, claim-to-evidence checks | Rewrite the paper during review |
| Claude reviewer | Adversarial peer review, theory, positioning, missing controls | Invent citations or results |
| Gemini/Antigravity writer | Apply accepted edits, produce figure artifacts, run bounded jobs | Decide contested claims alone |

The four-agent form keeps the coordinator independent. A three-agent form may
let the Codex coordinator also provide one review. Mark that review as
non-independent and use executable evidence for acceptance.

Only one role writes the manuscript in a round. Reviewers write separate review
files. This prevents “debate” from becoming concurrent edits to the same paper.

## Prepare one shared brief

Create one brief from the current manuscript, target venue, available code and
data, known results, permitted compute, and user constraints. Give every reviewer
the same brief and exact manuscript revision.

Keep artifacts under a user-approved root, for example:

```text
artifacts/herdr-paper/polish/
├── brief.md
├── round-01-codex.md
├── round-01-claude.md
├── round-02-codex-response.md
├── round-02-claude-response.md
├── decisions.md
├── experiment-gaps.md
├── figure-specs.md
└── acceptance.md
```

Do not hash every file during exploration. A Git revision or an explicit note
that the working tree is the source is enough. Add stronger freezing only when
the work becomes a release candidate or the evidence would otherwise drift.

## Run the rounds

1. Ask Codex and Claude for independent reviews. Neither sees the other's first
   review.
2. Extract only disputed claims, missing evidence, and incompatible proposals.
   Send that list to both reviewers for one response round.
3. Record each issue as accept, reject, user decision, or evidence needed. Keep
   the reason and source role. Do not manufacture consensus.
4. Send only accepted changes to the Gemini/Antigravity writer. Give one writable
   manuscript path and explicit figure output paths.
5. Rebuild the paper. Check citations, tables, figure references, claim strength,
   and the actual diff.
6. If essential evidence is missing, make an experiment plan. Run it only when
   data, compute, authorization, and a stopping rule are available.
7. Send the revised manuscript and new evidence to independent review. Stop
   after the defined acceptance gate or return unresolved issues to the user.

## Reviewer prompt

```markdown
**Outcome** Produce an independent, evidence-grounded review of the current paper.
**Read first** `<brief>` and `<manuscript>`.
**Allowed reads** the paper, cited sources, code, logs, and existing results.
**Allowed writes** only `<review-file>`.
**Constraints**
- Separate verified facts, inference, and recommendations.
- Quote no result that is absent from the supplied evidence.
- Flag unsupported citations; do not invent replacements.
- Rank issues by whether they block the central claim.
- Do not edit the manuscript and do not delegate.
**Acceptance** Every major issue names the affected claim, evidence, and smallest useful remedy.
**Return** Write the review to `<review-file>` and reply with its path and done/blocked.
```

## Debate response prompt

```markdown
Read `<your-review>` and `<disagreement-list>`. For each disagreement, state:
1. your revised position;
2. evidence that would change it;
3. the smallest manuscript or experiment change that resolves it.
Do not add unrelated review items. Write to `<response-file>`.
```

## Writer prompt

```markdown
**Outcome** Produce a new paper version that implements only accepted decisions.
**Read first** `<brief>`, `<decisions>`, and the current manuscript.
**Allowed reads** the paper project and accepted evidence.
**Allowed writes** only `<manuscript-path>`, `<figure-paths>`, and required build files.
**Constraints**
- Preserve unsupported claims as qualified or remove them.
- Do not invent citations, numbers, experiments, or statistical significance.
- Keep every figure linked to source data or label it as a schematic.
- Do not overwrite prior review artifacts and do not delegate.
**Acceptance** `<paper-build-command>` passes and all accepted decision IDs appear in the change log.
**Return** Write a change log to `<writer-report>`; reply with paths and done/blocked.
```

## Experiment evidence gate

Classify proposed experiments:

- Essential: without it, a central claim is unsupported.
- Discriminating: it resolves a live disagreement between explanations.
- Optional: it improves completeness but does not change the main conclusion.
- Unsupported: data, compute, authorization, or an observable metric is missing.

An experiment task must state the hypothesis, existing baseline, changed factor,
metric, resource limit, stop condition, and output path. Never treat a planned,
failed, partial, or synthetic experiment as completed evidence.

## Figure evidence gate

For each figure, preserve:

- purpose and claim;
- source data or explicit `schematic` label;
- script, notebook, or generation prompt;
- units, uncertainty, and sample counts when applicable;
- final vector or raster path and caption source.

Visual polish cannot repair unsupported evidence. If reviewers request new data,
keep the figure as a specification until the experiment produces that data.
