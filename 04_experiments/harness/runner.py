#!/usr/bin/env python
"""Reproducible experiment runner for the research lab.

Every experiment goes through :func:`run`, which materialises a self-describing
run folder under ``04_experiments/runs/<run_id>/`` with full provenance
(git hash + dirty flag, python, platform, command line, timings, peak RSS,
cpu count, seed, host, selected environment variables), an exact copy of the
resolved config, captured stdout/stderr, and a flat ``results.json``.

Contract: ``tools/CONTRACTS.md`` section 2 (run folders) and section 3
(``RESULTS-INDEX.json``, written by ``aggregate.py``).

Public API
----------
``run(config, experiment, fn, notes='') -> RunResult``
    ``config``   : dict, or path to a JSON config file (``name`` field or the
                   file stem names the config).
    ``experiment``: short experiment name, also the meta.json key that
                   ``aggregate.py`` groups on.
    ``fn``       : callable ``fn(resolved_config) -> dict`` of scalar metrics
                   (nested dicts allowed one level deep).
    ``notes``    : free text stored in meta.json.

``set_seeds(seed)``
    Seeds ``random`` and (when numpy is importable) ``numpy.random`` and sets
    ``PYTHONHASHSEED=0`` in ``os.environ`` so child processes inherit a fixed
    hash seed.  The current interpreter's hash seed cannot be changed at
    runtime, so a run started from a shell with a different PYTHONHASHSEED
    should be launched as ``PYTHONHASHSEED=0 python ...`` -- ``run`` records
    the observed value in ``meta.json:env`` either way.

Determinism notes
-----------------
``run`` calls :func:`set_seeds` *before* invoking ``fn``.  It does not try to
control thread counts / GPU nondeterminism; record those in the config.

CLI
---
    python 04_experiments/harness/runner.py --experiment toy \\
        --config 04_experiments/harness/configs/toy_baseline.json

    # CI-style rerun check: run the same config N times, compare all metrics
    python 04_experiments/harness/runner.py --experiment toy \\
        --config 04_experiments/harness/configs/toy_baseline.json --check-repro 3

Exit codes: 0 success / reproduction OK, 1 drift (check-repro) or run failed,
2 usage error.

``--check-repro`` writes real run folders (they are legitimate runs with
provenance); the first run is the baseline, runs 2..N are compared against it
on every leaf metric with a relative tolerance (default 1e-6).
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import json
import os
import platform
import random
import re
import socket
import subprocess
import sys
import threading
import time
import traceback
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

SCHEMA = "run/1"
DEFAULT_TOLERANCE = 1e-6
DEFAULT_SEED = 0

#: Environment variables captured into ``meta.json:env`` when set.
ENV_KEYS = (
    "PYTHONHASHSEED",
    "PYTHONUTF8",
    "PYTHONIOENCODING",
    "OMP_NUM_THREADS",
    "MKL_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "CUDA_VISIBLE_DEVICES",
    "RESEARCH_LAB_ROOT",
)

_SCALARS = (str, int, float, bool)


# --------------------------------------------------------------------------- #
# paths
# --------------------------------------------------------------------------- #
def repo_root() -> Path:
    """Repo root: ``$RESEARCH_LAB_ROOT`` if set, else the nearest ancestor
    containing ``RULES.md`` / ``04_experiments``."""
    env = os.environ.get("RESEARCH_LAB_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    here = Path(__file__).resolve().parent
    for cand in (here, *here.parents):
        if (cand / "RULES.md").is_file() or (cand / "04_experiments").is_dir():
            return cand
    return here.parents[1]


def runs_dir(root: Optional[Path] = None) -> Path:
    return Path(root) if root else repo_root() / "04_experiments" / "runs"


# --------------------------------------------------------------------------- #
# time / json helpers
# --------------------------------------------------------------------------- #
def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    """ISO-8601 UTC with a ``Z`` suffix, second resolution."""
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _json_default(obj: Any) -> Any:
    if isinstance(obj, Path):
        return str(obj)
    raise TypeError(f"not JSON serialisable: {type(obj).__name__}")


def canonical_json(obj: Any) -> str:
    """Stable serialisation used for hashing (sorted keys, no whitespace)."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      default=_json_default)


