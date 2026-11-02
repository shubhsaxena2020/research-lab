#!/usr/bin/env python
"""originality_check.py -- local n-gram overlap check between a draft and the sources we read.

RULES.md #3 (original wording only) needs a procedure that can be run on an unpublished
draft without uploading it anywhere. This tool is the mechanical half of that procedure
(06_review/ORIGINALITY.md): it compares the draft against a local corpus of source texts
and reports every *maximal* run of shared words, so a human can classify each hit.

It is NOT a plagiarism detector. It cannot prove originality. It can only show that no
long verbatim passage from *this corpus* survives in the draft -- and the corpus is only
the sources we actually consulted.

Usage
    python tools/originality_check.py --draft 05_paper/main.md --corpus 02_literature/sources/txt
    python tools/originality_check.py --draft d.tex --corpus c/ --json
    python tools/originality_check.py --draft d.md --corpus c/ --out 06_review/originality_report.md

What it does
    * normalizes whitespace and case, tokenizes on words (hyphens split, apostrophes kept);
    * strips LaTeX commands but keeps their argument text (\\emph{x} -> x). Citation
      commands (\\citep{...}) are removed entirely -- their argument is a bib key, not
      prose -- and replaced by a non-word sentinel so the quotation audit can still see
      that a citation was there;
    * strips unescaped % comments in .tex drafts and HTML comments in .md drafts, so
      commented-out text can never create a phantom overlap;
    * ignores the draft's own References/Bibliography section (it is not the author's prose);
    * splits the draft into sentences and records a line number for every token;
    * finds maximal shared runs, i.e. one hit per shared passage, not one hit per sliding
      window (a 20-word copy is one 20-word hit, not thirteen 8-word hits);
    * classifies each run QUOTED (every token inside a quotation) or UNQUOTED, and
      reports a 12-word context window on both sides;
    * audits quotations: each quoted span must carry a citation in the same sentence, and
      total quoted words must stay under --quote-budget (default 2% of the draft).

Exit codes (tools/CONTRACTS.md §6)
    0  no UNQUOTED run of at least --min-words words (and, with --strict-quotes, no
       quotation-audit finding)
    1  findings: at least one UNQUOTED run, or (with --strict-quotes) an uncited quote or
       a quote budget overrun
    2  usage error (missing/unreadable input, unsupported draft type, bad parameters)

Every hit still needs a human decision (see 06_review/ORIGINALITY.md):
coincidental technical phrase (fine) / unmarked quotation (MUST FIX) / paraphrase too
close (MUST FIX). The tool labels nothing as "fine".
"""

from __future__ import annotations

import argparse
import bisect
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

DRAFT_SUFFIXES = {".md", ".markdown", ".tex", ".txt"}
CORPUS_SUFFIXES = {".txt", ".md"}

# A citation was removed here. Non-word characters only, so it never becomes a token and
# can never create an overlap of its own.
CITE_SENTINEL = "\u00a7\u00a7\u00a7"

WORD_RE = re.compile(r"[^\W_]+(?:['\u2019][^\W_]+)*", re.UNICODE)

QUOTE_PATTERNS = (
    # Quotes may wrap across source lines (drafts are hard-wrapped), but must not swallow
    # a paragraph break -- that would mark unrelated prose as quoted.
    re.compile(r'"[^"]{1,1500}"', re.DOTALL),
    re.compile(r"\u201c[^\u201d]{1,1500}\u201d", re.DOTALL),   # curly double quotes
    re.compile(r"\u00ab[^\u00bb]{1,1500}\u00bb", re.DOTALL),   # guillemets
)
PARA_BREAK = re.compile(r"\n[ \t]*\n")

# Sentence boundary: after . ! ? (plus closing quotes/brackets), or at a blank line.
SENT_BOUNDARY = re.compile(r'(?<=[.!?])["\u201d\u2019\)\]]*\s+|\n[ \t]*\n')

# Citation markers, checked inside the sentence that contains a quotation.
CITE_MARK_RE = re.compile(
    r"\u00a7\u00a7\u00a7"                       # LaTeX \cite... (replaced)
    r"|\[@[^\]]+\]"                             # pandoc [@key]
    r"|\[\d+(?:\s*[,\u2013-]\s*\d+)*\]"         # numeric [3] / [3,5]
    r"|\(\s*[A-Z][A-Za-z.\-']+(?:\s+et\s+al\.?)?"  # (Author, 2020) / (Author et al., 2020)
    r"(?:\s+(?:and|&)\s+[A-Z][A-Za-z.\-']+)?"
    r",?\s+(?:19|20)\d{2}[a-z]?\s*\)"
)

