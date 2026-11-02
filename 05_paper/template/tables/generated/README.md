# `tables/generated/` — output directory

Nothing here is written by hand. `../make_tables.py` writes, per table name:

* `<name>.tex` — a booktabs `tabular` **body** (no float, no caption, no label;
  `main.tex` owns those, so labels cannot collide)
* `<name>.md` — the same table in Markdown, for the draft

This directory is empty until an experiment has written a
`04_experiments/results/summary_<experiment>.json`. `main.tex` falls back to a
placeholder box rather than failing to compile.

Regenerate with:

```bash
python tables/make_tables.py \
       --summary ../../04_experiments/results/summary_main.json \
       --out-dir tables/generated --name main-results --format both
```
