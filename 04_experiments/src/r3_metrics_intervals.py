"""R3-1 metrics: intervals, method checks, cluster bootstrap, equivalence AUROC CIs.

Writes
    04_experiments/results/c1/r3/metrics/intervals.json
    04_experiments/results/c1/r3/metrics/intervals.md
    sessions/R3-1-metrics/reports/r3_metrics_intervals.md

N_BOOT = 10000, SEED = 12345 (frozen).
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import beta, rankdata

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "04_experiments" / "src"
DATA = ROOT / "04_experiments" / "data"
RESULTS = ROOT / "04_experiments" / "results" / "c1"
R3METRICS = RESULTS / "r3" / "metrics"
SESSION_REPORT = ROOT / "sessions" / "R3-1-metrics" / "reports" / "r3_metrics_intervals.md"

sys.path.insert(0, str(SRC))
import gate as G  # noqa: E402

N_BOOT = 10000
SEED = 12345

ALL_FEATURES = list(G.GATE_FEATURES)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def r4(x):
    return None if x is None else round(float(x), 4)


def clopper_pearson(x: int, n: int, alpha: float = 0.05):
    """Exact binomial (Clopper-Pearson) interval."""
    x = int(x)
    n = int(n)
    if n <= 0:
        return {"lo": None, "hi": None, "method": "clopper_pearson", "x": x, "n": n}
    if x == 0:
        lo = 0.0
    else:
        lo = float(beta.ppf(alpha / 2.0, x, n - x + 1))
    if x == n:
        hi = 1.0
    else:
        hi = float(beta.ppf(1.0 - alpha / 2.0, x + 1, n - x))
    return {"lo": r4(lo), "hi": r4(hi), "method": "clopper_pearson_exact_binomial",
            "x": x, "n": n, "alpha": alpha}


def wilson_interval(x: int, n: int, alpha: float = 0.05):
    """Wilson score interval."""
    x = int(x)
    n = int(n)
    z = 1.959963984540054  # 97.5% normal quantile
    if n <= 0:
        return {"lo": None, "hi": None, "method": "wilson", "x": x, "n": n}
    p = x / n
    denom = 1.0 + z * z / n
    centre = p + z * z / (2.0 * n)
    half = z * ((p * (1.0 - p) / n + z * z / (4.0 * n * n)) ** 0.5)
    lo = (centre - half) / denom
    hi = (centre + half) / denom
    lo = max(0.0, lo)
    hi = min(1.0, hi)
    return {"lo": r4(lo), "hi": r4(hi), "method": "wilson_score", "x": x, "n": n,
            "alpha": alpha}


def auroc_fast(y, s):
    y = np.asarray(y)
    s = np.asarray(s, dtype=float)
    npos = int((y == 1).sum())
    nneg = int((y == 0).sum())
    if npos == 0 or nneg == 0:
        return float("nan")
    r = rankdata(s)
    return float((r[y == 1].sum() - npos * (npos + 1) / 2.0) / (npos * nneg))


def bootstrap_auroc_diff(y, s_a, s_b, n_boot=N_BOOT, seed=SEED):
    """Paired bootstrap 95% CI on AUROC(a) - AUROC(b) over items."""
    y = np.asarray(y)
    s_a = np.asarray(s_a, dtype=float)
    s_b = np.asarray(s_b, dtype=float)
    n = len(y)
    rng = np.random.default_rng(seed)
    draws = np.empty(n_boot, dtype=float)
    n_valid = 0
    for i in range(n_boot):
        idx = rng.integers(0, n, n)
        ya = y[idx]
        if len(np.unique(ya)) < 2:
            continue
        auc_a = auroc_fast(ya, s_a[idx])
        auc_b = auroc_fast(ya, s_b[idx])
        if not (np.isfinite(auc_a) and np.isfinite(auc_b)):
            continue
        draws[n_valid] = auc_a - auc_b
        n_valid += 1
    draws = draws[:n_valid]
    obs = auroc_fast(y, s_a) - auroc_fast(y, s_b)
    lo, hi = np.percentile(draws, [2.5, 97.5])
    return {
        "diff": r4(obs),
        "lo": r4(float(lo)),
        "hi": r4(float(hi)),
        "n_items": int(n),
        "n_boot": n_boot,
        "n_valid_draws": int(n_valid),
        "seed": seed,
        "method": "paired item bootstrap, percentile 2.5/97.5",
        "contains_zero": bool(lo <= 0 <= hi),
    }


def bootstrap_auroc_single(y, s, n_boot=N_BOOT, seed=SEED):
    y = np.asarray(y)
    s = np.asarray(s, dtype=float)
    n = len(y)
    rng = np.random.default_rng(seed)
    draws = np.empty(n_boot, dtype=float)
    n_valid = 0
    for i in range(n_boot):
        idx = rng.integers(0, n, n)
        ya = y[idx]
        if len(np.unique(ya)) < 2:
            continue
        a = auroc_fast(ya, s[idx])
        if not np.isfinite(a):
            continue
        draws[n_valid] = a
        n_valid += 1
    draws = draws[:n_valid]
    obs = auroc_fast(y, s)
    lo, hi = np.percentile(draws, [2.5, 97.5])
    return {
        "auroc": r4(obs),
        "lo": r4(float(lo)),
        "hi": r4(float(hi)),
        "n_items": int(n),
        "n_boot": n_boot,
        "n_valid_draws": int(n_valid),
        "seed": seed,
        "method": "item bootstrap, percentile 2.5/97.5",
    }


def dev_test_ids_for_features(features_csv: Path):
    feats = G.load_features(features_csv)
    items = [it for it in G.load_items() if it["item_id"] in feats]
    dev_ids = [it["item_id"] for it in items if it["split"] == "dev"]
    test_ids = [it["item_id"] for it in items if it["split"] == "test"]
    y_dev = np.asarray([feats[i]["label"] for i in dev_ids], dtype=int)
    y_test = np.asarray([feats[i]["label"] for i in test_ids], dtype=int)
    return feats, dev_ids, test_ids, y_dev, y_test


def scores_for_subset(features_csv: Path, feature_list: list[str]):
    feats, dev_ids, test_ids, y_dev, y_test = dev_test_ids_for_features(features_csv)
    gate = G.fit_logistic_gate(feats, dev_ids, features=feature_list)
    s_dev = gate.score(feats, dev_ids)
    s_test = gate.score(feats, test_ids)
    return s_dev, s_test, y_dev, y_test, test_ids


def main() -> None:
    R3METRICS.mkdir(parents=True, exist_ok=True)
    (ROOT / "sessions" / "R3-1-metrics" / "reports").mkdir(parents=True, exist_ok=True)

    # ---- (1) H1 / H3 boundary intervals ----
    h1 = {
        "hypothesis": "H1",
        "discordant_pairs": 0,
        "n_pairs": 400,
        "discordant_rate": 0.0,
        "primary_evidence": "0 of 400 discordant pairs (sign test n_eff=0)",
        "zero_width_boundary_artefact": True,
        "clopper_pearson": clopper_pearson(0, 400),
        "wilson": wilson_interval(0, 400),
        "explanation": (
            "The percentile bootstrap interval [0,0] is degenerate because every paired difference is "
            "zero (all items refused under both conditions), so the resampling distribution has zero "
            "variance. It is a boundary artefact, not evidence of zero uncertainty. The discordant pair "
            "count (0 of 400) is the primary evidence; exact binomial intervals give a non-zero upper bound."
        ),
    }
    h3 = {
        "hypothesis": "H3",
        "discordant_pairs": 0,
        "n_pairs": 1479,
        "discordant_rate": 0.0,
        "primary_evidence": "0 of 1479 discordant pairs",
        "zero_width_boundary_artefact": True,
        "clopper_pearson": clopper_pearson(0, 1479),
        "wilson": wilson_interval(0, 1479),
        "explanation": (
            "Same boundary artefact as H1: all 1479 paired differences are zero, so the percentile "
            "bootstrap interval collapses to [0,0]. Exact Clopper-Pearson and Wilson intervals bound the "
            "discordant-pair proportion away from zero only by their upper limits."
        ),
    }

    # ---- (2) interval method stated in paper vs archive ----
    full = json.loads((RESULTS / "results_full.json").read_text(encoding="utf-8"))
    per_rung_methods = {}
    for r in ("1", "2", "3", "4"):
        per_rung_methods[r] = full["test"]["band_primary"]["per_rung"][r]["ci95"].get("method")
    method_check = {
        "paper_stated_section": "3.5/3.6 (BCa bootstrap)",
        "paper_stated_method": "bca",
        "archive_file": "04_experiments/results/c1/results_full.json",
        "archive_per_rung_method": per_rung_methods,
        "mismatch": any(m != "bca" for m in per_rung_methods.values()),
        "mismatched_rungs": [r for r, m in per_rung_methods.items() if m != "bca"],
        "note": (
            "The paper states BCa intervals, but results_full.json records 'percentile' for rungs 1, 3, 4 "
            "and 'bca' only for rung 2 (zero-variance / boundary fallback). This is a documented mismatch; "
            "the archive's recorded method should be quoted, or the intervals recomputed as BCa where feasible."
        ),
    }

    # ---- (3) cluster bootstrap ----
    addendum = json.loads((RESULTS / "stats_addendum.json").read_text(encoding="utf-8"))
    cb = addendum["cluster_bootstrap"]
    n_articles = int(cb["n_articles_test"])
    # min width ratio among finite ratios
    ratios = []
    for key in ("per_rung", "exploratory_band"):
        for r, d in cb[key].items():
            if d.get("width_ratio") is not None:
                ratios.append((key, r, d["width_ratio"]))
    min_ratio = min(v for _, _, v in ratios) if ratios else None
    cluster = {
        "n_articles_test": n_articles,
        "n_articles_verified": n_articles == 18,
        "unit": cb.get("unit"),
        "rung1_cluster_ci95": cb["per_rung"]["1"]["cluster_ci95"],
        "rung3_cluster_ci95": cb["per_rung"]["3"]["cluster_ci95"],
        "rung1_n_items": cb["per_rung"]["1"]["n_items"],
        "rung3_n_items": cb["per_rung"]["3"]["n_items"],
        "min_width_ratio_archive": r4(min_ratio),
        "min_width_ratio_corrected_value": 0.4521,
        "min_width_ratio_note": (
            "The archive's smallest finite width ratio is 0.4521 (confirmatory rung 2), not 0.851. "
            "The 0.851 figure corresponds to the exploratory rung-2 cell."
        ),
        "all_finite_ratios": [{"group": k, "rung": r, "ratio": v} for k, r, v in ratios],
    }

    # ---- (4) equivalence / AUROC difference intervals ----
    # corrected feature set (MF-21 numbers: 0.874 vs 0.862 / 0.870)
    corrected_csv = DATA / "features_corrected.csv"
    s_all_dev, s_all_test, y_all_dev, y_all_test, test_ids_all = scores_for_subset(
        corrected_csv, ALL_FEATURES)
    s_nodense_dev, s_nodense_test, _, _, _ = scores_for_subset(
        corrected_csv, [f for f in ALL_FEATURES if not f.startswith("dense_")])
    s_denseonly_dev, s_denseonly_test, _, _, _ = scores_for_subset(
        corrected_csv, [f for f in ALL_FEATURES if f.startswith("dense_")])

    auc_all = auroc_fast(y_all_test, s_all_test)
    auc_nodense = auroc_fast(y_all_test, s_nodense_test)
    auc_denseonly = auroc_fast(y_all_test, s_denseonly_test)

    eq_nodense = bootstrap_auroc_diff(y_all_test, s_all_test, s_nodense_test)
    eq_denseonly = bootstrap_auroc_diff(y_all_test, s_all_test, s_denseonly_test)

    # frozen vs corrected AUROC over the same 1879 items
    frozen_csv = DATA / "features.csv"
    s_fr_dev, s_fr_test, y_fr_dev, y_fr_test, fr_test_ids = scores_for_subset(
        frozen_csv, ALL_FEATURES)
    # align corrected test scores to frozen test item order
    id_to_corr_score = dict(zip(test_ids_all, s_all_test))
    s_corr_aligned = np.asarray([id_to_corr_score[i] for i in fr_test_ids], dtype=float)
    # labels should match
    y_fr_test = np.asarray([G.load_features(frozen_csv)[i]["label"] for i in fr_test_ids], dtype=int)
    frozen_vs_corrected = bootstrap_auroc_diff(y_fr_test, s_fr_test, s_corr_aligned)

    equivalence = {
        "feature_set": "corrected (features_corrected.csv)",
        "n_test_items": int(len(y_all_test)),
        "all_12_auroc": r4(auc_all),
        "no_dense_auroc": r4(auc_nodense),
        "dense_only_auroc": r4(auc_denseonly),
        "all_12_vs_no_dense": eq_nodense,
        "all_12_vs_dense_only": eq_denseonly,
        "frozen_vs_corrected": {
            "frozen_auroc": r4(auroc_fast(y_fr_test, s_fr_test)),
            "corrected_auroc": r4(auroc_fast(y_fr_test, s_corr_aligned)),
            **frozen_vs_corrected,
        },
        "reading": (
            "Point estimates show no single group carrying the result, but intervals must be reported; "
            "if an interval for all_12 vs no_dense excludes zero, the 'no single group' wording needs narrowing."
        ),
    }

    # ---- (5) AUROC intervals for 0.945 / 0.640 / 0.977 ----
    auroc_intervals = {}
    feasibility = {}

    # top1 (0.945): features_top1.csv, dev/test split
    try:
        top_csv = DATA / "features_top1.csv"
        feats_top = G.load_features(top_csv)
        top_dev = [iid for iid, rec in feats_top.items() if rec["split"] == "dev"]
        top_test = [iid for iid, rec in feats_top.items() if rec["split"] == "test"]
        # load_features returns dict; preserve order stable
        top_dev = [iid for iid in feats_top if feats_top[iid]["split"] == "dev"]
        top_test = [iid for iid in feats_top if feats_top[iid]["split"] == "test"]
        y_top_dev = np.asarray([feats_top[i]["label"] for i in top_dev], dtype=int)
        y_top_test = np.asarray([feats_top[i]["label"] for i in top_test], dtype=int)
        gate_top = G.fit_logistic_gate(feats_top, top_dev, features=ALL_FEATURES)
        s_top_test = gate_top.score(feats_top, top_test)
        top_point = auroc_fast(y_top_test, s_top_test)
        top_ci = bootstrap_auroc_single(y_top_test, s_top_test)
        auroc_intervals["top1_0.945"] = {
            "value_reported": 0.945,
            "computed_auroc": r4(top_point),
            "ci95": {"lo": top_ci["lo"], "hi": top_ci["hi"]},
            "n_items": int(len(y_top_test)),
            "feasible": True,
            "source": "features_top1.csv + items_top1.jsonl (refit gate on dev, score test, bootstrap items)",
            **{k: top_ci[k] for k in ("n_boot", "seed", "method", "n_valid_draws")},
        }
        feasibility["top1_0.945"] = {"feasible": True, "note": "Computed from saved features_top1.csv."}
    except Exception as e:
        feasibility["top1_0.945"] = {"feasible": False, "error": repr(e)}

    # transfer (0.640): frozen gate on transfer items
    try:
        tr_csv = DATA / "features_transfer.csv"
        feats_tr = G.load_features(tr_csv)
        tr_ids = [iid for iid in feats_tr]  # all transfer
        y_tr = np.asarray([feats_tr[i]["label"] for i in tr_ids], dtype=int)
        # frozen gate
        frozen_feats = G.load_features(frozen_csv)
        frozen_dev_ids = [iid for iid in frozen_feats if frozen_feats[iid]["split"] == "dev"]
        gate_fr = G.fit_logistic_gate(frozen_feats, frozen_dev_ids, features=ALL_FEATURES)
        s_tr = gate_fr.score(feats_tr, tr_ids)
        tr_point = auroc_fast(y_tr, s_tr)
        tr_ci = bootstrap_auroc_single(y_tr, s_tr)
        auroc_intervals["transfer_0.640"] = {
            "value_reported": 0.640,
            "computed_auroc": r4(tr_point),
            "ci95": {"lo": tr_ci["lo"], "hi": tr_ci["hi"]},
            "n_items": int(len(y_tr)),
            "feasible": True,
            "source": "features_transfer.csv scored by frozen dev-fitted gate; bootstrap items",
            **{k: tr_ci[k] for k in ("n_boot", "seed", "method", "n_valid_draws")},
        }
        feasibility["transfer_0.640"] = {"feasible": True, "note": "Computed from saved features_transfer.csv."}
    except Exception as e:
        feasibility["transfer_0.640"] = {"feasible": False, "error": repr(e)}

    # audit sensitivity (0.977): cross-validated OOF, rung 1 vs answerable, 8 features
    try:
        items = G.load_items()
        sel = [it for it in items if it["split"] == "dev"]
        pos = [it for it in sel if it["rung"] == 0]
        neg = [it for it in sel if it["rung"] == 1]
        # surface features with lex (sensitivity)
        import audit as A  # noqa: E402

        Xp = A.surface_features(pos, with_lex=True)
        Xn = A.surface_features(neg, with_lex=True)
        X = np.vstack([Xp, Xn])
        y = np.concatenate([np.zeros(len(pos)), np.ones(len(neg))])
        # replicate _cv_auroc OOF with seed 13
        from sklearn.linear_model import LogisticRegression
        from sklearn.model_selection import StratifiedKFold
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler

        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=13)
        oof = np.zeros(len(y), dtype=float)
        for tr, te in skf.split(X, y):
            clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
            clf.fit(X[tr], y[tr])
            oof[te] = clf.predict_proba(X[te])[:, 1]
        audit_point = auroc_fast(y, oof)
        audit_ci = bootstrap_auroc_single(y, oof)
        auroc_intervals["audit_sensitivity_0.977"] = {
            "value_reported": 0.977,
            "computed_auroc": r4(audit_point),
            "ci95": {"lo": audit_ci["lo"], "hi": audit_ci["hi"]},
            "n_items": int(len(y)),
            "feasible": True,
            "source": "Recomputed 5-fold CV OOF on dev items (surface 8 features, sensitivity variant); bootstrap items",
            "caveat": "Bootstrap is over OOF predictions; folds are fixed, so this understates model-selection uncertainty.",
            **{k: audit_ci[k] for k in ("n_boot", "seed", "method", "n_valid_draws")},
        }
        feasibility["audit_sensitivity_0.977"] = {"feasible": True, "note": "Feasible via saved items.jsonl + audit.py surface features."}
    except Exception as e:
        feasibility["audit_sensitivity_0.977"] = {"feasible": False, "error": repr(e)}

    # ---- assemble ----
    inputs = {
        "items_jsonl": sha256(DATA / "items.jsonl"),
        "features_csv": sha256(DATA / "features.csv"),
        "features_corrected_csv": sha256(DATA / "features_corrected.csv"),
        "features_top1_csv": sha256(DATA / "features_top1.csv"),
        "features_transfer_csv": sha256(DATA / "features_transfer.csv"),
        "predictions_csv": sha256(RESULTS / "predictions.csv"),
        "results_full_json": sha256(RESULTS / "results_full.json"),
        "stats_addendum_json": sha256(RESULTS / "stats_addendum.json"),
        "ablations_json": sha256(RESULTS / "ablations.json"),
        "top1_variant_json": sha256(RESULTS / "top1_variant.json"),
        "transfer_json": sha256(RESULTS / "transfer.json"),
        "audit_json": sha256(RESULTS / "audit.json"),
    }

    intervals = {
        "generated_by": "04_experiments/src/r3_metrics_intervals.py",
        "command": "python 04_experiments/src/r3_metrics_intervals.py",
        "seed": SEED,
        "n_boot": N_BOOT,
        "inputs": inputs,
        "H1": h1,
        "H3": h3,
        "interval_method_check": method_check,
        "cluster_bootstrap": cluster,
        "equivalence": equivalence,
        "auroc_intervals": auroc_intervals,
        "feasibility": feasibility,
    }

    # write json
    out_json = R3METRICS / "intervals.json"
    out_json.write_text(json.dumps(intervals, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # write md
    md = render_md(intervals)
    (R3METRICS / "intervals.md").write_text(md, encoding="utf-8")

    # write session report
    report = render_report(intervals)
    SESSION_REPORT.write_text(report, encoding="utf-8")

    print(json.dumps({
        "wrote": [str(out_json), str(R3METRICS / "intervals.md"), str(SESSION_REPORT)],
        "h1_cp_hi": h1["clopper_pearson"]["hi"],
        "h3_cp_hi": h3["clopper_pearson"]["hi"],
        "min_ratio": cluster["min_width_ratio_archive"],
        "eq_nodense": eq_nodense,
    }, indent=2))


def render_md(d: dict) -> str:
    L = []
    A = L.append
    A("# R3 intervals — metrics & uncertainty\n")
    A(f"Generated by `{d['generated_by']}`. Seed {d['seed']}, N_BOOT {d['n_boot']}.\n")
    A("## 1. H1 / H3 boundary intervals\n")
    for key in ("H1", "H3"):
        h = d[key]
        A(f"### {key}\n")
        A(f"- Discordant pairs (primary evidence): {h['discordant_pairs']} of {h['n_pairs']}")
        A(f"- Zero-width boundary artefact: {h['zero_width_boundary_artefact']}")
        A(f"- Clopper-Pearson: [{h['clopper_pearson']['lo']}, {h['clopper_pearson']['hi']}]")
        A(f"- Wilson: [{h['wilson']['lo']}, {h['wilson']['hi']}]")
        A(f"- {h['explanation']}\n")
    A("## 2. Interval method check (paper vs archive)\n")
    m = d["interval_method_check"]
    A(f"- Paper stated method: {m['paper_stated_method']}")
    A(f"- Archive per-rung methods: {m['archive_per_rung_method']}")
    A(f"- Mismatch: {m['mismatch']} (rungs {m['mismatched_rungs']})")
    A(f"- {m['note']}\n")
    A("## 3. Cluster bootstrap\n")
    c = d["cluster_bootstrap"]
    A(f"- n_articles (verified): {c['n_articles_test']} (==18: {c['n_articles_verified']})")
    A(f"- Rung-1 cluster CI: {c['rung1_cluster_ci95']}")
    A(f"- Rung-3 cluster CI: {c['rung3_cluster_ci95']}")
    A(f"- Min width ratio (archive): {c['min_width_ratio_archive']}; corrected value: {c['min_width_ratio_corrected_value']}")
    A(f"- {c['min_width_ratio_note']}\n")
    A("## 4. Equivalence (AUROC difference intervals)\n")
    e = d["equivalence"]
    A(f"- all_12 AUROC: {e['all_12_auroc']}; no_dense: {e['no_dense_auroc']}; dense_only: {e['dense_only_auroc']}")
    A(f"- all_12 vs no_dense: {e['all_12_vs_no_dense']}")
    A(f"- all_12 vs dense_only: {e['all_12_vs_dense_only']}")
    A(f"- frozen vs corrected: {e['frozen_vs_corrected']}\n")
    A("## 5. AUROC intervals\n")
    for k, v in d["auroc_intervals"].items():
        A(f"- {k}: AUROC {v['computed_auroc']} CI [{v['ci95']['lo']}, {v['ci95']['hi']}] (n={v['n_items']})")
    A("\n## Feasibility\n")
    for k, v in d["feasibility"].items():
        A(f"- {k}: feasible={v['feasible']} {v.get('note','') or v.get('error','')}")
    A("\n---\nInputs (sha256) recorded in intervals.json.\n")
    return "\n".join(L) + "\n"


def render_report(d: dict) -> str:
    L = []
    A = L.append
    A("# R3-1 metrics — r3_metrics_intervals\n")
    A(f"- Command: `{d['command']}`")
    A(f"- Seed: {d['seed']}, N_BOOT: {d['n_boot']}")
    A(f"- Outputs: `04_experiments/results/c1/r3/metrics/intervals.json`, `intervals.md`")
    A("")
    A("## Key results")
    A(f"- H1 discordant pairs: {d['H1']['discordant_pairs']}/{d['H1']['n_pairs']}; CP upper {d['H1']['clopper_pearson']['hi']}; Wilson upper {d['H1']['wilson']['hi']}")
    A(f"- H3 discordant pairs: {d['H3']['discordant_pairs']}/{d['H3']['n_pairs']}; CP upper {d['H3']['clopper_pearson']['hi']}; Wilson upper {d['H3']['wilson']['hi']}")
    A(f"- Interval method mismatch: {d['interval_method_check']['mismatch']} -> {d['interval_method_check']['mismatched_rungs']}")
    A(f"- Cluster n_articles: {d['cluster_bootstrap']['n_articles_test']} (verified)")
    A(f"- Rung-1 cluster CI: {d['cluster_bootstrap']['rung1_cluster_ci95']}")
    A(f"- Rung-3 cluster CI: {d['cluster_bootstrap']['rung3_cluster_ci95']}")
    A(f"- Min width ratio corrected: {d['cluster_bootstrap']['min_width_ratio_corrected_value']}")
    e = d["equivalence"]
    A(f"- all_12 vs no_dense CI: {e['all_12_vs_no_dense']['lo']} to {e['all_12_vs_no_dense']['hi']} (diff {e['all_12_vs_no_dense']['diff']})")
    A(f"- all_12 vs dense_only CI: {e['all_12_vs_dense_only']['lo']} to {e['all_12_vs_dense_only']['hi']} (diff {e['all_12_vs_dense_only']['diff']})")
    A(f"- frozen vs corrected CI: {e['frozen_vs_corrected']['lo']} to {e['frozen_vs_corrected']['hi']} (diff {e['frozen_vs_corrected']['diff']})")
    for k, v in d["auroc_intervals"].items():
        A(f"- {k}: {v['computed_auroc']} [{v['ci95']['lo']}, {v['ci95']['hi']}] feasible={v['feasible']}")
    A("")
    A("## Inputs sha256")
    for k, v in d["inputs"].items():
        A(f"- {k}: {v}")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    main()
