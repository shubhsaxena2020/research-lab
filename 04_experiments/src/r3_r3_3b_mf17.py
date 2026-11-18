"""R3-3b / MF-17: post-hoc AUROC intervals from existing per-item predictions.

Owned file: 04_experiments/src/r3_r3_3b_mf17.py
Writes:     04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json

Run:   python 04_experiments/src/r3_r3_3b_mf17.py
Check: python 04_experiments/src/r3_r3_3b_mf17.py --check-repro

This lane recomputes, from already-existing files only, 95% bootstrap intervals
for the AUROCs named in the MF-17 response letter: frozen and corrected held-out
(test) AUROC, their paired difference on the common held-out items, top-1 AUROC,
transfer AUROC, and the lexical/gold-indicator audit AUROCs. It uses the
bootstrap helpers in ``r3_exp_auroc_ci`` unchanged, with n_boot=10000 and
seed=20261118. Both item-level and article-cluster-level resampling are kept.

Every number produced here is EXPLORATORY / POST-HOC. No frozen result,
preregistration artifact, threshold, or prior R3 result is modified.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "04_experiments" / "src"
DATA = ROOT / "04_experiments" / "data"
RESULTS = ROOT / "04_experiments" / "results" / "c1"
OUT_DEFAULT = RESULTS / "r3" / "R3-3b" / "mf17_auroc_intervals.json"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import audit as A  # noqa: E402
import eval_top1 as ET  # noqa: E402
import gate as G  # noqa: E402
import r3_exp_auroc_ci as CI  # noqa: E402

SEED = 20261118
N_BOOT = 10000
ALPHA = 0.05
AUDIT_CV_SEED = 13  # fold seed for the audit OOF scores; bootstrap uses SEED
COMMAND = "python 04_experiments/src/r3_r3_3b_mf17.py"
CHECK_COMMAND = COMMAND + " --check-repro"
PREFIX = "c1.r3_3b.mf17."


# --------------------------------------------------------------------------- #
# small helpers
# --------------------------------------------------------------------------- #
def sha256_file(path: Path) -> str:
    return CI.sha256_file(Path(path))


def _pred_rows(path: Path) -> list[dict]:
    return [r for r in CI.load_csv_rows(Path(path)) if r.get("split") == "test"]


def _oof_scores(X: np.ndarray, y: np.ndarray, seed: int = AUDIT_CV_SEED) -> np.ndarray:
    """5-fold OOF logistic scores, matching r3_exp_auroc_ci's audit construction."""
    y = np.asarray(y).astype(int)
    X = np.asarray(X, dtype=float)
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=int(seed))
    oof = np.zeros(len(y), dtype=float)
    for tr, te in skf.split(X, y):
        clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
        clf.fit(X[tr], y[tr])
        oof[te] = clf.predict_proba(X[te])[:, 1]
    return oof


def _add_auroc(section: dict, key: str, y, scores, cluster_ids,
               scope: str, split: str, n_boot: int, seed: int,
               note: str | None = None) -> dict:
    """Compute item-level and article-cluster-level percentile-bootstrap CIs."""
    y = list(y)
    scores = list(scores)
    ci_item = CI.bootstrap_auroc_ci(y, scores, n_boot=n_boot, seed=seed,
                                    cluster_ids=None, alpha=ALPHA)
    ci_cluster = None
    if cluster_ids is not None:
        ci_cluster = CI.bootstrap_auroc_ci(y, scores, n_boot=n_boot, seed=seed,
                                          cluster_ids=cluster_ids, alpha=ALPHA)
    entry = {
        "scope": scope,
        "split": split,
        "post_hoc": True,
        "point": ci_item["point"],
        "n": ci_item["n"],
        "n_positive": ci_item["n_positive"],
        "n_negative": ci_item["n_negative"],
        "n_clusters": ci_cluster["n_clusters"] if ci_cluster else None,
        "ci_item": ci_item,
        "ci_cluster": ci_cluster,
    }
    if note:
        entry["note"] = note
    section[key] = entry
    return entry


