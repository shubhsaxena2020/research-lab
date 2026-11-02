"""Tests for the experiment harness: runner, lock, aggregate.

Run with:  python -m pytest 04_experiments/harness/tests/test_runner.py -q

Every test writes into pytest's ``tmp_path``; the real ``runs/`` directory and
the real ``RESULTS-INDEX.json`` are never touched.
"""

from __future__ import annotations

import json
import os
import platform
import random
import re
import secrets
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import pytest

import aggregate
import lock
import runner

REPO = runner.repo_root()


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def config(name="unit", **extra):
    cfg = {"name": name, "experiment": "unit", "seed": 0, "toy": True}
    cfg.update(extra)
    return cfg


def seeded_fn(cfg):
    """Deterministic only if the runner seeded the RNGs before calling us."""
    print(f"seeded run for {cfg['name']} seed={cfg['seed']}")
    return {
        "accuracy": random.random(),
        "loss": 1.0 / (1.0 + float(cfg["seed"])),
        "n_test": 90,
        "config": {"depth": 2, "width": 4},
    }


def noisy_fn(cfg):
    return {"accuracy": secrets.randbits(53) / 2 ** 53, "loss": time.time()}


def constant_fn(cfg):
    return {"accuracy": 0.5, "loss": 1.0}


@pytest.fixture()
def runs_root(tmp_path):
    return tmp_path / "runs"


# --------------------------------------------------------------------------- #
# runner: run folder contents and provenance
# --------------------------------------------------------------------------- #
def test_run_creates_every_required_file(tmp_path, runs_root):
    result = runner.run(config("files"), "unit", seeded_fn, notes="unit-test",
                        runs_root=runs_root)

    assert result.run_dir.parent == runs_root
    for name in ("meta.json", "config.json", "stdout.log", "stderr.log", "results.json"):
        assert (result.run_dir / name).is_file(), f"missing {name}"
    assert (result.run_dir / "artifacts").is_dir()
    assert re.fullmatch(r"\d{8}T\d{6}Z_files_[0-9a-f]{7,40}(-\d+)?", result.run_id), \
        result.run_id

    # stdout capture really captured what fn printed
    stdout = (result.run_dir / "stdout.log").read_text(encoding="utf-8")
    assert "seeded run for files" in stdout

    # results.json follows CONTRACTS section 2
    results = json.loads((result.run_dir / "results.json").read_text(encoding="utf-8"))
    assert "_meta" in results
    for key in ("run_id", "config_name", "seed"):
        assert key in results["_meta"]
    assert results["_meta"]["run_id"] == result.run_id
    assert results["accuracy"] == result.results["accuracy"]
    assert set(results) >= {"accuracy", "loss", "n_test", "config"}
    assert all(not isinstance(v, (list, tuple)) for v in results.values())

    # config.json is the exact resolved config that was run, and its hash matches
    copied = json.loads((result.run_dir / "config.json").read_text(encoding="utf-8"))
    assert copied["name"] == "files" and copied["seed"] == 0
    assert runner.sha256_canonical(copied) == result.meta["config_sha256"]


def test_meta_has_real_git_hash_and_duration(runs_root):
    def slow_fn(cfg):
        time.sleep(0.05)
        return {"accuracy": 1.0}

    result = runner.run(config("meta"), "unit", slow_fn, runs_root=runs_root)
    meta = result.meta

    expected = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=str(REPO),
                              capture_output=True, text=True, timeout=30).stdout.strip()
    assert expected, "test repo is not a git checkout"
    assert meta["git_commit"] == expected
    assert re.fullmatch(r"[0-9a-f]{7,40}", meta["git_commit"])
    assert isinstance(meta["git_dirty"], bool)

    assert meta["duration_s"] >= 0.05, meta["duration_s"]
    assert meta["duration_s"] < 60
    assert meta["python"] == platform.python_version()
    assert meta["platform"]
    assert meta["started_at"].endswith("Z") and meta["finished_at"].endswith("Z")
    started = datetime.fromisoformat(meta["started_at"].replace("Z", "+00:00"))
    finished = datetime.fromisoformat(meta["finished_at"].replace("Z", "+00:00"))
    assert finished >= started
    assert meta["cpu_count"] == os.cpu_count()
    assert meta["seed"] == 0
    assert meta["host"] == runner.socket.gethostname()
    assert meta["env"].get("PYTHONHASHSEED") == "0"
    assert meta["status"] == "ok"
    assert meta["experiment"] == "unit"
    assert meta["toy"] is True
    # psutil is installed on this machine, so peak RSS must be a real number
    assert isinstance(meta["peak_rss_mb"], (int, float)) and meta["peak_rss_mb"] > 0
    for key in ("config_name", "config_sha256", "command", "device", "notes"):
        assert key in meta
    assert meta["notes"] == ""