TEX_CITE_RE = re.compile(r"\\[a-zA-Z]*cite[a-zA-Z]*\*?(?:\[[^\]]*\])*\{[^}]*\}")
TEX_HREF_RE = re.compile(r"\\href\{[^{}]*\}\{([^{}]*)\}")
TEX_URL_RE = re.compile(r"\\url\{[^{}]*\}")
TEX_ENQUOTE_RE = re.compile(r"\\enquote\{([^{}]*)\}")
TEX_MATH_RE = re.compile(
    r"\$\$.*?\$\$|\$[^$]*\$|\\\[.*?\\\]|\\\(.*?\\\)", re.DOTALL
)
TEX_CMD_ARG_RE = re.compile(r"\\[a-zA-Z@]+\*?(?:\[[^\]]*\])?\{([^{}]*)\}")
TEX_CMD_RE = re.compile(r"\\[a-zA-Z@]+\*?")
MD_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)

MD_REF_RE = re.compile(
    r"^\s{0,3}(?:#{1,6}\s*)?(?:\*\*)?"
    r"(?:references|bibliography|works cited|reference list)"
    r"(?:\*\*)?\s*$",
    re.IGNORECASE,
)
TXT_REF_RE = re.compile(
    r"^\s*(?:\d+\.?\s*)?(?:references|bibliography|works cited)\s*$", re.IGNORECASE
)
TEX_REF_RE = re.compile(
    r"^\s*(?:\\(?:section|subsection|chapter|part)\*?\s*\{\s*"
    r"(?:references|bibliography)\s*\}|\\bibliography\s*\{|"
    r"\\begin\s*\{\s*thebibliography\s*\}|\\printbibliography)",
    re.IGNORECASE,
)


# --------------------------------------------------------------------------- data types


@dataclass
class Quote:
    text: str
    line: int
    sentence: int
    words: int
    cited: bool


@dataclass
class Prepared:
    """A cleaned text with the token/offset bookkeeping the matcher needs."""

    path: Path
    text: str
    tokens: List[str] = field(default_factory=list)
    starts: List[int] = field(default_factory=list)
    ends: List[int] = field(default_factory=list)
    lines: List[int] = field(default_factory=list)
    sents: List[int] = field(default_factory=list)
    quoted: List[bool] = field(default_factory=list)
    quotes: List[Quote] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.tokens)

    def span_text(self, first: int, last: int) -> str:
        """Original (cleaned) characters covering tokens first..last inclusive."""
        return self.text[self.starts[first]: self.ends[last]]

    def context(self, first: int, last: int, ctx: int) -> str:
        lo = max(0, first - ctx)
        hi = min(len(self.tokens) - 1, last + ctx)
        return " ".join(self.text[self.starts[lo]: self.ends[hi]].split())


# --------------------------------------------------------------------------- cleaning


def read_text(path: Path) -> str:
    """Read UTF-8, falling back to cp1252/Latin-1 for PDF-dump oddities."""
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def strip_tex_comment(line: str) -> str:
    """Drop an unescaped % comment; keep escaped \\% and everything before it."""
    out: List[str] = []
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == "\\" and i + 1 < len(line):
            out.append(line[i: i + 2])
            i += 2
            continue
        if ch == "%":
            break
        out.append(ch)
        i += 1
    return "".join(out)


def latex_to_text(line: str) -> str:
    """Strip LaTeX markup, keep the words a reader would actually see."""
    s = line
    # TeX quotation marks become real quotation marks so the audit can see them.
    s = s.replace("``", "\u201c").replace("''", "\u201d")
    s = TEX_ENQUOTE_RE.sub(lambda m: "\u201c" + m.group(1) + "\u201d", s)
    s = TEX_MATH_RE.sub(" ", s)
    s = TEX_CITE_RE.sub(" " + CITE_SENTINEL + " ", s)
    s = TEX_HREF_RE.sub(r"\1", s)
    s = TEX_URL_RE.sub(" ", s)
    s = re.sub(r"\\(?:begin|end)\s*\{[^{}]*\}", " ", s)
    # Unwrap \cmd[opt]{arg} -> arg, repeatedly, to handle nesting.
    for _ in range(8):
        new = TEX_CMD_ARG_RE.sub(r"\1", s)
        if new == s:
            break
        s = new
    s = TEX_CMD_RE.sub(" ", s)          # commands without arguments
    s = re.sub(r"\\([%&_$#{}])", r"\1", s)   # escaped literals
    s = s.replace("\\", " ").replace("{", " ").replace("}", " ")
    s = s.replace("~", " ")
    return s


