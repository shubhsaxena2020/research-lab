# Subagent report — MF-7 gold-paragraph control (R3-3b)

**Task:** recompute the existing gold-indicator control from existing item/feature
data and, where feasible, the D3 pooled top-1 hit/miss sanity comparison. Post-hoc
and exploratory only.

## Work performed

- Created `04_experiments/src/r3_r3_3b_mf7.py` (new lane script only).
- Ran `python 04_experiments/src/r3_r3_3b_mf7.py` (wall time ~112 s, exit 0).
- Wrote `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json`
  (294 flat `results` keys, all prefixed `c1.r3_3b.mf7.`).
- Wrote item report `04_experiments/results/c1/r3/R3-3b/MF-7.md`.
- No draft, template, review, results-index, preregistration or prior result was
  touched. No git commit/push.

## Observed results

- Gold-indicator control: base surface+lex AUROCs reproduce the prior
  `audit_twosided.json` cells exactly in all 8 dev/test × R1–R4 cells
  (dev 0.9762 / 0.8901 / 0.9235 / 0.4047; test 0.9794 / 0.8614 / 0.9059 /
  0.4332). Adding the construction-derived `is_gold` indicator yields AUROC 1.0
  in every cell with 10000-resample 95% CI [1.0, 1.0]; `is_gold` alone is 0.0 in
  the audit.py orientation (1.0 when oriented to answerable-as-positive).
  denominators: 400 answerables per split; R1/R3/R4 400/400 negatives (dev),
  R2 273 dev / 280 test, R4 test 399.
- D3 pooled (rung = −1): dev 342 hits / 58 misses (85.50%), test 313/87
  (78.25%), all 655/145 (81.87%). Surface+lex OOF AUROC 0.7156 dev
  [0.6441, 0.7833], 0.7381 test [0.6780, 0.7945], 0.7327 pooled
  [0.6894, 0.7739] (item-level bootstrap). These match the prior R3-3 top1
  points exactly. Dev-fitted logistic gate on the ten numeric features reaches
  test hit-vs-miss AUROC 0.9499 [0.9268, 0.9700] (18 article clusters
  [0.9372, 0.9648]); pooled single-feature AUROCs include
  `bm25_margin` 0.8978 and `ce_presented` 0.8637.
- D3 scope guard recorded explicitly: `rungs_present = [-1]` and
  `per_rung_R1_R3_estimand_available = false`. **No D3 per-rung R1–R3 estimate
  is claimed.**

## Provenance recorded in JSON

Command `python 04_experiments/src/r3_r3_3b_mf7.py`; bootstrap seed 20261118,
10000 resamples, percentile 2.5/97.5, item and article-cluster levels; OOF CV /
gate seed 12345 (matching `r3_exp_audit_twosided.py`; `audit.py` default 13);
SHA-256 of items.jsonl, items_top1.jsonl, features_top1.csv, audit.py,
r3_exp_audit_twosided.py and r3_exp_auroc_ci.py; all denominators;
`post_hoc: true`, `label: exploratory/post-hoc`.

## Verification performed

- Fast rank-sum bootstrap cross-checked against read-only
  `r3_exp_auroc_ci.bootstrap_auroc_ci` on 200 resamples: item and cluster
  levels both PASS with max_abs_diff 0.0; the check is stored in the JSON.
- Independent inline check of the written JSON (command run in this lane):
  command/seed/n_boot/post-hoc flag correct, all 294 keys prefixed, 27 prior
  point comparisons equal to 12 decimals, D3 scope flags correct, bootstrap
  validation PASS, denominators exact. Output ended `ALL PASS True result_keys 294`.

## Issues

- Two pre-output fixes were needed: unequal cluster sizes required a list of
  per-replicate index arrays, and the bootstrap cross-check compares rounded
  reference percentiles (the reference returns unrounded floats). Both fixed
  before the final run.
- The first attempt used audit.py's default CV seed 13, which changed the point
  estimates; switched to the R3-3 audit_twosided seed 12345 so the control is a
  faithful recomputation. Final JSON records both seeds.
