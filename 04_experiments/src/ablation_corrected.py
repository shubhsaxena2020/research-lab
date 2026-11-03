"""C1 — stage 6 (D4): leave-one-group-out ablations on the SPEC-CONFORMANT feature set.

The frozen run's dense block is degenerate (features.py scored the presented passage against
itself), so an ablation table computed on it cannot say what the dense features do. This script
recomputes the same leave-one-group-out table on `data/features_corrected.csv` (D4), where the
dense query is the question. It imports gate.py and reuses its threshold rule; no metric is
re-derived by hand.

Run: python 04_experiments/src/ablation_corrected.py
Writes: 04_experiments/results/c1_corrected/ablations.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "04_experiments" / "src"))

import gate as G  # noqa: E402

FEATURES_CSV = ROOT / "04_experiments" / "data" / "features_corrected.csv"
OUT = ROOT / "04_experiments" / "results" / "c1_corrected" / "ablations.json"
CORRECTED_FULL = ROOT / "04_experiments" / "results" / "c1_corrected" / "results_full.json"

ALL = list(G.GATE_FEATURES)
GROUPS = {
    "all_12": ALL,
    "no_lex_overlap": [f for f in ALL if f != "lex_overlap"],
    "no_cross_encoder": [f for f in ALL if f != "ce_presented"],
    "no_dense": [f for f in ALL if not f.startswith("dense_")],
    "no_bm25": [f for f in ALL if not f.startswith("bm25_")],
    "no_rank": [f for f in ALL if f not in ("bm25_rank_log", "dense_rank_log")],
    "lex_overlap_only": ["lex_overlap"],
    "dense_only": [f for f in ALL if f.startswith("dense_")],
}


def main() -> int:
    from sklearn.metrics import roc_auc_score

    items = G.load_items()
    feats = G.load_features(FEATURES_CSV)
    ids = [it["item_id"] for it in items if it["item_id"] in feats]
    by_id = {it["item_id"]: it for it in items}
    dev = [i for i in ids if by_id[i]["split"] == "dev"]
    test = [i for i in ids if by_id[i]["split"] == "test"]
    y_dev = np.asarray([feats[i]["label"] for i in dev])
    y_test = np.asarray([feats[i]["label"] for i in test])

    rows = {}
    for name, featset in GROUPS.items():
        g = G.fit_logistic_gate(feats, dev, features=featset)
        s_dev, s_test = g.score(feats, dev), g.score(feats, test)
        band = G.fit_band_thresholds(s_dev, y_dev)
        xband = G.fit_band_constrained(s_dev, y_dev, 0.10)
        ref = G.refused_band(s_test, band["t_lo"], band["t_hi"])
        refx = G.refused_band(s_test, xband["t_lo"], xband["t_hi"])
        block = G.metrics_block(ref, [by_id[i] for i in test], s_test, name)
        block_x = G.metrics_block(refx, [by_id[i] for i in test], s_test, name + "_exploratory")
        rows[name] = {
            "n_features": len(featset),
            "features": featset,
            "auroc_dev": round(float(roc_auc_score(y_dev, s_dev)), 4),
            "auroc_test": round(float(roc_auc_score(y_test, s_test)), 4),
            "band": {"thresholds": {k: band.get(k) for k in ("t_lo", "t_hi", "dev_precision", "dev_recall")},
                     "over_refusal": block["over_refusal"], "coverage": block["coverage"],
                     "per_rung_precision": {k: v["abstain_precision"] for k, v in block["per_rung"].items()}},
            "exploratory_band": {"thresholds": {k: xband.get(k) for k in ("t_lo", "t_hi", "dev_precision",
                                                                        "dev_recall", "dev_over_refusal")},
                                 "over_refusal": block_x["over_refusal"], "coverage": block_x["coverage"],
                                 "per_rung_precision": {k: v["abstain_precision"]
                                                        for k, v in block_x["per_rung"].items()}},
        }
        print(f"{name:20s} n_feat={len(featset):2d} dev={rows[name]['auroc_dev']:.4f} "
              f"test={rows[name]['auroc_test']:.4f} over_ref={block['over_refusal']:.4f}",
              file=sys.stderr)

    # reproduction check against the corrected full run
    full = json.loads(CORRECTED_FULL.read_text(encoding="utf-8"))
    ref_auc = full["discrimination"]["test_auroc"]
    ok = abs(rows["all_12"]["auroc_test"] - ref_auc) <= 1e-3
    print(f"reproduction: all_12 test AUROC {rows['all_12']['auroc_test']:.4f} vs "
          f"results_full {ref_auc:.4f} -> {'OK' if ok else 'MISMATCH'}", file=sys.stderr)
    if not ok:
        return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "experiment": "c1",
        "label": "SPEC-CORRECTED ABLATIONS (D4) - exploratory, not the pre-registered analysis",
        "features_file": "04_experiments/data/features_corrected.csv",
        "generated_by": "04_experiments/src/ablation_corrected.py",
        "rule": "logistic gate on dev, band threshold at dev abstain precision >= 0.80; exploratory band adds dev over-refusal <= 0.10",
        "reproduction_check": {"all_12_test_auroc": rows["all_12"]["auroc_test"],
                               "results_full_test_auroc": ref_auc, "ok": bool(ok)},
        "rows": rows,
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
