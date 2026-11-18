# Build report (main laptop, res-s1, 2026-11-18)

Engine: Tectonic 0.17.0 (see ENGINE.md, "Current install — main laptop").

## Build command (one command, re-runnable on any later draft)

    powershell -ExecutionPolicy Bypass -File 05_paper/latex-build/build.ps1

Steps performed by build.ps1:
1. `python md2tex.py` (regenerates `body.tex` from `05_paper/draft/paper.md`)
2. `citations_to_bib.py` (regenerates `refs.bib` from `02_literature/verified_citations.csv`)
3. `svg2pdf.py` for every SVG in `05_paper/figures/generated/`
4. `tectonic paper-acl.tex --keep-logs`
5. `tectonic paper-article.tex --keep-logs`
6. Copy PDFs to `out/`.

Engine resolution: `$env:TECTONIC` -> `tools/tectonic/tectonic.exe` (repo-relative) -> `tectonic` on PATH. Fails loudly if none. Fails loudly if any log contains `undefined` (case-insensitive) or a build exits non-zero or a PDF is missing.

## Output

- `out/paper-acl.pdf` (20 pages)
- `out/paper-article.pdf` (19 pages)

## Checks (all pass)

- `python 05_paper/latex-build/tests/test_md2tex.py`: PASS — 4/4 tests (number preservation, known citation, unknown citation, unique figure labels); 317 numbers preserved byte-identical between `paper.md` and `body.tex`.
- Undefined references/citations: none (`grep -i undefined` on both `.log` files returns no matches).
- `??` in extracted PDF text: 0 in both PDFs (`pdftotext`).
- Tables: 7 numbered tables (Table 1..7) present in both PDFs; 8 `\\begin{table}` environments in `body.tex`.
- Overfull boxes > 10pt: none. Previously 10.95pt (ACL) and 16.68pt (article front-matter); both resolved (see below).
- Figures: `F1_abstain_precision_by_rung.pdf` and `F2_precision_overrefusal_vs_coverage.pdf` generated. Labels are unique: `fig:F1_abstain_precision_by_rung`, `fig:F2_precision_overrefusal_vs_coverage`; no duplicated `fig:main-accuracy`.
- Bibliography: non-empty in both PDFs (7 entries); no "no \citation commands" warning.

## Bounded retry / atomic promotion

- `md2tex.py` writes `body.tex` to a same-directory temp file and promotes with `os.replace`, retrying only OSError errno 22 / Windows error 1224 (up to 5 attempts); real errors propagate and prior output is preserved.
- `svg2pdf.py` writes PDFs the same way.
- `build.ps1` retries `citations_to_bib.py` (5 attempts) and Tectonic (4 attempts) only when output contains `os error 1224`/`Errno 22`; real TeX errors exit non-zero. Final `Copy-Item` to `out/` is retried.

## Overfull-box fix (no wording or number changed)

Resolved in the LaTeX preambles (`paper-acl.tex`, `paper-article.tex`) only:
- `\\setlength{\\emergencystretch}{3em}` -> `5em`
- `\\tolerance=2000` -> `5000`
No text in `paper.md` was changed. Rebuild shows 0 `Overfull` lines in both logs.

## Known limitations (carried)

- References section in `paper.md` is replaced by the BibTeX bibliography; Section 9 list numbers are stripped.
- Bold markers spanning lines may leave stray asterisks (md2tex handles single-line bold only).
- Figure converted with pure-Python `svg2pdf.py` (no external deps).
- Bibliography is now populated via natbib `\\citep{}` commands emitted from explicit draft arXiv/DOI markers. Citation coverage: 11 matched marker occurrences -> 7 unique keys; 1 unmatched marker (`arXiv:2309.07597`, C-Pack, absent from `refs.bib`), left visible and reported. No BibTeX entry invented.
- Non-fatal `Fontconfig error: Cannot load default config file` appears on this host; PDFs are written successfully.

## Historical note

Laptop-2 build (2026-11-08) recorded the original 10.9pt overfull box and older draft. This report supersedes it for the current draft; the old PDFs were rebuilt from the current draft by this laptop.