def sha256_canonical(obj: Any) -> str:
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, indent=2, sort_keys=True, ensure_ascii=False, default=_json_default)
        fh.write("\n")
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


# --------------------------------------------------------------------------- #
# git / environment
# --------------------------------------------------------------------------- #
def _git(args: Sequence[str], cwd: Path, timeout: float = 10.0) -> Optional[str]:
    try:
        proc = subprocess.run(["git", *args], cwd=str(cwd), capture_output=True,
                              text=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout


def git_commit(root: Optional[Path] = None) -> str:
    """``git rev-parse --short HEAD``; ``"unknown"`` outside a git repo."""
    out = _git(["rev-parse", "--short", "HEAD"], Path(root) if root else repo_root())
    return out.strip() if out else "unknown"


def git_dirty(root: Optional[Path] = None) -> Optional[bool]:
    """True when ``git status --porcelain`` is non-empty; None if git failed."""
    out = _git(["status", "--porcelain"], Path(root) if root else repo_root())
    return None if out is None else bool(out.strip())


def git_diff(root: Optional[Path] = None) -> str:
    """Capture a textual snapshot of the working-tree state.

    Combines ``git diff HEAD`` (tracked changes vs. HEAD), ``git diff --cached``
    (staged changes) and the list of untracked files.  Returns text even when git
    is unavailable.
    """
    root_path = Path(root) if root else repo_root()
    parts: List[str] = []
    head_diff = _git(["diff", "HEAD"], root_path)
    parts.append("===== git diff HEAD =====")
    parts.append(head_diff.rstrip(chr(10)) if head_diff is not None else "")
    cached_diff = _git(["diff", "--cached"], root_path)
    parts.append("===== git diff --cached =====")
    parts.append(cached_diff.rstrip(chr(10)) if cached_diff is not None else "")
    untracked_out = _git(["ls-files", "--others", "--exclude-standard"], root_path)
    untracked_files = [line for line in (untracked_out or "").splitlines() if line.strip()]
    parts.append("===== untracked files =====")
    parts.append(chr(10).join(untracked_files))
    return chr(10).join(parts).rstrip(chr(10)) + chr(10)


def git_preregistration_sha256(root: Optional[Path] = None) -> Optional[str]:
    """SHA-256 of ``04_experiments/PREREGISTRATION.md`` (None if absent)."""
    root_path = Path(root) if root else repo_root()
    path = root_path / "04_experiments" / "PREREGISTRATION.md"
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def capture_env() -> Dict[str, str]:
    return {k: os.environ[k] for k in ENV_KEYS if os.environ.get(k) is not None}


def command_line() -> str:
    return " ".join([Path(sys.executable).name, *sys.argv])


# --------------------------------------------------------------------------- #
# determinism
# --------------------------------------------------------------------------- #
def set_seeds(seed: int) -> int:
    """Seed every RNG this lab uses and pin PYTHONHASHSEED for child processes.

    Returns the seed so callers can log it.  numpy is optional.
    """
    seed = int(seed)
    os.environ["PYTHONHASHSEED"] = "0"
    random.seed(seed)
    try:  # numpy is optional; absence is not an error
        import numpy as np  # type: ignore
    except Exception:
        pass
    else:
        np.random.seed(seed)
    return seed


# --------------------------------------------------------------------------- #
# peak RSS sampling
# --------------------------------------------------------------------------- #
class _PeakRSS:
    """Sample RSS of this process (plus children) from a daemon thread.

    psutil is optional.  Without it the sampler is a documented no-op and
    ``peak_rss_mb`` is written as null -- provenance is never faked.
    """

    def __init__(self, interval_s: float = 0.05) -> None:
        self.interval_s = interval_s
        self.peak_bytes = 0
        self.available = False
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        try:
            import psutil  # type: ignore
        except Exception:
            self._psutil = None
            return
        self._psutil = psutil
        try:
            self._proc = psutil.Process(os.getpid())
        except Exception:
            self._psutil = None
            return
        self.available = True

    def _sample(self) -> int:
        total = self._proc.memory_info().rss
        try:
            for child in self._proc.children(recursive=True):
                try:
                    total += child.memory_info().rss
                except Exception:
                    pass
        except Exception:
            pass
        return total

    def _loop(self) -> None:
        while not self._stop.wait(self.interval_s):
            try:
                self.peak_bytes = max(self.peak_bytes, self._sample())
            except Exception:
                return

    def start(self) -> None:
        if not self.available:
            return
        try:
            self.peak_bytes = self._sample()
        except Exception:
            pass
        self._thread = threading.Thread(target=self._loop, name="peak-rss", daemon=True)
        self._thread.start()

    def stop(self) -> Optional[float]:
        """Stop sampling and return peak RSS in MiB (None when unavailable)."""
        if not self.available:
            return None
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=2.0)
        try:
            self.peak_bytes = max(self.peak_bytes, self._sample())
        except Exception:
            pass
        return round(self.peak_bytes / (1024 * 1024), 3)


