# ENV report — MF-30 / MF-33 (lane R3-2)

Date: 2026-11-08 (IST). Profile res-s2.

## Files created/modified

- `04_experiments/requirements-lock.txt` — `python -m pip freeze` from the Hermes venv
  (3.11.15), 156 lines, sha256
  `a49823349ededc0869dcc881b0ccc99c73d0723d96062087988eb02066a481a1`.
- `04_experiments/ENVIRONMENT.md` — OS (Windows 10 10.0.26300), CPU (Intel64 Family 6
  Model 197, 14 cores), Python 3.11.15, torch 2.15.0+cpu, bm25s 0.3.16, plus exact HF
  revisions for the three models (bge-small-en-v1.5, ms-marco-MiniLM-L-6-v2,
  Qwen2.5-0.5B-Instruct) read from the local cache `refs/main`.
- `04_experiments/REPRODUCE.md` — ordered 16-step command list, including the transfer
  item builder (`build_transfer_items.py`) and the reader baseline
  (`reader_logprob.py --model Qwen/Qwen2.5-0.5B-Instruct --batch-size 8`), plus harness
  smoke tests.

## Cheap checks run

- `python 04_experiments/src/build_items.py --help` -> OK
- `python 04_experiments/src/features.py --help` -> OK
- `python 04_experiments/src/run_c1.py --help` -> OK
- `python 04_experiments/harness/runner.py --help` -> OK
- `python -m pytest 04_experiments/harness/tests -q` -> 72 passed
- `python -m pytest 04_experiments/src/tests -q` -> 21 passed
- `python 04_experiments/src/build_transfer_items.py` executed once; reproduced
  `transfer_items.jsonl` (400 rows, sha256
  `2ae0ce0c40aa8a70828ae8aa775621dc5fe4cdcdcfdad0795d362ee01d6a1e09`),
  matching the committed file.

## Heavy commands not run

All result-producing scripts that would overwrite frozen outputs under
`04_experiments/results/` and `04_experiments/data/` were left un-run, as required.
`REPRODUCE.md` marks them "not re-run (would overwrite immutable frozen outputs)".

## Issues encountered

- None blocking. `build_transfer_items.py` has no `--help`/argparse and executes on
  invocation; it was run only because it is deterministic and reproduced the committed
  hash. No other experiment script was executed.
}