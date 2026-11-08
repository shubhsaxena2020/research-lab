# Batch 2 — reports

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

## VERIFY-BATCH1 (this file's new section, Batch 2)
- Created 04_experiments/src/r3_exp_verify_batch1.py
- Created 04_experiments/src/tests/test_r3_exp_verify_batch1.py (26 tests, pass)
- Output: 04_experiments/results/c1/r3/exp/verify_batch1.json — overall **PASS**, 50/50 leaf checks.
- Command: `python 04_experiments/src/r3_exp_verify_batch1.py`; ` --check-repro` → REPRO CHECK: PASS.
- Method: the verifier only *reads* the six batch-2 JSONs (auroc_ci.json,
  audit_twosided.json, ptruth_summary.json, both_runs.json, h2_verdict.json,
  r4_robustness.json) and cross-checks each headline number against the stored
  source of truth (c1/results_full.json, c1/rung5.json, c1/transfer.json and
  the c1_corrected equivalents). It re-derives nothing and fits no gate.
- Checked (grouped PASS/FAIL, tolerances TOL_4DP=5e-05 for 4-dp values,
  TOL_3DP=5e-04 for 3-dp quotes, exact for ids/flags/strings):

| Group | PASS | Key verified numbers |
|---|---|---|
| auroc_ci | 8/8 | frozen test 0.9824, corrected test 0.8738 (both vs discrimination.test_auroc), paired diff 0.1085, item-CI [0.0950, 0.1227], excludes zero, point == 0.9824-0.8738 |
| audit_twosided | 10/10 | R4 primary_6 dev 0.407 (inverted, passes), R4 with_lex dev 0.4047 (0.405 @3dp), top1 with_lex dev 0.7156 (0.716) / test 0.7381 (0.738), gold-indicator 1.0 (all 8 dev+test × rung cells) |
| audit_twosided_supporting | 6/6 | R1–R3 with_lex dev 0.9762 / 0.8901 / 0.9235, all fail two-sided as expected |
| ptruth | 4/4 | AUROC 0.2317, n_scored 553, threshold infeasible, model-differs disclosure |
| both_runs | 10/10 | frozen R5 exp 0.8925 / corrected 0.9375; transfer exp 0.855 / 0.975; AUROCs 0.6402 / 0.7059; all_match_stored true both runs; stored-field == table |
| h2_verdict | 6/6 | frozen exploratory 7.25pp UNDEFINED, corrected exploratory −2.0pp REFUTED; both confirmatory REFUTED |
| r4_robustness | 6/6 | registered 0.8471 / corrected 0.1253; matches_stored true; table == recomputed exploratory_band |

- COMPUTE.md cleaned: removed the stray trailing `EOF` / `echo done` lines
  (shell-heredoc artefact) so the file ends at
  `- **Verified on:** 2026-11-08.`
- Labelled exploratory/post-hoc verification (no new numbers); all six
  verified JSONs are exploratory/post-hoc already.

## Batch 2 — MF-3 / MF-6 / MF-14 (lead-verified, for the record)
- MF-3 (both_runs.json): R5 + transfer re-derived under both runs.
  Frozen R5 exploratory 0.8925 (AUROC 0.9736), corrected 0.9375 (0.9728);
  transfer exploratory 0.855 @0.6402 (frozen) vs 0.975 @0.7059 (corrected);
  confirmatory transfer 0.985 vs 1.0. `all_match_stored` true both runs.
- MF-6 (h2_verdict.json): frozen exploratory drop 7.25pp → **UNDEFINED**
  (falls in the (5,10) gap the preregistered binary rule leaves open);
  corrected exploratory −2.0pp → **REFUTED** (gain). Frozen confirmatory
  1.5pp → REFUTED; corrected confirmatory 0.0pp → REFUTED.
- MF-14 (r4_robustness.json): R4 exploratory abstain precision
  0.8471 (registered / frozen) vs 0.1253 (corrected); AUROC 0.9681 vs 0.5730;
  gap 0.7218, robust across 50% subsamples (20 reps, seeds 999/2024) and
  percentile bootstrap CIs. Confirmatory: 1.0 vs 0.9073.
