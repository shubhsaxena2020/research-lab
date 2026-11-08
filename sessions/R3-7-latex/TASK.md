# TASK R3-7 — LaTeX / PDF build (LAPTOP 2, profile res-s7)

You run on laptop 2 in a COPY of the repo at `C:\Users\admin\research-lab` (wherever RULES.md/COMMON.md say
`C:\Users\shubh\research-lab`, read `C:\Users\admin\research-lab`). The head copies your OWNED folder back.

Goal: a reproducible one-command build that turns `05_paper/draft/paper.md` (generated Markdown with `<!-- num: -->` markers
and Markdown tables) into a camera-ready PDF in ACL format, plus an arXiv-style article build. The draft will change in
round 3; the build must be re-runnable on any later version without hand edits.

OWNED: `05_paper/latex-build/**`, `sessions/R3-7-latex/**`. Everything else read-only (read `05_paper/template/` — main.tex,
acl/, ieee/, BUILD.md, build.sh, refs.bib, tools/citations_to_bib.py — and reuse what works).

Deliverables
1. Install the TeX engine: download the official Tectonic Windows x86_64 release zip from
   https://github.com/tectonic-typesetting/tectonic/releases (latest stable `tectonic@...` tag) into
   `C:\Users\admin\tools\tectonic\`, verify the sha256 against the release page if published, record version + URL + hash in
   `latex-build/ENGINE.md`. No admin rights, no other installs. If the download is blocked, write CARD BLOCKED with the reason.
2. `latex-build/md2tex.py`: converts paper.md -> body.tex (headings, emphasis, inline/display math if any, Markdown tables ->
   booktabs tables with captions/labels, figure inclusion, citations -> \cite keys from refs.bib generated from
   `02_literature/verified_citations.csv` via the template's citations_to_bib.py), stripping `num:` markers but keeping the
   numbers byte-identical. Tests: `latex-build/tests/` — every number in paper.md appears unchanged in body.tex.
3. Figures: the SVG in `05_paper/figures/generated/` -> PDF for LaTeX (find a converter that needs no install, e.g. a pure
   Python SVG->PDF path, or emit the figure as TikZ/pgfplots from its source data; record the choice).
4. `latex-build/build.ps1` (one command): md2tex -> tectonic -> `latex-build/out/paper-acl.pdf` and `paper-article.pdf`;
   log warnings; fail loudly on undefined references/citations.
5. Build the CURRENT draft, then check the PDF: page count, no overfull boxes > 10pt, no "??" references, all tables present
   (extract text with the pure-Python route you choose and diff the numbers against paper.md). Report in `latex-build/BUILD-REPORT.md`.
Batches of >= 3 subagents (engine+env / converter / figures / tests+checker), then a reviewer subagent re-runs the build clean.
