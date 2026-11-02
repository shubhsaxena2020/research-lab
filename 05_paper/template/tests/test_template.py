"""Tests for the venue-agnostic paper template.

What this suite is for: it is the only "compile check" available in an
environment without LaTeX. It asserts the structural properties that a broken
build would otherwise reveal late -- unbalanced braces, a stray \\end, a \\ref
with no \\label, a non-empty refs.bib -- and it runs both generators end to end
against fixture results, including their refusal paths.

Run:
    python -m pytest 05_paper/template/tests -q
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent
REPO = TEMPLATE.parents[1]
FIXTURES = HERE / "fixtures"
FIGURES = TEMPLATE / "figures" / "make_figures.py"
TABLES = TEMPLATE / "tables" / "make_tables.py"
CITE2BIB = TEMPLATE / "tools" / "citations_to_bib.py"

sys.path.insert(0, str(REPO / "tools"))
from lib import bibtex_min  # noqa: E402  (repo's own read-only parser)

TEX_FILES = sorted(TEMPLATE.rglob("*.tex"))


# -----------------------------------------------------------------------------
# helpers
# -----------------------------------------------------------------------------
def strip_tex_comments(text: str) -> str:
    """Remove % comments, respecting \\% and other escaped characters."""
    out_lines = []
    for line in text.splitlines():
        res = []
        i = 0
        while i < len(line):
            ch = line[i]
            if ch == "\\" and i + 1 < len(line):
                res.append(line[i:i + 2])
                i += 2
                continue
            if ch == "%":
                break
            res.append(ch)
            i += 1
        out_lines.append("".join(res))
    return "\n".join(out_lines)


def run(script: Path, *args, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(script), *[str(a) for a in args]],
        capture_output=True, text=True, cwd=str(cwd or TEMPLATE), timeout=120,
    )


def write_json(path: Path, payload: dict) -> Path:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


# -----------------------------------------------------------------------------
# 1. LaTeX structure
# -----------------------------------------------------------------------------
def test_tex_files_exist():
    names = {p.relative_to(TEMPLATE).as_posix() for p in TEX_FILES}
    assert {"main.tex", "ieee/main.tex", "acl/main.tex"} <= names


@pytest.mark.parametrize("tex", TEX_FILES, ids=lambda p: p.relative_to(TEMPLATE).as_posix())
def test_balanced_braces(tex: Path):
    text = strip_tex_comments(tex.read_text(encoding="utf-8"))
    text = re.sub(r"\\[{}]", "", text)          # \{ and \} are literal characters
    text = text.replace("\\\\", "")             # line breaks are not group delimiters
    depth = 0
    for lineno, line in enumerate(text.splitlines(), start=1):
        for ch in line:
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                assert depth >= 0, f"{tex.name}:{lineno}: unmatched closing brace"
    assert depth == 0, f"{tex.name}: {depth} unclosed opening brace(s)"


@pytest.mark.parametrize("tex", TEX_FILES, ids=lambda p: p.relative_to(TEMPLATE).as_posix())
def test_balanced_environments(tex: Path):
    text = strip_tex_comments(tex.read_text(encoding="utf-8"))
    stack: list[tuple[str, int]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for match in re.finditer(r"\\(begin|end)\{([^}]+)\}", line):
            kind, env = match.group(1), match.group(2)
            if kind == "begin":
                stack.append((env, lineno))
            else:
                assert stack, f"{tex.name}:{lineno}: \\end{{{env}}} with nothing open"
                open_env, open_line = stack.pop()
                assert open_env == env, (
                    f"{tex.name}:{lineno}: \\end{{{env}}} closes \\begin{{{open_env}}} "
                    f"from line {open_line}")
    assert not stack, f"{tex.name}: unclosed environments {[e for e, _ in stack]}"


def test_every_ref_has_a_label():
    labels: set[str] = set()
    refs: list[tuple[str, str]] = []
    for tex in TEX_FILES:
        text = strip_tex_comments(tex.read_text(encoding="utf-8"))
        labels.update(re.findall(r"\\label\{([^}]+)\}", text))
        refs.extend((tex.name, r) for r in re.findall(r"\\ref\{([^}]+)\}", text))
    missing = sorted({(f, r) for f, r in refs if r not in labels})
    assert not missing, f"\\ref targets with no \\label: {missing}"
    assert refs, "expected the skeleton to demonstrate cross-references"


def test_main_tex_section_skeleton_and_wiring():
    text = (TEMPLATE / "main.tex").read_text(encoding="utf-8")
    for section in ("Introduction", "Related Work", "Method", "Experiments",
                    "Results", "Limitations", "Ethics Statement",
                    "Reproducibility Statement", "Conclusion"):
        assert re.search(r"\\section\{" + re.escape(section) + r"\}", text), \
            f"missing section: {section}"
    assert r"\begin{abstract}" in text and r"\end{abstract}" in text
    assert r"\bibliography{refs}" in text
    assert "booktabs" in text
    # the table and figure must come from generated files, guarded so a fresh
    # clone still compiles
    assert r"\input{tables/generated/main-results.tex}" in text
    assert r"\input{figures/generated/main-accuracy.tex}" in text
    assert text.count(r"\IfFileExists") >= 2
    assert r"\label{tab:main-results}" in text
    assert r"\label{fig:main-accuracy}" in text


def test_ai_disclosure_present_in_every_skeleton():
    for rel in ("main.tex", "ieee/main.tex", "acl/main.tex"):
        text = (TEMPLATE / rel).read_text(encoding="utf-8")
        assert "Use of AI tools" in text, f"{rel}: no AI-disclosure footnote"
        assert "policy" in text.lower(), f"{rel}: disclosure does not reference the venue policy"
        assert r"\thanks" in text, f"{rel}: disclosure is not in the author block"


# -----------------------------------------------------------------------------
# 2. refs.bib
# -----------------------------------------------------------------------------
def test_refs_bib_parses_to_zero_active_entries():
    raw = (TEMPLATE / "refs.bib").read_text(encoding="utf-8")
    active = "\n".join(line for line in raw.splitlines()
                       if not line.lstrip().startswith("%"))
    entries = bibtex_min.parse_bibtex(active)
    assert entries == [], f"refs.bib must ship empty, found {len(entries)} active entries"


def test_refs_bib_documents_its_only_legal_source():
    raw = (TEMPLATE / "refs.bib").read_text(encoding="utf-8")
    assert "02_literature/verified_citations.csv" in raw
    assert "RULES.md #1" in raw
    assert raw.count("example - not a real reference, do not uncomment") >= 2


def test_refs_bib_examples_are_parseable_when_uncommented():
    """The examples must be valid BibTeX, or they teach the wrong shape."""
    raw = (TEMPLATE / "refs.bib").read_text(encoding="utf-8")
    body = []
    for line in raw.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("%"):
            candidate = stripped[1:]
            if candidate.startswith(" "):
                candidate = candidate[1:]
            body.append(candidate)
    entries = bibtex_min.parse_bibtex("\n".join(body))
    # header prose may contain no '@'; only the three examples should parse
    assert len(entries) == 3, [e.get("key") for e in entries]
    for entry in entries:
        assert entry.get("title"), entry
        assert entry.get("key")


# -----------------------------------------------------------------------------
# 3. figure generator
# -----------------------------------------------------------------------------
def test_make_figures_from_index(tmp_path: Path):
    out = tmp_path / "fig"
    result = run(FIGURES, "--index", FIXTURES / "fixture_index.json",
                 "--figure", "main-accuracy", "--out-dir", out)
    assert result.returncode == 0, result.stderr
    for suffix in (".csv", ".svg", ".tex"):
        path = out / f"main-accuracy{suffix}"
        assert path.is_file(), f"missing {path}"
        assert path.stat().st_size > 0

    rows = (out / "main-accuracy.csv").read_text(encoding="utf-8").splitlines()
    assert rows[0].startswith("series,value,id,key,file")
    assert len(rows) == 3  # header + 2 entries

    tree = ET.parse(out / "main-accuracy.svg")
    root = tree.getroot()
    assert root.tag.endswith("svg")
    tags = [el.tag.split("}")[-1] for el in root.iter()]
    assert tags.count("text") >= 5, "SVG has no axis/tick labels"
    assert "line" in tags, "SVG has no axes"
    assert any("title" == t for t in tags), "SVG has no accessible title"
    # the plotted values must be visible in the SVG, not just in the CSV
    svg_text = (out / "main-accuracy.svg").read_text(encoding="utf-8")
    assert "0.812" in svg_text and "0.91" in svg_text

    tex = (out / "main-accuracy.tex").read_text(encoding="utf-8")
    assert r"\includegraphics" in tex and r"\IfFileExists" in tex
    assert "fig:main-accuracy" in tex, "fragment does not name its label"
    assert r"\begin{figure}" not in tex, "fragment must be float body only; main.tex owns the float"
    assert str(out.as_posix()) in tex, "fragment does not point at its own output dir"
    # the generated LaTeX must itself be structurally valid
    stripped = strip_tex_comments(tex).replace("\\\\", "")
    depth = 0
    for ch in stripped:
        depth += ch == "{"
        depth -= ch == "}"
        assert depth >= 0, "generated figure fragment closes a brace it never opened"
    assert depth == 0, "generated figure fragment has unbalanced braces"


def test_make_figures_from_results_file(tmp_path: Path):
    out = tmp_path / "fig2"
    result = run(FIGURES, "--results", FIXTURES / "fixture_results.json",
                 "--figure", "smoke", "--metric", "accuracy", "f1_macro",
                 "--out-dir", out)
    assert result.returncode == 0, result.stderr
    rows = (out / "smoke.csv").read_text(encoding="utf-8").strip().splitlines()
    assert len(rows) == 3
    ET.parse(out / "smoke.svg")


def test_make_figures_refuses_missing_metric(tmp_path: Path):
    out = tmp_path / "fig3"
    result = run(FIGURES, "--results", FIXTURES / "fixture_results.json",
                 "--figure", "broken", "--metric", "accuracy", "not_a_metric",
                 "--out-dir", out)
    assert result.returncode == 2, result.stdout
    assert "not_a_metric" in result.stderr
    assert not (out / "broken.svg").exists(), "an empty chart was written anyway"


def test_make_figures_refuses_missing_index_key(tmp_path: Path):
    index = write_json(tmp_path / "index.json", {
        "version": 1,
        "entries": [{"id": "ghost.run1", "file": str(FIXTURES / "fixture_results.json"),
                     "key": "metric_that_does_not_exist", "description": "broken"}],
    })
    result = run(FIGURES, "--index", index, "--figure", "ghost",
                 "--out-dir", tmp_path / "fig4")
    assert result.returncode == 2
    assert "metric_that_does_not_exist" in result.stderr


def test_make_figures_refuses_unknown_figure(tmp_path: Path):
    result = run(FIGURES, "--index", FIXTURES / "fixture_index.json",
                 "--figure", "no-such-figure", "--out-dir", tmp_path / "fig5")
    assert result.returncode == 2
    assert "records" in result.stderr or "no index entry matches" in result.stderr


def test_make_figures_refuses_toy_files(tmp_path: Path):
    result = run(FIGURES, "--index", FIXTURES / "fixture_index.json",
                 "--figure", "toy-accuracy", "--out-dir", tmp_path / "fig6")
    assert result.returncode == 2
    assert "TOY" in result.stderr
    assert not (tmp_path / "fig6" / "toy-accuracy.svg").exists()


# -----------------------------------------------------------------------------
# 4. table generator
# -----------------------------------------------------------------------------
def test_make_tables_end_to_end(tmp_path: Path):
    out = tmp_path / "tab"
    result = run(TABLES, "--summary", FIXTURES / "fixture_summary.json",
                 "--out-dir", out, "--name", "main-results", "--format", "both",
                 "--decimals", "3")
    assert result.returncode == 0, result.stderr
    tex = (out / "main-results.tex").read_text(encoding="utf-8")
    assert r"\begin{tabular}" in tex and r"\end{tabular}" in tex
    assert r"\toprule" in tex and r"\midrule" in tex and r"\bottomrule" in tex
    assert r"$\pm$" in tex
    assert "0.798" in tex and "0.910" in tex
    assert "5" in tex  # n per cell
    assert "holm" in tex and "family size 3" in tex  # p-value carries its correction
    assert "bootstrap" in tex and "10000" in tex
    # every tabular row must have the same number of cells as the column spec
    body = [ln for ln in tex.splitlines() if ln.strip().endswith(r"\\")]
    assert body, "no tabular rows"
    cells = {ln.count("&") for ln in body}
    assert len(cells) == 1, f"ragged tabular rows: {cells}"

    md = (out / "main-results.md").read_text(encoding="utf-8")
    assert "| Config |" in md
    assert "0.798 ± 0.007" in md
    assert "holm" in md


def test_make_tables_refuses_missing_config(tmp_path: Path):
    out = tmp_path / "tab2"
    result = run(TABLES, "--summary", FIXTURES / "fixture_summary_missing.json",
                 "--out-dir", out, "--name", "broken")
    assert result.returncode == 2
    assert "ours" in result.stderr and "no stats" in result.stderr
    assert not (out / "broken.tex").exists()
    assert "nan" not in result.stdout.lower()


def test_make_tables_refuses_pvalue_without_correction(tmp_path: Path):
    payload = json.loads((FIXTURES / "fixture_summary.json").read_text(encoding="utf-8"))
    payload["paired"] = {"test": "wilcoxon", "p_value": 0.03, "n_pairs": 5}
    summary = write_json(tmp_path / "no_correction.json", payload)
    result = run(TABLES, "--summary", summary, "--out-dir", tmp_path / "tab3",
                 "--name", "nope")
    assert result.returncode == 2
    assert "correction" in result.stderr


def test_make_tables_refuses_metric_mismatch(tmp_path: Path):
    result = run(TABLES, "--summary", FIXTURES / "fixture_summary.json",
                 "--out-dir", tmp_path / "tab4", "--name", "nope",
                 "--metric", "f1_macro")
    assert result.returncode == 2
    assert "f1_macro" in result.stderr


# -----------------------------------------------------------------------------
# 5. citations -> bib
# -----------------------------------------------------------------------------
def test_citations_to_bib_keeps_only_verified(tmp_path: Path):
    out = tmp_path / "refs.generated.bib"
    result = run(CITE2BIB, "--csv", FIXTURES / "fixture_verified.csv", "--out", out)
    assert result.returncode == 0, result.stderr
    entries = bibtex_min.parse_bibtex(out.read_text(encoding="utf-8"))
    keys = {e["key"] for e in entries}
    assert keys == {"fixture-verified-2024", "fixture-arxiv-2025"}
    assert "fixture-mismatch-2023" not in keys
    by_key = {e["key"]: e for e in entries}
    assert by_key["fixture-arxiv-2025"]["eprint"] == "2501.00000"
    assert by_key["fixture-verified-2024"]["doi"] == "10.0000/fixture.0001"
    for entry in entries:
        assert entry["title"] and entry["url"]
    assert "% provenance:" in out.read_text(encoding="utf-8")


def test_citations_to_bib_refuses_a_file_without_status(tmp_path: Path):
    csv_path = tmp_path / "staging.csv"
    csv_path.write_text(
        "key,title,doi\nsomekey,Some title,10.0000/x.1\n", encoding="utf-8")
    result = run(CITE2BIB, "--csv", csv_path, "--out", tmp_path / "x.bib")
    assert result.returncode == 2
    assert "status" in result.stderr
    assert not (tmp_path / "x.bib").exists()


def test_citations_to_bib_refuses_verified_row_without_title(tmp_path: Path):
    csv_path = tmp_path / "rows.csv"
    csv_path.write_text(
        "key,title,status,source\n"
        "goodkey,A title,VERIFIED,crossref\n"
        "badkey,,VERIFIED,crossref\n", encoding="utf-8")
    result = run(CITE2BIB, "--csv", csv_path, "--out", tmp_path / "y.bib")
    assert result.returncode == 1
    assert "badkey" in result.stderr
    entries = bibtex_min.parse_bibtex((tmp_path / "y.bib").read_text(encoding="utf-8"))
    assert [e["key"] for e in entries] == ["goodkey"]


# -----------------------------------------------------------------------------
# 6. Markdown draft + build script
# -----------------------------------------------------------------------------
def test_draft_mirrors_the_skeleton_and_uses_num_markers():
    text = (TEMPLATE / "md" / "DRAFT.md").read_text(encoding="utf-8")
    for heading in ("Introduction", "Related Work", "Method", "Experiments",
                    "Results", "Limitations", "Ethics Statement",
                    "Reproducibility Statement", "Conclusion"):
        assert f"## " in text and heading in text, f"DRAFT.md missing section {heading}"
    assert "<!-- num:" in text and "<!-- /num -->" in text
    assert "RESULTS-INDEX.json" in text
    assert "TODO(" in text


def test_build_script_doctor_always_succeeds():
    bash = shutil.which("bash")
    if not bash:
        pytest.skip("bash not available")
    result = subprocess.run([bash, "build.sh", "--doctor"], capture_output=True,
                            text=True, cwd=str(TEMPLATE), timeout=120)
    assert result.returncode == 0, result.stderr
    assert "verdict" in result.stdout
    assert "latexmk" in result.stdout


def test_build_script_gives_instructions_when_no_latex():
    if shutil.which("latexmk") or shutil.which("pdflatex"):
        pytest.skip("a LaTeX engine is installed here; the no-engine path does not apply")
    bash = shutil.which("bash")
    if not bash:
        pytest.skip("bash not available")
    result = subprocess.run([bash, "build.sh"], capture_output=True, text=True,
                            cwd=str(TEMPLATE), timeout=120)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "No LaTeX engine found" in result.stdout
    assert "texlive" in result.stdout


def test_build_script_rejects_bad_usage():
    bash = shutil.which("bash")
    if not bash:
        pytest.skip("bash not available")
    result = subprocess.run([bash, "build.sh", "--venue", "nonsense"],
                            capture_output=True, text=True, cwd=str(TEMPLATE), timeout=120)
    assert result.returncode == 2
