"""C1 — stage 5: the confirmatory run, through the harness (provenance + repro check).

    python 04_experiments/src/run_c1.py                 # one run
    python 04_experiments/src/run_c1.py --check-repro 2  # CI-style rerun check

Writes, next to the harness run folder:
  04_experiments/results/c1/results_full.json   every number the paper may cite
  04_experiments/results/c1/audit.json          the §8 separability gate, before any result
  04_experiments/results/c1/predictions.csv     per-item gate decisions for every gate
and copies the same files into the run's artifacts/ folder.

If the separability audit fails after its rebuilds, this script still writes the audit, marks the run
`status: blocked_by_audit` and returns without reporting gate results — §8b says the audit *is* the
finding in that case.
"""
from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "04_experiments" / "src"))
sys.path.insert(0, str(ROOT / "04_experiments" / "harness"))

import audit as audit_mod  # noqa: E402
import gate as G  # noqa: E402
import runner  # noqa: E402

CFG = ROOT / "04_experiments" / "config" / "c1_gate.json"


def _write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True, default=lambda o: o.item()
                              if hasattr(o, "item") else str(o)) + "\n", encoding="utf-8")
    tmp.replace(path)


def analyse(cfg: dict) -> dict:
    seed_used = int(cfg.get("seed", 0))
    items = G.load_items()
    feats = G.load_features()
    ids = [it["item_id"] for it in items if it["item_id"] in feats]
    items = [it for it in items if it["item_id"] in feats]
    by_id = {it["item_id"]: it for it in items}

    # ---- §8a/§8b: the separability gate, run before anything is reported -------------
    rep_dev, kept_dev = audit_mod.audit_with_rebuild(items, split="dev",
                                                     seed=int(cfg.get("audit_seed", 13)))
    rep_test = audit_mod.audit(items, split="test")
    audit_report = {"dev_before_rebuild": audit_mod.audit(items, split="dev"),
                    "dev_after_rebuild": rep_dev, "test_reference": rep_test,
                    "stopping_rule": "PREREGISTRATION.md §8a/§8b"}
    _write_json(G.RESULTS / "audit.json", audit_report)
    blocking = [r for r in rep_dev["failing_rungs"]]
    if len(blocking) > int(cfg.get("max_failing_rungs", 2)):
        return {"status": "blocked_by_audit",
                "n_failing_rungs_after_rebuild": len(blocking),
                "failing_rungs_after_rebuild": ",".join(str(r) for r in blocking)}

    # rebuild selection is a dev-time rule; when it fires, apply the same rule to test items
    if any(k for k, v in rep_dev.get("rebuilt_rungs", {}).items() if v):
        for split in ("dev", "test"):
            sel = [it for it in items if it["split"] == split]
            pos = [it for it in sel if it["rung"] == 0]
            for r in [int(k) for k, v in rep_dev["rebuilt_rungs"].items() if v]:
                neg = [it for it in sel if it["rung"] == r]
                keep = {n["item_id"] for n in audit_mod.length_match(neg, pos, seed=int(cfg["audit_seed"]))}
                drop = {n["item_id"] for n in neg} - keep
                items = [it for it in items if it["item_id"] not in drop]
        by_id = {it["item_id"]: it for it in items}

    dev = [it["item_id"] for it in items if it["split"] == "dev"]
    test = [it["item_id"] for it in items if it["split"] == "test"]
    y_dev = np.asarray([feats[i]["label"] for i in dev])
    y_test = np.asarray([feats[i]["label"] for i in test])

    # ---- the gate and its thresholds, dev only ---------------------------------------
    gate = G.fit_logistic_gate(feats, dev)
    s_dev = gate.score(feats, dev)
    s_test = gate.score(feats, test)
    band = G.fit_band_thresholds(s_dev, y_dev)
    single = G.fit_single_threshold(s_dev, y_dev)
    band_matched = G.match_single_to_recall(s_dev, y_dev, band.get("dev_recall", 0.0))

    ref_band_dev = G.refused_band(s_dev, band["t_lo"], band["t_hi"])
    ref_single_dev = G.refused_single(s_dev, single["t"])
    ref_band = G.refused_band(s_test, band["t_lo"], band["t_hi"])
    ref_single = G.refused_single(s_test, single["t"])
    ref_matched = G.refused_single(s_test, band_matched["t"])

    # ---- baselines: same rule, one score each, fitted on dev --------------------------
    baselines = {}
    base_scores = {"B1_bm25_top1": feats, "B2_dense_top1": feats}
    for name, key in (("B1_bm25_top1", "bm25_top1"), ("B2_dense_top1", "dense_top1")):
        sd = np.asarray([feats[i][key] for i in dev])
        st = np.asarray([feats[i][key] for i in test])
        th = G.fit_single_threshold(sd, y_dev)
        baselines[name] = {"threshold": th, "test": G.metrics_block(G.refused_single(st, th["t"]),
                                                                   [by_id[i] for i in test], st, name)}
    reader = G.load_reader()
    if reader and all(i in reader for i in dev + test):
        sd = np.asarray([reader[i] for i in dev])      # lower logprob => less sure => refuse
        st = np.asarray([reader[i] for i in test])
        th = G.fit_single_threshold(sd, y_dev)
        baselines["B4_reader_logprob"] = {
            "threshold": th, "direction": "refuse if logprob < t (lower = less confident)",
            "test": G.metrics_block(G.refused_single(st, th["t"]), [by_id[i] for i in test], st,
                                    "B4_reader_logprob")}
    else:
        baselines["B4_reader_logprob"] = {"status": "NOT RUN",
                                          "reason": "no reader features file (see DATA/reader log)"}

    # ---- EXPLORATORY operating point (PREREGISTRATION.md §10 D1.2) --------------------
    over_cap = float(cfg.get("exploratory_max_over_refusal", 0.10))
    band_x = G.fit_band_constrained(s_dev, y_dev, over_cap)
    single_x = G.fit_single_constrained(s_dev, y_dev, over_cap)
    ref_band_x = G.refused_band(s_test, band_x["t_lo"], band_x["t_hi"])
    ref_single_x = G.refused_single(s_test, single_x["t"])

    # ---- evaluation on the held-out half --------------------------------------------
    test_items = [by_id[i] for i in test]
    blocks = {
        "band_primary": G.metrics_block(ref_band, test_items, s_test, "band_primary"),
        "single_B3": G.metrics_block(ref_single, test_items, s_test, "single_B3_same_features"),
        "single_matched_recall": G.metrics_block(ref_matched, test_items, s_test,
                                                 "single_matched_recall"),
        "exploratory_band": G.metrics_block(ref_band_x, test_items, s_test, "exploratory_band"),
        "exploratory_single": G.metrics_block(ref_single_x, test_items, s_test,
                                              "exploratory_single"),
    }
    from sklearn.metrics import roc_auc_score
    dev_auc = float(roc_auc_score(y_dev, s_dev))
    test_auc = float(roc_auc_score(y_test, s_test))
    discrimination = {"dev_auroc": round(dev_auc, 4), "test_auroc": round(test_auc, 4),
                      "n_dev": len(dev), "n_test": len(test)}

    # ---- hypotheses ------------------------------------------------------------------
    idx = {i: k for k, i in enumerate(test)}
    def paired_ref(rung_a: int, rung_b: int) -> tuple[np.ndarray, np.ndarray, np.ndarray] | None:
        a = {by_id[i]["qid"]: i for i in test if by_id[i]["rung"] == rung_a}
        b = {by_id[i]["qid"]: i for i in test if by_id[i]["rung"] == rung_b}
        qs = sorted(set(a) & set(b))
        if not qs:
            return None
        ra = np.asarray([ref_band[idx[a[q]]] for q in qs], dtype=float)
        rb = np.asarray([ref_band[idx[b[q]]] for q in qs], dtype=float)
        return ra, rb, np.ones(len(qs), dtype=bool)

    h1_pair = paired_ref(1, 3)
    h1 = {}
    if h1_pair is not None:
        ra, rb, mask = h1_pair
        d = ra - rb
        rng = np.random.default_rng(G.BOOT_SEED)
        draws = np.array([d[rng.integers(0, d.size, d.size)].mean() for _ in range(G.N_BOOT)])
        lo, hi = np.percentile(draws, [2.5, 97.5])
        h1 = {"rung1_precision": round(float(ra.mean()), 4), "rung3_precision": round(float(rb.mean()), 4),
              "diff_r1_minus_r3": round(float(d.mean()), 4), "ci95_lo": round(float(lo), 4),
              "ci95_hi": round(float(hi), 4), "n_pairs": int(d.size),
              "sign_test": G.paired_sign(ra, rb, mask),
              "monotone_1_to_4": None, "criterion_points": 15}
        seq = [blocks["band_primary"]["per_rung"][str(r)]["abstain_precision"] for r in (1, 2, 3, 4)
               if str(r) in blocks["band_primary"]["per_rung"]]
        h1["sequence"] = seq
        h1["monotone_1_to_4"] = all(x >= y - 1e-12 for x, y in zip(seq, seq[1:]))
        h1["passes_point_threshold"] = bool(h1["diff_r1_minus_r3"] >= 0.15)
        h1["supported"] = bool(h1["diff_r1_minus_r3"] >= 0.15 and lo > 0 and h1["monotone_1_to_4"])

    neg_dev_mask = np.asarray([by_id[i]["rung"] > 0 for i in dev])
    dev_pooled = round(float(ref_band_dev[neg_dev_mask].mean()), 4)
    h2 = {"dev_pooled_precision": dev_pooled,
          "test_pooled_precision": blocks["band_primary"]["pooled_abstain_precision"],
          "second_corpus": "NOT RUN (2WikiMultihopQA not available in this window; §9.5)"}
    h2["loss_points"] = round(h2["dev_pooled_precision"] - h2["test_pooled_precision"], 4)
    h2["p_value"] = None
    h2["p_note"] = "no test: one side is the fitting half (D1.4)"
    h2["supported"] = bool(h2["loss_points"] >= 0.10)
    h2["refuted"] = bool(abs(h2["loss_points"]) <= 0.05)

    d_h3 = G.boot_precision_diff(ref_band, ref_matched, np.asarray([not by_id[i]["label"] for i in test]),
                                 n_boot=int(cfg.get("n_boot", G.N_BOOT)))
    h3 = {"band_precision": blocks["band_primary"]["pooled_abstain_precision"],
          "matched_single_precision": blocks["single_matched_recall"]["pooled_abstain_precision"],
          "band_dev_recall": band.get("dev_recall"), "matched_threshold": band_matched,
          "difference": d_h3, "criterion_points": 5}
    h3["supported"] = bool(d_h3["diff"] >= 0.05 and not d_h3["contains_zero"])

    seq_x = [blocks["exploratory_band"]["per_rung"][str(r)]["abstain_precision"]
             for r in (1, 2, 3, 4) if str(r) in blocks["exploratory_band"]["per_rung"]]
    h1_x = {"sequence": seq_x,
            "monotone_1_to_4": all(a >= b - 1e-12 for a, b in zip(seq_x, seq_x[1:])),
            "diff_r1_minus_r3": round(seq_x[0] - seq_x[2], 4) if len(seq_x) >= 3 else None,
            "over_refusal": blocks["exploratory_band"]["over_refusal"],
            "coverage": blocks["exploratory_band"]["coverage"],
            "label": "EXPLORATORY (D1.2) - not a pre-registered test"}

    pvals = {}
    if h1:
        pvals["H1"] = float(h1["sign_test"]["p_value"])
    # H2 deliberately carries no p-value (D1.4): one side of the comparison is the fitting half.
    pvals["H3_sign"] = float(G.paired_sign(ref_band, ref_matched,
                                           np.asarray([not by_id[i]["label"] for i in test]))["p_value"])
    correction = G.holm(pvals) if pvals else {}

    # ---- placement diagnostic --------------------------------------------------------
    placement = {
        "dev_score_min": round(float(s_dev.min()), 4), "dev_score_max": round(float(s_dev.max()), 4),
        "dev_score_median": round(float(np.median(s_dev)), 4),
        "t_lo": band["t_lo"], "t_hi": band["t_hi"], "single_t": single["t"],
        "t_lo_inside_dev_range": bool(s_dev.min() <= band["t_lo"] <= s_dev.max()),
        "t_hi_inside_dev_range": bool(s_dev.min() <= band["t_hi"] <= s_dev.max()),
        "single_t_inside_dev_range": bool(s_dev.min() <= single["t"] <= s_dev.max()),
        "dev_admit_mass": round(float(np.mean(~ref_band_dev)), 4),
        "dev_refused_below_lo": round(float(np.mean(s_dev < band["t_lo"])), 4),
        "dev_refused_above_hi": round(float(np.mean(s_dev > band["t_hi"])), 4),
    }

    # ---- predictions ------------------------------------------------------------------
    pred_path = G.RESULTS / "predictions.csv"
    pred_path.parent.mkdir(parents=True, exist_ok=True)
    with open(pred_path, "w", encoding="utf-8", newline="\n") as fh:
        w = csv.writer(fh)
        w.writerow(["item_id", "split", "qid", "rung", "label", "band_score", "band_refused",
                    "single_refused", "matched_refused", "expl_band_refused",
                    "expl_single_refused"])
        for i, it in zip(test, test_items):
            w.writerow([i, it["split"], it["qid"], it["rung"], it["label"],
                        f"{float(s_test[test.index(i)]):.6g}", int(ref_band[test.index(i)]),
                        int(ref_single[test.index(i)]), int(ref_matched[test.index(i)]),
                        int(ref_band_x[test.index(i)]), int(ref_single_x[test.index(i)])])

    # ---- B4 on the dev items that have reader features (dev-only, D1.5) ---------------
    reader_dev_summary = {"status": "NOT RUN"}
    if reader:
        dset = [i for i in dev if i in reader]
        if len(dset) >= 50:
            sd = np.asarray([reader[i] for i in dset])
            yd = np.asarray([feats[i]["label"] for i in dset])
            th = G.fit_single_threshold(sd, yd)
            ref = G.refused_single(sd, th["t"])
            from sklearn.metrics import roc_auc_score
            auc = float(roc_auc_score(yd, sd)) if len(np.unique(yd)) == 2 else float("nan")
            per_rung = {}
            for r in (1, 2, 3, 4):
                m = np.asarray([by_id[i]["rung"] == r for i in dset])
                if m.any():
                    per_rung[str(r)] = {"abstain_precision": round(float(ref[m].mean()), 4),
                                        "n": int(m.sum())}
            reader_dev_summary = {
                "status": "dev-only, exploratory", "n": len(dset),
                "coverage_fraction_of_dev": round(len(dset) / max(1, len(dev)), 4),
                "threshold": th, "auroc_answerable_vs_negatives": round(auc, 4),
                "over_refusal": round(float(ref[yd == 1].mean()), 4) if (yd == 1).any() else None,
                "per_rung_abstain_precision": per_rung,
                "note": "reader = Qwen2.5-0.5B-Instruct, mean generated-token logprob; see "
                        "04_experiments/results/B4_reader_run_notes.md for the failure mode "
                        "(a confident NOT_ANSWERABLE string scores as high confidence)",
            }

    out = {
        "status": "ok",
        "experiment": "c1",
        "preregistration_sha256": (ROOT / "04_experiments" / "PREREGISTRATION.sha256").read_text().split()[0],
        "items": {"n_total": len(items),
                  "n_dev": len(dev), "n_test": len(test),
                  "per_rung_test": {str(r): sum(1 for i in test if by_id[i]["rung"] == r) for r in range(5)},
                  "per_rung_dev": {str(r): sum(1 for i in dev if by_id[i]["rung"] == r) for r in range(5)}},
        "gate": gate.info(),
        "thresholds": {"band": band, "single": single, "single_matched_recall": band_matched},
        "placement_diagnostic": placement,
        "discrimination": discrimination,
        "test": blocks,
        "baselines": baselines,
        "audit": {"dev_all_pass_after_rebuild": rep_dev["all_pass"],
                  "dev_failing_after_rebuild": rep_dev["failing_rungs"],
                  "dev_auroc_primary": {k: v["auroc_primary_6"] for k, v in rep_dev["per_rung"].items()},
                  "dev_auroc_sensitivity_with_lex": {k: v["auroc_with_lex_overlap"]
                                                     for k, v in rep_dev["per_rung"].items()},
                  "test_reference_primary": {k: v["auroc_primary_6"] for k, v in rep_test["per_rung"].items()},
                  "rebuilt_rungs": rep_dev["rebuilt_rungs"]},
        "hypotheses": {"H1": h1, "H2": h2, "H3": h3},
        "exploratory": {"operating_point": {"band": band_x, "single": single_x,
                                            "max_over_refusal": over_cap},
                        "H1_sequence": h1_x},
        "reader_baseline_dev_only": reader_dev_summary,
        "multiple_comparisons": correction,
        "config_seed": seed_used,
    }
    _write_json(G.RESULTS / "results_full.json", out)

    flat = {"status_ok": 1, "n_items": len(items), "test_band_roc_auc": test_auc}
    for r, blk in blocks["band_primary"]["per_rung"].items():
        flat[f"band.precision.r{r}"] = blk["abstain_precision"]
        flat[f"band.auroc.r{r}"] = blk["auroc_answerable_vs_this_rung"]
    for name, blk in baselines.items():
        if "test" in blk:
            flat[f"{name}.pooled_precision"] = blk["test"]["pooled_abstain_precision"]
    for r, blk in blocks["exploratory_band"]["per_rung"].items():
        flat[f"expl_band.precision.r{r}"] = blk["abstain_precision"]
    flat["expl_band.over_refusal"] = blocks["exploratory_band"]["over_refusal"]
    flat["band.over_refusal"] = blocks["band_primary"]["over_refusal"]
    flat["h1.diff_r1_r3"] = h1.get("diff_r1_minus_r3", float("nan"))
    flat["h2.loss_points"] = h2["loss_points"]
    flat["h3.diff"] = d_h3["diff"]
    return {"status": "ok", "metrics": flat}


