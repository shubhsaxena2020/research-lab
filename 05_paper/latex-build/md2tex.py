#!/usr/bin/env python
"""md2tex.py -- convert 05_paper/draft/paper.md to latex-build/body.tex."""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


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
        elif ch == "−":
            out.append("-")
        elif ch == "—":
            out.append("---")
        elif ch == "–":
            out.append("--")
        else:
            out.append(ch)
    return "".join(out)


def esc_code(text):
    # inside \texttt{}
    return esc(text)


def inline(text):
    # code spans first
    def code_repl(m):
        return r"\texttt{" + esc_code(m.group(1)) + "}"
    text = re.sub(r"`([^`]+)`", code_repl, text)
    # bold
    text = re.sub(r"\*\*(.+?)\*\*", lambda m: r"\textbf{" + esc(m.group(1)) + "}", text)
    # italic (single *)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", lambda m: r"\textit{" + esc(m.group(1)) + "}", text)
    # escape remaining specials (text outside commands). We already escaped inside; but plain text still has specials.
    # We need escape plain text not already in commands. Simpler: escape first then apply markup? 
    # Approach used above escapes inside markup; plain text still unescaped. Escape leftover specials carefully:
    # Split on backslash-commands? Instead, do a final pass that escapes % # & _ $ { } ~ ^ but not inside \cmd{...}.
    # For this paper, percentages and underscores in plain text need escaping. We'll do targeted replacements
    # on segments not starting with backslash.
    return text


def convert_inline_safe(text):
    # Escape special chars first (except backslash handling for commands we'll insert later).
    # We'll mark code/bold/italic with placeholders to avoid escaping their braces.
    placeholders = []

    def ph(s):
        placeholders.append(s)
        return f"\x00{len(placeholders)-1}\x00"

    # code spans
    def code_repl(m):
        return ph(r"\texttt{" + esc_code(m.group(1)) + "}")
    text = re.sub(r"`([^`]+)`", code_repl, text)
    # bold
    text = re.sub(r"\*\*(.+?)\*\*", lambda m: ph(r"\textbf{" + esc(m.group(1)) + "}"), text)
    # italic
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)",
                  lambda m: ph(r"\textit{" + esc(m.group(1)) + "}"), text)
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
    header = [c.strip() for c in tbl[0].strip().strip('|').split('|')]
    rows = []
    for line in tbl[2:]:
        if not line.strip():
            continue
        rows.append([c.strip() for c in line.strip().strip('|').split('|')])
    ncols = len(header)
    spec = 'l' + 'X' * (ncols - 1) if ncols > 1 else 'l'
    # X requires tabularx; for 3-col use tabularx too
    use_x = ncols >= 3
    out = []
    out.append(chr(92)+"begin{table}[t]")
    out.append(chr(92)+"centering")
    if caption:
        out.append(r"  \caption{" + convert_inline_safe(caption) + "}")
    if label:
        out.append(r"  \label{" + label + "}")
    out.append(chr(92)+"scriptsize")
    if use_x:
        out.append(r"  \begin{tabularx}{\textwidth}{" + spec + "}")
    else:
        out.append(r"  \begin{tabular}{" + spec + "}")
    out.append(r"    \toprule")
    out.append('    ' + ' & '.join(convert_inline_safe(c) for c in header) + chr(32)+chr(92)+chr(92)) 
    out.append(chr(92)+"midrule")
    for row in rows:
        while len(row) < ncols:
            row.append('')
        out.append('    ' + ' & '.join(convert_inline_safe(c) for c in row[:ncols]) + chr(32)+chr(92)+chr(92)) 
    out.append(r"    \bottomrule")
    if use_x:
        out.append(r"  \end{tabularx}")
    else:
        out.append(r"  \end{tabular}")
    out.append(r"\end{table}")
    return chr(10).join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=str(ROOT / "05_paper" / "draft" / "paper.md"))
    ap.add_argument("--output", default=str(ROOT / "05_paper" / "latex-build" / "body.tex"))
    args = ap.parse_args()

    src = Path(args.input)
    text = src.read_text(encoding="utf-8")
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
            pending_label = f"tab:table-{tnum}"
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

        # figure reference: detect svg path
        if ".svg" in stripped and "figures/generated" in stripped:
            close_list()
            # extract svg filename
            m = re.search(r"figures/generated/([A-Za-z0-9_\-]+)\.svg", stripped)
            if m:
                name = m.group(1)
                # insert figure environment
                out.append(r"\begin{figure}[t]")
                out.append(r"  \includegraphics[width=0.85\linewidth]{figures/" + name + r".pdf}")
                out.append(r"  \caption{Held-out results across the four rungs for both runs.}")
                out.append(r"  \label{fig:main-accuracy}")
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
                conv = r"	extit{" + conv + "}"
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
    Path(args.output).write_text(body + "\n", encoding="utf-8")
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
