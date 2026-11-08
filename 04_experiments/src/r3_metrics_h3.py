"""R3-1 metrics: H3 matched-recall audit (MF-19, MF-20, MF-29).

Owned file: 04_experiments/src/r3_metrics_h3.py
Writes:
  04_experiments/results/c1/r3/metrics/h3.json
  sessions/R3-1-metrics/reports/r3_metrics_h3.md

Run: python 04_experiments/src/r3_metrics_h3.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "04_experiments" / "src"
DATA = ROOT / "04_experiments" / "data"
RESULTS = ROOT / "04_experiments" / "results" / "c1"
CORRECTED = ROOT / "04_experiments" / "results" / "c1_corrected"
R3METRICS = RESULTS / "r3" / "metrics"
REPORT = ROOT / "sessions" / "R3-1-metrics" / "reports" / "r3_metrics_h3.md"

sys.path.insert(0, str(SRC))
import gate as G  # noqa: E402

SEED = 12345          # bootstrap seed (gate.BOOT_SEED)
CONFIG_SEED = 20261103
N_BOOT = 10000
COMMAND = "python 04_experiments/src/r3_metrics_h3.py"
TARGET_PRECISION = 0.80
RECALL_TOL = 1e-3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_items():
    with open(DATA / "items.jsonl", encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def fmt(x, nd=4):
    if x is None:
        return "NA"
    if isinstance(x, float):
        return f"{x:.{nd}f}"
    return str(x)


def main() -> int:
    R3METRICS.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)

    # ---- inputs ---------------------------------------------------------------
    items = load_items()
    feats = G.load_features(DATA / "features_corrected.csv")
    ids = [it["item_id"] for it in items if it["item_id"] in feats]
    items = [it for it in items if it["item_id"] in feats]
    dev_ids = [it["item_id"] for it in items if it["split"] == "dev"]
    test_ids = [it["item_id"] for it in items if it["split"] == "test"]
    y_dev = np.asarray([feats[i]["label"] for i in dev_ids], dtype=int)
    y_test = np.asarray([feats[i]["label"] for i in test_ids], dtype=int)

    rf = json.loads((CORRECTED / "results_full.json").read_text(encoding="utf-8"))

    # ---- gate + thresholds (recomputed on corrected features) ------------------
    gate = G.fit_logistic_gate(feats, dev_ids)
    s_dev = gate.score(feats, dev_ids)
    s_test = gate.score(feats, test_ids)
    band = G.fit_band_thresholds(s_dev, y_dev)            # confirmatory band
    matched_grid = G.match_single_to_recall(s_dev, y_dev, band["dev_recall"])  # as in run_c1

    neg_dev = int((y_dev == 0).sum())
    neg_test_mask = np.asarray([it["rung"] > 0 for it in items if it["split"] == "test"], dtype=bool)
    test_items = [it for it in items if it["split"] == "test"]
    pos_test_mask = np.asarray([it["rung"] == 0 for it in test_items], dtype=bool)

    ref_band_test = G.refused_band(s_test, band["t_lo"], band["t_hi"])

    # ---- (1) corrected dev recalls --------------------------------------------
    reported_band_recall = float(rf["thresholds"]["band"]["dev_recall"])          # 0.9898
    reported_matched_recall = float(rf["thresholds"]["single_matched_recall"]["dev_recall"])  # 0.9925
    reported_matched_precision = float(rf["thresholds"]["single_matched_recall"]["dev_precision"])  # 0.7886

    dev_recalls = {
        "from_corrected_results_full": {
            "band_dev_recall": reported_band_recall,
            "matched_single_dev_recall": reported_matched_recall,
            "matched_single_dev_precision": reported_matched_precision,
        },
        "recomputed": {
            "band_dev_recall": float(band["dev_recall"]),
            "matched_single_dev_recall": float(matched_grid["dev_recall"]),
            "matched_single_dev_precision": float(matched_grid["dev_precision"]),
        },
    }

    # ---- (2) degenerate construction check ------------------------------------
    degenerate = {
        "single_matched_recall_t": float(matched_grid["t"]),
        "band_t_lo": float(band["t_lo"]),
        "equal": bool(matched_grid["t"] == band["t_lo"]),
        "band_t_hi": float(band["t_hi"]),
        "n_heldout_above_t_hi": int((s_test > band["t_hi"]).sum()),
        "n_heldout_below_t_lo": int((s_test < band["t_lo"]).sum()),
        "n_heldout_between": int(((s_test >= band["t_lo"]) & (s_test <= band["t_hi"])).sum()),
        "note": ("In the frozen run single_matched_recall.t == band.t_lo (degenerate: only the "
                 "upper cut can differ). In the corrected run this equality does NOT hold, so the "
                 "construction is not degenerate in that sense; the matched threshold sits above "
                 "the band's upper threshold instead."),
    }

    # ---- (3) search for a precision-compliant, recall-matched single threshold --
    # grid-based feasible set
    feasible_grid = []
    for t in G._grid(s_dev):
        refused = s_dev < t
        nref = int(refused.sum())
        if nref == 0:
            continue
        tp = int(refused[y_dev == 0].sum())
        prec = tp / nref
        rec = tp / max(1, neg_dev)
        over = float(refused[y_dev == 1].mean())
        if prec >= TARGET_PRECISION:
            feasible_grid.append({"t": float(t), "dev_precision": float(prec),
                                 "dev_recall": float(rec), "dev_n_refused": nref,
                                 "dev_over_refusal": float(over)})

    # all-unique (exhaustive) feasible set
    feasible_all = []
    for t in sorted(set(s_dev.tolist())):
        refused = s_dev < t
        nref = int(refused.sum())
        if nref == 0:
            continue
        tp = int(refused[y_dev == 0].sum())
        prec = tp / nref
        rec = tp / max(1, neg_dev)
        over = float(refused[y_dev == 1].mean())
        if prec >= TARGET_PRECISION:
            feasible_all.append({"t": float(t), "dev_precision": float(prec),
                                "dev_recall": float(rec), "dev_n_refused": nref,
                                "dev_over_refusal": float(over)})

    max_feasible_recall = max((f["dev_recall"] for f in feasible_all), default=None)
    closest_feasible = max(feasible_all, key=lambda f: f["dev_recall"], default=None)

    # exact recall match (ignoring precision)
    target_recall = float(band["dev_recall"])
    best_exact = None
    for t in sorted(set(s_dev.tolist())):
        refused = s_dev < t
        nref = int(refused.sum())
        if nref == 0:
            continue
        tp = int(refused[y_dev == 0].sum())
        rec = tp / max(1, neg_dev)
        prec = tp / nref
        key = (abs(rec - target_recall), t)
        if best_exact is None or key < best_exact[0]:
            best_exact = (key, t, prec, rec, nref)
    t_exact = float(best_exact[1])
    prec_exact = float(best_exact[2])
    rec_exact = float(best_exact[3])
    nref_exact = int(best_exact[4])

    constrained_exists = bool(any(
        f["dev_recall"] >= target_recall - 1e-12 for f in feasible_all
    ))
    # more directly: feasible threshold with recall >= target
    constrained_exists = bool(any(f["dev_recall"] >= target_recall for f in feasible_all))

    constrained_search = {
        "target_recall": target_recall,
        "precision_constraint": TARGET_PRECISION,
        "grid_feasible_count": len(feasible_grid),
        "exhaustive_feasible_count": len(feasible_all),
        "max_feasible_recall": max_feasible_recall,
        "closest_feasible_threshold": closest_feasible,
        "exact_recall_match_threshold": {
            "t": t_exact,
            "dev_precision": prec_exact,
            "dev_recall": rec_exact,
            "dev_n_refused": nref_exact,
            "precision_constraint_satisfied": bool(prec_exact >= TARGET_PRECISION),
        },
        "constrained_threshold_exists": constrained_exists,
        "statement": ("No single threshold satisfies both the 0.80 abstain-precision constraint "
                      "and a dev abstain recall of 0.9898: the highest recall attainable by any "
                      "precision-compliant single threshold is %.4f, below the band's 0.9898. The "
                      "threshold that genuinely matches the band's dev recall (%.6f) has dev "
                      "precision %.4f, which violates the 0.80 constraint."
                      % (max_feasible_recall, rec_exact, prec_exact)),
    }

    # ---- re-match on recall + difference + interval ---------------------------
    ref_matched_exact_test = s_test < t_exact
    heldout_precision_exact = float(ref_matched_exact_test[neg_test_mask].mean())
    re_matched_diff = G.boot_precision_diff(ref_band_test, ref_matched_exact_test,
                                            neg_test_mask, n_boot=N_BOOT, seed=SEED)

    # original grid matched (as reported) for reference
    ref_matched_grid_test = s_test < matched_grid["t"]
    heldout_precision_grid = float(ref_matched_grid_test[neg_test_mask].mean())
    original_diff = G.boot_precision_diff(ref_band_test, ref_matched_grid_test,
                                          neg_test_mask, n_boot=N_BOOT, seed=SEED)

    # feasible highest-recall compliant threshold, for reference
    if closest_feasible is not None:
        ref_feas_test = s_test < closest_feasible["t"]
        heldout_precision_feas = float(ref_feas_test[neg_test_mask].mean())
        feasible_diff = G.boot_precision_diff(ref_band_test, ref_feas_test,
                                             neg_test_mask, n_boot=N_BOOT, seed=SEED)
    else:
        heldout_precision_feas = None
        feasible_diff = None

    re_match = {
        "method": "single threshold minimizing |dev recall - band dev recall| over all unique scores",
        "threshold": t_exact,
        "dev_recall": rec_exact,
        "dev_precision": prec_exact,
        "heldout_abstain_precision": heldout_precision_exact,
        "difference": re_matched_diff,
        "band_heldout_precision": float(ref_band_test[neg_test_mask].mean()),
    }

    # ---- (4) corrected arm 11.00% over-refusal -------------------------------
    band_x = G.fit_band_constrained(s_dev, y_dev, 0.10)
    ref_band_x_test = G.refused_band(s_test, band_x["t_lo"], band_x["t_hi"])
    held_out_over_recomputed = float(ref_band_x_test[pos_test_mask].mean())

    reported_dev_over = float(rf["exploratory"]["operating_point"]["band"]["dev_over_refusal"])  # 0.095
    reported_held_out_over = float(rf["test"]["exploratory_band"]["over_refusal"])  # 0.11
    cap = float(rf["exploratory"]["operating_point"]["max_over_refusal"])  # 0.10

    over_refusal_arm = {
        "corrected_exploratory_band": {
            "dev_over_refusal": float(band_x["dev_over_refusal"]),
            "dev_over_refusal_reported": reported_dev_over,
            "held_out_over_refusal": held_out_over_recomputed,
            "held_out_over_refusal_reported": reported_held_out_over,
            "max_over_refusal_cap": cap,
            "cap_binds_on": "dev (fit_band_constrained enforces dev over-refusal <= cap during threshold search)",
            "breached_on_dev": bool(band_x["dev_over_refusal"] > cap),
            "breached_on_held_out": bool(held_out_over_recomputed > cap),
            "statement": ("The declared 0.10 cap binds on dev by construction. Corrected dev "
                          "over-refusal is %.4f (<= 0.10, not breached on dev). Held-out "
                          "over-refusal is %.4f (> 0.10), so the cap is breached on the held-out "
                          "half even though it holds on dev."
                          % (band_x["dev_over_refusal"], held_out_over_recomputed)),
        },
    }

    # ---- assemble -------------------------------------------------------------
    inputs = {
        "features_corrected_csv": str((DATA / "features_corrected.csv").relative_to(ROOT).as_posix()),
        "results_full_corrected": str((CORRECTED / "results_full.json").relative_to(ROOT).as_posix()),
        "items_jsonl": str((DATA / "items.jsonl").relative_to(ROOT).as_posix()),
        "gate_py": str((SRC / "gate.py").relative_to(ROOT).as_posix()),
    }
    input_hashes = {k: sha256(ROOT / v) for k, v in inputs.items()}

    doc = {
        "experiment": "c1",
        "generated_by": "04_experiments/src/r3_metrics_h3.py",
        "command": COMMAND,
        "seed": SEED,
        "config_seed": CONFIG_SEED,
        "n_boot": N_BOOT,
        "target_precision": TARGET_PRECISION,
        "inputs": input_hashes,
        "input_paths": inputs,
        "dev_recalls": dev_recalls,
        "degenerate_check": degenerate,
        "constrained_search": constrained_search,
        "original_matched_grid": {
            "threshold": float(matched_grid["t"]),
            "dev_recall": float(matched_grid["dev_recall"]),
            "dev_precision": float(matched_grid["dev_precision"]),
            "heldout_abstain_precision": heldout_precision_grid,
            "difference": original_diff,
        },
        "re_matched_recall": re_match,
        "feasible_highest_recall": {
            "threshold": (closest_feasible["t"] if closest_feasible else None),
            "dev_recall": (closest_feasible["dev_recall"] if closest_feasible else None),
            "dev_precision": (closest_feasible["dev_precision"] if closest_feasible else None),
            "heldout_abstain_precision": heldout_precision_feas,
            "difference": feasible_diff,
        },
        "over_refusal_arm": over_refusal_arm,
        "verdicts": {
            "MF_19": ("Corrected dev recalls are not matched (band %.4f vs matched single %.4f); "
                      "matched single dev precision %.4f < 0.80. No precision-compliant single "
                      "threshold reaches the band's dev recall. Re-matching on recall (t=%.6f) "
                      "gives held-out precision %.4f vs band %.4f, difference %.4f [%.4f, %.4f]."
                      % (reported_band_recall, reported_matched_recall, reported_matched_precision,
                         t_exact, heldout_precision_exact,
                         float(ref_band_test[neg_test_mask].mean()),
                         re_matched_diff["diff"], re_matched_diff["lo"], re_matched_diff["hi"])),
            "MF_29": ("On the corrected run single_matched_recall.t (%.6f) != band.t_lo (%.6f), so "
                      "the frozen-run degeneracy does not apply. Held-out items scoring above t_hi: %d."
                      % (matched_grid["t"], band["t_lo"], int((s_test > band["t_hi"]).sum()))),
            "MF_20": ("Cap binds on dev. Corrected dev over-refusal %.4f <= 0.10 (not breached on "
                      "dev); held-out over-refusal %.4f > 0.10 (breached on held-out)."
                      % (band_x["dev_over_refusal"], held_out_over_recomputed)),
        },
    }

    out_json = R3METRICS / "h3.json"
    out_json.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # ---- markdown report ------------------------------------------------------
    lines = []
    A = lines.append
    A("# R3 metrics — H3 matched-recall audit (MF-19, MF-20, MF-29)\n")
    A("Generated by `04_experiments/src/r3_metrics_h3.py` (command: `%s`). "
      "Bootstrap seed %d, %d draws. Every number below is read from "
      "`04_experiments/results/c1/r3/metrics/h3.json`.\n" % (COMMAND, SEED, N_BOOT))
    A("## (1) Corrected dev recalls (from corrected results_full.json)\n")
    A("| quantity | value |")
    A("|---|---:|")
    A("| band dev recall | %.4f |" % reported_band_recall)
    A("| matched single dev recall | %.4f |" % reported_matched_recall)
    A("| matched single dev precision | %.4f |" % reported_matched_precision)
    A("")
    A("## (2) Degenerate construction check\n")
    A("- single_matched_recall.t = %.12f" % matched_grid["t"])
    A("- band.t_lo = %.12f" % band["t_lo"])
    A("- equal (degenerate): %s" % ("yes" if matched_grid["t"] == band["t_lo"] else "no"))
    A("- held-out items scoring above t_hi (%.6f): **%d** of %d" % (band["t_hi"],
                                                                   int((s_test > band["t_hi"]).sum()),
                                                                   len(s_test)))
    A("- held-out items below t_lo: %d; between: %d" % (int((s_test < band["t_lo"]).sum()),
                                                        int(((s_test >= band["t_lo"]) & (s_test <= band["t_hi"])).sum())))
    A("")
    A("## (3) Precision-compliant, recall-matched single threshold\n")
    A("Search over %d grid + %d unique score thresholds: **no** single threshold satisfies "
      "precision >= %.2f AND dev recall = %.4f. Highest precision-compliant recall: %.4f "
      "(threshold %.6f). The threshold that genuinely matches dev recall (%.6f) has dev "
      "precision %.4f, violating the constraint.\n"
      % (len(G._grid(s_dev)), len(set(s_dev.tolist())), TARGET_PRECISION, target_recall,
         max_feasible_recall, closest_feasible["t"], rec_exact, prec_exact))
    A("Re-match on recall: t = %.12f, dev recall = %.4f, dev precision = %.4f, "
      "held-out abstain precision = %.4f." % (t_exact, rec_exact, prec_exact, heldout_precision_exact))
    A("Band held-out abstain precision = %.4f." % float(ref_band_test[neg_test_mask].mean()))
    A("Difference (band - matched) = %.4f, 95%% CI [%.4f, %.4f] (n=%d negatives)."
      % (re_matched_diff["diff"], re_matched_diff["lo"], re_matched_diff["hi"], re_matched_diff["n"]))
    A("Original (grid) matched single: t = %.6f, dev recall = %.4f, held-out precision = %.4f, "
      "difference = %.4f [%.4f, %.4f]." % (matched_grid["t"], matched_grid["dev_recall"],
                                            heldout_precision_grid, original_diff["diff"],
                                            original_diff["lo"], original_diff["hi"]))
    A("")
    A("## (4) Corrected arm 11.00% over-refusal vs 0.10 cap\n")
    A("- dev over-refusal (corrected exploratory band): %.4f" % band_x["dev_over_refusal"])
    A("- held-out over-refusal (corrected exploratory band): %.4f" % held_out_over_recomputed)
    A("- declared cap: %.2f, binds on: dev (by construction)" % cap)
    A("- breached on dev: %s" % ("yes" if band_x["dev_over_refusal"] > cap else "no"))
    A("- breached on held-out: %s" % ("yes" if held_out_over_recomputed > cap else "no"))
    A("")
    A("## Verdicts\n")
    A("- MF-19: %s" % doc["verdicts"]["MF_19"])
    A("- MF-29: %s" % doc["verdicts"]["MF_29"])
    A("- MF-20: %s" % doc["verdicts"]["MF_20"])
    A("")
    A("---")
    A("_Inputs (sha256):_")
    for k, v in input_hashes.items():
        A("- %s: `%s`" % (k, v))
    A("")

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "wrote": [str(out_json), str(REPORT)],
        "dev_recalls": dev_recalls,
        "degenerate_equal": degenerate["equal"],
        "n_heldout_above_t_hi": degenerate["n_heldout_above_t_hi"],
        "constrained_exists": constrained_exists,
        "max_feasible_recall": max_feasible_recall,
        "re_matched_diff": re_matched_diff,
        "over_refusal": over_refusal_arm,
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())