class _Tee:
    """Write to several streams (log file + the real console)."""

    def __init__(self, *streams: Any) -> None:
        self.streams = streams

    def write(self, data: str) -> int:
        for stream in self.streams:
            try:
                stream.write(data)
            except Exception:
                pass
        return len(data)

    def flush(self) -> None:
        for stream in self.streams:
            try:
                stream.flush()
            except Exception:
                pass

    def isatty(self) -> bool:
        return False

    @property
    def encoding(self) -> str:
        return "utf-8"


# --------------------------------------------------------------------------- #
# config
# --------------------------------------------------------------------------- #
def _resolve_path(path: Path, root: Path) -> Path:
    path = Path(path).expanduser()
    if path.is_file():
        return path.resolve()
    alt = (root / path).resolve()
    if alt.is_file():
        return alt
    raise FileNotFoundError(f"config file not found: {path} (also tried {alt})")


def load_config(config: Any, fallback_name: str = "config") -> Tuple[Dict[str, Any], str]:
    """Return ``(config_dict, config_name)`` from a dict or a JSON path."""
    if isinstance(config, dict):
        cfg = json.loads(json.dumps(config, default=_json_default))
        if not isinstance(cfg, dict):
            raise TypeError("config must be a JSON object / dict")
        name = str(cfg.get("name") or fallback_name)
        return cfg, name
    path = _resolve_path(Path(config), repo_root())
    with open(path, "r", encoding="utf-8") as fh:
        cfg = json.load(fh)
    if not isinstance(cfg, dict):
        raise TypeError(f"config file {path} must contain a JSON object")
    name = str(cfg.get("name") or path.stem)
    return cfg, name


def resolve_config(cfg: Dict[str, Any], name: str) -> Dict[str, Any]:
    """Fill documented defaults; the result is what gets hashed and written."""
    resolved = json.loads(json.dumps(cfg, default=_json_default))
    resolved["name"] = name
    resolved["seed"] = int(resolved.get("seed", DEFAULT_SEED))
    resolved.setdefault("device", "cpu")
    return resolved


def _slug(name: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-.")
    return slug or "config"


# --------------------------------------------------------------------------- #
# results validation
# --------------------------------------------------------------------------- #
def _leaf(value: Any, where: str) -> Any:
    if value is None or isinstance(value, _SCALARS):
        return value
    raise TypeError(f"metric {where} is not a scalar "
                    f"(int/float/str/bool/null): {type(value).__name__}")


def validate_metrics(metrics: Any) -> Dict[str, Any]:
    """Enforce CONTRACTS section 2: flat dict, one nesting level, scalar leaves."""
    if not isinstance(metrics, dict):
        raise TypeError(f"experiment fn must return a dict of metrics, got {type(metrics).__name__}")
    out: Dict[str, Any] = {}
    for key, value in metrics.items():
        if key == "_meta":
            raise ValueError("metrics must not define '_meta'; the runner owns it")
        if not isinstance(key, str):
            raise TypeError(f"metric names must be strings, got {key!r}")
        if isinstance(value, dict):
            if not value:
                out[key] = {}
                continue
            nested: Dict[str, Any] = {}
            for sub, sub_value in value.items():
                if isinstance(sub_value, dict):
                    raise ValueError(f"metric {key}.{sub} nests more than one level")
                nested[str(sub)] = _leaf(sub_value, f"{key}.{sub}")
            out[key] = nested
        else:
            out[key] = _leaf(value, key)
    return out


# --------------------------------------------------------------------------- #
# run result
# --------------------------------------------------------------------------- #
@dataclass
class RunResult:
    run_id: str
    run_dir: Path
    meta: Dict[str, Any]
    results: Dict[str, Any]

    @property
    def results_path(self) -> Path:
        return Path(self.run_dir) / "results.json"

    @property
    def meta_path(self) -> Path:
        return Path(self.run_dir) / "meta.json"

    def metrics(self) -> Dict[str, Any]:
        return {k: v for k, v in self.results.items() if k != "_meta"}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "run_dir": str(self.run_dir),
            "results_path": str(self.results_path),
            "meta": self.meta,
            "results": self.results,
        }


