"""R3 exploratory: R5 and transfer under BOTH runs, re-derived from gate scores.

Owned file: 04_experiments/src/r3_exp_both_runs.py
Writes: 04_experiments/results/c1/r3/exp/both_runs.json

Run: python 04_experiments/src/r3_exp_both_runs.py
Check: python 04_experiments/src/r3_exp_both_runs.py --check-repro

Re-derivation:
- frozen gate: gate.fit_logistic_gate on dev ids from data/features.csv
- corrected gate: gate.fit_logistic_gate on dev ids from data/features_corrected.csv
- thresholds: read from each run's results_full.json (confirmatory band +
  exploratory band); never refit here.

Scores:
- R5: features_rung5.csv (frozen) / features_corrected_rung5.csv (corrected),
  split=test (primary), split=dev (reference). AUROC(answerable test rung0 vs rung5).
- Transfer: features_transfer.csv (frozen) / features_corrected_transfer.csv
  (corrected), items transfer_items.jsonl. Report rung-3 abstain precision,
  rung-0 over-refusal, AUROC(answerable vs rung3).

Abstain precision here is the rate of negatives refused (fraction refused on
the negative set), matching gate.py's definition used in eval_rung5.py /
eval_transfer.py. Stored values are compared field-by-field and reported as
match/mismatch. Everything here is exploratory / post-hoc.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "04_experiments" / "src"
DATA = ROOT / "04_experiments" / "data"
RESULTS = ROOT / "04_experiments" / "results"
OUT_DEFAULT = RESULTS / "c1" / "r3" / "exp" / "both_runs.json"

sys.path.insert(0, str(SRC))
import gate as G  # noqa: E402

COMMAND = "python 04_experiments/src/r3_exp_both_runs.py"
TOL = 1e-4  # exact-match tolerance for recomputed vs stored (rounded 4dp values should match to <1e-4)


# --------------------------------------------------------------------------- #
# pure helpers
# --------------------------------------------------------------------------- #
def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_items_jsonl(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def compute_point(scores: np.ndarray, t_lo: float, t_hi: float) -> dict:
    """Abstain precision (fraction refused) + n + mean/median scores."""
    scores = np.asarray(scores, dtype=float)
    refused = G.refused_band(scores, float(t_lo), float(t_hi))
    return {
        "abstain_precision": round(float(refused.mean()), 4),
        "n": int(refused.size),
        "n_refused": int(refused.sum()),
        "mean_score": round(float(scores.mean()), 4),
        "median_score": round(float(np.median(scores)), 4),
    }


def auroc_answerable_vs_neg(pos_scores: np.ndarray, neg_scores: np.ndarray) -> float:
    y = np.concatenate([np.ones(len(pos_scores)), np.zeros(len(neg_scores))])
    s = np.concatenate([pos_scores, neg_scores])
    return round(float(roc_auc_score(y, s)), 4)


def match_bool(recomputed: float | None, stored: float | None) -> bool | None:
    if recomputed is None or stored is None:
        return None
    return bool(abs(float(recomputed) - float(stored)) <= TOL)


# --------------------------------------------------------------------------- #
# one gate fit
# --------------------------------------------------------------------------- #
def fit_gate(features_csv: Path, items: list[dict]) -> tuple[object, dict, list[str]]:
    feats = G.load_features(features_csv)
    dev_ids = [it["item_id"] for it in items if it["split"] == "dev" and it["item_id"] in feats]
    gate = G.fit_logistic_gate(feats, dev_ids)
    return gate, feats, dev_ids


def gate_assert(gate, full: dict, n_dev_ids: int) -> dict:
    info = gate.info()
    diffs = []
    for c in G.GATE_FEATURES:
        diffs.append(abs(float(info["coef"][c]) - float(full["gate"]["coef"][c])))
    diffs.append(abs(float(info["intercept"]) - float(full["gate"]["intercept"])))
    max_diff = float(max(diffs)) if diffs else 0.0
    return {
        "passed": bool(max_diff <= 1e-3),
        "max_absdiff": round(max_diff, 10),
        "tolerance": 1e-3,
        "n_dev_ids": n_dev_ids,
        "coef": info["coef"],
        "intercept": info["intercept"],
    }


# --------------------------------------------------------------------------- #
# R5 block
# --------------------------------------------------------------------------- #
def r5_block(gate, feats_main, items, items5, feats5_path, full, stored_r5):
    feats5 = G.load_features(feats5_path)
    test5 = [it for it in items5 if it["split"] == "test"]
    dev5 = [it for it in items5 if it["split"] == "dev"]
    pos_test = [it for it in items if it["split"] == "test" and it["rung"] == 0 and it["item_id"] in feats_main]
    pos_ids = [it["item_id"] for it in pos_test]

    s_pos = gate.score(feats_main, pos_ids)
    test_ids = [it["item_id"] for it in test5]
    dev_ids = [it["item_id"] for it in dev5]
    s_test = gate.score(feats5, test_ids)
    s_dev = gate.score(feats5, dev_ids)

    band = full["thresholds"]["band"]
    expl = full["exploratory"]["operating_point"]["band"]
    ops = {
        "confirmatory_band": {"t_lo": float(band["t_lo"]), "t_hi": float(band["t_hi"])},
        "exploratory_band": {"t_lo": float(expl["t_lo"]), "t_hi": float(expl["t_hi"])},
    }
    test_out = {}
    dev_out = {}
    for name, op in ops.items():
        test_out[name] = compute_point(s_test, op["t_lo"], op["t_hi"])
        dev_out[name] = compute_point(s_dev, op["t_lo"], op["t_hi"])

    auroc = auroc_answerable_vs_neg(s_pos, s_test)
    stored_auroc = float(stored_r5["auroc"]["answerable_test_rung0_vs_rung5"])

    # comparison vs stored
    comparisons = {}
    for split, recomputed_map, stored_map in (
        ("test", test_out, stored_r5["rung5_test"]),
        ("dev", dev_out, stored_r5["rung5_dev_reference"]),
    ):
        comparisons[split] = {}
        for name in ("confirmatory_band", "exploratory_band"):
            rec = recomputed_map[name]["abstain_precision"]
            sto = float(stored_map[name]["abstain_precision"])
            comparisons[split][name] = {
                "recomputed": rec,
                "stored": sto,
                "match": match_bool(rec, sto),
                "diff": round(float(rec - sto), 4),
            }
    comparisons["auroc"] = {
        "recomputed": auroc,
        "stored": stored_auroc,
        "match": match_bool(auroc, stored_auroc),
        "diff": round(float(auroc - stored_auroc), 4),
    }

    return {
        "thresholds": ops,
        "test": test_out,
        "dev": dev_out,
        "auroc_answerable_vs_rung5": auroc,
        "n_answerable_test": len(pos_ids),
        "n_rung5_test": len(test_ids),
        "n_rung5_dev": len(dev_ids),
        "stored": {
            "confirmatory_test": float(stored_r5["rung5_test"]["confirmatory_band"]["abstain_precision"]),
            "exploratory_test": float(stored_r5["rung5_test"]["exploratory_band"]["abstain_precision"]),
            "auroc": stored_auroc,
        },
        "comparison": comparisons,
    }


# --------------------------------------------------------------------------- #
# transfer block
# --------------------------------------------------------------------------- #
def transfer_block(gate, feats_dev, items, titems, tfeats_path, full, stored_tr):
    tfeats = G.load_features(tfeats_path)
    tids = [it["item_id"] for it in titems]
    scores = gate.score(tfeats, tids)
    rung = np.array([it["rung"] for it in titems])
    pos_mask = rung == 0
    neg_mask = rung == 3

    band = full["thresholds"]["band"]
    expl = full["exploratory"]["operating_point"]["band"]
    ops = {
        "confirmatory_band": {"t_lo": float(band["t_lo"]), "t_hi": float(band["t_hi"])},
        "exploratory_band": {"t_lo": float(expl["t_lo"]), "t_hi": float(expl["t_hi"])},
    }

    y = pos_mask.astype(int)
    auroc = round(float(roc_auc_score(y, scores)), 4)

    stored_ops = stored_tr["transfer"]["operating_points"]
    out = {}
    for name, op in ops.items():
        refused = G.refused_band(scores, op["t_lo"], op["t_hi"])
        r3_prec = round(float(refused[neg_mask].mean()), 4)
        r0_over = round(float(refused[pos_mask].mean()), 4)
        sto = float(stored_ops[name]["transfer_rung3_abstain_precision"])
        sto_auroc = float(stored_ops[name]["auroc_answerable_vs_rung3"])
        out[name] = {
            "t_lo": op["t_lo"],
            "t_hi": op["t_hi"],
            "rung3_abstain_precision": r3_prec,
            "rung3_n": int(neg_mask.sum()),
            "rung3_n_refused": int(refused[neg_mask].sum()),
            "rung0_over_refusal": r0_over,
            "rung0_n": int(pos_mask.sum()),
            "n_refused_total": int(refused.sum()),
            "coverage": round(float(1.0 - refused.mean()), 4),
            "auroc_answerable_vs_rung3": auroc,
            "stored_rung3_precision": sto,
            "stored_auroc": sto_auroc,
            "match_rung3_precision": match_bool(r3_prec, sto),
            "match_auroc": match_bool(auroc, sto_auroc),
            "diff_rung3_precision": round(float(r3_prec - sto), 4),
            "diff_auroc": round(float(auroc - sto_auroc), 4),
        }

    return {
        "auroc_answerable_vs_rung3": auroc,
        "n_items": len(tids),
        "n_rung0": int(pos_mask.sum()),
        "n_rung3": int(neg_mask.sum()),
        "operating_points": out,
    }


# --------------------------------------------------------------------------- #
# main builder
# --------------------------------------------------------------------------- #
def build_result() -> dict:
    items = load_items_jsonl(DATA / "items.jsonl")
    items5 = load_items_jsonl(DATA / "items_rung5.jsonl")
    titems = load_items_jsonl(DATA / "transfer_items.jsonl")

    full_f = json.loads((RESULTS / "c1" / "results_full.json").read_text(encoding="utf-8"))
    full_c = json.loads((RESULTS / "c1_corrected" / "results_full.json").read_text(encoding="utf-8"))
    r5_f = json.loads((RESULTS / "c1" / "rung5.json").read_text(encoding="utf-8"))
    r5_c = json.loads((RESULTS / "c1_corrected" / "rung5.json").read_text(encoding="utf-8"))
    tr_f = json.loads((RESULTS / "c1" / "transfer.json").read_text(encoding="utf-8"))
    tr_c = json.loads((RESULTS / "c1_corrected" / "transfer.json").read_text(encoding="utf-8"))

    input_paths = {
        "items": "04_experiments/data/items.jsonl",
        "items_rung5": "04_experiments/data/items_rung5.jsonl",
        "transfer_items": "04_experiments/data/transfer_items.jsonl",
        "features": "04_experiments/data/features.csv",
        "features_corrected": "04_experiments/data/features_corrected.csv",
        "features_rung5": "04_experiments/data/features_rung5.csv",
        "features_corrected_rung5": "04_experiments/data/features_corrected_rung5.csv",
        "features_transfer": "04_experiments/data/features_transfer.csv",
        "features_corrected_transfer": "04_experiments/data/features_corrected_transfer.csv",
        "frozen_results_full": "04_experiments/results/c1/results_full.json",
        "corrected_results_full": "04_experiments/results/c1_corrected/results_full.json",
        "frozen_rung5": "04_experiments/results/c1/rung5.json",
        "corrected_rung5": "04_experiments/results/c1_corrected/rung5.json",
        "frozen_transfer": "04_experiments/results/c1/transfer.json",
        "corrected_transfer": "04_experiments/results/c1_corrected/transfer.json",
    }

    # Frozen gate on features.csv dev
    feats_f = G.load_features(DATA / "features.csv")
    dev_ids = [it["item_id"] for it in items if it["split"] == "dev"]
    g_f = G.fit_logistic_gate(feats_f, dev_ids)
    # Corrected gate on features_corrected.csv dev
    feats_c = G.load_features(DATA / "features_corrected.csv")
    g_c = G.fit_logistic_gate(feats_c, dev_ids)

    frozen_r5 = r5_block(g_f, feats_f, items, items5, DATA / "features_rung5.csv", full_f, r5_f)
    corrected_r5 = r5_block(g_c, feats_c, items, items5, DATA / "features_corrected_rung5.csv", full_c, r5_c)

    frozen_tr = transfer_block(g_f, feats_f, items, titems, DATA / "features_transfer.csv", full_f, tr_f)
    corrected_tr = transfer_block(g_c, feats_c, items, titems, DATA / "features_corrected_transfer.csv", full_c, tr_c)

    def all_match(r5: dict, tr: dict) -> bool:
        vals = [
            r5["comparison"]["test"]["confirmatory_band"]["match"],
            r5["comparison"]["test"]["exploratory_band"]["match"],
            r5["comparison"]["dev"]["confirmatory_band"]["match"],
            r5["comparison"]["dev"]["exploratory_band"]["match"],
            r5["comparison"]["auroc"]["match"],
            tr["operating_points"]["confirmatory_band"]["match_rung3_precision"],
            tr["operating_points"]["confirmatory_band"]["match_auroc"],
            tr["operating_points"]["exploratory_band"]["match_rung3_precision"],
            tr["operating_points"]["exploratory_band"]["match_auroc"],
        ]
        return bool(all(v is True for v in vals))

    out = {
        "experiment": "c1",
        "stage": "r3_exp_both_runs",
        "generated_by": "04_experiments/src/r3_exp_both_runs.py",
        "command": COMMAND,
        "commands": [COMMAND, COMMAND + " --check-repro"],
        "exploratory": True,
        "post_hoc": True,
        "label": "exploratory/post-hoc",
        "note": (
            "R5 and transfer re-derived under both runs. Frozen gate fit on features.csv dev; "
            "corrected gate fit on features_corrected.csv dev. Thresholds read from each run's "
            "results_full.json, never refit here. Abstain precision = fraction refused on negatives."
        ),
        "input_paths": input_paths,
        "inputs": {k: sha256_file(ROOT / v) for k, v in input_paths.items()},
        "sha256_inputs": {k: sha256_file(ROOT / v) for k, v in input_paths.items()},
        "runs": {
            "frozen": {
                "gate_features_csv": "04_experiments/data/features.csv",
                "gate_rung5_features_csv": "04_experiments/data/features_rung5.csv",
                "gate_transfer_features_csv": "04_experiments/data/features_transfer.csv",
                "gate_assertion": gate_assert(g_f, full_f, len(dev_ids)),
                "thresholds": {
                    "confirmatory_band": {
                        "t_lo": float(full_f["thresholds"]["band"]["t_lo"]),
                        "t_hi": float(full_f["thresholds"]["band"]["t_hi"]),
                    },
                    "exploratory_band": {
                        "t_lo": float(full_f["exploratory"]["operating_point"]["band"]["t_lo"]),
                        "t_hi": float(full_f["exploratory"]["operating_point"]["band"]["t_hi"]),
                    },
                },
                "rung5": frozen_r5,
                "transfer": frozen_tr,
                "all_match_stored": all_match(frozen_r5, frozen_tr),
            },
            "corrected": {
                "gate_features_csv": "04_experiments/data/features_corrected.csv",
                "gate_rung5_features_csv": "04_experiments/data/features_corrected_rung5.csv",
                "gate_transfer_features_csv": "04_experiments/data/features_corrected_transfer.csv",
                "gate_assertion": gate_assert(g_c, full_c, len(dev_ids)),
                "thresholds": {
                    "confirmatory_band": {
                        "t_lo": float(full_c["thresholds"]["band"]["t_lo"]),
                        "t_hi": float(full_c["thresholds"]["band"]["t_hi"]),
                    },
                    "exploratory_band": {
                        "t_lo": float(full_c["exploratory"]["operating_point"]["band"]["t_lo"]),
                        "t_hi": float(full_c["exploratory"]["operating_point"]["band"]["t_hi"]),
                    },
                },
                "rung5": corrected_r5,
                "transfer": corrected_tr,
                "all_match_stored": all_match(corrected_r5, corrected_tr),
            },
        },
        "table": {
            "frozen": {
                "rung5_confirmatory_test": frozen_r5["test"]["confirmatory_band"]["abstain_precision"],
                "rung5_exploratory_test": frozen_r5["test"]["exploratory_band"]["abstain_precision"],
                "rung5_auroc": frozen_r5["auroc_answerable_vs_rung5"],
                "transfer_confirmatory_rung3": frozen_tr["operating_points"]["confirmatory_band"]["rung3_abstain_precision"],
                "transfer_exploratory_rung3": frozen_tr["operating_points"]["exploratory_band"]["rung3_abstain_precision"],
                "transfer_auroc": frozen_tr["auroc_answerable_vs_rung3"],
            },
            "corrected": {
                "rung5_confirmatory_test": corrected_r5["test"]["confirmatory_band"]["abstain_precision"],
                "rung5_exploratory_test": corrected_r5["test"]["exploratory_band"]["abstain_precision"],
                "rung5_auroc": corrected_r5["auroc_answerable_vs_rung5"],
                "transfer_confirmatory_rung3": corrected_tr["operating_points"]["confirmatory_band"]["rung3_abstain_precision"],
                "transfer_exploratory_rung3": corrected_tr["operating_points"]["exploratory_band"]["rung3_abstain_precision"],
                "transfer_auroc": corrected_tr["auroc_answerable_vs_rung3"],
            },
        },
    }
    return out


def _compare_results(a: dict, b: dict) -> bool:
    return a.get("table") == b.get("table") and a.get("runs", {}).get("frozen", {}).get("all_match_stored") == b.get("runs", {}).get("frozen", {}).get("all_match_stored") and a.get("runs", {}).get("corrected", {}).get("all_match_stored") == b.get("runs", {}).get("corrected", {}).get("all_match_stored")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="R5 + transfer under both runs, re-derived.")
    ap.add_argument("--out", type=str, default=str(OUT_DEFAULT))
    ap.add_argument("--check-repro", action="store_true")
    args = ap.parse_args(argv)

    result = build_result()
    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = ROOT / out_path

    if args.check_repro and out_path.exists():
        existing = json.loads(out_path.read_text(encoding="utf-8"))
        ok = _compare_results(existing, result)
        print("REPRO CHECK:", "PASS" if ok else "FAIL")
        return 0 if ok else 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    fr = result["runs"]["frozen"]
    co = result["runs"]["corrected"]
    print("wrote", out_path)
    print(f"frozen R5 test conf={fr['rung5']['test']['confirmatory_band']['abstain_precision']} expl={fr['rung5']['test']['exploratory_band']['abstain_precision']} auroc={fr['rung5']['auroc_answerable_vs_rung5']}")
    print(f"corrected R5 test conf={co['rung5']['test']['confirmatory_band']['abstain_precision']} expl={co['rung5']['test']['exploratory_band']['abstain_precision']} auroc={co['rung5']['auroc_answerable_vs_rung5']}")
    print(f"frozen transfer conf={fr['transfer']['operating_points']['confirmatory_band']['rung3_abstain_precision']} expl={fr['transfer']['operating_points']['exploratory_band']['rung3_abstain_precision']} auroc={fr['transfer']['auroc_answerable_vs_rung3']}")
    print(f"corrected transfer conf={co['transfer']['operating_points']['confirmatory_band']['rung3_abstain_precision']} expl={co['transfer']['operating_points']['exploratory_band']['rung3_abstain_precision']} auroc={co['transfer']['auroc_answerable_vs_rung3']}")
    print(f"all_match frozen={fr['all_match_stored']} corrected={co['all_match_stored']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
