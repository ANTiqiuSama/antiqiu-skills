---
name: audit-research-release
description: Independently audit an existing research package or manuscript for evidence integrity, reproducibility, and release readiness; the audit is read-only.
---

# Audit Research Release

Independently assess structural and scientific readiness from immutable evidence. Keep the audit read-only: do not alter project state, manuscripts, artifacts, evidence, gates or review records.

## Procedure

1. Pin the revision and scope. Read applicable repository instructions and relevant charter, protocol, claims, runs, manuscript, reviews and release records. Reuse provenance and valid checks. Useless hash checks are forbidden: do not hash ordinary text, backups or all historical artifacts. A hash must answer an actionable integrity, security or protocol-version binding question in the smallest relevant scope; never substitute it for scientific or execution evidence.
2. Apply the relevant [release gates](references/release-gates.md). For supported `.research-program` state in scope, run this skill's `python scripts/audit_release.py --project <root> --json`; otherwise assess the available artifact evidence directly without requiring that record format or initializing a program.
3. Independently sample high-risk claims, citations, figures and run provenance; resolve disputed scientific claims against relevant primary sources.
4. Report `pass`, `partial` or `fail` with issue codes, evidence locators, impact and the smallest remediation. Distinguish checked facts, judgment and unresolved questions.

## Evidence and authority

Prose, structural script success and AI reviewer scores do not establish successful experiments or scientific truth. Preserve negative results, failed attempts, contradictions, missing evidence and integrity discrepancies. Human authorship, ethics, conflicts, rights, disclosure, submission and adoption decisions require their actual authorized source; a local pilot is execution evidence.

For audit-only work, return findings. If repairs are already authorized, finish and record the audit before continuing them; your own repair verification is not an independent release audit.

## Verdicts

- `pass`: applicable mandatory gates are evidenced with no critical unresolved issue; this is not human release approval.
- `partial`: evidence is inspectable but bounded non-critical checks remain incomplete.
- `fail`: required integrity, provenance, evidence, independent review or release gates are missing or contradicted.
