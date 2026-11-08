# VERIFY-A — Independent verification of MF-17 / MF-13 / MF-7 / MF-12 claims vs result JSONs and stored truths

**Scope:** Batch-1 numbers only (auroc_ci, audit_twosided, ptruth). This report is
**exploratory/post-hoc verification, not new results** — no model re-trained, no
number copied from `ANSWERS.md`/`BATCH1.md` without tracing to a JSON key + command.

**Date run:** 2026-11-08 (repro checks executed live for this report).
**Workspace:** `C:\Users\shubh\research-lab`

## How verification was done (three independent layers)

1. **Direct JSON extraction** — every headline number below was read from
   `04_experiments/results/c1/r3/exp/*.json` (file + key + raw value shown).
2. **Test execution (recompute, not just re-read):**
   `python -m pytest 04_experiments/src/tests/test_r3_exp_auroc_ci.py 04_experiments/src/tests/test_r3_exp_audit_twosided.py 04_experiments/src/tests/test_r3_exp_ptruth.py -q` → **21 passed in 117.10s**
3. **Repro check:**
   `python 04_experiments/src/r3_exp_verify_batch1.py --check-repro` → **REPRO CHECK: PASS**
   (stored `verify_batch1.json`: `overall=PASS`, `n_pass=50`, `n_fail=0`, `n_checks=50`).
4. **Stored-truth cross-check** — frozen/corrected `results_full.json` `discrimination.test_auroc`,
   plus independent Python recompute of the P(True) AUROC from `ptruth_scores.csv` (553 rows).

Shared parameters in all three JSONs: `seed=12345`, `n_boot=2000`, `exploratory/post-hoc=true`.

---

## MF-17 — AUROC intervals + paired difference

**Generator:** `04_experiments/src/r3_exp_auroc_ci.py` → `04_experiments/results/c1/r3/exp/auroc_ci.json`
**Command:** `python 04_experiments/src/r3_exp_auroc_ci.py` (`--check-repro` → PASS; 7 tests pass)

| Claimed | File + key | Raw value | Stored truth (`results_full.json`) | Verdict |
|---|---|---|---|---|
| frozen test AUROC 0.9824 | `auroc_ci.json` → `aurocs.frozen_test_overall.point` | `0.9823630831643002` | `c1/results_full.json` → `discrimination.test_auroc` = `0.9824` | **PASS** (diff 3.7e-05 < 5e-05) |
| frozen test 95% CI [0.9774, 0.9869] | `auroc_ci.json` → `aurocs.frozen_test_overall.ci_item` | `lo=0.977383867119937, hi=0.9868557360272447, method=percentile, n=1879 (400+,1479−), n_valid=2000, seed=12345` | — (new interval, bootstrap) | **PASS** (rounds to [0.9774,0.9869]) |
| corrected test AUROC 0.8738 | `auroc_ci.json` → `aurocs.corrected_test_overall.point` | `0.8738488843813388` | `c1_corrected/results_full.json` → `discrimination.test_auroc` = `0.8738` | **PASS** (diff 4.9e-05 < 5e-05) |
| corrected test 95% CI [0.8585, 0.8887] | `auroc_ci.json` → `aurocs.corrected_test_overall.ci_item` | `lo=0.8585208861863459, hi=0.8886909901076596, n=1879, n_valid=2000` | — | **PASS** (rounds to [0.8585,0.8887]) |
| paired diff 0.1085 CI [0.0950,0.1227] excludes zero | `auroc_ci.json` → `paired_diffs.frozen_vs_corrected_test_overall` | `point=0.10851419878296142, ci_item {lo=0.09504793035338292, hi=0.12272669771962555, contains_zero=false}` | arithmetic: 0.98236308 − 0.87384888 = 0.10851420 ✓ | **PASS** (point equals AUROC difference exactly; `verify_batch1.json` → `paired_point_equals_auroc_difference` PASS) |
| n_articles=18, n_boot=2000, seed=12345 | `auroc_ci.json` → `n_articles=18, n_boot=2000, seed=12345, n_articles_held_out=18` | — | `csv` 1879 test items, `n_clusters=18` in `ci_cluster` | **PASS** |

**Cluster-band note (informational, not a mismatch):** `ci_cluster` (article-level)
for frozen test is [0.9760, 0.9874], corrected [0.8649, 0.8838], paired [0.1009, 0.1144] —
all still exclude each other / zero; the claimed [0.9774,0.9869]/[0.8585,0.8887]/[0.0950,0.1227]
are the `ci_item` ones. Disclose level when citing.
**Disposition: MF-17 numeric claims PASS** (`verify_batch1.json` → `auroc_ci` 8/8).

---

## MF-13 — two-sided separability audit (R4 inversion explicit)

**Generator:** `04_experiments/src/r3_exp_audit_twosided.py` (rule `pass_rule = "|AUROC - 0.5| <= 0.25"`)
→ `04_experiments/results/c1/r3/exp/audit_twosided.json`
**Command:** `python 04_experiments/src/r3_exp_audit_twosided.py` (5 tests pass)

