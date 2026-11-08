# r3_metrics_core report

Script: `04_experiments/src/r3_metrics_core.py`
Command: `python 04_experiments/src/r3_metrics_core.py`
Seed: 20261103
Outputs: `04_experiments/results/c1/r3/metrics/{DEFINITIONS.md,metrics.json,metrics.md}`

Key numbers:
- Frozen band: pooled precision 0.83, coverage (item) 0.05, coverage (question) 0.25 (98/400), over-refusal 0.76.
- Frozen exploratory band: pooled precision 0.97, coverage (item) 0.25, coverage (question) 0.91 (362/400), over-refusal 0.10.
- Corrected band: pooled precision 0.80, coverage (item) 0.04, coverage (question) 0.09 (34/400), over-refusal 0.92.
- Corrected exploratory band: pooled precision 0.96, coverage (item) 0.40, coverage (question) 0.89 (356/400), over-refusal 0.11.
- Top-1 (band_target_precision_0.80, test): refuse_miss 0.63 (n_misses=87), precision_miss_given_refused 0.87 (n_refused=63), coverage 0.84.
- All five arms included for both runs (band_primary, exploratory_band, exploratory_single, single_B3, single_matched_recall).

Inputs sha256 recorded in metrics.json.
JSON parses: verified.
