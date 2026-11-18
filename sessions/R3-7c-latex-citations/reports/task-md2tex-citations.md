# Task report: md2tex citation/atomic-write/figure-label fixes (R3-7c)

## What changed
- `05_paper/latex-build/md2tex.py`:
  - Atomic write: `body.tex` now written via same-directory temp file + `os.replace`, with bounded retry (5 attempts) targeting only `OSError errno 22` / Windows error 1224. Prior output preserved on failure.
  - Citation conversion: explicit `arXiv:` and `DOI ` markers mapped to BibTeX keys present in auto-loaded `refs.bib`; emits natbib `\citep{}`. Unmatched markers remain visible and are reported (`UNMATCHED_CITATIONS`, counts printed). Conversion skipped inside code spans and references section.
  - Figure labels: each generated figure gets `\label{fig:<filename>}`; markdown-image-only emission removes duplicate `fig:main-accuracy` label. Unique labels: `fig:F1_abstain_precision_by_rung`, `fig:F2_precision_overrefusal_vs_coverage`.

## Citation coverage
- Matched: 11 marker occurrences -> 7 unique keys.
- Unmatched: `arXiv:2309.07597` (C-Pack; absent from refs.bib). Left intact; no entry invented.

## Checks
- `python 05_paper/latex-build/tests/test_md2tex.py`: PASS (all tests).
- `powershell -ExecutionPolicy Bypass -File 05_paper/latex-build/build.ps1`: exit 0.
- PDFs: `out/paper-acl.pdf` (20 pages), `out/paper-article.pdf` (19 pages).
- No `undefined` in logs; 0 `??` in both PDFs; 0 `Overfull` lines.

## Known limits
- `arXiv:2309.07597` remains unresolved (not in refs.bib); bibliography incomplete for that marker by design.
- Fontconfig warning is non-fatal on this host.
