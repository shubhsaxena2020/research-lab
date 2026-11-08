"""Tests for provenance capture: git diff + PREREGISTRATION.md sha256.

Run with:  python -m pytest 04_experiments/harness/tests/test_provenance.py -q
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import runner

REPO = runner.repo_root()


def config(name="prov", **extra):
    cfg = {"name": name, "experiment": "unit", "seed": 0, "toy": True}
    cfg.update(extra)
    return cfg


def constant_fn(cfg):
    return {"accuracy": 0.5, "loss": 1.0}


def test_provenance_files_exist_and_meta_keys(tmp_path, runs_root=None):
    # use fixture-style runs_root via tmp_path
    rr = tmp_path / "runs"
    result = runner.run(config("prov"), "unit", constant_fn, runs_root=rr)

    expected_files = ("git_diff.patch", "git_diff.txt", "git-diff.patch", "git-diff.txt")
    for base in expected_files:
        assert (result.run_dir / "artifacts" / base).is_file(), f"missing artifacts/{base}"
        assert (result.run_dir / base).is_file(), f"missing top-level {base}"

    expected_keys = (
        "git_diff", "git_diff_sha256", "git_diff_path",
        "git_untracked", "preregistration_sha256", "preregistration_path",
    )
    for key in expected_keys:
        assert key in result.meta, f"missing meta key {key}"

    # sha matches the written diff text
    diff_text = (result.run_dir / "artifacts" / "git_diff.patch").read_text(encoding="utf-8")
    assert result.meta["git_diff"] == diff_text
    assert result.meta["git_diff_sha256"] == hashlib.sha256(diff_text.encode("utf-8")).hexdigest()

    # top-level copies are identical
    for base in expected_files:
        assert (result.run_dir / base).read_text(encoding="utf-8") == diff_text

    # git_diff_path resolves to an existing file
    from pathlib import Path as _P
    p = _P(result.meta["git_diff_path"])
    assert p.is_file()

    # untracked is a list
    assert isinstance(result.meta["git_untracked"], list)

    # preregistration hash matches helper
    assert result.meta["preregistration_sha256"] == runner.git_preregistration_sha256(REPO)

    # preregistration path resolves
    pp = _P(result.meta["preregistration_path"])
    assert pp.is_file()


def test_git_diff_helper_returns_text():
    text = runner.git_diff(REPO)
    assert isinstance(text, str)
    assert "git diff HEAD" in text.lower() or "=====" in text


def test_git_preregistration_sha256_matches_file():
    h = runner.git_preregistration_sha256(REPO)
    assert isinstance(h, str) and len(h) == 64
    # recompute independently
    path = REPO / "04_experiments" / "PREREGISTRATION.md"
    data = path.read_bytes()
    assert h == hashlib.sha256(data).hexdigest()