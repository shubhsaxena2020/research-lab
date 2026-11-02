"""Tests for tools/make_digest.py.

These tests exercise the honesty contract, not just the formatting:
  * resolved evidence is quoted verbatim from the index/file and the verified CSV;
  * missing evidence produces [TO FILL], never a plausible number;
  * --check actually fails on an incomplete digest;
  * the glossary never contains a definition.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import textwrap
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TOOL = REPO / "tools" / "make_digest.py"
FIX = Path(__file__).resolve().parent / "fixtures" / "digest"
INDEX = FIX / "results_index.json"
CITATIONS = FIX / "verified_citations.csv"
METHOD = FIX / "method.md"

BLOCKS = [
    "What this section says",
    "Why it is there",
    "What could be asked at a talk",
    "Five likely questions with honest answers",
    "Glossary",
]


def run(*args: object) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TOOL), *[str(a) for a in args]],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(REPO),
    )


def generate(out_dir: Path, section: Path = METHOD) -> subprocess.CompletedProcess:
    return run(
        "--section", section,
        "--index", INDEX,
        "--citations", CITATIONS,
        "--root", FIX,
        "--out-dir", out_dir,
    )


def block(text: str, name: str) -> str:
    m = re.search(rf"^## {re.escape(name)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    assert m, f"missing block {name}"
    return m.group(1)


def q_blocks(text: str) -> list[tuple[str, str]]:
    body = block(text, "Five likely questions with honest answers")
    heads = list(re.finditer(r"^### Q(\d+)\.\s*(.+)$", body, re.M))
    out = []
    for i, head in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(body)
        out.append((head.group(2).strip(), body[head.end():end].strip()))
    return out


def test_generates_all_blocks_with_one_short_bullet_per_paragraph(tmp_path: Path) -> None:
    out = tmp_path / "digest"
    proc = generate(out)
    assert proc.returncode == 0, proc.stderr
    text = (out / "METHOD.md").read_text(encoding="utf-8")

    for name in BLOCKS:
        assert f"## {name}" in text

    bullets = [ln for ln in block(text, "What this section says").splitlines() if ln.startswith("- ")]
    assert len(bullets) == 6  # one per prose paragraph in the fixture
    for bullet in bullets:
        assert len(bullet[2:].replace("\u2026", "").split()) <= 25, bullet


def test_bullets_are_extractive_not_invented(tmp_path: Path) -> None:
    out = tmp_path / "digest"
    assert generate(out).returncode == 0
    text = (out / "METHOD.md").read_text(encoding="utf-8")
    source = METHOD.read_text(encoding="utf-8").lower()
    source_tokens = set(re.findall(r"[a-z0-9][a-z0-9_.\-]*", source))

    allowed = {"i", "my", "me", "myself", "here"}
    for bullet in [ln[2:] for ln in block(text, "What this section says").splitlines() if ln.startswith("- ")]:
        for token in re.findall(r"[A-Za-z0-9][A-Za-z0-9_.\-]*", bullet.lower()):
            if token in allowed:
                continue
            assert token in source_tokens, f"invented token {token!r} in bullet: {bullet}"


def test_resolved_number_and_citation_are_quoted_verbatim(tmp_path: Path) -> None:
    out = tmp_path / "digest"
    assert generate(out).returncode == 0
    text = (out / "METHOD.md").read_text(encoding="utf-8")
    qas = q_blocks(text)

    number_answers = [(q, a) for q, a in qas if "main.accuracy.baseline" in a]
    assert number_answers, "no answer resolved the numeric marker"
    _, answer = number_answers[0]
    assert "0.812" in answer
    assert "results/main_baseline.json" in answer
    assert "`accuracy`" in answer

    citation_answers = [(q, a) for q, a in qas if "reimers2019" in a]
    assert citation_answers, "no answer resolved the citation key"
    _, answer = citation_answers[0]
    assert "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks" in answer
    assert "EMNLP-IJCNLP" in answer
    assert "2019" in answer


def test_missing_index_id_yields_to_fill_not_an_invented_value(tmp_path: Path) -> None:
    section = tmp_path / "method.md"
    section.write_text(
        textwrap.dedent(
            """\
            # Method

            We report <!-- num:main.accuracy.missing -->0.777<!-- /num --> on the test split.

            We describe the pipeline so a reader can repeat it.
            """
        ),
        encoding="utf-8",
    )
    out = tmp_path / "digest"
    proc = generate(out, section)
    assert proc.returncode == 0, proc.stderr
    text = (out / "METHOD.md").read_text(encoding="utf-8")

    answers = [a for _, a in q_blocks(text) if "main.accuracy.missing" in a]
    assert answers, "the unresolved marker was not surfaced at all"
    answer = answers[0]
    assert "[TO FILL" in answer
    assert "0.777" not in answer          # the printed draft value is not evidence
    assert "the stored value there is" not in answer  # no value was read, so none may be claimed


def test_missing_citation_key_yields_to_fill(tmp_path: Path) -> None:
    section = tmp_path / "method.md"
    section.write_text(
        textwrap.dedent(
            """\
            # Method

            Our pipeline follows the design of \\cite{ghost2020} for retrieval.

            We fix the seed for every run.
            """
        ),
        encoding="utf-8",
    )
    out = tmp_path / "digest"
    assert generate(out, section).returncode == 0
    text = (out / "METHOD.md").read_text(encoding="utf-8")

    answers = [a for _, a in q_blocks(text) if "ghost2020" in a]
    assert answers
    assert "[TO FILL" in answers[0]
    assert "not in" in answers[0]


def test_check_fails_on_four_questions_and_passes_on_five(tmp_path: Path) -> None:
    out = tmp_path / "digest"
    assert generate(out).returncode == 0
    full = (out / "METHOD.md").read_text(encoding="utf-8")

    # A 5-question digest passes the structural check (TO FILL is allowed unless --strict).
    five = tmp_path / "five.md"
    five.write_text(full, encoding="utf-8")
    assert run("--check", five).returncode == 0

    four_text = re.sub(r"### Q5\..*?(?=^## Glossary)", "", full, flags=re.M | re.S)
    four = tmp_path / "four.md"
    four.write_text(four_text, encoding="utf-8")
    proc = run("--check", four)
    assert proc.returncode == 1
    assert "4 questions" in proc.stdout

    # A genuinely student-filled digest passes --strict as well.
    clean = textwrap.dedent(
        """\
        # Student digest - clean

        ## What this section says

        - I state the claim in one sentence.

        ## Why it is there

        - [ ] What problem is solved?
        - [ ] What is the contribution?
        - [ ] What is out of scope?

        ## What could be asked at a talk

        1. Why this metric? (paragraph 1)
        2. What would falsify it? (paragraph 1)
        3. How many seeds? (paragraph 1)

        ## Five likely questions with honest answers

        ### Q1. Why this metric?

        I answer with the number from the run file.

        ### Q2. What would falsify it?

        I answer with the result that would contradict the claim.

        ### Q3. How many seeds?

        I answer with the seed count from the metadata.

        ### Q4. What is the baseline?

        I answer with the tuned baseline from the results file.

        ### Q5. What is the limit?

        I answer with the scope stated in the limitations section.

        ## Glossary

        No terms outside the built-in BCA vocabulary were found in this section.
        """
    )
    clean_path = tmp_path / "clean.md"
    clean_path.write_text(clean, encoding="utf-8")
    proc = run("--check", clean_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_strict_fails_while_generated_digest_still_has_to_fill(tmp_path: Path) -> None:
    out = tmp_path / "digest"
    assert generate(out).returncode == 0
    digest = out / "METHOD.md"

    assert run("--check", digest).returncode == 0
    strict = run("--check", digest, "--strict")
    assert strict.returncode == 1
    assert "unresolved [TO FILL]" in strict.stdout


def test_glossary_only_ever_emits_placeholders(tmp_path: Path) -> None:
    out = tmp_path / "digest"
    assert generate(out).returncode == 0
    text = (out / "METHOD.md").read_text(encoding="utf-8")
    glossary = block(text, "Glossary")
    entries = [ln for ln in glossary.splitlines() if ln.startswith("- **")]

    assert len(entries) >= 3
    assert any("**BLEU**" in ln for ln in entries)
    assert any("**pipeline**" in ln for ln in entries)
    assert any("**initialisation**" in ln.lower() for ln in entries)
    assert not any("**section**" in ln for ln in entries)  # basic word, not glossed

    for line in entries:
        # Exactly: "- **term** — [TO FILL: ...]" and nothing that could be a definition.
        m = re.match(r"^- \*\*(.+?)\*\* — (.*)$", line)
        assert m, line
        assert m.group(2).startswith("[TO FILL"), line
        assert "first appears: paragraph" in m.group(2)
        assert "define it in my own words" in m.group(2)


def test_missing_block_fails_check(tmp_path: Path) -> None:
    out = tmp_path / "digest"
    assert generate(out).returncode == 0
    text = (out / "METHOD.md").read_text(encoding="utf-8")
    broken = re.sub(r"^## Glossary\s*$.*\Z", "", text, flags=re.M | re.S)
    path = tmp_path / "broken.md"
    path.write_text(broken, encoding="utf-8")
    proc = run("--check", path)
    assert proc.returncode == 1
    assert "missing block: ## Glossary" in proc.stdout


def test_all_mode_writes_one_digest_per_section(tmp_path: Path) -> None:
    out = tmp_path / "digest"
    proc = run(
        "--section", FIX,
        "--all",
        "--index", INDEX,
        "--citations", CITATIONS,
        "--root", FIX,
        "--out-dir", out,
    )
    assert proc.returncode == 0, proc.stderr
    assert (out / "METHOD.md").is_file()
    assert (out / "RESULTS.md").is_file()

    # The LaTeX-style marker in results.md resolves and is attached to its paragraph.
    results = (out / "RESULTS.md").read_text(encoding="utf-8")
    assert "0.812" in results
    assert "results/main_baseline.json" in results
    bullets = [ln for ln in block(results, "What this section says").splitlines() if ln.startswith("- ")]
    assert len(bullets) == 2
    assert not any(b.strip() == "- 0.812" for b in bullets)


def test_toy_evidence_is_never_quoted(tmp_path: Path) -> None:
    (tmp_path / "results").mkdir()
    (tmp_path / "results" / "toy.json").write_text(
        json.dumps({"toy": True, "accuracy": 0.5}), encoding="utf-8"
    )
    (tmp_path / "index.json").write_text(
        json.dumps({
            "version": 1,
            "entries": [{
                "id": "toy.accuracy",
                "file": "results/toy.json",
                "key": "accuracy",
                "toy": True,
            }],
        }),
        encoding="utf-8",
    )
    section = tmp_path / "method.md"
    section.write_text(
        textwrap.dedent(
            """\
            # Method

            We report <!-- num:toy.accuracy -->0.5<!-- /num --> on the test split.
            """
        ),
        encoding="utf-8",
    )
    out = tmp_path / "digest"
    proc = run(
        "--section", section,
        "--index", tmp_path / "index.json",
        "--citations", CITATIONS,
        "--root", tmp_path,
        "--out-dir", out,
    )
    assert proc.returncode == 0, proc.stderr
    text = (out / "METHOD.md").read_text(encoding="utf-8")
    answers = [a for _, a in q_blocks(text) if "toy.accuracy" in a]
    assert answers
    assert "[TO FILL" in answers[0]
    assert "TOY - NOT A RESULT" in answers[0]
    assert "0.5" not in answers[0]
