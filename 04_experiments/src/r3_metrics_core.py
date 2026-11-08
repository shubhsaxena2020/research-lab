"""R3-1 metrics core: definitions + recompute for frozen and corrected runs.

Owned file: 04_experiments/src/r3_metrics_core.py
Writes:
  04_experiments/results/c1/r3/metrics/DEFINITIONS.md
  04_experiments/results/c1/r3/metrics/metrics.json
  04_experiments/results/c1/r3/metrics/metrics.md

Run: python 04_experiments/src/r3_metrics_core.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC_REL = "04_experiments/src/r3_metrics_core.py"

FROZEN_PRED = ROOT / "04_experiments" / "results" / "c1" / "predictions.csv"
CORRECTED_PRED = ROOT / "04_experiments" / "results" / "c1_corrected" / "predictions.csv"
FROZEN_RESULTS = ROOT / "04_experiments" / "results" / "c1" / "results_full.json"
CORRECTED_RESULTS = ROOT / "04_experiments" / "results" / "c1_corrected" / "results_full.json"
TOP1 = ROOT / "04_experiments" / "results" / "c1" / "top1_variant.json"
OUT_DIR = ROOT / "04_experiments" / "results" / "c1" / "r3" / "metrics"

SEED = 20261103
COMMAND = "python 04_experiments/src/r3_metrics_core.py"

# Operating points available in predictions.csv.
POINTS = {"band": "band_refused", "exploratory_band": "expl_band_refused"}


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def refusal_rate_k(n_refused_rung: int, n_rung: int) -> float:
    """P(refused | negative of rung k)."""
    return n_refused_rung / max(1, n_rung)


def precision_k(n_refused_rung: int, n_refused_answerable: int) -> float | None:
    """P(negative of rung k | refused) = n_refused_rung/(n_refused_rung+n_refused_answerable)."""
    denom = n_refused_rung + n_refused_answerable
    if denom == 0:
        return None
    return n_refused_rung / denom


def pooled_precision(n_refused_neg: int, n_refused_ans: int) -> float | None:
    """P(negative | refused) over all items."""
    denom = n_refused_neg + n_refused_ans
    if denom == 0:
        return None
    return n_refused_neg / denom


def coverage_item(refused_flags: list[int]) -> float:
    """1 - mean(refused) over all items."""
    if not refused_flags:
        return 0.0
    return 1.0 - (sum(refused_flags) / len(refused_flags))


def coverage_question(rows: list[dict], col: str) -> tuple[float, int, int]:
    """(# qids whose rung-0 item is not refused) / (# qids)."""
    qids = sorted({r["qid"] for r in rows})
    n_answered = 0
    for q in qids:
        rung0 = [r for r in rows if r["qid"] == q and r["rung"] == "0"]
        if rung0 and rung0[0][col] != "1":
            n_answered += 1
    denom = len(qids)
    return (n_answered / max(1, denom), n_answered, denom)


def load_predictions(path: Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as fh:
        rows = [r for r in csv.DictReader(fh) if r["split"] == "test"]
    return rows


def compute_point(rows: list[dict], col: str) -> dict:
    pos = [r for r in rows if r["rung"] == "0"]
    n_pos = len(pos)
    n_refused_pos = sum(1 for r in pos if r[col] == "1")

    per_rung = {}
    tot_neg = 0
    tot_ref_neg = 0
    for k in ("1", "2", "3", "4"):
        neg = [r for r in rows if r["rung"] == k]
        if not neg:
            continue
        n_ref = sum(1 for r in neg if r[col] == "1")
        tot_neg += len(neg)
        tot_ref_neg += n_ref
        per_rung[k] = {
            "n": len(neg),
            "n_refused": n_ref,
            "refusal_rate": refusal_rate_k(n_ref, len(neg)),
            "abstain_precision": precision_k(n_ref, n_refused_pos),
        }

    ci = coverage_item([1 if r[col] == "1" else 0 for r in rows])
    cq, nq_ans, nq = coverage_question(rows, col)

    return {
        "refusal_column": col,
        "answerable": {
            "rung": 0,
            "n": n_pos,
            "n_refused": n_refused_pos,
            "refusal_rate": refusal_rate_k(n_refused_pos, n_pos),
            "label": "P(refused | answerable) = over_refusal",
        },
        "per_rung": per_rung,
        "pooled": {
            "n_negatives": tot_neg,
            "n_refused_negatives": tot_ref_neg,
            "n_refused_answerable": n_refused_pos,
            "abstain_recall_negatives": (tot_ref_neg / max(1, tot_neg)),
            "pooled_abstain_precision": pooled_precision(tot_ref_neg, n_refused_pos),
        },
        "coverage_item": ci,
        "coverage_question": cq,
        "coverage_question_n_answered": nq_ans,
        "coverage_question_n_qids": nq,
        "over_refusal": (n_refused_pos / max(1, n_pos)),
        "n_items": len(rows),
    }


def compute_run(rows: list[dict]) -> dict:
    return {point: compute_point(rows, col) for point, col in POINTS.items()}


def arms_from_results(results: dict) -> dict:
    out = {}
    for arm_name, arm in results.get("test", {}).items():
        per_rung_prec = {}
        for k, v in arm.get("per_rung", {}).items():
            per_rung_prec[k] = v.get("abstain_precision")
        out[arm_name] = {
            "gate": arm.get("gate"),
            "n_items": arm.get("n_items"),
            "coverage": arm.get("coverage"),
            "over_refusal": arm.get("over_refusal"),
            "pooled_abstain_precision": arm.get("pooled_abstain_precision"),
            "per_rung_abstain_precision": per_rung_prec,
        }
    return out


def top1_from_variant(variant: dict) -> dict:
    op = variant["operating_points"]["band_target_precision_0.80"]["test"]
    return {
        "operating_point": "band_target_precision_0.80",
        "split": "test",
        "refuse_miss": op.get("refusal_rate_misses"),  # P(refused | miss)
        "precision_miss_given_refused": op.get("precision_miss_given_refused"),  # P(miss | refused)
        "n_misses": op.get("n_misses"),
        "n_refused": op.get("n_refused"),
        "n_refused_misses": op.get("n_refused_misses"),
        "n_refused_hits": op.get("n_refused_hits"),
        "n_hits": op.get("n_hits"),
        "coverage": op.get("coverage"),
        "over_refusal": op.get("over_refusal"),
    }


def fmt_rate(x):
    if x is None:
        return "NA"
    return f"{x:.2f}"


def build_markdown(doc: dict) -> str:
    lines = []
    lines.append("# R3 metrics (core)")
    lines.append("")
    lines.append(f"Command: `{doc['command']}`")
    lines.append(f"Seed: {doc['seed']}")
    lines.append("")
    lines.append("## Inputs (sha256)")
    for k, v in doc["inputs"].items():
        lines.append(f"- {k}: `{v}`")
    lines.append("")
    for run_name in ("frozen", "corrected"):
        run = doc["runs"][run_name]
        lines.append(f"## Run: {run_name}")
        lines.append("")
        for point in ("band", "exploratory_band"):
            p = run["operating_points"][point]
            lines.append(f"### Operating point: {point} (column `{p['refusal_column']}`)")
            lines.append("")
            lines.append("| cell | n | n_refused | refusal_rate | abstain_precision |")
            lines.append("|---|---|---|---|---|")
            a = p["answerable"]
            lines.append(f"| answerable (rung 0) | {a['n']} | {a['n_refused']} | {fmt_rate(a['refusal_rate'])} | - |")
            for k in ("1", "2", "3", "4"):
                if k not in p["per_rung"]:
                    continue
                r = p["per_rung"][k]
                lines.append(f"| rung {k} | {r['n']} | {r['n_refused']} | {fmt_rate(r['refusal_rate'])} | {fmt_rate(r['abstain_precision'])} |")
            pl = p["pooled"]
            lines.append(f"| pooled negatives | {pl['n_negatives']} | {pl['n_refused_negatives']} | {fmt_rate(pl['abstain_recall_negatives'])} | {fmt_rate(pl['pooled_abstain_precision'])} |")
            lines.append("")
            lines.append(f"- coverage (item): {p['coverage_item']:.4f} -> {p['coverage_item']:.2f}")
            lines.append(f"- coverage (question): {p['coverage_question']:.4f} ({p['coverage_question_n_answered']}/{p['coverage_question_n_qids']})")
            lines.append(f"- over_refusal: {p['over_refusal']:.4f}")
            lines.append(f"- pooled precision: {pl['pooled_abstain_precision']}")
            lines.append("")
    lines.append("## Arms (from results_full.json)")
    lines.append("")
    lines.append("| run | arm | coverage | over_refusal | pooled_abstain_precision |")
    lines.append("|---|---|---|---|---|")
    for run_name in ("frozen", "corrected"):
        for arm, a in doc["arms"][run_name].items():
            lines.append(f"| {run_name} | {arm} | {fmt_rate(a['coverage'])} | {fmt_rate(a['over_refusal'])} | {fmt_rate(a['pooled_abstain_precision'])} |")
    lines.append("")
    lines.append("## Top-1 arm (band_target_precision_0.80, test)")
    lines.append("")
    t = doc["top1"]
    lines.append(f"- refuse_miss P(refused|miss) = {fmt_rate(t['refuse_miss'])} (n_misses={t['n_misses']})")
    lines.append(f"- precision_miss_given_refused P(miss|refused) = {fmt_rate(t['precision_miss_given_refused'])} (n_refused={t['n_refused']})")
    lines.append(f"- coverage = {fmt_rate(t['coverage'])}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    inputs = {
        "frozen_predictions": str(FROZEN_PRED.relative_to(ROOT).as_posix()),
        "corrected_predictions": str(CORRECTED_PRED.relative_to(ROOT).as_posix()),
        "frozen_results_full": str(FROZEN_RESULTS.relative_to(ROOT).as_posix()),
        "corrected_results_full": str(CORRECTED_RESULTS.relative_to(ROOT).as_posix()),
        "top1_variant": str(TOP1.relative_to(ROOT).as_posix()),
    }
    input_hashes = {k: sha256_file(ROOT / v) for k, v in inputs.items()}

    frozen_rows = load_predictions(FROZEN_PRED)
    corrected_rows = load_predictions(CORRECTED_PRED)
    frozen_results = json.loads(FROZEN_RESULTS.read_text(encoding="utf-8"))
    corrected_results = json.loads(CORRECTED_RESULTS.read_text(encoding="utf-8"))
    top1 = json.loads(TOP1.read_text(encoding="utf-8"))

    doc = {
        "experiment": "c1",
        "generated_by": SRC_REL,
        "command": COMMAND,
        "seed": SEED,
        "inputs": input_hashes,
        "input_paths": inputs,
        "definitions": {
            "refusal_rate_k": "P(refused | negative of rung k) = n_refused_rung_k / n_rung_k",
            "precision_k": "P(negative of rung k | refused) = n_refused_rung_k / (n_refused_rung_k + n_refused_answerable)",
            "pooled_precision": "P(negative | refused) over all items = n_refused_negatives / (n_refused_negatives + n_refused_answerable)",
            "coverage_item": "1 - mean(refused) over all items = admitted items / all items",
            "coverage_question": "(# qids whose rung-0 item is not refused) / (# qids)",
            "over_refusal": "P(refused | answerable) = n_refused_answerable / n_answerable",
            "abstain_recall": "P(refused | negative) pooled = n_refused_negatives / n_negatives",
        },
        "runs": {
            "frozen": {
                "source_predictions": inputs["frozen_predictions"],
                "operating_points": compute_run(frozen_rows),
            },
            "corrected": {
                "source_predictions": inputs["corrected_predictions"],
                "operating_points": compute_run(corrected_rows),
            },
        },
        "arms": {
            "frozen": arms_from_results(frozen_results),
            "corrected": arms_from_results(corrected_results),
        },
        "top1": top1_from_variant(top1),
    }

    # Write DEFINITIONS.md
    defs_path = OUT_DIR / "DEFINITIONS.md"
    defs_text = """# Metric definitions (R3-1)

- Abstain precision P(negative | refused): (number of refused items that are negatives) / (number of refused items); per-rung abstain precision restricts negatives to rung k: n_refused_rung_k / (n_refused_rung_k + n_refused_answerable).
- Per-rung refusal rate P(refused | negative of rung k): n_refused_rung_k / n_rung_k (abstain recall on that rung).
- Over-refusal P(refused | answerable): n_refused_answerable / n_answerable.
- Coverage (item population): 1 - mean(refused) over all items = admitted items / all items.
- Coverage (question population): (# qids whose rung-0 item is not refused) / (# qids).
- Abstain recall (pooled): n_refused_negatives / n_negatives.
"""
    defs_path.write_text(defs_text, encoding="utf-8")

    # Write metrics.json
    metrics_path = OUT_DIR / "metrics.json"
    metrics_path.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # Write metrics.md
    md_path = OUT_DIR / "metrics.md"
    md_path.write_text(build_markdown(doc), encoding="utf-8")

    # Print summary
    fb = doc["runs"]["frozen"]["operating_points"]["band"]
    fe = doc["runs"]["frozen"]["operating_points"]["exploratory_band"]
    cb = doc["runs"]["corrected"]["operating_points"]["band"]
    ce = doc["runs"]["corrected"]["operating_points"]["exploratory_band"]
    print("frozen band: pooled_precision=%.4f coverage_item=%.4f coverage_q=%.4f over_refusal=%.4f" % (
        fb["pooled"]["pooled_abstain_precision"], fb["coverage_item"], fb["coverage_question"], fb["over_refusal"]))
    print("frozen expl: pooled_precision=%.4f coverage_item=%.4f coverage_q=%.4f over_refusal=%.4f" % (
        fe["pooled"]["pooled_abstain_precision"], fe["coverage_item"], fe["coverage_question"], fe["over_refusal"]))
    print("corrected band: pooled_precision=%.4f coverage_item=%.4f coverage_q=%.4f over_refusal=%.4f" % (
        cb["pooled"]["pooled_abstain_precision"], cb["coverage_item"], cb["coverage_question"], cb["over_refusal"]))
    print("corrected expl: pooled_precision=%.4f coverage_item=%.4f coverage_q=%.4f over_refusal=%.4f" % (
        ce["pooled"]["pooled_abstain_precision"], ce["coverage_item"], ce["coverage_question"], ce["over_refusal"]))
    print("top1: refuse_miss=%.4f precision_miss_given_refused=%.4f coverage=%.4f" % (
        doc["top1"]["refuse_miss"], doc["top1"]["precision_miss_given_refused"], doc["top1"]["coverage"]))
    print("wrote", defs_path, metrics_path, md_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