def reference_start(lines: Sequence[str], suffix: str) -> Optional[int]:
    """Index of the draft's own reference section, if it has one."""
    rx = TEX_REF_RE if suffix == ".tex" else (MD_REF_RE if suffix in (".md", ".markdown") else TXT_REF_RE)
    for i, line in enumerate(lines):
        if rx.search(line):
            return i
    return None


def clean_lines(raw_lines: Sequence[str], suffix: str, drop_references: bool) -> List[str]:
    lines = list(raw_lines)
    if drop_references:
        start = reference_start(lines, suffix)
        if start is not None:
            lines = lines[:start]
    out: List[str] = []
    for line in lines:
        if suffix == ".tex":
            line = strip_tex_comment(line)
            line = latex_to_text(line)
        else:
            line = MD_COMMENT_RE.sub(" ", line) if suffix in (".md", ".markdown") else line
        out.append(line)
    return out


# --------------------------------------------------------------------------- preparation


def prepare(path: Path, drop_references: bool = False, suffix: Optional[str] = None) -> Prepared:
    suffix = (suffix or path.suffix).lower()
    raw = read_text(path)
    cleaned = clean_lines(raw.splitlines(), suffix, drop_references)
    text = "\n".join(cleaned)

    # line number per character offset
    line_offsets: List[int] = []
    pos = 0
    for ln in cleaned:
        line_offsets.append(pos)
        pos += len(ln) + 1

    bounds: List[int] = [0]
    for m in SENT_BOUNDARY.finditer(text):
        if m.end() > bounds[-1]:
            bounds.append(m.end())
    bounds.append(len(text) + 1)

    spans: List[Tuple[int, int]] = []
    for rx in QUOTE_PATTERNS:
        for m in rx.finditer(text):
            if PARA_BREAK.search(m.group(0)):
                continue
            spans.append((m.start(), m.end()))
    spans.sort()

    prep = Prepared(path=path, text=text)
    quote_words: Dict[int, int] = {}
    cite_positions = [m.start() for m in re.finditer(re.escape(CITE_SENTINEL), text)]

    for m in WORD_RE.finditer(text):
        word = m.group(0).lower()
        prep.tokens.append(word)
        prep.starts.append(m.start())
        prep.ends.append(m.end())
        prep.lines.append(bisect.bisect_right(line_offsets, m.start()))  # 1-based
        prep.sents.append(max(0, bisect.bisect_right(bounds, m.start()) - 1))
        inside = any(s <= m.start() and m.end() <= e for s, e in spans)
        prep.quoted.append(inside)

    # Quotation audit bookkeeping.
    for s, e in spans:
        body = text[s:e]
        n_words = len(WORD_RE.findall(body))
        if n_words == 0:
            continue
        sent = max(0, bisect.bisect_right(bounds, s) - 1)
        sent_start = bounds[sent]
        sent_end = bounds[sent + 1] if sent + 1 < len(bounds) else len(text) + 1
        window = text[sent_start:min(sent_end, len(text))]
        cited = bool(CITE_MARK_RE.search(window)) or any(
            sent_start <= c < sent_end for c in cite_positions
        )
        prep.quotes.append(
            Quote(
                text=" ".join(body.split()),
                line=bisect.bisect_right(line_offsets, s),
                sentence=sent + 1,
                words=n_words,
                cited=cited,
            )
        )
    return prep


# --------------------------------------------------------------------------- matching


def ngram_index(tokens: Sequence[str], n: int, cap: int = 40) -> Dict[Tuple[str, ...], List[int]]:
    idx: Dict[Tuple[str, ...], List[int]] = {}
    for i in range(len(tokens) - n + 1):
        key = tuple(tokens[i: i + n])
        bucket = idx.get(key)
        if bucket is None:
            idx[key] = [i]
        elif len(bucket) < cap:
            bucket.append(i)
    return idx


