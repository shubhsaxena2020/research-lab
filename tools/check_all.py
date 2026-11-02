#!/usr/bin/env python
"""check_all.py - one command that proves the whole toolchain still works.

WHY THIS EXISTS
---------------
The lab has eleven commands that must keep working: three test suites, the six integrity
tools (cited in the toy pipeline), the harness, and the paper template. Remembering the
right order and the right flags is exactly the kind of memory that fails at 2am and turns
into "I thought the tests passed". This runner is the single entry point:

    python tools/check_all.py

It runs, in order and as separate processes (so one crash cannot poison the next):

    1. tools-tests      python -m pytest tools/tests -q
    2. harness-tests    python -m pytest 04_experiments/harness/tests -q
    3. paper-tests      python -m pytest 05_paper/template/tests -q
    4. toy-pipeline     python 04_experiments/toy/run_pipeline.py

and prints one honest table:

    step | command | exit code | duration | result
    ...
    4/4 steps passed

Exit codes match the rest of the toolchain (CONTRACTS.md §6): 0 = every step passed,
1 = at least one step failed, 2 = usage error.

DESIGNED TO BE TRUSTWORTHY, NOT CONVENIENT
------------------------------------------
* A step that times out is a FAIL, never a pass. A hung pytest process would otherwise sit
  forever and the "run" would silently stop completing; `--timeout` (default 600 s, per
  step) turns that into a loud failure. `timeout` appears in the result column so it is
  never confused with a genuine non-zero exit.
* A step whose directory/script is missing is a FAIL, not a skip. "No tests found" must not
  read as "all good".
* The runner itself writes nothing into the repo: no report files, no cache. It runs pytest
  with `-p no:cacheprovider` and exports `PYTHONDONTWRITEBYTECODE=1`, so a check does not
  dirty the working tree it is supposed to be inspecting.
* Paths are resolved from `Path(__file__).resolve().parents[1]`, so it works from any
  working directory. Step commands are shown repo-relative because that is what you would
  type.

USAGE
-----
    python tools/check_all.py                 # everything (~1-2 min, the toy pipeline is slow)
    python tools/check_all.py --fast          # skip the toy pipeline (test suites only)
    python tools/check_all.py --list          # show the steps, run nothing
    python tools/check_all.py --only toys     # one step by name
    python tools/check_all.py --json          # machine-readable results (no table)
    python tools/check_all.py --timeout 120   # per-step timeout in seconds (default 600)

WINDOWS / MSYS NOTE
-------------------
Run it through `ops/check.sh` or type `python tools/check_all.py` yourself. If you invoke
the native python.exe from git-bash with a path argument, pass a native `C:/...` path, not
`/c/...`: MSYS does not translate arguments for native programs, so `/c/Users/...` arrives
at Python as a literal path that does not exist. This script itself is immune (it resolves
its own root), but arguments you pass to it are not translated either.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Sequence

# Repo root = the directory that contains tools/. Resolved, never relative to cwd.
ROOT = Path(__file__).resolve().parents[1]

DEFAULT_TIMEOUT = 600
OUTPUT_TAIL_LINES = 25  # how much of a failing step's output to show

# pytest flags that keep the working tree clean. `-p no:cacheprovider` stops pytest
# writing .pytest_cache; PYTHONDONTWRITEBYTECODE (below) stops __pycache__.
PYTEST_CLEAN = ["-q", "-p", "no:cacheprovider"]


@dataclass(frozen=True)
class Step:
    """One command the runner proves.

    `args` are passed to the current interpreter (sys.executable), so the runner tests the
    same Python that runs it. `display` is the repo-relative command a human would type.
    `requires` is a repo-relative path that must exist - if it does not, the step fails
    instead of being quietly reported as fine.
    """

    name: str
    args: List[str]
    display: str
    requires: Optional[str] = None
    is_toy: bool = False

    def missing(self, root: Path = ROOT) -> Optional[str]:
        if not self.requires:
            return None
        return None if (root / self.requires).exists() else self.requires


def _pytest_step(name: str, directory: str) -> Step:
    return Step(
        name=name,
        args=["-m", "pytest", directory, *PYTEST_CLEAN],
        display=f"python -m pytest {directory} -q",
        requires=directory,
    )


def build_steps(fast: bool = False) -> List[Step]:
    """The canonical ordered step list. `fast` drops the slow toy pipeline."""
    steps = [
        _pytest_step("tools-tests", "tools/tests"),
        _pytest_step("harness-tests", "04_experiments/harness/tests"),
        _pytest_step("paper-tests", "05_paper/template/tests"),
        Step(
            name="toy-pipeline",
            args=["04_experiments/toy/run_pipeline.py"],
            display="python 04_experiments/toy/run_pipeline.py",
            requires="04_experiments/toy/run_pipeline.py",
            is_toy=True,
        ),
    ]
    if fast:
        steps = [s for s in steps if not s.is_toy]
    return steps


def step_names(fast: bool = False) -> List[str]:
    return [s.name for s in build_steps(fast=fast)]


@dataclass
class StepResult:
    """Outcome of one step. `passed` is the only thing that counts; `result` explains it."""

    step: str
    command: str
    exit_code: Optional[int]
    duration_s: float
    result: str
    passed: bool
    timed_out: bool = False
    output: str = field(default="", repr=False)

    def as_dict(self) -> dict:
        d = {
            "step": self.step,
            "command": self.command,
            "exit_code": self.exit_code,
            "duration_s": round(self.duration_s, 3),
            "result": self.result,
            "passed": self.passed,
            "timed_out": self.timed_out,
        }
        if not self.passed and self.output.strip():
            d["output_tail"] = "\n".join(self.output.strip().splitlines()[-OUTPUT_TAIL_LINES:])
        return d


def _env() -> dict:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def _as_text(chunk) -> str:
    if chunk is None:
        return ""
    if isinstance(chunk, bytes):
        return chunk.decode("utf-8", "replace")
    return chunk


def run_step(step: Step, root: Path = ROOT, timeout: float = DEFAULT_TIMEOUT) -> StepResult:
    """Execute one step. Never raises for a failing/timed-out child - that is the point."""
    missing = step.missing(root)
    if missing:
        return StepResult(
            step=step.name,
            command=step.display,
            exit_code=None,
            duration_s=0.0,
            result=f"FAIL (missing {missing})",
            passed=False,
        )

    started = time.monotonic()
    try:
        proc = subprocess.run(
            [sys.executable, *step.args],
            cwd=str(root),
            stdin=subprocess.DEVNULL,  # an interactive prompt must not wedge the run
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            env=_env(),
        )
    except subprocess.TimeoutExpired as exc:
        elapsed = time.monotonic() - started
        out = _as_text(exc.stdout) + _as_text(exc.stderr)
        return StepResult(
            step=step.name,
            command=step.display,
            exit_code=None,
            duration_s=elapsed,
            result=f"FAIL (timeout {timeout:g}s)",
            passed=False,
            timed_out=True,
            output=out,
        )
    except OSError as exc:
        elapsed = time.monotonic() - started
        return StepResult(
            step=step.name,
            command=step.display,
            exit_code=None,
            duration_s=elapsed,
            result=f"FAIL (launch error: {exc.__class__.__name__})",
            passed=False,
            output=str(exc),
        )

    elapsed = time.monotonic() - started
    code = proc.returncode
    passed = code == 0
    return StepResult(
        step=step.name,
        command=step.display,
        exit_code=code,
        duration_s=elapsed,
        result="PASS" if passed else f"FAIL (exit {code})",
        passed=passed,
        output=(proc.stdout or "") + (proc.stderr or ""),
    )


def _fmt_duration(seconds: float) -> str:
    if seconds >= 60:
        return f"{int(seconds // 60)}m{seconds % 60:04.1f}s"
    return f"{seconds:.1f}s"


def format_table(results: Sequence[StepResult]) -> str:
    """Render the honesty table. Pure function: no I/O, no clock, easy to test."""
    header = ("step", "command", "exit", "duration", "result")
    rows = []
    for r in results:
        code = "-" if r.exit_code is None else str(r.exit_code)
        rows.append((r.step, r.command, code, _fmt_duration(r.duration_s), r.result))

    widths = [len(h) for h in header]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    def line(cells) -> str:
        return "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells)).rstrip()

    total_width = sum(widths) + 2 * (len(widths) - 1)
    sep = "-" * total_width
    out = [line(header), sep]
    out.extend(line(row) for row in rows)
    out.append(sep)
    passed = sum(1 for r in results if r.passed)
    out.append(f"{passed}/{len(results)} steps passed")
    return "\n".join(out)


def overall_exit(results: Sequence[StepResult]) -> int:
    """0 only when every step passed. An empty list is a usage problem, not a success."""
    if not results:
        return 2
    return 0 if all(r.passed for r in results) else 1


def _print_list(steps: Sequence[Step], root: Path) -> None:
    print(f"repo root: {root}")
    if not steps:
        print("no steps selected")
        return
    width = max(len(s.name) for s in steps)
    for i, step in enumerate(steps, 1):
        note = "  [skipped by --fast]" if step.is_toy else ""
        print(f"{i:2d}. {step.name.ljust(width)}  {step.display}{note}")
    print(f"{len(steps)} step(s) in order; --fast skips toy-pipeline")


def _print_failures(results: Sequence[StepResult]) -> None:
    failed = [r for r in results if not r.passed]
    if not failed:
        return
    print("\nfailed step output (last %d lines each):" % OUTPUT_TAIL_LINES)
    for r in failed:
        print(f"\n--- {r.step}: {r.result} ---")
        tail = "\n".join(r.output.strip().splitlines()[-OUTPUT_TAIL_LINES:])
        print(tail if tail else "(no output captured)")


def _positive_int(text: str) -> int:
    try:
        value = int(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"not an integer: {text!r}")
    if value <= 0:
        raise argparse.ArgumentTypeError(f"must be > 0 seconds, got {value}")
    return value


def _build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="check_all.py",
        description="Run the whole S3 toolchain (3 test suites + toy pipeline) and report one table.",
        epilog="Exit 0 = every step passed, 1 = a step failed, 2 = usage error.",
    )
    ap.add_argument("--fast", action="store_true", help="skip the slow toy pipeline step")
    ap.add_argument("--list", dest="list_steps", action="store_true",
                    help="print the steps without running them")
    ap.add_argument("--only", metavar="NAME", choices=step_names(),
                    help="run a single step by name (see --list)")
    ap.add_argument("--json", action="store_true", help="print machine-readable results")
    ap.add_argument("--timeout", type=_positive_int, default=DEFAULT_TIMEOUT, metavar="SECONDS",
                    help=f"per-step timeout in seconds (default {DEFAULT_TIMEOUT})")
    return ap


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = _build_parser()
    args = ap.parse_args(argv)

    fast = bool(args.fast)
    if args.only and fast and args.only not in step_names(fast=True):
        ap.error(
            f"--only {args.only} conflicts with --fast (the toy pipeline is skipped by --fast)"
        )

    steps = build_steps(fast=fast)
    if args.only:
        steps = [s for s in steps if s.name == args.only]

    if args.list_steps:
        if args.json:
            print(json.dumps(
                {
                    "root": str(ROOT),
                    "python": sys.executable,
                    "fast": fast,
                    "timeout_s": args.timeout,
                    "steps": [
                        {"index": i, "name": s.name, "command": s.display}
                        for i, s in enumerate(steps, 1)
                    ],
                },
                indent=2,
                ensure_ascii=False,
            ))
        else:
            _print_list(steps, ROOT)
        return 0

    if not args.json:
        print(f"repo root: {ROOT}")
        print(f"python:    {sys.executable}")
        print(f"running {len(steps)} step(s), timeout {args.timeout}s per step\n")

    results: List[StepResult] = []
    for step in steps:
        if not args.json:
            print(f".. {step.name}: {step.display}", flush=True)
        result = run_step(step, root=ROOT, timeout=args.timeout)
        results.append(result)
        if not args.json:
            print(f"   -> {result.result} in {_fmt_duration(result.duration_s)}", flush=True)

    code = overall_exit(results)

    if args.json:
        passed = sum(1 for r in results if r.passed)
        print(json.dumps(
            {
                "root": str(ROOT),
                "python": sys.executable,
                "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "fast": fast,
                "timeout_s": args.timeout,
                "passed": passed,
                "total": len(results),
                "ok": code == 0,
                "steps": [r.as_dict() for r in results],
            },
            indent=2,
            ensure_ascii=False,
        ))
        return code

    print()
    _print_failures(results)
    if any(not r.passed for r in results):
        print()
    print(format_table(results))
    return code


if __name__ == "__main__":
    sys.exit(main())
