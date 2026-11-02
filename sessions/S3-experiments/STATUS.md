# STATUS S3-experiments
last_update: 2026-11-03T01:10+05:30
state: IN PROGRESS — Phase 1 (Phase 2 LOCKED: no 03_topics/SELECTED.md, no `TOPIC APPROVED` in orchestration/HEAD-REVIEW.md)

## Done and verified (run, not claimed)
- S3-1 `tools/verify_citations.py` — resolution via Crossref / arXiv / DataCite / OpenAlex /
  Semantic Scholar, fuzzy title+author+year comparison, verdicts VERIFIED / MISMATCH /
  NOT_FOUND / ERROR, disk cache, polite rate limits, Retry-After handling, source-exhaustion
  detection, CSV+BibTeX input, verified_citations.csv + JSON + MD reports.
  Evidence: `python -m pytest tools/tests -q` -> 37 passed.
  Evidence: live run `tools/tests/live_sample.csv` -> 5/5 real papers VERIFIED with API
  provenance, the deliberately fake row NOT_FOUND (best title match 0.50 < 0.55).

## Environment facts learned
- `pandas`, `matplotlib`, `scikit-learn`, `bibtexparser` are NOT installed -> NEEDS_DEPS.md.
  numpy, requests, yaml, jsonschema, pytest, psutil are available.
- OpenAlex and Semantic Scholar both answer 429 from this network with `Retry-After: 15859`
  (OpenAlex credit exhausted for the IP). Crossref, arXiv and DataCite work fine.
  Consequence: title search now tries Crossref bibliographic first; exhausted hosts are
  skipped for the rest of a run instead of sleeping through 30/60/120 s ladders.

## In progress
- S3-2 .. S3-8 delegated in parallel; each verified here before ticking (RULES #14).
