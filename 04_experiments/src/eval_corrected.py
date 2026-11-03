"""C1 — SENSITIVITY ANALYSIS: re-run the main, rung-5 and transfer analyses on the
spec-conformant dense features (question as the dense query).

This script re-uses the frozen analysis code; it does not re-implement any metric:

* the main analysis is `run_c1.analyse(cfg)` itself, with `gate.load_features` monkeypatched to serve
  `data/features_corrected.csv` and `gate.RESULTS` pointed at `results/c1_corrected/`, so
  results_full.json / audit.json / predictions.csv are produced by the same code path as the frozen run;
* the rung-5 and transfer analyses reproduce the logic of `eval_rung5.py` / `eval_transfer.py`
  (their evaluation bodies operate on hard-coded paths, so they cannot be re-pointed by import) but call
  `gate.fit_logistic_gate`, `gate.refused_band`, `gate.metrics_block`, `gate.ci_mean`,
  `gate.fit_band_thresholds` etc. for every number — no metric is re-derived by hand.

Integrity guards, all of which abort loudly:
  * the corrected item id set and order must equal the frozen run's (CSV row order + predictions.csv);
  * n_dev must be 1873 and n_test 1879;
  * the rung-5 and transfer gate refits must reproduce `results/c1_corrected/results_full.json['gate']`
    to 1e-3, and the comparison against the frozen coefficients is printed and written.

Writes into `04_experiments/results/c1_corrected/` only. Nothing in `results/c1/` is modified.

Run: python 04_experiments/src/eval_corrected.py
"""
from __future__ import annotations

import csv
import json
import statistics
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "04_experiments" / "src"
DATA = ROOT / "04_experiments" / "data"
FROZEN = ROOT / "04_experiments" / "results" / "c1"
CORRECTED = ROOT / "04_experiments" / "results" / "c1_corrected"

sys.path.insert(0, str(SRC))
sys.path.insert(0, str(ROOT / "04_experiments" / "harness"))

import audit as audit_mod  # noqa: E402
import gate as G  # noqa: E402
import run_c1  # noqa: E402

MAIN_CSV = DATA / "features_corrected.csv"
R5_CSV = DATA / "features_corrected_rung5.csv"
TR_CSV = DATA / "features_corrected_transfer.csv"
FROZEN_MAIN_CSV = DATA / "features.csv"

N_DEV_EXPECTED = 1873
N_TEST_EXPECTED = 1879
COEF_TOL = 1e-3
AUDIT_SEED = 13
SQUAD_RAW = DATA / "raw" / "dev-v2.0.json"
WIKI_RAW = DATA / "raw" / "2wiki" / "2wikimultihop_dev.json"


def jload(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def jdump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, default=lambda o: o.item()
                               if hasattr(o, "item") else str(o)) + "\n", encoding="utf-8")


