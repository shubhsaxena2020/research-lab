# VERIFY-B — Independent verification of MF-3 / MF-6 / MF-14 / MF-7

**Label: exploratory / post-hoc.** All numbers below are exploratory/post-hoc verification of exploratory JSONs; no new result is claimed. Verdicts here do not change any pre-registered/confirmatory claim.

## Sources read

- `04_experiments/results/c1/r3/exp/both_runs.json` vs stored `04_experiments/results/c1/rung5.json`, `04_experiments/results/c1/transfer.json` and `04_experiments/results/c1_corrected/rung5.json`, `04_experiments/results/c1_corrected/transfer.json`
- `04_experiments/results/c1/r3/exp/h2_verdict.json` vs stored `transfer.json` `drop_vs_test_rung3`
- `04_experiments/results/c1/r3/exp/r4_robustness.json` vs stored `results_full.json` rung-4 (recall definition)
- `04_experiments/results/c1/r3/exp/audit_twosided.json` (`gold_indicator_control`, `top1`)
- `04_experiments/results/c1/r3/exp/verify_batch1.json`

Scripts inspected: `r3_exp_both_runs.py`, `r3_exp_h2_verdict.py`, `r3_exp_r4_robust.py`, `r3_exp_verify_batch1.py`.

## Repro / test evidence (run 2026-11-08, IST)

- `python -m pytest 04_experiments/src/tests/test_r3_exp_both_runs.py 04_experiments/src/tests/test_r3_exp_h2_verdict.py 04_experiments/src/tests/test_r3_exp_r4_robust.py -q` → **21 passed**
- `python -m pytest` with `test_r3_exp_verify_batch1.py` added → **47 passed**
- `python 04_experiments/src/r3_exp_verify_batch1.py --check-repro` → **REPRO CHECK: PASS**
- `python 04_experiments/src/r3_exp_both_runs.py --check-repro` → **PASS**
- `python 04_experiments/src/r3_exp_h2_verdict.py --check-repro` → **PASS**
- `python 04_experiments/src/r3_exp_r4_robust.py --check-repro` → **PASS**
- `verify_batch1.json`: overall **PASS**, 50/50 leaf checks.

---

## MF-3 — both_runs.json (R5 + transfer under both runs)

**Overall: PASS (all numbers match stored truths; `all_match_stored` true both runs).**

| Claim | Verified value(s) | PASS/FAIL |
|---|---|---|
| R5 exploratory test, frozen | 0.8925 (n=400, n_refused=357); stored `c1/rung5.json` `rung5_test.exploratory_band.abstain_precision` = 0.8925 | **PASS** |
| R5 exploratory test, corrected | 0.9375 (n=400, n_refused=375); stored `c1_corrected/rung5.json` = 0.9375 | **PASS** |
| R5 AUROC answerable-vs-rung5, frozen | 0.9736; stored `auroc.answerable_test_rung0_vs_rung5` = 0.9736 | **PASS** |
| R5 AUROC, corrected | 0.9728; stored = 0.9728 | **PASS** |
| R5 confirmatory test, frozen / corrected | 1.0 vs 0.9975; stored confirmatory = 1.0 / 0.9975 (matches `both_runs.table`) | **PASS** |
| Transfer exploratory rung-3 precision, frozen | 0.855; stored `transfer.operating_points.exploratory_band.transfer_rung3_abstain_precision` = 0.855 | **PASS** |
| Transfer exploratory, corrected | 0.975; stored = 0.975 | **PASS** |
| Transfer AUROC answerable-vs-rung3, frozen | 0.6402; stored = 0.6402 | **PASS** |
| Transfer AUROC, corrected | 0.7059; stored = 0.7059 | **PASS** |
| Transfer confirmatory rung-3, frozen / corrected | 0.985 vs 1.0; stored confirmatory = 0.985 / 1.0 | **PASS** |
| `all_match_stored` frozen / corrected | true / true | **PASS** |
| Gate refit assertions (frozen + corrected) | `passed:true`, `max_absdiff:0.0`, n_dev_ids=1873 both | **PASS** |

All `comparison.*.diff` and `diff_auroc` / `diff_rung3_precision` are 0.0 (tolerance 1e-4). Thresholds are read from each run's `results_full.json`, never refit: frozen confirmatory t_lo 0.9072 / t_hi 0.9478, exploratory t_lo 0.2974 / t_hi 0.9478; corrected confirmatory 0.5232 / 0.5370, exploratory 0.3032 / 0.6362.

**Disposition: MF-3 numeric claims PASS.**

## MF-6 — h2_verdict.json (H2 operating-point transfer)

**Overall: PASS (drops and verdict strings exactly as claimed).**

Rule applied: SUPPORTED if drop ≥10pp; REFUTED if drop within ±5pp; (5,10) and ≤−5 UNDEFINED. Drop = test rung-3 precision − transfer rung-3 precision.

| Claim | Verified value(s) | PASS/FAIL |
|---|---|---|
| Frozen exploratory drop | 7.25pp (0.9275−0.855); stored `drop_pp`/`recomputed_drop_pp` = 7.25, `stored_drop_matches:true` | **PASS** |
| Frozen exploratory verdict | **UNDEFINED** (7.25 ∈ (5,10), neither ≥10 nor ±5) | **PASS** |
| Corrected exploratory drop | −2.0pp (0.955−0.975); stored/recomputed = −2.0, direction `gain` | **PASS** |
| Corrected exploratory verdict | **REFUTED** (within ±5) | **PASS** |
| Frozen confirmatory drop / verdict | 1.5pp (1.0−0.985) → **REFUTED** | **PASS** |
| Corrected confirmatory drop / verdict | 0.0pp (1.0−1.0) → **REFUTED** | **PASS** |
| Transfer AUROCs carried through | frozen 0.6402, corrected 0.7059 (both bands) | **PASS** |