def _flat_entry(entry: dict, cluster: bool = False) -> dict:
    """Flatten one AUROC entry for the top-level results object."""
    ci = entry.get("ci_cluster") if cluster else entry.get("ci_item")
    return {
        "point": ci["point"],
        "lo": ci["lo"],
        "hi": ci["hi"],
        "n": ci["n"],
        "n_positive": ci.get("n_positive"),
        "n_negative": ci.get("n_negative"),
        "n_clusters": ci.get("n_clusters"),
        "n_boot": ci["n_boot"],
        "n_valid": ci["n_valid"],
        "seed": ci["seed"],
        "alpha": ci["alpha"],
        "level": ci["level"],
        "method": ci["method"],
        "post_hoc": True,
    }


def _flat_diff(entry: dict, cluster: bool = False) -> dict:
    ci = entry.get("ci_cluster") if cluster else entry.get("ci_item")
    return {
        "diff": ci["diff"],
        "lo": ci["lo"],
        "hi": ci["hi"],
        "contains_zero": ci["contains_zero"],
        "n": ci["n"],
        "n_clusters": ci.get("n_clusters"),
        "n_boot": ci["n_boot"],
        "n_valid": ci["n_valid"],
        "seed": ci["seed"],
        "alpha": ci["alpha"],
        "level": ci["level"],
        "method": ci["method"],
        "post_hoc": True,
    }


