"""Ablation-table generator: Markdown + booktabs LaTeX from a summary JSON.

Reads only files under ``04_experiments/results/`` in the shapes allowed by
CONTRACTS.md section 4 (single-metric summary) and its multi-metric ablation
generalisation.  Two rules drive the design:

1. Never print a number that is not in the results file.  A missing metric or
   config raises ``ValueError`` with the available names — no NaN, no 0.
2. Never bold a winner that is inside the noise.  A cell is bolded only when a
   paired test in the summary file says the best-vs-runner-up difference is
   significant; if the p-value is above alpha, the difference is footnoted as
   not significant and nothing is bolded.

Accepted JSON shapes (detected automatically)
---------------------------------------------
A. contract single metric::

       {"experiment": "main", "configs": [...], "metric": "accuracy",
        "per_run": {"baseline": [...], "ours": [...]},
        "stats": {"baseline": {...}}, "paired": {...}}

B. multi-metric nested::

       {"configs": [...], "metrics": ["accuracy", "f1_macro"],
        "per_run": {"accuracy": {"baseline": [...]}, ...},
        "stats":   {"accuracy": {"baseline": {...}}},
        "paired":  {"accuracy": {...}}}

C. per-metric blocks: ``{"per_metric": {"accuracy": {per_run, stats, paired}}}``
D. metrics as a dict: ``{"metrics": {"accuracy": {per_run, stats, paired}}}``
E. flat cells: ``{"cells": [{"metric": ..., "config": ..., "values": [...]}]}``
"""

from __future__ import annotations

import json
import math
from pathlib import Path

__all__ = ["ablation_table", "load_summary"]

_LOWER_IS_BETTER = (
    "loss",
    "error",
    "err",
    "rmse",
    "mae",
    "mse",
    "perplexity",
    "ppl",
    "latency",
    "time",
    "cost",
    "flops",
    "params",
    "size_mb",
    "wer",
    "cer",
    "eer",
)

_TEX_ESCAPES = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