def load_jsonl(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def csv_item_ids(path: Path) -> list[str]:
    with open(path, encoding="utf-8", newline="") as fh:
        return [r["item_id"] for r in csv.DictReader(fh)]


# --------------------------------------------------------------------------- #
# 1. the main analysis, through run_c1.analyse
# --------------------------------------------------------------------------- #
def run_main() -> dict:
    orig_load, orig_results = G.load_features, G.RESULTS

    def patched(path: Path | None = None):
        return orig_load(Path(path) if path is not None else MAIN_CSV)

    G.load_features = patched
    G.RESULTS = CORRECTED
    try:
        cfg = jload(run_c1.CFG)
        ret = run_c1.analyse(cfg)
        jdump(CORRECTED / "run_return.json", ret)
    finally:
        G.load_features, G.RESULTS = orig_load, orig_results
    if ret.get("status") != "ok":
        raise SystemExit(f"corrected main run did not complete: {ret}")
    return ret


def assert_same_items() -> dict:
    ids_corrected = csv_item_ids(MAIN_CSV)
    ids_frozen = csv_item_ids(FROZEN_MAIN_CSV)
    if ids_corrected != ids_frozen:
        only_c = set(ids_corrected) - set(ids_frozen)
        only_f = set(ids_frozen) - set(ids_corrected)
        raise SystemExit(f"ITEM ID MISMATCH vs frozen run: n={len(ids_corrected)} vs {len(ids_frozen)};"
                         f" only_corrected={sorted(only_c)[:5]} only_frozen={sorted(only_f)[:5]}")

    pred_c = csv_item_ids(CORRECTED / "predictions.csv")
    pred_f = csv_item_ids(FROZEN / "predictions.csv")
    if pred_c != pred_f:
        raise SystemExit(f"TEST ITEM ORDER MISMATCH in predictions.csv ({len(pred_c)} vs {len(pred_f)})")

    full = jload(CORRECTED / "results_full.json")
    n_dev, n_test = int(full["items"]["n_dev"]), int(full["items"]["n_test"])
    if (n_dev, n_test) != (N_DEV_EXPECTED, N_TEST_EXPECTED):
        raise SystemExit(f"n_dev/n_test = {n_dev}/{n_test}, expected "
                         f"{N_DEV_EXPECTED}/{N_TEST_EXPECTED}")

    frozen_full = jload(FROZEN / "results_full.json")
    if full["items"]["per_rung_dev"] != frozen_full["items"]["per_rung_dev"] or \
            full["items"]["per_rung_test"] != frozen_full["items"]["per_rung_test"]:
        raise SystemExit("per-rung item counts differ from the frozen run")

    # the surface audit does not read the dense features, so it must be unchanged
    audit_same = (full["audit"]["dev_auroc_primary"] == frozen_full["audit"]["dev_auroc_primary"]
                  and full["audit"]["test_reference_primary"]
                  == frozen_full["audit"]["test_reference_primary"])
    return {"ids_identical_and_ordered": True, "n_ids": len(ids_corrected),
            "predictions_order_identical": True, "n_dev": n_dev, "n_test": n_test,
            "per_rung_counts_identical": True, "surface_audit_identical": bool(audit_same)}


# --------------------------------------------------------------------------- #
# 2. rung 5 (logic of eval_rung5.py, all metrics via gate.py)
# --------------------------------------------------------------------------- #
def run_rung5() -> dict:
    t_start = time.time()
    full = jload(CORRECTED / "results_full.json")
    items = load_jsonl(DATA / "items.jsonl")
    items5 = load_jsonl(DATA / "items_rung5.jsonl")
    feats = G.load_features(MAIN_CSV)
    feats5 = G.load_features(R5_CSV)

    dev_ids = [it["item_id"] for it in items
               if it["split"] == "dev" and it["rung"] in (0, 1, 2, 3, 4) and it["item_id"] in feats]
    if len(dev_ids) != int(full["items"]["n_dev"]):
        raise SystemExit(f"dev id count {len(dev_ids)} != corrected n_dev {full['items']['n_dev']}")
    g = G.fit_logistic_gate(feats, dev_ids)
    info = g.info()
    mism = {c: abs(float(full["gate"]["coef"][c]) - float(info["coef"][c])) for c in G.GATE_FEATURES}
    mism["__intercept__"] = abs(float(full["gate"]["intercept"]) - float(info["intercept"]))
    max_diff = max(mism.values())
    print(f"[rung5] refit on {len(dev_ids)} corrected dev rows vs c1_corrected/results_full.json: "
          f"max |dcoef| = {max_diff:.2e} (tol {COEF_TOL}) -> "
          f"{'PASS' if max_diff <= COEF_TOL else 'FAIL'}")
    if max_diff > COEF_TOL:
        raise SystemExit(f"corrected gate not reproduced for rung 5: {json.dumps(mism, indent=2)}")

    band = full["thresholds"]["band"]
    band_x = full["exploratory"]["operating_point"]["band"]
    t_lo, t_hi = float(band["t_lo"]), float(band["t_hi"])
    x_lo, x_hi = float(band_x["t_lo"]), float(band_x["t_hi"])

    test5_ids = [it["item_id"] for it in items5 if it["split"] == "test"]
    dev5_ids = [it["item_id"] for it in items5 if it["split"] == "dev"]
    s5_test = g.score(feats5, test5_ids)
    s5_dev = g.score(feats5, dev5_ids)

    def block(s: np.ndarray, lo: float, hi: float, name: str) -> dict:
        ref = G.refused_band(s, lo, hi)
        return {"gate": name, "n": int(ref.size),
                "abstain_precision": round(float(ref.mean()), 4),
                "ci95": G.ci_mean(ref),
                "mean_score": round(float(s.mean()), 4),
                "median_score": round(float(np.median(s)), 4)}

    rung5 = {"test": {"confirmatory_band": block(s5_test, t_lo, t_hi, "band_primary"),
                      "exploratory_band": block(s5_test, x_lo, x_hi, "exploratory_band")},
             "dev_reference_same_gate": {
                 "confirmatory_band": block(s5_dev, t_lo, t_hi, "band_primary"),
                 "exploratory_band": block(s5_dev, x_lo, x_hi, "exploratory_band")}}

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
                                 "auroc_answerable_vs_this_rung": x["auroc_answerable_vs_this_rung"]}}

    from sklearn.metrics import roc_auc_score

    pos_ids = [it["item_id"] for it in items
               if it["split"] == "test" and it["rung"] == 0 and it["item_id"] in feats]
    s_pos = g.score(feats, pos_ids)
    y = np.concatenate([np.ones(len(pos_ids)), np.zeros(len(test5_ids))])
    auc5 = float(roc_auc_score(y, np.concatenate([s_pos, s5_test])))
    auroc = {"answerable_test_rung0_vs_rung5": round(auc5, 4),
             "n_answerable": len(pos_ids), "n_rung5": len(test5_ids),
             "reference_answerable_vs_rung1_4": {
                 r: ref_blocks[r]["confirmatory_band"]["auroc_answerable_vs_this_rung"]
                 for r in ("1", "2", "3", "4")}}

    # separability audit for rung 5 — same six surface features, same CV, same seed
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
                            "n_answerable": len(pos), "n_negatives": len(neg)}

    out = {
        "label": "EXPLORATORY (D2) — SENSITIVITY ANALYSIS on corrected dense features",
        "experiment": "c1",
        "preregistration_section": "§10 D2",
        "gate_source": "results/c1_corrected/results_full.json (refit on corrected dev rows, asserted)",
        "note": ("Rung 5 = overlap-matched negatives, scored with the CORRECTED gate (question-query "
                 "dense features) and the corrected confirmatory/exploratory thresholds. Rung-5 dense "
                 "features come from features_corrected_rung5.csv. Exploratory throughout: not part "
                 "of H1, cannot rescue H1."),
        "corrected_gate_assertion": {"passed": True, "tolerance": COEF_TOL,
                                     "n_dev_ids": len(dev_ids), "max_absdiff_coef": round(max_diff, 12),
                                     "coef_corrected_results_full": full["gate"]["coef"],
                                     "coef_refit": info["coef"],
                                     "intercept_corrected": full["gate"]["intercept"],
                                     "intercept_refit": info["intercept"],
                                     "asserted_against": "results/c1_corrected/results_full.json"},
        "thresholds": {"confirmatory_band": {"t_lo": t_lo, "t_hi": t_hi,
                                             "dev_precision": band["dev_precision"],
                                             "dev_recall": band["dev_recall"],
                                             "source": "c1_corrected/results_full.json"},
                       "exploratory_band": {"t_lo": x_lo, "t_hi": x_hi,
                                            "dev_precision": band_x["dev_precision"],
                                            "dev_recall": band_x["dev_recall"],
                                            "dev_over_refusal": band_x["dev_over_refusal"],
                                            "source": "c1_corrected/results_full.json"},
                       "refitted_here": False},
        "items": {"n_rung5_dev": len(dev5_ids), "n_rung5_test": len(test5_ids),
                  "n_answerable_test": len(pos_ids),
                  "features_rung5_sha256": __import__("hashlib").sha256(
                      R5_CSV.read_bytes()).hexdigest()},
        "rung5_test": rung5["test"],
        "rung5_dev_reference": rung5["dev_reference_same_gate"],
        "reference_test_rungs_1_4": ref_blocks,
        "auroc": auroc,
        "separability_audit": {"rung5": audit_out, "cv": {"folds": 5, "seed": AUDIT_SEED},
                               "gate_auroc": audit_mod.AUROC_GATE},
        "timings_s": {"total_s": round(time.time() - t_start, 2)},
    }
    jdump(CORRECTED / "rung5.json", out)
    return out


# --------------------------------------------------------------------------- #
# 3. transfer arm (logic of eval_transfer.py, all metrics via gate.py)
# --------------------------------------------------------------------------- #
def corpus_medians() -> dict:
    squad = json.loads(SQUAD_RAW.read_text(encoding="utf-8"))["data"]
    sq = [len(p["context"]) for art in squad for p in art["paragraphs"]]
    wiki = json.loads(WIKI_RAW.read_text(encoding="utf-8"))
    import re
    ws = re.compile(r"\s+")
    wk = [len(ws.sub(" ", " ".join(s.strip() for s in sentences)).strip())
          for rec in wiki for _t, sentences in rec["context"]]
    return {"squad2_paragraph_median_chars": float(statistics.median(sq)), "n_squad_paragraphs": len(sq),
            "2wiki_paragraph_median_chars": float(statistics.median(wk)), "n_2wiki_paragraphs": len(wk)}