# --------------------------------------------------------------------------- #
# main computation
# --------------------------------------------------------------------------- #
def build_result(n_boot: int = N_BOOT, seed: int = SEED) -> dict:
    n_boot = int(n_boot)
    seed = int(seed)

    input_paths = {
        "frozen_predictions": "04_experiments/results/c1/predictions.csv",
        "corrected_predictions": "04_experiments/results/c1_corrected/predictions.csv",
        "items": "04_experiments/data/items.jsonl",
        "items_top1": "04_experiments/data/items_top1.jsonl",
        "features_top1": "04_experiments/data/features_top1.csv",
        "transfer_items": "04_experiments/data/transfer_items.jsonl",
        "features_transfer_frozen": "04_experiments/data/features_transfer.csv",
        "features_transfer_corrected": "04_experiments/data/features_corrected_transfer.csv",
        "features_frozen": "04_experiments/data/features.csv",
        "features_corrected": "04_experiments/data/features_corrected.csv",
        "helper_r3_exp_auroc_ci": "04_experiments/src/r3_exp_auroc_ci.py",
    }
    out: dict = {
        "experiment": "c1",
        "lane": "R3-3b",
        "item": "MF-17",
        "stage": "r3_r3_3b_mf17",
        "generated_by": "04_experiments/src/r3_r3_3b_mf17.py",
        "command": COMMAND,
        "commands": [COMMAND, CHECK_COMMAND],
        "seed": seed,
        "seeds": {
            "bootstrap_seed": seed,
            "audit_oof_cv_seed": AUDIT_CV_SEED,
            "gate_seed": None,
        },
        "n_boot": n_boot,
        "alpha": ALPHA,
        "method": "non-parametric percentile bootstrap (2.5/97.5)",
        "level": "item and article-cluster (title)",
        "post_hoc": True,
        "exploratory": True,
        "label": "exploratory/post-hoc",
        "input_paths": input_paths,
        "input_sha256": {k: sha256_file(ROOT / v) for k, v in input_paths.items()},
        "inputs": {k: sha256_file(ROOT / v) for k, v in input_paths.items()},
        "aurocs": {},
        "paired_diffs": {},
        "alignment_assertions": {},
        "denominators": {},
        "resampling": {},
        "results": {},
        "limitations": [
            "All intervals are post-hoc/exploratory; no frozen verdict is revised.",
            "Held-out AUROCs are computed on all test rows (answerable rung 0 vs rungs 1-4) "
            "from band_score in predictions.csv; no model is retrained.",
            "Cluster resampling uses article title as the cluster id and is reported alongside, "
            "not instead of, item-level resampling.",
            "Audit OOF scores reuse the 5-fold, seed-13 audit construction from "
            "r3_exp_auroc_ci / r3_exp_audit_twosided; the bootstrap seed is 20261118.",
            "The gold-indicator column is a label-construction artefact; its AUROC is not "
            "evidence about rung hardness.",
        ],
    }
    out["sha256_inputs"] = out["input_sha256"]

    items = CI.items_list()
    iby = {it["item_id"]: it for it in items}
    title_by_id = {it["item_id"]: it["title"] for it in items}
    frozen_dev_ids = [it["item_id"] for it in items if it["split"] == "dev"]
    corrected_dev_ids = list(frozen_dev_ids)

    # ---- frozen vs corrected held-out (test) over COMMON item ids --------------
    fr_test = _pred_rows(ROOT / input_paths["frozen_predictions"])
    co_test = _pred_rows(ROOT / input_paths["corrected_predictions"])
    ids_f = [r["item_id"] for r in fr_test]
    ids_c = [r["item_id"] for r in co_test]
    common = sorted(set(ids_f) & set(ids_c))
    mf = {r["item_id"]: r for r in fr_test}
    mc = {r["item_id"]: r for r in co_test}
    y_f = [int(mf[i]["label"]) for i in common]
    y_c = [int(mc[i]["label"]) for i in common]
    rung_f = [mf[i]["rung"] for i in common]
    rung_c = [mc[i]["rung"] for i in common]
    clusters_common = [title_by_id[i] for i in common]

    alignment = {
        "frozen_test_rows": len(fr_test),
        "corrected_test_rows": len(co_test),
        "frozen_unique_ids": len(set(ids_f)),
        "corrected_unique_ids": len(set(ids_c)),
        "common_item_count": len(common),
        "id_sets_equal": set(ids_f) == set(ids_c),
        "labels_equal_on_common_items": y_f == y_c,
        "rungs_equal_on_common_items": rung_f == rung_c,
        "all_common_ids_have_title": all(i in title_by_id for i in common),
        "n_articles_common": len(set(clusters_common)),
    }
    # Hard assertions before any paired difference is computed.
    assert alignment["common_item_count"] > 0, "no common held-out item ids"
    assert alignment["id_sets_equal"], "frozen/corrected held-out item ids differ"
    assert alignment["labels_equal_on_common_items"], "labels differ on common items"
    assert alignment["rungs_equal_on_common_items"], "rungs differ on common items"
    assert alignment["all_common_ids_have_title"], "missing title for a common item"
    out["alignment_assertions"] = alignment

    y_common = np.asarray(y_f, dtype=int)
    s_f = np.asarray([float(mf[i]["band_score"]) for i in common], dtype=float)
    s_c = np.asarray([float(mc[i]["band_score"]) for i in common], dtype=float)

    fr_entry = _add_auroc(out["aurocs"], "frozen_held_out", y_common, s_f,
                          clusters_common, "frozen", "test", n_boot, seed,
                          note="band_score from results/c1/predictions.csv, common test items")
    co_entry = _add_auroc(out["aurocs"], "corrected_held_out", y_common, s_c,
                          clusters_common, "corrected", "test", n_boot, seed,
                          note="band_score from results/c1_corrected/predictions.csv, common test items")

    pd_item = CI.paired_auroc_diff_ci(y_common, s_f, s_c, n_boot=n_boot,
                                      seed=seed, cluster_ids=None, alpha=ALPHA)
    pd_cluster = CI.paired_auroc_diff_ci(y_common, s_f, s_c, n_boot=n_boot,
                                         seed=seed, cluster_ids=clusters_common,
                                         alpha=ALPHA)
    pd_entry = {
        "scope": "frozen_minus_corrected",
        "split": "test",
        "common_item_ids": len(common),
        "post_hoc": True,
        "point": pd_item["diff"],
        "ci_item": pd_item,
        "ci_cluster": pd_cluster,
        "note": "paired on identical, asserted-aligned held-out item ids",
    }
    out["paired_diffs"]["frozen_minus_corrected_held_out"] = pd_entry

    out["denominators"]["held_out_common"] = {
        "n_items": len(common),
        "n_positive_rung0": int((y_common == 1).sum()),
        "n_negative_rungs1to4": int((y_common == 0).sum()),
        "n_article_clusters": len(set(clusters_common)),
    }

    # ---- top-1 (presented passage) test AUROC ----------------------------------
    top_items, top_feats = ET.load()
    top_dev = [it["item_id"] for it in top_items if it["split"] == "dev"]
    top_test = [it["item_id"] for it in top_items if it["split"] == "test"]
    top_by_id = {it["item_id"]: it for it in top_items}
    top_gate = G.fit_logistic_gate(top_feats, top_dev)
    s_top_test = top_gate.score(top_feats, top_test)
    y_top_test = np.asarray([top_feats[i]["label"] for i in top_test], dtype=int)
    top_clusters = [top_by_id[i]["title"] for i in top_test]
    top_entry = _add_auroc(out["aurocs"], "top1_test", y_top_test, s_top_test,
                           top_clusters, "top1", "test", n_boot, seed,
                           note="gold vs non-gold on top1_presented test items; gate refit on dev")
    out["denominators"]["top1_test"] = {
        "n_items": int(len(top_test)),
        "n_hit_label1": int((y_top_test == 1).sum()),
        "n_miss_label0": int((y_top_test == 0).sum()),
        "n_article_clusters": len(set(top_clusters)),
    }

    # ---- transfer AUROC (rung 0 vs rung 3), both runs --------------------------
    transfer_items = CI.load_items_jsonl(DATA / "transfer_items.jsonl")
    t_ids = [it["item_id"] for it in transfer_items]
    t_y = np.asarray([1 if it["rung"] == 0 else 0 for it in transfer_items], dtype=int)
    t_clusters = [it["title"] for it in transfer_items]
    feats_fr = G.load_features(DATA / "features.csv")
    feats_co = G.load_features(DATA / "features_corrected.csv")
    g_fr = G.fit_logistic_gate(feats_fr, frozen_dev_ids)
    g_co = G.fit_logistic_gate(feats_co, corrected_dev_ids)
    feats_t_fr = G.load_features(DATA / "features_transfer.csv")
    feats_t_co = G.load_features(DATA / "features_corrected_transfer.csv")
    s_t_fr = g_fr.score(feats_t_fr, t_ids)
    s_t_co = g_co.score(feats_t_co, t_ids)
    tf_entry = _add_auroc(out["aurocs"], "transfer_frozen", t_y, s_t_fr,
                          t_clusters, "frozen", "transfer", n_boot, seed,
                          note="transfer rung0 vs rung3, frozen dev-fitted gate")
    tc_entry = _add_auroc(out["aurocs"], "transfer_corrected", t_y, s_t_co,
                          t_clusters, "corrected", "transfer", n_boot, seed,
                          note="transfer rung0 vs rung3, corrected dev-fitted gate")
    out["denominators"]["transfer"] = {
        "n_items": int(len(t_ids)),
        "n_rung0_label1": int((t_y == 1).sum()),
        "n_rung3_label0": int((t_y == 0).sum()),
        "n_article_clusters": len(set(t_clusters)),
    }

    # ---- lexical / gold-indicator audit AUROCs (dev) ---------------------------
    dev_items = [it for it in items if it["split"] == "dev"]
    pos = [it for it in dev_items if it["rung"] == 0]
    y_audit = None  # 0 = answerable, 1 = negative (audit convention)
    audit_entries: dict[str, dict] = {}
    for r in (1, 2, 3, 4):
        neg = [it for it in dev_items if it["rung"] == r]
        if not neg:
            continue
        items_r = pos + neg
        X_lex = np.vstack([A.surface_features(pos, with_lex=True),
                           A.surface_features(neg, with_lex=True)])
        y = np.concatenate([np.zeros(len(pos)), np.ones(len(neg))]).astype(int)
        y_audit = y
        clusters_r = [it["title"] for it in items_r]
        oof_lex = _oof_scores(X_lex, y, AUDIT_CV_SEED)
        lex_entry = _add_auroc(out["aurocs"], f"audit_lex_overlap_rung{r}",
                               y, oof_lex, clusters_r, "audit_lex", "dev",
                               n_boot, seed,
                               note="surface_6 + lex_jaccard/q_len, 5-fold OOF (seed 13), "
                                    "negative vs answerable direction")
        X_gold = np.column_stack([X_lex, np.concatenate([np.ones(len(pos)), np.zeros(len(neg))])])
        oof_gold = _oof_scores(X_gold, y, AUDIT_CV_SEED)
        gold_entry = _add_auroc(out["aurocs"], f"audit_gold_indicator_lexical_rung{r}",
                                y, oof_gold, clusters_r, "audit_gold_lex", "dev",
                                n_boot, seed,
                                note="surface_6 + lex features + gold indicator; "
                                     "gold indicator is a label-construction artefact")
        is_gold_alone = np.concatenate([np.ones(len(pos)), np.zeros(len(neg))])
        alone_point = float(roc_auc_score(y, is_gold_alone))
        audit_entries[str(r)] = {
            "n_answerable": len(pos),
            "n_negatives": len(neg),
            "lexical_audit": lex_entry,
            "gold_indicator_lexical_audit": gold_entry,
            "gold_indicator_alone_point_raw": alone_point,
            "gold_indicator_alone_reverse_direction": 1.0 - alone_point,
            "direction_note": "y=1 for negatives; raw is_gold-alone AUROC is 0 and its "
                              "reverse direction is 1 by construction",
        }
        out["denominators"][f"audit_rung{r}"] = {
            "n_items": int(len(y)),
            "n_answerable_rung0": len(pos),
            "n_negative_rung": len(neg),
            "n_article_clusters": len(set(clusters_r)),
        }
    out["audit_details"] = audit_entries

    out["resampling"] = {
        "item_level": "bootstrap_auroc_ci / paired_auroc_diff_ci with cluster_ids=None "
                      "(resample item rows with replacement)",
        "cluster_level": "same helpers with cluster_ids=article title (resample whole "
                         "articles with replacement; n_boot resamples of the cluster set)",
        "alpha": ALPHA,
        "interval": "percentile 2.5 / 97.5",
        "helpers_source": "04_experiments/src/r3_exp_auroc_ci.py",
        "n_boot": n_boot,
        "bootstrap_seed": seed,
    }

    # ---- flat, bindable results object ----------------------------------------
    results: dict[str, object] = {}
    canonical = {
        "frozen_held_out_auroc": _flat_entry(fr_entry),
        "corrected_held_out_auroc": _flat_entry(co_entry),
        "paired_auroc_diff": _flat_diff(pd_entry),
        "top1_auroc": _flat_entry(top_entry),
        "transfer_auroc": {
            "frozen": _flat_entry(tf_entry),
            "corrected": _flat_entry(tc_entry),
            "primary": "corrected",
            "note": "both runs reported; corrected is the primary bindable arm",
        },
        "transfer_frozen_auroc": _flat_entry(tf_entry),
        "transfer_corrected_auroc": _flat_entry(tc_entry),
        "lexical_audit_auroc": _flat_entry(audit_entries["1"]["lexical_audit"]),
        "gold_indicator_lexical_audit_auroc": _flat_entry(
            audit_entries["1"]["gold_indicator_lexical_audit"]),
        "gold_indicator_alone_auroc": {
            "point": audit_entries["1"]["gold_indicator_alone_point_raw"],
            "reverse_direction": audit_entries["1"]["gold_indicator_alone_reverse_direction"],
            "level": "item",
            "method": "analytic (perfect separation by construction)",
            "post_hoc": True,
            "note": "label-construction artefact, not evidence about rung hardness",
        },
    }
    for name, value in canonical.items():
        results[PREFIX + name] = value
    # Cluster-level companions (same estimands, article-cluster resampling).
    for name, entry, flattener in (
        ("frozen_held_out_auroc_cluster", fr_entry, _flat_entry),
        ("corrected_held_out_auroc_cluster", co_entry, _flat_entry),
        ("paired_auroc_diff_cluster", pd_entry, _flat_diff),
        ("top1_auroc_cluster", top_entry, _flat_entry),
        ("transfer_frozen_auroc_cluster", tf_entry, _flat_entry),
        ("transfer_corrected_auroc_cluster", tc_entry, _flat_entry),
        ("lexical_audit_auroc_cluster", audit_entries["1"]["lexical_audit"], _flat_entry),
        ("gold_indicator_lexical_audit_auroc_cluster",
         audit_entries["1"]["gold_indicator_lexical_audit"], _flat_entry),
    ):
        results[PREFIX + name] = flattener(entry, cluster=True)

    # Aliases for integrators that used the earlier spelling.
    aliases = {
        "frozen_heldout_auroc": "frozen_held_out_auroc",
        "corrected_heldout_auroc": "corrected_held_out_auroc",
        "frozen_test_auroc": "frozen_held_out_auroc",
        "corrected_test_auroc": "corrected_held_out_auroc",
        "paired_diff_auroc": "paired_auroc_diff",
        "paired_auroc_diff_ci": "paired_auroc_diff",
        "top1_test_auroc": "top1_auroc",
        "transfer_auroc_frozen": "transfer_frozen_auroc",
        "transfer_auroc_corrected": "transfer_corrected_auroc",
        "audit_lex_overlap_auroc": "lexical_audit_auroc",
        "gold_indicator_control_auroc": "gold_indicator_lexical_audit_auroc",
    }
    for alias, target in aliases.items():
        results[PREFIX + alias] = canonical[target]

    # Scalar subkeys: make point / bounds directly bindable as numbers.
    for key in list(results):
        value = results[key]
        if isinstance(value, dict) and {"point"} <= set(value):
            results[key + ".point"] = value["point"]
            if "lo" in value:
                results[key + ".ci95_lo"] = value["lo"]
                results[key + ".ci95_hi"] = value["hi"]
            elif "diff" in value:
                results[key + ".ci95_lo"] = value["lo"]
                results[key + ".ci95_hi"] = value["hi"]
        if isinstance(value, dict) and {"diff"} <= set(value):
            results[key + ".diff"] = value["diff"]
            results[key + ".ci95_lo"] = value["lo"]
            results[key + ".ci95_hi"] = value["hi"]

    out["results"] = results
    return out