def test_failed_run_writes_meta_and_reraises(runs_root):
    def broken_fn(cfg):
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError, match="boom"):
        runner.run(config("broken"), "unit", broken_fn, runs_root=runs_root)

    dirs = sorted(p for p in runs_root.iterdir() if p.is_dir())
    assert len(dirs) == 1
    run_dir = dirs[0]
    meta = json.loads((run_dir / "meta.json").read_text(encoding="utf-8"))
    assert meta["status"] == "error"
    assert "boom" in meta["error"]
    assert not (run_dir / "results.json").exists()
    assert "RuntimeError" in (run_dir / "stderr.log").read_text(encoding="utf-8")


def test_config_sha256_stable_and_distinct(runs_root):
    one = runner.run({"name": "hash", "seed": 0, "a": 1, "b": [1, 2]}, "unit",
                     constant_fn, runs_root=runs_root)
    two = runner.run({"b": [1, 2], "a": 1, "seed": 0, "name": "hash"}, "unit",
                     constant_fn, runs_root=runs_root)
    three = runner.run({"name": "hash", "seed": 0, "a": 2, "b": [1, 2]}, "unit",
                       constant_fn, runs_root=runs_root)

    assert one.meta["config_sha256"] == two.meta["config_sha256"]
    assert one.meta["config_sha256"] != three.meta["config_sha256"]
    assert len(one.meta["config_sha256"]) == 64

    # four runs of the same config still produce distinct run_ids (suffix on collision)
    assert len({one.run_id, two.run_id, three.run_id}) == 3


def test_set_seeds_makes_random_and_numpy_reproducible(runs_root):
    first = runner.run(config("seeds", seed=7), "unit", seeded_fn, runs_root=runs_root)
    second = runner.run(config("seeds", seed=7), "unit", seeded_fn, runs_root=runs_root)
    other = runner.run(config("seeds", seed=8), "unit", seeded_fn, runs_root=runs_root)
    assert first.meta["seed"] == 7
    assert first.results["accuracy"] == second.results["accuracy"]
    assert first.results["accuracy"] != other.results["accuracy"]

    np = pytest.importorskip("numpy")
    runner.set_seeds(11)
    a = np.random.rand()
    runner.set_seeds(11)
    assert np.random.rand() == a


# --------------------------------------------------------------------------- #
# runner: --check-repro
# --------------------------------------------------------------------------- #
def test_check_repro_passes_for_deterministic_fn(runs_root):
    report = runner.check_repro(config("repro", seed=3), "unit", seeded_fn, n=3,
                                runs_root=runs_root)
    assert report.ok
    assert report.exit_code == 0
    assert len(report.run_ids) == 3
    assert len(set(report.run_ids)) == 3
    table = report.format_table()
    assert "REPRO OK" in table
    assert "DRIFT" not in table
    assert "accuracy" in table


def test_check_repro_fails_for_noisy_fn(runs_root):
    report = runner.check_repro(config("noisy"), "unit", noisy_fn, n=2,
                                runs_root=runs_root)
    assert not report.ok
    assert report.exit_code == 1
    assert any(row.metric == "accuracy" for row in report.failures())
    assert "REPRO DRIFT" in report.format_table()