def maximal_runs(draft: Prepared, corpus: Prepared, index: Dict[Tuple[str, ...], List[int]],
                 n: int, min_words: int, max_runs: int = 5000) -> List[Tuple[int, int, int]]:
    """(draft_start, corpus_start, length) maximal shared runs of >= min_words words."""
    dt, ct = draft.tokens, corpus.tokens
    found = set()
    for i in range(len(dt) - n + 1):
        key = tuple(dt[i: i + n])
        positions = index.get(key)
        if not positions:
            continue
        for p in positions:
            left = 0
            while i - left - 1 >= 0 and p - left - 1 >= 0 and dt[i - left - 1] == ct[p - left - 1]:
                left += 1
            right = n
            while i + right < len(dt) and p + right < len(ct) and dt[i + right] == ct[p + right]:
                right += 1
            length = left + right
            if length >= min_words:
                found.add((i - left, p - left, length))
            if len(found) > max_runs:
                break
        if len(found) > max_runs:
            break

    runs = sorted(found, key=lambda r: (r[0], -r[2]))
    kept: List[Tuple[int, int, int]] = []
    for a in runs:
        a_end = a[0] + a[2]
        contained = any(
            b[2] > a[2] and b[0] <= a[0] and b[0] + b[2] >= a_end for b in runs
        )
        if not contained:
            kept.append(a)
    # Same passage can be reached from several corpus offsets; keep the first.
    seen = set()
    uniq = []
    for r in kept:
        if r[0] in seen:
            continue
        seen.add(r[0])
        uniq.append(r)
    return uniq


# --------------------------------------------------------------------------- report


def analyze(draft_path: Path, corpus_path: Path, n: int, min_words: int,
            context: int, quote_budget: float) -> dict:
    draft = prepare(draft_path, drop_references=True)
    if not draft.tokens:
        raise ValueError(f"draft has no words after cleaning: {draft_path}")

    if corpus_path.is_dir():
        files = sorted(
            p for p in corpus_path.rglob("*")
            if p.is_file() and p.suffix.lower() in CORPUS_SUFFIXES
        )
    else:
        files = [corpus_path]
    if not files:
        raise ValueError(f"no .txt/.md files under corpus path: {corpus_path}")

    sources = []
    hits: List[dict] = []
    for path in files:
        src = prepare(path)
        if len(src) < n:
            sources.append({"file": str(path), "words": len(src), "hits": 0,
                            "longest_run": 0, "status": "TOO_SHORT"})
            continue
        idx = ngram_index(src.tokens, n)
        runs = maximal_runs(draft, src, idx, n, min_words)
        longest = 0
        for d_start, c_start, length in runs:
            d_last, c_last = d_start + length - 1, c_start + length - 1
            quoted = all(draft.quoted[d_start: d_start + length])
            longest = max(longest, length)
            hits.append({
                "id": f"H{len(hits) + 1:03d}",
                "status": "QUOTED" if quoted else "UNQUOTED",
                "length": length,
                "source": str(path),
                "source_line": src.lines[c_start],
                "source_sentence": src.sents[c_start] + 1,
                "source_context": src.context(c_start, c_last, context),
                "draft_line": draft.lines[d_start],
                "draft_sentence": draft.sents[d_start] + 1,
                "draft_context": draft.context(d_start, d_last, context),
                "text": " ".join(draft.span_text(d_start, d_last).split()),
                "quoted_words": sum(1 for q in draft.quoted[d_start: d_start + length] if q),
            })
        sources.append({"file": str(path), "words": len(src), "hits": len(runs),
                        "longest_run": longest,
                        "status": "OK" if runs else "CLEAR"})

    hits.sort(key=lambda h: (h["status"] == "QUOTED", -h["length"], h["draft_line"]))
    for i, h in enumerate(hits, 1):
        h["id"] = f"H{i:03d}"

    unquoted = [h for h in hits if h["status"] == "UNQUOTED"]
    quoted_hits = [h for h in hits if h["status"] == "QUOTED"]

    quoted_words = sum(1 for q in draft.quoted if q)
    ratio = quoted_words / max(1, len(draft.tokens))
    uncited = [q for q in draft.quotes if not q.cited]

    failures = []
    if unquoted:
        failures.append(f"{len(unquoted)} UNQUOTED shared run(s) of >= {min_words} words")
    quote_findings = []
    if uncited:
        quote_findings.append(f"{len(uncited)} quoted span(s) without a citation in the same sentence")
    if ratio > quote_budget:
        quote_findings.append(
            f"quoted words {ratio:.2%} exceed the {quote_budget:.2%} budget"
        )

    return {
        "tool": "tools/originality_check.py",
        "tool_version": 1,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "draft": str(draft_path),
        "draft_words": len(draft.tokens),
        "corpus": {
            "path": str(corpus_path),
            "n_files": len(files),
            "words": sum(s["words"] for s in sources),
            "files": sources,
        },
        "params": {"n": n, "min_words": min_words, "context": context,
                   "quote_budget": quote_budget, "ignore_references": True},
        "summary": {
            "verdict": "FAIL" if unquoted else "PASS",
            "n_hits": len(hits),
            "n_unquoted": len(unquoted),
            "n_quoted": len(quoted_hits),
            "longest_unquoted": max((h["length"] for h in unquoted), default=0),
            "longest_quoted": max((h["length"] for h in quoted_hits), default=0),
            "quoted_words": quoted_words,
            "quote_ratio": round(ratio, 6),
            "quote_budget": quote_budget,
            "n_quotes": len(draft.quotes),
            "n_uncited_quotes": len(uncited),
            "failures": failures,
            "quote_findings": quote_findings,
            "caveat": ("Not a plagiarism detector. A PASS means no shared run of >= "
                       f"{min_words} words outside quotation marks was found in THIS corpus, "
                       "which contains only the sources we consulted. It does not prove "
                       "originality and does not check the web."),
        },
        "hits": hits,
        "quotes": [
            {"text": q.text, "line": q.line, "sentence": q.sentence,
             "words": q.words, "cited": q.cited}
            for q in draft.quotes
        ],
    }


