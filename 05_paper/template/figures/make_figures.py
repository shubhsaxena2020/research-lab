#!/usr/bin/env python
"""make_figures.py -- build paper figures from results files, and nothing else.

Every plotted value comes from a JSON file that an experiment wrote:
  * a results file (tools/CONTRACTS.md section 2), or
  * 04_experiments/RESULTS-INDEX.json (section 3), which maps an id used in the
    draft to "file + dotted key".

Nothing here invents, averages or smooths a number. If a key is missing the
script exits 2 and names it -- an empty or all-zero chart is worse than no chart,
because it looks like a result.

Outputs, per figure `<name>` in --out-dir (default 05_paper/template/figures/generated):
  <name>.csv   the plotted rows, with the id / key / file each value came from
  <name>.svg   hand-written SVG (stdlib only: axes, ticks, labels, values)
  <name>.tex   a LaTeX fragment: \\includegraphics of the PDF when it exists,
               otherwise a visible placeholder, so the paper still compiles
  <name>.pdf   only when matplotlib is importable (optional; not installed here)
  <name>.png   ditto

CLI
  python figures/make_figures.py --index 04_experiments/RESULTS-INDEX.json \
         --figure main-accuracy
  python figures/make_figures.py --results 04_experiments/results/main_baseline.json \
         --figure smoke --metric accuracy f1_macro
  # which entries belong to a figure:
  #   every index entry whose id is `<figure>` or starts with `<figure>.`
  #   (the trailing part becomes the bar label), optionally filtered by --metric

Exit codes: 0 ok, 1 write/render failure, 2 usage error or missing data.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from pathlib import Path
from typing import NoReturn
from xml.sax.saxutils import escape, quoteattr

# -----------------------------------------------------------------------------
# paths
# -----------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent          # .../05_paper/template/figures
TEMPLATE_DIR = HERE.parent                      # .../05_paper/template


def find_repo_root(start: Path) -> Path:
    for cand in [start, *start.parents]:
        if (cand / "04_experiments").is_dir() or (cand / ".git").is_dir():
            return cand
    return start


REPO_ROOT = find_repo_root(TEMPLATE_DIR)
DEFAULT_OUT = TEMPLATE_DIR / "figures" / "generated"

PALETTE = ["#3b6ea5", "#c8553d", "#5b8c5a", "#8d6a9f", "#d9a441", "#4f6d7a"]


def die(msg: str, code: int = 2) -> NoReturn:
    print(f"make_figures: error: {msg}", file=sys.stderr)
    raise SystemExit(code)


# -----------------------------------------------------------------------------
# data loading
# -----------------------------------------------------------------------------
def load_json(path: Path):
    try:
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        die(f"file not found: {path}")
    except json.JSONDecodeError as exc:
        die(f"{path} is not valid JSON: {exc}")
    except OSError as exc:
        die(f"cannot read {path}: {exc}")


def resolve_data_path(raw: str, index_path: Path) -> Path | None:
    """Resolve a path from the index: as given, next to the index, or repo-root relative."""
    p = Path(raw)
    candidates = [p] if p.is_absolute() else [
        Path.cwd() / p, index_path.parent / p, REPO_ROOT / p,
    ]
    for cand in candidates:
        if cand.is_file():
            return cand.resolve()
    return None


def lookup_dotted(obj, dotted: str):
    cur = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            raise KeyError(dotted)
        cur = cur[part]
    return cur


def as_number(value, what: str) -> float:
    if isinstance(value, bool) or value is None:
        die(f"{what} is not a number (got {value!r}); refusing to plot it")
    if isinstance(value, (int, float)):
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            die(f"{what} is {value!r}; refusing to plot a non-finite value")
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            pass
    die(f"{what} is not a number (got {value!r}); refusing to plot it")


def check_not_toy(data, path: Path, allow_toy: bool) -> None:
    if isinstance(data, dict) and data.get("toy") is True and not allow_toy:
        die(f"{path} is a TOY file (tools/CONTRACTS.md section 5). "
            f"Toy numbers may never appear in a paper; pass --allow-toy only for "
            f"a pipeline smoke test, and never cite the output.")


def series_from_index(index_path: Path, figure: str, metrics: list[str],
                      allow_toy: bool) -> list[dict]:
    index = load_json(index_path)
    entries = index.get("entries")
    if not isinstance(entries, list):
        die(f"{index_path} has no 'entries' list -- not a RESULTS-INDEX file")

    prefixes = (figure + ".", figure + "/")
    selected = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        eid = str(entry.get("id", ""))
        if eid == figure or eid.startswith(prefixes):
            selected.append(entry)
    if not selected:
        known = sorted({str(e.get("id", "")) for e in entries if isinstance(e, dict)})
        die(f"no index entry matches figure {figure!r}. Known ids:\n  "
            + "\n  ".join(known[:40])
            + ("\n  ..." if len(known) > 40 else ""))

    if metrics:
        selected = [e for e in selected if e.get("key") in metrics]
        if not selected:
            die(f"figure {figure!r} has no entry with key in {metrics}")

    rows = []
    for entry in selected:
        eid = str(entry.get("id", ""))
        key = entry.get("key")
        raw_file = entry.get("file")
        if not key or not raw_file:
            die(f"index entry {eid!r} is missing 'key' or 'file'")
        data_path = resolve_data_path(str(raw_file), index_path)
        if data_path is None:
            die(f"index entry {eid!r} points at {raw_file!r}, which does not exist "
                f"(tried cwd, {index_path.parent}, {REPO_ROOT})")
        if entry.get("toy") is True and not allow_toy:
            die(f"index entry {eid!r} is marked toy=true (CONTRACTS section 5); "
                f"toy numbers may never appear in a paper")
        data = load_json(data_path)
        check_not_toy(data, data_path, allow_toy)
        try:
            value = lookup_dotted(data, str(key))
        except KeyError:
            die(f"metric key {key!r} does not exist in {data_path} (entry {eid!r}). "
                f"Top-level keys: {sorted(k for k in data if not k.startswith('_'))}")
        label = eid[len(figure):].strip("._/") or eid
        rows.append({
            "id": eid,
            "key": str(key),
            "file": _rel(data_path),
            "series": label,
            "value": as_number(value, f"{eid} ({key})"),
        })
    return rows


def series_from_results(results_path: Path, metrics: list[str],
                        allow_toy: bool) -> list[dict]:
    data = load_json(results_path)
    check_not_toy(data, results_path, allow_toy)
    if not isinstance(data, dict):
        die(f"{results_path} is not a JSON object")

    flat: dict[str, object] = {}
    for key, value in data.items():
        if key.startswith("_"):
            continue
        if isinstance(value, dict):          # one level of nesting is allowed
            for sub, subval in value.items():
                flat[f"{key}.{sub}"] = subval
        else:
            flat[key] = value

    available = sorted(k for k, v in flat.items()
                       if isinstance(v, (int, float)) and not isinstance(v, bool))
    if metrics:
        chosen = []
        for metric in metrics:
            if metric not in flat:
                die(f"metric {metric!r} does not exist in {results_path}. "
                    f"Numeric metrics present: {available}")
            chosen.append(metric)
    else:
        chosen = available
        if not chosen:
            die(f"{results_path} contains no numeric metrics to plot")

    rows = []
    for metric in chosen:
        rows.append({
            "id": metric,
            "key": metric,
            "file": _rel(results_path),
            "series": metric,
            "value": as_number(flat[metric], metric),
        })
    return rows


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


# -----------------------------------------------------------------------------
# formatting helpers
# -----------------------------------------------------------------------------
def fmt_num(value: float) -> str:
    magnitude = abs(value)
    if magnitude != 0 and (magnitude < 1e-3 or magnitude >= 1e5):
        return f"{value:.3e}"
    if magnitude >= 100:
        return f"{value:.1f}"
    if magnitude >= 1:
        return f"{value:.3f}"
    return f"{value:.4g}"


def fmt_tick(value: float, step: float) -> str:
    """Tick labels follow the step, so a 0.2 step prints 0.2 and not 0.2000."""
    if step <= 0:
        return fmt_num(value)
    decimals = max(0, min(6, -int(math.floor(math.log10(step)))))
    text = f"{value:.{decimals}f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return "0" if text in ("-0", "") else text


def nice_num(x: float) -> float:
    if x <= 0:
        return 1.0
    exponent = math.floor(math.log10(x))
    fraction = x / (10 ** exponent)
    for candidate in (1.0, 2.0, 2.5, 5.0, 10.0):
        if fraction <= candidate:
            return candidate * (10 ** exponent)
    return 10.0 * (10 ** exponent)


def axis_ticks(values: list[float]) -> tuple[float, float, float]:
    """Return (lo, hi, step) covering the values and z=0, with a readable step."""
    lo = min(0.0, min(values))
    hi = max(0.0, max(values))
    if hi == lo:
        hi = lo + 1.0
    span = hi - lo
    step = nice_num(span / 5.0) or 1.0
    for _ in range(20):
        tick_lo = math.floor(lo / step) * step
        tick_hi = math.ceil(hi / step) * step
        if (tick_hi - tick_lo) / step <= 10:
            return tick_lo, tick_hi, step
        step = nice_num(step * 2)
    return math.floor(lo / step) * step, math.ceil(hi / step) * step, step


def wrap_label(text: str, width: int = 16, max_lines: int = 2) -> list[str]:
    words = re.sub(r"[_/]+", " ", text).split()
    lines: list[str] = []
    current = ""
    for word in words:
        if not current:
            current = word
        elif len(current) + 1 + len(word) <= width:
            current += " " + word
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    if not lines:
        lines = ["(unnamed)"]
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][: max(width - 3, 1)] + "..."
    return lines


# -----------------------------------------------------------------------------
# SVG
# -----------------------------------------------------------------------------
def build_svg(rows: list[dict], title: str, xlabel: str, ylabel: str,
              provenance: str) -> str:
    width, height = 720, 430
    left, right, top, bottom = 78, 28, 52, 92
    plot_w = width - left - right
    plot_h = height - top - bottom

    values = [r["value"] for r in rows]
    tick_lo, tick_hi, step = axis_ticks(values)

    def y_of(value: float) -> float:
        frac = (value - tick_lo) / (tick_hi - tick_lo)
        return top + plot_h - frac * plot_h

    zero_y = y_of(0.0)

    # ticks
    ticks: list[float] = []
    tick = tick_lo
    guard = 0
    while tick <= tick_hi + step / 2 and guard < 40:
        ticks.append(round(tick, 12))
        tick += step
        guard += 1

    parts: list[str] = []
    parts.append('<?xml version="1.0" encoding="UTF-8"?>')
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" '
        f'aria-label={quoteattr(f"{title}: bar chart of {len(rows)} values")}>')
    parts.append(f"  <title>{escape(title)}</title>")
    parts.append(f"  <desc>{escape(provenance)}</desc>")
    parts.append('  <rect x="0" y="0" width="100%" height="100%" fill="#ffffff"/>')

    # title + axis titles
    parts.append(
        f'  <text x="{left}" y="28" font-family="Helvetica, Arial, sans-serif" '
        f'font-size="15" font-weight="bold" fill="#1a1a1a">{escape(title)}</text>')
    parts.append(
        f'  <text x="{left + plot_w / 2:.1f}" y="{height - 16}" '
        f'text-anchor="middle" font-family="Helvetica, Arial, sans-serif" '
        f'font-size="12" fill="#333333">{escape(xlabel)}</text>')
    parts.append(
        f'  <text x="18" y="{top + plot_h / 2:.1f}" text-anchor="middle" '
        f'transform="rotate(-90 18 {top + plot_h / 2:.1f})" '
        f'font-family="Helvetica, Arial, sans-serif" font-size="12" '
        f'fill="#333333">{escape(ylabel)}</text>')

    # grid + y tick labels
    for value in ticks:
        y = y_of(value)
        parts.append(
            f'  <line x1="{left}" y1="{y:.2f}" x2="{left + plot_w}" y2="{y:.2f}" '
            f'stroke="#e3e3e3" stroke-width="1"/>')
        parts.append(
            f'  <text x="{left - 8}" y="{y + 4:.2f}" text-anchor="end" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="11" '
            f'fill="#444444">{escape(fmt_tick(value, step))}</text>')

    # bars
    slot = plot_w / len(rows)
    bar_w = max(10.0, min(64.0, slot * 0.62))
    for index, row in enumerate(rows):
        cx = left + slot * (index + 0.5)
        value = row["value"]
        y_val = y_of(value)
        bar_top = min(y_val, zero_y)
        bar_h = abs(zero_y - y_val)
        colour = PALETTE[index % len(PALETTE)]
        parts.append(
            f'  <rect x="{cx - bar_w / 2:.2f}" y="{bar_top:.2f}" width="{bar_w:.2f}" '
            f'height="{max(bar_h, 1.0):.2f}" fill="{colour}" fill-opacity="0.88" '
            f'stroke="{colour}" stroke-width="1">'
            f'<title>{escape(row["series"])} = {escape(fmt_num(value))}</title></rect>')
        label_y = bar_top - 6 if value >= 0 else bar_top + bar_h + 13
        parts.append(
            f'  <text x="{cx:.2f}" y="{label_y:.2f}" text-anchor="middle" '
            f'font-family="Helvetica, Arial, sans-serif" font-size="10" '
            f'fill="#222222">{escape(fmt_num(value))}</text>')
        # x tick + wrapped categorical label
        parts.append(
            f'  <line x1="{cx:.2f}" y1="{top + plot_h}" x2="{cx:.2f}" '
            f'y2="{top + plot_h + 4}" stroke="#333333" stroke-width="1"/>')
        lines = wrap_label(row["series"])
        for line_no, line in enumerate(lines):
            parts.append(
                f'  <text x="{cx:.2f}" y="{top + plot_h + 18 + line_no * 12:.2f}" '
                f'text-anchor="middle" font-family="Helvetica, Arial, sans-serif" '
                f'font-size="10.5" fill="#333333">{escape(line)}</text>')

    # axes drawn last so they sit above the bars
    parts.append(
        f'  <line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" '
        f'stroke="#1a1a1a" stroke-width="1.2"/>')
    parts.append(
        f'  <line x1="{left}" y1="{zero_y:.2f}" x2="{left + plot_w}" '
        f'y2="{zero_y:.2f}" stroke="#1a1a1a" stroke-width="1.2"/>')
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


# -----------------------------------------------------------------------------
# LaTeX fragment
# -----------------------------------------------------------------------------
def tex_escape(text: str) -> str:
    for old, new in (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                     ("#", r"\#"), ("_", r"\_"), ("$", r"\$")):
        text = text.replace(old, new)
    return text


def build_tex(name: str, rows: list[dict], title: str, caption: str,
              label: str, source: str, rel_dir: str) -> str:
    """Body-only fragment: main.tex owns the figure float, caption and label.

    Emitting a whole float here would nest inside the float in main.tex, which
    is a hard LaTeX error ("Not in outer par mode"). Caption and label are
    therefore written as comments for pasting, exactly like the table generator.
    """
    ids = ", ".join(r["id"] for r in rows[:6]) + (" ..." if len(rows) > 6 else "")
    cap = caption or (
        f"TODO(caption): what is plotted, on what data, over how many runs, and "
        f"what the reader should notice. Values traced to index ids: {ids}."
    )
    stem = f"{rel_dir}/{name}"
    return f"""% Generated by 05_paper/template/figures/make_figures.py -- do not edit by hand.
