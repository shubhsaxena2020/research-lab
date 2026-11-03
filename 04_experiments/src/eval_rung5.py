"""C1 — EXPLORATORY rung 5 evaluation + separability audit (PREREGISTRATION.md §10 D2).

What this does, in order:

1. Loads rungs 0-4 from `data/items.jsonl` + `data/features.csv` and rung 5 from
   `data/items_rung5.jsonl` + `data/features_rung5.csv`.
2. Re-fits the frozen logistic gate with `gate.fit_logistic_gate` on the **dev** ids of rungs 0-4 only,
   and ASSERTS that every coefficient and the intercept reproduce `results_full.json['gate']` to 1e-3.
   Aborts loudly otherwise — a mismatch means the rung-5 numbers would not be the frozen gate's.
3. Reads the frozen thresholds from `results_full.json` (confirmatory band and exploratory band). No
   threshold is refitted here.
4. Scores the test rung-5 items and reports abstain precision (fraction refused), its BCa 95% CI via
   `gate.ci_mean`, and n, at both operating points, next to the rungs 1-4 reference values from the same
   file. Also AUROC(answerable test rung 0 vs rung 5).
5. Runs the surface separability audit for rung 5 on dev and test by reusing
   `audit.surface_features()` and `audit._cv_auroc()` (5-fold, seed 13) — `audit.py` is not modified.

Writes `04_experiments/results/c1/rung5.json`. Rung 5 is exploratory: it is not part of H1, it cannot
rescue H1, and every file that reports it says so.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "04_experiments" / "src"
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(ROOT / "04_experiments" / "harness"))

import audit as audit_mod  # noqa: E402
import gate as G  # noqa: E402

DATA = ROOT / "04_experiments" / "data"
RESULTS = ROOT / "04_experiments" / "results" / "c1"
FULL = RESULTS / "results_full.json"
COEF_TOL = 1e-3
AUDIT_SEED = 13


def load_jsonl(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def main() -> None:
    t_start = time.time()
    timings: dict[str, float] = {}

    full = json.loads(FULL.read_text(encoding="utf-8"))
    items = load_jsonl(DATA / "items.jsonl")
    items5 = load_jsonl(DATA / "items_rung5.jsonl")
    feats = G.load_features()
    feats5 = G.load_features(DATA / "features_rung5.csv")

    # ---- 1. refit the frozen gate on dev rungs 0-4 and assert it reproduces -------------
    t0 = time.time()
    dev_ids = [it["item_id"] for it in items
               if it["split"] == "dev" and it["rung"] in (0, 1, 2, 3, 4)
               and it["item_id"] in feats]
    if len(dev_ids) != int(full["items"]["n_dev"]):
        raise SystemExit(f"dev id count {len(dev_ids)} != results_full n_dev {full['items']['n_dev']}")
    gate = G.fit_logistic_gate(feats, dev_ids)
    info = gate.info()
    timings["gate_refit_s"] = round(time.time() - t0, 2)

    mismatches = []
    for c in G.GATE_FEATURES:
        ref, got = float(full["gate"]["coef"][c]), float(info["coef"][c])
        if abs(ref - got) > COEF_TOL:
            mismatches.append({"feature": c, "results_full": ref, "refit": got,
                               "absdiff": abs(ref - got)})
    if abs(float(full["gate"]["intercept"]) - float(info["intercept"])) > COEF_TOL:
        mismatches.append({"feature": "__intercept__", "results_full": full["gate"]["intercept"],
                           "refit": info["intercept"],
                           "absdiff": abs(float(full["gate"]["intercept"]) - float(info["intercept"]))})
    if mismatches:
        raise SystemExit("FROZEN GATE MISMATCH — refusing to score rung 5:\n"
                         + json.dumps(mismatches, indent=2))
    coef_check = {"passed": True, "tolerance": COEF_TOL, "n_dev_ids": len(dev_ids),
                  "n_features": len(G.GATE_FEATURES),
                  "max_absdiff": max([abs(float(full["gate"]["coef"][c]) - float(info["coef"][c]))
                                      for c in G.GATE_FEATURES]
                                     + [abs(float(full["gate"]["intercept"])
                                            - float(info["intercept"]))]),
                  "coef_refit": info["coef"], "intercept_refit": info["intercept"]}

    # ---- 2. frozen thresholds (read, never refit) --------------------------------------
    band = full["thresholds"]["band"]
    band_x = full["exploratory"]["operating_point"]["band"]
    t_lo, t_hi = float(band["t_lo"]), float(band["t_hi"])
    x_lo, x_hi = float(band_x["t_lo"]), float(band_x["t_hi"])
    thresholds = {
        "confirmatory_band": {"t_lo": t_lo, "t_hi": t_hi,
                             "source": "results_full.json['thresholds']['band']",
                             "dev_precision": band["dev_precision"],
                             "dev_recall": band["dev_recall"]},
        "exploratory_band": {"t_lo": x_lo, "t_hi": x_hi,
                             "source": "results_full.json['exploratory']['operating_point']['band']",
                             "dev_precision": band_x["dev_precision"],
                             "dev_recall": band_x["dev_recall"],
                             "dev_over_refusal": band_x["dev_over_refusal"]},
        "refitted_here": False,
    }

    # ---- 3. score rung 5 ---------------------------------------------------------------
    test5_ids = [it["item_id"] for it in items5 if it["split"] == "test"]
    dev5_ids = [it["item_id"] for it in items5 if it["split"] == "dev"]
    t0 = time.time()
    s5_test = gate.score(feats5, test5_ids)
    s5_dev = gate.score(feats5, dev5_ids)
    timings["score_rung5_s"] = round(time.time() - t0, 2)

    def block(s: np.ndarray, lo: float, hi: float, name: str) -> dict:
        ref = G.refused_band(s, lo, hi)
        return {"gate": name, "n": int(ref.size),
                "abstain_precision": round(float(ref.mean()), 4),
                "ci95": G.ci_mean(ref),
                "mean_score": round(float(s.mean()), 4),
                "median_score": round(float(np.median(s)), 4)}

    rung5 = {
        "test": {"confirmatory_band": block(s5_test, t_lo, t_hi, "band_primary"),
                 "exploratory_band": block(s5_test, x_lo, x_hi, "exploratory_band")},
        "dev_reference_same_gate": {
            "confirmatory_band": block(s5_dev, t_lo, t_hi, "band_primary"),
            "exploratory_band": block(s5_dev, x_lo, x_hi, "exploratory_band")},
    }

    # reference: test rungs 1-4 from the same file
    ref_blocks = {}
    for r in ("1", "2", "3", "4"):
        c = full["test"]["band_primary"]["per_rung"][r]
        x = full["test"]["exploratory_band"]["per_rung"][r]
        ref_blocks[r] = {
            "confirmatory_band": {"abstain_precision": c["abstain_precision"], "n": c["n"],
                                  "ci95": c["ci95"],
                                  "auroc_answerable_vs_this_rung": c["auroc_answerable_vs_this_rung"]},
            "exploratory_band": {"abstain_precision": x["abstain_precision"], "n": x["n"],
                                 "ci95": x["ci95"],
                                 "auroc_answerable_vs_this_rung": x["auroc_answerable_vs_this_rung"]},
        }

    # ---- 4. AUROC(answerable rung 0 vs rung 5) -----------------------------------------
    from sklearn.metrics import roc_auc_score
    pos_ids = [it["item_id"] for it in items
               if it["split"] == "test" and it["rung"] == 0 and it["item_id"] in feats]
    s_pos = gate.score(feats, pos_ids)
    y = np.concatenate([np.ones(len(pos_ids)), np.zeros(len(test5_ids))])
    s_all = np.concatenate([s_pos, s5_test])
    auc5 = float(roc_auc_score(y, s_all))
    auroc = {"answerable_test_rung0_vs_rung5": round(auc5, 4),
             "n_answerable": len(pos_ids), "n_rung5": len(test5_ids),
             "reference_answerable_vs_rung1_4": {
                 r: ref_blocks[r]["confirmatory_band"]["auroc_answerable_vs_this_rung"]
                 for r in ("1", "2", "3", "4")}}

    # ---- 5. separability audit (reuse audit.py functions; do not modify it) ------------
    t0 = time.time()
    pos_all = [it for it in items if it["rung"] == 0]
    audit_out = {}
    for split in ("dev", "test"):
        pos = [it for it in pos_all if it["split"] == split]
        neg = [it for it in items5 if it["split"] == split]
        Xp6 = audit_mod.surface_features(pos, with_lex=False)
        Xpl = audit_mod.surface_features(pos, with_lex=True)
        Xn6 = audit_mod.surface_features(neg, with_lex=False)
        Xnl = audit_mod.surface_features(neg, with_lex=True)
        yy = np.concatenate([np.zeros(len(pos)), np.ones(len(neg))])
        a6 = audit_mod._cv_auroc(np.vstack([Xp6, Xn6]), yy, AUDIT_SEED)
        al = audit_mod._cv_auroc(np.vstack([Xpl, Xnl]), yy, AUDIT_SEED)
        audit_out[split] = {"auroc_primary_6": round(a6, 4),
                            "auroc_with_lex_overlap": round(al, 4),
                            "passes_primary_6": bool(a6 <= audit_mod.AUROC_GATE),
                            "n_answerable": len(pos), "n_negatives": len(neg),
                            "length_chars_neg_median": float(np.median([len(i["context"]) for i in neg])),
                            "length_chars_pos_median": float(np.median([len(i["context"]) for i in pos]))}
    timings["audit_s"] = round(time.time() - t0, 2)
    audit_ref = {r: {"dev_auroc_primary_6": full["audit"]["dev_auroc_primary"][r],
                     "dev_auroc_with_lex_overlap":
                         full["audit"]["dev_auroc_sensitivity_with_lex"][r],
                     "test_auroc_primary_6": full["audit"]["test_reference_primary"][r]}
                 for r in ("1", "2", "3", "4")}

    # ---- 6. matching diagnostic: did the overlap match actually work? ------------------
    import re as _re

    def _ov(q: str, p: str) -> float:
        qs = set(_re.findall(r"[a-z0-9]+", q.lower()))
        ps = set(_re.findall(r"[a-z0-9]+", p.lower()))
        return len(qs & ps) / max(1, len(qs))

    gold_of = {(it["split"], it["qid"]): it["context"] for it in items if it["rung"] == 0}
    r1_ctx = {(it["split"], it["qid"]): it["context"] for it in items if it["rung"] == 1}
    diag = {}
    for split in ("dev", "test"):
        tgt, chosen, r1diff = [], [], []
        for it in items5:
            if it["split"] != split:
                continue
            key = (split, it["qid"])
            tgt.append(it["overlap_target"])
            chosen.append(it["overlap_chosen"])
            if key in r1_ctx:  # contrast: how far a random (rung-1) negative sits from the target
                r1diff.append(abs(_ov(it["question"], r1_ctx[key]) - it["overlap_target"]))
        ad = [abs(a - b) for a, b in zip(chosen, tgt)]
        diag[split] = {
            "mean_overlap_target": round(float(np.mean(tgt)), 4),
            "mean_overlap_chosen": round(float(np.mean(chosen)), 4),
            "mean_overlap_absdiff": round(float(np.mean(ad)), 4),
            "median_overlap_absdiff": round(float(np.median(ad)), 4),
            "max_overlap_absdiff": round(float(np.max(ad)), 4),
            "contrast_rung1_random_negative_mean_overlap_absdiff":
                round(float(np.mean(r1diff)), 4) if r1diff else None,
            "contrast_n": len(r1diff),
        }

    out = {
        "label": "EXPLORATORY (D2)",
        "experiment": "c1",
        "preregistration_section": "§10 D2",
        "note": ("Rung 5 = overlap-matched negatives. Exploratory: not part of H1, cannot rescue H1, "
                 "never described as confirmatory. The gate and both thresholds are frozen from "
                 "results_full.json and were not refitted for this rung."),
        "frozen_gate_assertion": coef_check,
        "thresholds": thresholds,
        "items": {"n_rung5_dev": len(dev5_ids), "n_rung5_test": len(test5_ids),
                  "n_answerable_test": len(pos_ids),
                  "rung5_sha256": __import__("hashlib").sha256(
                      (DATA / "items_rung5.jsonl").read_bytes()).hexdigest(),
                  "features_rung5_sha256": __import__("hashlib").sha256(
                      (DATA / "features_rung5.csv").read_bytes()).hexdigest()},
        "rung5_test": rung5["test"],
        "rung5_dev_reference": rung5["dev_reference_same_gate"],
        "reference_test_rungs_1_4": ref_blocks,
        "auroc": auroc,
        "separability_audit": {"rung5": audit_out, "reference_rungs_1_4": audit_ref,
                               "cv": {"folds": 5, "seed": AUDIT_SEED},
                               "gate_auroc": audit_mod.AUROC_GATE},
        "matching_diagnostic": diag,
        "timings_s": {**timings, "total_s": round(time.time() - t_start, 2)},
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "rung5.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n",
                                        encoding="utf-8")

    print(json.dumps({
        "label": out["label"],
        "frozen_gate_assertion_passed": coef_check["passed"],
        "max_coef_absdiff": coef_check["max_absdiff"],
        "rung5_test_confirmatory": rung5["test"]["confirmatory_band"],
        "rung5_test_exploratory": rung5["test"]["exploratory_band"],
        "auroc_r0_vs_r5": auroc["answerable_test_rung0_vs_rung5"],
        "audit_rung5": audit_out,
        "matching": diag,
        "timings_s": out["timings_s"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