def test_check_repro_cli_exit_codes(tmp_path, runs_root):
    good = tmp_path / "good_task.py"
    good.write_text("def run_task(config):\n    return {'accuracy': 1.0}\n",
                    encoding="utf-8")
    bad = tmp_path / "bad_task.py"
    bad.write_text("import secrets\n"
                   "def run_task(config):\n"
                   "    return {'accuracy': secrets.randbits(30) / 2 ** 30}\n",
                   encoding="utf-8")
    cfg = tmp_path / "cli.json"
    cfg.write_text(json.dumps({"name": "cli"}), encoding="utf-8")

    common = ["--config", str(cfg), "--check-repro", "2", "--tol", "1e-9",
              "--runs-root", str(runs_root), "--repo-root", str(REPO)]
    assert runner.main(["--experiment", "unit", "--module", f"{good}:run_task", *common]) == 0
    assert runner.main(["--experiment", "unit", "--module", f"{bad}:run_task", *common]) == 1
    assert runner.main(["--experiment", "unit", "--module", f"{good}:run_task",
                        "--config", str(cfg), "--check-repro", "1"]) == 2


def test_check_repro_detects_missing_metric(runs_root):
    state = {"n": 0}

    def flaky_keys(cfg):
        state["n"] += 1
        metrics = {"accuracy": 0.5}
        if state["n"] > 1:
            metrics.pop("accuracy")
        return metrics

    report = runner.check_repro(config("keys"), "unit", flaky_keys, n=2,
                                runs_root=runs_root)
    assert report.exit_code == 1


# --------------------------------------------------------------------------- #
# lock
# --------------------------------------------------------------------------- #
def test_lock_refuses_second_acquire_and_names_holder(tmp_path):
    path = tmp_path / "HEAVY.lock"
    with lock.acquire("train-a", path=path):
        assert path.is_file()
        started = time.monotonic()
        with pytest.raises(lock.LockError) as excinfo:
            lock.acquire("train-b", path=path, timeout=0.3)
        elapsed = time.monotonic() - started
        message = str(excinfo.value)
        assert "train-a" in message
        assert str(os.getpid()) in message
        assert 0.2 <= elapsed < 3.0
    assert not path.exists()


def test_lock_releases_after_exception(tmp_path):
    path = tmp_path / "HEAVY.lock"
    with pytest.raises(ValueError):
        with lock.acquire("boom", path=path):
            raise ValueError("kaboom")
    assert not path.exists()
    # and can be taken again immediately
    with lock.acquire("next", path=path):
        assert lock.status(path)["name"] == "next"
    assert not path.exists()


def test_lock_reclaims_dead_pid(tmp_path):
    path = tmp_path / "HEAVY.lock"
    proc = subprocess.Popen([sys.executable, "-c", "pass"])
    proc.wait(timeout=60)
    dead_pid = proc.pid

    path.write_text(json.dumps({
        "name": "crashed-job", "pid": dead_pid, "host": lock.socket.gethostname(),
        "created_at": "2026-01-01T00:00:00Z", "created_ts": time.time(), "token": "old",
    }), encoding="utf-8")

    state = lock.staleness(path)
    assert state["stale"], state
    assert "not running" in state["reason"]

    with lock.acquire("replacement", path=path) as handle:
        assert lock.status(path)["name"] == "replacement"
        assert handle.info["token"] != "old"
    assert not path.exists()


def test_lock_reclaims_old_lock_even_with_live_pid(tmp_path):
    path = tmp_path / "HEAVY.lock"
    path.write_text(json.dumps({
        "name": "very-old", "pid": os.getpid(), "host": lock.socket.gethostname(),
        "created_at": "2026-01-01T00:00:00Z",
        "created_ts": time.time() - 5 * 3600, "token": "old",
    }), encoding="utf-8")

    assert lock.staleness(path)["stale"] is True
    with lock.acquire("fresh", path=path):
        assert lock.status(path)["name"] == "fresh"


def test_lock_does_not_release_someone_elses_lock(tmp_path):
    path = tmp_path / "HEAVY.lock"
    handle = lock.acquire("owner", path=path)
    # simulate a stale-reclaim by another process: the file is replaced
    path.write_text(json.dumps({"name": "thief", "pid": 1, "host": "other",
                                "created_at": "2026-01-01T00:00:00Z",
                                "created_ts": time.time(), "token": "other-token"}),
                    encoding="utf-8")
    handle.release()
    assert path.exists(), "must not delete a lock that is no longer ours"
    path.unlink()


