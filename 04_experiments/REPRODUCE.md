# REPRODUCE — C1 (MF-33)

All commands run from the repository root `C:\Users\shubh\research-lab` unless noted.
Interpreter: the Hermes venv `python` (3.11.15); set `PYTHONHASHSEED=0` in the
environment before any run. Frozen inputs must be present first:
`04_experiments/data/raw/dev-v2.0.json` (sha256
`80a5225e94905956a6446d296ca1093975c4d3b3260f1d6c8f68bc2ab77182d8`) and
`04_experiments/data/raw/2wiki/2wikimultihop_dev.json`.

Lockfile: `04_experiments/requirements-lock.txt`,
sha256 `a49823349ededc0869dcc881b0ccc99c73d0723d96062087988eb02066a481a1`.
Environment: `04_experiments/ENVIRONMENT.md`.

Heavy compute: one job at a time through `ops/HEAVY.lock`
(`04_experiments/harness/lock.py`). The reader baseline is the only long CPU
job; everything else is minutes on CPU.

## Ordered command list

Run in this order. Each step writes the named artefact; later steps depend on
the earlier ones' outputs.

1. `python 04_experiments/src/build_items.py`
   - Builds `data/items.jsonl` + `data/item_stats.json` (4,000 paired items).
   - Seeds: `SPLIT_SEED=7`, `DATA_SEED=20261103`.

2. `python 04_experiments/src/features.py`
   - As-run retrieval features -> `data/features.csv` + `data/features_meta.json`.
   - Uses `BAAI/bge-small-en-v1.5` @ `5c38ec7c405ec4b44b94cc5a9bb96e735b38267a`
     and `cross-encoder/ms-marco-MiniLM-L-6-v2` @ `233902d25c440f23af6f7d6e94d2946bac0bee0a`.
   - Dense block is degenerate by construction (see D4); kept as the frozen run.

3. `python 04_experiments/src/run_c1.py`
   - Pre-registered analysis -> `results/c1/results_full.json`, `audit.json`,
     `predictions.csv`. Run time ~6.5 s on CPU. Confirmatory only.

4. `python 04_experiments/src/features_corrected.py`
   - Spec-corrected features -> `data/features_corrected.csv` (+ rung5/transfer).

5. `python 04_experiments/src/eval_corrected.py`
   - Corrected analysis -> `results/c1_corrected/`.

6. `python 04_experiments/src/build_items_rung5.py && python 04_experiments/src/features_rung5.py && python 04_experiments/src/eval_rung5.py`
   - R5 control arm -> `results/c1/rung5.json` (exploratory).

7. `python 04_experiments/src/features_transfer.py && python 04_experiments/src/eval_transfer.py`
   - Transfer features + frozen operating point on 2Wiki -> `results/c1/transfer.json`.

8. `python 04_experiments/src/build_items_top1.py && python 04_experiments/src/features_top1.py && python 04_experiments/src/eval_top1.py`
   - Top-1 control arm -> `results/c1/top1_variant.json` (exploratory).

9. `python 04_experiments/src/ablation_corrected.py`
   - Leave-one-group-out ablations -> `results/c1_corrected/ablations.json`.

10. `python 04_experiments/src/stats_addendum.py`
    - Statistics addendum -> `results/c1/stats_addendum.json`, `ablations.json`,
      `STATS-ADDENDUM.md`.

11. `python 04_experiments/src/build_transfer_items.py`
    - Second-corpus item builder -> `data/transfer_items.jsonl` (400 items).
    - Must run before step 7's features/eval; listed here to make the transfer
      item builder explicit (MF-33).

12. `python 04_experiments/src/reader_logprob.py --model Qwen/Qwen2.5-0.5B-Instruct --batch-size 8`
    - Reader baseline B4 -> `data/reader_features.csv` (+ errors/meta).
    - Heavy CPU job (~minutes); run alone, RAM >= 8 GB. Dev-only, 553 items.
    - Model revision `7ae557604adf67be50417f59c2c2f167def9a775`.

13. `python 04_experiments/src/precision_metrics.py`
    - Refusal/precision split -> `results/c1/precision_metrics.json` and
      `results/c1_corrected/precision_metrics.json`.

14. `python 04_experiments/src/make_paper_assets.py`
    - Tables + index entries.

15. `python 05_paper/build_draft.py`
    - Regenerates `05_paper/draft/paper.md` from the template.

16. `python tools/check_numbers.py --draft 05_paper/draft/paper.md`
    - Must PASS (zero findings).

## Harness provenance (toy smoke test)

```
python 04_experiments/harness/runner.py --experiment toy \
  --config 04_experiments/harness/configs/toy_baseline.json
```
and the reproducibility check
```
python 04_experiments/harness/runner.py --experiment toy \
  --config 04_experiments/harness/configs/toy_baseline.json --check-repro 3
```
Harness tests: `python -m pytest 04_experiments/harness/tests -q` (72 passed on
2026-11-08).

## Verification status (this lane, 2026-11-08)

- Cheap checks run: `--help` on `build_items.py`, `features.py`, `run_c1.py`,
  `runner.py`; `python -m pytest 04_experiments/harness/tests -q` (72 passed);
  `python -m pytest 04_experiments/src/tests -q` (21 passed).
- Heavy experiment commands above are **not re-run** (would overwrite immutable
  frozen outputs in `04_experiments/results/` and `04_experiments/data/`).
  They are recorded here for reproducibility only.
- `build_transfer_items.py` was executed once during verification and reproduced
  `transfer_items.jsonl` (400 rows, sha256 `2ae0ce0c40aa8a70828ae8aa775621dc5fe4cdcdcfdad0795d362ee01d6a1e09`),
  matching the committed file; no other data or result file was overwritten.
}