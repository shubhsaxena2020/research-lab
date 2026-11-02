# Experiment harness

Reproducible runs with provenance, a single-slot heavy-compute lock, and the
aggregator that feeds `04_experiments/results/` and `RESULTS-INDEX.json`.
Formats follow `tools/CONTRACTS.md` sections 2-4; operations follow
`RULES.md` #2 (every number from a logged run), #10 (heavy compute one at a
time) and #12 (save state).

```
04_experiments/harness/
  runner.py     # run() + CLI + --check-repro
  lock.py       # ops/HEAVY.lock semantics + CLI
  aggregate.py  # runs -> summary_<experiment>.json -> RESULTS-INDEX.json
  configs/      # committed configs (toy_baseline.json, toy_ours.json)
  tests/        # pytest: test_runner.py (runner, lock, aggregate)
  stats.py      # owned by another worker: bootstrap CIs, paired tests, effects
  tables.py     # owned by another worker: table generation
```

## Running an experiment

```python
import runner                      # 04_experiments/harness on sys.path

def fn(config):                    # config = the resolved dict
    ...
    return {"accuracy": 0.81, "f1_macro": 0.79, "loss": 0.41}   # scalars only

result = runner.run(config, "main", fn, notes="baseline, seed 0")
result.run_id        # 20261103T014500Z_baseline_a1b2c3d
result.run_dir       # 04_experiments/runs/<run_id>/
result.results_path  # .../results.json
```

`config` may be a dict or a path to a JSON file (`name` field or file stem
names the config; `seed` defaults to 0; `device` defaults to `cpu`). The
resolved config is hashed (sha256 of canonical JSON: sorted keys, no
whitespace) and copied verbatim to `config.json`.

CLI:

```bash
python 04_experiments/harness/runner.py --experiment toy \
    --config 04_experiments/harness/configs/toy_baseline.json

# CI-style rerun check: N runs of the same config, every metric compared
python 04_experiments/harness/runner.py --experiment toy \
    --config 04_experiments/harness/configs/toy_baseline.json --check-repro 3
```

Exit codes: `0` ok, `1` drift in `--check-repro` (or run failed), `2` usage.
`--json` prints the machine-readable result/report.

### Run folder

`runs/<run_id>/{meta.json, config.json, stdout.log, stderr.log, results.json, artifacts/}`

`meta.json` carries `run_id, config_name, config_sha256, git_commit, git_dirty,
python, platform, command, started_at, finished_at, duration_s, peak_rss_mb,
device, cpu_count, seed, host, env, notes` plus `experiment`, `status`
(`ok`/`error`), `schema` and `toy` when set. `peak_rss_mb` is sampled from a
daemon thread over this process + children via psutil; without psutil it is
`null` (documented no-op, never a fake number). `env` records
`PYTHONHASHSEED`, `PYTHONUTF8`, `PYTHONIOENCODING`, thread-count variables,
`CUDA_VISIBLE_DEVICES` and `RESEARCH_LAB_ROOT` when set.

`results.json` is `{"_meta": {...}, <flat scalar metrics>}`; nested dicts are
allowed one level, leaves must be `int/float/str/bool/null`.

A failing experiment still gets `meta.json` (`status: "error"`, `error:
"ExcType: message"`), `stdout.log` and the traceback in `stderr.log`; then the
exception is re-raised and no `results.json` is written (so aggregates never
pick up a half-finished run).

### Determinism

`run` calls `set_seeds(seed)` *before* `fn`: `random.seed`, `numpy.random.seed`
(when numpy is importable) and `PYTHONHASHSEED=0` in the environment for child
processes. The running interpreter's hash seed cannot change, so launch with
`PYTHONHASHSEED=0 python ...` if the experiment depends on string hashing; the
observed value is always recorded in `meta.json:env`.

`--check-repro N` runs the config N times (first run = baseline), compares every
leaf metric and `_meta.seed` with relative tolerance `--tol` (default `1e-6`,
absolute floor `1e-12`), prints a table and exits 1 on any drift -- including a
metric that appears/disappears between runs.

Same-second runs of the same config would collide in `run_id`, so the second and
later get a `-2`, `-3` suffix (the seed in `meta.json` is the authoritative
identity). No run is ever overwritten.

## Heavy-compute lock (`ops/HEAVY.lock`)

```python
import lock
with lock.acquire("train-main", timeout=0):     # timeout=0 => fail fast
    train()
```

* Atomic `O_CREAT|O_EXCL` creation; two racing processes cannot both win.
* A **live** lock raises `LockError` naming `name/pid/host/age`; with
  `timeout>0` it polls until the deadline (cap `MAX_WAIT_S` = 1 h).
* **Stale** = older than 4 h (`HEAVY_LOCK_STALE_S` overrides) or holder pid dead
  on this host. Reclaiming prints a warning, happens under an `O_EXCL` guard
  file, and re-checks the lock inside the guard, so two processes cannot both
  reclaim.
* Released on exception (`finally`), and only if the file still carries our
  token -- a reclaimed lock is never deleted by its previous owner.
* CLI: `lock.py status` (exit 0 free, 1 held), `lock.py acquire --name X
  [--timeout S] [--pid P]`, `lock.py release [--force]`, `--json` on any.

The CLI records the invoking shell's pid as holder (the CLI exits immediately,
the shell lives for the job); `--pid` overrides. If that shell dies, the next
`acquire` sees a dead pid and reclaims.

## Aggregating

```bash
python 04_experiments/harness/aggregate.py --experiment main --metric accuracy
python 04_experiments/harness/aggregate.py --experiment main --config baseline --config ours
```

Reads every `runs/*/results.json` whose `meta.json:experiment` matches, groups
the chosen metric by config, keeps the newest run per (config, seed) (dropped
duplicates are listed on stderr), and writes
`04_experiments/results/summary_<experiment>.json` in CONTRACTS section 4 shape:
`experiment, configs, metric, n_seeds, seeds, per_run, stats, paired, tables`
(+ `generated_at`, `n_runs`, `run_ids`, `toy` when applicable).

* mean/std are computed here (sample SD, ddof=1); `n` is the number of runs;
* inference comes from `stats.py` through `apply_stats(summary, metric,
  stats_module=None, root=None)`: `enrich_summary(summary[, metric])` if that
  exists, otherwise the primitive API (`summarise`, `bootstrap_ci` with
  `n_boot=10000`/`ci_seed=12345`, `paired_test`, `effect_size`, `holm`;
  baseline = first config, family size = comparisons). Without `stats.py` the
  summary stays valid: `ci95: null`, `ci_method: "none"`, `paired: null`, and a
  warning is printed; `--require-stats` turns that into exit 2.
* index entries are refreshed (not duplicated) per `(experiment, metric)`,
  other entries preserved, written via temp file + `os.replace`; each entry
  points at `stats.<config>.mean` in the summary file. `--no-index` skips it.

`tables` stays `[]`; table generation belongs to `tables.py`.

## Tests

```bash
python -m pytest 04_experiments/harness/tests/test_runner.py -q
```

Covers run-folder contents, real git hash / duration / peak RSS, config-hash
stability, RNG seeding, `--check-repro` pass/fail/exit codes, lock refusal,
release-on-exception, stale reclaim (dead pid and age), aggregate shape,
index idempotency and the stats hook. Everything writes to `tmp_path`; the real
`runs/` and `RESULTS-INDEX.json` are never touched by tests.
