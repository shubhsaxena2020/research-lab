# STATUS S2-literature
last_update: 2026-11-03 01:05 IST
state: IN PROGRESS — batch 1 (landscape + 6 deep dives) dispatched

## Done
- Read PROMPT.md, README.md, RULES.md, DIRECTIVES.md (no directives yet), HEAD-REVIEW.md (phase 2
  LOCKED until head writes `TOPIC APPROVED`), ai-memory-core PRIOR-ART.md + FINAL-HANDOFF.md (read-only).
- Built `02_literature/tools/verify_citations.py` (lead-owned, frozen): modes search / enrich / add /
  spotcheck against arXiv API, OpenAlex, Crossref. API-truth metadata, 0.90 title-similarity gate,
  mismatches rejected not repaired. Smoke-tested: 5 claims -> 3 VERIFIED, 2 MISMATCH (both intentional).
- Wrote `sessions/S2-literature/BRIEF.md` — binding subagent brief (hardware, citation discipline, output shape).

## In flight
- Batch 1: S2-1 landscape + S2-2..S2-7 six deep dives (7 subagents, parallel).

## Done since
- S2-8 gap mining: `02_literature/GAP-MINING.md` — 16 de-duplicated gaps, each with research
  question, nearest prior work, cheapest honest test (dataset/size/baseline/metric/wall-clock),
  failure modes and cost; ranked table; combination plan; exclusions. ~6.2k words including a
  40-item bibliography and the ranking table.
- 4 new citations verified into `staging/S2-8-verified.csv` (SKR, FLARE, StreamingQA, Marchisio
  et al. quantisation-multilingual). Ran `check_docs.py merge`: canonical register now 270 rows.
- CORRECTION for later files: LANDSCAPE §5 lists "quantisation damage in Indic scripts" as
  unmeasured; Marchisio et al. (2024) measured it (non-Latin scripts worst affected). That gap is
  closed — do not re-propose it.

## Next
- Verify each returned file (row counts vs claims, titles in .md ⊆ verified CSV).
- Merge staging CSVs -> 02_literature/verified_citations.csv (global dedupe).
- Batch 2: S2-9 candidates (GAP-MINING §3 names the candidate paper bundles).
- Batch 3: two novelty checks (>=30 queries each) for top-2.
- Then 03_topics/SELECTED.md + PROPOSAL.md, 06_review/STUDENT-DIGEST-S2.md, spot-check 20 citations.

## Notes / blockers
- Semantic Scholar API returns 429 without a key -> not used; arXiv+OpenAlex+Crossref are the
  verification sources (3 independent ones is enough).
- Experiments NOT started and must not start: HEAD-REVIEW.md gates phase 2.

## Done since (S2-10)
- Novelty pre-scan across all four candidate families: `02_literature/NOVELTY-PRESCAN.md`
  (91 documented queries, 72 papers verified into `staging/S2-10-verified.csv`). Verdicts:
  B (memory staleness) ALREADY DONE; A (retrieval-feature abstention gate) and D (scam at realistic
  prevalence) CROWDED with one narrow slice each; C (Indic abstention) CROWDED and predictable.
- BLOCKER carried forward: OpenAlex returned HTTP 429 (daily budget exhausted on this IP) for the
  whole window, so all queries ran arXiv-only. Re-run the 91 queries against OpenAlex after 00:00 UTC
  or with an activated key before writing `NOVELTY-CHECK.md`.