Caveat (held in `h2_verdict.json` itself, not a FAIL): H2 requires *equal* abstain recall. `equal_recall_check.holds` is true only for corrected confirmatory (gap 0.0); frozen confirmatory (1.5pp), frozen exploratory (7.25pp) and corrected exploratory (2.0pp) do **not** hold. Verdicts are thus frozen-threshold precision-drop verdicts, not recall-matched. H2 gets no p-value (D1.4). Corrected confirmatory numbers are sensitivity-only and cannot overturn the frozen confirmatory verdict.

**Disposition: MF-6 numeric + verdict claims PASS (with equal-recall caveat noted).**

## MF-14 — r4_robustness.json (R4 registered vs corrected)

**Overall: PASS (gap 0.7218 robust across seeds 999/2024).**

Definitions: abstain precision = fraction refused on rung-4 negatives (recall definition, matching 84.71%/12.53%); `true_precision` = P(rung4|refused) reported alongside.

| Claim | Verified value(s) | PASS/FAIL |
|---|---|---|
| R4 exploratory, registered/frozen | 0.8471 (n_rung4=399, n_refused=338, over-refusal 0.095) | **PASS** |
| R4 exploratory, corrected | 0.1253 (n=399, n_refused=50, over-refusal 0.110) | **PASS** |
| R4 gap exploratory registered−corrected | 0.7218 (= 0.8471−0.1253); `stability.gap_full_sample` = 0.7218 | **PASS** |
| R4 AUROC answerable-vs-rung4 | 0.9681 vs 0.573 | **PASS** |
| R4 confirmatory | 1.0 vs 0.9073 | **PASS** |
| Stored match flags | `exploratory_matches_stored:true`, `confirmatory_matches_stored:true`, `auroc_matches_stored:true` (both runs) | **PASS** |

Robustness (exploratory band):

- **50% subsample without replacement, 20 reps:** registered mean 0.8473 (seed 999, sd 0.0186, [0.8197,0.8802] p025–p975) / 0.8502 (seed 2024, sd 0.0167, [0.8224,0.8802]); corrected mean 0.1312 (seed 999, sd 0.0135, [0.1021,0.1476]) / 0.1280 (seed 2024, sd 0.0126, [0.1100,0.1552]).
- **Paired gap by seed:** mean 0.716 (seed 999), 0.7223 (seed 2024); min 0.665–0.68, max 0.75 — never near 0.
- **Percentile bootstrap, 2000 reps, n=399:** registered CI [0.8145,0.8822] (999) / [0.8095,0.8847] (2024), point 0.8471 both; corrected CI [0.0952,0.1579] (999) / [0.0927,0.1554] (2024), point 0.1253 both. CIs do not overlap.
- **Gate assertions:** `passed:true`, `max_absdiff:0.0`, n_dev_ids=1873 both runs.

**Disposition: MF-14 numeric claims PASS; "robust across seeds 999/2024" PASS.**

## MF-7 — gold-indicator / top1 claims (audit_twosided.json)

**Overall: PASS.**

| Claim | Verified value(s) | PASS/FAIL |
|---|---|---|
| Gold-indicator control AUROC | 1.0 in all 8 cells (dev+test × rungs 1–4) — `gold_indicator_control.*.auroc_with_is_gold` = 1.0 | **PASS** |
| Gold-indicator `abs_diff_with_is_gold` | 0.5 all cells; `direction_with_is_gold:normal`, `passes_with_is_gold:false` (perfect separation correctly fails two-sided |AUROC−0.5|≤0.25) | **PASS** |
| Top1-presented with_lex dev / test | 0.7156 (0.716 @3dp) / 0.7381 (0.738 @3dp) | **PASS** |
| Top1 primary_6 dev / test | 0.5039 / 0.5705 (both `passes_primary_6:true`, `passes_with_lex:true`) | **PASS** |
| (Supporting, explains contrast) R1–R3 with_lex dev | 0.9762 / 0.8901 / 0.9235, all `passes_with_lex:false` | **PASS** |
| (Supporting) R4 primary_6,with_lex dev (frozen artifact) | 0.407 inverted passes two-sided / 0.4047 (0.405 @3dp) inverted passes | **PASS** |

**Disposition: MF-7 numeric claims PASS.**

---

## Summary

- MF-3 (both_runs): **PASS** — 0.8925 vs 0.9375; AUROCs 0.9736 vs 0.9728; transfer 0.855@0.6402 vs 0.975@0.7059; all match stored exactly.
- MF-6 (h2_verdict): **PASS** — frozen exploratory 7.25pp UNDEFINED, corrected exploratory −2.0pp REFUTED, confirmatory REFUTED/REFUTED.
- MF-14 (r4_robustness): **PASS** — 0.8471 vs 0.1253, gap 0.7218, robust across subsample seeds 999/2024 and bootstrap.
- MF-7 (gold/top1): **PASS** — gold-indicator 1.0 all 8 cells; top1 with_lex 0.7156/0.7381.
- No FAILs found. All artifacts labelled exploratory/post-hoc; corrected confirmatory cannot overturn frozen confirmatory; H2 equal-recall caveat stands.