# --------------------------------------------------------------------------
# loading / normalising
# --------------------------------------------------------------------------
def load_summary(path) -> dict:
    """Read a summary JSON, raising a readable error if it is unusable."""
    p = Path(path)
    if not p.exists():
        raise ValueError(f"summary file not found: {p}")
    try:
        with p.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    except json.JSONDecodeError as exc:
        raise ValueError(f"summary file is not valid JSON: {p}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"summary file must contain a JSON object: {p}")
    return data


def _metric_specs(metrics) -> list:
    """Normalise the ``metrics`` argument to [{name, label, direction, explicit}]."""
    if isinstance(metrics, str):
        metrics = [metrics]
    if isinstance(metrics, dict):
        metrics = [
            dict(v, name=k) if isinstance(v, dict) else {"name": k, "direction": v}
            for k, v in metrics.items()
        ]
    if not isinstance(metrics, (list, tuple)) or not metrics:
        raise ValueError("metrics must be a non-empty list of names or dicts")

    specs = []
    for item in metrics:
        if isinstance(item, str):
            name, label, direction = item, item, None
        elif isinstance(item, dict):
            name = item.get("name") or item.get("metric")
            if not name:
                raise ValueError(f"metric dict without a name: {item!r}")
            label = item.get("label", name)
            direction = item.get("direction") or item.get("better")
            if direction in {"max", "maximize", "higher"}:
                direction = "higher"
            elif direction in {"min", "minimize", "lower"}:
                direction = "lower"
            elif direction is not None:
                raise ValueError(
                    f"direction must be 'higher'/'lower' for {name!r}, got {direction!r}"
                )
        else:
            raise ValueError(f"unsupported metric spec: {item!r}")
        specs.append(
            {
                "name": name,
                "label": label,
                "direction": direction,
                "explicit": direction is not None,
            }
        )
    return specs


def _looks_lower_is_better(name: str) -> bool:
    n = name.lower()
    return any(tok in n for tok in _LOWER_IS_BETTER)


def _paired_source(data: dict, metric=None):
    """Prefer ``paired_all`` (the full list of comparisons) over ``paired``.

    aggregate.py writes ``paired`` = first comparison only and ``paired_all`` =
    every comparison; using the list lets the table pick the one that actually
    involves the best-vs-second pair instead of guessing.
    """
    for key in ("paired_all", "paired"):
        src = data.get(key)
        if isinstance(src, dict) and metric is not None:
            src = src.get(metric)
        if src:
            return src
    return None


def _normalise(data: dict, path) -> tuple[dict, list]:
    """Return ({metric: {config: cell}}, warnings).  cell = values/stats/paired."""
    warnings = []
    cells: dict[str, dict] = {}

    def put(metric, cfg, values=None, stats=None, paired=None):
        cells.setdefault(metric, {})[cfg] = {
            "values": list(values) if values is not None else None,
            "stats": dict(stats) if isinstance(stats, dict) else None,
            "paired": paired,
        }

    if "cells" in data:
        for row in data["cells"]:
            put(
                row["metric"],
                row["config"],
                row.get("values") or row.get("per_run"),
                row.get("stats"),
                row.get("paired"),
            )
        return cells, warnings

    per_metric = None
    if isinstance(data.get("per_metric"), dict):
        per_metric = data["per_metric"]
    elif isinstance(data.get("metrics"), dict):
        # {"metrics": {"accuracy": {per_run, stats, paired}, ...}}
        per_metric = data["metrics"]

    if per_metric is not None:
        for metric, block in per_metric.items():
            if not isinstance(block, dict):
                raise ValueError(
                    f"{path}: per-metric block for {metric!r} must be an object"
                )
            pr = block.get("per_run") or block.get("runs") or {}
            st = block.get("stats") or {}
            block_paired = _paired_source(block)
            for cfg, vals in pr.items():
                put(metric, cfg, vals, st.get(cfg), block_paired)
            for cfg, s in st.items():
                if cfg not in cells.get(metric, {}):
                    put(metric, cfg, None, s, block_paired)
        return cells, warnings

    per_run = data.get("per_run")
    if not isinstance(per_run, dict):
        raise ValueError(
            f"{path}: unrecognised summary shape — expected 'per_run', "
            "'per_metric', 'metrics' (dict) or 'cells'"
        )

    single = isinstance(data.get("metric"), str)
    nested = (not single) and all(isinstance(v, dict) for v in per_run.values())
    if single:
        metric = data["metric"]
        stats = data.get("stats") or {}
        paired_src = _paired_source(data)
        for cfg, vals in per_run.items():
            put(metric, cfg, vals, stats.get(cfg), paired_src)
        for cfg, s in stats.items():
            if cfg not in cells[metric]:
                put(metric, cfg, None, s, paired_src)
    elif nested:
        stats_all = data.get("stats") or {}
        for metric, by_cfg in per_run.items():
            stats = stats_all.get(metric) or {}
            for cfg, vals in by_cfg.items():
                put(metric, cfg, vals, stats.get(cfg), _paired_source(data, metric))
            for cfg, s in stats.items():
                if cfg not in cells[metric]:
                    put(metric, cfg, None, s, _paired_source(data, metric))
    else:
        raise ValueError(
            f"{path}: cannot tell whether this is a single- or multi-metric "
            "summary; expected a 'metric' string or per-metric nested 'per_run'"
        )
    return cells, warnings


# --------------------------------------------------------------------------
# formatting helpers
# --------------------------------------------------------------------------
def _num(v: float, sig: int = 4) -> str:
    """Significant-digit formatting, used for p-values and prose."""
    if v is None or (isinstance(v, float) and (math.isnan(v) or math.isinf(v))):
        return "—"
    if v == 0:
        return "0"
    return f"{v:.{sig}g}"


def _fixed(v: float, dec: int) -> str:
    """Fixed-decimal formatting, so a column lines up in the rendered table."""
    if v is None or (isinstance(v, float) and (math.isnan(v) or math.isinf(v))):
        return "—"
    return f"{v:.{dec}f}"


def _decimals(table_metric: dict, configs) -> int:
    """Pick one decimal count per metric from its smallest non-zero SD.

    Rationale: the reader must be able to see the spread, so the number of
    decimals is driven by the tightest SD in the column, not by the mean.  This
    keeps every cell in a column aligned (0.7980 vs 0.9100, not 0.798 vs 0.91).
    """
    spreads = [
        table_metric[c]["std"]
        for c in configs
        if table_metric[c]["std"] is not None and table_metric[c]["std"] > 0
    ]
    if spreads:
        ref = min(spreads)
    else:
        ref = max(abs(table_metric[c]["mean"]) for c in configs) or 1.0
    if ref <= 0:
        return 2
    return max(0, min(6, math.ceil(-math.log10(ref)) + 1))


def _tex(s: str) -> str:
    out = []
    for ch in str(s):
        out.append(_TEX_ESCAPES.get(ch, ch))
    return "".join(out)


def _cell_stats(cell, warnings, metric, cfg):
    """Return (mean, std, n, ci) for a cell, recomputing only when documented."""
    st = cell.get("stats") or {}
    vals = cell.get("values")
    mean = st.get("mean")
    std = st.get("std")
    n = st.get("n")
    ci = st.get("ci95") or st.get("ci")
    ci_method = st.get("ci_method")
    if mean is None:
        if not vals:
            raise ValueError(
                f"metric {metric!r}, config {cfg!r}: no 'stats.mean' and no "
                "per-run values; refusing to print a placeholder"
            )
        mean = sum(vals) / len(vals)
        warnings.append(
            f"{metric}/{cfg}: stats block missing, mean recomputed from per_run "
            "(verify against the run files)"
        )
    if std is None and vals and len(vals) > 1:
        m = sum(vals) / len(vals)
        var = sum((v - m) ** 2 for v in vals) / (len(vals) - 1)
        std = math.sqrt(var)
        warnings.append(
            f"{metric}/{cfg}: std missing, recomputed from per_run with ddof=1"
        )
    if n is None:
        n = len(vals) if vals else st.get("n_runs")
    if n is None:
        raise ValueError(
            f"metric {metric!r}, config {cfg!r}: sample size missing; the table "
            "must report n per cell"
        )
    return float(mean), (float(std) if std is not None else None), int(n), ci, ci_method


def _comparison_names(c: dict) -> list:
    """Config names a paired block refers to, from any of the known key styles."""
    for key in ("configs", "comparison"):
        val = c.get(key)
        if isinstance(val, (list, tuple)) and val:
            return [x for x in val if x]
    for keys in (("config_a", "config_b"), ("baseline", "treatment")):
        names = [c.get(k) for k in keys]
        if all(names):
            return names
    return []


def _paired_p(paired, best, second):
    """Extract (p, description) for the best-vs-second comparison.

    Returns (None, note) when no usable p-value is present.  The paired block
    may be a single dict (contract shape), a list of comparisons (aggregate.py
    writes ``paired_all``), or a dict of named comparisons.
    """
    if not paired:
        return None, "no paired test recorded"
    candidates = []
    if isinstance(paired, dict):
        if "p_value" in paired:
            candidates.append(paired)
        else:
            for k, v in paired.items():
                if isinstance(v, dict) and "p_value" in v:
                    candidates.append(dict(v, _key=k))
    elif isinstance(paired, list):
        candidates = [c for c in paired if isinstance(c, dict) and "p_value" in c]
    if not candidates:
        return None, "paired block has no p_value"

    for c in candidates:
        names = _comparison_names(c)
        if not names or (best in names and second in names):
            return c, None
    c = candidates[0]
    names = _comparison_names(c)
    if names and not (best in names and second in names):
        return None, (
            "paired test is for "
            + " vs ".join(names)
            + f", not {best} vs {second}; not used for bolding"
        )
    return c, None


# --------------------------------------------------------------------------
# main entry point
# --------------------------------------------------------------------------
def ablation_table(
    summary_json_path,
    metrics,
    configs,
    fmt: str = "md",
    alpha: float = 0.05,
    dispersion: str = "std",
    caption: str | None = None,
    label: str | None = None,
) -> tuple[str, list]:
    """Render an ablation table from a summary JSON.

    Parameters
    ----------
    summary_json_path : path to ``04_experiments/results/summary_*.json``.
    metrics : list of metric names, or dicts ``{"name", "label", "direction"}``.
        Direction defaults to "higher" and is *inferred* for names containing
        loss/error/latency/...; every inference is reported as a warning.
    configs : row order (list of config names).
    fmt : ``"md"`` or ``"tex"``.
    alpha : significance threshold for bolding (default 0.05).
    dispersion : ``"std"`` -> ``mean ± std``; ``"ci"`` -> ``mean [lo, hi]``
        (falls back to std with a warning when ``ci95`` is absent).
    caption, label : LaTeX caption/label (ignored for Markdown).

    Returns
    -------
    (markdown_or_latex_string, warnings) where warnings is a list of strings the
    caller should print next to the table (they are *not* silently dropped).

    Assumptions
    -----------
    * One row per configuration, one column per metric, all measured on the same
      test split with the same n; if n differs it is printed per cell.
    * ``stats.mean`` in the file is the number to publish; this function never
      recomputes it except when the block is absent, and says so.

    Limitations a reviewer will attack
    ----------------------------------
    * Bolding is only as good as the paired test: if the summary carries a test
      for a different pair of configs, no cell is bolded (reported as a warning).
    * A p-value with no correction metadata is still printed; ``warnings`` says
      the correction is missing, because CONTRACTS section 4 requires one.
    * ``mean ± std`` over 5 seeds is a descriptive spread, not a confidence
      interval; use ``dispersion="ci"`` when the CI is in the file.
    """
    fmt = str(fmt).lower().lstrip(".")
    if fmt not in {"md", "markdown", "tex", "latex"}:
        raise ValueError(f"fmt must be 'md' or 'tex', got {fmt!r}")
    fmt = "md" if fmt.startswith("md") else "tex"
    dispersion = str(dispersion).lower()
    if dispersion not in {"std", "ci"}:
        raise ValueError("dispersion must be 'std' or 'ci'")

    data = load_summary(summary_json_path)
    cells, warnings = _normalise(data, summary_json_path)
    specs = _metric_specs(metrics)

    if configs is None:
        configs = list(data.get("configs") or [])
        if not configs:
            raise ValueError(
                f"{summary_json_path}: configs argument is None and the file has "
                "no 'configs' list"
            )
        warnings.append("configs taken from the summary file; pass them explicitly")
    if isinstance(configs, str):
        configs = [configs]
    configs = list(configs)
    if not configs:
        raise ValueError("configs is empty")

    available_metrics = sorted(cells)
    for spec in specs:
        if spec["name"] not in cells:
            raise ValueError(
                f"metric {spec['name']!r} not found in {summary_json_path}; "
                f"available metrics: {available_metrics}"
            )
    # ---- collect numbers per cell -------------------------------------
    table = {}  # metric -> config -> dict(mean,std,n,ci,ci_method,bold)
    for spec in specs:
        m = spec["name"]
        if spec["direction"] is None:
            spec["direction"] = (
                "lower" if _looks_lower_is_better(m) else "higher"
            )
            warnings.append(
                f"{m}: direction inferred as {spec['direction']}-is-better from the "
                "metric name; pass {'name': ..., 'direction': ...} to be explicit"
            )
        for cfg in configs:
            if cfg not in cells[m]:
                raise ValueError(
                    f"config {cfg!r} has no data for metric {m!r} in "
                    f"{summary_json_path}; available configs for that metric: "
                    f"{sorted(cells[m])}"
                )
            mean, std, n, ci, ci_method = _cell_stats(cells[m][cfg], warnings, m, cfg)
            if n < 5:
                warnings.append(
                    f"{m}/{cfg}: n={n} < 5, intervals are unreliable (report as "
                    "indicative)"
                )
            table.setdefault(m, {})[cfg] = {
                "mean": mean,
                "std": std,
                "n": n,
                "ci": ci,
                "ci_method": ci_method,
                "bold": False,
            }
        if dispersion == "ci" and not any(
            table[m][c]["ci"] for c in configs
        ):
            warnings.append(
                f"{m}: dispersion='ci' requested but no ci95 in the summary; "
                "fell back to mean ± std"
            )

    # ---- decide bolding -------------------------------------------------
    footnotes = []
    for spec in specs:
        m = spec["name"]
        ordered = sorted(
            configs,
            key=lambda c: table[m][c]["mean"],
            reverse=(spec["direction"] == "higher"),
        )
        best, second = ordered[0], (ordered[1] if len(ordered) > 1 else None)
        if second is None:
            footnotes.append(f"{_label(spec)}: only one config, nothing to compare.")
            continue
        if table[m][best]["mean"] == table[m][second]["mean"]:
            footnotes.append(
                f"{_label(spec)}: {best} and {second} have identical means; no "
                "winner is marked."
            )
            continue

        paired, note = _paired_p(cells[m][best].get("paired"), best, second)
        if paired is None:
            warnings.append(f"{m}: {note}; best value not bolded")
            footnotes.append(
                f"{_label(spec)}: best value ({best}) is not bolded — {note}."
            )
            continue
        corr = paired.get("correction") or {}
        p_raw = paired.get("p_value")
        p_adj = corr.get("p_adjusted")
        use_adjusted = isinstance(p_adj, (int, float)) and not isinstance(p_adj, bool)
        p = p_adj if use_adjusted else p_raw
        if p is None:
            warnings.append(f"{m}: paired test has no p_value; not bolded")
            footnotes.append(
                f"{_label(spec)}: best value not bolded — the paired test for "
                f"{best} vs {second} reported no p-value."
            )
            continue
        p = float(p)
        test_name = paired.get("test") or "paired test"
        if corr.get("method"):
            family = corr.get("family_size", "?")
            if use_adjusted:
                corr_txt = f", {corr['method']}-adjusted, family size {family}"
            else:
                corr_txt = f", unadjusted p, {corr['method']} family of {family}"
                warnings.append(
                    f"{m}: correction block present but p_adjusted is null; the "
                    "p-value shown is unadjusted — do not present it as corrected"
                )
        else:
            corr_txt = ", uncorrected"
            warnings.append(
                f"{m}: p-value has no correction method/family size; CONTRACTS "
                "section 4 requires both"
            )
        alpha_used = float(paired["alpha"]) if paired.get("alpha") is not None else float(alpha)
        if p <= alpha_used:
            table[m][best]["bold"] = True
            footnotes.append(
                f"{_label(spec)}: bold marks the best config; {best} vs {second} "
                f"p = {_num(p, 3)} ({test_name}{corr_txt}, alpha = {alpha_used:g})."
            )
        else:
            footnotes.append(
                f"{_label(spec)}: the difference between {best} and {second} is "
                f"not statistically significant (p = {_num(p, 3)}, {test_name}"
                f"{corr_txt}, alpha = {alpha_used:g}); no cell is bolded."
            )

    # ---- CI provenance footnote (CONTRACTS 4: report n_boot and ci_seed) ----
    if dispersion == "ci":
        meta = set()
        for m in table:
            for c in configs:
                st = cells[m][c].get("stats") or {}
                if st.get("ci95") or st.get("ci"):
                    meta.add(
                        (
                            st.get("ci_method", "unspecified"),
                            st.get("n_boot", "?"),
                            st.get("ci_seed", "?"),
                        )
                    )
        if meta:
            parts = [
                f"{a} ({b} resamples, seed {c})" for a, b, c in sorted(meta, key=str)
            ]
            footnotes.append("Intervals: " + "; ".join(parts) + ".")
            if any(str(b) == "?" or str(c) == "?" for _, b, c in meta):
                warnings.append(
                    "at least one ci95 has no n_boot/ci_seed; CONTRACTS section 4 "
                    "requires both next to every interval"
                )

    # ---- render ---------------------------------------------------------
    decimals = {m: _decimals(table[m], configs) for m in table}
    if fmt == "md":
        body = _render_md(specs, configs, table, dispersion, decimals)
        text = body
        if footnotes:
            text += "\n" + "\n".join(f"*{f}*" for f in footnotes)
        text += "\n"
    else:
        text = _render_tex(
            specs, configs, table, dispersion, decimals, footnotes, caption, label
        )
    return text, warnings


def _label(spec) -> str:
    return spec["label"]


def _cell_text(cell, spec, dispersion: str, tex: bool, dec: int) -> str:
    mean = _fixed(cell["mean"], dec)
    if dispersion == "ci" and cell["ci"]:
        lo, hi = _fixed(cell["ci"][0], dec), _fixed(cell["ci"][1], dec)
        if tex:
            core = f"${mean}\\ [{lo},\\ {hi}]$"
        else:
            core = f"{mean} [{lo}, {hi}]"
    else:
        std = _fixed(cell["std"], dec) if cell["std"] is not None else "—"
        if tex:
            core = f"${mean} \\pm {std}$"
        else:
            core = f"{mean} ± {std}"
    if cell["bold"]:
        core = f"\\textbf{{{core}}}" if tex else f"**{core}**"
    return f"{core} (n={cell['n']})"


def _render_md(specs, configs, table, dispersion, decimals) -> str:
    header = "| config | " + " | ".join(s["label"] for s in specs) + " |"
    sep = "|:--|" + "|".join("--:" for _ in specs) + "|"
    lines = [header, sep]
    for cfg in configs:
        row = [str(cfg)]
        for s in specs:
            row.append(
                _cell_text(
                    table[s["name"]][cfg], s, dispersion, tex=False, dec=decimals[s["name"]]
                )
            )
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def _render_tex(
    specs, configs, table, dispersion, decimals, footnotes, caption, label
) -> str:
    colspec = "l" + "c" * len(specs)
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{" + _tex(caption or "Ablation results") + "}",
        r"\label{" + _tex(label or "tab:ablation") + "}",
        r"\begin{tabular}{" + colspec + "}",
        r"\toprule",
        "Config & " + " & ".join(_tex(s["label"]) for s in specs) + r" \\",
        r"\midrule",
    ]
    for cfg in configs:
        cells = [
            _cell_text(
                table[s["name"]][cfg],
                s,
                dispersion,
                tex=True,
                dec=decimals[s["name"]],
            )
            for s in specs
        ]
        lines.append(_tex(cfg) + " & " + " & ".join(cells) + r" \\")
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    if footnotes:
        lines.append(r"\par\smallskip")
        lines.append(r"{\footnotesize")
        lines.append(r"\textit{Notes.} " + " ".join(_tex(f) for f in footnotes))
        lines.append(r"}")
    lines.append(r"\end{table}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":  # pragma: no cover - manual smoke test
    import sys

    if len(sys.argv) > 1:
        print(ablation_table(sys.argv[1], sys.argv[2:], None)[0])