def main() -> None:
    ap = argparse.ArgumentParser(description="Run the C1 confirmatory experiment.")
    ap.add_argument("--check-repro", type=int, default=0, metavar="N")
    ap.add_argument("--notes", default="")
    a = ap.parse_args()
    cfg = json.loads(CFG.read_text(encoding="utf-8"))

    if a.check_repro:
        res = runner.run(cfg, "c1", analyse, notes=a.notes or "C1 confirmatory run",
                         command=None)
        print(json.dumps({"run_id": res.run_id, "run_dir": str(res.run_dir)},
                         indent=2, sort_keys=True))
        rc = runner.check_repro(cfg, "c1", analyse, n=a.check_repro)
        sys.exit(0 if rc else 1)

    res = runner.run(cfg, "c1", analyse, notes=a.notes or "C1 confirmatory run")
    art = Path(res.run_dir) / "artifacts"
    art.mkdir(parents=True, exist_ok=True)
    for f in ("results_full.json", "audit.json", "predictions.csv"):
        src = G.RESULTS / f
        if src.exists():
            shutil.copy2(src, art / f)
    print(json.dumps({"run_id": res.run_id, "run_dir": str(res.run_dir),
                      "n_metrics": len(res.metrics())}, indent=2, sort_keys=True))
    print(json.dumps(res.metrics(), indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