def test_lock_cli_status_acquire_release(tmp_path, capsys):
    path = tmp_path / "HEAVY.lock"
    assert lock.main(["status", "--path", str(path)]) == 0
    assert lock.main(["acquire", "--name", "cli", "--path", str(path)]) == 0
    assert lock.main(["status", "--path", str(path)]) == 1
    assert lock.main(["release", "--path", str(path), "--force"]) == 0
    assert lock.main(["status", "--path", str(path)]) == 0


# --------------------------------------------------------------------------- #
# aggregate
# --------------------------------------------------------------------------- #
def _populate(runs_root, seeds=(0, 1, 2), value_fn=None):
    value_fn = value_fn or (lambda name, seed: 0.8 if name == "toy_baseline"
                            else 0.9 + seed * 0.001)
    for name in ("toy_baseline", "toy_ours"):
        for seed in seeds:
            def fn(cfg, name=name, seed=seed):
                return {"accuracy": value_fn(name, seed), "loss": 1.0}

            runner.run(config(name, seed=seed, experiment="toy"), "toy", fn,
                       runs_root=runs_root)


def test_aggregate_summary_matches_contract(tmp_path, runs_root):
    _populate(runs_root)
    summary = aggregate.aggregate("toy", metric="accuracy", runs_root=runs_root,
                                  root=tmp_path, write_index=True, quiet=True)

    for key in ("experiment", "configs", "metric", "n_seeds", "seeds", "per_run",
                "stats", "paired", "tables"):
        assert key in summary, f"summary missing {key}"
    assert summary["experiment"] == "toy"
    assert summary["metric"] == "accuracy"
    assert summary["configs"] == ["toy_baseline", "toy_ours"]
    assert summary["seeds"] == [0, 1, 2]
    assert summary["n_seeds"] == 3
    assert summary["per_run"]["toy_baseline"] == [0.8, 0.8, 0.8]
    assert len(summary["per_run"]["toy_ours"]) == 3
    assert summary["toy"] is True
    assert summary["tables"] == []

    stats = summary["stats"]["toy_ours"]
    for key in ("mean", "std", "ci95", "n", "ci_method"):
        assert key in stats
    assert stats["n"] == 3
    assert stats["mean"] == pytest.approx(0.901, abs=1e-9)
    assert stats["std"] == pytest.approx(0.001, abs=1e-9)
    assert stats["ci95"] is None or (len(stats["ci95"]) == 2
                                     and stats["ci95"][0] <= stats["mean"] <= stats["ci95"][1])

    on_disk = json.loads(aggregate.summary_path("toy", root=tmp_path).read_text(encoding="utf-8"))
    assert on_disk == summary


def test_aggregate_index_is_idempotent_and_preserves_others(tmp_path, runs_root):
    _populate(runs_root)
    index_file = tmp_path / "04_experiments" / "RESULTS-INDEX.json"
    index_file.parent.mkdir(parents=True, exist_ok=True)
    index_file.write_text(json.dumps({
        "version": 1,
        "updated_at": "2020-01-01T00:00:00Z",
        "entries": [{"id": "main.accuracy.baseline",
                     "file": "04_experiments/results/summary_main.json",
                     "key": "stats.baseline.mean", "description": "other worker's entry",
                     "run_id": "x", "tolerance": 0.0}],
    }), encoding="utf-8")

    aggregate.aggregate("toy", metric="accuracy", runs_root=runs_root, root=tmp_path,
                        quiet=True)
    first = json.loads(index_file.read_text(encoding="utf-8"))
    ids_first = sorted(e["id"] for e in first["entries"])
    assert ids_first == ["main.accuracy.baseline",
                         "toy.accuracy.toy_baseline", "toy.accuracy.toy_ours"]
    assert first["version"] == 1

    aggregate.aggregate("toy", metric="accuracy", runs_root=runs_root, root=tmp_path,
                        quiet=True)
    second = json.loads(index_file.read_text(encoding="utf-8"))
    assert sorted(e["id"] for e in second["entries"]) == ids_first
    assert len(second["entries"]) == 3

    entry = next(e for e in second["entries"] if e["id"] == "toy.accuracy.toy_ours")
    assert entry["file"] == "04_experiments/results/summary_toy.json"
    assert entry["key"] == "stats.toy_ours.mean"
    assert entry["toy"] is True
    assert "TOY - NOT A RESULT" in entry["description"]
    # the referenced key really resolves inside the summary file
    summary = json.loads(aggregate.summary_path("toy", root=tmp_path).read_text(encoding="utf-8"))
    resolved = summary
    for part in entry["key"].split("."):
        resolved = resolved[part]
    assert isinstance(resolved, float)


