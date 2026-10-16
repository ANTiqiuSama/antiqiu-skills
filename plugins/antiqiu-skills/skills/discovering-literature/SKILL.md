---
name: discovering-literature
description: Build a reproducible corpus for systematic or scoping literature review, including bilingual search and screening; skip small claim checks.
---

# Discovering Literature

Build a traceable corpus for systematic or scoping review. Small explicit claim checks should go directly to relevant primary sources. Model-generated terms are search hypotheses, not evidence.

Infer scope, languages, period and budget from the request; ask only about material missing choices. Build a concept matrix from canonical terms, aliases, Chinese/English variants, controlled vocabulary and defensible exclusions.

Select indexes by coverage and adapt a neutral Boolean query to each database's current syntax. Use [search-design.md](references/search-design.md) for record schemas, `scripts/compile_queries.py` for JSON matrices and `scripts/deduplicate_records.py` for conservative JSONL clustering. Resolve script paths from this skill.

Log exact queries, fields, filters, dates, counts and access limits, including failed or zero-result searches. Normalize records and deduplicate by compatible DOI, then exact normalized title/year. Preserve provenance, conflicting IDs and publication-version relationships.

Apply declared inclusion rules; rank by question relevance, methodological fitness, authority, independence, recency and access rather than a universal venue hierarchy. Follow backward/forward citations from useful seeds and retain query revisions with their reasons.

Stop at documented saturation, budget or access limits. Deliver the screened corpus and reproducible search/screening trail, exclusions, gaps and stopping reason. Then perform any separately requested synthesis; a search-only request does not require additional research stages. Avoid credential exposure, access-control/paywall circumvention and unlicensed full-text copying.
