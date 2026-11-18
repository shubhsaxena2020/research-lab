# task-reviewer-clean — clean rebuild verification report

Date: 2026-11-18 (profile res-s1)
Scope: completely clean re-run of R3-7b LaTeX build (delete generated artifacts, then build).

## Clean step
Deleted before build: `paper-acl.pdf`, `paper-article.pdf`, `body.tex`, `refs.bib`,
`paper-*.log`, `out/*.pdf`, `figures/*.pdf`. Confirmed absent pre-build.

## Build
Command: `powershell -ExecutionPolicy Bypass -File build.ps1` (working dir `05_paper/latex-build`)
Result: exit code 0. Steps md2tex, citations_to_bib (342 entries), figure conversion (2 SVGs),
and both tectonic builds completed. PDFs copied to `out/`.

## Verification checks

| # | Criterion | Result |
|---|-----------|--------|
| 1 | Exit code 0 | PASS |
| 2 | `out/paper-acl.pdf` exists | PASS (107,179 bytes) |
| 3 | `out/paper-article.pdf` exists | PASS (106,908 bytes) |
| 4 | Page count acl = 20 (from log) | PASS — `Output written on paper-acl.xdv (20 pages, …)` |
| 5 | Page count article = 19 (from log) | PASS — `Output written on paper-article.xdv (19 pages, …)` |
| 6 | `test_md2tex.py` PASS (317) | PASS — `PASS: 317 numbers preserved in body.tex` |
| 7 | No `undefined` in logs | PASS — 0 matches in both `paper-acl.log` and `paper-article.log` |
| 8 | No `Overfull` in logs | PASS — 0 matches in both logs |
| 9 | No `??` in pdftotext output | PASS — 0 matches in both PDFs |
| 10 | Tables 1–7 present | PASS — `Table 1` … `Table 7` found in both PDFs |

## Additional observations (not in named criteria)
- BibTeX reports `I found no \citation commands` (blg) and natbib emits
  `Empty 'thebibliography' environment` because the document contains no `\cite`
  commands; bibliography is therefore empty. This is pre-existing behavior, not a
  build failure, and does not affect exit code or the named criteria.
- `LaTeX Warning: Label 'fig:main-accuracy' multiply defined` (3 definitions in
  `body.tex`) appears in both logs. Not an `undefined`/`Overfull` issue, but a
  correctness smell worth a follow-up.
- Fontconfig emits a non-fatal stderr line on this host (noted previously).

## Verdict
All ten named verification criteria PASS. No mismatch against the specified
acceptance criteria. Two pre-existing correctness smells (empty bibliography,
multiply-defined `fig:main-accuracy` label) are flagged above for follow-up.