# --------------------------------------------------------------------------- #
# reproducibility check
# --------------------------------------------------------------------------- #
def _numeric_equal(a, b, tol: float = 1e-9) -> bool:
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(_numeric_equal(a[k], b[k], tol) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_numeric_equal(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, bool) or isinstance(b, bool):
        return a is b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if isinstance(a, float) and np.isnan(a):
            return isinstance(b, float) and np.isnan(b)
        return abs(float(a) - float(b)) <= tol
    return a == b


def _compare_results(old: dict, new: dict) -> tuple[bool, str]:
    for section in ("results", "aurocs", "paired_diffs", "denominators",
                    "alignment_assertions", "resampling"):
        if not _numeric_equal(old.get(section), new.get(section)):
            return False, section
    for field in ("seed", "n_boot", "alpha", "label", "command"):
        if old.get(field) != new.get(field):
            return False, field
    return True, "all compared sections match"


def main() -> int:
    global N_BOOT, SEED
    ap = argparse.ArgumentParser(description="R3-3b MF-17 post-hoc AUROC intervals.")
    ap.add_argument("--n-boot", type=int, default=N_BOOT)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--out", type=str, default=str(OUT_DEFAULT))
    ap.add_argument("--check-repro", action="store_true")
    args = ap.parse_args()

    n_boot = int(args.n_boot)
    seed = int(args.seed)
    if n_boot < 10000:
        ap.error("--n-boot must be >= 10000 for MF-17")
    N_BOOT, SEED = n_boot, seed

    result = build_result(n_boot=n_boot, seed=seed)
    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = ROOT / out_path

    if args.check_repro:
        if not out_path.exists():
            print("REPRO CHECK: FAIL (missing output file)", file=sys.stderr)
            return 1
        existing = json.loads(out_path.read_text(encoding="utf-8"))
        ok, detail = _compare_results(existing, result)
        print("REPRO CHECK:", "PASS" if ok else "FAIL", "|", detail)
        return 0 if ok else 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
    print("wrote", out_path)
    print("item MF-17 | post-hoc/exploratory | seed", seed, "| n_boot", n_boot)
    r = result["results"]
    for k in ("c1.r3_3b.mf17.frozen_held_out_auroc",
              "c1.r3_3b.mf17.corrected_held_out_auroc",
              "c1.r3_3b.mf17.paired_auroc_diff",
              "c1.r3_3b.mf17.top1_auroc",
              "c1.r3_3b.mf17.transfer_frozen_auroc",
              "c1.r3_3b.mf17.transfer_corrected_auroc",
              "c1.r3_3b.mf17.lexical_audit_auroc",
              "c1.r3_3b.mf17.gold_indicator_lexical_audit_auroc"):
        v = r[k]
        if "diff" in v:
            print(k, "=", round(v["diff"], 4), "[", round(v["lo"], 4), ",",
                  round(v["hi"], 4), "]")
        else:
            print(k, "=", round(v["point"], 4), "[", round(v["lo"], 4), ",",
                  round(v["hi"], 4), "]")
    print("n aurocs:", len(result["aurocs"]), "| n paired diffs:",
          len(result["paired_diffs"]), "| flat result keys:", len(result["results"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
