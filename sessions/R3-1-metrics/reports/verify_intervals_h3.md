# Verify intervals and H3 deliverables — R3-1

Date: 2026-11-08 (verification run)

## 1. Script re-runs

- Command: `python 04_experiments/src/r3_metrics_intervals.py` (run from `C:/Users/shubh/research-lab`)
  - Exit code: **0**
  - Outputs (re)written:
    - `04_experiments/results/c1/r3/metrics/intervals.json`
    - `04_experiments/results/c1/r3/metrics/intervals.md`
    - `sessions/R3-1-metrics/reports/r3_metrics_intervals.md`
- Command: `python 04_experiments/src/r3_metrics_h3.py` (run from `C:/Users/shubh/research-lab`)
  - Exit code: **0**
  - Outputs (re)written:
    - `04_experiments/results/c1/r3/metrics/h3.json`
    - `sessions/R3-1-metrics/reports/r3_metrics_h3.md`

## 2. Independent checks

### Clopper-Pearson upper bounds (scipy.stats.binomtest, exact, 95%)

| x/n | independent upper (raw) | rounded (4 dp) | intervals.json | match |
|---|---:|---:|---:|---|
| 0/400 | 0.009179804583673406 | 0.0092 | 0.0092 | yes |
| 0/1479 | 0.002491063507609249 | 0.0025 | 0.0025 | yes |

(Wilson upper bounds also reproduce: 0/400 = 0.0095, 0/1479 = 0.0026.)

### Cluster bootstrap

- `stats_addendum.json` cluster_bootstrap.n_articles_test = **18** (matches required value).
- Finite width ratios: per_rung/2 = 0.4521, exploratory_band/{1,2,3,4} = {0.5435, 0.8511, 0.9034, 1.1658}; minimum = **0.4521** (matches required value and intervals.json `min_width_ratio_archive`).

### Equivalence CIs contain/exclude 0 (intervals.json)

| comparison | CI [lo, hi] | contains_zero flag | actual contains 0? | match |
|---|---|---|---|---|
| all_12 vs no_dense | [0.0038, 0.0196] | false | no | yes |
| all_12 vs dense_only | [-0.0078, 0.0161] | true | yes | yes |
| frozen vs corrected | [0.0951, 0.1228] | false | no | yes |

### H3 constrained threshold search

- `h3.json` constrained_search.constrained_threshold_exists = **false**.
- Independent recompute over all unique dev scores: 1790 precision-compliant thresholds (precision >= 0.80), max feasible recall = 0.97556, below the band dev recall 0.9898; no precision-compliant threshold reaches the band recall. Matches h3.json and its report statement.

## 3. Mismatches

None found in the verified scope (script exit codes, Clopper-Pearson upper bounds, n_articles, min width ratio, equivalence contain/exclude flags, H3 constrained-threshold feasibility).

Note: the deliverables themselves document separate, already-known findings that are not verification mismatches — the interval-method mismatch (paper states BCa; archive records percentile for rungs 1, 3, 4) and the all_12 vs no_dense interval excluding zero (which narrows the "no single group carries the result" wording). These are consistent with the recomputed values above.