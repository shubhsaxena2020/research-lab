# MF-7 — gold-paragraph control (R3-3b, post-hoc)

**Status:** exploratory / post-hoc re-derivation from existing data. No frozen
result is revised; no draft or prior result file was edited.

**Item (round-2 reviewer objection):** the surface+lexical audit's R1/R2/R3
separation (0.977 / 0.889 / 0.923) may measure "is this the gold paragraph?"
rather than rung hardness, because answerable items always present the gold
paragraph and the negatives never do.

## Design

1. **Gold-indicator control.** From `items.jsonl`, for each split (dev, test) and
   rung R1–R4, compare the 400 answerable items (rung 0) with that rung's
   negatives on the eight `audit.surface_features(with_lex=True)` columns.
   Compute five-fold stratified OOF logistic AUROC, then repeat with the binary
   `is_gold` column appended. `is_gold` is derived from construction: 1 for
   rung 0, 0 for rungs 1–4. AUROC direction follows `audit.py` (y = 1 for the
   rung negative), so `is_gold` alone has raw AUROC 0.0 and answerable-oriented
   AUROC 1.0.
2. **D3 sanity (pooled only).** `items_top1.jsonl` and `features_top1.csv`
   contain only `rung = -1` top-1-presented items: label 1 = "hit" (BM25 rank-1
   is the gold paragraph), label 0 = "miss". The same surface+lex audit is run
   on the pooled hit-vs-miss contrast per split and across splits. Individual
   feature AUROCs and a dev-fitted logistic gate on the ten numeric
   `features_top1.csv` columns (scored on test) are reported as a sanity check
   that the feature stack detects retrieval correctness.
3. **Intervals.** Non-parametric percentile bootstrap, 10000 resamples, seed
   20261118, 2.5/97.5 percentiles, at both the item level and the
   article-title-cluster level (18 titles). Item-id and label alignment between
   `items_top1.jsonl` and `features_top1.csv` is asserted in code.

## Findings

Gold-indicator control (base = surface+lex; plus = base + `is_gold`):

| Split / rung | n (pos + neg) | base AUROC | base 95% CI (item) | plus `is_gold` | `is_gold` alone (raw / oriented) | Δ AUROC |
|---|---:|---:|---:|---:|---:|---:|
| dev R1 | 400 + 400 = 800 | 0.9762 | [0.9665, 0.9845] | 1.0000 | 0.0000 / 1.0000 | +0.0238 |
| dev R2 | 400 + 273 = 673 | 0.8901 | [0.8641, 0.9147] | 1.0000 | 0.0000 / 1.0000 | +0.1099 |
| dev R3 | 400 + 400 = 800 | 0.9235 | [0.9047, 0.9408] | 1.0000 | 0.0000 / 1.0000 | +0.0765 |
| dev R4 | 400 + 400 = 800 | 0.4047 | [0.3667, 0.4451] | 1.0000 | 0.0000 / 1.0000 | +0.5953 |
| test R1 | 400 + 400 = 800 | 0.9794 | [0.9714, 0.9865] | 1.0000 | 0.0000 / 1.0000 | +0.0206 |
| test R2 | 400 + 280 = 680 | 0.8614 | [0.8331, 0.8881] | 1.0000 | 0.0000 / 1.0000 | +0.1386 |
| test R3 | 400 + 400 = 800 | 0.9059 | [0.8849, 0.9255] | 1.0000 | 0.0000 / 1.0000 | +0.0941 |
| test R4 | 400 + 399 = 799 | 0.4332 | [0.3927, 0.4732] | 1.0000 | 0.0000 / 1.0000 | +0.5668 |

All eight base point estimates reproduce `audit_twosided.json` exactly; adding
the construction-derived gold indicator gives a perfect AUROC of 1.0 in every
cell, with 95% bootstrap interval [1.0000, 1.0000]. This is a label artefact,
not new evidence about the gate.

D3 pooled hit/miss sanity (rung = −1 only):

| Scope | hits / misses | hit rate | surface+lex AUROC | 95% CI (item / cluster) |
|---|---:|---:|---:|---:|
| dev | 342 / 58 | 85.50% | 0.7156 | [0.6441, 0.7833] / [0.6438, 0.7870] |
| test | 313 / 87 | 78.25% | 0.7381 | [0.6780, 0.7945] / [0.6813, 0.7909] |
| all | 655 / 145 | 81.87% | 0.7327 | [0.6894, 0.7739] / [0.6859, 0.7794] |

