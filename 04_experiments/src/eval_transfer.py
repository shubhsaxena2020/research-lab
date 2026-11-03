"""C1 — H2 second arm: the FROZEN operating point applied to the 400 2WikiMultihopQA items.

Reads nothing that it fits: the logistic gate is re-fitted from the same dev rows as the main run
and its coefficients are asserted against `results_full.json` (tolerance 1e-3) before any transfer
number is computed; both thresholds are read from that file, never recomputed. The transfer corpus
is used for evaluation only.

Reported per operating point (confirmatory band, exploratory band from PREREGISTRATION §10 D1.2):
abstain precision on transfer rung 3, over-refusal on transfer rung 0, coverage,
AUROC(answerable vs rung 3), BCa 95% CI for every rate, n — beside the main run's test rung-3 and
rung-1 precision, and the drop relative to test rung 3.

This is a DIRECTION test: the transfer construct differs (no article grouping, different question
type, shorter passages), so no magnitude equivalence is claimed.

Writes `04_experiments/results/c1/transfer.json`.

Run: python 04_experiments/src/eval_transfer.py
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "04_experiments" / "src"
DATA = ROOT / "04_experiments" / "data"
RESULTS = ROOT / "04_experiments" / "results" / "c1"
FULL = RESULTS / "results_full.json"
OUT = RESULTS / "transfer.json"

sys.path.insert(0, str(SRC))
import gate  # noqa: E402

COEF_TOL = 1e-3
SQUAD_RAW = DATA / "raw" / "dev-v2.0.json"
WIKI_RAW = DATA / "raw" / "2wiki" / "2wikimultihop_dev.json"


def load_transfer_items() -> list[dict]:
    with open(DATA / "transfer_items.jsonl", encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def corpus_medians() -> dict:
    """Median paragraph length (chars) of each corpus, measured from the raw files."""
    squad = json.loads(SQUAD_RAW.read_text(encoding="utf-8"))["data"]
    sq = [len(p["context"]) for art in squad for p in art["paragraphs"]]
    wiki = json.loads(WIKI_RAW.read_text(encoding="utf-8"))
    import re
    ws = re.compile(r"\s+")
    wk = [len(ws.sub(" ", " ".join(s.strip() for s in sentences)).strip())
          for rec in wiki for _t, sentences in rec["context"]]
    return {"squad2_paragraph_median_chars": float(statistics.median(sq)), "n_squad_paragraphs": len(sq),
            "2wiki_paragraph_median_chars": float(statistics.median(wk)), "n_2wiki_paragraphs": len(wk)}


def dense_degeneracy() -> dict:
    """Measured check on the dense features, in the main run and in the transfer arm.

    `features.py` encodes the presented passage as the dense *query* (`Pq = dense.encode(present_text)`)
    and then scores `P @ Pq[k]`, so the presented passage is compared with itself. This function only
    reports the consequence from the written CSVs; `features.py` is not modified here.
    """
    import csv

    def stats(path: Path) -> dict:
        with open(path, encoding="utf-8", newline="") as fh:
            rows = list(csv.DictReader(fh))
        ones = sum(1 for r in rows if abs(float(r["dense_presented"]) - 1.0) <= 1e-6)
        eq_top1 = sum(1 for r in rows if abs(float(r["dense_presented"]) - float(r["dense_top1"])) <= 1e-9)
        ranks = {r["dense_rank_log"] for r in rows}
        return {"n_rows": len(rows), "frac_dense_presented_eq_1": round(ones / len(rows), 4),
                "frac_dense_presented_eq_dense_top1": round(eq_top1 / len(rows), 4),
                "n_distinct_dense_rank_log": len(ranks)}

    main = stats(DATA / "features.csv")
    main["per_rung_frac_dense_presented_eq_1"] = {}
    with open(DATA / "features.csv", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    for r in ("0", "1", "2", "3", "4"):
        sub = [x for x in rows if x["rung"] == r]
        if sub:
            main["per_rung_frac_dense_presented_eq_1"][r] = round(
                sum(1 for x in sub if abs(float(x["dense_presented"]) - 1.0) <= 1e-6) / len(sub), 4)
    return {"main_run_features_csv": main,
            "transfer_features_csv": stats(DATA / "features_transfer.csv"),
            "note": ("features.py sets the dense query to the presented passage itself "
                     "(Pq = dense.encode(present_text)), so the presented passage is scored against "
                     "itself: dense_presented is 1.0 and dense_rank_log is log1p(1) for every main-run "
                     "row of rungs 0-3 and for every transfer row. The dense terms therefore carry no "
                     "question-conditioned retrieval signal; the gate's separation comes from BM25, the "
                     "cross-encoder and lexical overlap. The transfer arm reuses the maths exactly as "
                     "instructed; features.py was not modified (out of scope for this task).")}


def main() -> int:
    ap = argparse.ArgumentParser(description="Evaluate the frozen gate on the transfer arm.")
    ap.add_argument("--no-write", action="store_true")
    a = ap.parse_args()

    ref = json.loads(FULL.read_text(encoding="utf-8"))
    items = gate.load_items()
    feats = gate.load_features()

    # ---- 1. refit the gate on exactly the main run's dev ids, then assert it matches
    dev_ids = [it["item_id"] for it in items if it["split"] == "dev"]
    g = gate.fit_logistic_gate(feats, dev_ids)
    coef_ref = ref["gate"]["coef"]
    diffs = {c: abs(float(w) - float(coef_ref[c])) for c, w in zip(g.features, g.clf.coef_[0])}
    int_diff = abs(float(g.clf.intercept_[0]) - float(ref["gate"]["intercept"]))
    max_diff = max(max(diffs.values()), int_diff)
    assertion = {"n_dev": len(dev_ids), "tolerance": COEF_TOL,
                 "max_abs_diff": round(float(max_diff), 10),
                 "max_abs_diff_per_coef": {c: round(v, 10) for c, v in diffs.items()},
                 "intercept_abs_diff": round(float(int_diff), 10),
                 "passed": bool(max_diff <= COEF_TOL)}
    print(f"gate refit on {len(dev_ids)} dev rows; max |Δcoef| = {max_diff:.2e} "
          f"(tolerance {COEF_TOL}) -> {'PASS' if assertion['passed'] else 'FAIL'}")
    if not assertion["passed"]:
        print(json.dumps(diffs, indent=2), file=sys.stderr)
        raise SystemExit("coefficient assertion failed — refusing to report transfer numbers")

    # ---- 2. frozen thresholds (read, not recomputed)
    band = ref["thresholds"]["band"]
    expl = ref["exploratory"]["operating_point"]["band"]
    ops = {"confirmatory_band": {"label": "confirmatory (pre-registered)",
                                "t_lo": float(band["t_lo"]), "t_hi": float(band["t_hi"]),
                                "source": "results_full.json ['thresholds']['band']"},
           "exploratory_band": {"label": "EXPLORATORY (D1.2 constrained band)",
                                "t_lo": float(expl["t_lo"]), "t_hi": float(expl["t_hi"]),
                                "source": "results_full.json ['exploratory']['operating_point']['band']"}}

    # ---- 3. transfer items
    titems = load_transfer_items()
    tfeats = gate.load_features(DATA / "features_transfer.csv")
    tids = [it["item_id"] for it in titems]
    assert len(tids) == 400 and len(set(tids)) == 400, len(tids)
    assert set(tids) == set(tfeats), "feature rows do not match item ids"
    scores = g.score(tfeats, tids)
    rung = np.array([it["rung"] for it in titems])
    assert int((rung == 0).sum()) == 200 and int((rung == 3).sum()) == 200

    blocks, drops = {}, {}
    for name, op in ops.items():
        refused = gate.refused_band(scores, op["t_lo"], op["t_hi"])
        blk = gate.metrics_block(refused, titems, scores, name)
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
        drops[name] = {
            "test_rung3_precision": main["3"]["abstain_precision"],
            "test_rung1_precision": main["1"]["abstain_precision"],
            "transfer_rung3_precision": r3["abstain_precision"],
            "drop_points": round(float(main["3"]["abstain_precision"] - r3["abstain_precision"]), 4),
            "drop_pp": round(100.0 * float(main["3"]["abstain_precision"] - r3["abstain_precision"]), 2),
            "definition": "test rung-3 abstain precision minus transfer rung-3 abstain precision (same gate, same thresholds)",
        }

    med = corpus_medians()
    tmed = statistics.median([it["n_context_chars"] for it in titems])
    construct_note = (
        "DIRECTION TEST ONLY. The transfer corpus is 2WikiMultihopQA dev (Ho et al., COLING 2020), "
        "not SQuAD 2.0, and three construct differences prevent magnitude equivalence. "
        f"(1) No article grouping: each 2Wiki item ships `context` as independent Wikipedia articles, "
        f"so the rung-3 negative is another paragraph from the same question's article set, not a "
        f"same-document neighbour as in the dev arm. "
        f"(2) Passage length: corpus median paragraph {med['2wiki_paragraph_median_chars']:.0f} chars vs "
        f"{med['squad2_paragraph_median_chars']:.0f} for SQuAD 2.0 dev; the 400 presented transfer "
        f"passages have median {tmed:.0f} chars (length-filtered to 120-1200 by the builder). "
        f"(3) Question type: 2Wiki questions are multi-hop (compositional / comparison / bridge-"
        f"comparison / inference) and need two or more articles, whereas SQuAD questions are single-"
        f"paragraph extractive. The retrieval pool is also different in kind: the union of the 200 "
        f"source questions' article sets, not a split-wide paragraph pool. Read the transfer numbers as "
        f"the direction in which the frozen operating point moves on a harder, differently-built "
        f"corpus, not as an estimate of the same quantity."
    )

    out = {
        "experiment": "c1-transfer",
        "status": "ok",
        "gate": "same dev-fitted logistic gate as results_full.json, re-fitted and asserted",
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
            "frac_below_confirmatory_t_lo": round(float((scores < ops["confirmatory_band"]["t_lo"]).mean()), 4),
            "frac_below_exploratory_t_lo": round(float((scores < ops["exploratory_band"]["t_lo"]).mean()), 4)},
        "corpus_lengths": med,
        "feature_observation_dense_degenerate": dense_degeneracy(),
        "construct_note": construct_note,
        "statistics": {"ci": "item-level BCa bootstrap, gate.ci_mean", "n_boot": gate.N_BOOT,
                       "seed": gate.BOOT_SEED},
        "command": "python 04_experiments/src/eval_transfer.py",
    }

    print()
    for name in ("confirmatory_band", "exploratory_band"):
        b, d = blocks[name], drops[name]
        print(f"[{name}] t_lo={b['operating_point']['t_lo']:.6f} t_hi={b['operating_point']['t_hi']:.6f}")
        print(f"  transfer rung-3 abstain precision = {b['transfer_rung3_abstain_precision']:.4f} "
              f"CI95 [{b['transfer_rung3_ci95']['lo']}, {b['transfer_rung3_ci95']['hi']}] "
              f"({b['transfer_rung3_ci95'].get('method')}) n={b['transfer_rung3_n']}")
        print(f"  transfer rung-0 over-refusal     = {b['transfer_rung0_over_refusal']:.4f}  "
              f"coverage = {b['coverage']:.4f}  refused = {b['n_refused']}/{b['n_items']}")
        print(f"  AUROC(answerable vs rung 3)      = {b['auroc_answerable_vs_rung3']:.4f}")
        print(f"  test rung-3 = {d['test_rung3_precision']:.4f}  test rung-1 = {d['test_rung1_precision']:.4f}"
              f"  -> drop vs test rung-3 = {d['drop_pp']:+.2f} pp")
    print()
    print("score distribution on transfer:", json.dumps(out["score_distribution_transfer"]))

    if not a.no_write:
        OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
