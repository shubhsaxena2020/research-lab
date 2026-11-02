TOY - NOT A RESULT

# Toy experiment (pipeline smoke test)

This directory exists for exactly one reason: to prove that the experiment
harness works end to end. **Nothing here is a scientific result.** No number
produced by this folder may be cited, tabulated, quoted or used in a claim in
any draft. The contract banner form is `TOY — NOT A RESULT` (see
`tools/CONTRACTS.md` section 5); the ASCII first line above is the same label.

## What it does

`task.py` builds a deterministic synthetic two-class problem and fits two
models:

| config (`harness/configs/`) | model | what it is |
|---|---|---|
| `toy_baseline.json` | `centroid` | nearest class mean, the "baseline" |
| `toy_ours.json` | `logistic` | binary logistic regression from scratch, full-batch GD on log loss |

The data are two anisotropic gaussian blobs (class 0 wider on one axis, class 1
on the other), rotated by 20 degrees, drawn from `random.Random(seed)`, split
70/30 into train/test with a second seeded RNG. Same seed => byte-identical
data. `run_task(config)` returns the flat metric dict that the runner stores:
`accuracy`, `accuracy_train`, `f1_macro`, `loss`, `n_train`, `n_test`, `model`.

`run_toy.py` runs 3 seeds x 2 configs through `harness/runner.run`, writes
`toy_runs.json`, then calls `harness/aggregate.py` to produce
`04_experiments/results/summary_toy.json` and the matching
`04_experiments/RESULTS-INDEX.json` entries.

```bash
python 04_experiments/toy/run_toy.py                 # ~1.3 s, 6 runs
python 04_experiments/toy/run_toy.py --seeds 0 1     # fewer seeds
python 04_experiments/toy/run_toy.py --no-aggregate  # skip summary/index
```

## Why it is safe

* every JSON written here (and every `meta.json` / `results.json` of a toy run)
  carries `"toy": true`;
* `RESULTS-INDEX.json` entries are prefixed `toy.` and flagged `"toy": true`,
  so `tools/check_numbers.py` can reject them without `--allow-toy`;
* the runner's provenance is real (git hash, timing, RSS, config hash) -- only
  the *data* is synthetic.

To keep the real number index clean after experimenting, re-run the aggregator
with `--no-index` or delete the `toy.*` entries.
