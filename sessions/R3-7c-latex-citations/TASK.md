# TASK R3-7c — reliable, cited LaTeX builds on the main laptop

Lane: R3-7c-latex-citations; main laptop; profile res-s1; created 2026-11-18.

## Context

R3-7b completed the main-laptop Tectonic migration and built the ACL and article PDFs. Claude Code verified Tectonic 0.17.0, 0 overfull boxes, no unresolved `??` references, and `test_md2tex.py` PASS with 317 numeric markers. It also found three remaining defects: transient Windows Defender/indexer file mapping causes `Errno 22` / OS error 1224 when outputs are overwritten; `md2tex.py` emits no citation commands so the bibliography is empty despite 342 entries in `refs.bib`; and `body.tex` defines `fig:main-accuracy` three times.

R3-4c-fold owns the draft and template. Never edit `05_paper/draft/**` or `05_paper/template/**`. If citation markers lack corresponding verified bibliography entries, report them in this lane's report and leave the marker intact; never invent a BibTeX entry or key. `refs.bib` is generated from `02_literature/verified_citations.csv` by the existing `citations_to_bib.py`; do not change that source or generator.

The shared Hermes gateway is not yours to restart. MCP tools are unavailable until a coordinated gateway restart; use built-in tools and available skills. Do not inspect, message, or alter res-s4 or the other Hermes project. Only res-s1 and res-s4 may be active for research-lab. Laptop 2 is offline.

## Owned paths

- `05_paper/latex-build/**`
- `sessions/R3-7c-latex-citations/**`

Everything else is read-only. Do not edit `tools/tectonic/**`, draft/template files, `refs.bib` source, global tools, or shared configuration. Do not commit or push.

## Deliverables

1. Make the build reliable under the observed Windows file-mapping race. Keep retries bounded and target only the transient OS error 1224 / Errno 22 condition; real TeX errors must still fail. Consider generating to a same-directory temporary file and promoting with `os.replace` plus bounded retry, so an existing complete PDF is not truncated before replacement. Inspect Tectonic output options before relying on them. Preserve useful prior outputs on failed builds.
2. Add citation conversion in `md2tex.py`: map explicit draft citation markers such as arXiv identifiers or DOI identifiers to BibTeX keys that actually occur in the generated `refs.bib`. Emit valid natbib commands. Do not infer or manufacture entries. An unmatched marker must remain visible and be reported clearly in output or the lane report. Avoid converting citation-like text inside code spans or the references section.
3. Give each generated figure a unique stable LaTeX label; remove the duplicated `fig:main-accuracy` label while preserving the existing figure content and captions.
4. Add focused converter tests for known citations, unknown citations, and unique figure labels. Keep the existing number-preservation check.
5. Rebuild both PDFs using `powershell -ExecutionPolicy Bypass -File 05_paper/latex-build/build.ps1`; rerun `python 05_paper/latex-build/tests/test_md2tex.py` and the existing PDF checks. Verify both output PDFs exist and are current, no empty bibliography warning remains when citations are present, no undefined citation/reference or `??` remains, all expected tables remain, and no overfull box exceeds 10pt.
6. Update `05_paper/latex-build/BUILD-REPORT.md` with commands, results, citation coverage and any unmatched markers, bounded retry/atomic-promotion behavior, and known limits. Do not claim a clean bibliography if citation resolution is incomplete.

## Progress

Create/update `sessions/R3-7c-latex-citations/PROGRESS.md` after every batch, recording file + command + observed value and next step. Write one report per subagent task under `reports/`. Verify subagent claims by opening files and re-running relevant commands. Last line may be `CARD COMPLETE` only after all deliverables and checks pass; otherwise use `CARD BLOCKED: <specific reason>` for a genuine blocker.

## Batches

Every batch is exactly one blocking `delegate_task` call with exactly three parallel tasks. The first action after reading instructions is that call. Each task must have one independent deliverable, exact owned write paths, input files to read, a proving check, and a report path under this lane. From batch two onward, one task must independently review and re-run/check previous batch output. Do not leave subagents running when ending a turn.
