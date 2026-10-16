# Release gates

Select gates by declared scope and research type. Automated checks establish structure and provenance, not scientific truth or human approval. Useless hash checks are forbidden. Validate an existing integrity mechanism only when it is relevant to the audit; do not introduce new manuscript, backup or artifact hashes without an actionable integrity, security or protocol-version binding question. Missing an unnecessary digest is not a release defect.

1. Ledger, when in scope: contiguous events, valid hash chain, replayable snapshot and no undeclared mutation.
2. Scope: current charter, non-goals, budget/access boundaries and protocol revisions.
3. Literature: stable source IDs, coverage limits and required search/screening records.
4. Claims: material claims map to scoped evidence; empirical claims are verified; critical contradictions remain visible.
5. Experiments: required tasks are complete, including retained failures and negative results. Manifests identify code, data, environment, parameters, seeds, input/output versions and locators, and logs. Require a digest only where an actual integrity or version-binding consumer needs it.
6. Analysis: confirmatory analysis follows the locked protocol; deviations and exploration are labeled; numbers and figures trace to immutable artifacts.
7. Manuscript: sections, tables, figures and references agree and stay within the evidence.
8. Independent review: a reviewer who did not produce the evidence chain assessed a pinned snapshot, with findings and dispositions recorded.
9. Human release: applicable authorship, ethics, privacy, licenses, conflicts, AI disclosure, venue policy, data/code availability and release approval are explicit.

## Severity and verdict

- Critical: corruption, fabricated/missing core evidence, hash mismatch, leakage, undeclared protocol change, absent required human authority or claims beyond evidence.
- Major: incomplete reproducibility/review, missing independent support, unresolved contradiction or broken figure/citation provenance.
- Minor: documentation/metadata defects that do not change interpretation. Advisory: optional improvement outside scope.

Applicable critical issues or missing mandatory gates yield `fail`; bounded non-critical incompleteness may yield `partial`. `pass` establishes the declared criteria, not universal truth or guaranteed publication.
