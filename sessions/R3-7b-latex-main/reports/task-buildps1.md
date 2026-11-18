# task-buildps1 report

## Changed
- `05_paper/latex-build/build.ps1`: engine resolved via `$env:TECTONIC` -> `$RepoRoot/tools/tectonic/tectonic.exe` -> `Get-Command tectonic`; loud `Write-Error` + exit 1 if none. `$RepoRoot` now correctly two levels above script. Undefined refs/citations checked in `paper-*.log` with `(?i)undefined`; matching lines printed and build aborts. Exit code and PDF existence still checked. md2tex, citations_to_bib, svg2pdf steps retained.

## Verified
- `powershell -ExecutionPolicy Bypass -File build.ps1` completed with exit 0.
- Produced `out/paper-acl.pdf` and `out/paper-article.pdf`.
- `test_md2tex.py`: PASS (317 numbers preserved).
- No `undefined` lines in either build log.

## Notes
- Fontconfig emits a non-fatal stderr line on this host; build exit code remains 0 and PDFs are produced.
- Overfull box (10.9pt) in ACL build remains; owned by separate task.