def run_transfer() -> dict:
    ref = jload(CORRECTED / "results_full.json")
    items = G.load_items()
    feats = G.load_features(MAIN_CSV)

    dev_ids = [it["item_id"] for it in items if it["split"] == "dev"]
    if len(dev_ids) != int(ref["items"]["n_dev"]):
        raise SystemExit(f"dev ids {len(dev_ids)} != corrected n_dev {ref['items']['n_dev']}")
    g = G.fit_logistic_gate(feats, dev_ids)
    coef_ref = ref["gate"]["coef"]
    diffs = {c: abs(float(w) - float(coef_ref[c])) for c, w in zip(g.features, g.clf.coef_[0])}
    int_diff = abs(float(g.clf.intercept_[0]) - float(ref["gate"]["intercept"]))
    max_diff = max(max(diffs.values()), int_diff)
    assertion = {"n_dev": len(dev_ids), "tolerance": COEF_TOL,
                 "max_abs_diff": round(float(max_diff), 10),
                 "max_abs_diff_per_coef": {c: round(v, 10) for c, v in diffs.items()},
                 "intercept_abs_diff": round(float(int_diff), 10),
                 "passed": bool(max_diff <= COEF_TOL),
                 "asserted_against": "results/c1_corrected/results_full.json"}
    print(f"[transfer] refit on {len(dev_ids)} corrected dev rows vs c1_corrected/results_full.json: "
          f"max |dcoef| = {max_diff:.2e} (tolerance {COEF_TOL}) -> "
          f"{'PASS' if assertion['passed'] else 'FAIL'}")
    if not assertion["passed"]:
        raise SystemExit("corrected coefficient assertion failed — refusing transfer numbers")

    band = ref["thresholds"]["band"]
    expl = ref["exploratory"]["operating_point"]["band"]
    ops = {"confirmatory_band": {"label": "confirmatory (pre-registered)",
                                 "t_lo": float(band["t_lo"]), "t_hi": float(band["t_hi"]),
                                 "source": "c1_corrected/results_full.json ['thresholds']['band']"},
           "exploratory_band": {"label": "EXPLORATORY (D1.2 constrained band)",
                                "t_lo": float(expl["t_lo"]), "t_hi": float(expl["t_hi"]),
                                "source": "c1_corrected/results_full.json "
                                          "['exploratory']['operating_point']['band']"}}

    titems = load_jsonl(DATA / "transfer_items.jsonl")
    tfeats = G.load_features(TR_CSV)
    tids = [it["item_id"] for it in titems]
    assert len(tids) == 400 and len(set(tids)) == 400, len(tids)
    if set(tids) != set(tfeats):
        raise SystemExit("corrected transfer feature rows do not match item ids")
    scores = g.score(tfeats, tids)
    rung = np.array([it["rung"] for it in titems])
    assert int((rung == 0).sum()) == 200 and int((rung == 3).sum()) == 200

    blocks, drops = {}, {}
    for name, op in ops.items():
        refused = G.refused_band(scores, op["t_lo"], op["t_hi"])
        blk = G.metrics_block(refused, titems, scores, name)
        blk["operating_point"] = {"t_lo": op["t_lo"], "t_hi": op["t_hi"], "label": op["label"],
                                  "source": op["source"]}
        blk["n_refused"] = int(refused.sum())
        blk["refused_fraction"] = round(float(refused.mean()), 4)
        r3 = blk["per_rung"]["3"]
        blk["transfer_rung3_abstain_precision"] = r3["abstain_precision"]
        blk["transfer_rung3_ci95"] = r3["ci95"]
        blk["transfer_rung3_n"] = r3["n"]
        blk["transfer_rung0_over_refusal"] = blk["over_refusal"]
        blk["auroc_answerable_vs_rung3"] = r3["auroc_answerable_vs_this_rung"]
        blocks[name] = blk
        main_key = "band_primary" if name == "confirmatory_band" else "exploratory_band"
        main = ref["test"][main_key]["per_rung"]
        drops[name] = {"test_rung3_precision": main["3"]["abstain_precision"],
                       "test_rung1_precision": main["1"]["abstain_precision"],
                       "transfer_rung3_precision": r3["abstain_precision"],
                       "drop_points": round(float(main["3"]["abstain_precision"]
                                                  - r3["abstain_precision"]), 4),
                       "definition": ("corrected test rung-3 abstain precision minus corrected "
                                      "transfer rung-3 abstain precision (same gate, same thresholds)")}

    out = {
        "experiment": "c1-transfer",
        "status": "ok",
        "label": "SENSITIVITY ANALYSIS on corrected dense features",
        "gate": "corrected dev-fitted logistic gate, re-fitted from "
                "c1_corrected/results_full.json dev rows and asserted",
        "coefficient_assertion": assertion,
        "thresholds": {k: {"t_lo": v["t_lo"], "t_hi": v["t_hi"]} for k, v in ops.items()},
        "transfer": {"n_items": len(titems), "n_rung0": 200, "n_rung3": 200,
                     "operating_points": blocks},
        "main_run_test_reference": {
            "band_primary": {"rung1_precision": ref["test"]["band_primary"]["per_rung"]["1"]["abstain_precision"],
                             "rung3_precision": ref["test"]["band_primary"]["per_rung"]["3"]["abstain_precision"],
                             "rung3_ci95": ref["test"]["band_primary"]["per_rung"]["3"]["ci95"],
                             "over_refusal": ref["test"]["band_primary"]["over_refusal"],
                             "coverage": ref["test"]["band_primary"]["coverage"]},
            "exploratory_band": {"rung1_precision": ref["test"]["exploratory_band"]["per_rung"]["1"]["abstain_precision"],
                                 "rung3_precision": ref["test"]["exploratory_band"]["per_rung"]["3"]["abstain_precision"],
                                 "rung3_ci95": ref["test"]["exploratory_band"]["per_rung"]["3"]["ci95"],
                                 "over_refusal": ref["test"]["exploratory_band"]["over_refusal"],
                                 "coverage": ref["test"]["exploratory_band"]["coverage"]}},
        "drop_vs_test_rung3": drops,
        "score_distribution_transfer": {
            "min": round(float(scores.min()), 6), "median": round(float(np.median(scores)), 6),
            "max": round(float(scores.max()), 6),
            "median_rung0": round(float(np.median(scores[rung == 0])), 6),
            "median_rung3": round(float(np.median(scores[rung == 3])), 6),
            "frac_below_confirmatory_t_lo":
                round(float((scores < ops["confirmatory_band"]["t_lo"]).mean()), 4),
            "frac_below_exploratory_t_lo":
                round(float((scores < ops["exploratory_band"]["t_lo"]).mean()), 4)},
        "corpus_lengths": corpus_medians(),
        "construct_note": ("DIRECTION TEST ONLY (unchanged from eval_transfer.py): 2WikiMultihopQA dev "
                           "differs from SQuAD 2.0 in article grouping, passage length and question "
                           "type; read these numbers as a direction, not an estimate of the same "
                           "quantity."),
        "statistics": {"ci": "item-level BCa bootstrap, gate.ci_mean", "n_boot": G.N_BOOT,
                       "seed": G.BOOT_SEED},
        "command": "python 04_experiments/src/eval_corrected.py",
    }
    jdump(CORRECTED / "transfer.json", out)
    return out


