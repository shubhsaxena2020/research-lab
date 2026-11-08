# Verify rung2 deliverable — R3-1

Date: 2026-11-08 (verification run)

## 1. Script re-run

- Command: `python 04_experiments/src/r3_metrics_rung2.py` (run from `C:/Users/shubh/research-lab`)
- Exit code: **0**
- Outputs (re)written:
  - `04_experiments/results/c1/r3/metrics/rung2.json`
  - `sessions/R3-1-metrics/reports/r3_metrics_rung2.md`

## 2. Tests

- Command: `python -m pytest 04_experiments/src/tests/test_r3_metrics_rung2.py -q`
- Exit code: **0**
- Result: **2 passed** (test_shortfall_counts, test_json_written_with_required_keys)

## 3. Independent recompute (exchangeability min p-value from items.jsonl)

Method: read `04_experiments/data/items.jsonl` directly; for each split, take rung-0 rows as the 400 sampled questions, mark a question "kept" when a rung-2 row with its qid exists in items.jsonl (otherwise dropped). Compute `q_chars`, `q_tokens`, `gold_chars`, `n_paragraphs` (paragraph count from `dev-v2.0.json`) and `answer_type` (from `gold_answer`) on the rung-0 row; run two-sided Mann-Whitney U (no continuity correction) for the four continuous variables and the Monte Carlo permutation chi-square (10,000 draws, seed 12345) for the 5x2 answer-type table. No use of `r3_metrics_rung2` or `stats_addendum` helpers. Collapsed 2x2 Fisher p-values also recomputed.

Shortfall counts: dev 273 kept / 127 dropped; test 280 kept / 120 dropped (matches script).

### p-values, independent vs rung2.json (dev)

| variable | independent | rung2.json | match |
|---|---:|---:|---|
| q_chars | 0.052366 | 0.052366 | yes |
| q_tokens | 0.362028 | 0.362028 | yes |
| gold_chars | 0.087968 | 0.087968 | yes |
| n_paragraphs | 0.924249 | 0.924249 | yes |
| answer_type | 0.354065 | 0.354065 | yes |

### p-values, independent vs rung2.json (test)

| variable | independent | rung2.json | match |
|---|---:|---:|---|
| q_chars | 0.69666 | 0.69666 | yes |
| q_tokens | 0.620548 | 0.620548 | yes |
| gold_chars | 0.210955 | 0.210955 | yes |
| n_paragraphs | 0.442933 | 0.442933 | yes |
| answer_type | 0.262774 | 0.262774 | yes |

### Min p-value

- Independent: 0.052366 (`dev/q_chars`)
- rung2.json `min_p`: 0.052366 (`dev/q_chars`)
- Match: **yes**

Collapsed Fisher p-values also reproduced: dev name_vs_other 0.080542, dev numeric_vs_other 0.469841, test name_vs_other 0.232892, test numeric_vs_other 0.098295 (all consistent with rung2.json).

## 4. Mismatches

None found within the verified scope (script exit code, test pass, shortfall counts, p-values, min p-value).
