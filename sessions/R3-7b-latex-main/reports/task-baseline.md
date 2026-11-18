# Task baseline — draft build diagnostics (R3-7b)

Baseline build of `05_paper/latex-build` using Tectonic 0.17.0 (`research-lab/tools/tectonic/tectonic.exe`). No code changed.

## Steps run

1. `python md2tex.py` — OK; rewrote `body.tex`.
2. `python ../template/tools/citations_to_bib.py --csv ../../02_literature/verified_citations.csv --out refs.bib` — OK; 342 entries.
3. `python svg2pdf.py --in ../figures/generated/F1_abstain_precision_by_rung.svg --out figures/F1_abstain_precision_by_rung.pdf` — OK.
4. `python svg2pdf.py --in ../figures/generated/F2_precision_overrefusal_vs_coverage.svg --out figures/F2_precision_overrefusal_vs_coverage.pdf` — OK.
5. `tectonic paper-acl.tex --keep-logs` — OK (exit 0).
6. `tectonic paper-article.tex --keep-logs` — OK (exit 0).
7. `python tests/test_md2tex.py` — OK.

## Diagnostics

### Overfull boxes

- `paper-acl`: 1 — `Overfull \hbox (10.94777pt too wide) in paragraph at lines 1078--1079` (`body.tex`).
- `paper-article`: 1 — `Overfull \hbox (16.6791pt too wide) in paragraph at lines 7--8` (`body.tex`).
- No other `Overfull` lines in either log.

### Undefined references / citations

- `grep -i undefined` on both logs: no matches. No undefined `\ref`/`\cite` reported.
- BibTeX (both builds): `I found no \citation commands` — `body.tex` contains no `\cite` commands and neither `.tex` includes a bibliography, so BibTeX emitted an ignored error and no bibliography was produced. Not an undefined-citation failure, but noted.

### Page counts (from "Output written on")

- `paper-acl`: 20 pages (`paper-acl.xdv`).
- `paper-article`: 19 pages (`paper-article.xdv`).

### Tables

- `body.tex`: 8 `\begin{table}` environments (all `tabularx`).

### test_md2tex

- PASS: 317 numbers preserved in `body.tex`.

### Figures

- `F1_abstain_precision_by_rung.svg` exists; converted to `figures/F1_abstain_precision_by_rung.pdf`.
- `F2_precision_overrefusal_vs_coverage.svg` exists; converted to `figures/F2_precision_overrefusal_vs_coverage.pdf`.

## Other notes

- Non-fatal `Fontconfig error: Cannot load default config file` appeared in both builds; PDFs written successfully.
- BibTeX errors (`no \citation commands`) were ignored by Tectonic but logged in `.blg`; builds still completed.
- Build artifacts present: `paper-acl.pdf`, `paper-article.pdf`, `paper-acl.log`, `paper-article.log`, `refs.bib`, `body.tex`, and both figure PDFs under `figures/`.