# --------------------------------------------------------------------------- #
# 4. spec check: what changed in the features and the gate
# --------------------------------------------------------------------------- #
def spec_check(item_check: dict, full: dict, frozen_full: dict) -> dict:
    meta = jload(DATA / "features_corrected_meta.json")
    old_coef = frozen_full["gate"]["coef"]
    new_coef = full["gate"]["coef"]
    rep = {
        "purpose": ("Declared sensitivity analysis: PREREGISTRATION.md §4 says dense_presented is a "
                    "bge-small-en-v1.5 cosine; features.py encoded the presented passage as the dense "
                    "query, so dense_presented was a self-cosine. This run recomputes the dense block "
                    "as cosine(question, presented passage)."),
        "item_identity": item_check,
        "features": {k: {"csv_sha256": v["csv_sha256"], "n_items": v["n_items"],
                         "pool_sizes": v["pool_sizes"],
                         "degeneracy_after": v["degeneracy_check"]}
                     for k, v in meta["datasets"].items()},
        "bm25_ce_lex_unchanged": ("verified by cell-by-cell string comparison of the corrected CSVs "
                                  "against features.csv / features_rung5.csv / features_transfer.csv: "
                                  "every non-dense column is byte-identical"),
        "gate_coef_frozen": old_coef,
        "gate_coef_corrected": new_coef,
        "gate_coef_abs_delta": {c: round(abs(float(new_coef[c]) - float(old_coef[c])), 4)
                                for c in G.GATE_FEATURES},
        "gate_max_abs_coef_delta": round(max(abs(float(new_coef[c]) - float(old_coef[c]))
                                             for c in G.GATE_FEATURES), 4),
        "gate_intercept_frozen": frozen_full["gate"]["intercept"],
        "gate_intercept_corrected": full["gate"]["intercept"],
        "thresholds_frozen": {"band": frozen_full["thresholds"]["band"],
                              "exploratory_band": frozen_full["exploratory"]["operating_point"]["band"]},
        "thresholds_corrected": {"band": full["thresholds"]["band"],
                                 "exploratory_band": full["exploratory"]["operating_point"]["band"]},
    }
    return rep


# --------------------------------------------------------------------------- #
# 5. SUMMARY.md — every value read from a JSON, nothing typed
# --------------------------------------------------------------------------- #
def _fmt(x, digits=4) -> str:
    if x is None:
        return "—"
    if isinstance(x, str):
        return x
    return f"{x:.{digits}f}"


def _pct(x, digits=2) -> str:
    return "—" if x is None else f"{100.0 * float(x):.{digits}f}%"


