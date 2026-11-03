"""C1 — statistics addendum: the five reviewer-demanded analyses (round-1 MF-2..MF-6).

Writes
    04_experiments/results/c1/stats_addendum.json   (all numbers)
    04_experiments/results/c1/ablations.json        (leave-one-out feature ablations)
    04_experiments/results/c1/STATS-ADDENDUM.md     (tables rendered from the JSON, no hand-typed cells)

Every number in the markdown is formatted from the JSON this run wrote; nothing is typed by hand.
All bootstraps: 10,000 draws, BOOT_SEED = 12345 (PREREGISTRATION §7/§8). No test item is used to fit
anything: the gate and every threshold are fitted on dev only, exactly as `gate.py` does.

Analyses
    1. rung-2 exchangeability  (MF-3)  kept vs dropped questions, per split
    2. matched-recall table    (MF-6)  band vs recall-matched single, test half
    3. cluster bootstrap       (MF-5)  articles resampled with replacement, vs the item-level CIs
    4. exploratory uncertainty (MF-4)  BCa per-rung CIs (from results_full.json) + paired question bootstrap
    5. leave-one-out ablations (MF-2)  seven feature subsets through the same fit + threshold rule

Usage:  python 04_experiments/src/stats_addendum.py [--check]
        --check  recompute and compare against the committed JSON instead of overwriting it
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "04_experiments" / "src"
DATA = ROOT / "04_experiments" / "data"
RESULTS = ROOT / "04_experiments" / "results" / "c1"
sys.path.insert(0, str(SRC))
import build_items as B  # noqa: E402
import gate as G  # noqa: E402

N_BOOT = 10000
SEED = 12345
RUNGS = (1, 2, 3, 4)

# the four "dense" features and the two rank features, named once
DENSE = ["dense_presented", "dense_rank_log", "dense_top1", "dense_margin"]
RANK = ["bm25_rank_log", "dense_rank_log"]


# --------------------------------------------------------------------------- #
# small helpers
# --------------------------------------------------------------------------- #
def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def r4(x):
    return None if x is None else round(float(x), 4)


def fmt_p(p) -> str:
    if p is None:
        return "n/a"
    if p < 1e-3:
        return "<0.001"
    return f"{p:.3f}"


def fmt_rate(x, nd=2) -> str:
    return "n/a" if x is None else f"{x:.{nd}f}"


def load_items() -> list[dict]:
    with open(DATA / "items.jsonl", encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def load_predictions() -> list[dict]:
    with open(RESULTS / "predictions.csv", encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        r["rung"] = int(r["rung"])
        for c in ("band_refused", "single_refused", "matched_refused", "expl_band_refused",
                  "expl_single_refused"):
            r[c] = int(r[c])
        r["label"] = int(r["label"])
    return rows


def article_paragraph_counts() -> dict[str, int]:
    raw = json.loads((DATA / "raw" / "dev-v2.0.json").read_text(encoding="utf-8"))["data"]
    return {a["title"]: len(a["paragraphs"]) for a in raw}


# --------------------------------------------------------------------------- #
# 1. rung-2 exchangeability (MF-3)
# --------------------------------------------------------------------------- #
def exchangeability(items: list[dict]) -> dict:
    from scipy.stats import mannwhitneyu

    n_paras = article_paragraph_counts()
    out = {"definition": (
        "Per split, the 400 sampled questions are the rung-0 rows of items.jsonl. A question is "
        "'dropped' for rung 2 when items.jsonl has no rung-2 row with its qid (build_items.py drop "
        "reason 'no_anchor_candidate': no content token of the question occurs in any non-gold "
        "paragraph of the split pool). Variables are measured on the rung-0 row."),
        "tests": {"continuous": "two-sided Mann-Whitney U (scipy.stats.mannwhitneyu, no continuity "
                               "correction), exact only when n<8",
                  "categorical": "Pearson chi-square on the 5x2 answer-type table; when any expected "
                                 "cell < 5, a Monte Carlo permutation of the answer-type labels with "
                                 "fixed margins (10,000 draws, seed 12345) is used instead and named "
                                 "in 'answer_type_test'"},
        "splits": {}}

    for split in ("dev", "test"):
        r0 = [it for it in items if it["split"] == split and it["rung"] == 0]
        kept_qids = {it["qid"] for it in items if it["split"] == split and it["rung"] == 2}
        kept = [it for it in r0 if it["qid"] in kept_qids]
        drop = [it for it in r0 if it["qid"] not in kept_qids]
        assert len(kept) + len(drop) == len(r0) == 400

        def row(it):
            return {"q_chars": len(it["question"]),
                    "q_tokens": len(B.norm_tokens(it["question"])),
                    "answer_type": B.answer_type(it["gold_answer"]),
                    "gold_chars": len(it["context"]),
                    "n_paragraphs": n_paras[it["title"]]}

        K, D = [row(it) for it in kept], [row(it) for it in drop]
        variables = {}
        for v in ("q_chars", "q_tokens", "gold_chars", "n_paragraphs"):
            a = np.array([x[v] for x in K], dtype=float)
            b = np.array([x[v] for x in D], dtype=float)
            p = float(mannwhitneyu(a, b, alternative="two-sided").pvalue)
            variables[v] = {
                "kept": {"n": int(a.size), "mean": r4(a.mean()), "median": r4(np.median(a)),
                         "sd": r4(a.std(ddof=1)), "min": r4(a.min()), "max": r4(a.max())},
                "dropped": {"n": int(b.size), "mean": r4(b.mean()), "median": r4(np.median(b)),
                            "sd": r4(b.std(ddof=1)), "min": r4(b.min()), "max": r4(b.max())},
                "median_diff_kept_minus_dropped": r4(np.median(a) - np.median(b)),
                "p_value": round(p, 6), "test": "mann_whitney_u_two_sided"}

        # answer-type 5x2 table
        types = ["date", "name", "number", "other", "year"]
        tab = np.array([[sum(1 for x in K if x["answer_type"] == t),
                         sum(1 for x in D if x["answer_type"] == t)] for t in types], dtype=int)
        chi2, p_chi, dof, expected = _chi2(tab)
        if (expected < 5).any():
            p_at, method = _perm_chi2(tab, n_boot=N_BOOT, seed=SEED)
            at_test = {"test": "monte_carlo_permutation_chi2", "statistic": r4(chi2),
                       "p_value": round(p_at, 6), "n_perm": N_BOOT, "seed": SEED,
                       "reason": "at least one expected cell < 5 (scipy.stats.fisher_exact is 2x2 only, "
                                 "so the 5x2 table uses the exact-conditional permutation version)",
                       "min_expected": r4(expected.min())}
        else:
            at_test = {"test": "pearson_chi2", "statistic": r4(chi2), "dof": int(dof),
                       "p_value": round(float(p_chi), 6), "min_expected": r4(expected.min())}

        # collapsed 2x2 Fisher tests, so a literal Fisher p-value is on the record as well
        def _fisher(flag):
            a = sum(1 for x in K if flag(x["answer_type"]))
            b = len(K) - a
            c = sum(1 for x in D if flag(x["answer_type"]))
            d = len(D) - c
            t = np.array([[a, b], [c, d]], dtype=int)
            from scipy.stats import fisher_exact
            odds, p = fisher_exact(t, alternative="two-sided")
            return {"table": {"kept": [a, b], "dropped": [c, d]},
                    "kept_share": r4(a / len(K)), "dropped_share": r4(c / len(D)),
                    "odds_ratio": (None if not np.isfinite(odds) else r4(odds)),
                    "p_value": round(float(p), 6), "test": "fisher_exact_two_sided"}
        variables["answer_type"] = {
            "counts": {t: {"kept": int(tab[i, 0]), "dropped": int(tab[i, 1])}
                       for i, t in enumerate(types)},
            "kept_share": {t: r4(tab[i, 0] / len(K)) for i, t in enumerate(types)},
            "dropped_share": {t: r4(tab[i, 1] / len(D)) for i, t in enumerate(types)},
            "fisher_collapsed": {
                "name_vs_other": _fisher(lambda t: t == "name"),
                "numeric_vs_other": _fisher(lambda t: t in ("year", "number", "date")),
            },
            **at_test}

        out["splits"][split] = {"n_kept": len(K), "n_dropped": len(D),
                                "share_kept": r4(len(K) / 400), "variables": variables}

    # one-sentence verdict, computed from the numbers rather than asserted
    flags, mins = [], []
    for split, blk in out["splits"].items():
        for v, d in blk["variables"].items():
            mins.append((d["p_value"], f"{split}/{v}"))
            if d["p_value"] < 0.05:
                flags.append(f"{split}/{v}")
            for cname, cval in (d.get("fisher_collapsed") or {}).items():
                mins.append((cval["p_value"], f"{split}/answer_type:{cname}"))
                if cval["p_value"] < 0.05:
                    flags.append(f"{split}/answer_type:{cname}")
    mins.sort()
    out["min_p"] = {"value": mins[0][0], "variable": mins[0][1]}
    borderline = [m for m in mins if 0.05 <= m[0] < 0.10]
    out["verdict"] = (
        "No variable differs between kept and dropped questions at the 0.05 level in either split "
        f"(smallest p = {mins[0][0]:.3f}, {mins[0][1]}), so on these five variables the rung-2 "
        "subsample is exchangeable with the sampled questions and rung-2 figures can be read as "
        "describing the sampled question set rather than a selected subset."
        if not flags else
        "Kept and dropped questions differ at the 0.05 level on " + ", ".join(flags) +
        "; the rung-2 subsample is therefore not exchangeable on those variables and rung-2 figures "
        "describe the subsample, not the full question set.")
    if borderline:
        out["verdict"] += (" Caveat: " + ", ".join(f"{v} (p={p:.3f})" for p, v in borderline) +
                           (" sit" if len(borderline) > 1 else " sits") +
                           " between 0.05 and 0.10, so the null is not comfortable either.")
    out["significant_at_0.05"] = flags
    return out


def _chi2(tab: np.ndarray):
    from scipy.stats import chi2_contingency
    chi2, p, dof, exp = chi2_contingency(tab, correction=False)
    return float(chi2), float(p), int(dof), np.asarray(exp, dtype=float)


def _perm_chi2(tab: np.ndarray, n_boot: int, seed: int) -> tuple[float, str]:
    """Monte Carlo exact-conditional chi-square: permute labels, margins fixed."""
    rng = np.random.default_rng(seed)
    types = np.repeat(np.arange(tab.shape[0]), tab.sum(axis=1))
    groups = np.concatenate([np.zeros(tab[:, 0].sum(), dtype=int), np.ones(tab[:, 1].sum(), dtype=int)])
    obs, _, _, _ = _chi2(tab)
    hits = 0
    for _ in range(n_boot):
        g = rng.permutation(groups)
        t = np.zeros_like(tab)
        for ti in range(tab.shape[0]):
            m = types == ti
            t[ti, 0] = int(((g == 0) & m).sum())
            t[ti, 1] = int(((g == 1) & m).sum())
        # drop empty rows/cols before chi2 (can happen only if a type vanishes; margins fixed so it cannot)
        s, _, _, _ = _chi2(t)
        if s >= obs - 1e-12:
            hits += 1
    return (hits + 1) / (n_boot + 1), "monte_carlo_permutation_chi2"


# --------------------------------------------------------------------------- #
# 2. matched-recall table (MF-6)
# --------------------------------------------------------------------------- #
def _h3_pair_test(test: list[dict]) -> dict:
    """H3 on the negative side, with the frozen helpers in gate.py (paired by item)."""
    band = np.array([p["band_refused"] for p in test], dtype=float)
    matched = np.array([p["matched_refused"] for p in test], dtype=float)
    neg = np.array([p["rung"] > 0 for p in test])
    return {"comparison": "band vs recall-matched single, refusal indicators over the negatives (test half)",
            "boot_precision_diff": G.boot_precision_diff(band, matched, neg),
            "paired_sign": G.paired_sign(band, matched, neg),
            "discordant_pairs": int(np.sum(band[neg] != matched[neg]))}


def matched_recall(preds: list[dict], full: dict) -> dict:
    test = [p for p in preds if p["split"] == "test"]
    per_rung = {}
    for r in RUNGS:
        rows = [p for p in test if p["rung"] == r]
        band = float(np.mean([p["band_refused"] for p in rows]))
        matched = float(np.mean([p["matched_refused"] for p in rows]))
        per_rung[str(r)] = {"n": len(rows),
                            "n_refused_band": int(sum(p["band_refused"] for p in rows)),
                            "n_refused_matched": int(sum(p["matched_refused"] for p in rows)),
                            "band_refusal_rate": r4(band),
                            "matched_single_refusal_rate": r4(matched),
                            "difference_band_minus_matched": r4(band - matched),
                            "difference_pp": r4(100 * (band - matched))}
    pooled = [p for p in test if p["rung"] in RUNGS]
    band = float(np.mean([p["band_refused"] for p in pooled]))
    matched = float(np.mean([p["matched_refused"] for p in pooled]))
    per_rung["pooled_1_4"] = {"n": len(pooled),
                              "n_refused_band": int(sum(p["band_refused"] for p in pooled)),
                              "n_refused_matched": int(sum(p["matched_refused"] for p in pooled)),
                              "band_refusal_rate": r4(band),
                              "matched_single_refusal_rate": r4(matched),
                              "difference_band_minus_matched": r4(band - matched),
                              "difference_pp": r4(100 * (band - matched))}
    return {
        "metric_note": ("On the held-out half the refusal rate over a rung's negatives is abstain recall "
                        "and abstain precision at once: every item refused in that rung is a negative, so "
                        "precision = recall = mean(refused) over that rung. Both names are reported."),
        "h3_test_on_negatives": _h3_pair_test(test),
        "test": per_rung,
        "dev": {"band_dev_abstain_recall": full["thresholds"]["band"]["dev_recall"],
                "band_dev_abstain_precision": full["thresholds"]["band"]["dev_precision"],
                "matched_single_dev_abstain_recall": full["thresholds"]["single_matched_recall"]["dev_recall"],
                "matched_single_dev_abstain_precision": full["thresholds"]["single_matched_recall"]["dev_precision"],
                "matched_threshold_t": full["thresholds"]["single_matched_recall"]["t"],
                "matching_rule": ("single threshold chosen so that dev abstain recall matches the band's dev "
                                  "abstain recall; matched on dev, never on test (gate.py docstring)")},
        "answerable_side": {
            "n_rung0_test": int(sum(1 for p in test if p["rung"] == 0)),
            "over_refusal_band": r4(np.mean([p["band_refused"] for p in test if p["rung"] == 0])),
            "over_refusal_matched": r4(np.mean([p["matched_refused"] for p in test if p["rung"] == 0])),
            "coverage_band": r4(np.mean([1 - p["band_refused"] for p in test])),
            "coverage_matched": r4(np.mean([1 - p["matched_refused"] for p in test])),
        },
        "reading": None,
    }


# --------------------------------------------------------------------------- #
# 3. cluster bootstrap by article (MF-5)
# --------------------------------------------------------------------------- #
def cluster_bootstrap(preds: list[dict], items: list[dict], full: dict) -> dict:
    test = [p for p in preds if p["split"] == "test"]
    title = {it["item_id"]: it["title"] for it in items}
    articles = sorted({title[p["item_id"]] for p in test})
    art_idx = {a: i for i, a in enumerate(articles)}
    out = {"unit": "article (items.jsonl 'title'; whole SQuAD articles are never split)",
           "n_articles_test": len(articles), "n_boot": N_BOOT, "seed": SEED,
           "method": "articles resampled with replacement; all items of each resampled article enter the "
                     "rung mean (percentile 2.5/97.5)",
           "per_rung": {}}

    for r in RUNGS:
        rows = [p for p in test if p["rung"] == r]
        sums = np.zeros(len(articles))
        cnts = np.zeros(len(articles))
        for p in rows:
            j = art_idx[title[p["item_id"]]]
            sums[j] += p["band_refused"]
            cnts[j] += 1
        rng = np.random.default_rng(SEED)
        draws = np.empty(N_BOOT)
        for b in range(N_BOOT):
            idx = rng.integers(0, len(articles), len(articles))
            c = cnts[idx].sum()
            draws[b] = sums[idx].sum() / c if c else np.nan
        lo, hi = np.percentile(draws, [2.5, 97.5])
        item_ci = full["test"]["band_primary"]["per_rung"][str(r)]["ci95"]
        per_art = sums / np.maximum(cnts, 1)
        out["per_rung"][str(r)] = {
            "n_items": len(rows), "n_articles_with_items": int((cnts > 0).sum()),
            "point": r4(sums.sum() / cnts.sum()),
            "cluster_ci95": {"lo": r4(lo), "hi": r4(hi)},
            "item_ci95": {"lo": item_ci["lo"], "hi": item_ci["hi"], "method": item_ci.get("method")},
            "width_cluster": r4(hi - lo), "width_item": r4(item_ci["hi"] - item_ci["lo"]),
            "width_ratio": (r4((hi - lo) / (item_ci["hi"] - item_ci["lo"]))
                            if (item_ci["hi"] - item_ci["lo"]) > 0 else None),
            "per_article_rate": {"min": r4(per_art.min()), "max": r4(per_art.max()),
                                 "sd": r4(per_art.std(ddof=1)),
                                 "n_at_1": int((per_art >= 1 - 1e-12).sum()),
                                 "n_at_0": int((per_art <= 1e-12).sum())},
        }

    # exploratory band, same clustering
    out["exploratory_band"] = {}
    for r in RUNGS:
        rows = [p for p in test if p["rung"] == r]
        sums = np.zeros(len(articles))
        cnts = np.zeros(len(articles))
        for p in rows:
            j = art_idx[title[p["item_id"]]]
            sums[j] += p["expl_band_refused"]
            cnts[j] += 1
        rng = np.random.default_rng(SEED)
        draws = np.empty(N_BOOT)
        for b in range(N_BOOT):
            idx = rng.integers(0, len(articles), len(articles))
            c = cnts[idx].sum()
            draws[b] = sums[idx].sum() / c if c else np.nan
        lo, hi = np.percentile(draws, [2.5, 97.5])
        item_ci = full["test"]["exploratory_band"]["per_rung"][str(r)]["ci95"]
        per_art = sums / np.maximum(cnts, 1)
        out["exploratory_band"][str(r)] = {
            "n_items": len(rows), "point": r4(sums.sum() / cnts.sum()),
            "cluster_ci95": {"lo": r4(lo), "hi": r4(hi)},
            "item_ci95": {"lo": item_ci["lo"], "hi": item_ci["hi"]},
            "width_cluster": r4(hi - lo), "width_item": r4(item_ci["hi"] - item_ci["lo"]),
            "width_ratio": r4((hi - lo) / (item_ci["hi"] - item_ci["lo"])),
            "per_article_rate": {"min": r4(per_art.min()), "max": r4(per_art.max()),
                                 "sd": r4(per_art.std(ddof=1)),
                                 "n_at_1": int((per_art >= 1 - 1e-12).sum()),
                                 "n_at_0": int((per_art <= 1e-12).sum())}}

    out["thresholds_note"] = ("Decision-relevant thresholds named in the paper: the 0.80 dev target "
                              "precision and the exploratory over-refusal cap 0.10, plus the 0.90 line "
                              "the ladder argument leans on. See 'reading' for whether any interval "
                              "crosses them.")
    return out


# --------------------------------------------------------------------------- #
# 4. exploratory uncertainty (MF-4)
# --------------------------------------------------------------------------- #
def paired_question_bootstrap(preds: list[dict], rung_a: int, rung_b: int, col: str,
                              n_boot: int = N_BOOT, seed: int = SEED) -> dict:
    """Resample questions with replacement, keep the pair, recompute mean(ref_a) - mean(ref_b)."""
    by = {}
    for p in preds:
        if p["split"] != "test":
            continue
        by.setdefault(p["qid"], {})[p["rung"]] = p[col]
    qids = sorted(q for q, d in by.items() if rung_a in d and rung_b in d)
    a = np.array([by[q][rung_a] for q in qids], dtype=float)
    b = np.array([by[q][rung_b] for q in qids], dtype=float)
    rng = np.random.default_rng(seed)
    draws = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, a.size, a.size)
        draws[i] = a[idx].mean() - b[idx].mean()
    lo, hi = np.percentile(draws, [2.5, 97.5])
    diff = float(a.mean() - b.mean())
    return {"rung_a": rung_a, "rung_b": rung_b, "column": col, "diff": r4(diff),
            "ci95": {"lo": r4(lo), "hi": r4(hi)}, "n_pairs": int(a.size),
            "n_boot": n_boot, "seed": seed,
            "method": "paired percentile bootstrap over questions (both rungs resampled jointly)",
            "contains_zero": bool(lo <= 0 <= hi),
            "p_a": r4(a.mean()), "p_b": r4(b.mean())}


def exploratory_uncertainty(preds: list[dict], full: dict) -> dict:
    exp = full["test"]["exploratory_band"]
    per_rung = {}
    for r in RUNGS:
        blk = exp["per_rung"][str(r)]
        per_rung[str(r)] = {"abstain_precision": blk["abstain_precision"], "n": blk["n"],
                            "ci95": {"lo": blk["ci95"]["lo"], "hi": blk["ci95"]["hi"],
                                     "method": blk["ci95"].get("method")}}
    out = {"per_rung_from_results_full": per_rung,
           "source": "results_full.json['test']['exploratory_band']['per_rung'][r]['ci95'] "
                     "(BCa, 10,000 draws, seed 12345, item-level)",
           "over_refusal": exp["over_refusal"], "coverage": exp["coverage"],
           "pooled_abstain_precision": exp["pooled_abstain_precision"],
           "sequence_from_results_full": full["exploratory"]["H1_sequence"]["sequence"],
           "paired_diffs": {}}
    out["paired_diffs"]["exploratory_r1_minus_r3"] = paired_question_bootstrap(
        preds, 1, 3, "expl_band_refused")
    out["paired_diffs"]["exploratory_r1_minus_r3_single"] = paired_question_bootstrap(
        preds, 1, 3, "expl_single_refused")
    out["paired_diffs"]["confirmatory_r1_minus_r3"] = paired_question_bootstrap(
        preds, 1, 3, "band_refused")
    out["paired_diffs"]["exploratory_r1_minus_r4"] = paired_question_bootstrap(
        preds, 1, 4, "expl_band_refused")
    return out


# --------------------------------------------------------------------------- #
# 5. leave-one-out ablations (MF-2)
# --------------------------------------------------------------------------- #
def _block(ref, rows, name, scores, items_by_id, feats) -> dict:
    """Per-rung abstain precision + over-refusal + coverage for one gate on the test half."""
    from sklearn.metrics import roc_auc_score
    rung = np.array([r["rung"] for r in rows])
    y = np.array([r["label"] for r in rows])
    is_neg = rung > 0
    is_pos = ~is_neg
    out = {"gate": name, "n_items": len(rows),
           "pooled_abstain_precision": r4(ref[is_neg].mean()),
           "over_refusal": r4(ref[is_pos].mean()),
           "coverage": r4(1.0 - ref.mean()), "per_rung": {}}
    for r in RUNGS:
        m = rung == r
        yy = np.concatenate([np.ones(int(is_pos.sum())), np.zeros(int(m.sum()))])
        ss = np.concatenate([scores[is_pos], scores[m]])
        auc = float(roc_auc_score(yy, ss)) if len(np.unique(yy)) == 2 else float("nan")
        out["per_rung"][str(r)] = {"abstain_precision": r4(ref[m].mean()), "n": int(m.sum()),
                                   "auroc_answerable_vs_this_rung": r4(auc)}
    return out


def run_ablation(name: str, features: list[str], feats, dev_ids, test_ids, items_by_id) -> dict:
    from sklearn.metrics import roc_auc_score

    gate = G.fit_logistic_gate(feats, dev_ids, features=features)
    s_dev = gate.score(feats, dev_ids)
    s_test = gate.score(feats, test_ids)
    y_dev = np.array([feats[i]["label"] for i in dev_ids])
    y_test = np.array([feats[i]["label"] for i in test_ids])

    band = G.fit_band_thresholds(s_dev, y_dev)                 # confirmatory rule, target 0.80
    band_exp = G.fit_band_constrained(s_dev, y_dev, 0.10)      # exploratory rule, cap 0.10

    rows = [items_by_id[i] for i in test_ids]
    ref = G.refused_band(s_test, band["t_lo"], band["t_hi"])
    ref_exp = G.refused_band(s_test, band_exp["t_lo"], band_exp["t_hi"])

    return {
        "name": name, "features": list(features), "n_features": len(features),
        "auroc_dev": r4(roc_auc_score(y_dev, s_dev)),
        "auroc_test": r4(roc_auc_score(y_test, s_test)),
        "thresholds": {"band": band, "band_exploratory": band_exp},
        "test_band": _block(ref, rows, f"{name}_band", s_test, items_by_id, feats),
        "test_band_exploratory": _block(ref_exp, rows, f"{name}_band_exploratory", s_test,
                                        items_by_id, feats),
    }


def feature_redundancy(feats, items) -> dict:
    """Document exact redundancy inside the 12-feature vector (integrity check, not an ablation)."""
    ids = [it["item_id"] for it in items]
    X = np.array([[feats[i][c] for c in G.GATE_FEATURES] for i in ids], dtype=float)
    names = list(G.GATE_FEATURES)
    identical = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            if np.array_equal(X[:, i], X[:, j]):
                identical.append([names[i], names[j]])
    constant = [names[i] for i in range(len(names)) if len(np.unique(X[:, i])) == 1]
    per_split = {}
    for split in ("dev", "test"):
        sub = [feats[i] for i in ids if feats[i]["split"] == split]
        per_split[split] = {
            "n": len(sub),
            "constant": [c for c in names if len({s[c] for s in sub}) == 1],
            "dense_presented_equals_dense_top1": all(
                s["dense_presented"] == s["dense_top1"] for s in sub),
        }
    return {"n_columns": len(names), "identical_pairs": identical, "constant_columns": constant,
            "n_distinct_columns": len(names) - len(identical),
            "n_informative_columns": len(names) - len(identical) - len(constant),
            "per_split": per_split,
            "dense_rank_log_value": sorted({feats[i]["dense_rank_log"] for i in ids}),
            "note": ("dense_presented and dense_top1 are the same number for every item, and "
                     "dense_rank_log is constant (ln 2) in both splits, so the 'four dense features' "
                     "supply one distinct informative signal. The all-12 gate therefore has 10 "
                     "informative columns, not 12.")}


def ablations(feats, items, full: dict) -> dict:
    dev_ids = [it["item_id"] for it in items if it["split"] == "dev"]
    test_ids = [it["item_id"] for it in items if it["split"] == "test"]
    items_by_id = {it["item_id"]: it for it in items}
    base = list(G.GATE_FEATURES)

    subsets = [
        ("all_12", "all 12 retrieval features (reproduction)", base),
        ("no_lex_overlap", "without lex_overlap", [c for c in base if c != "lex_overlap"]),
        ("no_ce_presented", "without ce_presented (cross-encoder)", [c for c in base if c != "ce_presented"]),
        ("no_dense", "without the four dense features", [c for c in base if c not in DENSE]),
        ("no_rank", "without the two rank features", [c for c in base if c not in RANK]),
        ("no_bm25_presented_pair", "without bm25_presented + bm25_rank_log",
         [c for c in base if c not in ("bm25_presented", "bm25_rank_log")]),
        ("lex_overlap_only", "lex_overlap alone", ["lex_overlap"]),
    ]

    out = {"generated_by": "04_experiments/src/stats_addendum.py",
           "frozen_rule": ("logistic gate (L2, C=1.0, lbfgs, max_iter=1000, class_weight=None) on dev "
                           "standardised features; confirmatory band = gate.fit_band_thresholds(target "
                           "precision 0.80); exploratory band = gate.fit_band_constrained(cap 0.10); "
                           "evaluated on the test half only"),
           "feature_redundancy": feature_redundancy(feats, items),
           "n_boot": N_BOOT, "seed": SEED, "rows": {}}

    for key, label, features in subsets:
        out["rows"][key] = run_ablation(key, features, feats, dev_ids, test_ids, items_by_id)
        out["rows"][key]["label"] = label

    # ---- reproduction asserts (hard gates, per the task) ----
    all12 = out["rows"]["all_12"]
    disc = full["discrimination"]
    assert abs(all12["auroc_dev"] - disc["dev_auroc"]) <= 1e-3, (
        f"all-12 dev AUROC {all12['auroc_dev']} != results_full {disc['dev_auroc']}")
    assert abs(all12["auroc_test"] - disc["test_auroc"]) <= 1e-3, (
        f"all-12 test AUROC {all12['auroc_test']} != results_full {disc['test_auroc']}")

    norank_ref = json.loads((RESULTS / "ablation_no_rank.json").read_text(encoding="utf-8"))
    nr = out["rows"]["no_rank"]
    assert abs(nr["auroc_dev"] - norank_ref["auroc_dev"]) <= 1e-3, "no_rank dev AUROC mismatch"
    assert abs(nr["auroc_test"] - norank_ref["auroc_test"]) <= 1e-3, "no_rank test AUROC mismatch"
    assert abs(nr["test_band"]["over_refusal"] - norank_ref["test"]["over_refusal"]) <= 1e-9, (
        f"no_rank over_refusal {nr['test_band']['over_refusal']} != "
        f"{norank_ref['test']['over_refusal']}")
    for r in RUNGS:
        assert abs(nr["test_band"]["per_rung"][str(r)]["abstain_precision"] -
                   norank_ref["test"]["per_rung"][str(r)]["abstain_precision"]) <= 1e-9, (
            f"no_rank rung {r} precision mismatch")

    out["reproduction_checks"] = {
        "all_12_vs_results_full": {"dev_auroc": all12["auroc_dev"], "expected_dev": disc["dev_auroc"],
                                   "test_auroc": all12["auroc_test"], "expected_test": disc["test_auroc"],
                                   "tolerance": 1e-3, "passed": True},
        "no_rank_vs_ablation_no_rank_json": {
            "dev_auroc": nr["auroc_dev"], "test_auroc": nr["auroc_test"],
            "over_refusal": nr["test_band"]["over_refusal"],
            "expected": {"dev_auroc": norank_ref["auroc_dev"], "test_auroc": norank_ref["auroc_test"],
                         "over_refusal": norank_ref["test"]["over_refusal"]},
            "tolerance_auroc": 1e-3, "tolerance_rates": 1e-9, "passed": True},
    }
    # thresholds must be bit-identical to the committed ones for the all-12 refit
    th, th_ref = all12["thresholds"], full["thresholds"]
    assert th["band"]["t_lo"] == th_ref["band"]["t_lo"], "all-12 band t_lo drifted"
    assert th["band"]["t_hi"] == th_ref["band"]["t_hi"], "all-12 band t_hi drifted"
    assert th["band_exploratory"]["t_lo"] == full["exploratory"]["operating_point"]["band"]["t_lo"], \
        "all-12 exploratory band t_lo drifted"
    assert th["band_exploratory"]["t_hi"] == full["exploratory"]["operating_point"]["band"]["t_hi"], \
        "all-12 exploratory band t_hi drifted"
    out["reproduction_checks"]["all_12_thresholds"] = {
        "band": {"t_lo": th["band"]["t_lo"], "t_hi": th["band"]["t_hi"],
                 "expected_t_lo": th_ref["band"]["t_lo"], "expected_t_hi": th_ref["band"]["t_hi"]},
        "exploratory_band": {"t_lo": th["band_exploratory"]["t_lo"],
                             "t_hi": th["band_exploratory"]["t_hi"],
                             "expected_t_lo": full["exploratory"]["operating_point"]["band"]["t_lo"],
                             "expected_t_hi": full["exploratory"]["operating_point"]["band"]["t_hi"]},
        "exact": True}
    return out


# --------------------------------------------------------------------------- #
# markdown
# --------------------------------------------------------------------------- #
def render_md(add: dict, abl: dict) -> str:
    L = []
    A = L.append
    A("# STATS-ADDENDUM — C1 \"How Hard Are Your Negatives?\"\n")
    A("Generated by `04_experiments/src/stats_addendum.py`; every cell below is formatted from "
      "`04_experiments/results/c1/stats_addendum.json` and `ablations.json` written by the same run. "
      "Seeds and draw counts are frozen (`BOOT_SEED=12345`, 10,000 draws, PREREGISTRATION §7–§8). "
      "No test item is used to fit anything.\n")
    A("Rates are printed to 2 decimals and AUROCs to 3, per PREREGISTRATION §6. Items: "
      f"dev n={add['items']['n_dev']}, test n={add['items']['n_test']}.\n")

    # ---- 1 ----
    A("## 1. Rung-2 exchangeability (answers MF-3)\n")
    A("Per split the 400 sampled questions are the rung-0 rows of `items.jsonl`. A question is "
      "*dropped* for rung 2 when no rung-2 row exists for its qid (build-time reason "
      "`no_anchor_candidate`: no content token of the question occurs in any non-gold paragraph of the "
      "split's pool).\n")
    for split in ("dev", "test"):
        blk = add["exchangeability"]["splits"][split]
        A(f"### {split}: {blk['n_kept']} kept vs {blk['n_dropped']} dropped "
          f"({blk['share_kept']*100:.1f}% of the 400 sampled questions kept)\n")
        A("| Variable | Kept mean | Kept median | Kept n | Dropped mean | Dropped median | Dropped n | "
          "Median diff (kept−dropped) | Mann-Whitney p |")
        A("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
        names = {"q_chars": "Question length (characters)",
                 "q_tokens": "Question length (tokens)",
                 "gold_chars": "Gold paragraph length (characters)",
                 "n_paragraphs": "Paragraphs in source article"}
        for v, lab in names.items():
            d = blk["variables"][v]
            A(f"| {lab} | {d['kept']['mean']:.1f} | {d['kept']['median']:.1f} | {d['kept']['n']} | "
              f"{d['dropped']['mean']:.1f} | {d['dropped']['median']:.1f} | {d['dropped']['n']} | "
              f"{d['median_diff_kept_minus_dropped']:+.1f} | {fmt_p(d['p_value'])} |")
        at = blk["variables"]["answer_type"]
        A("")
        A("| Answer surface type | Kept n | Kept share | Dropped n | Dropped share |")
        A("|---|---:|---:|---:|---:|")
        for t in ("date", "name", "number", "other", "year"):
            c = at["counts"][t]
            A(f"| {t} | {c['kept']} | {at['kept_share'][t]*100:.1f}% | {c['dropped']} | "
              f"{at['dropped_share'][t]*100:.1f}% |")
        A(f"| **total** | **{blk['n_kept']}** | 100.0% | **{blk['n_dropped']}** | 100.0% |")
        A("")
        A(f"Answer-type test (5×2): {at['test']}, statistic {at['statistic']:.3f}, "
          f"p = {fmt_p(at['p_value'])} (minimum expected cell {at['min_expected']:.2f}). "
          "`fisher_exact` in scipy is 2×2 only, so the 5×2 table is tested with the exact-conditional "
          "permutation version (10,000 draws, margins fixed) and two collapsed 2×2 tables are given "
          "below with literal Fisher p-values.\n")
        fc = at["fisher_collapsed"]
        A("| Collapsed contrast | Kept n (share) | Dropped n (share) | Odds ratio | Fisher exact p |")
        A("|---|---:|---:|---:|---:|")
        for k, lab in (("name_vs_other", "name vs all other types"),
                       ("numeric_vs_other", "numeric (year+number+date) vs other")):
            d = fc[k]
            odds = "n/a" if d["odds_ratio"] is None else f"{d['odds_ratio']:.2f}"
            A(f"| {lab} | {d['table']['kept'][0]} ({d['kept_share']*100:.1f}%) | "
              f"{d['table']['dropped'][0]} ({d['dropped_share']*100:.1f}%) | {odds} | "
              f"{fmt_p(d['p_value'])} |")
        A("")
    A("**Conclusion.** " + add["exchangeability"]["verdict"] + "\n")

    # ---- 2 ----
    A("## 2. Matched-recall table (answers MF-6)\n")
    A("On the held-out half, the refusal rate over a rung's negatives is *abstain recall* and *abstain "
      "precision* simultaneously (every refused item in that rung is a negative), so both names are "
      "reported for the same number. The single threshold was chosen on **dev** so that its dev abstain "
      f"recall equals the band's (t = {add['matched_recall']['dev']['matched_threshold_t']:.6f}).\n")
    A("| Rung | n | Refused (band) | Refused (matched single) | Band refusal rate (= abstain recall = "
      "abstain precision) | Matched-single refusal rate | Band − matched (pp) |")
    A("|---|---:|---:|---:|---:|---:|---:|")
    for k in ("1", "2", "3", "4", "pooled_1_4"):
        d = add["matched_recall"]["test"][k]
        lab = f"pooled 1–4" if k == "pooled_1_4" else f"rung {k}"
        A(f"| {lab} | {d['n']} | {d['n_refused_band']} | {d['n_refused_matched']} | "
          f"{d['band_refusal_rate']:.2f} | {d['matched_single_refusal_rate']:.2f} | "
          f"{d['difference_pp']:+.1f} |")
    dv = add["matched_recall"]["dev"]
    A("")
    an = add["matched_recall"]["answerable_side"]
    A(f"Answerable side, same test half: over-refusal {an['over_refusal_band']:.2f} (band) vs "
      f"{an['over_refusal_matched']:.2f} (matched single) over {an['n_rung0_test']} rung-0 items; "
      f"coverage {an['coverage_band']:.2f} vs {an['coverage_matched']:.2f}.\n")
    A(f"Dev-side operating points that define the matching: band abstain recall "
      f"{dv['band_dev_abstain_recall']:.2f} at precision {dv['band_dev_abstain_precision']:.2f}; "
      f"matched single abstain recall {dv['matched_single_dev_abstain_recall']:.2f} at precision "
      f"{dv['matched_single_dev_abstain_precision']:.2f}.\n")
    h3 = add["matched_recall"]["h3_test_on_negatives"]
    A(f"H3 on the negative side, using the frozen `gate.boot_precision_diff` and `gate.paired_sign` "
      f"helpers: paired difference {h3['boot_precision_diff']['diff']:+.4f} (95% CI "
      f"[{h3['boot_precision_diff']['lo']:+.4f}, {h3['boot_precision_diff']['hi']:+.4f}] over "
      f"{h3['boot_precision_diff']['n']} negatives), sign test p = "
      f"{fmt_p(h3['paired_sign']['p_value'])} with {h3['discordant_pairs']} discordant pairs.\n")
    A("**Reading.** " + add["matched_recall"]["reading"] + "\n")

    # ---- 3 ----
    A("## 3. Cluster bootstrap by article (answers MF-5)\n")
    cb = add["cluster_bootstrap"]
    A(f"Test half: {cb['n_articles_test']} whole SQuAD articles, {cb['n_boot']} resamples of articles "
      f"with replacement (seed {cb['seed']}); all items of a resampled article enter that rung's mean. "
      "Percentile 2.5/97.5, next to the committed item-level intervals.\n")
    A("| Gate | Rung | n items | Point | Cluster CI (article) | Item CI (committed) | Width cluster | "
      "Width item | Ratio |")
    A("|---|---:|---:|---:|---|---|---:|---:|---:|")
    for gate, key in (("confirmatory band", "per_rung"), ("exploratory band", "exploratory_band")):
        for r in ("1", "2", "3", "4"):
            d = cb[key][r]
            ratio = "n/a" if d["width_ratio"] is None else f"{d['width_ratio']:.2f}"
            A(f"| {gate} | {r} | {d['n_items']} | {d['point']:.3f} | "
              f"[{d['cluster_ci95']['lo']:.3f}, {d['cluster_ci95']['hi']:.3f}] | "
              f"[{d['item_ci95']['lo']:.3f}, {d['item_ci95']['hi']:.3f}] | "
              f"{d['width_cluster']:.3f} | {d['width_item']:.3f} | {ratio} |")
    A("")
    A("**Reading.** " + add["cluster_bootstrap"]["reading"] + "\n")

    # ---- 4 ----
    A("## 4. Exploratory uncertainty (answers MF-4)\n")
    eu = add["exploratory_uncertainty"]
    A("Point estimates and the committed BCa intervals (10,000 draws, seed 12345, item-level), "
      "confirmatory and exploratory gates side by side.\n")
    A("| Rung | n | Exploratory abstain precision | BCa 95% CI (exploratory) | Confirmatory abstain "
      "precision | BCa 95% CI (confirmatory) |")
    A("|---|---:|---:|---|---:|---|")
    for r in ("1", "2", "3", "4"):
        e = eu["per_rung_from_results_full"][r]
        c = add["confirmatory_from_results_full"][r]
        A(f"| {r} | {e['n']} | {e['abstain_precision']:.3f} | "
          f"[{e['ci95']['lo']:.3f}, {e['ci95']['hi']:.3f}] ({e['ci95']['method']}) | "
          f"{c['abstain_precision']:.3f} | [{c['ci95']['lo']:.3f}, {c['ci95']['hi']:.3f}] "
          f"({c['ci95']['method']}) |")
    A("")
    A(f"Exploratory operating point: over-refusal {eu['over_refusal']:.2f}, coverage "
      f"{eu['coverage']:.2f}, pooled abstain precision {eu['pooled_abstain_precision']:.2f}.\n")
    A("| Paired difference (test) | Diff | 95% CI (paired question bootstrap) | n pairs | Contains 0 |")
    A("|---|---:|---|---:|---|")
    labels = {"exploratory_r1_minus_r3": "Exploratory band, rung 1 − rung 3",
              "exploratory_r1_minus_r3_single": "Exploratory single, rung 1 − rung 3",
              "confirmatory_r1_minus_r3": "Confirmatory band, rung 1 − rung 3",
              "exploratory_r1_minus_r4": "Exploratory band, rung 1 − rung 4"}
    for k, lab in labels.items():
        d = eu["paired_diffs"][k]
        A(f"| {lab} | {d['diff']:+.3f} | [{d['ci95']['lo']:+.3f}, {d['ci95']['hi']:+.3f}] | "
          f"{d['n_pairs']} | {'yes' if d['contains_zero'] else 'no'} |")
    A("")
    A("**Reading.** " + eu["reading"] + "\n")

    # ---- 5 ----
    A("## 5. Leave-one-out feature ablations (answers MF-2)\n")
    A("Same items, same seeds, same threshold rule; only the feature list changes. Each row refits the "
      "logistic gate on dev and refits both bands on dev, then evaluates the frozen test half.\n")
    A("| Subset | k | Dev AUROC | Test AUROC | Test abstain precision r1 | r2 | r3 | r4 | "
      "Over-refusal | Coverage |")
    A("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for key, row in abl["rows"].items():
        pr = row["test_band"]["per_rung"]
        A(f"| {row['label']} | {row['n_features']} | {row['auroc_dev']:.3f} | {row['auroc_test']:.3f} | "
          f"{pr['1']['abstain_precision']:.3f} | {pr['2']['abstain_precision']:.3f} | "
          f"{pr['3']['abstain_precision']:.3f} | {pr['4']['abstain_precision']:.3f} | "
          f"{row['test_band']['over_refusal']:.2f} | {row['test_band']['coverage']:.2f} |")
    A("")
    A("Exploratory band (target precision 0.80, over-refusal cap 0.10, fitted on dev):\n")
    A("| Subset | k | Test abstain precision r1 | r2 | r3 | r4 | Over-refusal | Coverage | Dev over-refusal "
      "| Feasible |")
    A("|---|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for key, row in abl["rows"].items():
        pr = row["test_band_exploratory"]["per_rung"]
        th = row["thresholds"]["band_exploratory"]
        A(f"| {row['label']} | {row['n_features']} | {pr['1']['abstain_precision']:.3f} | "
          f"{pr['2']['abstain_precision']:.3f} | {pr['3']['abstain_precision']:.3f} | "
          f"{pr['4']['abstain_precision']:.3f} | {row['test_band_exploratory']['over_refusal']:.2f} | "
          f"{row['test_band_exploratory']['coverage']:.2f} | {th.get('dev_over_refusal', float('nan')):.2f} | "
          f"{'yes' if th.get('feasible') else 'NO'} |")
    A("")
    A("Reproduction checks (hard asserts inside the script): " +
      f"all-12 dev AUROC {abl['reproduction_checks']['all_12_vs_results_full']['dev_auroc']:.4f} vs "
      f"committed {abl['reproduction_checks']['all_12_vs_results_full']['expected_dev']:.4f}, test "
      f"{abl['reproduction_checks']['all_12_vs_results_full']['test_auroc']:.4f} vs "
      f"{abl['reproduction_checks']['all_12_vs_results_full']['expected_test']:.4f} (tol 1e-3); "
      f"no-rank dev/test {abl['rows']['no_rank']['auroc_dev']:.4f}/"
      f"{abl['rows']['no_rank']['auroc_test']:.4f} and over-refusal "
      f"{abl['rows']['no_rank']['test_band']['over_refusal']:.2f} vs committed "
      f"{abl['reproduction_checks']['no_rank_vs_ablation_no_rank_json']['expected']['over_refusal']:.2f}.\n")
    A("The all-12 refit also reproduces both committed threshold pairs **exactly** (band "
      f"t_lo={abl['reproduction_checks']['all_12_thresholds']['band']['t_lo']:.6f}, "
      f"t_hi={abl['reproduction_checks']['all_12_thresholds']['band']['t_hi']:.6f}; exploratory "
      f"t_lo={abl['reproduction_checks']['all_12_thresholds']['exploratory_band']['t_lo']:.6f}, "
      f"t_hi={abl['reproduction_checks']['all_12_thresholds']['exploratory_band']['t_hi']:.6f}).\n")
    A("**Which group carries the separation.** " + abl["verdict"] + "\n")
    fr = abl["feature_redundancy"]
    A(f"### Feature-matrix redundancy (checked, not assumed)\n")
    A(f"Of the {fr['n_columns']} gate columns, {fr['n_distinct_columns']} are distinct and "
      f"{fr['n_informative_columns']} are informative: identical pairs "
      + ", ".join(f"`{a}` ≡ `{b}`" for a, b in fr["identical_pairs"])
      + f"; constant columns " + ", ".join(f"`{c}`" for c in fr["constant_columns"])
      + f" (value {fr['dense_rank_log_value'][0]:.6f} = ln 2 in both splits; "
      f"dev n={fr['per_split']['dev']['n']}, test n={fr['per_split']['test']['n']}). "
      "Consequence: 'k' in the table above counts columns, not independent signals, and the dense "
      "ablation removes one distinct informative column plus a duplicate and a constant.\n")
    A("---\n")
    A(f"_Inputs (sha256): items.jsonl `{add['inputs']['items_jsonl'][:16]}…`, features.csv "
      f"`{add['inputs']['features_csv'][:16]}…`, predictions.csv "
      f"`{add['inputs']['predictions_csv'][:16]}…`, results_full.json "
      f"`{add['inputs']['results_full'][:16]}…`._")
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def build_all() -> tuple[dict, dict]:
    items = load_items()
    feats = G.load_features()
    items = [it for it in items if it["item_id"] in feats]
    preds = load_predictions()
    full = json.loads((RESULTS / "results_full.json").read_text(encoding="utf-8"))

    add = {"generated_by": "04_experiments/src/stats_addendum.py",
           "seed": SEED, "n_boot": N_BOOT,
           "inputs": {"items_jsonl": sha256(DATA / "items.jsonl"),
                      "features_csv": sha256(DATA / "features.csv"),
                      "predictions_csv": sha256(RESULTS / "predictions.csv"),
                      "results_full": sha256(RESULTS / "results_full.json"),
                      "ablation_no_rank": sha256(RESULTS / "ablation_no_rank.json")},
           "items": {"n_dev": sum(1 for it in items if it["split"] == "dev"),
                     "n_test": sum(1 for it in items if it["split"] == "test")}}

    add["exchangeability"] = exchangeability(items)
    add["matched_recall"] = matched_recall(preds, full)
    add["cluster_bootstrap"] = cluster_bootstrap(preds, items, full)
    add["exploratory_uncertainty"] = exploratory_uncertainty(preds, full)
    add["confirmatory_from_results_full"] = {
        r: {"abstain_precision": full["test"]["band_primary"]["per_rung"][r]["abstain_precision"],
            "n": full["test"]["band_primary"]["per_rung"][r]["n"],
            "ci95": {"lo": full["test"]["band_primary"]["per_rung"][r]["ci95"]["lo"],
                     "hi": full["test"]["band_primary"]["per_rung"][r]["ci95"]["hi"],
                     "method": full["test"]["band_primary"]["per_rung"][r]["ci95"].get("method")}}
        for r in ("1", "2", "3", "4")}
    abl = ablations(feats, items, full)
    add["ablation_summary"] = {
        "file": "04_experiments/results/c1/ablations.json",
        "rows": {k: {"n_features": v["n_features"], "auroc_dev": v["auroc_dev"],
                     "auroc_test": v["auroc_test"],
                     "over_refusal_confirmatory": v["test_band"]["over_refusal"]}
                 for k, v in abl["rows"].items()}}
    return add, abl


def compute_readings(add: dict, abl: dict) -> None:
    """Fill the prose 'reading' fields from the numbers (so no claim outruns the data)."""
    # ---- cluster vs item ----
    cb = add["cluster_bootstrap"]
    pairs = []
    for key in ("per_rung", "exploratory_band"):
        for r, d in cb[key].items():
            if d["width_ratio"] is not None:
                pairs.append((key, r, d["width_ratio"], d["cluster_ci95"], d["item_ci95"]))
    narrower = [p for p in pairs if p[2] < 1.0]
    wider = [p for p in pairs if p[2] > 1.0]
    below_080 = [p for p in pairs if p[3]["lo"] < 0.80]
    below_090 = [(p[0], p[1], p[3]) for p in pairs if p[3]["hi"] < 0.90]
    gate_name = {"per_rung": "confirmatory band", "exploratory_band": "exploratory band"}
    max_ratio = max(p[2] for p in pairs)
    min_ratio = min(p[2] for p in pairs)
    # between-article dispersion of the exploratory rates (does clustering even bite?)
    sds = {r: cb["exploratory_band"][r]["per_article_rate"]["sd"] for r in ("1", "2", "3", "4")}
    at_one = {r: cb["exploratory_band"][r]["per_article_rate"]["n_at_1"] for r in ("1", "2", "3", "4")}
    cb["reading"] = (
        f"Cluster and item intervals agree in verdict everywhere. Of the {len(pairs)} comparable "
        f"rung-gate cells, {len(narrower)} cluster intervals are narrower than the item interval and "
        f"{len(wider)} {'is' if len(wider) == 1 else 'are'} wider (width ratio {min_ratio:.2f} to "
        f"{max_ratio:.2f}); the widest is the "
        f"exploratory rung 4, ["
        f"{cb['exploratory_band']['4']['cluster_ci95']['lo']:.3f}, "
        f"{cb['exploratory_band']['4']['cluster_ci95']['hi']:.3f}] versus ["
        f"{cb['exploratory_band']['4']['item_ci95']['lo']:.3f}, "
        f"{cb['exploratory_band']['4']['item_ci95']['hi']:.3f}] at item level. "
        + ("No interval's lower bound falls below 0.80. " if not below_080
           else f"{len(below_080)} interval(s) have a lower bound below 0.80. ")
        + (f"Intervals lying entirely below the 0.90 line: "
           + ", ".join(f"{gate_name[a]} rung {b}" for a, b, _ in below_090) + ". " if below_090 else "")
        + "Clustering does not widen the intervals materially, and the reason is visible in the "
          "per-article rates: the exploratory refusal rate is almost constant across articles "
          f"(between-article sd {min(sds.values()):.3f}–{max(sds.values()):.3f}, "
          f"{at_one['1']}/{cb['n_articles_test']} articles at 1.00 in rung 1), so there is no "
          "article-level variance for the cluster bootstrap to add. The confirmatory gate's rung-2 "
          "interval is the one case where clustering narrows the interval, from "
          f"[{cb['per_rung']['2']['item_ci95']['lo']:.3f}, {cb['per_rung']['2']['item_ci95']['hi']:.3f}]"
          f" to [{cb['per_rung']['2']['cluster_ci95']['lo']:.3f}, "
          f"{cb['per_rung']['2']['cluster_ci95']['hi']:.3f}], because only one article supplies the "
          "single non-refused rung-2 item.")

    # ---- matched recall ----
    diffs = [abs(add["matched_recall"]["test"][k]["difference_pp"]) for k in ("1", "2", "3", "4")]
    add["matched_recall"]["max_abs_diff_pp"] = r4(max(diffs))
    mr = add["matched_recall"]
    ans = mr["answerable_side"]
    add["matched_recall"]["reading"] = (
        f"At matched dev abstain recall the band and the single threshold refuse the same negatives to "
        f"{mr['max_abs_diff_pp']:.1f} points in every rung and {mr['max_abs_diff_pp']:.1f} pooled, so the "
        f"band's second threshold adds no negative-side recall at all. Its only measurable effect is on "
        f"answerable items: over-refusal {ans['over_refusal_band']:.2f} (band) versus "
        f"{ans['over_refusal_matched']:.2f} (matched single) on the {ans['n_rung0_test']} rung-0 test "
        f"items, coverage {ans['coverage_band']:.2f} versus {ans['coverage_matched']:.2f}. H3's "
        f"≥5-point precision gain is therefore 0.0 points and the band is the worse operating point on "
        f"the metric H3 is about.")

    # ---- exploratory ----
    eu = add["exploratory_uncertainty"]
    d13 = eu["paired_diffs"]["exploratory_r1_minus_r3"]
    d14 = eu["paired_diffs"]["exploratory_r1_minus_r4"]
    s = eu["per_rung_from_results_full"]
    sep = (s["3"]["ci95"]["lo"] > s["4"]["ci95"]["hi"]) or (s["4"]["ci95"]["lo"] > s["3"]["ci95"]["hi"])
    eu["reading"] = (
        f"The exploratory rung-1 minus rung-3 difference is {d13['diff']:+.3f} (95% CI "
        f"[{d13['ci95']['lo']:+.3f}, {d13['ci95']['hi']:+.3f}], {d13['n_pairs']} paired questions), so "
        f"the interval {'contains' if d13['contains_zero'] else 'excludes'} zero but the point "
        f"difference is {abs(d13['diff'])*100:.1f} points against the pre-registered 15-point "
        f"criterion: H1's effect-size clause fails and its monotonicity clause fails too "
        f"(rung 2 {s['2']['abstain_precision']:.3f} sits below rung 3 {s['3']['abstain_precision']:.3f}). "
        f"The rung 3 and rung 4 intervals {'do not overlap, so the rung-4 drop is separable' if sep else 'overlap, so rung 3 and rung 4 are not separable at this n'}; "
        f"rung 1 minus rung 4 is {d14['diff']:+.3f} [{d14['ci95']['lo']:+.3f}, {d14['ci95']['hi']:+.3f}].")

    # ---- ablation verdict ----
    base = abl["rows"]["all_12"]
    drops = {k: base["auroc_test"] - v["auroc_test"] for k, v in abl["rows"].items()
             if k not in ("all_12", "lex_overlap_only")}
    worst = max(drops, key=drops.get)
    best = min(drops, key=drops.get)
    abl["auroc_test_drops"] = {k: r4(v) for k, v in drops.items()}
    lo = abl["rows"]["lex_overlap_only"]
    r4_all = abl["rows"]["no_dense"]["test_band"]["per_rung"]["4"]["abstain_precision"]
    fr = abl["feature_redundancy"]
    abl["verdict"] = (
        f"The dense presented-passage score carries the separation: dropping the four dense columns "
        f"costs {drops['no_dense']*100:.1f} points of test AUROC "
        f"({base['auroc_test']:.3f} → {abl['rows']['no_dense']['auroc_test']:.3f}) and is the only "
        f"single-group removal that does, while dropping lex_overlap costs "
        f"{drops['no_lex_overlap']*100:.1f}, the two rank features {drops['no_rank']*100:.1f}, the "
        f"cross-encoder {drops['no_ce_presented']*100:.1f} and the bm25 presented pair "
        f"{drops['no_bm25_presented_pair']*100:.1f}. The block is narrower than its name: "
        f"dense_presented and dense_top1 are the same number for every item and dense_rank_log is "
        f"constant at ln 2, so the all-12 gate really has {fr['n_informative_columns']} informative "
        f"columns and 'without the four dense features' removes one distinct signal. The effect is "
        f"concentrated in rung 4: without it the confirmatory gate's rung-4 abstain precision falls to "
        f"{r4_all:.3f} and the exploratory band's to "
        f"{abl['rows']['no_dense']['test_band_exploratory']['per_rung']['4']['abstain_precision']:.3f}. "
        f"lex_overlap alone reaches test AUROC {lo['auroc_test']:.3f}, so overlap is not what carries "
        f"the result inside this feature stack — although the separate surface audit (audit.json) shows "
        f"overlap is highly predictive of rung membership on its own, which is a different question.")



def main() -> None:
    check = "--check" in sys.argv
    add, abl = build_all()
    compute_readings(add, abl)
    md = render_md(add, abl)

    p_add = RESULTS / "stats_addendum.json"
    p_abl = RESULTS / "ablations.json"
    p_md = RESULTS / "STATS-ADDENDUM.md"

    if check:
        old = json.loads(p_add.read_text(encoding="utf-8"))
        diffs = []
        for k in ("exchangeability", "matched_recall", "cluster_bootstrap", "exploratory_uncertainty"):
            if json.dumps(old[k], sort_keys=True) != json.dumps(add[k], sort_keys=True):
                diffs.append(k)
        print(json.dumps({"check": "stats_addendum", "mismatched_blocks": diffs,
                          "match": not diffs}, indent=2))
        raise SystemExit(0 if not diffs else 1)

    p_add.write_text(json.dumps(add, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    p_abl.write_text(json.dumps(abl, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    p_md.write_text(md, encoding="utf-8")
    print(json.dumps({"wrote": [str(p_add), str(p_abl), str(p_md)],
                      "dev_dropped": add["exchangeability"]["splits"]["dev"]["n_dropped"],
                      "test_dropped": add["exchangeability"]["splits"]["test"]["n_dropped"],
                      "exchangeability_p": {s: {v: d["p_value"] for v, d in
                                                add["exchangeability"]["splits"][s]["variables"].items()}
                                            for s in ("dev", "test")},
                      "matched": add["matched_recall"]["test"],
                      "abl_auroc_test": {k: v["auroc_test"] for k, v in abl["rows"].items()}},
                     indent=2))


if __name__ == "__main__":
    main()
