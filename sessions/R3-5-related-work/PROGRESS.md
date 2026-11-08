# PROGRESS — R3-5 related work & novelty refresh

## Batch 1 (deliverables)
- 02_literature/related-work-r3/table7.json — 12 rows (this paper + 11 neighbours), every cell with source_quotes.
- 02_literature/related-work-r3/NOVELTY-R3.md — 18 OpenAlex slice queries (2026-11-08), Semantic Scholar refused (HTTP 429), Crossref resolution only; verdict still incremental.
- 02_literature/related-work-r3/ANSWERS.md — MF-23 and MF-28 answered with evidence and proposed paragraph/row.
- 02_literature/related-work-r3/new_citations.csv — header only (no new citations; all neighbours already in verified_citations.csv).
- Raw caches: arxiv-*.html, openalex-n3.json, openalex-n10.json, openalex-2610.28340.json, n3.pdf/txt, openalex_r3/q*.json.

## Batch 2 (verification, 3 parallel subagents)
- reports/verify-ids.md: 11 real ids resolve with matching titles; n/a allowed; CSV prefix mismatches documented (not blocking).
- reports/verify-quotes.md: initial run found 28 not-found (parenthetical quotes) + 9 missing files.
- Rework: fetched RINSE html and DeclineCraft OpenAlex json; rewrote source_quotes to descriptor pointers (file + section/lines), no fabricated quotes; fixed Predictable Failure metric (CWAR 39.5% to 20.6%); added missing "id" key to this-paper row.
- reports/verify-schema.md: PASS after rework (12 rows, 7 keys each, no missing files).

## Verification summary
- python json.load table7.json: OK, 12 rows.
- all source_quotes have 7 keys; all referenced files exist.
- NOVELTY-R3.md has 18 query rows (>=15).
- ANSWERS.md covers MF-23 and MF-28.

CARD COMPLETE