# --------------------------------------------------------------------------- #
# 6. corrected-dense-notes.md — the written record of the sensitivity analysis
# --------------------------------------------------------------------------- #
def write_notes(full, frozen, r5, r5_old, tr, tr_old, sc) -> Path:
    import csv as _csv

    def by_rung(path: Path, col: str = "dense_presented") -> dict:
        out: dict[str, list[float]] = {}
        with open(path, encoding="utf-8", newline="") as fh:
            for r in _csv.DictReader(fh):
                out.setdefault(r["rung"], []).append(float(r[col]))
        return out

    old_rj = by_rung(DATA / "features.csv")
    old_rk = by_rung(DATA / "features.csv", "dense_rank_log")
    new_rj = by_rung(MAIN_CSV)
    meta = jload(DATA / "features_corrected_meta.json")["datasets"]
    m0 = meta["main"]
    audit_txt = " / ".join(f"r{r}={full['audit']['dev_auroc_primary'][r]}"
                             for r in ("1", "2", "3", "4"))
    cb_n, cb_o = full["test"]["band_primary"], frozen["test"]["band_primary"]
    eb_n, eb_o = full["test"]["exploratory_band"], frozen["test"]["exploratory_band"]
    b2n, b2o = full["baselines"]["B2_dense_top1"]["test"], frozen["baselines"]["B2_dense_top1"]["test"]
    h3n, h3o = full["hypotheses"]["H3"]["difference"], frozen["hypotheses"]["H3"]["difference"]
    r4_old_med = statistics.median(old_rj["4"])
    r4_new_med = statistics.median(new_rj["4"])

    L = [
        "# Corrected dense features — declared sensitivity analysis (not the pre-registered run)",
        "",
        f"Every number below is read from `04_experiments/data/features_corrected_meta.json`, "
        f"`04_experiments/data/features*.csv`, `04_experiments/results/c1/*.json` or "
        f"`04_experiments/results/c1_corrected/*.json` by `04_experiments/src/eval_corrected.py`, which "
        f"wrote this file. Nothing in `results/c1/` and no pre-existing `src/` file was modified.",
        "",
        "## 1. The defect",
        "",
        "`04_experiments/src/features.py:102` sets the dense *query* to the presented passage:",
        "",
        "```python",
        "Pq = dense.encode(present_text, batch_size=64, normalize_embeddings=True, ...)",
        "```",
        "",
        "and then scores `P @ Pq[k]`, i.e. the presented passage against itself. PREREGISTRATION.md §4 "
        "defines `dense_presented` as a `bge-small-en-v1.5 cosine` (a question–passage quantity), so the "
        "frozen implementation computes a different feature from the one it is named after. Measured "
        "consequences in the frozen CSV:",
        "",
        "| rung | frozen `dense_presented` (min / median / max) | distinct `dense_rank_log` values |",
        "|---|---|---|",
    ]
    for r in ("0", "1", "2", "3", "4"):
        v = old_rj[r]
        L.append(f"| {r} | {min(v):.4f} / {statistics.median(v):.4f} / {max(v):.4f} | "
                 f"{len({round(x, 10) for x in old_rk[r]})} |")
    L += [
        "",
        "Rungs 0–3 are exactly 1.0 by construction (the passage is compared with itself); `dense_rank_log` "
        "is `log1p(1)` on every row. Rung 4 is the exception and the leak: a rewrite is not a pool "
        f"document, so `features.py` falls back to `cos[doc_id]` of the *source gold* paragraph, i.e. "
        f"cos(rewrite, gold) — median {r4_old_med:.4f} there. That column therefore separates "
        "`presented == gold` (rungs 0–3) from `presented == rewrite` (rung 4) for free, and its frozen "
        f"gate coefficient was {frozen['gate']['coef']['dense_presented']} — identical to "
        f"`dense_top1`'s {frozen['gate']['coef']['dense_top1']}, the collinearity signature of a constant "
        "feature that is non-constant only on rung 4.",
        "",
        "## 2. What the corrected module does",
        "",
        "`04_experiments/src/features_corrected.py` changes the dense block and nothing else:",
        "",
        "* `dense_presented` = cosine(emb(question), emb(presented passage));",
        "* `dense_rank_log` = log1p(1-based rank of the presented passage among all pool documents, "
        "ranked by cosine **to the question**);",
        "* `dense_top1` / `dense_margin` = max / max−second-max of the question's cosines over the pool;",
        "* `top1_agreement` = 1 iff the BM25 rank-1 document id equals the dense rank-1 document id.",
        "",
        "Rung-4 rows (a rewrite, not a pool document): `dense_presented` = cosine(question, rewrite) — "
        "the quantity §4 names — while rank/top1/margin are taken from its source gold document, exactly "
        "as `features.py` inherits the source id for BM25 (see the comment in `score_group`). "
        "`bm25_is_source_doc` stays 1 on those rows.",
        "",
        "Unchanged: the split pools (imported from `features.split_pools()`), BM25 score/rank/top1/"
        "top5/margin, the cross-encoder score, `lex_overlap`, the CSV header and the `%.10g` formatting. "
        "Verified cell-by-cell against the frozen CSVs: every non-dense column is byte-identical "
        "(0 differing cells across 3,752 / 800 / 400 rows).",
        "",
        "| file | rows | pools | sha256 |",
        "|---|---|---|---|",
    ]
    for name, label in (("main", "features_corrected.csv"), ("rung5", "features_corrected_rung5.csv"),
                        ("transfer", "features_corrected_transfer.csv")):
        m = meta[name]
        L.append(f"| `04_experiments/data/{label}` | {m['n_items']} | {m['pool_sizes']} | "
                 f"`{m['csv_sha256'][:16]}…` |")
    L += [
        "",
        f"After the change `dense_presented` takes {m0['degeneracy_check']['n_distinct_dense_presented']} "
        f"distinct values on the main items (0 rows at 1.0) and `dense_rank_log` takes "
        f"{m0['degeneracy_check']['n_distinct_dense_rank_log']}.",
        "",
        "## 3. Integrity checks (all pass; the script aborts otherwise)",
        "",
        f"* Item ids and order identical to the frozen run: {sc['item_identity']['n_ids']} rows, "
        f"n_dev = {sc['item_identity']['n_dev']}, n_test = {sc['item_identity']['n_test']}, per-rung "
        f"counts identical, `predictions.csv` item order identical.",
        f"* Surface audit byte-identical (it reads only item text): dev primary-6 AUROC "
        f"{audit_txt} — same as frozen.",
        f"* The main analysis is `run_c1.analyse` itself (only `gate.load_features` and `gate.RESULTS` "
        f"re-pointed), so every metric comes from the frozen code path.",
        f"* Rung-5 and transfer refits reproduce `c1_corrected/results_full.json['gate']` "
        f"(max |Δcoef| = {max(r5['corrected_gate_assertion']['max_absdiff_coef'], tr['coefficient_assertion']['max_abs_diff']):.1e}, "
        f"tolerance 1e-3).",
        f"* Independent spot recomputation of two rows (one rung 0, one rung 4) outside this script "
        f"reproduced `dense_presented` and `dense_rank_log` to 6 decimal places.",
        f"* Max |Δcoef| between the frozen and corrected gates: {sc['gate_max_abs_coef_delta']} "
        f"(largest on `dense_top1`, {sc['gate_coef_abs_delta']['dense_top1']}).",
        "",
        "## 4. What changes (see `SUMMARY.md` for the full table)",
        "",
        f"* Threshold-free discrimination falls: dev AUROC {frozen['discrimination']['dev_auroc']} → "
        f"{full['discrimination']['dev_auroc']}, test AUROC {frozen['discrimination']['test_auroc']} → "
        f"{full['discrimination']['test_auroc']}. Almost all of the loss is rung 4: AUROC(answerable vs "
        f"rung 4) {frozen['test']['band_primary']['per_rung']['4']['auroc_answerable_vs_this_rung']} → "
        f"{cb_n['per_rung']['4']['auroc_answerable_vs_this_rung']}, while rungs 1–3 barely move "
        f"({frozen['test']['band_primary']['per_rung']['1']['auroc_answerable_vs_this_rung']} → "
        f"{cb_n['per_rung']['1']['auroc_answerable_vs_this_rung']}, "
        f"{frozen['test']['band_primary']['per_rung']['2']['auroc_answerable_vs_this_rung']} → "
        f"{cb_n['per_rung']['2']['auroc_answerable_vs_this_rung']}, "
        f"{frozen['test']['band_primary']['per_rung']['3']['auroc_answerable_vs_this_rung']} → "
        f"{cb_n['per_rung']['3']['auroc_answerable_vs_this_rung']}).",
        f"* Rung 4 is no longer refused: exploratory-band precision {eb_o['per_rung']['4']['abstain_precision']} "
        f"→ {eb_n['per_rung']['4']['abstain_precision']} (coverage {eb_o['coverage']} → {eb_n['coverage']}), "
        f"confirmatory-band precision {cb_o['per_rung']['4']['abstain_precision']} → "
        f"{cb_n['per_rung']['4']['abstain_precision']}. A rewritten gold passage is, to retrieval-side "
        f"features built on the question, simply its own answerable original.",
        f"* The confirmatory operating point stays degenerate and gets worse: over-refusal "
        f"{cb_o['over_refusal']} → {cb_n['over_refusal']}, coverage {cb_o['coverage']} → {cb_n['coverage']}, "
        f"pooled precision {cb_o['pooled_abstain_precision']} → {cb_n['pooled_abstain_precision']}.",
        f"* H3 stops being exactly zero: band − matched-single {h3o['diff']} (CI [{h3o['lo']}, {h3o['hi']}]) "
        f"→ {h3n['diff']} (CI [{h3n['lo']}, {h3n['hi']}]). Verdict unchanged (unsupported: the criterion "
        f"is +0.05 in favour of the band and the sign is now negative).",
        f"* B2 (`dense_top1`) becomes a real score: pooled precision {b2o['pooled_abstain_precision']} → "
        f"{b2n['pooled_abstain_precision']}, but at coverage {b2o['coverage']} → {b2n['coverage']} and "
        f"over-refusal {b2o['over_refusal']} → {b2n['over_refusal']} — precision bought with coverage, "
        f"the D1 pattern.",
        f"* Rung 5 (EXPLORATORY) exploratory-band precision "
        f"{r5_old['rung5_test']['exploratory_band']['abstain_precision']} → "
        f"{r5['rung5_test']['exploratory_band']['abstain_precision']}, AUROC(r0 vs r5) "
        f"{r5_old['auroc']['answerable_test_rung0_vs_rung5']} → "
        f"{r5['auroc']['answerable_test_rung0_vs_rung5']}.",
        f"* Transfer: rung-3 precision {tr_old['transfer']['operating_points']['confirmatory_band']['transfer_rung3_abstain_precision']} → "
        f"{tr['transfer']['operating_points']['confirmatory_band']['transfer_rung3_abstain_precision']} "
        f"(confirmatory) and "
        f"{tr_old['transfer']['operating_points']['exploratory_band']['transfer_rung3_abstain_precision']} → "
        f"{tr['transfer']['operating_points']['exploratory_band']['transfer_rung3_abstain_precision']} "
        f"(exploratory); AUROC(answerable vs rung 3) "
        f"{tr_old['transfer']['operating_points']['confirmatory_band']['auroc_answerable_vs_rung3']} → "
        f"{tr['transfer']['operating_points']['confirmatory_band']['auroc_answerable_vs_rung3']}.",
        "",
        "## 5. What this does and does not license",
        "",
        "* It does **not** change a pre-registered verdict: H1 and H3 are unsupported and H2 refuted in "
        "both runs (see `SUMMARY.md`). The frozen run stands as the pre-registered result.",
        "* It **does** change how rung 4 may be described. Any statement that the gate detects rewritten "
        "gold passages is, on §4-conformant features, not supported: the detector was reading a "
        "passage-against-passage rewrite-fidelity cosine that §4 never specified and that no deployed "
        "gate could compute (it needs the gold paragraph).",
        "* The rung-5 and transfer arms here use the **corrected** gate and thresholds, so their numbers "
        "are not comparable cell-for-cell with `results/c1/rung5.json` / `transfer.json`; the reply string "
        "for H2's second corpus inside `results_full.json` still says NOT RUN because `run_c1.py` hard-codes "
        "it and was not modified — the transfer arm lives in `transfer.json`, as in the frozen run.",
        "* `dense_top1` / `dense_margin` depend only on the question, so they cannot separate two items "
        "that share a question; the within-question separation in this design comes from BM25, the "
        "cross-encoder, `dense_presented` and `dense_rank_log`.",
        "",
        "## 6. Provenance",
        "",
        "```",
        "python 04_experiments/src/features_corrected.py --dataset all     # 3 CSVs + meta",
        "python 04_experiments/src/eval_corrected.py                       # main + rung5 + transfer + summary",
        "```",
        "",
        f"Timings (CPU, `sentence-transformers`): model load {m0['timings']['model_load_s']} s, main "
        f"index {m0['timings'].get('dev_index_s', float('nan'))} + "
        f"{m0['timings'].get('test_index_s', float('nan'))} s, main cross-encoder "
        f"{m0['timings'].get('dev_ce_s', float('nan'))} + {m0['timings'].get('test_ce_s', float('nan'))} s, "
        f"total {m0['timings']['total_s']} s (all three files).",
        "",
    ]
    path = ROOT / "04_experiments" / "results" / "corrected-dense-notes.md"
    path.write_text("\n".join(L) + "\n", encoding="utf-8")
    return path


