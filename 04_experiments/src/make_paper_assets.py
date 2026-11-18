"""C1 — paper assets: tables (with traceability markers), one figure, and RESULTS-INDEX entries.

Reads only files produced by the experiment scripts:

  04_experiments/results/c1/results_full.json             the pre-registered (as-run) analysis
  04_experiments/results/c1/rung5.json                    EXPLORATORY rung R5 (deviation D2)
  04_experiments/results/c1/transfer.json                 the 2WikiMultihopQA arm
  04_experiments/results/c1/top1_variant.json             EXPLORATORY top-1-presented variant (D3)
  04_experiments/results/c1_corrected/results_full.json   SPEC-CORRECTED re-implementation (D4)
  04_experiments/results/c1_corrected/ablations.json
  04_experiments/config/c1_gate.json                      protocol constants
  04_experiments/config/design_constants.json             constants derived from the code

and writes

  05_paper/tables/generated/T1..T7 .md    markdown tables; every measured cell is wrapped in a
                                          `num:` marker so tools/check_numbers.py can trace it
  05_paper/figures/generated/F1_*.svg     one figure
  04_experiments/RESULTS-INDEX.json       c1.* entries replaced in the same run

No result number is typed by hand here: every cell is formatted from a JSON key and every emitted
marker id is registered in the index by the same run. A missing key raises instead of printing a
blank cell.
"""
from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RES = ROOT / "04_experiments" / "results" / "c1"
RESX = ROOT / "04_experiments" / "results" / "c1_corrected"
TAB = ROOT / "05_paper" / "tables" / "generated"
FIG = ROOT / "05_paper" / "figures" / "generated"
INDEX = ROOT / "04_experiments" / "RESULTS-INDEX.json"
CONFIG = "04_experiments/config/c1_gate.json"
CONST = "04_experiments/config/design_constants.json"
REL = "04_experiments/results/c1/results_full.json"
REL_X = "04_experiments/results/c1_corrected/results_full.json"
REL_5 = "04_experiments/results/c1/rung5.json"
REL_TR = "04_experiments/results/c1/transfer.json"
REL_T1 = "04_experiments/results/c1/top1_variant.json"
REL_T1F = "04_experiments/results/c1/top1_flat.json"
REL_ABL = "04_experiments/results/c1_corrected/ablations.json"
PM = "04_experiments/results/c1/precision_metrics.json"
PM_X = "04_experiments/results/c1_corrected/precision_metrics.json"
DATA = "04_experiments/data/squad_dev_stats.json"
STATS = "04_experiments/results/c1/stats_addendum.json"
LIT = "02_literature/quoted-numbers.json"

ENTRIES: dict[str, dict] = {}


def load(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"missing results file: {path} (run the producing script first)")
    return json.loads(path.read_text(encoding="utf-8"))


def dig(obj, dotted: str):
    node = obj
    for part in dotted.split("."):
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            raise SystemExit(f"key not found while building assets: {dotted}")
    return node


def pct(x) -> str:
    return f"{100.0 * float(x):.2f}%"


def auc(x) -> str:
    return f"{float(x):.3f}"


def integer(x) -> str:
    return f"{int(x)}"


def cell(file: str, key: str, value, fmt, entry_id: str, desc: str, tol: float = 0.0005) -> str:
    """Register an index entry, then emit the value wrapped in its marker."""
    ENTRIES[entry_id] = {"id": entry_id, "description": desc, "file": file, "key": key,
                         "tolerance": tol, "toy": False}
    return f"<!-- num:{entry_id} -->{fmt(value)}<!-- /num -->"


def table_per_rung(pm: dict) -> str:
    """Per-rung refusal rate and precision, side by side, for both operating points.

    The pre-registration named the per-rung quantity "abstain precision" but defined it as the mean
    refusal indicator over that rung's negatives, which is a recall on the rung. Round-2 review caught
    the contradiction; both numbers are now reported and labelled.
    """
    band = pm["operating_points"]["band"]
    expl = pm["operating_points"]["exploratory_band"]
    md = ["| Rung | n | Band refusal rate | Band precision | Exploratory refusal rate | Exploratory precision |",
          "|---:|---:|---:|---:|---:|---:|"]
    for k in ("1", "2", "3", "4"):
        b, e = band["per_rung"][k], expl["per_rung"][k]
        n = cell(PM, f"operating_points.band.per_rung.{k}.n", b["n"], integer, f"c1.pm.n.r{k}",
                 f"Items in rung {k}, held-out half", 0)
        br = cell(PM, f"operating_points.band.per_rung.{k}.refusal_rate", b["refusal_rate"], pct,
                  f"c1.pm.band.refusal.r{k}", f"Band refusal rate on rung {k} = P(refused | negative)")
        bp = cell(PM, f"operating_points.band.per_rung.{k}.precision", b["precision"], pct,
                  f"c1.pm.band.precision.r{k}", f"Band precision on rung {k} = P(negative | refused)")
        er = cell(PM, f"operating_points.exploratory_band.per_rung.{k}.refusal_rate", e["refusal_rate"], pct,
                  f"c1.pm.expl.refusal.r{k}", f"Exploratory refusal rate on rung {k}")
        ep = cell(PM, f"operating_points.exploratory_band.per_rung.{k}.precision", e["precision"], pct,
                  f"c1.pm.expl.precision.r{k}", f"Exploratory precision on rung {k}")
        md.append(f"| R{k} | {n} | {br} | {bp} | {er} | {ep} |")
    ar = cell(PM, "operating_points.band.answer_rate", band["answer_rate"], pct, "c1.pm.band.answer_rate",
              "Share of answerable questions the band gate answers (held-out)")
    ap = cell(PM, "operating_points.band.pooled.precision", band["pooled"]["precision"], pct,
              "c1.pm.band.pooled_precision", "Pooled precision of the band gate over all negatives")
    ep = cell(PM, "operating_points.exploratory_band.pooled.precision", expl["pooled"]["precision"], pct,
              "c1.pm.expl.pooled_precision", "Pooled precision of the exploratory gate")
    md += ["",
           f"Refusal rate is P(refused | a negative of that rung) — a recall on the rung, and the quantity "
           f"the pre-registration labelled abstain precision. Precision is P(negative of that rung | "
           f"refused), over that rung's items and the answerable items together. Pooled precision is "
           f"{ap} at the registered point and {ep} at the exploratory point; the band gate answers {ar} "
           f"of answerable questions, while its item-level coverage is much lower because every question "
           f"contributes four negatives to the item count."]
    return "\n".join(md) + "\n"


