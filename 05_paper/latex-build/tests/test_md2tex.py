#!/usr/bin/env python
"""test_md2tex.py -- converter regression tests.

Covers:
  * number preservation between paper.md and body.tex (existing check, fixed escape)
  * known citation conversion: an arXiv id present in refs.bib -> \\citep{key}
  * unknown citation remains visible in body.tex and is reported as unmatched
  * generated figure labels are unique (no duplicate fig: labels; fig:main-accuracy
    no longer duplicated)

Run directly: python 05_paper/latex-build/tests/test_md2tex.py
Run via pytest: python -m pytest 05_paper/latex-build/tests/test_md2tex.py -q
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BUILD = ROOT / "05_paper" / "latex-build"
PAPER = ROOT / "05_paper" / "draft" / "paper.md"
MD2TEX = BUILD / "md2tex.py"
BODY = BUILD / "body.tex"
REFS = BUILD / "refs.bib"

# A verified arXiv id (present as eprint in refs.bib) and an unverified one.
KNOWN_ID = "2403.01461"
UNKNOWN_ID = "2309.07597"


def _load_module():
    """Import md2tex.py by path."""
    if str(BUILD) not in sys.path:
        sys.path.insert(0, str(BUILD))
    spec = importlib.util.spec_from_file_location("md2tex_under_test", MD2TEX)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _reset_unmatched_state(mod):
    """Reset any module-level collections that record unmatched citations.

    Converter implementations name this state differently (``unmatched``,
    ``unresolved``, ``unknown``, ``missing``); clear every container whose
    name looks like a report of unresolved markers before each in-process run
    so one test cannot leak state into another.
    """
    hints = ("unmatch", "unresolved", "unknown", "missing")
    for name in list(vars(mod)):
        lowered = name.lower()
        if any(hint in lowered for hint in hints):
            obj = getattr(mod, name)
            if isinstance(obj, (list, set, dict)) and obj is not None:
                obj.clear()


def _run_subprocess():
    proc = subprocess.run(
        [sys.executable, str(MD2TEX)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = (proc.stdout or "") + "\n" + (proc.stderr or "")
    assert proc.returncode == 0, "md2tex.py failed:\n" + output
    body = BODY.read_text(encoding="utf-8")
    return output, body


def _run_in_process():
    """Run the converter in-process (imports by path, resets global state) and capture output."""
    mod = _load_module()
    _reset_unmatched_state(mod)
    old_argv = sys.argv
    sys.argv = [str(MD2TEX)]
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            try:
                mod.main()
            except SystemExit as e:
                if e.code not in (0, None):
                    raise
    finally:
        sys.argv = old_argv
    body = BODY.read_text(encoding="utf-8")
    return buf.getvalue(), body, mod


def _bib_key_for(arxiv_id, refs_text):
    """Return the BibTeX key whose entry contains arxiv_id (eprint/url), else None."""
    for m in re.finditer(r"@\w+\{([^,]+),(.*?)\n\s*\}", refs_text, re.S):
        key, block = m.group(1).strip(), m.group(2)
        if arxiv_id in block:
            return key
    return None


# --------------------------------------------------------------------------- number preservation


def test_number_preservation():
    """Every number in paper.md survives byte-identical in body.tex."""
    md = PAPER.read_text(encoding="utf-8")
    nums = re.findall(r"<!--\s*num:[^>]*-->(.*?)<!--\s*/num\s*-->", md, flags=re.S)
    nums = [n.strip() for n in nums]
    _run_subprocess()
    tex = BODY.read_text(encoding="utf-8")
    missing = [n for n in nums if n not in tex and n.replace("%", r"\%") not in tex]
    assert not missing, "missing numbers: " + repr(missing[:20])
    assert len(nums) > 0


# --------------------------------------------------------------------------- citations


def test_known_arxiv_citation_becomes_citep():
    """An arXiv id present in refs.bib becomes \\citep{key} in body.tex."""
    refs = REFS.read_text(encoding="utf-8")
    key = _bib_key_for(KNOWN_ID, refs)
    assert key is not None, "expected {} to be present in refs.bib".format(KNOWN_ID)
    _out, body = _run_subprocess()
    # Accept \citep{key} possibly among a comma-separated list.
    pattern = re.compile(r"\\citep?\{[^}]*" + re.escape(key) + r"[^}]*\}")
    assert pattern.search(body), (
        "expected \\citep{{{key}}} in body.tex".format(key=key)
    )


def test_unknown_citation_remains_visible_and_is_reported():
    """An arXiv id absent from refs.bib stays visible and is reported as unmatched."""
    refs = REFS.read_text(encoding="utf-8")
    assert _bib_key_for(UNKNOWN_ID, refs) is None, "test fixture must be unmatched"

    out, body, mod = _run_in_process()
    marker = "arXiv:" + UNKNOWN_ID
    assert marker in body, "unmatched marker disappeared from body.tex"

    reported = (marker in out) or any(
        k in out.lower()
        for k in ("unmatch", "unresolved", "unknown", "no matching", "no bib",
                  "not found", "missing", "no key", "no entry", "warn", "could not")
    )
    globals_reported = False
    for name, obj in vars(mod).items():
        items = []
        if isinstance(obj, dict):
            items = list(obj.keys()) + list(obj.values())
        elif isinstance(obj, (list, set, tuple)):
            items = list(obj)
        elif isinstance(obj, str):
            items = [obj]
        if any(UNKNOWN_ID in str(x) for x in items):
            globals_reported = True
            break
    assert reported or globals_reported, (
        "unmatched marker was not reported in output or module state; output=\n" + out
    )


# --------------------------------------------------------------------------- figure labels


def test_figure_labels_unique():
    """Generated figure labels must be unique; fig:main-accuracy no longer duplicated."""
    _out, body = _run_subprocess()
    labels = re.findall(r"\\label\{(fig:[^}]*)\}", body)
    assert labels, "no generated figure labels found in body.tex"
    assert len(labels) == len(set(labels)), (
        "duplicate figure labels: " + repr(labels)
    )
    assert body.count("\\label{fig:main-accuracy}") <= 1, (
        "fig:main-accuracy still duplicated: " + str(body.count("\\label{fig:main-accuracy}"))
    )


def main():
    tests = [
        test_number_preservation,
        test_known_arxiv_citation_becomes_citep,
        test_unknown_citation_remains_visible_and_is_reported,
        test_figure_labels_unique,
    ]
    failures = []
    for t in tests:
        try:
            t()
            print("PASS: " + t.__name__)
        except AssertionError as exc:
            failures.append((t.__name__, str(exc)))
            print("FAIL: " + t.__name__ + ": " + str(exc))
    if failures:
        print("FAILURES: " + str(len(failures)))
        return 1
    print("PASS: all tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())