#!/usr/bin/env python
"""Aggregate ``04_experiments/runs/*/results.json`` into a contract summary.

Reads every run of one experiment (optionally filtered by config), groups the
chosen metric by config, and writes:

* ``04_experiments/results/summary_<experiment>.json`` -- CONTRACTS section 4
  shape: ``experiment, configs, metric, n_seeds, seeds, per_run, stats, paired,
  tables``;
* the matching entries in ``04_experiments/RESULTS-INDEX.json`` (CONTRACTS
  section 3), preserving entries owned by other experiments and writing
  atomically via temp file + ``os.replace``.

The aggregator computes ``mean``/``std`` (sample std, ddof=1) itself.  The
inferential fields (bootstrap ``ci95``, paired tests, effect sizes) belong to
``04_experiments/harness/stats.py`` (owned by another worker) and are injected
through the documented hook :func:`apply_stats`, which imports that module
lazily and raises a clear ``ImportError`` when it is missing.  With no
``stats.py`` the summary is still valid: ``ci95`` is null with
``ci_method: "none"`` and ``paired`` is null -- no numbers are invented.

CLI
---
    python 04_experiments/harness/aggregate.py --experiment toy
    python 04_experiments/harness/aggregate.py --experiment toy --metric accuracy \\
        --config toy_baseline --config toy_ours
    python 04_experiments/harness/aggregate.py --experiment toy --require-stats

Exit codes: 0 ok, 1 no runs found, 2 usage/config error or missing stats.py with
``--require-stats``.

Per (config, seed) duplicates: only the newest run is used (by ``started_at``,
then directory mtime); the dropped ones are listed on stderr so the choice is
auditable.
"""

from __future__ import annotations

import argparse
import importlib.util
import inspect
import json
import os
import re
import statistics
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, cast

DEFAULT_METRIC = "accuracy"
DEFAULT_TOLERANCE = 0.0005
PREFERRED_METRICS = ("accuracy", "f1_macro", "loss")


