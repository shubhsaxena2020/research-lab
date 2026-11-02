# STATUS S1-foundations
last_update: 2026-11-03 04:50 IST
state: **DONE** (Part A complete; Part B complete on the data that was reachable; 3 APIs blocked and documented)

## DONE
Part A (00_foundations), verified by `00_foundations/verify_foundations.py` -> `logs/verify_foundations.json`:
| file | words | sources | dangling citations |
|---|---|---|---|
| WHAT-IS-A-PAPER.md | 4038 | 20 | 0 |
| HOW-TO-WRITE-ONE.md | 4571 | 27 | 0 |
| VENUES-AND-PUBLISHING.md | 7140 | 57 | 0 (one dead arXiv URL found by the verifier and fixed) |
| ETHICS-AND-AI-USE.md | 5680 | 24 | 0 (18 verbatim policy quotes) |
| WHAT-A-PAPER-DOES-FOR-YOU.md | 5978 | 25 | 0 |
| GLOSSARY.md | — | 25 | 125 terms |
| READING-LIST.md | 2446 | 15 | 0 |

Part B (01_psit_data):
- `papers.csv` — 793 deduplicated records (Crossref 690 + Europe PMC 102 + PubMed 1 unique; 460 merges),
  years 2007–2026, 394 venues, 168 AI-related (21.2%), 5476 Crossref citations, median 1.
- `README.md` (dataset + institutional identity), `COVERAGE-COMPARISON.md`, `INSTITUTE-PUBLISHED-FIGURES.md`,
  `analysis/ANALYSIS.md` + `analysis/numbers.json` + 10 tables, `STATUS-OF-RESEARCH.md`,
  `drafts/EMAIL-TO-PSIT-RnD-CELL.md`, `subfolder_ai_research/AI-RESEARCH-AT-PSIT.md` + 4 CSVs.
- Scripts (all re-runnable): `scripts/harvest_crossref.py`, `harvest_epmc_pubmed.py`, `build_dataset.py`,
  `enrich_s2_dblp.py`, `analyze.py`, `ai_subset_tables.py`, `harvest_openalex.py`.
- `06_review/STUDENT-DIGEST-S1.md` written.

## Verification actually performed (not assumed)
- Re-ran `analyze.py` twice: headline numbers stable across runs.
- 10/10 randomly sampled DOIs resolve at `api.crossref.org/works/{doi}` (seed 7).
- Independently reproduced the SSR DVV table from the saved PDF: p.89/95 before 148/136/87/72/147 -> after 37/21/18/17/24.
- Independently re-counted "AI records at a recognised AI venue": 0 of 168, by venue-name regex.
- Found and fixed an `analyze.py` bug (`records_with_affil_string` never incremented); replaced with two
  explicitly named keys (792 non-empty affiliation text / 784 naming PSIT) and patched both documents that mentioned it.
- Fixed one dead URL (arXiv submission page) found by the verifier.

## NOT DONE / blocked (evidence file named for each)
- OpenAlex full harvest — HTTP 429, "Insufficient budget ... $0 remaining; resets at midnight UTC"
  (`raw/openalex_institution_I4405287327.json` is the only record obtained). Script ready.
- Semantic Scholar — 429 on single and batch endpoints (`raw/s2_unavailable.json`).
- DBLP — 429 / connection reset (`raw/dblp_unavailable.json`).
- Therefore: `open_access` and `in_dblp` columns are empty; institution works_count (1412) could not be
  reconciled with our 793; the 721 affiliation-string probe reading remains a single unharvested reading.
- No manual 100-record audit of affiliation correctness (listed in BACKLOG as open).

## Open problems for the next session
1. OpenAlex after 00:00 UTC: `python 01_psit_data/scripts/harvest_openalex.py`. This is the single highest-value next step
   (concepts/topics, full citation counts, institution disambiguation).
2. Entity attribution: PSIT engineering vs PSIT-CHE vs PSIT-Pharmacy is unresolved by public data; needs either the
   institution's own list (email draft ready) or per-paper affiliation inspection.
3. `papers.csv` `topics` is a keyword heuristic; a real subject classification needs OpenAlex topics.
4. Eligibility facts about Shubh (BCA maths/statistics on transcript, NIMCET/CSJM rules) need his own documents.

## Second pass (orchestrator DIRECTIVES round 2 + head CHECKPOINT 1), 2026-11-03 05:10 IST
- [x] `06_review/claims_evidence.md` — 20 consequential claims, each with the verbatim supporting sentence from the live page,
      fetch method and verdict: 17 SUPPORTED, 3 PARTLY (arXiv "typically not accepted" softened; SRFP affiliation clause deleted -
      not on the page; DAAD WISE "5th/6th semester" demoted to UNCERTAIN), 0 unverified/unsupported.
- [x] 10-line "READ THIS FIRST" block added to all 7 foundation docs; `00_foundations/verify_read_first.py` passes (10 lines each, delta < 250 words).
- [x] `ANALYSIS.md` corrected: "teaching-heavy institution", "cheapest publication type" and every manual `[papers.csv check]`
      figure removed or scripted; interpretation now visually separated; new `scripts/analyze_extra.py` -> `analysis/numbers_extra.json`.
- [x] `AI-RESEARCH-AT-PSIT.md`: "0 of 168 at a named AI venue" scoped (denominator, 21-name regex, limits, one-line reproducer);
      "evaluation discipline is thin" replaced by a counted abstract audit (`scripts/ai_abstract_audit.py`, `raw/ai_abstract_audit.json`:
      3/108 baseline, 0/108 seeds).
- [x] `06_review/STUDENT-DIGEST-S1.md` written (<= 1 page).