def render_markdown(rep: dict) -> str:
    s = rep["summary"]
    p = rep["params"]
    out: List[str] = []
    out.append("# Originality check report")
    out.append("")
    out.append(f"- Generated: {rep['generated_at']}")
    out.append(f"- Draft: `{rep['draft']}` ({rep['draft_words']} words)")
    out.append(f"- Corpus: `{rep['corpus']['path']}` -- {rep['corpus']['n_files']} file(s), "
               f"{rep['corpus']['words']} words")
    out.append(f"- Parameters: n={p['n']}, min-words={p['min_words']}, context={p['context']} "
               f"words each side, quote budget={p['quote_budget']:.2%}")
    out.append("")
    verdict = s["verdict"]
    out.append(f"## Verdict: **{verdict}**")
    out.append("")
    if s["failures"]:
        for f in s["failures"]:
            out.append(f"- FAIL: {f}")
    else:
        out.append(f"- No UNQUOTED shared run of {p['min_words']}+ words found in this corpus.")
    out.append(f"- Hits: {s['n_hits']} total, {s['n_unquoted']} unquoted "
               f"(longest {s['longest_unquoted']}), {s['n_quoted']} quoted "
               f"(longest {s['longest_quoted']}).")
    out.append("")
    out.append("## Quotation audit")
    out.append("")
    out.append(f"- Quoted words: {s['quoted_words']} / {rep['draft_words']} "
               f"= **{s['quote_ratio']:.2%}** (budget {p['quote_budget']:.2%})")
    out.append(f"- Quoted spans: {s['n_quotes']}; without a citation in the same sentence: "
               f"{s['n_uncited_quotes']}")
    for f in s["quote_findings"]:
        out.append(f"- QUOTE FINDING: {f}")
    if rep["quotes"]:
        out.append("")
        out.append("| # | line | words | cited | text |")
        out.append("|---|------|-------|-------|------|")
        for i, q in enumerate(rep["quotes"], 1):
            text = q["text"].replace("|", "\\|")
            if len(text) > 120:
                text = text[:117] + "..."
            out.append(f"| Q{i:02d} | {q['line']} | {q['words']} | "
                       f"{'yes' if q['cited'] else '**NO**'} | {text} |")
    out.append("")
    out.append("## Corpus sources")
    out.append("")
    out.append("| source | words | hits | longest shared run |")
    out.append("|--------|-------|------|--------------------|")
    for src in rep["corpus"]["files"]:
        name = Path(src["file"]).name
        out.append(f"| {name} | {src['words']} | {src['hits']} | "
                   f"{src['longest_run']} ({src['status']}) |")
    out.append("")
    out.append("## Hits")
    out.append("")
    if not rep["hits"]:
        out.append("None. Nothing in this corpus shares a run of "
                   f"{p['min_words']}+ consecutive words with the draft.")
        out.append("")
    for h in rep["hits"]:
        out.append(f"### {h['id']} -- {h['status']}, {h['length']} words")
        out.append("")
        out.append(f"- Draft: line {h['draft_line']}, sentence {h['draft_sentence']}")
        out.append(f"- Source: `{Path(h['source']).name}` line {h['source_line']}, "
                   f"sentence {h['source_sentence']}")
        out.append(f"- Shared text: \"{h['text'][:300]}\"")
        out.append(f"- Draft context: ...{h['draft_context']}...")
        out.append(f"- Source context: ...{h['source_context']}...")
        if h["status"] == "UNQUOTED":
            out.append("- Decide: coincidental technical phrase (fine) / unmarked quotation "
                       "(MUST FIX: quotes + citation) / paraphrase too close (MUST FIX: rewrite).")
        else:
            out.append("- Quoted: confirm the citation is in the same sentence and the "
                       "quotation is no longer than needed.")
        out.append("")
    out.append("## Caveat")
    out.append("")
    out.append(s["caveat"])
    out.append("")
    return "\n".join(out)


