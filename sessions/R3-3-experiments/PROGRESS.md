# R3-3 experiments — PROGRESS

Lane: R3-3 new experiments & controls (profile res-s3)
Owner: FORGE lead

## Batch 0 — setup
- Created results/c1/r3/exp/ and reports/.
- Ollama available: qwen2.5:1.5b-instruct supports logprobs (verified /api/generate).

## Batch 1 — done (lead verified)
- MF-17: r3_exp_auroc_ci.py → results/c1/r3/exp/auroc_ci.json (20 AUROCs, 2 paired diffs, n_articles=18, seed 12345, 2000 resamples). Paired diff test 0.1085 CI [0.0950,0.1227]. (--check-repro passed per report)
- MF-13/MF-7: r3_exp_audit_twosided.py → audit_twosided.json. Two-sided |AUROC-0.5|<=0.25; R4 with_lex dev 0.405/0.407 inverted (passes); R1-R3 with_lex 0.976/0.890/0.924 (fail two-sided as expected). Top1-presented with_lex 0.716/0.738 (passes). Gold-indicator control 1.0.
- MF-12: r3_exp_ptruth.py → ptruth_scores.csv (553) + ptruth_summary.json. AUROC 0.232 (inverted direction 0.768); 0.80 threshold infeasible. COMPUTE.md documents Ollama logprob support. Model differs from paper (Qwen2.5-1.5B vs 0.5B); exploratory dev-only.
- Tests: 21 passed (pytest 04_experiments/src/tests/test_r3_exp_*.py).
- Reports: sessions/R3-3-experiments/reports/BATCH1.md

## Next
- Batch 2: MF-3/MF-6/MF-14 (both-runs table R5+transfer, H2 verdict, R4 robustness) + verify Batch 1.
## Batch 2 — done (lead verified 2026-11-08)
- MF-3: both_runs.json — R5 0.8925/0.9375, transfer 0.855@0.640 vs 0.975@0.706. all_match_stored true.
- MF-6: h2_verdict.json — frozen exp 7.25 UNDEFINED, corrected exp -2.0 REFUTED, confirmatory REFUTED/REFUTED. Over-refusal main/transfer reported.
- MF-14: r4_robustness.json — R4 0.8471 vs 0.1253 (gap 0.7218); bootstrap + 50% subsample robust across seeds 999/2024.
- Verify: verify_batch1.json overall PASS (50/50). COMPUTE.md cleaned. BATCH2.md written.
- Tests: 21 passed.

## Batch 3 — done (lead verified 2026-11-08)
- MF-10: sample (100, 25/rung, seed 20261103) + rubric + label_A (30/100, qwen2.5:1.5b) + label_B (6/100, qwen3:1.7b) + resolve (5/100, qwen2.5:1.5b strict). Kappa = 0.1975. adjudication.json + final_summary.md + ANSWERS.md (MF-10 updated to resolved 5%).
- Quality gates: pytest test_r3_exp_*.py 78/78 PASS; 5x --check-repro PASS; git status clean under results/.
- All 8 MFs (3,6,7,10,12,13,14,17) now have evidence files under 04_experiments/results/c1/r3/exp/.

CARD COMPLETE
