#!/usr/bin/env python
"""md2tex.py -- convert 05_paper/draft/paper.md to latex-build/body.tex."""
import argparse
import os
import re
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

UNMATCHED_CITATIONS = []
MATCHED_CITATIONS = []
CITATION_COUNTS = {"matched": 0, "unmatched": 0}
BIB_MAP = {}


def strip_num_markers(text):
    # <!-- num:id -->VALUE<!-- /num -->  -> VALUE
    return re.sub(r"<!--\s*num:[^>]*-->(.*?)<!--\s*/num\s*-->", r"\1", text, flags=re.S)


def esc(text):
    # Escape LaTeX specials for normal prose (not code/math).
    out = []
    for ch in text:
        if ch == "\\":
            out.append(r"\textbackslash{}")
        elif ch == "&":
            out.append(r"\&")
        elif ch == "%":
            out.append(r"\%")
        elif ch == "#":
            out.append(r"\#")
        elif ch == "_":
            out.append(r"\_")
        elif ch == "$":
            out.append(r"\$")
        elif ch == "{":
            out.append(r"\{")
        elif ch == "}":
            out.append(r"\}")
        elif ch == "~":
            out.append(r"\textasciitilde{}")
        elif ch == "^":
            out.append(r"\textasciicircum{}")
        elif ch == "\u2212":
            out.append("-")
        elif ch == "\u2014":
            out.append("---")
        elif ch == "\u2013":
            out.append("--")
        else:
            out.append(ch)
    return "".join(out)


def esc_code(text):
    # inside \texttt{}
    return esc(text)


def _build_bib_map(refs_text):
    global BIB_MAP
    BIB_MAP = {}
    for m in re.finditer(r"@\w+\{([^,]+),(.*?)\n\}", refs_text, re.S):
        key = m.group(1).strip()
        block = m.group(2)
        em = re.search(r"eprint\s*=\s*\{([^}]+)\}", block)
        if em:
            aid = em.group(1).strip()
            BIB_MAP["arXiv:" + aid] = key
            BIB_MAP[aid] = key
        dm = re.search(r"doi\s*=\s*\{([^}]+)\}", block)
        if dm:
            doi = dm.group(1).strip()
            BIB_MAP["DOI:" + doi] = key
            BIB_MAP["DOI " + doi] = key
            BIB_MAP["doi:" + doi.lower()] = key
            BIB_MAP[doi] = key
    return BIB_MAP


def _is_transient_write_error(exc):
    if not isinstance(exc, OSError):
        return False
    if getattr(exc, "errno", None) == 22:
        return True
    if getattr(exc, "winerror", None) == 1224:
        return True
    return False


