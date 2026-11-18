# Progress R3-7c (md2tex citations)

- Build reliability: `build.ps1` hardened; `svg2pdf.py` atomic write. Tectonic retries only on os error 1224; real errors fail. Report: reports/task-build-reliability.md.
- Converter: `md2tex.py` writes `body.tex` via temp file + `os.replace` (bounded retry); converts 11 matched arXiv markers to `\citep{}` (7 keys); leaves `arXiv:2309.07597` unmatched and reported; figure labels unique (`fig:F1_...`, `fig:F2_...`). Report: reports/task-md2tex-citations.md.
- Tests: `python 05_paper/latex-build/tests/test_md2tex.py` -> PASS (4/4; 317 numbers preserved). Report: reports/task-tests.md.
- Rebuild: `powershell -ExecutionPolicy Bypass -File 05_paper/latex-build/build.ps1` -> exit 0; `out/paper-acl.pdf` (20 pages), `out/paper-article.pdf` (19 pages).
- Checks: no `undefined` in logs; 0 `??` in both PDFs; 8 table envs; 0 overfull >10pt; bibliography non-empty (7 entries).
- BUILD-REPORT.md updated with commands, results, citation coverage, retry behavior, and limits.

CARD COMPLETE
