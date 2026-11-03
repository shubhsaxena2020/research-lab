"""C1 — reviewer-demanded ablation: the gate without presented-passage rank features.

Answers the top must-fix from round-1 review ("the gate can identify rung-0 items from construction
artefacts"). Same items, same seeds, same threshold rule; the only change is that `bm25_rank_log` and
`dense_rank_log` are removed from the feature vector. Writes `04_experiments/results/c1/ablation_no_rank.json`
and appends the numbers to `results_full.json` under `ablation_no_rank` so the paper can cite them.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "04_experiments" / "src"))
import gate as G  # noqa: E402

DROP = {"bm25_rank_log", "dense_rank_log"}


def run() -> dict:
    feats = G.load_features()
    items = [it for it in G.load_items() if it["item_id"] in feats]
    by_id = {it["item_id"]: it for it in items}
    feats12 = G.GATE_FEATURES
    G.GATE_FEATURES = [c for c in feats12 if c not in DROP]
    try:
        dev = [it["item_id"] for it in items if it["split"] == "dev"]
        test = [it["item_id"] for it in items if it["split"] == "test"]
        y_dev = np.asarray([feats[i]["label"] for i in dev])
        gate = G.fit_logistic_gate(feats, dev)
        s_dev, s_test = gate.score(feats, dev), gate.score(feats, test)
        band = G.fit_band_thresholds(s_dev, y_dev)
        single = G.fit_single_threshold(s_dev, y_dev)
        ref = G.refused_band(s_test, band["t_lo"], band["t_hi"])
        blocks = G.metrics_block(ref, [by_id[i] for i in test], s_test, "ablation_no_rank_band")
        from sklearn.metrics import roc_auc_score
        return {
            "features": G.GATE_FEATURES,
            "n_features": len(G.GATE_FEATURES),
            "thresholds": {"band": band, "single": single},
            "test": blocks,
            "auroc_dev": round(float(roc_auc_score(y_dev, s_dev)), 4),
            "auroc_test": round(float(roc_auc_score(np.asarray([feats[i]["label"] for i in test]), s_test)), 4),
            "note": "same items, seeds and threshold rule; only the two presented-passage rank features removed",
        }
    finally:
        G.GATE_FEATURES = feats12


def main() -> None:
    out = run()
    p = ROOT / "04_experiments" / "results" / "c1" / "ablation_no_rank.json"
    p.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    full = ROOT / "04_experiments" / "results" / "c1" / "results_full.json"
    r = json.loads(full.read_text(encoding="utf-8"))
    r["ablation_no_rank"] = out
    full.write_text(json.dumps(r, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"auroc_test": out["auroc_test"], "over_refusal": out["test"]["over_refusal"],
                      "per_rung": {k: v["abstain_precision"] for k, v in out["test"]["per_rung"].items()},
                      "band": out["thresholds"]["band"]}, indent=2))


if __name__ == "__main__":
    main()
