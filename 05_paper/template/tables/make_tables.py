#!/usr/bin/env python
"""make_tables.py -- build a booktabs results table from a summary JSON.

Input : 04_experiments/results/summary_<experiment>.json (tools/CONTRACTS.md
        section 4), i.e. the file the experiment harness aggregates from the
        per-run results.json files.
Output: <name>.tex   a booktabs tabular body (meant to be \\input inside the
                     table float in main.tex, which owns the caption and label)
        <name>.md    the same table in Markdown, for the draft

What is refused, on purpose (exit 2), because a table that quietly prints
"nan" or "0.0" is indistinguishable from a result:
  * the summary has no `stats` block, or a config in `configs` has no entry;
  * mean / std / ci95 is missing or not numeric;
  * `n` is missing and cannot be derived from `per_run`;
  * `n` disagrees with len(per_run[config]) -- one of the two is wrong;
  * a p-value appears without its multiple-comparison correction and family
    size, or an effect size without a name (CONTRACTS section 4 requires both).

Usage
  python tables/make_tables.py --summary 04_experiments/results/summary_main.json \
         --out-dir tables/generated --name main-results
  python tables/make_tables.py --summary ... --format ci --decimals 4 --json

Exit codes: 0 ok, 1 write failure, 2 usage error or missing/inconsistent data.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import NoReturn

HERE = Path(__file__).resolve().parent          # .../05_paper/template/tables
TEMPLATE_DIR = HERE.parent


def find_repo_root(start: Path) -> Path:
    for cand in [start, *start.parents]:
        if (cand / "04_experiments").is_dir() or (cand / ".git").is_dir():
            return cand
    return start


REPO_ROOT = find_repo_root(TEMPLATE_DIR)
DEFAULT_OUT = TEMPLATE_DIR / "tables" / "generated"


def die(msg: str, code: int = 2) -> NoReturn:
    print(f"make_tables: error: {msg}", file=sys.stderr)
    raise SystemExit(code)


# -----------------------------------------------------------------------------
# loading + validation
# -----------------------------------------------------------------------------
def load_summary(path: Path) -> dict:
    try:
        with path.open(encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        die(f"summary file not found: {path}")
    except json.JSONDecodeError as exc:
        die(f"{path} is not valid JSON: {exc}")
    except OSError as exc:
        die(f"cannot read {path}: {exc}")
    if not isinstance(data, dict):
        die(f"{path} is not a JSON object -- expected a summary_*.json")
    if data.get("toy") is True:
        die(f"{path} is a TOY summary (CONTRACTS section 5); toy numbers may "
            f"never appear in a paper")
    return data


def number(value, what: str) -> float:
    if isinstance(value, bool) or value is None:
        die(f"{what} is missing -- refusing to render a table that would print 'nan'")
    if isinstance(value, (int, float)):
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            die(f"{what} is {value!r}; refusing to render a non-finite value")
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            pass
    die(f"{what} is not a number (got {value!r})")


def rows_from_summary(summary: dict, fmt: str, metric_filter: str | None) -> tuple[list[dict], str]:
    metric = summary.get("metric")
    if metric_filter:
        if metric and metric != metric_filter:
            die(f"summary metric is {metric!r} but --metric {metric_filter!r} was "
                f"requested; refusing to mislabel the table")
        metric = metric_filter
    if not metric:
        die("summary has no 'metric' field, so the table cannot say what it measures")

    stats = summary.get("stats")
    if not isinstance(stats, dict) or not stats:
        die("summary has no 'stats' block (CONTRACTS section 4)")

    configs = summary.get("configs") or list(stats)
    if not isinstance(configs, list) or not configs:
        die("summary has an empty 'configs' list")

    per_run = summary.get("per_run") or {}
    if not isinstance(per_run, dict):
        die("'per_run' must be an object mapping config -> list of values")

    rows = []
    for config in configs:
        config = str(config)
        block = stats.get(config)
        if not isinstance(block, dict):
            die(f"metric {metric!r} has no stats for config {config!r} -- "
                f"refusing to render (a missing cell is not a zero)")
        mean = number(block.get("mean"), f"{config}: mean of {metric}")
        std = None
        ci = None
        if fmt in ("mean-std", "both"):
            std = number(block.get("std"), f"{config}: std of {metric}")
        if fmt in ("ci", "both"):
            raw_ci = block.get("ci95")
            if not isinstance(raw_ci, (list, tuple)) or len(raw_ci) != 2:
                die(f"{config}: ci95 must be a two-element list, got {raw_ci!r}")
            ci = (number(raw_ci[0], f"{config}: ci95[0]"),
                  number(raw_ci[1], f"{config}: ci95[1]"))
            if ci[0] > ci[1]:
                die(f"{config}: ci95 is reversed ({ci[0]} > {ci[1]})")
            if not (ci[0] <= mean <= ci[1]):
                die(f"{config}: mean {mean} lies outside its 95% CI {ci} -- "
                    f"one of the two numbers is wrong")

        n = block.get("n")
        runs = per_run.get(config)
        if n is None:
            if isinstance(runs, list) and runs:
                n = len(runs)
            else:
                die(f"{config}: no 'n' and no 'per_run' list, so the table cannot "
                    f"state how many runs a cell rests on")
        n = int(number(n, f"{config}: n"))
        if n <= 0:
            die(f"{config}: n={n} is not a positive count")
        if isinstance(runs, list) and runs and len(runs) != n:
            die(f"{config}: n={n} but per_run has {len(runs)} values -- the summary "
                f"contradicts itself")

        rows.append({
            "config": config,
            "mean": mean,
            "std": std,
            "ci": ci,
            "n": n,
            "ci_method": block.get("ci_method"),
            "n_boot": block.get("n_boot"),
            "ci_seed": block.get("ci_seed"),
        })

    paired = summary.get("paired")
    if isinstance(paired, dict):
        if paired.get("p_value") is not None or paired.get("p_adjusted") is not None:
            correction = paired.get("correction")
            if not isinstance(correction, dict) or not correction.get("method") \
                    or correction.get("family_size") in (None, ""):
                die("summary reports a p-value without a correction method and "
                    "family size (CONTRACTS section 4) -- a bare p-value in the "
                    "paper is not reportable")
        effect = paired.get("effect_size")
        if isinstance(effect, dict) and effect.get("value") is not None and not effect.get("name"):
            die("summary reports an effect size with no name")
    return rows, str(metric)


# -----------------------------------------------------------------------------
# rendering
# -----------------------------------------------------------------------------
def tex_escape(text: str) -> str:
    out = str(text)
    for old, new in (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                     ("#", r"\#"), ("_", r"\_"), ("$", r"\$")):
        out = out.replace(old, new)
    return out


def fmt_p(p: float, tex: bool = True) -> str:
    if p < 0.001:
        return "$p<0.001$" if tex else "p<0.001"
    return f"$p={p:.3f}$" if tex else f"p={p:.3f}"


_EFFECT_SYMBOLS = {"cohens_d": ("Cohen's", "d"),
                   "cliffs_delta": ("Cliff's", r"\delta"),
                   "hedges_g": ("Hedges'", "g")}


def paired_note(paired: dict, tex: bool = True) -> str:
    if not isinstance(paired, dict):
        return ""
    bits: list[str] = []
    test = paired.get("test")
    label = (str(test)[:1].upper() + str(test)[1:]) if test else ""
    p_adj = paired.get("p_adjusted", paired.get("p_value"))
    if p_adj is not None:
        p_txt = fmt_p(float(p_adj), tex=tex)
        prefix = f"Paired {tex_escape(label)} test" if label else "Paired test"
        bits.append(f"{prefix}: {p_txt}")
    correction = paired.get("correction")
    if isinstance(correction, dict) and correction.get("method"):
        fam = correction.get("family_size")
        bits.append(f"{tex_escape(correction['method'])}-corrected, family size {fam}")
    effect = paired.get("effect_size")
    if isinstance(effect, dict) and effect.get("value") is not None and effect.get("name"):
        raw_name = str(effect["name"])
        pretty, symbol = _EFFECT_SYMBOLS.get(raw_name, (tex_escape(raw_name), None))
        value = float(effect["value"])
        if tex:
            bits.append(f"{pretty} ${symbol}={value:.2f}$" if symbol
                        else f"{pretty} {value:.2f}")
        else:
            plain = {"d": "d", "g": "g", r"\delta": "delta"}.get(symbol or "", symbol or "")
            bits.append(f"{pretty} {plain}={value:.2f}")
    if paired.get("n_pairs") is not None:
        n_pairs = int(paired["n_pairs"])
        bits.append(f"$n_{{pairs}}={n_pairs}$" if tex else f"n_pairs={n_pairs}")
    if not bits:
        return ""
    return "; ".join(bits) + "."


def build_tex(rows: list[dict], metric: str, fmt: str, decimals: int,
              source: str, caption: str | None, label: str, paired) -> str:
    def f(value: float) -> str:
        return f"{value:.{decimals}f}"

    header = ["Config"]
    align = "l"
    if fmt in ("mean-std", "both"):
        header.append(r"Mean $\pm$ std")
        align += "r"
    if fmt in ("ci", "both"):
        header.append("95\\% CI")
        align += "r"
    header.append("$n$")
    align += "r"

    lines = []
    for row in rows:
        cells = [tex_escape(row["config"])]
        if fmt in ("mean-std", "both"):
            cells.append(f"{f(row['mean'])} $\\pm$ {f(row['std'])}")
        if fmt in ("ci", "both"):
            cells.append(f"[{f(row['ci'][0])}, {f(row['ci'][1])}]")
        cells.append(str(row["n"]))
        lines.append(" & ".join(cells) + r" \\")

    methods = sorted({str(r["ci_method"]) for r in rows if r.get("ci_method")})
    boots = sorted({int(r["n_boot"]) for r in rows if r.get("n_boot") is not None})
    seeds = sorted({int(r["ci_seed"]) for r in rows if r.get("ci_seed") is not None})

    meta_bits: list[str] = []
    if fmt in ("ci", "both") and methods:
        text = tex_escape("/".join(methods)) + " CI"
        if boots:
            text += f", {boots[0]} resamples"
        if seeds:
            text += f", ci seed {seeds[0]}"
        meta_bits.append(text)

    note = paired_note(paired, tex=True)
    if note:
        meta_bits.append(note)
    prov = (f"% Generated by 05_paper/template/tables/make_tables.py -- do not edit.\n"
            f"% Source : {source}\n"
            f"% Metric : {metric}; format={fmt}; decimals={decimals}\n"
            f"% Rows   : {len(rows)}; n and intervals copied from the summary, not recomputed\n")

    caption_tex = tex_escape(caption) if caption else (
        f"TODO(caption): {tex_escape(metric)} per configuration, mean over the seeds "
        f"in the cited summary file; state the dataset, the direction of the metric "
        f"and what the interval is."
    )
    prov += (f"% Caption for the table float in main.tex:\n%   {caption_tex}\n"
             f"% Label for the table float in main.tex: tab:{label}\n")

    body = "\n".join(
        [r"\begin{tabular}{" + align + "}",
         r"\toprule",
         " & ".join(header) + r" \\",
         r"\midrule",
         *lines,
         r"\bottomrule",
         r"\end{tabular}"]
    )
    if meta_bits:
        body += "\n\n" + r"{\footnotesize " + "; ".join(meta_bits) + "}"
    return prov + body + "\n"


def build_md(rows: list[dict], metric: str, fmt: str, decimals: int,
             source: str, caption: str | None, paired) -> str:
    def f(value: float) -> str:
        return f"{value:.{decimals}f}"

    header = ["Config"]
    if fmt in ("mean-std", "both"):
        header.append("Mean ± std")
    if fmt in ("ci", "both"):
        header.append("95% CI")
    header.append("n")
    lines = ["| " + " | ".join(header) + " |",
             "|" + "|".join(["---"] * len(header)) + "|"]
    for row in rows:
        cells = [f"`{row['config']}`"]
        if fmt in ("mean-std", "both"):
            cells.append(f"{f(row['mean'])} ± {f(row['std'])}")
        if fmt in ("ci", "both"):
            cells.append(f"[{f(row['ci'][0])}, {f(row['ci'][1])}]")
        cells.append(str(row["n"]))
        lines.append("| " + " | ".join(cells) + " |")

    note = paired_note(paired, tex=False)
    out = [f"<!-- generated by 05_paper/template/tables/make_tables.py from {source} -->",
           f"<!-- metric: {metric} -->", ""]
    if caption:
        out.append(f"**{caption}**")
        out.append("")
    out.extend(lines)
    if note:
        out += ["", f"_{note}_"]
    out += ["", f"_Source: `{source}` (metric `{metric}`); values copied from the "
                f"summary file, not recomputed._", ""]
    return "\n".join(out)


# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
def sanitise_name(raw: str) -> str:
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", raw.strip()).replace("_", "-").strip("-.")
    if not name:
        die(f"name {raw!r} is empty after sanitising")
    return name


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Build a booktabs table + Markdown twin from a summary JSON.",
        epilog="Refuses to render a metric that is missing (exit 2).",
    )
    ap.add_argument("--summary", required=True, help="path to summary_<experiment>.json")
    ap.add_argument("--out-dir", default=str(DEFAULT_OUT))
    ap.add_argument("--name", required=True, help="output basename, e.g. main-results")
    ap.add_argument("--format", choices=("mean-std", "ci", "both"), default="mean-std",
                    help="mean ± std, 95%% CI, or both (default: mean-std)")
    ap.add_argument("--decimals", type=int, default=3)
    ap.add_argument("--metric", default=None,
                    help="assert the summary's metric; refuses if it disagrees")
    ap.add_argument("--caption", default=None, help="caption text (LaTeX/plain)")
    ap.add_argument("--label", default=None, help="LaTeX label without the tab: prefix")
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args(argv)

    if args.decimals < 0 or args.decimals > 8:
        die("--decimals must be between 0 and 8")
    summary_path = Path(args.summary)
    if not summary_path.is_absolute():
        summary_path = (Path.cwd() / summary_path).resolve()
    if not summary_path.is_file():
        summary_path = (REPO_ROOT / args.summary).resolve()
    if not summary_path.is_file():
        die(f"summary file not found: {args.summary}")

    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()

    summary = load_summary(summary_path)
    rows, metric = rows_from_summary(summary, args.format, args.metric)

    name = sanitise_name(args.name)
    try:
        rel_source = summary_path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        rel_source = summary_path.as_posix()

    tex = build_tex(rows, metric, args.format, args.decimals, rel_source,
                    args.caption, args.label or name, summary.get("paired"))
    md = build_md(rows, metric, args.format, args.decimals, rel_source,
                  args.caption, summary.get("paired"))

    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        tex_path = out_dir / f"{name}.tex"
        md_path = out_dir / f"{name}.md"
        tex_path.write_text(tex, encoding="utf-8", newline="\n")
        md_path.write_text(md, encoding="utf-8", newline="\n")
    except OSError as exc:
        die(f"cannot write into {out_dir}: {exc}", 1)

    if args.as_json:
        print(json.dumps({"summary": rel_source, "metric": metric,
                          "rows": len(rows), "tex": tex_path.as_posix(),
                          "md": md_path.as_posix()}, indent=2, ensure_ascii=False))
    else:
        print(f"make_tables: {name}: {len(rows)} row(s), metric {metric!r}, "
              f"format {args.format} from {rel_source}")
        for row in rows:
            cell = f"{row['mean']:.{args.decimals}f}"
            if row["std"] is not None:
                cell += f" +- {row['std']:.{args.decimals}f}"
            if row["ci"]:
                cell += f"  CI [{row['ci'][0]:.{args.decimals}f}, {row['ci'][1]:.{args.decimals}f}]"
            print(f"  {row['config']:<20} {cell}  n={row['n']}")
        print(f"  wrote {tex_path}")
        print(f"  wrote {md_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
