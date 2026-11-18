# Task report: converter tests (R3-7c)

## Files changed
- `05_paper/latex-build/tests/test_md2tex.py` (rewritten)

## What was done
- Kept the existing number-preservation check and fixed the invalid `\%` escape
  (`n.replace("%", r"\%")` instead of `"\%"`).
- Added `test_known_arxiv_citation_becomes_citep`: derives the BibTeX key for a
  known arXiv id (`2403.01461`, present in `refs.bib`) from `refs.bib` and asserts
  `\citep{key}` (or `\cite{key}`) appears in `body.tex`.
- Added `test_unknown_citation_remains_visible_and_is_reported`: uses an arXiv id
  absent from `refs.bib` (`2309.07597`), asserts the `arXiv:...` marker stays
  visible in `body.tex`, and that it is reported as unmatched (via stdout or module
  global state).
- Added `test_figure_labels_unique`: asserts no duplicate `fig:` labels and that
  `fig:main-accuracy` is no longer duplicated.
- Tests import `md2tex.py` by path via `importlib.util`, reset module-level
  unmatched state, and run both as a plain script (`python .../test_md2tex.py`)
  and under pytest.

## Verification
- `python -m py_compile 05_paper/latex-build/tests/test_md2tex.py` -> OK
- `python 05_paper/latex-build/tests/test_md2tex.py`:
  - `test_number_preservation`: PASS (317 numbers)
  - The three new checks currently fail against the pre-change `md2tex.py`
    (no citation conversion, duplicate `fig:main-accuracy` labels), as expected;
    they are written against the R3-7c `md2tex.py` changes and should pass once
    those land.
- `python -m pytest 05_paper/latex-build/tests/test_md2tex.py -q` collects 4 tests.

## Notes
- Test file does not edit `md2tex.py`. Known/unknown fixtures are derived from
  `refs.bib` at runtime so they track the generated bibliography.
"""