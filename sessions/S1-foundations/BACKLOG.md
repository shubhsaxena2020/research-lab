# BACKLOG S1-foundations
Ticked only after verifying the file exists and its numbers/links check out.
Session: 2026-11-03 (00:45–04:45 IST). Verification evidence in `logs/` and `00_foundations/verify_foundations.json`.

## Part A — 00_foundations
- [x] A1 `WHAT-IS-A-PAPER.md` — 4038 words, 20 sources, 0 dangling citations (verify_foundations.py)
- [x] A2 `HOW-TO-WRITE-ONE.md` — 4571 words, 27 sources
- [x] A3 `VENUES-AND-PUBLISHING.md` — 7140 words, 57 sources; one dead arXiv URL found by verification and fixed
- [x] A4 `ETHICS-AND-AI-USE.md` — 5680 words, 24 sources, 18 verbatim policy quotes
- [x] A5 `WHAT-A-PAPER-DOES-FOR-YOU.md` — 5978 words, 25 sources, age/year eligibility rules verified per programme
- [x] A6 `GLOSSARY.md` (125 terms) + `READING-LIST.md` (15 entries, 15/15 URLs 200 at write time)

## Part B — 01_psit_data
- [x] B1 dataset built (`papers.csv`, 793 records) + `README.md` (institution identity + data dictionary).
      OpenAlex full harvest NOT done: HTTP 429 shared-budget exhaustion, evidence + ready script saved.
- [x] B2 `COVERAGE-COMPARISON.md` — Crossref / Europe PMC / PubMed compared with real counts;
      Semantic Scholar + DBLP blocked (429), documented with evidence files.
- [x] B2b filter + coverage audit (`scripts/audit_crossref.py` -> `raw/crossref_audit.json`, §6 of the file):
      690 Crossref-attributed / 103 Europe PMC-only / 0 Crossref records without a PSIT string;
      583 distinct matched strings, 0 false positives; recall probe on 3 top authors, 0 missed PSIT papers.
- [x] B3 `INSTITUTE-PUBLISHED-FIGURES.md` — NIRF DCS, NAAC SSR, AICTE disclosure; 18 PDFs saved in `raw/institute_docs/`.
      Spot-verified independently: SSR p.89/95 DVV table 148/136/87/72/147 -> 37/21/18/17/24 reproduced from the PDF.
- [x] B4 `analysis/ANALYSIS.md` + `analysis/numbers.json` + `analysis/tables/*.md|.csv` (10 tables, reproducible via `scripts/analyze.py`).
      Analysis bug found by a subagent and fixed (see README §4 note); no headline number changed.
- [x] B5 `STATUS-OF-RESEARCH.md` + `drafts/EMAIL-TO-PSIT-RnD-CELL.md` (no R&D address is public; Dean-Research named, placeholder used)
- [x] B6 `subfolder_ai_research/AI-RESEARCH-AT-PSIT.md` + 4 CSVs; "0 of 168 AI records at a recognised AI venue" independently re-verified

## Finish
- [x] `06_review/STUDENT-DIGEST-S1.md` (673 words, one page)
- [x] STATUS.md final state
- [x] `git commit` (local only)

## Open, for the next session
- [ ] Re-run `python 01_psit_data/scripts/harvest_openalex.py` after 00:00 UTC (or with a free OpenAlex key) to replace the Crossref-only baseline with a full institution harvest.
- [ ] Semantic Scholar enrichment (`enrich_s2_dblp.py`) once an S2 key exists, to fill `open_access`.
- [ ] DBLP venue-type check (`enrich_s2_dblp.py --dblp-cap 200`) — was 429 today.
- [ ] 100-record **human** read of `papers.csv` (the programmatic audit is done; a person has not eyeballed 100 rows).
- [ ] Entity attribution PSIT (engineering) vs PSIT-CHE vs PSIT-Pharmacy per record — needs the institute's list or a manual read.
- [ ] Fill `records_with_*` / `open_access` gaps if new sources land; keep `numbers.json` keys stable.