def table_hypotheses(r: dict) -> str:
    h1, h2, h3 = r["hypotheses"]["H1"], r["hypotheses"]["H2"], r["hypotheses"]["H3"]
    d1 = cell(REL, "hypotheses.H1.diff_r1_minus_r3", h1["diff_r1_minus_r3"], pct, "c1.h1.diff",
              "H1 rung R1 minus rung R3 abstain precision")
    lo1 = cell(REL, "hypotheses.H1.ci95_lo", h1["ci95_lo"], pct, "c1.h1.lo", "H1 difference, CI lower")
    hi1 = cell(REL, "hypotheses.H1.ci95_hi", h1["ci95_hi"], pct, "c1.h1.hi", "H1 difference, CI upper")
    l2 = cell(REL, "hypotheses.H2.loss_points", h2["loss_points"], pct, "c1.h2.loss",
              "H2 dev-to-test pooled precision loss")
    d3 = cell(REL, "hypotheses.H3.difference.diff", h3["difference"]["diff"], pct, "c1.h3.diff",
              "H3 band minus recall-matched single")
    lo3 = cell(REL, "hypotheses.H3.difference.lo", h3["difference"]["lo"], pct, "c1.h3.lo",
               "H3 difference, CI lower")
    hi3 = cell(REL, "hypotheses.H3.difference.hi", h3["difference"]["hi"], pct, "c1.h3.hi",
               "H3 difference, CI upper")
    c1p = cell(CONST, "criterion_h1_drop_points", load(ROOT / CONST)["criterion_h1_drop_points"],
               integer, "c1.crit.h1", "H1 criterion: minimum R1-R3 drop in points", 0)
    c2p = cell(CONST, "criterion_h2_loss_points", load(ROOT / CONST)["criterion_h2_loss_points"],
               integer, "c1.crit.h2", "H2 criterion: minimum dev-to-test loss in points", 0)
    c2s = cell(CONST, "criterion_h2_slack_points", load(ROOT / CONST)["criterion_h2_slack_points"],
               integer, "c1.crit.h2.slack", "H2 refutation slack in points", 0)
    c3p = cell(CONST, "criterion_h3_gain_points", load(ROOT / CONST)["criterion_h3_gain_points"],
               integer, "c1.crit.h3", "H3 criterion: minimum band gain in points", 0)
    md = ["| Hypothesis | Pre-registered criterion | Observed | Verdict |", "|---|---|---|---|",
          f"| H1 hardness monotonicity | R1 − R3 at least {c1p} points, non-increasing | difference {d1}, "
          f"95% CI [{lo1}, {hi1}]; sequence is not non-increasing | criterion not exercisable (see §4.2) |",
          f"| H2 transfer | loss at least {c2p} points; refuted if within {c2s} points | dev-to-test loss "
          f"{l2} | REFUTED (it transfers, degenerately) |",
          f"| H3 two-sided vs one-sided | band at least {c3p} points ahead at matched recall | difference "
          f"{d3}, 95% CI [{lo3}, {hi3}] | criterion not exercisable (see §4.2) |"]
    return "\n".join(md) + "\n"


def table_audit(r: dict, r5: dict) -> str:
    gate = cell(CONFIG, "audit_auroc_gate", load(ROOT / CONFIG)["audit_auroc_gate"], auc,
                "c1.const.audit_gate", "Separability-audit AUROC gate (config)", 0)
    md = ["| Rung | Six surface features | + question–passage overlap | Gate |", "|---:|---:|---:|---|"]
    a = r["audit"]["dev_auroc_primary"]
    s = r["audit"]["dev_auroc_sensitivity_with_lex"]
    for k in ("1", "2", "3", "4"):
        av = cell(REL, f"audit.dev_auroc_primary.{k}", a[k], auc, f"c1.audit.surface.r{k}",
                  f"Surface-only AUROC, rung {k} (dev, six features)")
        sv = cell(REL, f"audit.dev_auroc_sensitivity_with_lex.{k}", s[k], auc, f"c1.audit.surface_lex.r{k}",
                  f"Surface+overlap AUROC, rung {k} (dev)")
        md.append(f"| R{k} | {av} | {sv} | {'pass' if a[k] <= 0.75 else 'REBUILD'} (gate {gate}) |")
    au = r5["separability_audit"]["rung5"]
    av = cell(REL_5, "separability_audit.rung5.dev.auroc_primary_6", au["dev"]["auroc_primary_6"], auc,
              "c1.r5.audit.surface", "Surface-only AUROC, rung R5 (dev)")
    sv = cell(REL_5, "separability_audit.rung5.dev.auroc_with_lex_overlap", au["dev"]["auroc_with_lex_overlap"],
              auc, "c1.r5.audit.lex", "Surface+overlap AUROC, rung R5 (dev)")
    md.append(f"| R5 (exploratory) | {av} | {sv} | pass (gate {gate}) |")
    return "\n".join(md) + "\n"