% Figure : {name}
% Source : {source}
% Rows   : {len(rows)}
% Caption for the figure float in main.tex:
%   {cap}
% Label for the float in main.tex: {label}
% Note   : body only -- no float, no caption, no label, so it can be \input
%          inside the figure environment in main.tex without nesting. Paths are
%          relative to 05_paper/template/. A PDF exists only when matplotlib is
%          installed; without it the fallback box keeps the paper compiling.
\IfFileExists{{{stem}.pdf}}{{%
  \includegraphics[width=0.85\linewidth]{{{stem}.pdf}}%
}}{{\fbox{{\parbox[c][4cm][c]{{0.82\linewidth}}{{\centering\small
  Figure \texttt{{{tex_escape(name)}}} has no PDF: matplotlib is not installed.
  The vector preview is \texttt{{{tex_escape(stem)}.svg}} and the plotted values
  are in \texttt{{{tex_escape(stem)}.csv}}.}}}}}}
"""


# -----------------------------------------------------------------------------
# optional matplotlib render
# -----------------------------------------------------------------------------
def render_with_matplotlib(rows: list[dict], name: str, out_dir: Path,
                           title: str, ylabel: str, xlabel: str) -> list[Path]:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("make_figures: matplotlib not installed -> SVG + .tex only "
              "(install it to get PDF/PNG; see BUILD.md)")
        return []
    try:
        fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=200)
        positions = range(len(rows))
        values = [r["value"] for r in rows]
        colours = [PALETTE[i % len(PALETTE)] for i in positions]
        ax.bar(positions, values, width=0.62, color=colours, edgecolor=colours)
        ax.set_xticks(list(positions))
        ax.set_xticklabels([r["series"] for r in rows], rotation=0, fontsize=8)
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        ax.set_title(title, fontsize=10, loc="left")
        ax.grid(axis="y", color="#e3e3e3", linewidth=0.8)
        ax.set_axisbelow(True)
        ax.axhline(0.0, color="#1a1a1a", linewidth=0.9)
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)
        fig.tight_layout()
        pdf = out_dir / f"{name}.pdf"
        png = out_dir / f"{name}.png"
        fig.savefig(pdf)
        fig.savefig(png, dpi=200)
        plt.close(fig)
        return [pdf, png]
    except Exception as exc:  # backend trouble must not lose the SVG we already wrote
        print(f"make_figures: warning: matplotlib render failed ({exc}); kept SVG",
              file=sys.stderr)
        return []


# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
def sanitise_name(raw: str) -> str:
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", raw.strip())
    name = name.replace("_", "-").strip("-.")
    if not name:
        die(f"figure name {raw!r} is empty after sanitising")
    return name


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Build a figure (CSV + SVG + LaTeX fragment) from results files.",
        epilog="Refuses to plot a metric that does not exist (exit 2).",
    )
    source = ap.add_mutually_exclusive_group(required=True)
    source.add_argument("--index", help="04_experiments/RESULTS-INDEX.json")
    source.add_argument("--results", help="a single results.json file")
    ap.add_argument("--out-dir", default=str(DEFAULT_OUT))
    ap.add_argument("--figure", required=True,
                    help="figure name; in --index mode also the id prefix "
                         "(entries `NAME.<label>` are plotted)")
    ap.add_argument("--metric", nargs="+", action="extend", default=[],
                    help="metric key(s) to plot (default: all numeric metrics)")
    ap.add_argument("--title", default=None)
    ap.add_argument("--xlabel", default="Condition")
    ap.add_argument("--ylabel", default="Value")
    ap.add_argument("--caption", default=None, help="LaTeX caption for the .tex fragment")
    ap.add_argument("--allow-toy", action="store_true",
                    help="only for pipeline smoke tests; never cite the output")
    args = ap.parse_args(argv)

    name = sanitise_name(args.figure)
    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    label = "fig:" + name

    if args.index:
        index_path = Path(args.index)
        if not index_path.is_absolute():
            index_path = (Path.cwd() / index_path).resolve()
        if not index_path.is_file():
            index_path = (REPO_ROOT / args.index).resolve()
        if not index_path.is_file():
            die(f"index file not found: {args.index}")
        rows = series_from_index(index_path, args.figure, args.metric, args.allow_toy)
        source_text = _rel(index_path)
    else:
        results_path = Path(args.results)
        if not results_path.is_absolute():
            results_path = (Path.cwd() / results_path).resolve()
        if not results_path.is_file():
            results_path = (REPO_ROOT / args.results).resolve()
        if not results_path.is_file():
            die(f"results file not found: {args.results}")
        rows = series_from_results(results_path, args.metric, args.allow_toy)
        source_text = _rel(results_path)

    if not rows:
        die("no data rows to plot")

    rows.sort(key=lambda r: r["series"])
    title = args.title or re.sub(r"[-_]+", " ", name).strip().title()

    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        csv_path = out_dir / f"{name}.csv"
        with csv_path.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.writer(fh, lineterminator="\n")
            writer.writerow(["series", "value", "id", "key", "file"])
            for row in rows:
                writer.writerow([row["series"], repr(row["value"]), row["id"],
                                 row["key"], row["file"]])

        svg_path = out_dir / f"{name}.svg"
        provenance = (f"figure={name}; source={source_text}; "
                      + "; ".join(f"{r['id']}={r['value']!r} from {r['file']}"
                                  for r in rows))
        svg_path.write_text(build_svg(rows, title, args.xlabel, args.ylabel, provenance),
                            encoding="utf-8", newline="\n")

        try:
            rel_dir = out_dir.relative_to(TEMPLATE_DIR).as_posix()
        except ValueError:
            rel_dir = out_dir.as_posix()
        tex_path = out_dir / f"{name}.tex"
        tex_path.write_text(
            build_tex(name, rows, title, args.caption, label, source_text, rel_dir),
            encoding="utf-8", newline="\n")
    except OSError as exc:
        die(f"cannot write into {out_dir}: {exc}", 1)

    extras = render_with_matplotlib(rows, name, out_dir, title, args.ylabel, args.xlabel)

    print(f"make_figures: {name}: {len(rows)} value(s) from {source_text}")
    for row in rows:
        print(f"  {row['series']:<28} {fmt_num(row['value']):>10}   [{row['id']}]")
    print(f"  wrote {csv_path}")
    print(f"  wrote {svg_path}")
    print(f"  wrote {tex_path}")
    for path in extras:
        print(f"  wrote {path}")
    if not extras:
        print("  (no PDF/PNG: matplotlib is not installed -- the .tex fragment "
              "falls back to a placeholder)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
