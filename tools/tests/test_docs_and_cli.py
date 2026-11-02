"""Drift tests: the documentation, the CLIs and the files on disk must agree.

These tests are deliberately *not* unit tests of tool behaviour (each tool has
its own behavioural suite).  They exist so that the written contract cannot rot
quietly as the repo changes:

  1. every tool answers ``--help`` (discovered by globbing, so a new tool cannot
     skip the check);
  2. bad usage exits 2, per CONTRACTS.md section 6;
  3. every repo-path backticked in tools/README.md / tools/CONTRACTS.md exists;
  4. the formats described in CONTRACTS.md sections 1-5 match real files;
  5. toy artefacts stay labelled as toy and never leak into the paper tree;
  6. the Phase-2 gate cannot release itself on a passing mention.

Read-only apart from pytest's tmp_path.  No network, no experiment runs, no
compilation: only ``--help``, argument-parsing errors, and files already on
disk.  When an assertion fails, the message names the file and the fix.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
TIMEOUT = 60  # generous; --help on this toolchain takes ~0.2 s

DOC_SUFFIXES = (".py", ".md", ".json", ".csv", ".bib", ".tex", ".sh")


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def _run(rel: str, *args: str) -> subprocess.CompletedProcess:
    """Run a repo-relative script with the same interpreter as pytest."""
    return subprocess.run(
        [sys.executable, str(REPO / rel), *args],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=TIMEOUT,
    )


def _output(proc: subprocess.CompletedProcess) -> str:
    return (proc.stdout or "") + (proc.stderr or "")


def _rel(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def _has_argparse(path: Path) -> bool:
    return re.search(r"^\s*import argparse|^\s*from argparse import", path.read_text(
        encoding="utf-8", errors="replace"), re.MULTILINE) is not None


# Directories searched for tools.  Deliberately shallow (``*.py``, not
# ``**/*.py``) so that package support code, test packages and __pycache__ are
# not mistaken for tools: tools/lib/, 04_experiments/harness/tests/ and
# 05_paper/template/tests/ are excluded by construction.
TOOL_DIRS = (
    "tools",
    "04_experiments/harness",
    "04_experiments/toy",
    "05_paper/template/figures",
    "05_paper/template/tables",
    "05_paper/template/tools",
)


def _discover_tools() -> list[str]:
    found: list[str] = []
    for d in TOOL_DIRS:
        for p in sorted((REPO / d).glob("*.py")):
            found.append(_rel(p))
    return found


ALL_SCRIPTS = _discover_tools()

# Scripts that legitimately have NO command-line interface: they are libraries
# you import.  Each has only a ``__main__`` smoke hook (or none at all); the
# guard test below proves the claim by checking they never import argparse, so
# adding a CLI to one of them fails this suite until the entry is moved out.
LIBRARY_MODULES = {
    "04_experiments/harness/stats.py":
        "library: bootstrap CIs / paired tests / effects; __main__ prints a smoke sample",
    "04_experiments/harness/tables.py":
        "library: ablation table builder; __main__ is a manual smoke hook that takes "
        "a summary path, not argparse (so `--help` is not supported by design)",
    "04_experiments/toy/task.py":
        "library: the toy task/fixture generator; imported by run_toy.py",
}

CLI_TOOLS = [p for p in ALL_SCRIPTS if p not in LIBRARY_MODULES]

# Required-argument map, read off each tool's ``--help`` usage line
# (``[--opt]`` = optional, bare ``--opt`` = required).  ``base`` is a set of
# arguments that satisfies the parser, used only to reach the "unknown flag"
# branch of argparse; the values are never opened because parsing fails first.
# ``required`` is empty for tools whose every option has a default.
CLI_SPEC: dict[str, dict[str, list[str]]] = {
    "tools/verify_citations.py": {
        "required": [],  # --csv defaults to 02_literature/citations.csv
        "base": [],
    },
    "tools/check_all.py": {  # runs the whole toolchain; never invoke without a flag
        "required": [],
        "base": [],
    },
    "tools/check_numbers.py": {
        "required": ["--draft"],
        "base": ["--draft", "NOPE-drift.md"],
    },
    "tools/claims_audit.py": {
        "required": ["--audit", "--draft", "--index", "--citations"],
        "base": ["--audit", "NOPE-drift.md", "--draft", "NOPE-drift.md",
                 "--index", "NOPE-drift.json", "--citations", "NOPE-drift.csv"],
    },
    "tools/originality_check.py": {
        "required": ["--draft", "--corpus"],
        "base": ["--draft", "NOPE-drift.md", "--corpus", "NOPE-drift"],
    },
    "tools/simulate_review.py": {
        "required": ["subcommand"],  # {pack,ingest,aggregate,compare}
        "base": ["pack"],
    },
    "tools/make_digest.py": {  # --section required unless --check DIGEST
        "required": ["--section"],
        "base": ["--section", "NOPE-drift.md"],
    },
    "04_experiments/harness/runner.py": {
        "required": ["--config"],
        "base": ["--config", "NOPE-drift.json"],
    },
    "04_experiments/harness/lock.py": {
        "required": ["subcommand"],  # {status,acquire,release}
        "base": ["status"],
    },
    "04_experiments/harness/aggregate.py": {
        "required": ["--experiment"],
        "base": ["--experiment", "nope"],
    },
    "05_paper/template/figures/make_figures.py": {
        "required": ["--figure"],  # plus one of --index / --results
        "base": ["--index", "NOPE-drift.json", "--figure", "x"],
    },
    "05_paper/template/tables/make_tables.py": {
        "required": ["--summary", "--name"],
        "base": ["--summary", "NOPE-drift.json", "--name", "x"],
    },
    "05_paper/template/tools/citations_to_bib.py": {
        "required": ["--csv", "--out"],
        "base": ["--csv", "NOPE-drift.csv", "--out", "NOPE-drift.bib"],
    },
    "04_experiments/toy/run_pipeline.py": {
        "required": [],
        "base": [],
    },
    "04_experiments/toy/run_toy.py": {
        "required": [],
        "base": [],
    },
}

TOOLS_WITH_REQUIRED_ARGS = sorted(k for k, v in CLI_SPEC.items() if v["required"])


# --- documentation path extraction -----------------------------------------

# Files a tool writes on demand (they may legitimately be absent until the tool
# is run with that output enabled).  Every entry says which code writes it.
TOOL_OUTPUT_ALLOWLIST = {
    "02_literature/verification_report.json":
        "written by tools/verify_citations.py (write_report_json) when a run writes "
        "outputs; the last run/writer did not leave one behind",
    "02_literature/verification_report.md":
        "written by tools/verify_citations.py (write_report_md), same reason",
}

# Paths the docs use as *example inputs* that no tool produces.  They are absent
# because the artefact is authored, not generated, and the project has no
# approved topic yet (Phase 2 locked, 03_topics/ empty, 05_paper/draft/ absent).
# Kept as an exact list (not a prefix) so any *other* stale path still fails.
AUTHOR_INPUT_ALLOWLIST = {
    "02_literature/citations.csv":
        "CONTRACTS section 1 input: the rows the author wants to verify; S2 stages "
        "them under 02_literature/staging/ instead, so the contract path is unused",
    "06_review/CLAIMS-AUDIT.md":
        "claims_audit.py --audit input, authored by hand; only "
        "06_review/CLAIMS-AUDIT-TEMPLATE.md exists so far",
    "05_paper/draft/method.md":
        "draft section, authored after the head approves a topic; 05_paper/draft/ "
        "does not exist yet (only 05_paper/template/)",
}

ALLOWED_ABSENT = {**TOOL_OUTPUT_ALLOWLIST, **AUTHOR_INPUT_ALLOWLIST}


def _tokens_from_backticks(text: str) -> list[str]:
    """Repo-relative file tokens inside `single backticks`."""
    out: list[str] = []
    for span in re.findall(r"`([^`\n]+)`", text):
        for tok in re.split(r"[\s,()\[\]{}|]+", span):
            tok = tok.strip("'\"`.,;:")
            if not tok or tok.startswith("-"):
                continue
            if "<" in tok or ">" in tok or "*" in tok:  # placeholders
                continue
            if "/" not in tok:
                continue
            if not tok.endswith(DOC_SUFFIXES):
                continue
            out.append(tok)
    seen: dict[str, None] = {}
    for t in out:
        seen.setdefault(t, None)
    return list(seen)


def _contracts_section(low: int, high: int) -> str:
    """Slice tools/CONTRACTS.md between '## <low>.' and '## <high>.'."""
    text = (REPO / "tools/CONTRACTS.md").read_text(encoding="utf-8")
    start = re.search(rf"^## {low}\.", text, re.MULTILINE)
    end = re.search(rf"^## {high}\.", text, re.MULTILINE)
    assert start, f"CONTRACTS.md has no section '## {low}.'"
    assert end, f"CONTRACTS.md has no section '## {high}.' - renumbering breaks this test"
    return text[start.start():end.start()]


def _resolve_token(tok: str, doc: Path) -> Path | None:
    """Resolve a documented path relative to repo root, then to the doc's dir.

    tools/README.md writes support modules as ``lib/netcache.py``, i.e. relative
    to tools/, while CONTRACTS paths are repo-relative; both readings are legal,
    so a token exists if either resolves.
    """
    for base in (REPO, doc.parent):
        cand = base / tok
        if cand.exists():
            return cand
    return None


# --------------------------------------------------------------------------
# 1. every tool answers --help and exits 0
# --------------------------------------------------------------------------

@pytest.mark.parametrize("rel", CLI_TOOLS, ids=CLI_TOOLS)
def test_tool_help_exits_zero(rel: str) -> None:
    proc = _run(rel, "--help")
    out = _output(proc)
    assert proc.returncode == 0, (
        f"{rel} --help exited {proc.returncode}, expected 0 (CONTRACTS section 6). "
        f"Output tail:\n{out[-800:]}"
    )
    lines = [ln for ln in out.splitlines() if ln.strip()]
    assert len(lines) >= 5, (
        f"{rel} --help printed only {len(lines)} non-empty line(s); a help screen "
        f"must document its usage. Got:\n{out}"
    )
    stem = Path(rel).stem
    assert stem in out or "--" in out, (
        f"{rel} --help neither names the tool ({stem}) nor lists an --option. "
        f"Got:\n{out}"
    )


def test_every_discovered_script_is_classified() -> None:
    """A new tool cannot skip the checks by not being in CLI_SPEC."""
    missing = [p for p in CLI_TOOLS if p not in CLI_SPEC]
    assert not missing, (
        "new tool(s) discovered but not covered by CLI_SPEC: "
        f"{missing}. Add required args / base args to CLI_SPEC in this file so the "
        "--help and exit-code-2 contracts are tested for them too."
    )
    stale = [p for p in CLI_SPEC if p not in ALL_SCRIPTS]
    assert not stale, f"CLI_SPEC lists scripts that no longer exist: {stale}"


def test_library_allowlist_is_truthful() -> None:
    """Every 'no CLI' exemption really has no CLI."""
    for rel, reason in LIBRARY_MODULES.items():
        path = REPO / rel
        assert path.is_file(), f"allowlisted library {rel} does not exist - remove it"
        assert not _has_argparse(path), (
            f"{rel} now imports argparse, so it does have a CLI; drop it from "
            f"LIBRARY_MODULES and add it to CLI_SPEC. (Recorded reason: {reason})"
        )


# --------------------------------------------------------------------------
# 2. exit code 2 on bad usage (CONTRACTS.md section 6)
# --------------------------------------------------------------------------

@pytest.mark.parametrize("rel", TOOLS_WITH_REQUIRED_ARGS, ids=TOOLS_WITH_REQUIRED_ARGS)
def test_exit_2_when_required_argument_missing(rel: str) -> None:
    proc = _run(rel)  # no arguments at all
    assert proc.returncode == 2, (
        f"{rel} with a required argument missing exited {proc.returncode}, "
        f"expected 2 (usage error, CONTRACTS section 6). 0 or 1 would let a "
        f"broken invocation look like a pass or like findings. Output tail:\n"
        f"{_output(proc)[-600:]}"
    )


@pytest.mark.parametrize("rel", CLI_TOOLS, ids=CLI_TOOLS)
def test_exit_2_on_unknown_flag(rel: str) -> None:
    base = CLI_SPEC[rel]["base"]
    proc = _run(rel, *base, "--definitely-not-a-real-flag")
    assert proc.returncode == 2, (
        f"{rel} {' '.join(base + ['--definitely-not-a-real-flag'])} exited "
        f"{proc.returncode}, expected 2. A tool that silently swallows an unknown "
        f"flag is worse than one that crashes. Output tail:\n{_output(proc)[-600:]}"
    )


# --------------------------------------------------------------------------
# 3. documented paths exist
# --------------------------------------------------------------------------

@pytest.mark.parametrize("doc_name", ["tools/README.md", "tools/CONTRACTS.md"])
def test_documented_paths_exist(doc_name: str) -> None:
    doc = REPO / doc_name
    tokens = _tokens_from_backticks(doc.read_text(encoding="utf-8"))
    assert tokens, f"no repo-relative paths parsed out of {doc_name} - parser drifted"

    missing = []
    for tok in tokens:
        if _resolve_token(tok, doc) is not None:
            continue
        if tok in ALLOWED_ABSENT:
            continue
        missing.append(tok)
    assert not missing, (
        f"{doc_name} documents path(s) that do not exist on disk and are not "
        f"allowlisted: {missing}. Either the doc is stale or the file was "
        f"deleted; fix one of the two (this test must not be widened silently - "
        f"add an entry to TOOL_OUTPUT_ALLOWLIST/AUTHOR_INPUT_ALLOWLIST only if the "
        f"path is genuinely created on demand)."
    )


def test_allowlisted_absences_still_documented() -> None:
    """The allowlists must not outlive the line they excuse.

    Matched on the file name, because CONTRACTS writes
    ``02_literature/verification_report.json`` in full but only
    ``verification_report.md`` for its twin.
    """
    both = (REPO / "tools/README.md").read_text(encoding="utf-8") + \
           (REPO / "tools/CONTRACTS.md").read_text(encoding="utf-8")
    dead = [p for p in ALLOWED_ABSENT if p not in both and Path(p).name not in both]
    assert not dead, (
        f"allowlist entries no longer mentioned by the docs: {dead}; delete them "
        f"so the allowlist cannot accumulate stale permission"
    )


def test_readme_tool_table_entries_exist() -> None:
    text = (REPO / "tools/README.md").read_text(encoding="utf-8")
    entries = re.findall(r"^\|\s*`([A-Za-z0-9_]+\.py)`\s*\|", text, re.MULTILINE)
    assert len(entries) >= 6, f"README tool table parsed only {entries}"
    absent = [n for n in entries if not (REPO / "tools" / n).is_file()]
    assert not absent, (
        f"tools/README.md advertises tool(s) that do not exist: {absent}. "
        f"Each row of the table must name a real file in tools/."
    )


def test_readme_json_flag_claim() -> None:
    """tools/README.md line 4-5: 'exit code ... and `--json` on all of them'.

    "all of them" is the six tools in the table below that line, so each must
    advertise --json in its own help.
    """
    text = (REPO / "tools/README.md").read_text(encoding="utf-8")
    entries = re.findall(r"^\|\s*`([A-Za-z0-9_]+\.py)`\s*\|", text, re.MULTILINE)
    missing = []
    for name in entries:
        rel = f"tools/{name}"
        if not (REPO / rel).is_file():
            continue  # reported by test_readme_tool_table_entries_exist
        proc = _run(rel, "--help")
        blob = _output(proc)
        if "--json" not in blob and "[--json]" not in blob:
            missing.append(rel)
    assert not missing, (
        f"tools/README.md claims '`--json` on all of them', but {missing} has no "
        "--json option (checked in --help). Either add the flag or scope the "
        "README sentence to the tools that have one."
    )


# --------------------------------------------------------------------------
# 4. cross-file path + schema truth (CONTRACTS.md sections 1-5)
# --------------------------------------------------------------------------

def test_contracts_section_paths_exist() -> None:
    section = _contracts_section(1, 6)
    doc = REPO / "tools/CONTRACTS.md"
    tokens = _tokens_from_backticks(section)
    assert "02_literature/verified_citations.csv" in tokens, (
        f"section 1-5 path parser found {tokens}; it must at least see the two "
        f"paths the contract is built around"
    )
    assert "04_experiments/RESULTS-INDEX.json" in tokens
    missing = [t for t in tokens
               if _resolve_token(t, doc) is None and t not in ALLOWED_ABSENT]
    assert not missing, (
        f"CONTRACTS.md sections 1-5 reference missing path(s): {missing}. The "
        f"contract says these are the canonical locations; a tool following it "
        f"would fail on a fresh checkout."
    )


def test_contracts_s2_results_json_keys_are_real() -> None:
    section = _contracts_section(2, 3)
    blocks = re.findall(r"```json\n(.*?)```", section, re.DOTALL)
    documented = None
    for block in blocks:
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict) and "_meta" in data:
            documented = data
            break
    assert documented is not None, (
        "could not find the results.json example (a ```json block with a _meta "
        "key) in CONTRACTS.md section 2"
    )

    runs = sorted((REPO / "04_experiments/runs").glob("*/results.json"))
    assert runs, (
        "no 04_experiments/runs/*/results.json on disk, so the documented "
        "results.json shape cannot be checked against anything real"
    )
    top: set[str] = set()
    meta: set[str] = set()
    for path in runs:
        data = json.loads(path.read_text(encoding="utf-8"))
        top |= set(data)
        meta |= set(data.get("_meta") or {})

    want_top = {k for k in documented if k != "_meta"}
    want_meta = set(documented.get("_meta") or {})
    absent_top = sorted(want_top - top)
    absent_meta = sorted(want_meta - meta)
    assert not absent_top and not absent_meta, (
        "CONTRACTS.md section 2 documents results.json keys that no real run "
        f"writes: top-level {absent_top}, _meta {absent_meta}. Documented keys: "
        f"top={sorted(want_top)} _meta={sorted(want_meta)}. Writes seen across "
        f"{len(runs)} run(s): top={sorted(top)} _meta={sorted(meta)}. Either the "
        "harness must write them or the example must drop them."
    )


# --- 4b. section 1 output columns vs the file on disk ----------------------

def test_contracts_s1_verified_citations_columns() -> None:
    """CONTRACTS section 1 fixes the verified_citations.csv columns.

    Consumers rely on them: citations_to_bib.py refuses a file with no `status`
    column, claims_audit.py maps key -> status, make_digest.py reads `key`.
    """
    section = _contracts_section(1, 2)
    match = re.search(
        r"Output `02_literature/verified_citations\.csv`.*?```\n([^\n]+)\n```",
        section, re.DOTALL,
    )
    assert match, "CONTRACTS.md section 1 no longer shows the output CSV header"
    documented = [c.strip() for c in match.group(1).split(",")]

    real_path = REPO / "02_literature/verified_citations.csv"
    assert real_path.is_file(), f"{real_path} is missing"
    header = real_path.read_text(encoding="utf-8").splitlines()[0]
    actual = [c.strip() for c in header.split(",")]

    if actual != documented:
        absent = [c for c in documented if c not in actual]
        extra = [c for c in actual if c not in documented]
        pytest.fail(
            "CONTRACTS.md section 1 documents columns "
            f"{documented}\nbut {real_path.relative_to(REPO).as_posix()} has "
            f"{actual}\n  documented but absent on disk: {absent}\n"
            f"  on disk but undocumented:   {extra}\n"
            "Consequence, measured today: citations_to_bib.py exits 2 "
            "('lacks required column(s): key'); claims_audit.py builds its "
            "key->status map from these columns, so all rows collapse to one "
            "empty key and no citation can read as VERIFIED (266 rows unusable).\n"
            "Fix one side: (a) write the file with the section-1 columns - "
            "`python tools/verify_citations.py --csv <input.csv> --online` - or "
            "(b) amend section 1 and every consumer to the 9-column schema that "
            "02_literature/tools/verify_citations.py add writes."
        )


# --------------------------------------------------------------------------
# 5. toy artefacts are labelled where it matters
# --------------------------------------------------------------------------

def test_toy_readme_starts_with_banner() -> None:
    readme = REPO / "04_experiments/toy/README.md"
    assert readme.is_file(), f"{readme} is missing"
    first = readme.read_text(encoding="utf-8").splitlines()[0]
    assert first.strip() == "TOY - NOT A RESULT", (
        f"04_experiments/toy/README.md must begin with 'TOY - NOT A RESULT' on "
        f"line 1; found {first!r}. A banner further down is not a banner."
    )


def _contains_true_toy(node) -> bool:
    if isinstance(node, dict):
        if node.get("toy") is True:
            return True
        return any(_contains_true_toy(v) for v in node.values())
    if isinstance(node, list):
        return any(_contains_true_toy(v) for v in node)
    return False


def test_toy_json_artefacts_carry_toy_true() -> None:
    """CONTRACTS section 5: every JSON under toy/ and results/ is marked toy.

    While Phase 2 is locked, results/ may only hold toy artefacts; once the head
    approves a topic (see test_phase2_gate_is_not_self_releasing) a real
    summary_<experiment>.json is legitimate, so from then on only toy-named
    files are required to carry the flag.
    """
    gate_open = _gate_open()
    unmarked: list[str] = []
    for root in ("04_experiments/toy", "04_experiments/results"):
        for path in sorted((REPO / root).rglob("*.json")):
            rel = _rel(path)
            if gate_open and "toy" not in rel.lower():
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:  # a toy file that cannot be read
                unmarked.append(f"{rel} (invalid JSON: {exc})")
                continue
            if not _contains_true_toy(data):
                unmarked.append(rel)
    assert not unmarked, (
        f"toy JSON without a \"toy\": true marker: {unmarked}. Section 5 requires "
        f"the flag so make_tables.py / check_numbers.py / make_figures.py can "
        f"refuse the numbers by default."
    )


TOY_NUMBER_RE = re.compile(r"\d+\.\d+|\d+\s*%")
TOY_WORD_RE = re.compile(r"\b(toy|TOY)\b")


def test_paper_tree_has_no_toy_result_numbers() -> None:
    """No file under 05_paper/template/ or 05_paper/draft/ may present a toy
    number as a result: a line that both talks about toy output and carries a
    decimal/percentage number is exactly the leak this guards."""
    hits: list[str] = []
    for root in ("05_paper/template", "05_paper/draft"):
        base = REPO / root
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in {
                ".md", ".tex", ".bib", ".csv", ".txt", ".json",
            }:
                continue
            for lineno, line in enumerate(
                path.read_text(encoding="utf-8", errors="replace").splitlines(), 1
            ):
                if TOY_WORD_RE.search(line) and TOY_NUMBER_RE.search(line):
                    hits.append(f"{_rel(path)}:{lineno}: {line.strip()[:120]}")
    assert not hits, (
        "paper tree contains a toy number presented as a result:\n  "
        + "\n  ".join(hits)
        + "\nToy numbers may not appear in a draft (RULES.md #1/#2, CONTRACTS "
          "section 5) except as an explicit refusal note with no number."
    )


# --------------------------------------------------------------------------
# 6. the Phase-2 gate is not self-releasing
# --------------------------------------------------------------------------

APPROVAL_LINE = "TOPIC APPROVED"


def _has_approval_line(text: str) -> bool:
    """True only for a line that is exactly the approval token.

    A mention inside a sentence - including the one that explains the rule, and
    a backticked `TOPIC APPROVED` - must not count: that is the trap that would
    let an unapproved experiment run.
    """
    return any(line.strip() == APPROVAL_LINE for line in text.splitlines())


def _gate_open() -> bool:
    selected = REPO / "03_topics" / "SELECTED.md"
    head = REPO / "orchestration" / "HEAD-REVIEW.md"
    if not selected.exists() or not head.is_file():
        return False
    return _has_approval_line(head.read_text(encoding="utf-8", errors="replace"))


def test_phase2_gate_is_not_self_releasing() -> None:
    selected = REPO / "03_topics" / "SELECTED.md"
    head = REPO / "orchestration" / "HEAD-REVIEW.md"
    assert head.is_file(), "orchestration/HEAD-REVIEW.md is missing - the gate has no record"

    text = head.read_text(encoding="utf-8", errors="replace")
    approved = _has_approval_line(text)

    if selected.exists():
        assert approved, (
            f"03_topics/SELECTED.md exists but orchestration/HEAD-REVIEW.md has no "
            f"line that is exactly '{APPROVAL_LINE}'. Selection is not approval "
            f"(orchestration/DIRECTIVES.md, S2 item 3)."
        )
    else:
        assert not approved, (
            f"orchestration/HEAD-REVIEW.md carries a bare '{APPROVAL_LINE}' line "
            f"while 03_topics/SELECTED.md does not exist: approval of a topic "
            f"nobody selected. Remove the line or land SELECTED.md first."
        )


def test_approval_detector_rejects_a_mention(tmp_path: Path) -> None:
    """Self-test of the detector: a sentence mention is not approval."""
    sentence = (
        "# HEAD-REVIEW\n"
        "Phase 2 stays LOCKED. This file does not yet contain the approval line.\n"
        "- the head reads them, then writes `TOPIC APPROVED` (or a veto) here.\n"
    )
    assert not _has_approval_line(sentence)
    assert not _has_approval_line(sentence + "pre-TOPIC APPROVED-post\n")
    assert _has_approval_line(sentence + "TOPIC APPROVED\n")
    assert _has_approval_line("TOPIC APPROVED\r\n")  # CRLF on Windows
    assert _has_approval_line("   TOPIC APPROVED   \n")  # stray indentation

    probe = tmp_path / "HEAD-REVIEW.md"
    probe.write_text(sentence, encoding="utf-8")
    assert not _has_approval_line(probe.read_text(encoding="utf-8"))
