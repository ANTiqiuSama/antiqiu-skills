# Literature Search Design Reference

## Contents

1. Routing boundary
2. Input contract
3. Concept matrix
4. Search modes
5. Database adaptation
6. Search logging
7. Record normalization and deduplication
8. Screening and ranking
9. Citation chaining and iteration
10. Stopping and handoff
11. Access and integrity boundaries

## 1. Routing boundary

Use this workflow to discover a literature corpus for an answerable topic. Use claim investigation when the task is to support or contradict a small, explicit claim set. Use problem framing when the research question is not yet answerable. Discovery ends with a screened corpus and reproducible trail; it does not produce scientific conclusions.

## 2. Input contract

Record:

- primary research topic or review question;
- population, context, intervention or method, comparison, and outcomes when applicable;
- date range, languages, publication types, disciplines, and geography;
- known seed sources and controlled vocabularies;
- inclusion, exclusion, access, licensing, time, and screening-budget limits.

Do not silently infer a material boundary. Use a labeled reversible assumption only when it does not change the intended corpus.

## 3. Concept matrix

For each concept, record:

| Field | Purpose |
|---|---|
| `name` | Stable concept identifier |
| `terms.en` | English names, phrases, spellings, and acronyms |
| `terms.zh` | Chinese names, translations, and abbreviations |
| `controlled` | Subject headings or database vocabulary |
| `broader` | Recall-expanding parent terms |
| `narrower` | Precision-increasing child terms |
| `exclude` | Homonyms or unwanted senses |
| `sources` | Seed paper, thesaurus, expert input, or model suggestion |

Model suggestions are candidate terms. Confirm important vocabulary against seed papers, controlled vocabularies, or observed database records before treating the matrix as stable.

Example JSON accepted by `compile_queries.py`:

```json
{
  "groups": [
    {
      "name": "model",
      "terms": {
        "en": ["large language model", "LLM"],
        "zh": ["大语言模型", "大模型"]
      }
    },
    {
      "name": "risk",
      "terms": {
        "en": ["financial risk", "fraud detection"],
        "zh": ["金融风险", "反欺诈"]
      }
    }
  ],
  "exclude": {
    "en": ["course assignment"],
    "zh": ["课程作业"]
  }
}
```

## 4. Search modes

- **Recall-first**: include broader terms, acronyms, spelling variants, and multiple fields. Use for scoping, review discovery, or an unfamiliar vocabulary.
- **Precision-first**: require the most discriminating concept blocks, restrict fields, and apply defensible exclusions. Use for verification or a limited screening budget.
- **Balanced**: start with canonical terms and common aliases, inspect vocabulary and result volume, then revise once.

Do not use a universal numeric threshold. Compare result volume with the review purpose, database coverage, and available screening budget.

## 5. Database adaptation

Create a neutral Boolean expression first. Then adapt phrase quoting, field tags, proximity operators, wildcards, controlled vocabulary, and escaping to the current database interface.

The bundled compiler provides `generic`, `pubmed`, `wos`, and `scopus` renderers. Treat them as query drafts and verify current official database syntax before running a consequential search. For interfaces whose syntax changes by mode or locale, such as CNKI, compile a Chinese `generic` query and map its concept blocks using the interface's current advanced-search help.

Never paste one database's field tags into another database unchanged. Preserve both the neutral expression and each executed adaptation.

## 6. Search logging

For every run, record:

```json
{
  "database": "<INDEX>",
  "interface": "<WEB_OR_API>",
  "query": "<EXACT_EXECUTED_QUERY>",
  "concept_revision": "<HASH_OR_VERSION>",
  "fields": ["<FIELD>"],
  "filters": {"date": "<RANGE>", "language": ["<LANG>"]},
  "executed_at": "<ISO_TIMESTAMP>",
  "result_count": 0,
  "access_notes": "<LIMITS>"
}
```

Log zero-result and failed searches; they explain later widening decisions.

## 7. Record normalization and deduplication

Keep title, authors, year, DOI, database identifier, publication type, abstract, language, source database, query revision, URL, and retrieval date when available.

Deduplicate conservatively:

1. exact normalized DOI;
2. exact Unicode-normalized title plus year when DOI is absent or compatible;
3. otherwise retain separate records for manual review.

Keep preprints, conference papers, accepted manuscripts, and journal versions linked as versions unless identity is certain. Never discard source-database provenance.

## 8. Screening and ranking

Apply inclusion and exclusion criteria before reading conclusions. Record the screening stage and reason for each exclusion.

Rank candidates using question relevance, primary-versus-secondary status, methodological fitness, source authority, independence, recency, sample or evidence quality, and accessibility. Venue labels may inform screening but do not prove quality across disciplines.

## 9. Citation chaining and iteration

Use strong seeds for backward references, forward citations, related-record links, author searches, and terminology harvesting. Record which seed produced each addition.

Revise queries when observed vocabulary exposes missing synonyms, unwanted senses, or field mismatches. Preserve the prior query and state why the revision was made.

## 10. Stopping and handoff

Stop when:

- consecutive query or citation passes add no decision-relevant concepts or sources;
- the documented screening or time budget is exhausted;
- remaining databases are inaccessible or out of scope;
- a stable coverage gap is established.

Hand off the concept matrix, query bundle, search log, normalized records, deduplication clusters, screening register, citation-chain log, gaps, and stopping reason. A downstream claim investigation may then map evidence to explicit claims.

## 11. Access and integrity boundaries

- Do not store credentials, cookies, private tokens, or paid-content bodies in the skill or logs.
- Do not bypass login, risk control, licensing, robots rules, or paywalls.
- Do not treat a platform's corpus-size, ranking, or access claim as verified without authoritative documentation and a current test.
- Do not use model consensus as source validation.
- Preserve copyright-limited material as metadata and short evidence notes rather than copied full text.