# --------------------------------------------------------------------------- CLI


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="originality_check.py",
        description="Local n-gram overlap check between a draft and a corpus of source texts. "
                    "Not a plagiarism detector; see 06_review/ORIGINALITY.md.",
    )
    ap.add_argument("--draft", required=True, help="draft file (.md, .tex, .txt)")
    ap.add_argument("--corpus", required=True,
                    help="directory searched recursively for .txt/.md, or one such file")
    ap.add_argument("--n", type=int, default=8, help="n-gram length (default 8)")
    ap.add_argument("--min-words", type=int, default=None,
                    help="minimum run length flagged/reported (default: same as --n)")
    ap.add_argument("--context", type=int, default=12,
                    help="context words shown on each side of a run (default 12)")
    ap.add_argument("--quote-budget", type=float, default=0.02,
                    help="max fraction of draft words inside quotation marks (default 0.02)")
    ap.add_argument("--strict-quotes", action="store_true",
                    help="exit 1 also for uncited quotations or a quote-budget overrun")
    ap.add_argument("--json", action="store_true", help="print the JSON report to stdout")
    ap.add_argument("--out", help="write the markdown report to this path")
    return ap


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = build_parser()
    args = ap.parse_args(argv)

    draft = Path(args.draft)
    corpus = Path(args.corpus)
    min_words = args.min_words if args.min_words is not None else args.n

    if not draft.is_file():
        print(f"error: draft not found: {draft}", file=sys.stderr)
        return 2
    if draft.suffix.lower() not in DRAFT_SUFFIXES:
        print(f"error: unsupported draft type '{draft.suffix}' (use .md/.tex/.txt)", file=sys.stderr)
        return 2
    if not corpus.exists():
        print(f"error: corpus path not found: {corpus}", file=sys.stderr)
        return 2
    if args.n < 3:
        print("error: --n must be >= 3", file=sys.stderr)
        return 2
    if min_words < args.n:
        print("error: --min-words must be >= --n", file=sys.stderr)
        return 2
    if args.context < 0:
        print("error: --context must be >= 0", file=sys.stderr)
        return 2
    if not (0.0 <= args.quote_budget <= 1.0):
        print("error: --quote-budget must be between 0 and 1", file=sys.stderr)
        return 2

    try:
        rep = analyze(draft, corpus, args.n, min_words, args.context, args.quote_budget)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except Exception:
        pass

    if args.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        s = rep["summary"]
        print(f"draft: {rep['draft']} ({rep['draft_words']} words)")
        print(f"corpus: {rep['corpus']['n_files']} file(s), {rep['corpus']['words']} words")
        print(f"verdict: {s['verdict']}  hits={s['n_hits']} "
              f"unquoted={s['n_unquoted']} quoted={s['n_quoted']} "
              f"longest_unquoted={s['longest_unquoted']}")
        print(f"quoted words: {s['quoted_words']}/{rep['draft_words']} "
              f"= {s['quote_ratio']:.2%} (budget {rep['params']['quote_budget']:.2%}); "
              f"uncited quotes: {s['n_uncited_quotes']}")
        for h in rep["hits"][:20]:
            print(f"  {h['id']} {h['status']:8s} {h['length']:3d}w "
                  f"draft:{h['draft_line']} <- {Path(h['source']).name}:{h['source_line']}")
        if len(rep["hits"]) > 20:
            print(f"  ... {len(rep['hits']) - 20} more (use --json or --out)")
        for f in s["failures"] + s["quote_findings"]:
            print(f"  finding: {f}")

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(render_markdown(rep), encoding="utf-8")
        if not args.json:
            print(f"report: {out_path}")

    failed = bool(rep["summary"]["n_unquoted"]) or (
        args.strict_quotes and bool(rep["summary"]["quote_findings"])
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
