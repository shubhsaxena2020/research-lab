#!/usr/bin/env python
"""Unit tests for tools/check_all.py - the one-command toolchain runner.

RECURSION GUARD (read this before adding a test)
------------------------------------------------
`check_all.py` runs `pytest tools/tests`. This file lives in `tools/tests`. Therefore no
test here may ever invoke the runner in run mode: `--only tools-tests`, bare
`python tools/check_all.py`, `python tools/check_all.py --fast` would all start a pytest
that collects this file again, which starts another pytest, forever. Only two safe things
are tested from a subprocess:

  * `--list` (and `--list --json`), which runs nothing;
  * argument errors, which exit before running anything.

Everything about execution and formatting is tested by calling the functions directly
(`run_step`, `format_table`, `overall_exit`) with fake steps and fake results.

The behaviours that matter are the ones that would let a broken toolchain look healthy:
a timeout counted as a pass, a missing suite treated as a skip, a table where pass and
fail look alike, or a runner that only works when launched from the repo root.

Run:  python -m pytest tools/tests/test_check_all.py -q
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))

import check_all  # noqa: E402

SCRIPT = TOOLS / "check_all.py"
ALL_STEPS = ["tools-tests", "harness-tests", "paper-tests", "toy-pipeline"]


def run_runner(*args, cwd=ROOT):
    """Invoke the runner with --list-style args only (never a real run - see guard)."""
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
    )


def fake(step, code: "int | None" = 0, result=None, passed=None, duration=1.25, timed_out=False):
    """Build a StepResult without running anything."""
    if result is None:
        result = "PASS" if code == 0 else f"FAIL (exit {code})"
    if passed is None:
        passed = code == 0 and not timed_out
    return check_all.StepResult(
        step=step,
        command=f"python -m pytest {step} -q",
        exit_code=code,
        duration_s=duration,
        result=result,
        passed=passed,
        timed_out=timed_out,
    )


class TestStepDiscovery(unittest.TestCase):
    def test_steps_are_exactly_the_four_required_ones_in_order(self):
        self.assertEqual(check_all.step_names(), ALL_STEPS)

    def test_fast_drops_only_the_toy_pipeline(self):
        self.assertEqual(check_all.step_names(fast=True), ALL_STEPS[:3])

    def test_each_pytest_step_targets_its_own_directory(self):
        steps = {s.name: s for s in check_all.build_steps()}
        self.assertIn("tools/tests", steps["tools-tests"].args)
        self.assertIn("04_experiments/harness/tests", steps["harness-tests"].args)
        self.assertIn("05_paper/template/tests", steps["paper-tests"].args)
        self.assertIn("04_experiments/toy/run_pipeline.py", steps["toy-pipeline"].args)

    def test_pytest_steps_do_not_write_caches_into_the_repo(self):
        # read-only claim: pytest must not create .pytest_cache, and -q must be present
        for name in ALL_STEPS[:3]:
            args = next(s.args for s in check_all.build_steps() if s.name == name)
            self.assertIn("-q", args)
            self.assertIn("no:cacheprovider", " ".join(args))


class TestCliWithoutRunning(unittest.TestCase):
    def test_list_names_all_four_steps_and_exits_zero(self):
        proc = run_runner("--list")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        for name in ALL_STEPS:
            self.assertIn(name, proc.stdout)
        # order is part of the contract: cheap suites first, slow pipeline last
        positions = [proc.stdout.index(name) for name in ALL_STEPS]
        self.assertEqual(positions, sorted(positions))
        self.assertIn(str(ROOT), proc.stdout)

    def test_unknown_only_exits_two_and_names_the_valid_choices(self):
        proc = run_runner("--only", "no-such-step")
        self.assertEqual(proc.returncode, 2)
        combined = proc.stdout + proc.stderr
        self.assertIn("no-such-step", combined)
        for name in ALL_STEPS:
            self.assertIn(name, combined, "usage error must list the valid step names")

    def test_only_conflicts_with_fast(self):
        proc = run_runner("--only", "toy-pipeline", "--fast")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("conflict", (proc.stdout + proc.stderr).lower())

    def test_non_positive_timeout_is_a_usage_error(self):
        for bad in ("0", "-5", "abc"):
            proc = run_runner("--timeout", bad, "--list")
            self.assertEqual(proc.returncode, 2, f"--timeout {bad} should be rejected")

    def test_json_list_is_parseable_and_names_the_same_steps(self):
        proc = run_runner("--list", "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)  # must be pure JSON on stdout
        self.assertEqual([s["name"] for s in payload["steps"]], ALL_STEPS)
        self.assertEqual([s["index"] for s in payload["steps"]], [1, 2, 3, 4])
        for step in payload["steps"]:
            self.assertTrue(step["command"].startswith("python "))

    def test_root_resolves_from_a_different_working_directory(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            proc = run_runner("--list", "--json", cwd=Path(tmp))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = json.loads(proc.stdout)
            self.assertEqual(Path(payload["root"]), ROOT)
            self.assertEqual([s["name"] for s in payload["steps"]], ALL_STEPS)


class TestTableFormatting(unittest.TestCase):
    def test_table_has_the_five_required_columns(self):
        table = check_all.format_table([fake("tools-tests")])
        header = table.splitlines()[0]
        for column in ("step", "command", "exit", "duration", "result"):
            self.assertIn(column, header)

    def test_pass_and_fail_rows_are_distinguishable(self):
        table = check_all.format_table([
            fake("tools-tests", code=0),
            fake("harness-tests", code=1),
        ])
        lines = table.splitlines()
        pass_row = next(l for l in lines if l.startswith("tools-tests"))
        fail_row = next(l for l in lines if l.startswith("harness-tests"))
        self.assertIn("PASS", pass_row)
        self.assertNotIn("FAIL", pass_row)
        self.assertIn("FAIL", fail_row)
        self.assertIn("1", fail_row)  # exit code is visible, not inferred
        self.assertIn("1/2 steps passed", table)

    def test_timeout_row_says_timeout_and_is_not_a_pass(self):
        table = check_all.format_table([
            fake("toy-pipeline", code=None, result="FAIL (timeout 600s)",
                 passed=False, timed_out=True),
        ])
        row = next(l for l in table.splitlines() if l.startswith("toy-pipeline"))
        self.assertIn("FAIL", row)
        self.assertIn("timeout", row.lower())
        self.assertNotIn("PASS", row)
        self.assertIn("0/1 steps passed", table)

    def test_duration_is_rendered_for_short_and_long_steps(self):
        table = check_all.format_table([
            fake("tools-tests", duration=41.83),
            fake("harness-tests", duration=95.0),
        ])
        self.assertIn("41.8s", table)   # seconds below a minute
        self.assertIn("1m35.0s", table)  # minutes above a minute
        self.assertEqual(check_all._fmt_duration(95.0), "1m35.0s")

    def test_all_passed_reports_full_count(self):
        table = check_all.format_table([fake(n) for n in ALL_STEPS])
        self.assertTrue(table.rstrip().endswith("4/4 steps passed"))


class TestRunStepSemantics(unittest.TestCase):
    """Direct calls - no pytest subprocess, so no recursion risk."""

    def test_zero_exit_is_a_pass(self):
        step = check_all.Step(name="ok", args=["-c", "raise SystemExit(0)"], display="python -c ok")
        result = check_all.run_step(step, timeout=60)
        self.assertTrue(result.passed)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.result, "PASS")

    def test_nonzero_exit_is_a_fail_with_the_code_visible(self):
        step = check_all.Step(name="bad", args=["-c", "raise SystemExit(3)"], display="python -c bad")
        result = check_all.run_step(step, timeout=60)
        self.assertFalse(result.passed)
        self.assertEqual(result.exit_code, 3)
        self.assertIn("FAIL", result.result)
        self.assertIn("3", result.result)

    def test_timeout_kills_the_step_and_is_never_a_pass(self):
        step = check_all.Step(
            name="hang",
            args=["-c", "import time; time.sleep(30)"],
            display="python -c hang",
        )
        result = check_all.run_step(step, timeout=1)
        self.assertFalse(result.passed, "a timed-out step must never count as passed")
        self.assertTrue(result.timed_out)
        self.assertIn("timeout", result.result.lower())
        self.assertIsNone(result.exit_code)
        self.assertLess(result.duration_s, 20, "the step must actually be killed, not waited out")

    def test_missing_suite_is_a_fail_not_a_skip(self):
        step = check_all.Step(
            name="gone",
            args=["-m", "pytest", "no/such/dir", "-q"],
            display="python -m pytest no/such/dir -q",
            requires="no/such/dir",
        )
        result = check_all.run_step(step, timeout=30)
        self.assertFalse(result.passed)
        self.assertIn("missing", result.result)
        self.assertIn("no/such/dir", result.result)

    def test_overall_exit_codes(self):
        self.assertEqual(check_all.overall_exit([fake("a"), fake("b")]), 0)
        self.assertEqual(check_all.overall_exit([fake("a"), fake("b", code=1)]), 1)
        self.assertEqual(check_all.overall_exit([]), 2, "no steps run is not a success")


class TestJsonResultShape(unittest.TestCase):
    """The --json payload is a contract for future CI, so pin its keys."""

    def test_result_dict_has_the_documented_keys(self):
        payload = fake("tools-tests", code=1, duration=2.5).as_dict()
        for key in ("step", "command", "exit_code", "duration_s", "result", "passed", "timed_out"):
            self.assertIn(key, payload)
        self.assertEqual(payload["exit_code"], 1)
        self.assertFalse(payload["passed"])
        self.assertEqual(payload["duration_s"], 2.5)

    def test_passing_result_carries_no_output_tail(self):
        payload = check_all.StepResult(
            step="x", command="c", exit_code=0, duration_s=1.0,
            result="PASS", passed=True, output="noise",
        ).as_dict()
        self.assertNotIn("output_tail", payload)


if __name__ == "__main__":
    unittest.main()