def test_aggregate_dedupes_repeated_seeds(tmp_path, runs_root):
    for _ in range(2):
        runner.run(config("toy_baseline", seed=0, experiment="toy"), "toy",
                   constant_fn, runs_root=runs_root)

    summary = aggregate.aggregate("toy", metric="accuracy", runs_root=runs_root,
                                  root=tmp_path, write_index=False, quiet=True)
    assert summary["per_run"]["toy_baseline"] == [0.5]
    assert summary["n_seeds"] == 1


def test_aggregate_skips_failed_and_other_experiment_runs(tmp_path, runs_root):
    _populate(runs_root, seeds=(0,))
    with pytest.raises(RuntimeError):
        runner.run(config("toy_ours", seed=9, experiment="toy"), "toy",
                   lambda cfg: (_ for _ in ()).throw(RuntimeError("nope")),
                   runs_root=runs_root)
    runner.run(config("other", experiment="different"), "different", constant_fn,
               runs_root=runs_root)

    summary = aggregate.aggregate("toy", metric="accuracy", runs_root=runs_root,
                                  root=tmp_path, write_index=False, quiet=True)
    assert summary["n_seeds"] == 1
    assert summary["configs"] == ["toy_baseline", "toy_ours"]


def test_aggregate_requires_stats_module_when_asked(tmp_path, runs_root, monkeypatch):
    _populate(runs_root, seeds=(0, 1))
    # point the stats lookup at a tree with no stats.py
    with pytest.raises(ImportError) as excinfo:
        aggregate.aggregate("toy", metric="accuracy", runs_root=runs_root, root=tmp_path,
                            require_stats=True, write_index=False, quiet=True)
    assert "stats.py" in str(excinfo.value)


def test_apply_stats_hook_uses_real_stats_module():
    module = aggregate.load_stats_module(REPO)
    summary = {
        "experiment": "unit", "configs": ["a", "b"], "metric": "accuracy",
        "n_seeds": 5, "seeds": [0, 1, 2, 3, 4],
        "per_run": {"a": [0.79, 0.80, 0.81, 0.79, 0.80],
                    "b": [0.90, 0.91, 0.89, 0.92, 0.91]},
        "stats": {"a": {"mean": 0.798, "std": 0.0, "ci95": None, "n": 5,
                        "ci_method": "none"},
                  "b": {"mean": 0.906, "std": 0.0, "ci95": None, "n": 5,
                        "ci_method": "none"}},
        "paired": None, "tables": [],
    }
    aggregate.apply_stats(summary, "accuracy", module)

    for name in ("a", "b"):
        entry = summary["stats"][name]
        assert entry["ci_method"] == "bootstrap"
        assert entry["n_boot"] == 10000 and entry["ci_seed"] == 12345
        assert len(entry["ci95"]) == 2 and entry["ci95"][0] <= entry["mean"] <= entry["ci95"][1]
        assert entry["n"] == 5
    paired = summary["paired"]
    assert paired["test"] in ("wilcoxon", "sign_test")
    assert paired["n_pairs"] == 5
    assert paired["correction"]["method"] == "holm"
    assert 0.0 <= paired["correction"]["p_adjusted"] <= 1.0
    assert paired["effect_size"]["name"] == "cohens_d"
    assert paired["effect_size"]["value"] < 0  # b beats a


def test_aggregate_metric_selection_and_errors(tmp_path, runs_root):
    _populate(runs_root, seeds=(0,))
    with pytest.raises(ValueError, match="not present"):
        aggregate.aggregate("toy", metric="does_not_exist", runs_root=runs_root,
                            root=tmp_path, write_index=False, quiet=True)
    with pytest.raises(LookupError):
        aggregate.aggregate("no_such_experiment", runs_root=runs_root, root=tmp_path,
                            write_index=False, quiet=True)