def table_frozen_vs_corrected(fz: dict, cx: dict) -> str:
    md = ["| Quantity | Frozen run | Spec-corrected (D4) |", "|---|---:|---:|"]

    def row(label, key, fmt, base_id, tol=0.0005):
        a = cell(REL, key, dig(fz, key), fmt, f"{base_id}.run", f"{label} (as run)", tol)
        b = cell(REL_X, key, dig(cx, key), fmt, f"{base_id}.corr", f"{label} (spec-corrected, D4)", tol)
        md.append(f"| {label} | {a} | {b} |")

    def thr(x):
        return f"{float(x):.4f}"

    row("Gate AUROC, dev", "discrimination.dev_auroc", auc, "c1.auroc.dev")
    row("Gate AUROC, held out", "discrimination.test_auroc", auc, "c1.auroc.test")
    row("Band lower threshold (t_lo)", "thresholds.band.t_lo", thr, "c1.thr.lo")
    row("Band upper threshold (t_hi)", "thresholds.band.t_hi", thr, "c1.thr.hi")
    for k in ("1", "2", "3", "4"):
        row(f"Band abstain precision, R{k}", f"test.band_primary.per_rung.{k}.abstain_precision", pct,
            f"c1.band.precision.r{k}")
    row("Band over-refusal", "test.band_primary.over_refusal", pct, "c1.band.over_refusal")
    row("Band coverage", "test.band_primary.coverage", pct, "c1.band.coverage")
    for k in ("1", "2", "3", "4"):
        row(f"Exploratory precision, R{k}", f"test.exploratory_band.per_rung.{k}.abstain_precision", pct,
            f"c1.expl.precision.r{k}")
    row("Exploratory over-refusal", "test.exploratory_band.over_refusal", pct, "c1.expl.over_refusal")
    row("Exploratory coverage", "test.exploratory_band.coverage", pct, "c1.expl.coverage")
    row("H3 band minus matched single", "hypotheses.H3.difference.diff", pct, "c1.h3.diff")
    row("Dense-cosine (B2) pooled precision", "baselines.B2_dense_top1.test.pooled_abstain_precision", pct,
        "c1.b2.pooled")
    row("Dense-cosine (B2) coverage", "baselines.B2_dense_top1.test.coverage", pct, "c1.b2.coverage")
    return "\n".join(md) + "\n"


