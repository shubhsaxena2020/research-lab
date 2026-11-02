#!/usr/bin/env python
"""run_pipeline.py — end-to-end dry run of the whole S3 toolchain on the TOY experiment.

TOY - NOT A RESULT. Nothing this script produces may appear in the paper; it exists to
prove the plumbing works before the topic is approved and real experiments start.

It is deliberately built as a series of *expectations*, not just a series of calls: each
step declares the exit code it must produce. A guard that stops working (for example if
`make_tables.py` silently started rendering toy summaries into paper tables) makes this
script fail, which is exactly the alarm we want.

    python 04_experiments/toy/run_pipeline.py            # run everything, print a table
    python 04_experiments/toy/run_pipeline.py --keep     # keep generated artefacts
    python 04_experiments/toy/run_pipeline.py --list     # list steps without running

Exit 0 when every step behaves as expected, 1 otherwise.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PY = sys.executable


def run(args, cwd=ROOT):
    """Run a command, return (exit_code, combined_output)."""
    proc = subprocess.run(
        [PY] + args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=300,
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def build_steps(tmp: Path):
    idx = "04_experiments/RESULTS-INDEX.json"
    toy_draft = "04_experiments/toy/draft_toy.md"
    tampered = str(tmp / "tampered.md")
    return [
        # (name, argv, expected exit code, what the step proves)
        (
            "run toy experiment",
            ["04_experiments/toy/run_toy.py"],
            0,
            "3 seeds x 2 configs produce run folders",
        ),
        (
            "aggregate runs -> summary",
            ["04_experiments/harness/aggregate.py", "--experiment", "toy"],
            0,
            "summary + index entries rebuilt from runs",
        ),
        (
            "rerun reproducibility check",
            ["04_experiments/harness/runner.py", "--experiment", "toy",
             "--config", "04_experiments/harness/configs/toy_ours.json",
             "--check-repro", "2"],
            0,
            "same config twice gives identical metrics",
        ),
        (
            "table generator REFUSES toy summary",
            ["05_paper/template/tables/make_tables.py",
             "--summary", "04_experiments/results/summary_toy.json",
             "--name", "toy-table", "--out-dir", str(tmp / "tables")],
            2,
            "guard: toy numbers can never reach a paper table",
        ),
        (
            "figure generator (toy, explicit --allow-toy)",
            ["05_paper/template/figures/make_figures.py", "--index", idx,
             "--figure", "toy.accuracy", "--out-dir", str(tmp / "figures"), "--allow-toy"],
            0,
            "CSV + SVG + .tex emitted from the index only",
        ),
        (
            "check_numbers on a clean toy draft",
            ["tools/check_numbers.py", "--draft", toy_draft, "--allow-toy", "--no-write", "--quiet"],
            0,
            "every number traces to index -> config/results",
        ),
        (
            "check_numbers on a TAMPERED draft",
            ["tools/check_numbers.py", "--draft", tampered, "--allow-toy", "--no-write", "--quiet"],
            1,
            "a changed digit is caught as MISMATCH",
        ),
        (
            "claims audit",
            ["tools/claims_audit.py", "--audit", "04_experiments/toy/claims_audit_toy.md",
             "--draft", toy_draft, "--index", idx,
             "--citations", "02_literature/verified_citations.csv"],
            0,
            "each abstract claim binds to real evidence",
        ),
        (
            "student digest",
            ["tools/make_digest.py", "--section", toy_draft, "--index", idx,
             "--citations", "02_literature/verified_citations.csv",
             "--out-dir", str(tmp / "digest")],
            0,
            "digest generated from the draft + evidence only",
        ),
        (
            "student digest self-check",
            ["tools/make_digest.py", "--check", str(tmp / "digest" / "DRAFT_TOY.md")],
            0,
            "generated digest passes its own completeness check",
        ),
        (
            "review pack",
            ["tools/simulate_review.py", "pack", "--draft", toy_draft,
             "--round", "1", "--out", str(tmp / "reviews")],
            0,
            "six persona prompts written",
        ),
        (
            "originality check (clean draft vs corpus)",
            ["tools/originality_check.py", "--draft", toy_draft,
             "--corpus", "04_experiments/toy/corpus", "--json"],
            1,
            "planted verbatim run is caught (the corpus copy in this repo is deliberate)",
        ),
    ]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="TOY end-to-end dry run of the S3 toolchain.")
    ap.add_argument("--keep", action="store_true", help="keep the temporary output directory")
    ap.add_argument("--list", action="store_true", help="list steps and exit")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args(argv)

    tmp = Path(tempfile.mkdtemp(prefix="toy_pipeline_"))
    steps = build_steps(tmp)

    if args.list:
        for i, (name, _, want, why) in enumerate(steps, 1):
            print(f"{i:2d}. {name:45s} expect exit {want}  ({why})")
        return 0

    # The tampered draft: one digit changed, everything else identical.
    src = (ROOT / "04_experiments/toy/draft_toy.md").read_text(encoding="utf-8")
    tampered = src.replace("-->0.8852<", "-->0.9952<")
    if tampered == src:
        print("SETUP FAILED: could not tamper with the draft (marker changed?)", file=sys.stderr)
        return 1
    (tmp / "tampered.md").write_text(tampered, encoding="utf-8")

    rows, failures = [], 0
    for name, cmd, want, why in steps:
        code, out = run(cmd)
        ok = code == want
        failures += 0 if ok else 1
        rows.append((ok, name, want, code, why))
        if not ok or args.verbose:
            print(f"\n--- {name} (exit {code}, expected {want}) ---")
            print("\n".join(out.strip().splitlines()[:20]))

    print("\n" + "=" * 78)
    print(f"{'':2s} {'step':45s} {'want':>4s} {'got':>4s}  proves")
    print("=" * 78)
    for ok, name, want, code, why in rows:
        mark = "ok  " if ok else "FAIL"
        print(f"{mark} {name:45s} {want:4d} {code:4d}  {why}")
    print("=" * 78)
    print(f"{len(rows) - failures}/{len(rows)} steps behaved as expected")

    if not args.keep:
        shutil.rmtree(tmp, ignore_errors=True)
    else:
        print(f"artefacts kept in {tmp}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