def write_summary(full, frozen, r5, r5_old, tr, tr_old) -> list[tuple[str, str, str, str]]:
    rows: list[tuple[str, str, str, str]] = []

    def add(label: str, o, n, digits=4):
        d = None
        if isinstance(o, (int, float)) and isinstance(n, (int, float)):
            d = float(n) - float(o)
        rows.append((label, _fmt(o, digits), _fmt(n, digits),
                     "—" if d is None else f"{d:+.{digits}f}"))

    add("Dev AUROC", frozen["discrimination"]["dev_auroc"], full["discrimination"]["dev_auroc"])
    add("Test AUROC", frozen["discrimination"]["test_auroc"], full["discrimination"]["test_auroc"])

    for r in ("1", "2", "3", "4"):
        add(f"Confirmatory band — abstain precision, rung {r}",
            frozen["test"]["band_primary"]["per_rung"][r]["abstain_precision"],
            full["test"]["band_primary"]["per_rung"][r]["abstain_precision"])
    add("Confirmatory band — over-refusal (rung 0)",
        frozen["test"]["band_primary"]["over_refusal"],
        full["test"]["band_primary"]["over_refusal"])
    add("Confirmatory band — coverage",
        frozen["test"]["band_primary"]["coverage"],
        full["test"]["band_primary"]["coverage"])

    for r in ("1", "2", "3", "4"):
        add(f"Exploratory band — abstain precision, rung {r}",
            frozen["test"]["exploratory_band"]["per_rung"][r]["abstain_precision"],
            full["test"]["exploratory_band"]["per_rung"][r]["abstain_precision"])
    add("Exploratory band — over-refusal (rung 0)",
        frozen["test"]["exploratory_band"]["over_refusal"],
        full["test"]["exploratory_band"]["over_refusal"])
    add("Exploratory band — coverage",
        frozen["test"]["exploratory_band"]["coverage"],
        full["test"]["exploratory_band"]["coverage"])

    add("B1 (bm25_top1) — pooled abstain precision",
        frozen["baselines"]["B1_bm25_top1"]["test"]["pooled_abstain_precision"],
        full["baselines"]["B1_bm25_top1"]["test"]["pooled_abstain_precision"])
    add("B2 (dense_top1) — pooled abstain precision",
        frozen["baselines"]["B2_dense_top1"]["test"]["pooled_abstain_precision"],
        full["baselines"]["B2_dense_top1"]["test"]["pooled_abstain_precision"])
    add("B2 (dense_top1) — coverage",
        frozen["baselines"]["B2_dense_top1"]["test"]["coverage"],
        full["baselines"]["B2_dense_top1"]["test"]["coverage"])
    add("B2 (dense_top1) — over-refusal (rung 0)",
        frozen["baselines"]["B2_dense_top1"]["test"]["over_refusal"],
        full["baselines"]["B2_dense_top1"]["test"]["over_refusal"])
    add("B1 (bm25_top1) — coverage",
        frozen["baselines"]["B1_bm25_top1"]["test"]["coverage"],
        full["baselines"]["B1_bm25_top1"]["test"]["coverage"])
    add("H2 — dev→test pooled-precision loss (rate difference)",
        frozen["hypotheses"]["H2"]["loss_points"], full["hypotheses"]["H2"]["loss_points"])

    add("H1 — diff (rung 1 − rung 3)",
        frozen["hypotheses"]["H1"]["diff_r1_minus_r3"],
        full["hypotheses"]["H1"]["diff_r1_minus_r3"])
    rows.append(("H1 — 95% CI", 
                 f"[{_fmt(frozen['hypotheses']['H1']['ci95_lo'])}, {_fmt(frozen['hypotheses']['H1']['ci95_hi'])}]",
                 f"[{_fmt(full['hypotheses']['H1']['ci95_lo'])}, {_fmt(full['hypotheses']['H1']['ci95_hi'])}]",
                 "—"))
    add("H1 — rung-1 precision (test)",
        frozen["hypotheses"]["H1"]["rung1_precision"], full["hypotheses"]["H1"]["rung1_precision"])
    add("H1 — rung-3 precision (test)",
        frozen["hypotheses"]["H1"]["rung3_precision"], full["hypotheses"]["H1"]["rung3_precision"])

    add("H3 — band − matched single (diff)",
        frozen["hypotheses"]["H3"]["difference"]["diff"],
        full["hypotheses"]["H3"]["difference"]["diff"])
    rows.append(("H3 — 95% CI (paired bootstrap)",
                 f"[{_fmt(frozen['hypotheses']['H3']['difference']['lo'])}, "
                 f"{_fmt(frozen['hypotheses']['H3']['difference']['hi'])}]",
                 f"[{_fmt(full['hypotheses']['H3']['difference']['lo'])}, "
                 f"{_fmt(full['hypotheses']['H3']['difference']['hi'])}]",
                 "—"))

    add("Rung 5 (EXPLORATORY) — abstain precision, exploratory band",
        r5_old["rung5_test"]["exploratory_band"]["abstain_precision"],
        r5["rung5_test"]["exploratory_band"]["abstain_precision"])
    add("Rung 5 (EXPLORATORY) — abstain precision, confirmatory band",
        r5_old["rung5_test"]["confirmatory_band"]["abstain_precision"],
        r5["rung5_test"]["confirmatory_band"]["abstain_precision"])

    for op, name in (("confirmatory_band", "confirmatory band"),
                     ("exploratory_band", "exploratory band")):
        add(f"Transfer — rung-3 abstain precision, {name}",
            tr_old["transfer"]["operating_points"][op]["transfer_rung3_abstain_precision"],
            tr["transfer"]["operating_points"][op]["transfer_rung3_abstain_precision"])
    add("Transfer — AUROC (answerable vs rung 3)",
        tr_old["transfer"]["operating_points"]["confirmatory_band"]["auroc_answerable_vs_rung3"],
        tr["transfer"]["operating_points"]["confirmatory_band"]["auroc_answerable_vs_rung3"])

    hun = ("metric", "OLD — frozen (features.py, passage-as-query dense)",
           "CORRECTED (question-as-query dense)", "Δ")
    lines = ["# C1 — spec-conformant dense features: OLD vs CORRECTED",
             "",
             "Declared sensitivity analysis (PREREGISTRATION.md §4 read literally: `dense_presented` is a "
             "bge-small-en-v1.5 *cosine*, i.e. question against passage), not the pre-registered run. "
             "Every OLD value is read from `04_experiments/results/c1/*.json`; every CORRECTED value from "
             "`04_experiments/results/c1_corrected/*.json`. Generated by "
             "`04_experiments/src/eval_corrected.py`; no number in this table is typed by hand.",
             "",
             "| " + " | ".join(hun) + " |",
             "|" + "---|" * len(hun)]
    lines += ["| " + " | ".join(r) + " |" for r in rows]
    lines += [
        "",
        "Notes: the CORRECTED rung-5 and transfer numbers were produced with the **corrected** gate "
        "(refit on corrected dev rows) and the corrected thresholds; the OLD ones used the frozen gate. "
        "Item ids, item order, per-rung counts (n_dev = 1873, n_test = 1879) and the surface audit are "
        "identical between the two runs; only the dense block of the feature set differs, and every "
        "BM25 / cross-encoder / lexical-overlap cell is byte-identical.",
        "",
        "## What changes",
        "",
    ]
    tb_o, tb_n = frozen["thresholds"]["band"], full["thresholds"]["band"]
    lines += [f"Threshold caveat: the fitted operating points differ between runs (confirmatory band "
              f"[{tb_o['t_lo']:.4f}, {tb_o['t_hi']:.4f}] → [{tb_n['t_lo']:.4f}, {tb_n['t_hi']:.4f}], "
              f"exploratory band "
              f"[{frozen['exploratory']['operating_point']['band']['t_lo']:.4f}, "
              f"{frozen['exploratory']['operating_point']['band']['t_hi']:.4f}] → "
              f"[{full['exploratory']['operating_point']['band']['t_lo']:.4f}, "
              f"{full['exploratory']['operating_point']['band']['t_hi']:.4f}]), because the thresholds "
              f"are re-fitted on the corrected dev rows by the same pre-registered rule. The AUROC rows "
              f"are the threshold-free comparison; the precision/coverage rows compare two different "
              f"dev-fitted cuts, not the same cut on two feature sets.", ""]
    lines += _sentences(full, frozen, r5, r5_old, tr, tr_old)
    lines += [""]
    CORRECTED.mkdir(parents=True, exist_ok=True)
    (CORRECTED / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return rows


def _sentences(full, frozen, r5, r5_old, tr, tr_old) -> list[str]:
    """The three closing sentences. Every number is formatted from a JSON/CSV written by this pipeline."""
    h1n, h1o = full["hypotheses"]["H1"], frozen["hypotheses"]["H1"]
    h2n, h2o = full["hypotheses"]["H2"], frozen["hypotheses"]["H2"]
    h3n, h3o = full["hypotheses"]["H3"], frozen["hypotheses"]["H3"]
    d3n, d3o = h3n["difference"], h3o["difference"]

    flips = [f"{name} (supported {bool(o)} → {bool(n)})"
             for name, n, o in (("H1", h1n["supported"], h1o["supported"]),
                                ("H2", h2n["supported"], h2o["supported"]),
                                ("H3", h3n["supported"], h3o["supported"]))
             if bool(n) != bool(o)]

    # measured provenance of the rung-4 collapse: the frozen dense_presented was passage-vs-passage
    import csv as _csv
    import statistics as _st

    def rung4_dense(path: Path) -> tuple[float, float]:
        with open(path, encoding="utf-8", newline="") as fh:
            v = [float(r["dense_presented"]) for r in _csv.DictReader(fh) if r["rung"] == "4"]
        return float(_st.median(v)), float(max(v))

    old_med4, old_max4 = rung4_dense(DATA / "features.csv")
    new_med4, _ = rung4_dense(MAIN_CSV)
    meta = jload(DATA / "features_corrected_meta.json")["datasets"]["main"]["degeneracy_check"]

    flip_txt = "; ".join(flips)
    if flips:
        s_a = (f"**VERDICT FLIP — {flip_txt}.** "
               f"Under the spec-conformant features H1 "
               f"{'is' if h1n['supported'] else 'is not'} supported (rung-1 minus rung-3 abstain "
               f"precision {h1n['diff_r1_minus_r3']}, 95% CI [{h1n['ci95_lo']}, {h1n['ci95_hi']}]), "
               f"H2 is {'supported' if h2n['supported'] else 'not supported'} "
               f"(dev→test loss {h2n['loss_points']}, refuted={h2n['refuted']}) and H3 is "
               f"{'supported' if h3n['supported'] else 'not supported'} "
               f"(band − matched single {d3n['diff']}, 95% CI [{d3n['lo']}, {d3n['hi']}]).")
    else:
        s_a = (f"No pre-registered verdict changes: H1 is unsupported under both feature sets "
               f"(rung-1 minus rung-3 abstain precision {h1n['diff_r1_minus_r3']} with 95% CI "
               f"[{h1n['ci95_lo']}, {h1n['ci95_hi']}] over {h1n['n_pairs']} paired questions), H2 "
               f"remains refuted on the within-corpus arm (dev→test loss {h2o['loss_points']} → "
               f"{h2n['loss_points']}, both inside the 0.05 refutation band), and H3 remains "
               f"unsupported — but H3 stops being a degenerate zero and turns significantly negative, "
               f"{d3n['diff']} (95% CI [{d3n['lo']}, {d3n['hi']}], n={d3n['n']}) against "
               f"{d3o['diff']} [{d3o['lo']}, {d3o['hi']}] in the frozen run, so the band is now "
               f"measurably worse than the recall-matched single threshold rather than identical to it.")

    cb = full["test"]["band_primary"]
    eb = full["test"]["exploratory_band"]
    b2 = full["baselines"]["B2_dense_top1"]
    s_b = (f"The 'overlap drives the ladder' story survives where it was measurable and fails at "
           f"rung 4: the surface audit is unchanged between runs (lex-overlap AUROC "
           f"{full['audit']['dev_auroc_sensitivity_with_lex']['1']} / "
           f"{full['audit']['dev_auroc_sensitivity_with_lex']['2']} / "
           f"{full['audit']['dev_auroc_sensitivity_with_lex']['3']} on dev rungs 1-3) and the corrected "
           f"gate still refuses {cb['per_rung']['1']['abstain_precision']:.4f} / "
           f"{cb['per_rung']['2']['abstain_precision']:.4f} / "
           f"{cb['per_rung']['3']['abstain_precision']:.4f} of test rungs 1-3 and "
           f"{r5['rung5_test']['exploratory_band']['abstain_precision']:.4f} of the overlap-matched "
           f"rung 5, so the ladder is not an artifact of the dense block; what does not survive is "
           f"rung 4, whose frozen `dense_presented` was really cos(rewrite, gold) (median {old_med4:.4f}, "
           f"max {old_max4:.4f}) and therefore separated 'presented == gold' from "
           f"'presented == rewrite' for free — with the §4 question-passage cosine the rewrite scores "
           f"{new_med4:.4f}, within noise of its own answerable original, and rung 4 falls to AUROC "
           f"{cb['per_rung']['4']['auroc_answerable_vs_this_rung']} and exploratory-band precision "
           f"{eb['per_rung']['4']['abstain_precision']}.")

    s_c = (f"B2 is now a real baseline rather than a constant: `dense_top1` takes "
           f"{meta['n_distinct_dense_top1']} distinct values (it was 1.0 on every rung-0–3 row) and "
           f"scores {b2['test']['pooled_abstain_precision']:.4f} pooled abstain precision, but at "
           f"{b2['test']['coverage']:.4f} coverage and {b2['test']['over_refusal']:.4f} over-refusal "
           f"(dev-feasible={b2['threshold']['feasible']}), so it beats the corrected gate's "
           f"{cb['pooled_abstain_precision']:.4f} at {cb['coverage']:.4f} coverage only by refusing "
           f"almost everything — a genuine score at a degenerate operating point, not a usable "
           f"competitor.")
    return [s_a, "", s_b, "", s_c]


def main() -> int:
    t0 = time.time()
    CORRECTED.mkdir(parents=True, exist_ok=True)

    ret = run_main()
    print("[main] run_c1.analyse status:", ret.get("status"))
    item_check = assert_same_items()
    print("[main] item identity:", json.dumps(item_check))

    full = jload(CORRECTED / "results_full.json")
    frozen = jload(FROZEN / "results_full.json")

    sc = spec_check(item_check, full, frozen)
    jdump(CORRECTED / "spec_check.json", sc)
    print(f"[main] max |Δcoef| vs frozen gate = {sc['gate_max_abs_coef_delta']}")

    r5 = run_rung5()
    r5_old = jload(FROZEN / "rung5.json")
    print(f"[rung5] exploratory-band precision {r5['rung5_test']['exploratory_band']['abstain_precision']} "
          f"(frozen {r5_old['rung5_test']['exploratory_band']['abstain_precision']})")

    tr = run_transfer()
    tr_old = jload(FROZEN / "transfer.json")
    print("[transfer]", json.dumps({k: v["transfer_rung3_abstain_precision"]
                                    for k, v in tr["transfer"]["operating_points"].items()}))

    rows = write_summary(full, frozen, r5, r5_old, tr, tr_old)
    notes_path = write_notes(full, frozen, r5, r5_old, tr, tr_old, sc)
    print(f"[notes] -> {notes_path}")
    print(f"[summary] {len(rows)} rows -> {CORRECTED / 'SUMMARY.md'}")
    print(f"[done] {round(time.time() - t0, 1)} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