# --------------------------------------------------------------------------- #
# paths / io
# --------------------------------------------------------------------------- #
def repo_root() -> Path:
    env = os.environ.get("RESEARCH_LAB_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    here = Path(__file__).resolve().parent
    for cand in (here, *here.parents):
        if (cand / "RULES.md").is_file() or (cand / "04_experiments").is_dir():
            return cand
    return here.parents[1]


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def write_json_atomic(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(obj, fh, indent=2, sort_keys=True, ensure_ascii=False, default=str)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


# --------------------------------------------------------------------------- #
# collection
# --------------------------------------------------------------------------- #
@dataclass
class RunRecord:
    run_id: str
    path: Path
    config_name: str
    seed: Any
    started_at: str
    results: Dict[str, Any]
    meta: Dict[str, Any]

    @property
    def toy(self) -> bool:
        return bool(self.meta.get("toy") or self.results.get("_meta", {}).get("toy"))


def _read_json(path: Path) -> Optional[Dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def collect_runs(experiment: str, *, runs_root: Optional[Path] = None,
                 configs: Optional[Sequence[str]] = None,
                 quiet: bool = False) -> List[RunRecord]:
    """All usable runs of ``experiment``, newest-first per (config, seed)."""
    root = Path(runs_root) if runs_root else repo_root() / "04_experiments" / "runs"
    if not root.is_dir():
        return []
    wanted = set(configs or [])
    records: List[RunRecord] = []
    for run_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        results = _read_json(run_dir / "results.json")
        if results is None:
            continue  # failed runs have no results.json by design
        meta = _read_json(run_dir / "meta.json") or {}
        run_experiment = meta.get("experiment") or results.get("_meta", {}).get("experiment")
        if run_experiment != experiment:
            continue
        config_name = str(meta.get("config_name")
                          or results.get("_meta", {}).get("config_name")
                          or run_dir.name.split("_", 2)[-1])
        if wanted and config_name not in wanted:
            continue
        seed = results.get("_meta", {}).get("seed", meta.get("seed"))
        records.append(RunRecord(
            run_id=run_dir.name,
            path=run_dir,
            config_name=config_name,
            seed=seed,
            started_at=str(meta.get("started_at") or ""),
            results=results,
            meta=meta,
        ))
    if not quiet:
        missing = sorted(p.name for p in root.iterdir()
                         if p.is_dir() and not (p / "results.json").is_file())
        if missing:
            print(f"note: {len(missing)} run folder(s) without results.json skipped: "
                  f"{', '.join(missing[:5])}{' ...' if len(missing) > 5 else ''}",
                  file=sys.stderr)
    return records


def _dedupe_by_seed(records: Sequence[RunRecord]) -> Tuple[Dict[str, List[RunRecord]], List[str]]:
    """config -> runs sorted by seed, keeping only the newest run per seed."""
    grouped: Dict[str, List[RunRecord]] = {}
    dropped: List[str] = []
    for record in records:
        grouped.setdefault(record.config_name, []).append(record)
    chosen: Dict[str, List[RunRecord]] = {}
    for config_name, runs in grouped.items():
        best: Dict[str, RunRecord] = {}
        for run in runs:
            key = json.dumps(run.seed, sort_keys=True, default=str)
            current = best.get(key)
            if current is None:
                best[key] = run
                continue
            newer = (run.started_at, run.path.stat().st_mtime) > (
                current.started_at, current.path.stat().st_mtime)
            winner, loser = (run, current) if newer else (current, run)
            best[key] = winner
            dropped.append(f"{loser.run_id} (superseded by {winner.run_id})")
        chosen[config_name] = sorted(best.values(),
                                     key=lambda r: json.dumps(r.seed, default=str))
    return chosen, dropped


def metric_names(records: Sequence[RunRecord]) -> List[str]:
    names = set()
    for record in records:
        names.update(k for k in record.results if k != "_meta")
    return sorted(names)


def pick_metric(records: Sequence[RunRecord], metric: Optional[str]) -> str:
    available = metric_names(records)
    if metric:
        if metric not in available:
            raise ValueError(f"metric {metric!r} not present in any run; "
                             f"available: {', '.join(available) or '<none>'}")
        return metric
    for candidate in PREFERRED_METRICS:
        if candidate in available:
            return candidate
    if not available:
        raise ValueError("no scalar metrics found in the selected runs")
    return available[0]


# --------------------------------------------------------------------------- #
# stats hook
# --------------------------------------------------------------------------- #
def stats_module_path(root: Optional[Path] = None) -> Path:
    base = Path(root) if root else repo_root()
    return base / "04_experiments" / "harness" / "stats.py"


def load_stats_module(root: Optional[Path] = None) -> Any:
    """Import ``harness/stats.py`` lazily (it is owned by another worker)."""
    path = stats_module_path(root)
    if not path.is_file():
        raise ImportError(
            f"{path} is not present. It supplies bootstrap CIs / paired tests / "
            f"effect sizes for the summary; without it aggregate.py writes "
            f"mean+std only (ci95 and paired stay null). Implement "
            f"``enrich_summary(summary)`` or ``summarize(per_run)`` in that module.")
    spec = importlib.util.spec_from_file_location("_lab_stats", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load stats module at {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _call_adaptive(fn: Callable[..., Any], summary: Dict[str, Any], metric: str) -> Any:
    """Call a hook that may take (summary), (summary, metric) or no args."""
    try:
        params = [p for p in inspect.signature(fn).parameters.values()
                  if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)]
    except (TypeError, ValueError):
        return fn(summary)
    if len(params) >= 2:
        return fn(summary, metric)
    if len(params) == 1:
        return fn(summary)
    return fn()


#: Contract-mandated defaults for every bootstrap CI (CONTRACTS section 4).
DEFAULT_N_BOOT = 10000
DEFAULT_CI_SEED = 12345
DEFAULT_CI_ALPHA = 0.05
DEFAULT_EFFECT = "cohens_d"


def _compose_stats(module: Any, summary: Dict[str, Any]) -> Dict[str, Any]:
    """Fill CIs and the paired block from stats.py primitives.

    Uses ``summarise(values)`` (mean/SD/median/min/max/note), ``bootstrap_ci``,
    ``paired_test``, ``effect_size`` and ``holm`` when the module provides them.
    Mean/std/n stay as computed here so the summary is reproducible even if
    stats.py changes its summariser.
    """
    per_run: Dict[str, List[float]] = summary["per_run"]
    stats_out: Dict[str, Dict[str, Any]] = {}
    ci_fn = getattr(module, "bootstrap_ci", None)
    summarise_fn = None
    for name in ("summarise", "summarize"):
        summarise_fn = getattr(module, name, None)
        if callable(summarise_fn):
            break

    for config_name, values in per_run.items():
        entry = dict(summary["stats"].get(config_name, {}))
        entry.setdefault("n", len(values))
        if callable(summarise_fn):
            try:
                extra = summarise_fn(values)
            except Exception as exc:  # pragma: no cover - defensive
                print(f"warning: stats summariser failed for {config_name!r}: {exc}",
                      file=sys.stderr)
            else:
                if isinstance(extra, dict):
                    for key, value in extra.items():
                        if key in ("mean", "std", "n"):
                            continue
                        if value is None or isinstance(value, (int, float, str, bool)):
                            entry[key] = value
                        elif isinstance(value, (list, tuple)) and all(
                                isinstance(v, (int, float)) for v in value):
                            entry[key] = list(value)
        if callable(ci_fn) and len(values) >= 2:
            last_error: Optional[Exception] = None
            for variant in ("bca", "percentile"):
                try:
                    ci = cast(Dict[str, Any], ci_fn(values, n_boot=DEFAULT_N_BOOT,
                                                    alpha=DEFAULT_CI_ALPHA,
                                                    seed=DEFAULT_CI_SEED, method=variant))
                except Exception as exc:  # small n / zero variance
                    last_error = exc
                    continue
                entry["ci95"] = [round(float(ci["lo"]), 10), round(float(ci["hi"]), 10)]
                entry["ci_method"] = "bootstrap"
                entry["ci_variant"] = variant
                entry["n_boot"] = int(ci.get("n_boot", DEFAULT_N_BOOT))
                entry["ci_seed"] = int(ci.get("seed", DEFAULT_CI_SEED))
                entry["ci_alpha"] = float(ci.get("alpha", DEFAULT_CI_ALPHA))
                break
            else:
                entry["ci95"] = None
                entry["ci_method"] = "none"
                entry["ci_note"] = f"bootstrap unavailable: {last_error}"
        elif len(values) < 2:
            entry["ci_note"] = "n < 2: no interval can be estimated"
        stats_out[config_name] = entry
    summary["stats"] = stats_out

    paired_fn = getattr(module, "paired_test", None)
    effect_fn = getattr(module, "effect_size", None)
    holm_fn = getattr(module, "holm", None)
    configs = summary["configs"]
    if callable(paired_fn) and len(configs) >= 2:
        baseline = configs[0]
        family = len(configs) - 1
        comparisons: List[Dict[str, Any]] = []
        for other in configs[1:]:
            a, b = per_run.get(baseline, []), per_run.get(other, [])
            if len(a) != len(b) or not a:
                continue
            try:
                test = cast(Dict[str, Any], paired_fn(a, b, correction="holm",
                                                      family_size=family))
            except Exception as exc:  # pragma: no cover - defensive
                print(f"warning: paired test failed for {baseline} vs {other}: {exc}",
                      file=sys.stderr)
                continue
            block: Dict[str, Any] = {
                "baseline": baseline,
                "treatment": other,
                "test": test.get("test"),
                "p_value": test.get("p_value"),
                "n_pairs": test.get("n_pairs", len(a)),
                "n_eff": test.get("n_eff"),
                "notes": test.get("notes"),
                "correction": {
                    "method": "holm",
                    "family_size": family,
                    "p_adjusted": None,
                    "note": f"{family} comparison(s) in this family",
                },
            }
            if callable(effect_fn):
                try:
                    raw_effect = cast(Dict[str, Any], effect_fn(a, b, kind=DEFAULT_EFFECT))
                except Exception as exc:  # zero pooled SD / n < 2
                    block["effect_size"] = {"name": DEFAULT_EFFECT, "value": None,
                                            "note": f"undefined: {exc}"}
                else:
                    if isinstance(raw_effect, dict):
                        block["effect_size"] = {
                            "name": raw_effect.get("name", DEFAULT_EFFECT),
                            "value": raw_effect.get("value"),
                            "interpretation": raw_effect.get("interpretation"),
                        }
            comparisons.append(block)

        p_values = [c["p_value"] for c in comparisons if isinstance(c["p_value"], (int, float))]
        if p_values and callable(holm_fn):
            try:
                adjusted = cast(Dict[str, Any], holm_fn(p_values)).get("p_adjusted", [])
            except Exception as exc:  # pragma: no cover - defensive
                print(f"warning: holm correction failed: {exc}", file=sys.stderr)
                adjusted = []
            index = 0
            for block in comparisons:
                if isinstance(block["p_value"], (int, float)):
                    if index < len(adjusted):
                        block["correction"]["p_adjusted"] = float(adjusted[index])
                    index += 1
        if comparisons:
            summary["paired"] = comparisons[0]
            summary["paired_all"] = comparisons
    return summary


def apply_stats(summary: Dict[str, Any], metric: str, stats_module: Any = None, *,
                root: Optional[Path] = None) -> Dict[str, Any]:
    """Hook: let ``stats.py`` fill ``stats[*].ci95`` and ``paired``.

    Accepted APIs, tried in order:
      * ``enrich_summary(summary[, metric]) -> dict | None`` -- may mutate and/or
        return ``{"stats": ..., "paired": ..., "tables": ...}`` to merge.
      * the primitive API of ``harness/stats.py``: ``summarise``/``summarize``,
        ``bootstrap_ci``, ``paired_test``, ``effect_size``, ``holm`` -- combined
        here per config (CI: bootstrap, n_boot=10000, ci_seed=12345) and once for
        the paired block (baseline = first config, Holm-corrected family).
    Raises ``ImportError`` when the module is absent or exposes neither.
    """
    module = stats_module if stats_module is not None else load_stats_module(root)
    if hasattr(module, "enrich_summary"):
        result = _call_adaptive(module.enrich_summary, summary, metric)
        if isinstance(result, dict):
            for key in ("stats", "paired", "tables"):
                if key in result:
                    summary[key] = result[key]
        return summary
    primitive_names = ("summarise", "summarize", "bootstrap_ci", "paired_test")
    if any(hasattr(module, name) for name in primitive_names):
        return _compose_stats(module, summary)
    raise ImportError(
        f"{getattr(module, '__file__', module)} exposes none of enrich_summary, "
        f"summarise, bootstrap_ci, paired_test; cannot apply statistics.")


# --------------------------------------------------------------------------- #
# summary
# --------------------------------------------------------------------------- #
def build_summary(experiment: str, records: Sequence[RunRecord], metric: str) -> Dict[str, Any]:
    chosen, dropped = _dedupe_by_seed(records)
    for note in dropped:
        print(f"note: duplicate seed run ignored: {note}", file=sys.stderr)

    per_run: Dict[str, List[float]] = {}
    stats_block: Dict[str, Dict[str, Any]] = {}
    seed_map: Dict[str, List[Any]] = {}
    latest_run: Dict[str, str] = {}
    seed_sets = set()

    for config_name in sorted(chosen):
        runs = chosen[config_name]
        values: List[float] = []
        seeds: List[Any] = []
        for run_rec in runs:
            value = run_rec.results.get(metric)
            if isinstance(value, dict) or value is None or isinstance(value, str) \
                    or isinstance(value, bool):
                print(f"warning: run {run_rec.run_id} has no numeric {metric!r}; skipped",
                      file=sys.stderr)
                continue
            values.append(float(value))
            seeds.append(run_rec.seed)
        if not values:
            print(f"warning: config {config_name!r} contributes no values for {metric!r}; "
                  f"dropped from summary", file=sys.stderr)
            continue
        per_run[config_name] = values
        seed_map[config_name] = seeds
        seed_sets.add(tuple(json.dumps(s, sort_keys=True, default=str) for s in seeds))
        stats_block[config_name] = {
            "mean": round(statistics.fmean(values), 10),
            "std": round(statistics.stdev(values), 10) if len(values) > 1 else 0.0,
            "ci95": None,
            "n": len(values),
            "ci_method": "none",
        }
        latest_run[config_name] = max(runs, key=lambda r: (r.started_at,
                                                           r.path.stat().st_mtime)).run_id

    if len(seed_sets) > 1:
        raise ValueError(
            "configs do not share the same seed set: "
            + "; ".join(f"{c}={seed_map[c]}" for c in sorted(seed_map))
            + ". A paired summary needs aligned seeds -- rerun the missing seeds.")

    seeds_out: List[Any] = []
    if per_run:
        seeds_out = seed_map[next(iter(per_run))]

    toy = any(r.toy for r in records)
    summary: Dict[str, Any] = {
        "experiment": experiment,
        "configs": sorted(per_run),
        "metric": metric,
        "n_seeds": len(seeds_out),
        "seeds": seeds_out,
        "per_run": per_run,
        "stats": stats_block,
        "paired": None,
        "tables": [],
        "generated_at": utcnow_iso(),
        "n_runs": sum(len(v) for v in per_run.values()),
        "run_ids": latest_run,
    }
    if toy:
        summary["toy"] = True
    return summary


def summary_path(experiment: str, root: Optional[Path] = None,
                 out_dir: Optional[Path] = None) -> Path:
    base = Path(out_dir) if out_dir else (Path(root) if root else repo_root()) / "04_experiments" / "results"
    return base / f"summary_{experiment}.json"


def index_path(root: Optional[Path] = None) -> Path:
    return (Path(root) if root else repo_root()) / "04_experiments" / "RESULTS-INDEX.json"


def update_index(summary: Dict[str, Any], summary_file: Path, *, root: Optional[Path] = None,
                 tolerance: float = DEFAULT_TOLERANCE, dry_run: bool = False) -> Dict[str, Any]:
    """Refresh this (experiment, metric)'s entries; preserve everybody else's."""
    base = Path(root) if root else repo_root()
    path = index_path(base)
    data = _read_json(path) or {}
    if not data:
        data = {"version": 1, "updated_at": utcnow_iso(), "entries": []}
    entries = data.get("entries")
    if not isinstance(entries, list):
        raise ValueError(f"{path} has no 'entries' list; refusing to overwrite a malformed index")
    data.setdefault("version", 1)

    experiment = summary["experiment"]
    metric = summary["metric"]
    owned_prefix = f"{experiment}.{metric}."
    try:
        rel_file = str(summary_file.resolve().relative_to(base.resolve())).replace(os.sep, "/")
    except ValueError:
        rel_file = str(summary_file)

    kept = [e for e in entries if not str(e.get("id", "")).startswith(owned_prefix)]
    new_entries: List[Dict[str, Any]] = []
    for config_name in summary["configs"]:
        stats = summary["stats"].get(config_name, {})
        entry: Dict[str, Any] = {
            "id": f"{experiment}.{metric}.{config_name}",
            "file": rel_file,
            "key": f"stats.{config_name}.mean",
            "description": (f"{metric} for config '{config_name}' of experiment "
                            f"'{experiment}': mean over {stats.get('n')} run(s)"
                            + (f", seeds {summary.get('seeds')}" if summary.get("seeds") else "")),
            "run_id": summary.get("run_ids", {}).get(config_name, ""),
            "tolerance": float(tolerance),
        }
        if summary.get("toy"):
            entry["toy"] = True
            entry["description"] += " [TOY - NOT A RESULT]"
        new_entries.append(entry)

    data["entries"] = kept + new_entries
    data["updated_at"] = utcnow_iso()
    if not dry_run:
        write_json_atomic(path, data)
    return data


# --------------------------------------------------------------------------- #
# orchestration
# --------------------------------------------------------------------------- #
def aggregate(experiment: str, *, configs: Optional[Sequence[str]] = None,
              metric: Optional[str] = None, runs_root: Optional[Path] = None,
              root: Optional[Path] = None, out_dir: Optional[Path] = None,
              tolerance: float = DEFAULT_TOLERANCE, require_stats: bool = False,
              write_index: bool = True, quiet: bool = False) -> Dict[str, Any]:
    records = collect_runs(experiment, runs_root=runs_root, configs=configs)
    if not records:
        raise LookupError(f"no runs found for experiment {experiment!r} "
                          f"under {runs_root or repo_root() / '04_experiments' / 'runs'}")
    chosen_metric = pick_metric(records, metric)
    summary = build_summary(experiment, records, chosen_metric)

    try:
        apply_stats(summary, chosen_metric, root=root)
    except ImportError as exc:
        if require_stats:
            raise
        if not quiet:
            print(f"warning: statistics not applied ({exc})", file=sys.stderr)
            print("warning: summary carries mean/std only; ci95 and paired are null.",
                  file=sys.stderr)

    target = summary_path(experiment, root=root, out_dir=out_dir)
    write_json_atomic(target, summary)
    if write_index:
        update_index(summary, target, root=root, tolerance=tolerance)
    if not quiet:
        print_summary(summary, target)
    return summary


def print_summary(summary: Dict[str, Any], path: Path) -> None:
    print(f"experiment={summary['experiment']} metric={summary['metric']} "
          f"n_seeds={summary['n_seeds']} seeds={summary['seeds']}")
    header = f"{'config':<24} {'n':>3} {'mean':>12} {'std':>12} {'ci95':>22}"
    print(header)
    print("-" * len(header))
    for config_name in summary["configs"]:
        stats = summary["stats"].get(config_name, {})
        ci = stats.get("ci95")
        ci_txt = "null" if not ci else f"[{ci[0]:.6g}, {ci[1]:.6g}]"
        print(f"{config_name:<24} {stats.get('n', 0):>3} {stats.get('mean', 0):>12.6g} "
              f"{stats.get('std', 0):>12.6g} {ci_txt:>22}")
    print(f"summary: {path}")
    if summary.get("toy"):
        print("NOTE: toy experiment -- TOY - NOT A RESULT, never citable.")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="aggregate.py",
        description="Aggregate runs into 04_experiments/results/summary_<experiment>.json")
    parser.add_argument("--experiment", required=True)
    parser.add_argument("--config", action="append", default=None,
                        help="restrict to config name(s); repeatable")
    parser.add_argument("--metric", default=None,
                        help=f"metric to summarise (default: {DEFAULT_METRIC} if present)")
    parser.add_argument("--runs-root", default=None)
    parser.add_argument("--out-dir", default=None)
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--tolerance", type=float, default=DEFAULT_TOLERANCE,
                        help="tolerance written into RESULTS-INDEX entries")
    parser.add_argument("--require-stats", action="store_true",
                        help="fail (exit 2) instead of warning when harness/stats.py is absent")
    parser.add_argument("--no-index", action="store_true", help="do not touch RESULTS-INDEX.json")
    parser.add_argument("--json", action="store_true", help="print the summary to stdout")
    args = parser.parse_args(argv)

    root = Path(args.repo_root).resolve() if args.repo_root else None
    try:
        summary = aggregate(
            args.experiment,
            configs=args.config,
            metric=args.metric,
            runs_root=Path(args.runs_root) if args.runs_root else None,
            root=root,
            out_dir=Path(args.out_dir) if args.out_dir else None,
            tolerance=args.tolerance,
            require_stats=args.require_stats,
            write_index=not args.no_index,
            quiet=args.json,
        )
    except LookupError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except (ValueError, ImportError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
