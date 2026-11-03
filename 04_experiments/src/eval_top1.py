"""C1 — exploratory 'top-1 presented' variant, stage 3: fit a fresh gate and evaluate (D3).

    python 04_experiments/src/eval_top1.py

Reads `data/items_top1.jsonl` + `data/features_top1.csv`, writes `results/c1/top1_variant.json`.

Why a new gate: this variant's population is retrieval hits and retrieval misses, with label
prevalence equal to the BM25 hit rate (~0.8), not the ladder's 400-positives-to-1,473-negatives. The
frozen gate's intercept and thresholds are calibrated to the old prevalence and do not apply
(PREREGISTRATION.md §10 D3 says so explicitly). So the gate is re-fitted on the dev top-1 items with
exactly the §5 estimator and the §5 threshold rules, and evaluated on the test top-1 items.

Reported, per the task: n and hit rate per split, test AUROC (gold vs non-gold), abstain precision at
both operating points with BCa CIs, over-refusal, coverage, and the refusal rate split by retrieval
hit vs retrieval miss — the last one is the number that decides whether the gate reads retrieval
correctness. Plus the reverse-direction check: AUROC of `dense_presented` alone, and of every other
single feature, so the reader can see what the 12-feature logistic adds over one cosine.

In this population there is one negative class (retrieval misses), so two different numbers both get
called "abstain precision" in the literature and they are not the same:

* `refusal_rate_misses` = P(refused | non-gold) — the task's definition, and what the pre-registered
  files report under that name (PREREGISTRATION §6's parenthetical defines precision as the mean
  refusal indicator over negatives, which is recall);
* `precision_miss_given_refused` = P(non-gold | refused) — the conditional precision a user of the
  gate actually experiences.

Both are reported, with their own intervals; neither is substituted for the other.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "04_experiments" / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import features as F  # noqa: E402
import gate as G  # noqa: E402

DATA = F.DATA
ITEMS_IN = DATA / "items_top1.jsonl"
FEATS_IN = DATA / "features_top1.csv"
OUT = ROOT / "04_experiments" / "results" / "c1" / "top1_variant.json"
TARGET_PRECISION = 0.80
OVER_CAP = 0.10


def load() -> tuple[list[dict], dict[str, dict]]:
    with open(ITEMS_IN, encoding="utf-8") as fh:
        items = [json.loads(line) for line in fh if line.strip()]
    feats = G.load_features(FEATS_IN)
    missing = [it["item_id"] for it in items if it["item_id"] not in feats]
    if missing:
        raise RuntimeError(f"{len(missing)} items have no features: {missing[:3]}")
    for it in items:  # the CSV is the source of truth for labels; they must agree with the items
        if int(feats[it["item_id"]]["label"]) != int(it["label"]):
            raise RuntimeError(f"label mismatch for {it['item_id']}")
    return items, feats


def bca_ratio(num: np.ndarray, den: np.ndarray, n_boot: int = G.N_BOOT,
              seed: int = G.BOOT_SEED) -> dict:
    """BCa interval for a ratio of means sum(num)/sum(den), resampling items.

    Used for P(non-gold | refused), which is a ratio of two item-level indicators and therefore cannot
    be handed to `stats.bootstrap_ci` (whose statistic is a function of one 1-D array).
    """
    num, den = np.asarray(num, float), np.asarray(den, float)
    n = num.size
    if den.sum() == 0:
        return {"lo": None, "hi": None, "n": int(n), "note": "nothing refused; ratio undefined"}
    theta = float(num.sum() / den.sum())
    rng = np.random.default_rng(seed)
    draws = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, n, n)
        d = den[idx].sum()
        draws[b] = num[idx].sum() / d if d > 0 else np.nan
    draws = draws[np.isfinite(draws)]
    if draws.size < 10:
        return {"lo": None, "hi": None, "n": int(n), "note": "too few usable replicates"}

    from statistics import NormalDist
    nd = NormalDist()
    frac_below = float(np.mean(draws < theta))
    frac_below = min(max(frac_below, 1.0 / (draws.size + 1)), 1.0 - 1.0 / (draws.size + 1))
    z0 = nd.inv_cdf(frac_below)

    jack = np.empty(n)  # leave-one-out
    for i in range(n):
        keep = np.ones(n, bool)
        keep[i] = False
        d = den[keep].sum()
        jack[i] = num[keep].sum() / d if d > 0 else np.nan
    jack = jack[np.isfinite(jack)]
    jm = jack.mean()
    num_s = float(np.sum((jm - jack) ** 3))
    den_s = 6.0 * float(np.sum((jm - jack) ** 2)) ** 1.5
    accel = num_s / den_s if den_s > 0 else 0.0

    out = {}
    for name, q in (("lo", 0.025), ("hi", 0.975)):
        z = nd.inv_cdf(q)
        adj = nd.cdf(z0 + (z0 + z) / (1.0 - accel * (z0 + z)))
        out[name] = round(float(np.quantile(draws, adj)), 4)
    out.update({"n": int(n), "n_boot": int(draws.size), "seed": seed, "method": "bca",
                "statistic": "sum(refused & non-gold) / sum(refused)"})
    return out


def rates(ref: np.ndarray, y: np.ndarray) -> dict:
    """Refusal rates with BCa CIs over the items each rate is defined on."""
    miss, hit = y == 0, y == 1
    refused = np.asarray(ref, dtype=bool)
    out = {
        "n_misses": int(miss.sum()), "n_hits": int(hit.sum()),
        "n_refused": int(refused.sum()),
        "n_refused_misses": int((refused & miss).sum()),
        "n_refused_hits": int((refused & hit).sum()),
        # the task's "abstain precision" = P(refused | non-gold) (== abstain recall)
        "refusal_rate_misses": round(float(refused[miss].mean()), 4) if miss.any() else None,
        "refusal_rate_hits": round(float(refused[hit].mean()), 4) if hit.any() else None,
        "over_refusal": round(float(refused[hit].mean()), 4) if hit.any() else None,
        "coverage": round(float(1.0 - refused.mean()), 4),
        # the conditional precision a user experiences
        "precision_miss_given_refused": (round(float((refused & miss).sum() / refused.sum()), 4)
                                         if refused.any() else None),
        "precision_miss_given_refused_ci95": bca_ratio((refused & miss).astype(float),
                                                       refused.astype(float)),
        "refuse_all_precision": round(float(miss.mean()), 4),
    }
    if miss.sum() > 1:
        out["refusal_rate_misses_ci95"] = G.ci_mean(refused[miss].astype(float))
    if hit.sum() > 1:
        out["refusal_rate_hits_ci95"] = G.ci_mean(refused[hit].astype(float))
    out["abstain_precision"] = out["refusal_rate_misses"]
    out["abstain_precision_definition"] = "P(refused | non-gold), i.e. the fraction of retrieval misses refused"
    return out


def verify_inputs(items: list[dict], feats: dict[str, dict]) -> dict:
    """Assert the emitted files against SQuAD and items.jsonl before any number is computed.

    Cheap, and it is the difference between "the hit rate is 0.8550 because I computed it" and "the
    hit rate is 0.8550 because the item file says so and the item file was checked against the corpus".
    """
    import math

    raw = json.loads((DATA / "raw" / "dev-v2.0.json").read_text(encoding="utf-8"))
    gold = {}
    for art in raw["data"]:
        for p in art["paragraphs"]:
            for q in p["qas"]:
                gold[q["id"]] = p["context"]

    base = [json.loads(line) for line in open(DATA / "items.jsonl", encoding="utf-8") if line.strip()]
    checks = {
        "n_items_800": len(items) == 800,
        "all_rung_minus1": all(it["rung"] == -1 for it in items),
        "all_variant_top1": all(it["variant"] == "top1_presented" for it in items),
        "label_equals_is_gold": all(int(it["label"]) == int(it["is_gold"]) for it in items),
        "label_equals_context_is_gold_paragraph": all(
            int(it["label"]) == int(it["context"] == gold[it["qid"]]) for it in items),
        "n_context_chars_matches": all(it["n_context_chars"] == len(it["context"]) for it in items),
        "item_id_format": all(it["item_id"] == f"{it['split']}:{it['qid']}:top1" for it in items),
        "qids_are_the_sampled_rung0_qids": {
            s: {it["qid"] for it in items if it["split"] == s} for s in ("dev", "test")} == {
            s: {it["qid"] for it in base if it["split"] == s and it["rung"] == 0}
            for s in ("dev", "test")},
        "400_per_split": all(sum(1 for it in items if it["split"] == s) == 400
                             for s in ("dev", "test")),
        "feature_rows_800": len(feats) == 800,
        "feature_ids_match": set(feats) == {it["item_id"] for it in items},
        "bm25_rank_log_constant_log1p1": {round(feats[i]["bm25_rank_log"], 9) for i in feats} ==
                                         {round(math.log1p(1), 9)},
        "dense_presented_varies": len({round(feats[i]["dense_presented"], 3) for i in feats}) > 50,
    }
    bad = [k for k, v in checks.items() if not v]
    if bad:
        raise RuntimeError(f"input verification failed: {bad}")
    return {"checks": checks, "all_passed": True,
            "note": "recomputed from data/raw/dev-v2.0.json and data/items.jsonl, not from the builders"}


def main() -> None:
    ap = argparse.ArgumentParser(description="Fit and evaluate the top-1-presented gate (D3).")
    ap.add_argument("--no-write", action="store_true")
    a = ap.parse_args()

    from sklearn.metrics import roc_auc_score

    items, feats = load()
    verification = verify_inputs(items, feats)
    dev = [it["item_id"] for it in items if it["split"] == "dev"]
    test = [it["item_id"] for it in items if it["split"] == "test"]
    by_id = {it["item_id"]: it for it in items}
    y_dev = np.asarray([feats[i]["label"] for i in dev], dtype=int)
    y_test = np.asarray([feats[i]["label"] for i in test], dtype=int)

    # ---- gate + thresholds, dev only ---------------------------------------------------
    gate = G.fit_logistic_gate(feats, dev)
    s_dev, s_test = gate.score(feats, dev), gate.score(feats, test)
    band = G.fit_band_thresholds(s_dev, y_dev)
    band_x = G.fit_band_constrained(s_dev, y_dev, OVER_CAP)
    single = G.fit_single_threshold(s_dev, y_dev)          # reported for context, not a headline
    single_x = G.fit_single_constrained(s_dev, y_dev, OVER_CAP)

    ref_band_dev, ref_band = G.refused_band(s_dev, band["t_lo"], band["t_hi"]), \
        G.refused_band(s_test, band["t_lo"], band["t_hi"])
    ref_bandx_dev, ref_bandx = G.refused_band(s_dev, band_x["t_lo"], band_x["t_hi"]), \
        G.refused_band(s_test, band_x["t_lo"], band_x["t_hi"])
    ref_single = G.refused_single(s_test, single["t"])
    ref_singlex = G.refused_single(s_test, single_x["t"])

    auc_test = float(roc_auc_score(y_test, s_test))
    auc_dev = float(roc_auc_score(y_dev, s_dev))

    # ---- reverse direction: one feature alone -----------------------------------------
    single_auc = {}
    for c in G.GATE_FEATURES:
        vd = np.asarray([feats[i][c] for i in dev], dtype=float)
        vt = np.asarray([feats[i][c] for i in test], dtype=float)
        if np.std(vt) == 0:
            single_auc[c] = {"test_auroc": 0.5, "note": "constant on test; AUROC undefined, 0.5 by convention"}
            continue
        single_auc[c] = {"test_auroc": round(float(roc_auc_score(y_test, vt)), 4),
                         "dev_auroc": round(float(roc_auc_score(y_dev, vd)), 4)}
    single_auc["dense_presented"]["role"] = ("reverse-direction check: AUROC of the raw bge cosine "
                                            "between question and presented passage, no fitting")

    # ---- hit vs miss refusal: the number that matters ---------------------------------
    def split_rates(ref: np.ndarray, y: np.ndarray) -> dict:
        return rates(ref, y)

    # paired view: how many hits and misses does each operating point refuse, and the gap with a CI
    def gap(ref: np.ndarray) -> dict:
        miss, hit = y_test == 0, y_test == 1
        d = float(ref[hit].mean() - ref[miss].mean())
        # item-level bootstrap over the pooled test items, stratified by class (hits and misses are
        # disjoint item sets, so resample each and recompute the difference)
        rng = np.random.default_rng(G.BOOT_SEED)
        hm, mm = ref[hit], ref[miss]
        draws = np.empty(G.N_BOOT)
        for b in range(G.N_BOOT):
            draws[b] = hm[rng.integers(0, hm.size, hm.size)].mean() - \
                mm[rng.integers(0, mm.size, mm.size)].mean()
        lo, hi = np.percentile(draws, [2.5, 97.5])
        return {"hits_minus_misses_refusal": round(d, 4), "ci95_lo": round(float(lo), 4),
                "ci95_hi": round(float(hi), 4), "n_boot": G.N_BOOT, "seed": G.BOOT_SEED,
                "method": "stratified item-level bootstrap (hits and misses resampled separately)"}

    ops = {
        "band_target_precision_0.80": {"thresholds": band, "dev": split_rates(ref_band_dev, y_dev),
                                       "test": split_rates(ref_band, y_test), "test_gap": gap(ref_band)},
        "band_constrained_over_refusal_0.10": {"thresholds": band_x,
                                               "dev": split_rates(ref_bandx_dev, y_dev),
                                               "test": split_rates(ref_bandx, y_test),
                                               "test_gap": gap(ref_bandx)},
        "single_target_precision_0.80": {"thresholds": single, "test": split_rates(ref_single, y_test)},
        "single_constrained_over_refusal_0.10": {"thresholds": single_x,
                                                 "test": split_rates(ref_singlex, y_test)},
    }

    # ---- score distribution diagnostic -------------------------------------------------
    placement = {
        "dev_score_min": round(float(s_dev.min()), 4), "dev_score_max": round(float(s_dev.max()), 4),
        "dev_score_median": round(float(np.median(s_dev)), 4),
        "test_score_min": round(float(s_test.min()), 4), "test_score_max": round(float(s_test.max()), 4),
        "dev_hit_rate": round(float(y_dev.mean()), 4), "test_hit_rate": round(float(y_test.mean()), 4),
        "band_lo_inside_dev_range": bool(s_dev.min() <= band["t_lo"] <= s_dev.max()),
        "band_hi_inside_dev_range": bool(s_dev.min() <= band["t_hi"] <= s_dev.max()),
        "dev_refused_below_lo": round(float(np.mean(s_dev < band["t_lo"])), 4),
        "dev_refused_above_hi": round(float(np.mean(s_dev > band["t_hi"])), 4),
        "n_dev": len(dev), "n_test": len(test),
    }

    meta = json.loads((DATA / "features_top1_meta.json").read_text(encoding="utf-8"))
    out = {
        "experiment": "C1 — exploratory top-1-presented variant",
        "label": "EXPLORATORY (PREREGISTRATION.md §10 D3) — not part of H1/H2/H3",
        "status": "ok",
        "design": {
            "variant": "top1_presented", "rung": -1,
            "presented_passage": "BM25 rank-1 paragraph for the question, from the item's own split pool",
            "label_rule": "1 iff the rank-1 paragraph is the question's gold paragraph (hit) else 0 (miss)",
            "gate": "logistic regression, L2 C=1.0, lbfgs, max_iter=1000, standardised on dev — same §5 estimator",
            "thresholds": "gate.fit_band_thresholds (target dev abstain precision 0.80) and "
                          "gate.fit_band_constrained (dev over-refusal cap 0.10); fitted on dev only",
            "why_new_gate": "different item population and label prevalence; the frozen gate does not apply (D3)",
            "statistics": f"BCa bootstrap, {G.N_BOOT} resamples, BOOT_SEED={G.BOOT_SEED}, item-level",
        },
        "items": {
            "n_items_total": len(items),
            "per_split": {s: {k: meta["items"][s][k] for k in
                              ("n_items", "n_hits", "n_misses", "hit_rate", "pool_size",
                               "gold_rank_median", "gold_rank_leq5", "gold_rank_leq10",
                               "mean_n_context_chars")}
                          for s in ("dev", "test")},
            "hit_rate_definition": "fraction of the 400 sampled questions per split whose BM25 rank-1 "
                                   "paragraph is the gold paragraph",
            "items_sha256": meta.get("items_sha256"),
        },
        "features": {
            "n_features": len(G.GATE_FEATURES), "features": list(G.GATE_FEATURES),
            "csv_sha256": meta.get("features", {}).get("csv_sha256"),
            "constant_by_construction": meta.get("features", {}).get("constant_by_construction"),
            "dense_math": meta.get("features", {}).get("dense_math"),
            "frozen_dense_columns_are_degenerate": meta.get("features", {}).get(
                "frozen_dense_columns_are_degenerate"),
            "consistency_check_vs_frozen_rung0": meta.get("features", {}).get(
                "consistency_check_vs_frozen_rung0"),
        },
        "gate": gate.info(),
        "auroc": {"test_gate_auroc": round(auc_test, 4), "dev_gate_auroc": round(auc_dev, 4),
                  "definition": "P(score_hit > score_miss), gold vs non-gold, test items"},
        "single_feature_auroc": single_auc,
        "operating_points": ops,
        "placement_diagnostic": placement,
        "verification": verification,
    }

    if not a.no_write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(out, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")

    print(json.dumps({
        "hit_rate": {s: out["items"]["per_split"][s]["hit_rate"] for s in ("dev", "test")},
        "test_auroc": out["auroc"]["test_gate_auroc"],
        "band_0.80": {k: ops["band_target_precision_0.80"]["test"][k]
                      for k in ("n_refused", "n_refused_misses", "n_refused_hits",
                                "abstain_precision", "precision_miss_given_refused",
                                "refusal_rate_misses", "refusal_rate_hits", "coverage",
                                "over_refusal", "refuse_all_precision")},
        "band_0.80_ci": ops["band_target_precision_0.80"]["test"].get("refusal_rate_misses_ci95"),
        "band_0.80_precision_ci": ops["band_target_precision_0.80"]["test"].get(
            "precision_miss_given_refused_ci95"),
        "band_0.10": {k: ops["band_constrained_over_refusal_0.10"]["test"][k]
                      for k in ("n_refused", "n_refused_misses", "n_refused_hits",
                                "abstain_precision", "precision_miss_given_refused",
                                "refusal_rate_misses", "refusal_rate_hits", "coverage",
                                "over_refusal")},
        "band_0.10_ci": ops["band_constrained_over_refusal_0.10"]["test"].get("refusal_rate_misses_ci95"),
        "band_0.10_precision_ci": ops["band_constrained_over_refusal_0.10"]["test"].get(
            "precision_miss_given_refused_ci95"),
        "dev_at_band": {k: ops["band_target_precision_0.80"]["dev"][k]
                        for k in ("abstain_precision", "precision_miss_given_refused",
                                  "refusal_rate_hits", "coverage")},
        "thresholds": {"band": ops["band_target_precision_0.80"]["thresholds"],
                       "band_x": ops["band_constrained_over_refusal_0.10"]["thresholds"]},
        "operating_points_identical": (
            ops["band_target_precision_0.80"]["thresholds"]["t_lo"],
            ops["band_target_precision_0.80"]["thresholds"]["t_hi"]) == (
            ops["band_constrained_over_refusal_0.10"]["thresholds"]["t_lo"],
            ops["band_constrained_over_refusal_0.10"]["thresholds"]["t_hi"]),
        "dense_presented_auroc": single_auc["dense_presented"],
        "placement": placement,
    }, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