Feature-stack sanity on pooled D3 (all splits): `bm25_margin` AUROC 0.8978
[0.8748, 0.9192], `ce_presented` 0.8637 [0.8300, 0.8946], `lex_overlap` 0.7072
[0.6615, 0.7517], `dense_presented` 0.7250 [0.6779, 0.7708]. The dev-fitted
logistic gate on the ten numeric features reaches test AUROC 0.9499
(item CI [0.9268, 0.9700], cluster CI [0.9372, 0.9648]; 400 hits / 87 misses
scored), consistent with the paper's retrieval-correctness detector.

**Reading.** When gold presence varies (D3), surface+lex separation is ~0.72–0.74
rather than 0.89–0.98; the feature stack still detects retrieval correctness
well. This supports the stated confound limitation. It does **not** exculpate the
gate, and it is not a re-estimation of the reviewer's requested D3 R1–R3
comparison.

## Limitations

- The gold indicator is a deterministic function of the label by construction;
  the AUROC = 1.0 control is tautological and carries no independent information.
- **D3 has only pooled rung = −1 hit/miss observations in these files. There are
  no D3 R1/R2/R3 items, so no D3 per-rung R1–R3 estimand is available and none is
  claimed.** The D3 numbers above are pooled hit-vs-miss sanity checks only.
- The dev-fitted gate uses a simple standardized logistic model over the ten
  numeric features in `features_top1.csv` and is not the frozen paper gate.
- All results are exploratory/post-hoc with no confirmatory status.

## Evidence and reproducibility

- Script: `04_experiments/src/r3_r3_3b_mf7.py`
- JSON: `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json`
- Command: `python 04_experiments/src/r3_r3_3b_mf7.py`
- Seeds: bootstrap 20261118; OOF CV and gate random_state 12345 (matches
  `r3_exp_audit_twosided.py`; `audit.py` default is 13). Bootstrap: 10000
  resamples, percentile 2.5/97.5, item and article-cluster levels. The fast
  rank-sum bootstrap was cross-checked against
  `r3_exp_auroc_ci.bootstrap_auroc_ci` on 200 resamples; both levels matched
  exactly (max_abs_diff 0.0).
- Inputs (SHA-256): `items.jsonl` c6f46ad80e7d15f495cd2a4b1e7b5a5556bfa929264c7afabd81826dd8d049d0;
  `items_top1.jsonl` a586606d6ec23b10f86c9104e343e77ccc2fc03130feb0bc5cb014a39f42ed55;
  `features_top1.csv` 3d22e100c1991ed63b3155ef6f0f66a873377d410ce0b9d629346ed4185e4a5c;
  `audit.py` 9db4b2464181c547de4f2ce5e44eb9c4b7618cbce1f74a80064871a215e8b7b2;
  `r3_exp_audit_twosided.py` 1b03bcbf95f096d551d6a2188558bb84cb898f7e7a2e937dcec8acdae19e7971;
  `r3_exp_auroc_ci.py` 8330d275210f3f7f88c13157a674e85aa6a8088204d4c700d614ff63e25c6062.

## Bindable result keys (exact)

All keys live under the JSON `results` object and start with `c1.r3_3b.mf7.`.

Gold control, base AUROC (replace `{S}` with `dev`/`test`, `{R}` with `1`–`4`):
`c1.r3_3b.mf7.gold_control.{S}.r{R}.auroc_surface_lex`.
With the artefact indicator: `...auroc_plus_is_gold` and
`...auroc_is_gold_alone_answerable_oriented` (also
`...auroc_is_gold_alone_raw` for the audit.py orientation); increment:
`...delta_auroc_plus_minus_base`; denominators: `...n_answerable`, `...n_negatives`, `...n`.
Intervals: `...auroc_surface_lex_ci_{item|cluster}_{lo|hi}`,
`...auroc_plus_is_gold_ci_{item|cluster}_{lo|hi}`,
`...delta_auroc_ci_{item|cluster}_{lo|hi}`.

D3 pooled (replace `{S}` with `dev`/`test`/`all`):
`c1.r3_3b.mf7.d3_pooled.{S}.n_hit`, `...n_miss`, `...hit_rate`,
`...auroc_surface_lex_hit_vs_miss`,
`...auroc_surface_lex_ci_{item|cluster}_{lo|hi}`,
`...feature_{bm25_margin|ce_presented|dense_presented|lex_overlap|...}_auroc`
and `...feature_..._ci_item_{lo|hi}`.
Gate sanity: `c1.r3_3b.mf7.d3_pooled.dev_fit_gate.test.auroc_hit_vs_miss`,
`...ci_{item|cluster}_{lo|hi}`, `...n_dev_fit`, `...n_test`.
Scope guards: `c1.r3_3b.mf7.d3_pooled.per_rung_R1_R3_estimand_available` (false),
`c1.r3_3b.mf7.d3_pooled.rungs_present_value` (−1).

To enumerate all 294 keys:
`python -c "import json;print('\\n'.join(json.load(open('04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json'))['results']))"`
