# `figures/generated/` — output directory

Nothing here is written by hand. `../make_figures.py` writes, per figure name:

* `<name>.csv` — the plotted rows, with the index id / file each value came from
* `<name>.svg` — hand-written vector preview (stdlib only)
* `<name>.tex` — body-only LaTeX fragment, `\input` by `main.tex`
* `<name>.pdf` / `<name>.png` — only when matplotlib is installed

This directory is empty until an experiment has produced a results file and an
entry in `04_experiments/RESULTS-INDEX.json`. An empty directory is the correct
state for a repo with no results: `main.tex` falls back to a placeholder box
rather than failing to compile.

Regenerate with:

```bash
python figures/make_figures.py --index ../../04_experiments/RESULTS-INDEX.json \
       --figure main-accuracy --out-dir figures/generated
```