| Claimed | File + key | Raw value | Verdict |
|---|---|---|---|
| R4 primary_6 dev 0.407, inverted | `audit_twosided.json` → `dev.per_rung["4"].auroc_primary_6` | `0.407, direction_primary_6="inverted", passes_primary_6=true, ci {lo=0.3674,hi=0.4469,n=800(seed 12345)}` | **PASS** |
| R4 with_lex dev 0.4047, inverted | … → `dev.per_rung["4"].auroc_with_lex` | `0.4047, direction_with_lex="inverted", passes_with_lex=true, ci {lo=0.3654,hi=0.445}` (0.405 @3dp ✓) | **PASS** |
| R1 with_lex dev 0.9762 | `dev.per_rung["1"].auroc_with_lex` | `0.9762, passes_with_lex=false (diff 0.4762>0.25)` | **PASS** |
| R2 with_lex dev 0.8901 | `dev.per_rung["2"].auroc_with_lex` | `0.8901, passes_with_lex=false (n=673, 273 negs)` | **PASS** |
| R3 with_lex dev 0.9235 | `dev.per_rung["3"].auroc_with_lex` | `0.9235, passes_with_lex=false` | **PASS** |
| top1 with_lex dev 0.7156 / test 0.7381 | `top1.dev.auroc_with_lex`, `top1.test.auroc_with_lex` | `0.7156 (n_hit=342/58), 0.7381 (313/87), both passes_with_lex=true` | **PASS** |

Full 4-rung dev/test × {primary_6, with_lex} table is present (incl. test R4
`0.4275/0.4332` inverted and template duplicates under `audit`, `original`,
`twosided_audit` — all identical values, no divergence).
**Disposition: MF-13 numeric claims PASS** (`verify_batch1.json` → `audit_twosided` 10/10 + supporting 6/6).

---

## MF-7 — "is this the gold paragraph" control

**File:** same `audit_twosided.json` → `gold_control` / `gold_indicator_control`

| Claimed | File + key | Raw value | Verdict |
|---|---|---|---|
| gold-indicator AUROC 1.0 | `gold_control.{dev,test}.per_rung.{1..4}.auroc_with_is_gold` (8 cells) | `1.0` in every dev/test × rung cell; `auroc_is_gold_alone=0.0, direction="normal", passes_with_is_gold=false` | **PASS** |
| top1 with_lex 0.7156/0.7381 | `top1.{dev,test}.auroc_with_lex` | `0.7156 / 0.7381` (see MF-13 above; present because top1-presented is the non-gold answerable control) | **PASS** |

**Note:** `auroc_is_gold_alone = 0.0` (not 1.0) — the indicator keyed as
"is-gold-alone" is the negated direction; it is the *combined* `with_is_gold`
that hits 1.0. `r4_robustness.json`/`both_runs.json` cells were **not** re-checked
here (out of Batch-1 scope).
**Disposition: MF-7 numeric claims PASS.**

---

## MF-12 — P(True)-style reader baseline

**Generator:** `04_experiments/src/r3_exp_ptruth.py` → `04_experiments/results/c1/r3/exp/ptruth_summary.json` + `ptruth_scores.csv` (553 rows + header)
**Command:** `python 04_experiments/src/r3_exp_ptruth.py` (9 tests pass)
**Endpoint:** `http://127.0.0.1:11434/api/generate` — `COMPUTE.md`

| Claimed | File + key | Raw value | Verdict |
|---|---|---|---|
| AUROC 0.2317, inverted 0.7683 | `ptruth_summary.json` → `auroc_answerable_vs_negative` | `0.23172608610948767` (independent pairwise recompute from the 553 CSV rows: `0.23172608610948764`, 118 pos / 435 neg — matches to 3e-17; 1− = 0.7683 ✓) | **PASS** |
| n=553 | `ptruth_summary.json` → `n_scored=553, n_dev_items_with_reader_scores=553` | CSV `wc -l` = 554 (header + 553) | **PASS** |
| threshold 0.80 infeasible | `ptruth_summary.json` → `threshold_080_rule.feasible` | `false (threshold=0.999984, n_refused=0, coverage=1.0, abstain_precision=null, recall=0.0)` | **PASS** |
| model differs from paper | `ptruth_summary.json` → `model_ollama="qwen2.5:1.5b-instruct"`, `paper_reader="Qwen/Qwen2.5-0.5B-Instruct"`, `model_differs_from_paper_reader=true`, plus `disclosure` string | `COMPUTE.md`: "model is NOT the paper's pinned reader", "not directly comparable to B4", Ollama 0.40.15 logprob-verified (top_logprobs ≤ 20, num_predict=1, temp=0.0) | **PASS** |

`per_rung_auroc` shows rung 0 = 118 answerable, rungs 1–4 = 118/81/118/118 negatives
— consistent with a dev-only, rung-0-vs-negatives design (no within-rung AUROC possible).
**Disposition: MF-12 numeric claims PASS** (`verify_batch1.json` → `ptruth` 4/4).

---

## Mismatches

**None in Batch-1 scope.** Every claimed number matches its JSON key within the
verify tolerances (`TOL_4DP=5e-05`, `TOL_3DP=5e-04`, exact for flags/1.0).
Two non-blocking presentation notes:
1. CI level must be named: claimed CIs are `ci_item` (percentile); `ci_cluster` differs slightly.
2. Gold control "1.0" refers to `auroc_with_is_gold`, while `auroc_is_gold_alone = 0.0` (direction flip) — cite the combined key.

## Summary disposition

| MF | Verdict | Key evidence |
|---|---|---|
| MF-17 | **PASS** | frozen 0.98236 / corrected 0.87385 / paired 0.10851 excl. zero; `auroc_ci` 8/8 |
| MF-13 | **PASS** | R4 0.407/0.4047 inverted (pass); R1–R3 0.9762/0.8901/0.9235 (fail); `audit_twosided` 10/10+6/6 |
| MF-7 | **PASS** | gold `with_is_gold` 1.0 all 8 cells; top1 0.7156/0.7381 |
| MF-12 | **PASS** | AUROC 0.23173 (recomputed) → inverted 0.7683; infeasible; model-differs disclosed; 553 rows |

Overall: `verify_batch1.json` overall PASS 50/50; pytest 21/21; `--check-repro` PASS.
**Label: exploratory/post-hoc** (as stored in every JSON).
