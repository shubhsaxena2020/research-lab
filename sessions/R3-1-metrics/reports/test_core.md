# Test core metrics deliverable — R3-1

Date: 2026-11-08 (test run)

## 1. Test file

- Path: `04_experiments/src/tests/test_r3_metrics_core.py`
- Tests:
  - `test_handmade_10row_fixture_metrics` — 10-row hand-made fixture (2 answerable rung-0 + 8 negatives across rungs 1-4) with hand-computed refusal_rate, per-rung precision, pooled precision, coverage_item, coverage_question.
  - `test_definitions_md_required_definitions_present` — DEFINITIONS.md contains required definitions (abstain precision, refusal rate, over-refusal, coverage, abstain recall).
  - `test_metrics_json_frozen_and_corrected` — metrics.json has frozen and corrected runs with per_rung refusal_rate and abstain_precision.

## 2. Test run

- Command: `python -m pytest 04_experiments/src/tests/test_r3_metrics_core.py -q`
- Exit code: **0**
- Result: **3 passed**

## 3. Notes

- No mismatches; pytest import resolves at runtime via the project environment.
- Owned deliverables: test file + this report.
