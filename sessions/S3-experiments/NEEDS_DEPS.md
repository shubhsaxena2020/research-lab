# NEEDS_DEPS — packages this session could not install (RULES: request, don't install)

Checked 2026-11-03 against `python` = 3.11.15 (hermes venv). Everything below is
*optional*: all S3 tooling degrades gracefully without it. Nothing here blocks Phase 1.

| package      | wanted for                                   | fallback already implemented |
|--------------|----------------------------------------------|------------------------------|
| matplotlib   | 05_paper figure generation (PNG/PDF)          | figure scripts emit CSV + a pure-python SVG writer; PNG needs matplotlib |
| pandas       | tabular summaries, ablation tables            | stdlib csv + statistics are used instead |
| scikit-learn | bootstrap CI cross-check, paired tests        | own bootstrap + permutation test in harness/stats.py |
| bibtexparser | BibTeX parsing                                | `tools/lib/bibtex_min.py` (no dependency) |

Install command for whoever owns the environment (do NOT run from inside a session):

    python -m pip install matplotlib pandas scikit-learn bibtexparser

Note: `scipy` is also absent, so `harness/stats.py` implements Wilcoxon signed-rank and
the bootstrap itself (documented in the module docstring, tested against hand-computed
values). If scipy is installed later, stats.py should be preferred over hand-rolled maths
for p-values — the hand-rolled version is validated but not a substitute for a maintained
implementation.
