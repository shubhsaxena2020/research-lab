# R3-7c-latex-citations — orchestrator pass 2 report

Date: 2026-11-18 (about 21:50 IST)

## Read and inspected

- `RULES.md`, `sessions/R3/COMMON.md`, `orchestration/HEAD-REVIEW.md`, and superseded `orchestration/DIRECTIVES.md`.
- Existing R3-7b task and prompt, `05_paper/latex-build/BUILD-REPORT.md`, `build.ps1`, `md2tex.py`, `tests/test_md2tex.py`, `body.tex`, `refs.bib`, and `citations_to_bib.py`.
- Graphify skill instructions. No existing `graphify-out/graph.json` or interpreter sidecar was present; did not build an unrelated graph for this narrow build task.

## Decision

Use the now-idle res-s1 for R3-7c-latex-citations. It directly addresses the three defects Claude Code verified after R3-7b: Windows file-map write failures, no citation commands emitted, and three identical figure labels. Keep R3-4c-fold untouched; it owns the draft/template. Do not restart the shared gateway; MCP tools remain unavailable until a coordinated restart.

## Written

- `sessions/R3-7c-latex-citations/TASK.md`: source ownership, citation and file-race constraints, PDF/test gates, and exactly-three-task batch requirements.
- `sessions/R3-7c-latex-citations/PROMPT-R3.txt`: lane invocation prompt with no double-quote characters.
- Checkpoint 7 appended to `orchestration/HEAD-REVIEW.md`.

## Launched

Started `ops/hermes_runner.ps1` on profile res-s1 with budget 10800, lane output `sessions/R3-7c-latex-citations/`. Confirmed a Hermes process exists for res-s1 after launch. res-s4 was not touched.

## Open risks and Claude Code watch items

- Citation-marker syntax and generated BibTeX keys must be resolved by exact arXiv/DOI identifier against `refs.bib`; unmatched markers must be reported without fabricated citations.
- Verify bounded retries handle only transient mapping errors and do not hide TeX/source failures; ensure previous complete PDFs are preserved if atomic promotion is used.
- Check the regenerated body has unique labels and no empty bibliography warning when actual citations are present.
- Read lane PROGRESS and reports after completion; independently rerun both-PDF build, `test_md2tex.py`, and PDF checks. Confirm BUILD-REPORT records actual counts and unresolved citations.
- Confirm no draft/template, res-s4, shared-gateway, or other-project files were modified.

Runner PowerShell PID: 28520. Hermes res-s1 PID: 18000. Active research-lab Hermes sessions: 2 (res-s1 and res-s4). Prompt double-quote check: 0.