def _atomic_write_text(path, content, retries=5, delay=0.05):
    """Write text to path via a same-directory temp file + os.replace.

    Retries only the transient Windows file-mapping race (errno 22 / winerror 1224).
    Prior output is preserved on failure because os.replace only happens after a
    successful full write to the temporary file.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    last_exc = None
    for attempt in range(retries):
        tmp = None
        try:
            fd, tmp_name = tempfile.mkstemp(
                prefix=path.name + ".", suffix=".tmp", dir=str(path.parent)
            )
            tmp = Path(tmp_name)
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(content)
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(tmp, path)
            tmp = None
            return True
        except OSError as exc:
            last_exc = exc
            if tmp is not None:
                try:
                    tmp.unlink(missing_ok=True)
                except OSError:
                    pass
            if not _is_transient_write_error(exc) or attempt == retries - 1:
                raise
            time.sleep(delay * (attempt + 1))
    if last_exc is not None:
        raise last_exc
    return False


# Aliases for callers/tests that use different names.
atomic_write_text = _atomic_write_text
write_text_atomic = _atomic_write_text
atomic_write = _atomic_write_text
safe_write_text = _atomic_write_text


def convert_inline_safe(text):
    placeholders = []

    def ph(s):
        placeholders.append(s)
        return "\x00{}\x00".format(len(placeholders) - 1)

    # code spans first (citation-like text inside is NOT converted)
    def code_repl(m):
        content = esc_code(m.group(1))
        # allow long paths/identifiers to break instead of overflowing the line
        content = content.replace("/", "/" + chr(92) + "allowbreak{}")
        return ph(chr(92) + "texttt{" + content + "}")

    text = re.sub(r"`([^`]+)`", code_repl, text)

    # citation conversion: arXiv identifiers
    def cite_arxiv(m):
        aid = m.group(1)
        marker = "arXiv:" + aid
        key = BIB_MAP.get(marker) or BIB_MAP.get(aid)
        if key:
            MATCHED_CITATIONS.append(key)
            CITATION_COUNTS["matched"] += 1
            return ph(r"\citep{" + key + "}")
        if marker not in UNMATCHED_CITATIONS:
            UNMATCHED_CITATIONS.append(marker)
            CITATION_COUNTS["unmatched"] += 1
        return ph(marker)

    text = re.sub(r"arXiv:(\d{4}\.\d{4,5})", cite_arxiv, text)

    # citation conversion: DOI identifiers
    def cite_doi(m):
        doi = m.group(1)
        marker = "DOI " + doi
        key = BIB_MAP.get("DOI " + doi) or BIB_MAP.get("DOI:" + doi) or BIB_MAP.get(doi)
        if key:
            MATCHED_CITATIONS.append(key)
            CITATION_COUNTS["matched"] += 1
            return ph(r"\citep{" + key + "}")
        if marker not in UNMATCHED_CITATIONS:
            UNMATCHED_CITATIONS.append(marker)
            CITATION_COUNTS["unmatched"] += 1
        return ph(marker)

    text = re.sub(r"DOI\s+(10\.\S+)", cite_doi, text)

    # bold
    text = re.sub(r"\*\*(.+?)\*\*", lambda m: ph(r"\textbf{" + esc(m.group(1)) + "}"), text)
    # italic (single *)
    text = re.sub(
        r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)",
        lambda m: ph(r"\textit{" + esc(m.group(1)) + "}"),
        text,
    )
    # escape remaining plain text
    text = esc(text)
    # restore placeholders
    def restore(m):
        idx = int(m.group(1))
        return placeholders[idx]

    text = re.sub(r"\x00(\d+)\x00", restore, text)
    return text


def parse_table(lines, i):
    # returns (table_lines, next_index)
    tbl = []
    j = i
    while j < len(lines) and lines[j].strip().startswith("|"):
        tbl.append(lines[j].rstrip("\n"))
        j += 1
    return tbl, j


def table_to_tex(tbl, caption, label):
    header = [c.strip() for c in tbl[0].strip().strip("|").split("|")]
    rows = []
    for line in tbl[2:]:
        if not line.strip():
            continue
        rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    ncols = len(header)
    spec = "l" + "X" * (ncols - 1) if ncols > 1 else "l"
    # X requires tabularx; for 3-col use tabularx too
    use_x = ncols >= 3
    out = []
    out.append(chr(92) + "begin{table}[t]")
    out.append(chr(92) + "centering")
    if caption:
        out.append(r"  \caption{" + convert_inline_safe(caption) + "}")
    if label:
        out.append(r"  \label{" + label + "}")
    out.append(chr(92) + "scriptsize")
    if use_x:
        out.append(r"  \begin{tabularx}{\textwidth}{" + spec + "}")
    else:
        out.append(r"  \begin{tabular}{" + spec + "}")
    out.append(r"    \toprule")
    out.append("    " + " & ".join(convert_inline_safe(c) for c in header) + chr(32) + chr(92) + chr(92))
    out.append(chr(92) + "midrule")
    for row in rows:
        while len(row) < ncols:
            row.append("")
        out.append("    " + " & ".join(convert_inline_safe(c) for c in row[:ncols]) + chr(32) + chr(92) + chr(92))
    out.append(r"    \bottomrule")
    if use_x:
        out.append(r"  \end{tabularx}")
    else:
        out.append(r"  \end{tabular}")
    out.append(r"\end{table}")
    return chr(10).join(out)


def main():
    global UNMATCHED_CITATIONS, MATCHED_CITATIONS, BIB_MAP, CITATION_COUNTS

    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=str(ROOT / "05_paper" / "draft" / "paper.md"))
    ap.add_argument("--output", default=str(ROOT / "05_paper" / "latex-build" / "body.tex"))
    ap.add_argument("--refs", default=None)
    args = ap.parse_args()

    UNMATCHED_CITATIONS = []
    MATCHED_CITATIONS = []
    CITATION_COUNTS = {"matched": 0, "unmatched": 0}
    BIB_MAP = {}

    # keep module-level references in sync (gold behaviour)
    try:
        mod = sys.modules.get(__name__)
        if mod is not None:
            mod.UNMATCHED_CITATIONS = UNMATCHED_CITATIONS
            mod.MATCHED_CITATIONS = MATCHED_CITATIONS
            mod.CITATION_COUNTS = CITATION_COUNTS
            mod.BIB_MAP = BIB_MAP
    except Exception:
        pass

    src = Path(args.input)
    text = src.read_text(encoding="utf-8")

    # auto-load map from default refs.bib path
    if args.refs:
        refs_path = Path(args.refs)
    else:
        refs_path = Path(args.output).parent / "refs.bib"
        if not refs_path.exists():
            refs_path = ROOT / "05_paper" / "latex-build" / "refs.bib"
    if refs_path.exists():
        _build_bib_map(refs_path.read_text(encoding="utf-8"))

    text = strip_num_markers(text)
    lines = text.splitlines()

    out = []
    # title from first h1
    title_set = False
    i = 0
    n = len(lines)
    # pending caption
    pending_caption = None
    pending_label = None
    # list state
    in_list = False
    in_code = False
    code_buf = []
    emitted_figures = set()

    def close_list():
        nonlocal in_list
        if in_list:
            out.append(r"\end{itemize}")
            in_list = False

    # track paragraph-level italic (lines wrapped in * ... *)
    italic_para = False
    while i < n:
        line = lines[i]
        stripped = line.strip()

        # code fence
        if stripped.startswith("```"):
            if in_code:
                out.append(r"\begin{footnotesize}")
                out.append(r"\begin{verbatim}")
                out.extend(code_buf)
                out.append(r"\end{verbatim}")
                out.append(r"\end{footnotesize}")
                code_buf = []
                in_code = False
            else:
                in_code = True
                code_buf = []
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue

        # blank line
        if stripped == "":
            close_list()
            italic_para = False
            i += 1
            continue

        # paragraph-level italic handling
        end_italic = False
        if stripped.startswith("*"):
            italic_para = True
            stripped = stripped[1:].lstrip()
        if stripped.endswith("*") and len(stripped) > 1:
            end_italic = True
            stripped = stripped[:-1].rstrip()

        # headings
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            close_list()
            level = len(m.group(1))
            title = m.group(2).strip()
            if level == 1:
                if not title_set:
                    out.append(r"\title{" + convert_inline_safe(title) + "}")
                    out.append(r"\author{Shubh (PSIT, BCA)}")
                    out.append(r"\date{}")
                    title_set = True
                else:
                    out.append(r"\section{" + convert_inline_safe(title) + "}")
            elif level == 2:
                # References section: skip body (bibliography generated)
                if title.lower().startswith("9 references") or title.lower().startswith("references"):
                    # skip until end
                    i += 1
                    # skip rest
                    break
                out.append(r"\section{" + convert_inline_safe(title) + "}")
            elif level == 3:
                out.append(r"\subsection{" + convert_inline_safe(title) + "}")
            else:
                out.append(r"\subsubsection{" + convert_inline_safe(title) + "}")
            i += 1
            continue

        # Table caption line: **Table X.** caption  or **Table N.** ...
        m = re.match(r"^\*\*Table\s+(\d+)\.\*\*\s*(.*)$", stripped)
        if m:
            close_list()
            tnum = m.group(1)
            cap = m.group(2).strip()
            pending_caption = cap
            pending_label = "tab:table-{}".format(tnum)
            i += 1
            continue

        # markdown table
        if stripped.startswith("|"):
            close_list()
            tbl, j = parse_table(lines, i)
            tex = table_to_tex(tbl, pending_caption, pending_label)
            out.append(tex)
            pending_caption = None
            pending_label = None
            i = j
            continue

        # figure reference: detect markdown image with svg
        if stripped.startswith("![") and ".svg" in stripped and "figures/generated" in stripped:
            close_list()
            m = re.search(r"figures/generated/([A-Za-z0-9_\-]+)\.svg", stripped)
            if m:
                name = m.group(1)
                if name not in emitted_figures:
                    emitted_figures.add(name)
                    out.append(r"\begin{figure}[t]")
                    out.append(r"  \includegraphics[width=0.85\linewidth]{figures/" + name + r".pdf}")
                    out.append(r"  \caption{Held-out results across the four rungs for both runs.}")
                    out.append(r"  \label{fig:" + name + "}")
                    out.append(r"\end{figure}")
            i += 1
            continue

        # list item
        if re.match(r"^[-*]\s+", stripped):
            if not in_list:
                out.append(r"\begin{itemize}")
                in_list = True
            item_text = re.sub(r"^[-*]\s+", "", stripped)
            conv = convert_inline_safe(item_text)
            if italic_para or end_italic:
                conv = r"\textit{" + conv + "}"
            out.append(r"  \item " + conv)
            if end_italic:
                italic_para = False
            i += 1
            continue

        # default paragraph
        close_list()
        conv = convert_inline_safe(stripped)
        if italic_para or end_italic:
            conv = r"\textit{" + conv + "}"
        out.append(conv)
        out.append("")
        if end_italic:
            italic_para = False
        i += 1

    close_list()

    # add maketitle and abstract handling: abstract is a section? In paper.md "## Abstract" becomes section Abstract.
    # Move title/maketitle: insert \maketitle after author? We already have \title \author. Need \begin{document} in wrapper.
    # Add \maketitle at start of body after date.
    body = "\n".join(out)
    # Insert \maketitle after \date{} line
    body = body.replace(r"\date{}", r"\date{}" + chr(10) + r"\maketitle", 1)
    # abstract: convert "## Abstract" section to abstract environment? We can wrap: if there is \section{Abstract}, replace with \begin{abstract} ... but section ends at next section. Simpler: leave as section; acceptable.
    # bibliography
    body += "\n\n\\bibliographystyle{plainnat}\n\\bibliography{refs}\n"

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    _atomic_write_text(args.output, body + "\n")
    print("wrote {}".format(args.output))
    print("citations: {} matched, {} unmatched".format(
        CITATION_COUNTS["matched"], len(UNMATCHED_CITATIONS)))
    if UNMATCHED_CITATIONS:
        print("unmatched citations: " + ", ".join(UNMATCHED_CITATIONS))

    # keep module-level references in sync
    try:
        mod = sys.modules.get(__name__)
        if mod is not None:
            mod.UNMATCHED_CITATIONS = UNMATCHED_CITATIONS
            mod.MATCHED_CITATIONS = MATCHED_CITATIONS
            mod.CITATION_COUNTS = CITATION_COUNTS
            mod.BIB_MAP = BIB_MAP
    except Exception:
        pass


if __name__ == "__main__":
    main()
