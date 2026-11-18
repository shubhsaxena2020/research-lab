# Task build-reliability report (R3-7c)

Owner: res-s1. Scope: harden `05_paper/latex-build/build.ps1` and
`05_paper/latex-build/svg2pdf.py` against the transient Windows
file-mapping race (Errno 22 / OS error 1224). `md2tex.py` and tests were
not modified.

## Changes

### `svg2pdf.py`
- Imports added: `io`, `os`, `tempfile`, `time`.
- New helpers `_is_transient_write_error` and `_atomic_write_bytes`.
- `convert()` now builds the full PDF in an `io.BytesIO` buffer and promotes
  it to the target via a same-directory temp file (`tempfile.mkstemp`) plus
  `os.replace`, with bounded retry (5 attempts, 1.0 s delay) on transient
  errors (winerror 1224/32/5, errno 22/13, or messages containing "1224",
  "errno 22", "user-mapped", "mapped section", "being used by another
  process", "sharing violation").
- Prior target content is preserved until `os.replace` succeeds; on total
  failure the temp file is removed and the original exception re-raised.

### `build.ps1`
- `Build-Paper` retry detection now matches both `os error 1224` and
  `Errno 22` (plus user-mapped/mapped-section wording), case-insensitively.
  Real TeX errors (non-zero exit without a transient marker) break immediately
  and remain fatal.
- Added `Copy-WithRetry`: copies source to a same-dir temp file, then promotes
  with `Move-Item -Force` plus bounded retry (5 attempts, 3 s delay) on
  transient errors; prior destination is preserved until promotion succeeds;
  missing source throws immediately.
- Final out/ copies now use `Copy-WithRetry`.
- Tectonic is invoked in place (no temp-output flag exists in 0.17.0).

## Commands run

```
powershell -ExecutionPolicy Bypass -File 05_paper/latex-build/build.ps1
python 05_paper/latex-build/tests/test_md2tex.py
```

Tectonic inspection:

```
tools/tectonic/tectonic.exe --help        # no --temp-out / temp-output flag
tools/tectonic/tectonic.exe -Zhelp        # no temp-output unstable option
```

## Observed values

- Tectonic: 0.17.0 (engine resolution: repo-relative `tools/tectonic/tectonic.exe`).
- Build exit code: 0.
- `out/paper-acl.pdf`: 20 pages, 107810 bytes.
- `out/paper-article.pdf`: 19 pages, 107112 bytes.
- Overfull lines (>10pt): 0 in both logs.
- Undefined reference/citation lines: 0 in both logs.
- `??` in extracted PDF text: 0 in both PDFs.
- svg2pdf outputs: `figures/F1_abstain_precision_by_rung.pdf`,
  `figures/F2_precision_overrefusal_vs_coverage.pdf` written; no leftover
  `.tmp` files.
- `test_md2tex.py`: 1 PASS (`test_number_preservation`, 317 numbers), 3 FAIL
  (`test_known_arxiv_citation_becomes_citep`, `test_unknown_citation...`,
  `test_figure_labels_unique`). These failures are caused by citation
  conversion and duplicate figure labels in `md2tex.py`, which is outside this
  task's owned paths and was not edited; reported per TASK.md.

## Atomic/retry verification

- Simulated permanent failure (os.replace raising Errno 22): prior target
  bytes preserved, exception re-raised, no temp leftovers.
- Simulated transient failure (os.replace failing twice then succeeding):
  final content written, 3 attempts used.

## Known limits

- Tectonic writes its PDF in place; a race during the engine run is retried
  but a partial PDF may exist until a successful retry completes.
- Bibliography remains empty (`no \citation commands`) because citation
  conversion in `md2tex.py` is not part of this task.
- Non-fatal `Fontconfig error: Cannot load default config file` appears on
  this host; PDFs are written successfully.
path">
C:/Users/shubh/research-lab/sessions/R3-7c-latex-citations/reports/task-build-reliability.md