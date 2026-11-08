# Batch 1 — reports

## TASK1-1 auroc-ci
- Created 04_experiments/src/r3_exp_auroc_ci.py
- Created 04_experiments/src/tests/test_r3_exp_auroc_ci.py (7 tests, pass)
- Output: 04_experiments/results/c1/r3/exp/auroc_ci.json (20 AUROCs + 2 paired diffs)
- Key: frozen test 0.9824 CI [0.9774,0.9869], corrected 0.8738 CI [0.8585,0.8887], paired diff 0.1085 CI [0.0950,0.1227] excludes zero.
- n_articles held-out = 18 confirmed.
- Labelled exploratory/post-hoc, seed 12345, 2000 resamples.

## TASK1-2 audit-twosided
- Created 04_experiments/src/r3_exp_audit_twosided.py
- Created 04_experiments/src/tests/test_r3_exp_audit_twosided.py (5 tests, pass)
- Output: 04_experiments/results/c1/r3/exp/audit_twosided.json
- Two-sided rule |AUROC-0.5|<=0.25. R4 primary_6 dev 0.407 (inverted, passes), with_lex 0.4047 (inverted, passes). R1-R3 with_lex AUROCs 0.976/0.890/0.924 (do not pass with_lex, as expected sensitivity). Top1-presented: primary 0.504/0.571, with_lex 0.716/0.738 (both pass two-sided). Gold-indicator control AUROC 1.0.
- n_boot 2000, seed 12345.

## TASK1-3 ptruth
- Created 04_experiments/src/r3_exp_ptruth.py (Ollama qwen2.5:1.5b-instruct, /api/generate logprobs)
- Created 04_experiments/src/tests/test_r3_exp_ptruth.py (9 tests, pass)
- Output: 04_experiments/results/c1/r3/exp/ptruth_scores.csv (553 rows) + ptruth_summary.json
- AUROC(answerable vs negative) = 0.2317 (inverted; i.e. 1-0.2317=0.7683 in reverse direction). Threshold 0.80 infeasible (feasible false).
- COMPUTE.md written documenting Ollama logprob support (top_logprobs max 20).
- Disclosure: model differs from paper's Qwen2.5-0.5B; exploratory dev-only.
