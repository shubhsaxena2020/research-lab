# BACKLOG S2-literature
Ticked only after the lead verified the file (row counts, title presence in verified CSV, spot-check).

- [x] S2-1 02_literature/LANDSCAPE.md — map of active AI areas 2025-2026; 5-8 verified landmarks each
- [x] S2-2 02_literature/deep_dives/D2-1_agent_memory_retrieval.md — 25+ verified papers
- [x] S2-3 02_literature/deep_dives/D2-2_abstention_calibration_hallucination.md
- [x] S2-4 02_literature/deep_dives/D2-3_efficient_on_device_inference.md
- [x] S2-5 02_literature/deep_dives/D2-4_evaluation_methodology_agents.md
- [x] S2-6 02_literature/deep_dives/D2-5_indic_low_resource_nlp.md
- [x] S2-7 02_literature/deep_dives/D2-6_scam_misinformation_detection.md
- [x] merge 02_literature/staging/*-verified.csv -> 02_literature/verified_citations.csv (317 rows)
- [x] S2-8 02_literature/GAP-MINING.md — 16 gaps (>=15 required)
- [x] S2-9 03_topics/CANDIDATES.md — 5 topics + rubric scores
- [ ] NOVELTY-CHECK.md — 48 of 60 required queries, arXiv only; OpenAlex/S2 unavailable (429).
      Written and honest, but does NOT meet the >=30-per-topic x 4-source bar. Now a HEAD CONDITION:
      re-run before any draft claims a gap. See STATUS gap 1.
- [x] head redo items from DIRECTIVES round 3: reader features split out of the "retrieval-feature" gate
      (CANDIDATES, GAP-MINING, PROPOSAL); register count reconciled (317, snapshot time stated); measured
      vs estimated timings separated; "nobody did this" claims narrowed to the 91-query arXiv sweep.
- [x] head condition 4 applied: private-corpus numbers removed from LANDSCAPE + 4 deep dives + all
      decision documents (verified by grep).
- [x] 03_topics/SELECTED.md — rank 1 + runner-up
- [x] 03_topics/PROPOSAL.md — 2 pages
- [x] 06_review/STUDENT-DIGEST-S2.md — 1 page
- [x] finish: spot-check 20 random citations (20 OK / 0 failed), STATUS updated

Tooling (lead-owned, frozen): 02_literature/tools/verify_citations.py, 02_literature/tools/check_docs.py
