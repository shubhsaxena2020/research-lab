# Test run — r3_metrics intervals & H3 (R3-1)

Date: 2026-11-08

## Files created

- `04_experiments/src/tests/test_r3_metrics_intervals.py`
- `04_experiments/src/tests/test_r3_metrics_h3.py`

## Tests

### test_r3_metrics_intervals.py — 6 tests

- Clopper-Pearson upper for 0/400 ≈ 0.0092 (`lo == 0.0`, `hi == 0.0092`)
- Clopper-Pearson upper for 0/1479 ≈ 0.0025 (`lo == 0.0`, `hi == 0.0025`)
- Independent check via `scipy.stats.binomtest` (exact, 95%)
- Method mismatch detection: `interval_method_check.mismatch is True`, mismatched rungs `["1","3","4"]`, paper method `bca`, rung 2 archive `bca`
- Equivalence CI contains/excludes 0:
  - all_12 vs no_dense `[0.0038, 0.0196]` → `contains_zero False`
  - all_12 vs dense_only `[-0.0078, 0.0161]` → `contains_zero True`
  - frozen vs corrected `[0.0951, 0.1228]` → `contains_zero False`
- `main()` writes required keys (`command`, `seed=12345`, `H1`/`H3` CP bounds, etc.)

### test_r3_metrics_h3.py — 5 tests

- Degenerate equality check is false (`degenerate_check.equal is False`, `t != band_t_lo`)
- Constrained search returns no feasible threshold (`constrained_threshold_exists is False`, `max_feasible_recall < target_recall`)
- Independent recompute of degenerate equality via `gate.py`
- Independent exhaustive search over all unique dev scores (precision ≥ 0.80, recall ≥ band recall) → empty
- `main()` writes required keys (`command`, `seed=12345`, `constrained_search`, `degenerate_check`)

## Run

- Command: `python -m pytest 04_experiments/src/tests/test_r3_metrics_intervals.py 04_experiments/src/tests/test_r3_metrics_h3.py -q`
- Result: **11 passed in 238.61s**
  - intervals: **6 passed in 92.86s**
  - h3: **5 passed in 254.76s**
- Exit code: **0**

## Notes

- Runtimes are dominated by in-process `main()` re-runs (intervals `N_BOOT=10000`, h3 `N_BOOT=10000` plus exhaustive threshold search).
- The `pytest` import diagnostic from the editor LSP is cosmetic — tests run under the project venv.
