# R3 metrics (core)

Command: `python 04_experiments/src/r3_metrics_core.py`
Seed: 20261103

## Inputs (sha256)
- frozen_predictions: `154ed6df4756ae28a13823ffdf6811db0e7c6809d5d23498cb799e24ccd03133`
- corrected_predictions: `95eac015e11cca67141e3139f28cd9a49b39adf9a6ccd55935d2d70ae6632393`
- frozen_results_full: `e4cf65cb0b2bae52e4ee4b379e0c4e66450ed21474d71b57e49e8d4218c36b35`
- corrected_results_full: `936ce0b89e2231092b9fd71243db9456c267208376ea580c888ee4d0dfcc6ff6`
- top1_variant: `299c3e0569b4cef98342ac57930ce2b12398f00a7810a5b4bb80df7af7b65117`

## Run: frozen

### Operating point: band (column `band_refused`)

| cell | n | n_refused | refusal_rate | abstain_precision |
|---|---|---|---|---|
| answerable (rung 0) | 400 | 302 | 0.76 | - |
| rung 1 | 400 | 400 | 1.00 | 0.57 |
| rung 2 | 280 | 279 | 1.00 | 0.48 |
| rung 3 | 400 | 400 | 1.00 | 0.57 |
| rung 4 | 399 | 399 | 1.00 | 0.57 |
| pooled negatives | 1479 | 1478 | 1.00 | 0.83 |

- coverage (item): 0.0527 -> 0.05
- coverage (question): 0.2450 (98/400)
- over_refusal: 0.7550
- pooled precision: 0.8303370786516854

### Operating point: exploratory_band (column `expl_band_refused`)

| cell | n | n_refused | refusal_rate | abstain_precision |
|---|---|---|---|---|
| answerable (rung 0) | 400 | 38 | 0.10 | - |
| rung 1 | 400 | 399 | 1.00 | 0.91 |
| rung 2 | 280 | 255 | 0.91 | 0.87 |
| rung 3 | 400 | 371 | 0.93 | 0.91 |
| rung 4 | 399 | 338 | 0.85 | 0.90 |
| pooled negatives | 1479 | 1363 | 0.92 | 0.97 |

- coverage (item): 0.2544 -> 0.25
- coverage (question): 0.9050 (362/400)
- over_refusal: 0.0950
- pooled precision: 0.9728765167737331

## Run: corrected

### Operating point: band (column `band_refused`)

| cell | n | n_refused | refusal_rate | abstain_precision |
|---|---|---|---|---|
| answerable (rung 0) | 400 | 366 | 0.92 | - |
| rung 1 | 400 | 400 | 1.00 | 0.52 |
| rung 2 | 280 | 279 | 1.00 | 0.43 |
| rung 3 | 400 | 400 | 1.00 | 0.52 |
| rung 4 | 399 | 362 | 0.91 | 0.50 |
| pooled negatives | 1479 | 1441 | 0.97 | 0.80 |

- coverage (item): 0.0383 -> 0.04
- coverage (question): 0.0850 (34/400)
- over_refusal: 0.9150
- pooled precision: 0.7974543442169342

### Operating point: exploratory_band (column `expl_band_refused`)

| cell | n | n_refused | refusal_rate | abstain_precision |
|---|---|---|---|---|
| answerable (rung 0) | 400 | 44 | 0.11 | - |
| rung 1 | 400 | 399 | 1.00 | 0.90 |
| rung 2 | 280 | 260 | 0.93 | 0.86 |
| rung 3 | 400 | 382 | 0.95 | 0.90 |
| rung 4 | 399 | 50 | 0.13 | 0.53 |
| pooled negatives | 1479 | 1091 | 0.74 | 0.96 |

- coverage (item): 0.3960 -> 0.40
- coverage (question): 0.8900 (356/400)
- over_refusal: 0.1100
- pooled precision: 0.9612334801762115

## Arms (from results_full.json)

| run | arm | coverage | over_refusal | pooled_abstain_precision |
|---|---|---|---|---|
| frozen | band_primary | 0.05 | 0.76 | 1.00 |
| frozen | exploratory_band | 0.25 | 0.10 | 0.92 |
| frozen | exploratory_single | 0.22 | 0.15 | 0.96 |
| frozen | single_B3 | 0.02 | 0.93 | 1.00 |
| frozen | single_matched_recall | 0.06 | 0.72 | 1.00 |
| corrected | band_primary | 0.04 | 0.92 | 0.97 |
| corrected | exploratory_band | 0.40 | 0.11 | 0.74 |
| corrected | exploratory_single | 0.38 | 0.13 | 0.76 |
| corrected | single_B3 | 0.05 | 0.87 | 0.97 |
| corrected | single_matched_recall | 0.01 | 0.98 | 1.00 |

## Top-1 arm (band_target_precision_0.80, test)

- refuse_miss P(refused|miss) = 0.63 (n_misses=87)
- precision_miss_given_refused P(miss|refused) = 0.87 (n_refused=63)
- coverage = 0.84