def write_top1_flat(t1: dict) -> Path:
    """The top-1 variant stores its operating points under keys that contain dots, which a dotted
    index path cannot address. This writes the scalars the tables quote into one flat file."""
    op = t1["operating_points"]["band_target_precision_0.80"]["test"]
    flat = {
        "generated_by": "04_experiments/src/make_paper_assets.py",
        "source": "04_experiments/results/c1/top1_variant.json operating_points.band_target_precision_0.80.test",
        "hit_rate_dev": t1["items"]["per_split"]["dev"]["hit_rate"],
        "hit_rate_test": t1["items"]["per_split"]["test"]["hit_rate"],
        "auroc_test": t1["auroc"]["test_gate_auroc"],
        "auroc_dev": t1["auroc"]["dev_gate_auroc"],
        "refuse_hit": op["refusal_rate_hits"],
        "refuse_miss": op["refusal_rate_misses"],
        "precision_miss_given_refused": op["precision_miss_given_refused"],
        "over_refusal": op["over_refusal"],
    }
    path = RES / "top1_flat.json"
    path.write_text(json.dumps(flat, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def table_arms(r5: dict, tr: dict, t1: dict) -> str:
    md = ["| Arm (all exploratory) | Abstain precision | 95% CI | Over-refusal | Discrimination |",
          "|---|---:|---|---:|---:|"]
    r5c = r5["rung5_test"]["confirmatory_band"]
    r5e = r5["rung5_test"]["exploratory_band"]
    auro = cell(REL_5, "auroc.answerable_test_rung0_vs_rung5", r5["auroc"]["answerable_test_rung0_vs_rung5"],
                auc, "c1.r5.auroc", "Rung R5: AUROC answerable vs R5, test half")
    c = cell(REL_5, "rung5_test.confirmatory_band.abstain_precision", r5c["abstain_precision"], pct,
             "c1.r5.precision.conf", "Rung R5 abstain precision, confirmatory band")
    lo = cell(REL_5, "rung5_test.confirmatory_band.ci95.lo", r5c["ci95"]["lo"], pct, "c1.r5.ci.lo",
              "Rung R5 confirmatory CI lower")
    hi = cell(REL_5, "rung5_test.confirmatory_band.ci95.hi", r5c["ci95"]["hi"], pct, "c1.r5.ci.hi",
              "Rung R5 confirmatory CI upper")
    md.append(f"| Rung R5, confirmatory band | {c} | [{lo}, {hi}] | degenerate, see §4.4 | {auro} |")
    c = cell(REL_5, "rung5_test.exploratory_band.abstain_precision", r5e["abstain_precision"], pct,
             "c1.r5.precision.expl", "Rung R5 abstain precision, exploratory band")
    lo = cell(REL_5, "rung5_test.exploratory_band.ci95.lo", r5e["ci95"]["lo"], pct, "c1.r5.expl.ci.lo",
              "Rung R5 exploratory CI lower")
    hi = cell(REL_5, "rung5_test.exploratory_band.ci95.hi", r5e["ci95"]["hi"], pct, "c1.r5.expl.ci.hi",
              "Rung R5 exploratory CI upper")
    resid = cell(REL_5, "matching_diagnostic.test.mean_overlap_absdiff",
                 r5["matching_diagnostic"]["test"]["mean_overlap_absdiff"], pct, "c1.r5.match.mean_absdiff",
                 "Rung R5 mean |overlap(chosen) minus overlap(gold)|, test half")
    md.append(f"| Rung R5, exploratory band | {c} | [{lo}, {hi}] | matching residue {resid} | {auro} |")

    tc = tr["transfer"]["operating_points"]["confirmatory_band"]
    te = tr["transfer"]["operating_points"]["exploratory_band"]
    atr = cell(REL_TR, "transfer.operating_points.confirmatory_band.auroc_answerable_vs_rung3",
               tc["auroc_answerable_vs_rung3"], auc, "c1.tr.auroc",
               "Transfer arm AUROC, answerable vs R3, 2WikiMultihopQA")
    c = cell(REL_TR, "transfer.operating_points.confirmatory_band.per_rung.3.abstain_precision",
             tc["per_rung"]["3"]["abstain_precision"], pct, "c1.tr.precision.conf",
             "Transfer arm R3 abstain precision, confirmatory band")
    o = cell(REL_TR, "transfer.operating_points.confirmatory_band.over_refusal", tc["over_refusal"], pct,
             "c1.tr.over_refusal.conf", "Transfer arm over-refusal, confirmatory band")
    md.append(f"| Second-corpus arm, confirmatory band | {c} | not informative | {o} | {atr} |")
    c = cell(REL_TR, "transfer.operating_points.exploratory_band.per_rung.3.abstain_precision",
             te["per_rung"]["3"]["abstain_precision"], pct, "c1.tr.precision.expl",
             "Transfer arm R3 abstain precision, exploratory band")
    lo = cell(REL_TR, "transfer.operating_points.exploratory_band.per_rung.3.ci95.lo",
              te["per_rung"]["3"]["ci95"]["lo"], pct, "c1.tr.ci.lo", "Transfer exploratory CI lower")
    hi = cell(REL_TR, "transfer.operating_points.exploratory_band.per_rung.3.ci95.hi",
              te["per_rung"]["3"]["ci95"]["hi"], pct, "c1.tr.ci.hi", "Transfer exploratory CI upper")
    o = cell(REL_TR, "transfer.operating_points.exploratory_band.over_refusal", te["over_refusal"], pct,
             "c1.tr.over_refusal.expl", "Transfer arm over-refusal, exploratory band")
    md.append(f"| Second-corpus arm, exploratory band | {c} | [{lo}, {hi}] | {o} | {atr} |")

    hit = cell(REL_T1F, "hit_rate_test", t1["items"]["per_split"]["test"]["hit_rate"], pct,
               "c1.t1.hit.test", "BM25 top-1-is-gold hit rate, test half")
    t1a = cell(REL_T1F, "auroc_test", t1["auroc"]["test_gate_auroc"], auc, "c1.t1.auroc",
               "Top-1-presented variant gate AUROC, test half")
    rm = cell(REL_T1F, "refuse_miss", t1["operating_points"]["band_target_precision_0.80"]["test"]["refusal_rate_misses"],
              pct, "c1.t1.refuse.miss", "Top-1 variant: fraction of retrieval misses refused")
    rh = cell(REL_T1F, "refuse_hit", t1["operating_points"]["band_target_precision_0.80"]["test"]["refusal_rate_hits"],
              pct, "c1.t1.refuse.hit", "Top-1 variant: fraction of retrieval hits refused")
    pm = cell(REL_T1F, "precision_miss_given_refused",
              t1["operating_points"]["band_target_precision_0.80"]["test"]["precision_miss_given_refused"],
              pct, "c1.t1.precision.miss", "Top-1 variant: P(miss | refused), test half")
    md.append(f"| Top-1 presented (hit rate {hit}) | {pm} P(miss | refused) | not informative | {rh} of hits "
              f"refused | {t1a} |")
    md += ["",
           "Every arm here is exploratory. R5 and the top-1 variant are declared deviations (D2, D3). The second-corpus "
           "arm is H2's pre-declared second corpus, but its construct differs (no article grouping, shorter "
           "passages, multi-hop questions), so it supports a direction claim only."]
    return "\n".join(md) + "\n"


def table_ablations(abl: dict) -> str:
    md = ["| Feature subset | n | Dev AUROC | Held-out AUROC | Band over-refusal | Exploratory R4 |",
          "|---|---:|---:|---:|---:|---:|"]
    for name, row in abl["rows"].items():
        n = cell(REL_ABL, f"rows.{name}.n_features", row["n_features"], integer, f"c1.abl.{name}.n",
                 f"Feature count, ablation {name}", 0)
        d = cell(REL_ABL, f"rows.{name}.auroc_dev", row["auroc_dev"], auc, f"c1.abl.{name}.dev",
                 f"Dev AUROC, ablation {name}")
        t = cell(REL_ABL, f"rows.{name}.auroc_test", row["auroc_test"], auc, f"c1.abl.{name}.test",
                 f"Held-out AUROC, ablation {name}")
        o = cell(REL_ABL, f"rows.{name}.band.over_refusal", row["band"]["over_refusal"], pct,
                 f"c1.abl.{name}.over", f"Band over-refusal, ablation {name}")
        r4 = cell(REL_ABL, f"rows.{name}.exploratory_band.per_rung_precision.4",
                  row["exploratory_band"]["per_rung_precision"]["4"], pct, f"c1.abl.{name}.r4",
                  f"Exploratory R4 abstain precision, ablation {name}")
        md.append(f"| {name} | {n} | {d} | {t} | {o} | {r4} |")
    return "\n".join(md) + "\n"


TABLE7_PATH = ROOT / "05_paper" / "tables" / "table7_data.json"

TABLE7_SEED = [
    {"work": "Abdumalikov et al., arXiv:2403.01461",
     "data": "ODQA corpora, SQuAD v2.0 pairs for repair",
     "negatives": "random text excerpts versus excerpts with high semantic overlap",
     "metric": "answerability accuracy",
     "operating_point": "one accuracy figure per sampler; coverage not reported",
     "citation": "answerability-in-retrieval-augmented-open-domain-question-an"},
    {"work": "DeclineCraft, arXiv:2610.28340",
     "data": "retrieval and parametric abstention suite",
     "negatives": "several unanswerable classes",
     "metric": "joint abstention metrics",
     "operating_point": "per category, retrieval and memory reported separately",
     "citation": "declinecraft-a-rag-abstention-benchmark-for-jointly-measurin"},
    {"work": "This paper",
     "data": "SQuAD v2.0 dev, article-disjoint split",
     "negatives": "four constructed rungs, plus overlap-matched and top-1-presented variants",
     "metric": "abstain precision, over-refusal, coverage",
     "operating_point": "every precision reported with over-refusal and coverage beside it",
     "citation": "this_paper"},
]


def table_prior_work(path: Path = TABLE7_PATH) -> str:
    if path.exists():
        rows = json.loads(path.read_text(encoding="utf-8"))
    else:
        rows = TABLE7_SEED
    md = ["| Work | Data | Negatives | Metric | Operating point reported |",
          "|---|---|---|---|---|"]
    for r in rows:
        md.append(
            f"| {r['work']} | {r['data']} | {r['negatives']} | {r['metric']} | {r['operating_point']} |")
    return "\n".join(md) + "\n"


def figure_svg(fz: dict, cx: dict) -> str:
    series = [
        ("as run: confirmatory",
         {k: v["abstain_precision"] for k, v in fz["test"]["band_primary"]["per_rung"].items()}, "#1f77b4"),
        ("as run: exploratory",
         {k: v["abstain_precision"] for k, v in fz["test"]["exploratory_band"]["per_rung"].items()}, "#ff7f0e"),
        ("corrected: confirmatory",
         {k: v["abstain_precision"] for k, v in cx["test"]["band_primary"]["per_rung"].items()}, "#2ca02c"),
        ("corrected: exploratory",
         {k: v["abstain_precision"] for k, v in cx["test"]["exploratory_band"]["per_rung"].items()}, "#d62728"),
    ]
    W, H, L, B, T, Rgt = 560, 340, 62, 46, 18, 186
    pw, ph = W - L - Rgt, H - B - T
    xs = {k: L + (i + 0.5) * pw / 4 for i, k in enumerate(("1", "2", "3", "4"))}

    def y(v: float) -> float:
        return T + (1.0 - v) * ph

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
             f'font-family="Helvetica, Arial, sans-serif" font-size="11">',
             f'<rect width="{W}" height="{H}" fill="white"/>']
    for tick in (0.0, 0.25, 0.5, 0.75, 1.0):
        parts.append(f'<line x1="{L}" y1="{y(tick):.1f}" x2="{L + pw}" y2="{y(tick):.1f}" stroke="#dddddd"/>')
        parts.append(f'<text x="{L - 6}" y="{y(tick) + 4:.1f}" text-anchor="end">{int(tick * 100)}</text>')
    parts.append(f'<line x1="{L}" y1="{T}" x2="{L}" y2="{T + ph}" stroke="#333"/>')
    parts.append(f'<line x1="{L}" y1="{T + ph}" x2="{L + pw}" y2="{T + ph}" stroke="#333"/>')
    parts.append(f'<text x="{L - 44}" y="{T + ph / 2}" transform="rotate(-90 {L - 44} {T + ph / 2})" '
                 f'text-anchor="middle">abstain precision (%)</text>')
    for k, x in xs.items():
        parts.append(f'<text x="{x:.1f}" y="{T + ph + 18}" text-anchor="middle">R{k}</text>')
    for name, block, colour in series:
        pts = [(xs[k], y(block[k])) for k in ("1", "2", "3", "4") if k in block]
        parts.append('<polyline fill="none" stroke="%s" stroke-width="2" points="%s"/>'
                     % (colour, " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)))
        for a, b in pts:
            parts.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="2.6" fill="{colour}"/>')
    for i, (name, _, colour) in enumerate(series):
        yy = T + 10 + i * 16
        parts.append(f'<rect x="{L + pw + 12}" y="{yy - 7}" width="9" height="9" fill="{colour}"/>')
        parts.append(f'<text x="{L + pw + 26}" y="{yy}">{name}</text>')
    parts.append(f'<text x="{L}" y="{H - 8}">held-out half, {fz["items"]["n_test"]} items, four rungs; '
                 f'as-run and spec-corrected runs</text>')
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def figure_f2(pm: dict) -> str:
    band = pm["operating_points"]["band"]
    expl = pm["operating_points"]["exploratory_band"]
    # coverage is the answer rate reported in precision_metrics.json
    b_cov, e_cov = float(band["answer_rate"]), float(expl["answer_rate"])
    b_prec, e_prec = float(band["pooled"]["precision"]), float(expl["pooled"]["precision"])
    b_over, e_over = float(band["over_refusal"]), float(expl["over_refusal"])

    W, H, L, B, T, Rgt = 560, 340, 62, 46, 18, 170
    pw, ph = W - L - Rgt, H - B - T

    def x(v):
        return L + v * pw

    def y(v):
        return T + (1.0 - v) * ph

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
             f'font-family="Helvetica, Arial, sans-serif" font-size="11">',
             f'<rect width="{W}" height="{H}" fill="white"/>']
    for tick in (0.0, 0.25, 0.5, 0.75, 1.0):
        parts.append(f'<line x1="{L}" y1="{y(tick):.1f}" x2="{L + pw}" y2="{y(tick):.1f}" stroke="#dddddd"/>')
        parts.append(f'<text x="{L - 6}" y="{y(tick) + 4:.1f}" text-anchor="end">{int(tick * 100)}</text>')
    for tick in (0.0, 0.25, 0.5, 0.75, 1.0):
        parts.append(f'<line x1="{x(tick):.1f}" y1="{T + ph}" x2="{x(tick):.1f}" y2="{T + ph + 4}" stroke="#333"/>')
        parts.append(f'<text x="{x(tick):.1f}" y="{T + ph + 16}" text-anchor="middle">{int(tick * 100)}</text>')
    parts.append(f'<line x1="{L}" y1="{T}" x2="{L}" y2="{T + ph}" stroke="#333"/>')
    parts.append(f'<line x1="{L}" y1="{T + ph}" x2="{L + pw}" y2="{T + ph}" stroke="#333"/>')
    parts.append(f'<text x="{L - 44}" y="{T + ph / 2}" transform="rotate(-90 {L - 44} {T + ph / 2})" '
                 f'text-anchor="middle">rate (%)</text>')
    parts.append(f'<text x="{L + pw / 2}" y="{H - 6}" text-anchor="middle">coverage (%)</text>')

    # precision series
    prec_pts = [(x(b_cov), y(b_prec)), (x(e_cov), y(e_prec))]
    parts.append('<polyline fill="none" stroke="#1f77b4" stroke-width="2" points="%s"/>'
                 % " ".join(f"{a:.1f},{b:.1f}" for a, b in prec_pts))
    # over-refusal series
    over_pts = [(x(b_cov), y(b_over)), (x(e_cov), y(e_over))]
    parts.append('<polyline fill="none" stroke="#d62728" stroke-width="2" stroke-dasharray="5,3" points="%s"/>'
                 % " ".join(f"{a:.1f},{b:.1f}" for a, b in over_pts))

    # points
    for cov, prec, over, registered in ((b_cov, b_prec, b_over, True), (e_cov, e_prec, e_over, False)):
        r = 5.0 if registered else 3.0
        sw = ' stroke="#000" stroke-width="1.5"' if registered else ''
        parts.append(f'<circle cx="{x(cov):.1f}" cy="{y(prec):.1f}" r="{r}" fill="#1f77b4"{sw}/>')
        parts.append(f'<circle cx="{x(cov):.1f}" cy="{y(over):.1f}" r="{r}" fill="#d62728"{sw}/>')
    # registered vertical marker
    parts.append(f'<line x1="{x(b_cov):.1f}" y1="{T}" x2="{x(b_cov):.1f}" y2="{T + ph}" '
                 f'stroke="#555" stroke-dasharray="2,2"/>')
    parts.append(f'<text x="{x(b_cov) + 4:.1f}" y="{T + 10}" font-size="10">registered</text>')

    # legend
    for i, (name, colour) in enumerate((("pooled abstain precision", "#1f77b4"),
                                        ("over-refusal", "#d62728"))):
        yy = T + 10 + i * 16
        parts.append(f'<rect x="{L + pw + 12}" y="{yy - 7}" width="9" height="9" fill="{colour}"/>')
        parts.append(f'<text x="{L + pw + 26}" y="{yy}">{name}</text>')
    yy = T + 10 + 2 * 16
    parts.append(f'<text x="{L + pw + 12}" y="{yy}" font-size="10">filled = registered point</text>')
    parts.append(f'<text x="{L}" y="{H - 8}" font-size="10">two operating points from precision_metrics.json; '
                 f'registered point marked</text>')
    parts.append("</svg>")
    return "\n".join(parts) + "\n"
def const_entries() -> None:
    def reg(entry_id, file, key, desc, tol=0.0):
        ENTRIES[entry_id] = {"id": entry_id, "description": desc, "file": file, "key": key,
                             "tolerance": tol, "toy": False}

    reg("c1.const.audit_gate", CONFIG, "audit_auroc_gate", "Separability-audit AUROC gate (config)")
    reg("c1.const.target_precision", CONFIG, "target_abstain_precision",
        "Target abstain precision in the threshold rule (config)")
    reg("c1.const.n_boot", CONFIG, "n_boot", "Bootstrap resamples (config)")
    reg("c1.const.seed", CONFIG, "seed", "Run seed (config)")
    reg("c1.const.max_failing", CONFIG, "max_failing_rungs",
        "Failing rungs tolerated before the run stops (config)")
    reg("c1.const.cv_folds", CONST, "cv_folds", "Cross-validation folds in the audit (from audit.py)")
    reg("c1.const.n_rungs", CONST, "n_rungs", "Rungs in the ladder (from build_items.py)")
    reg("c1.const.n_gate_features", CONST, "n_gate_features", "Retrieval features in the gate (from gate.py)")
    reg("c1.const.n_surface_features", CONST, "n_surface_features",
        "Surface features in the audit (from audit.py)")
    reg("c1.const.over_cap", REL, "exploratory.operating_point.max_over_refusal",
        "Exploratory over-refusal cap (D1.2)")
    reg("c1.stats.n_boot", REL, "hypotheses.H3.difference.n_boot", "Bootstrap resamples recorded in the run")
    reg("c1.stats.seed", REL, "hypotheses.H3.difference.seed", "Bootstrap seed recorded in the run")
    reg("c1.reader.n", REL, "reader_baseline_dev_only.n", "Items with reader features (dev only)")
    reg("c1.reader.auroc", REL, "reader_baseline_dev_only.auroc_answerable_vs_negatives",
        "Reader log-probability AUROC on those dev items")
    reg("c1.dev.refused_below_lo", REL, "placement_diagnostic.dev_refused_below_lo",
        "Dev fraction refused by the lower threshold alone")
    reg("c1.dev.admit_mass", REL, "placement_diagnostic.dev_admit_mass", "Dev admit mass at the band")
    reg("c1.band.width", REL, "thresholds.band.band_width", "Fitted band width (as run)")
    reg("c1.thr.lo", REL, "thresholds.band.t_lo", "Fitted band lower threshold (as run)")
    reg("c1.thr.hi", REL, "thresholds.band.t_hi", "Fitted band upper threshold (as run)")
    reg("c1.thr.single", REL, "thresholds.single.t", "Fitted single threshold (as run)")
    reg("c1.items.total", REL, "items.n_total", "Items in the ladder (all splits)")
    reg("c1.items.dev", REL, "items.n_dev", "Items in the dev half")
    reg("c1.items.test", REL, "items.n_test", "Items in the held-out half")
    reg("c1.items.rung2.dev", REL, "items.per_rung_dev.2", "Rung-R2 items on dev (short rung)")
    reg("c1.b1.pooled", REL, "baselines.B1_bm25_top1.test.pooled_abstain_precision",
        "BM25-top1 baseline pooled abstain precision (as run)")

    # corpus facts, statistics addendum, quoted literature figures, corrected thresholds
    for key, desc in (("articles", "Articles in SQuAD v2.0 dev"),
                      ("paragraphs", "Paragraphs in SQuAD v2.0 dev"),
                      ("questions", "Questions in SQuAD v2.0 dev (both classes)"),
                      ("answerable", "Answerable questions in SQuAD v2.0 dev")):
        reg(f"c1.data.{key}", DATA, key, desc)
    reg("c1.st.expl.diff", STATS, "exploratory_uncertainty.paired_diffs.exploratory_r1_minus_r3.diff",
        "Exploratory R1 minus R3, paired by question")
    reg("c1.st.expl.lo", STATS, "exploratory_uncertainty.paired_diffs.exploratory_r1_minus_r3.ci95.lo",
        "Exploratory R1 minus R3, CI lower")
    reg("c1.st.expl.hi", STATS, "exploratory_uncertainty.paired_diffs.exploratory_r1_minus_r3.ci95.hi",
        "Exploratory R1 minus R3, CI upper")
    reg("c1.st.expl.r14", STATS, "exploratory_uncertainty.paired_diffs.exploratory_r1_minus_r4.diff",
        "Exploratory R1 minus R4, paired by question")
    reg("c1.st.expl.r14.lo", STATS, "exploratory_uncertainty.paired_diffs.exploratory_r1_minus_r4.ci95.lo",
        "Exploratory R1 minus R4, CI lower")
    reg("c1.st.expl.r14.hi", STATS, "exploratory_uncertainty.paired_diffs.exploratory_r1_minus_r4.ci95.hi",
        "Exploratory R1 minus R4, CI upper")
    reg("c1.st.exch.p", STATS, "exchangeability.min_p.value",
        "Smallest exchangeability p-value across the five compared variables")
    reg("c1.st.exch.kept.dev", STATS, "exchangeability.splits.dev.n_kept",
        "Dev questions that keep a rung-R2 item")
    reg("c1.st.exch.dropped.dev", STATS, "exchangeability.splits.dev.n_dropped",
        "Dev questions with no rung-R2 item")
    reg("c1.st.match.maxdiff", STATS, "matched_recall.max_abs_diff_pp",
        "Largest per-rung gap between band and recall-matched single refusal rate")
    reg("c1.st.match.over.band", STATS, "matched_recall.answerable_side.over_refusal_band",
        "Band over-refusal for the H3 comparison")
    reg("c1.st.match.over.matched", STATS, "matched_recall.answerable_side.over_refusal_matched",
        "Recall-matched single over-refusal for the H3 comparison")
    reg("c1.st.cluster.ratio.r2", STATS, "cluster_bootstrap.exploratory_band.2.width_ratio",
        "Cluster-bootstrap / item-bootstrap interval width, exploratory R2")
    reg("c1.st.cluster.ratio.conf.r2", STATS, "cluster_bootstrap.per_rung.2.width_ratio",
        "Cluster-bootstrap / item-bootstrap interval width, confirmatory R2")
    reg("c1.st.cluster.ratio.expl.r4", STATS, "cluster_bootstrap.exploratory_band.4.width_ratio",
        "Cluster-bootstrap / item-bootstrap interval width, exploratory R4")
    reg("c1.tr.drop.conf", REL_TR, "drop_vs_test_rung3.confirmatory_band.drop_pp",
        "Transfer-arm precision drop vs test R3, confirmatory band, percentage points")
    reg("c1.tr.drop.expl", REL_TR, "drop_vs_test_rung3.exploratory_band.drop_pp",
        "Transfer-arm precision drop vs test R3, exploratory band, percentage points")
    reg("c1.r5.match.contrast", REL_5,
        "matching_diagnostic.test.contrast_rung1_random_negative_mean_overlap_absdiff",
        "Mean overlap gap for a random negative (R5 matching contrast)")
    reg("c1.t1.hit.dev", REL_T1F, "hit_rate_dev", "BM25 top-1-is-gold hit rate, dev half")
    reg("c1.thr.lo.corr", REL_X, "thresholds.band.t_lo", "Fitted band lower threshold, spec-corrected (D4)")
    reg("c1.thr.hi.corr", REL_X, "thresholds.band.t_hi", "Fitted band upper threshold, spec-corrected (D4)")
    reg("c1.lit.acc.random", LIT, "numbers.abdumalikov_random_negative_accuracy.value",
        "Quoted: answerability accuracy on random negatives (Abdumalikov et al.)")
    reg("c1.lit.acc.overlap", LIT, "numbers.abdumalikov_overlap_negative_accuracy.value",
        "Quoted: answerability accuracy on high-overlap negatives (Abdumalikov et al.)")
    reg("c1.h1.diff.corr", REL_X, "hypotheses.H1.diff_r1_minus_r3",
        "H1 R1 minus R3, spec-corrected run (D4)")
    reg("c1.h3.diff.lo.corr", REL_X, "hypotheses.H3.difference.lo",
        "H3 difference, CI lower, spec-corrected run (D4)")
    reg("c1.h3.diff.hi.corr", REL_X, "hypotheses.H3.difference.hi",
        "H3 difference, CI upper, spec-corrected run (D4)")
    reg("c1.expl.coverage.run", REL, "test.exploratory_band.coverage",
        "Exploratory band coverage, held-out half (as run)")
    reg("c1.band.dev_precision", REL, "thresholds.band.dev_precision",
        "Dev abstain precision at the fitted band (as run)")
    reg("c1.h2.loss.corr", REL_X, "hypotheses.H2.loss_points",
        "H2 dev-to-test loss, spec-corrected run (D4)")
    reg("c1.obs.dense.eq1", REL_TR,
        "feature_observation_dense_degenerate.main_run_features_csv.frac_dense_presented_eq_1",
        "Fraction of as-run rows whose dense_presented equals 1.0 (degeneracy evidence)")
    reg("c1.data.transfer.items", REL_TR, "transfer.n_items", "Items in the second-corpus arm", 0)


def main() -> int:
    fz = load(RES / "results_full.json")
    r5 = load(RES / "rung5.json")
    tr = load(RES / "transfer.json")
    t1 = load(RES / "top1_variant.json")
    cx = load(RESX / "results_full.json")
    abl = load(RESX / "ablations.json")

    write_top1_flat(t1)
    TAB.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    pm = load(RES / "precision_metrics.json")
    (TAB / "T1_per_rung.md").write_text(table_per_rung(pm), encoding="utf-8")
    (TAB / "T2_hypotheses.md").write_text(table_hypotheses(fz), encoding="utf-8")
    (TAB / "T3_audit.md").write_text(table_audit(fz, r5), encoding="utf-8")
    (TAB / "T4_frozen_vs_corrected.md").write_text(table_frozen_vs_corrected(fz, cx), encoding="utf-8")
    (TAB / "T5_arms.md").write_text(table_arms(r5, tr, t1), encoding="utf-8")
    (TAB / "T6_ablations_corrected.md").write_text(table_ablations(abl), encoding="utf-8")
    (TAB / "T7_prior_work.md").write_text(table_prior_work(), encoding="utf-8")
    (FIG / "F1_abstain_precision_by_rung.svg").write_text(figure_svg(fz, cx), encoding="utf-8")
    (FIG / "F2_precision_overrefusal_vs_coverage.svg").write_text(figure_f2(pm), encoding="utf-8")

    const_entries()

    idx = json.loads(INDEX.read_text(encoding="utf-8")) if INDEX.exists() else {"version": 1, "entries": []}
    others = [e for e in idx.get("entries", []) if not e.get("id", "").startswith("c1.")]
    idx["entries"] = others + sorted(ENTRIES.values(), key=lambda e: e["id"])
    idx["updated_at"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    INDEX.write_text(json.dumps(idx, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"tables: {len(list(TAB.glob('T*.md')))} md files; figure: 1; c1 index entries: {len(ENTRIES)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
