#!/usr/bin/env python
"""TOY - NOT A RESULT

End-to-end smoke test of the experiment harness: 3 seeds x 2 configs of the
synthetic toy task in ``toy/task.py``, each through ``harness/runner.run`` (run
folder + provenance + config copy + logs + results.json), then through
``harness/aggregate.py`` (summary_toy.json + RESULTS-INDEX entries).

    python 04_experiments/toy/run_toy.py            # ~1 s
    python 04_experiments/toy/run_toy.py --seeds 0 1 2 --no-aggregate

Every JSON written here carries ``"toy": true`` and every number is synthetic.
Nothing in this folder may be cited in a draft (RULES #2, CONTRACTS section 5).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
HARNESS = EXPERIMENTS / "harness"
for _path in (str(HARNESS), str(HERE)):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import aggregate  # noqa: E402
import runner  # noqa: E402
import task  # noqa: E402

BANNER = "TOY - NOT A RESULT"
CONFIG_FILES = ("toy_baseline.json", "toy_ours.json")
SEEDS = (0, 1, 2)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="run_toy.py", description=BANNER)
    parser.add_argument("--seeds", nargs="+", type=int, default=list(SEEDS))
    parser.add_argument("--configs", nargs="+", default=list(CONFIG_FILES),
                        help="config file names inside 04_experiments/harness/configs/")
    parser.add_argument("--no-aggregate", action="store_true",
                        help="skip the aggregate step (no summary/index update)")
    args = parser.parse_args(argv)

    started = time.perf_counter()
    print(BANNER)
    print(f"running {len(args.configs)} config(s) x {len(args.seeds)} seed(s) "
          f"through the harness\n")

    records = []
    config_names = []
    for config_file in args.configs:
        config_path = HARNESS / "configs" / config_file
        if not config_path.is_file():
            print(f"error: missing config {config_path}", file=sys.stderr)
            return 2
        base = json.loads(config_path.read_text(encoding="utf-8"))
        config_names.append(str(base.get("name") or Path(config_file).stem))
        for seed in args.seeds:
            config = dict(base, seed=int(seed))
            result = runner.run(config, "toy", task.run_task,
                                notes=f"{BANNER}; synthetic blobs; seed {seed}")
            metrics = result.metrics()
            records.append({
                "config_name": result.meta["config_name"],
                "seed": int(seed),
                "run_id": result.run_id,
                "results": str(result.results_path.relative_to(runner.repo_root()))
                           .replace("\\", "/"),
                "accuracy": metrics.get("accuracy"),
                "f1_macro": metrics.get("f1_macro"),
                "loss": metrics.get("loss"),
            })

    out_path = HERE / "toy_runs.json"
    payload = {
        "toy": True,
        "banner": BANNER,
        "experiment": "toy",
        "generated_at": runner.iso(runner.utcnow()),
        "seeds": [int(s) for s in args.seeds],
        "configs": config_names,
        "n_runs": len(records),
        "runs": records,
    }
    runner.write_json(out_path, payload)
    print(f"\nwrote {out_path} ({len(records)} runs)")

    if not args.no_aggregate:
        summary = aggregate.aggregate("toy", metric="accuracy")
        if not summary.get("toy"):
            print("error: aggregate() dropped the toy flag; refusing to continue",
                  file=sys.stderr)
            return 1
        print(f"wrote {aggregate.summary_path('toy')}")

    elapsed = time.perf_counter() - started
    print(f"\n{BANNER}: {len(records)} harness runs in {elapsed:.2f}s "
          f"(budget 5.00s)")
    if elapsed > 5.0:
        print("warning: toy run exceeded the 5 s budget", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
