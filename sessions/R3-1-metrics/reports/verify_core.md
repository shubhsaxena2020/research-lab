# Verify core metrics deliverable — R3-1

Date: 2026-11-08 (verification run)

## 1. Script re-run

- Command: `python 04_experiments/src/r3_metrics_core.py` (run from `C:/Users/shubh/research-lab`)
- Exit code: **0**
- Outputs (re)written:
  - `04_experiments/results/c1/r3/metrics/DEFINITIONS.md`
  - `04_experiments/results/c1/r3/metrics/metrics.json`
  - `04_experiments/results/c1/r3/metrics/metrics.md`

## 2. Independent recompute (band column, test split)

Method: read `predictions.csv` directly, filter `split == "test"`, count `band_refused == "1"` per rung, compute pooled precision = `n_refused_negatives / (n_refused_negatives + n_refused_answerable)`. No use of `r3_metrics_core` helpers.

### Frozen run (`04_experiments/results/c1/predictions.csv`)

| rung | n | n_refused (independent) | n_refused (metrics.json) | match |
|---|---|---|---|---|
| 0 (answerable) | 400 | 302 | 302 | yes |
| 1 | 400 | 400 | 400 | yes |
| 2 | 280 | 279 | 279 | yes |
| 3 | 400 | 400 | 400 | yes |
| 4 | 399 | 399 | 399 | yes |
| pooled precision | — | 0.8303370786516854 | 0.8303370786516854 | yes |

### Corrected run (`04_experiments/results/c1_corrected/predictions.csv`)

| rung | n | n_refused (independent) | n_refused (metrics.json) | match |
|---|---|---|---|---|
| 0 (answerable) | 400 | 366 | 366 | yes |
| 1 | 400 | 400 | 400 | yes |
| 2 | 280 | 279 | 279 | yes |
| 3 | 400 | 400 | 400 | yes |
| 4 | 399 | 362 | 362 | yes |
| pooled precision | — | 0.7974543442169342 | 0.7974543442169342 | yes |

Result: **no mismatches** in per-rung refusal counts or pooled precision for the band column between independent recompute and `metrics.json` for either run.

## 3. DEFINITIONS.md

- Path: `04_experiments/results/c1/r3/metrics/DEFINITIONS.md` — exists.
- Required definitions present:
  - Abstain precision — yes
  - Per-rung refusal rate — yes
  - Over-refusal — yes
  - Coverage — yes
  - Abstain recall — yes
- Note: file lists 6 bullets (item-level coverage in addition to question-level coverage); all five required definitions are present. Not a mismatch.

## 4. metrics.md

- Path: `04_experiments/results/c1/r3/metrics/metrics.md` — exists (100 lines).

## 5. Mismatches

None found within the verified scope (script exit code, per-rung refusal counts, pooled precision, definition presence, metrics.md existence).
