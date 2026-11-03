"""C1 — paper assets: tables, one SVG figure, and RESULTS-INDEX entries.

Reads ONLY `04_experiments/results/c1/results_full.json` (+ `audit.json` for the audit table) and writes:

  05_paper/tables/generated/T1_per_rung.{md,tex}
  05_paper/tables/generated/T2_hypotheses.{md,tex}
  05_paper/tables/generated/T3_audit.{md,tex}
  05_paper/figures/generated/F1_abstain_precision_by_rung.svg
  04_experiments/RESULTS-INDEX.json   (entries upserted, toy entries preserved)

No number is typed by hand anywhere in this file: every cell is formatted from a key in the results JSON,
and every index entry points at that key, so `tools/check_numbers.py` can trace a draft number back to it.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RES = ROOT / "04_experiments" / "results" / "c1"
TAB = ROOT / "05_paper" / "tables" / "generated"
FIG = ROOT / "05_paper" / "figures" / "generated"
INDEX = ROOT / "04_experiments" / "RESULTS-INDEX.json"
REL = "04_experiments/results/c1/results_full.json"


def load() -> dict:
    return json.loads((RES / "results_full.json").read_text(encoding="utf-8"))


def pct(x: float) -> str:
    return f"{100.0 * x:.2f}"


def table_per_rung(r: dict) -> tuple[str, str]:
    band = r["test"]["band_primary"]["per_rung"]
    expl = r["test"]["exploratory_band"]["per_rung"]
    b2 = r["baselines"]["B2_dense_top1"]["test"]["per_rung"]
    rows = []
    for rung in ("1", "2", "3", "4"):
        rows.append((rung, band[rung], expl[rung], b2[rung]))
    md = ["| Rung | n | Band (confirmatory) abstain prec. | Band over-refusal | Exploratory band prec. | Dense-cosine baseline prec. |",
          "|---:|---:|---:|---:|---:|---:|"]
    for rung, b, e, d in rows:
        md.append(f"| {rung} | {b['n']} | {pct(b['abstain_precision'])} | {pct(r['test']['band_primary']['over_refusal'])} "
                  f"| {pct(e['abstain_precision'])} | {pct(d['abstain_precision'])} |")
    md.append("")
    md.append("All values are percentages on the held-out half. Over-refusal is a property of the gate, "
              "not of a rung, so it is repeated for readability.")
    tex = [r"\begin{tabular}{rrrrrr}", r"\hline",
           r"Rung & $n$ & Band (conf.) & Over-refusal & Exploratory band & Dense-cosine \\",
           r"\hline"]
    for rung, b, e, d in rows:
        tex.append(f"{rung} & {b['n']} & {pct(b['abstain_precision'])} & "
                   f"{pct(r['test']['band_primary']['over_refusal'])} & "
                   f"{pct(e['abstain_precision'])} & {pct(d['abstain_precision'])} \\\\")
    tex += [r"\hline", r"\end{tabular}"]
    return "\n".join(md) + "\n", "\n".join(tex) + "\n"


def table_hypotheses(r: dict) -> tuple[str, str]:
    h = r["hypotheses"]
    h1, h2, h3 = h["H1"], h["H2"], h["H3"]
    ex = r["exploratory"]["H1_sequence"]
    md = ["| Hypothesis | Pre-registered criterion | Observed | Verdict |", "|---|---|---|---|"]
    md.append(f"| H1 hardness monotonicity | rung 1 − rung 3 ≥ 15 pts, non-increasing | "
              f"difference {pct(h1['diff_r1_minus_r3'])} pts; sequence "
              f"{', '.join(pct(x) for x in h1['sequence'])} | {'SUPPORTED' if h1['supported'] else 'REFUTED'} |")
    md.append(f"| H2 transfer | loss ≥ 10 pts, refuted if within ±5 | "
              f"loss {pct(h2['loss_points'])} pts (dev {pct(h2['dev_pooled_precision'])} → "
              f"test {pct(h2['test_pooled_precision'])}) | "
              f"{'SUPPORTED' if h2['supported'] else ('REFUTED (transfer holds)' if h2['refuted'] else 'INCONCLUSIVE')} |")
    md.append(f"| H3 two-sided vs one-sided | band ≥ +5 pts at matched recall | "
              f"difference {pct(h3['difference']['diff'])} pts, 95% CI "
              f"[{pct(h3['difference']['lo'])}, {pct(h3['difference']['hi'])}] | "
              f"{'SUPPORTED' if h3['supported'] else 'REFUTED'} |")
    md.append("")
    md.append(f"Exploratory operating point (over-refusal ≤ {pct(ex['over_refusal'])} %, "
              f"coverage {pct(ex['coverage'])} %): per-rung abstain precision "
              f"{', '.join(pct(x) for x in ex['sequence'])}; monotone 1→4: "
              f"{'yes' if ex['monotone_1_to_4'] else 'no'}. Exploratory only — not a registered test.")
    tex = [r"\begin{tabular}{p{3.2cm}p{4.2cm}p{5.2cm}p{2.6cm}}", r"\hline",
           r"Hypothesis & Criterion & Observed & Verdict \\", r"\hline"]
    tex.append(f"H1 & rung 1 $- $ rung 3 $\\ge 15$ pts & "
               f"{pct(h1['diff_r1_minus_r3'])} pts & {'SUPPORTED' if h1['supported'] else 'REFUTED'} \\\\")
    tex.append(f"H2 & loss $\\ge 10$ pts & {pct(h2['loss_points'])} pts & "
               f"{'SUPPORTED' if h2['supported'] else ('REFUTED' if h2['refuted'] else 'INCONCLUSIVE')} \\\\")
    tex.append(f"H3 & band $\\ge +5$ pts & {pct(h3['difference']['diff'])} pts "
               f"[{pct(h3['difference']['lo'])}, {pct(h3['difference']['hi'])}] & "
               f"{'SUPPORTED' if h3['supported'] else 'REFUTED'} \\\\")
    tex += [r"\hline", r"\end{tabular}"]
    return "\n".join(md) + "\n", "\n".join(tex) + "\n"


def table_audit(r: dict) -> tuple[str, str]:
    a = r["audit"]["dev_auroc_primary"]
    s = r["audit"]["dev_auroc_sensitivity_with_lex"]
    md = ["| Rung | Surface-only AUROC (6 features, gate) | + question–passage overlap | Gate at 0.75 |",
          "|---:|---:|---:|---|"]
    for k in ("1", "2", "3", "4"):
        md.append(f"| {k} | {a[k]:.3f} | {s[k]:.3f} | {'pass' if a[k] <= 0.75 else 'REBUILD'} |")
    tex = [r"\begin{tabular}{rrrr}", r"\hline",
           r"Rung & 6 surface feats & + overlap & Gate 0.75 \\", r"\hline"]
    for k in ("1", "2", "3", "4"):
        tex.append(f"{k} & {a[k]:.3f} & {s[k]:.3f} & {'pass' if a[k] <= 0.75 else 'rebuild'} \\\\")
    tex += [r"\hline", r"\end{tabular}"]
    return "\n".join(md) + "\n", "\n".join(tex) + "\n"


def figure_svg(r: dict) -> str:
    band = r["test"]["band_primary"]["per_rung"]
    expl = r["test"]["exploratory_band"]["per_rung"]
    b2 = r["baselines"]["B2_dense_top1"]["test"]["per_rung"]
    series = [("band (confirmatory)", band, "#1f77b4"), ("band (exploratory)", expl, "#ff7f0e"),
              ("dense cosine alone", b2, "#2ca02c")]
    W, H, L, B, T, Rgt = 520, 330, 62, 46, 18, 130
    pw, ph = W - L - Rgt, H - B - T
    xs = {k: L + (i + 0.5) * pw / 4 for i, k in enumerate(("1", "2", "3", "4"))}
    def y(v: float) -> float:
        return T + (1.0 - v) * ph
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif" font-size="11">',
             f'<rect width="{W}" height="{H}" fill="white"/>']
    for tick in (0.0, 0.25, 0.5, 0.75, 1.0):
        parts.append(f'<line x1="{L}" y1="{y(tick):.1f}" x2="{L + pw}" y2="{y(tick):.1f}" '
                     f'stroke="#dddddd" stroke-width="1"/>')
        parts.append(f'<text x="{L - 6}" y="{y(tick) + 4:.1f}" text-anchor="end">{int(tick * 100)}</text>')
    parts.append(f'<line x1="{L}" y1="{T}" x2="{L}" y2="{T + ph}" stroke="#333"/>')
    parts.append(f'<line x1="{L}" y1="{T + ph}" x2="{L + pw}" y2="{T + ph}" stroke="#333"/>')
    parts.append(f'<text x="{L - 44}" y="{T + ph / 2}" transform="rotate(-90 {L - 44} {T + ph / 2})" '
                 f'text-anchor="middle">abstain precision (%)</text>')
    for k, x in xs.items():
        parts.append(f'<text x="{x:.1f}" y="{T + ph + 18}" text-anchor="middle">rung {k}</text>')
    for name, block, colour in series:
        pts = [(xs[k], y(block[k]["abstain_precision"])) for k in ("1", "2", "3", "4") if k in block]
        parts.append('<polyline fill="none" stroke="%s" stroke-width="2" points="%s"/>'
                     % (colour, " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)))
        for a, b in pts:
            parts.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="2.6" fill="{colour}"/>')
    for i, (name, _, colour) in enumerate(series):
        yy = T + 8 + i * 16
        parts.append(f'<rect x="{L + pw + 12}" y="{yy - 7}" width="9" height="9" fill="{colour}"/>')
        parts.append(f'<text x="{L + pw + 26}" y="{yy}">{name}</text>')
    parts.append(f'<text x="{L}" y="{H - 8}">held-out half, %d items; SQuAD 2.0 dev</text>'
                 % r["items"]["n_test"])
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def index_entries(r: dict) -> list[dict]:
    e: list[dict] = []
    def add(i, desc, key, tol=0.0005):
        e.append({"id": i, "description": desc, "file": REL, "key": key, "tolerance": tol, "toy": False})
    add("c1.items.total", "Items in the C1 benchmark (all splits)", "items.n_total", 0)
    add("c1.items.test", "Items in the held-out half", "items.n_test", 0)
    add("c1.items.rung2.total", "Rung-2 items (short rung, §8c)", "items.per_rung_dev.2", 0)
    add("c1.auroc.dev", "Gate AUROC on dev (answerable vs all negatives)", "discrimination.dev_auroc")
    add("c1.auroc.test", "Gate AUROC on the held-out half", "discrimination.test_auroc")
    for k in ("1", "2", "3", "4"):
        add(f"c1.audit.surface.r{k}", f"Surface-only AUROC rung {k} (6 features)", f"audit.dev_auroc_primary.{k}")
        add(f"c1.audit.surface_lex.r{k}", f"Surface+overlap AUROC rung {k}", f"audit.dev_auroc_sensitivity_with_lex.{k}")
        add(f"c1.band.precision.r{k}", f"Band gate abstain precision, rung {k} (held-out)", f"test.band_primary.per_rung.{k}.abstain_precision")
        add(f"c1.band.n.r{k}", f"Band gate n, rung {k}", f"test.band_primary.per_rung.{k}.n", 0)
        add(f"c1.expl.precision.r{k}", f"Exploratory band abstain precision, rung {k}", f"test.exploratory_band.per_rung.{k}.abstain_precision")
        add(f"c1.b2.precision.r{k}", f"Dense-cosine baseline abstain precision, rung {k}", f"baselines.B2_dense_top1.test.per_rung.{k}.abstain_precision")
    add("c1.band.over_refusal", "Band gate over-refusal rate (held-out)", "test.band_primary.over_refusal")
    add("c1.expl.over_refusal", "Exploratory band over-refusal rate (held-out)", "test.exploratory_band.over_refusal")
    add("c1.band.coverage", "Band gate coverage (held-out)", "test.band_primary.coverage")
    add("c1.expl.coverage", "Exploratory band coverage (held-out)", "exploratory.H1_sequence.coverage")
    add("c1.thr.lo", "Fitted band lower threshold", "thresholds.band.t_lo", 0)
    add("c1.thr.hi", "Fitted band upper threshold", "thresholds.band.t_hi", 0)
    add("c1.thr.single", "Fitted single threshold", "thresholds.single.t", 0)
    add("c1.dev.admit_mass", "Dev admit mass at the band", "placement_diagnostic.dev_admit_mass")
    add("c1.dev.refused_below_lo", "Dev fraction refused by the lower threshold", "placement_diagnostic.dev_refused_below_lo")
    add("c1.b1.pooled", "BM25-top1 baseline pooled abstain precision", "baselines.B1_bm25_top1.test.pooled_abstain_precision")
    add("c1.b2.pooled", "Dense-cosine baseline pooled abstain precision", "baselines.B2_dense_top1.test.pooled_abstain_precision")
    add("c1.h1.diff", "H1 rung1 minus rung3 abstain precision", "hypotheses.H1.diff_r1_minus_r3")
    add("c1.h2.loss", "H2 dev-to-test precision loss", "hypotheses.H2.loss_points")
    add("c1.h3.diff", "H3 band minus matched single", "hypotheses.H3.difference.diff")
    add("c1.h3.lo", "H3 difference, 95% CI lower", "hypotheses.H3.difference.lo")
    add("c1.h3.hi", "H3 difference, 95% CI upper", "hypotheses.H3.difference.hi")
    add("c1.expl.diff_r1_r3", "Exploratory rung1 minus rung3", "exploratory.H1_sequence.diff_r1_minus_r3")
    add("c1.reader.n", "Items with reader features (dev only)", "reader_baseline_dev_only.n", 0)
    add("c1.reader.auroc", "Reader logprob AUROC on those dev items", "reader_baseline_dev_only.auroc_answerable_vs_negatives")
    return e


def main() -> None:
    r = load()
    TAB.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    (TAB / "T1_per_rung.md").write_text(table_per_rung(r)[0], encoding="utf-8")
    (TAB / "T1_per_rung.tex").write_text(table_per_rung(r)[1], encoding="utf-8")
    (TAB / "T2_hypotheses.md").write_text(table_hypotheses(r)[0], encoding="utf-8")
    (TAB / "T2_hypotheses.tex").write_text(table_hypotheses(r)[1], encoding="utf-8")
    (TAB / "T3_audit.md").write_text(table_audit(r)[0], encoding="utf-8")
    (TAB / "T3_audit.tex").write_text(table_audit(r)[1], encoding="utf-8")
    (FIG / "F1_abstain_precision_by_rung.svg").write_text(figure_svg(r), encoding="utf-8")

    idx = json.loads(INDEX.read_text(encoding="utf-8")) if INDEX.exists() else {"version": 1, "entries": []}
    keep = [e for e in idx.get("entries", []) if not e.get("id", "").startswith("c1.")]
    idx["entries"] = keep + index_entries(r)
    import datetime
    idx["updated_at"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    INDEX.write_text(json.dumps(idx, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"tables: {len(list(TAB.glob('T*')))} files, figure: 1, index entries: {len(index_entries(r))}")


if __name__ == "__main__":
    main()