def _make_run_dir(parent: Path, slug: str, commit: str) -> Tuple[str, Path]:
    parent.mkdir(parents=True, exist_ok=True)
    stamp = utcnow().strftime("%Y%m%dT%H%M%SZ")
    base = f"{stamp}_{slug}_{commit}"
    run_id, suffix = base, 1
    while True:
        path = parent / run_id
        try:
            path.mkdir(parents=False, exist_ok=False)
            return run_id, path
        except FileExistsError:
            # Two runs of the same config inside the same UTC second: keep the
            # contract shape and disambiguate with a numeric suffix.  The seed
            # in meta.json remains the authoritative identity of the run.
            suffix += 1
            run_id = f"{base}-{suffix}"


# --------------------------------------------------------------------------- #
# the core entry point
# --------------------------------------------------------------------------- #
def run(config: Any, experiment: str, fn: Callable[[Dict[str, Any]], Dict[str, Any]],
        notes: str = "", *, runs_root: Optional[Path] = None,
        repo_root_path: Optional[Path] = None, command: Optional[str] = None,
        seed: Optional[int] = None, toy: Optional[bool] = None) -> RunResult:
    """Execute ``fn(resolved_config)`` and persist a fully-provenanced run.

    Raises whatever ``fn`` raises, after writing meta.json/stdout.log/stderr.log
    with ``status: "error"`` (no results.json is written for a failed run).
    """
    root = Path(repo_root_path).resolve() if repo_root_path else repo_root()
    parent = runs_dir(runs_root)
    cfg, name = load_config(config, fallback_name=experiment)
    resolved = resolve_config(cfg, name)
    if seed is not None:
        resolved["seed"] = int(seed)
    seed_value = int(resolved["seed"])
    is_toy = bool(resolved.get("toy", False)) if toy is None else bool(toy)

    config_text = json.dumps(resolved, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    config_sha = sha256_canonical(resolved)
    commit = git_commit(root)
    dirty = git_dirty(root)
    diff_text = git_diff(root)
    _untracked_out = _git(["ls-files", "--others", "--exclude-standard"], root)
    untracked_files = [line for line in (_untracked_out or "").splitlines() if line.strip()] if _untracked_out is not None else []
    prereg_path = root / "04_experiments" / "PREREGISTRATION.md"
    prereg_sha = git_preregistration_sha256(root)

    run_id, run_dir = _make_run_dir(parent, _slug(name), commit)
    (run_dir / "artifacts").mkdir(exist_ok=True)
    for _fname in ("git_diff.patch", "git_diff.txt", "git-diff.patch", "git-diff.txt"):
        for _target in (run_dir / "artifacts" / _fname, run_dir / _fname):
            with open(_target, "w", encoding="utf-8", newline="\n") as _fh:
                _fh.write(diff_text)
    with open(run_dir / "config.json", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(config_text)

    started = utcnow()
    started_perf = time.perf_counter()
    monitor = _PeakRSS()
    set_seeds(seed_value)

    metrics: Optional[Dict[str, Any]] = None
    error: Optional[BaseException] = None
    peak_mb: Optional[float] = None

    with open(run_dir / "stdout.log", "w", encoding="utf-8", newline="\n") as out_fh, \
            open(run_dir / "stderr.log", "w", encoding="utf-8", newline="\n") as err_fh:
        tee_out = _Tee(out_fh, sys.__stdout__ or sys.stdout)
        tee_err = _Tee(err_fh, sys.__stderr__ or sys.stderr)
        monitor.start()
        try:
            with contextlib.redirect_stdout(tee_out), contextlib.redirect_stderr(tee_err):
                try:
                    metrics = validate_metrics(fn(resolved))
                except BaseException as exc:  # noqa: BLE001 - recorded, then re-raised
                    error = exc
                    traceback.print_exc(file=tee_err)
        finally:
            peak_mb = monitor.stop()
        duration_s = round(time.perf_counter() - started_perf, 4)

    finished = utcnow()

    meta: Dict[str, Any] = {
        "run_id": run_id,
        "config_name": name,
        "config_sha256": config_sha,
        "git_commit": commit,
        "git_dirty": dirty,
        "git_diff": diff_text,
        "git_diff_sha256": hashlib.sha256(diff_text.encode("utf-8")).hexdigest(),
        "git_diff_path": str((run_dir / "artifacts" / "git_diff.patch").resolve()),
        "git_untracked": untracked_files,
        "preregistration_sha256": prereg_sha,
        "preregistration_path": str(prereg_path.resolve() if prereg_path.is_file() else prereg_path),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "command": command if command is not None else command_line(),
        "started_at": iso(started),
        "finished_at": iso(finished),
        "duration_s": duration_s,
        "peak_rss_mb": peak_mb,
        "device": str(resolved.get("device", "cpu")),
        "cpu_count": os.cpu_count(),
        "seed": seed_value,
        "host": socket.gethostname(),
        "env": capture_env(),
        "notes": notes,
        # extras beyond CONTRACTS section 2, needed by aggregate.py / audits:
        "experiment": experiment,
        "status": "error" if error is not None else "ok",
        "schema": SCHEMA,
    }
    if is_toy:
        meta["toy"] = True

    if error is not None:
        meta["error"] = f"{type(error).__name__}: {error}"
        write_json(run_dir / "meta.json", meta)
        raise error

    assert metrics is not None
    results_meta: Dict[str, Any] = {
        "run_id": run_id,
        "config_name": name,
        "seed": seed_value,
        "experiment": experiment,
        "split": resolved.get("split", "test"),
    }
    n_value = resolved.get("n")
    if not isinstance(n_value, (int, float, str, bool)) or n_value is None:
        n_value = metrics.get("n_test")
    if n_value is None:
        n_value = metrics.get("n")
    if isinstance(n_value, (int, float, str, bool)) and n_value is not None:
        results_meta["n"] = n_value
    if is_toy:
        results_meta["toy"] = True

    results: Dict[str, Any] = {"_meta": results_meta, **metrics}
    write_json(run_dir / "results.json", results)
    write_json(run_dir / "meta.json", meta)
    return RunResult(run_id=run_id, run_dir=run_dir, meta=meta, results=results)


# --------------------------------------------------------------------------- #
# reproducibility check
# --------------------------------------------------------------------------- #
@dataclass
class ReproRow:
    run_id: str
    metric: str
    baseline: Any
    observed: Any
    rel_diff: Optional[float]
    ok: bool


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def flatten_results(results: Dict[str, Any]) -> Dict[str, Any]:
    """Flatten metric leaves to dotted paths, skipping the ``_meta`` block."""
    flat: Dict[str, Any] = {}

    def walk(obj: Any, prefix: str) -> None:
        for key, value in obj.items():
            path = f"{prefix}{key}"
            if isinstance(value, dict):
                walk(value, path + ".")
            else:
                flat[path] = value

    walk({k: v for k, v in results.items() if k != "_meta"}, "")
    return flat


def compare_scalars(baseline: Any, observed: Any, tolerance: float) -> Tuple[bool, Optional[float]]:
    """Relative comparison (abs fallback for near-zero); exact for non-numbers."""
    if _is_number(baseline) and _is_number(observed):
        base, obs = float(baseline), float(observed)
        diff = abs(obs - base)
        if diff == 0.0:
            return True, 0.0
        scale = max(abs(base), abs(obs), 1e-12)
        rel = diff / scale
        return (rel <= tolerance or diff <= 1e-12), rel
    return baseline == observed, None


@dataclass
class ReproReport:
    n: int
    tolerance: float
    run_ids: List[str]
    rows: List[ReproRow]

    @property
    def ok(self) -> bool:
        return all(row.ok for row in self.rows)

    @property
    def exit_code(self) -> int:
        return 0 if self.ok else 1

    def failures(self) -> List[ReproRow]:
        return [row for row in self.rows if not row.ok]

    def format_table(self) -> str:
        header = f"{'metric':<24} {'baseline':>14} {'observed':>14} {'rel_diff':>10}  status"
        lines = [header, "-" * len(header)]
        seen_runs: Dict[str, int] = {}
        for row in self.rows:
            seen_runs[row.run_id] = seen_runs.get(row.run_id, 0) + 1
        for row in self.rows:
            base = _fmt(row.baseline)
            obs = _fmt(row.observed)
            rel = "-" if row.rel_diff is None else f"{row.rel_diff:.3e}"
            lines.append(f"{row.metric:<24} {base:>14} {obs:>14} {rel:>10}  "
                         f"{'ok' if row.ok else 'DRIFT'}")
        if self.ok:
            lines.append(f"\nREPRO OK: {len(self.rows)} metric(s) reproduced across "
                         f"{self.n} runs (relative tolerance {self.tolerance:g})")
        else:
            bad = self.failures()
            lines.append(f"\nREPRO DRIFT: {len(bad)} of {len(self.rows)} metric comparisons "
                         f"exceeded tolerance {self.tolerance:g}")
            for row in bad[:12]:
                lines.append(f"  - {row.metric}: baseline={_fmt(row.baseline)} "
                             f"observed={_fmt(row.observed)} run={row.run_id}")
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "n": self.n,
            "tolerance": self.tolerance,
            "run_ids": self.run_ids,
            "ok": self.ok,
            "exit_code": self.exit_code,
            "rows": [row.__dict__ for row in self.rows],
        }


def _fmt(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


def check_repro(config: Any, experiment: str, fn: Callable[[Dict[str, Any]], Dict[str, Any]],
                n: int = 3, tolerance: float = DEFAULT_TOLERANCE, notes: str = "", *,
                runs_root: Optional[Path] = None,
                repo_root_path: Optional[Path] = None) -> ReproReport:
    """Run ``config`` ``n`` times and compare every metric to the first run."""
    n = int(n)
    if n < 2:
        raise ValueError("--check-repro needs N >= 2 (a baseline plus at least one rerun)")
    if tolerance < 0:
        raise ValueError("tolerance must be >= 0")

    baseline: Optional[RunResult] = None
    run_ids: List[str] = []
    rows: List[ReproRow] = []
    for index in range(n):
        note = (notes + " | " if notes else "") + f"check-repro {index + 1}/{n}"
        result = run(config, experiment, fn, notes=note, runs_root=runs_root,
                     repo_root_path=repo_root_path)
        run_ids.append(result.run_id)
        if baseline is None:
            baseline = result
            continue
        base_flat = flatten_results(baseline.results)
        obs_flat = flatten_results(result.results)
        for metric in sorted(set(base_flat) | set(obs_flat)):
            base_value = base_flat.get(metric)
            obs_value = obs_flat.get(metric)
            ok, rel = compare_scalars(base_value, obs_value, tolerance)
            rows.append(ReproRow(result.run_id, metric, base_value, obs_value, rel, ok))
        base_seed = baseline.results.get("_meta", {}).get("seed")
        obs_seed = result.results.get("_meta", {}).get("seed")
        if base_seed != obs_seed:
            rows.append(ReproRow(result.run_id, "_meta.seed", base_seed, obs_seed, None, False))
    assert baseline is not None
    return ReproReport(n=n, tolerance=tolerance, run_ids=run_ids, rows=rows)


# --------------------------------------------------------------------------- #
# experiment loading / CLI
# --------------------------------------------------------------------------- #
def _split_module_spec(module_spec: str) -> Tuple[str, str]:
    """``path/to/task.py:fn`` -> (path, 'fn'); Windows drive letters survive."""
    if ":" in module_spec:
        head, _, tail = module_spec.rpartition(":")
        if tail.isidentifier():
            return head, tail
    return module_spec, "run_task"


def load_experiment(experiment: Optional[str] = None, *, module_spec: Optional[str] = None,
                    repo_root_path: Optional[Path] = None) -> Callable[..., Any]:
    """Resolve an experiment entry point.

    Default convention: ``04_experiments/<experiment>/task.py`` exposing
    ``run_task(config) -> dict``.  ``--module path.py:fn`` (or ``pkg.mod:fn``)
    overrides it for tests.
    """
    root = Path(repo_root_path) if repo_root_path else repo_root()
    if module_spec:
        target, fn_name = _split_module_spec(module_spec)
        candidate = Path(target)
        if candidate.is_file():
            spec = importlib.util.spec_from_file_location(f"_runner_exp_{fn_name}", candidate)
            if spec is None or spec.loader is None:
                raise ImportError(f"cannot load {candidate}")
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
        else:
            module = importlib.import_module(target)
        fn = getattr(module, fn_name, None)
        if not callable(fn):
            raise AttributeError(f"{target} has no callable {fn_name!r}")
        return fn

    if not experiment:
        raise ValueError("either experiment name or module_spec is required")
    path = root / "04_experiments" / experiment / "task.py"
    if not path.is_file():
        raise FileNotFoundError(
            f"no experiment entry point at {path}; expected "
            f"04_experiments/{experiment}/task.py with run_task(config)")
    spec = importlib.util.spec_from_file_location(f"_runner_exp_{_slug(experiment)}", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    fn = getattr(module, "run_task", None)
    if not callable(fn):
        raise AttributeError(f"{path} must define run_task(config) -> dict")
    return fn


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="runner.py",
        description="Run an experiment with full provenance, or verify reproducibility.")
    parser.add_argument("--experiment", help="experiment name (04_experiments/<name>/task.py)")
    parser.add_argument("--config", required=True, help="path to the JSON config")
    parser.add_argument("--notes", default="", help="free-text notes stored in meta.json")
    parser.add_argument("--seed", type=int, default=None, help="override config seed")
    parser.add_argument("--check-repro", type=int, default=None, metavar="N",
                        help="run the config N times and compare every metric to run 1")
    parser.add_argument("--tol", type=float, default=DEFAULT_TOLERANCE,
                        help=f"relative tolerance for --check-repro (default {DEFAULT_TOLERANCE:g})")
    parser.add_argument("--module", default=None,
                        help="override entry point, e.g. path/to/task.py:run_task")
    parser.add_argument("--runs-root", default=None, help="override the runs/ directory (CI)")
    parser.add_argument("--repo-root", default=None, help="override repo root (CI)")
    parser.add_argument("--json", action="store_true", help="print machine-readable output")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.experiment and not args.module:
        parser.error("--experiment or --module is required")
    if args.check_repro is not None and args.check_repro < 2:
        print("error: --check-repro needs N >= 2 (a baseline plus at least one rerun)",
              file=sys.stderr)
        return 2

    root = Path(args.repo_root).resolve() if args.repo_root else repo_root()
    runs_root = Path(args.runs_root) if args.runs_root else None
    experiment = args.experiment or Path(_split_module_spec(args.module)[0]).stem

    try:
        fn = load_experiment(args.experiment, module_spec=args.module, repo_root_path=root)
    except (FileNotFoundError, ImportError, AttributeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    try:
        if args.check_repro is not None:
            report = check_repro(args.config, experiment, fn, n=args.check_repro,
                                 tolerance=args.tol, notes=args.notes,
                                 runs_root=runs_root, repo_root_path=root)
            if args.json:
                print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
            else:
                print(report.format_table())
            return report.exit_code

        result = run(args.config, experiment, fn, notes=args.notes, runs_root=runs_root,
                     repo_root_path=root, seed=args.seed)
    except (FileNotFoundError, ValueError, TypeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    else:
        print(f"run_id:  {result.run_id}")
        print(f"run_dir: {result.run_dir}")
        print(f"results: {result.results_path}")
        print(f"metrics: {json.dumps(result.metrics(), sort_keys=True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
