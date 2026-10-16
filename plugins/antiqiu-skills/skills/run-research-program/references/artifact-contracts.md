# Research Artifact Contracts

Store project work outside the skill and reuse its current objective. Without an existing record, an authorized durable program may use `GOAL_PROMPT.md`; do not duplicate the goal in the ledger or charter. Code, configuration, raw results and generated figures are the working deliverables; add prose only for requested writing or information needed to use, reproduce or hand off the work.

## Layout

```text
.research-program/project.json, events/, .lock
research/charter/, literature/, evidence/, protocol/, implementation/
research/experiments/runs/<run-id>/
research/analysis/, manuscript/, review/, release/
```

Create only the paths needed by the current work, not the whole layout. Reuse machine-readable records and logs instead of writing parallel Markdown reports. Use repository-relative state paths, reject traversal and keep credentials, cookies, private headers and restricted raw data out of events.

## Trial and evidence records

For a small exploratory trial, retain its question, comparator, input/data identifiers and known exposure, code/configuration, parameters/seed, resource limit, outputs/logs, timing and outcome. This can be one compact record. Capture what makes it reproducible without creating unused record types or rehashing all historical inputs.

For consequential long or confirmatory runs, record task/attempt/run IDs; protocol revision and metric contract; code/environment identity and dirty state; input identifiers/versions; parameters, seeds and resources; output/checkpoint locators; executor/command and start/end times. Hashes are conditional: retain an existing valid digest only when the protocol or an actual consumer uses it for integrity, security or immutable-version binding; compute a new one only when that decision needs it. Routine artifact, text, backup or historical-corpus hashing is forbidden. Keep failed runs. Execution outcome and scientific finding are separate fields.

Search records preserve executed query, interface/date/filter, count, screening/exclusion reasons, stable source IDs and useful query/citation revisions. Claims record scope, kind, maturity, contradictions and manuscript location. Evidence records its source/artifact locator, producer, relevant provenance, validation and supersession; a URL alone supports `sourced`, not `verified`.

Analysis and figures link to actual run artifacts and generation inputs. Amend primary metrics or exclusions transparently; label exploratory deviations. Independent reviews identify the reviewer, input snapshot, findings and disposition. Release records applicable human authority, authorship, ethics, rights, venue/AI disclosure and availability requirements. Ordinary trial completion does not create a release record requirement.
