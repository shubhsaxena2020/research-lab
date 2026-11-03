"""C1 — stage 7: what the per-rung number actually is, and what precision actually is.

The pre-registration (§6) names "abstain precision = P(negative | refused)" but defines the estimator as
"the mean of the refusal indicator over that rung's negatives", which is P(refused | negative) — a recall
on that rung, not a precision. Round-2 review caught the contradiction. This script computes both, for
every operating point, from the committed per-item predictions:

  refusal_rate_k   = P(refused | negative of rung k)      the number the tables used to call "precision"
  precision_k      = P(negative of rung k | refused), computed over {R0 items, rung-k items}
  pooled_precision = P(negative | refused) over all negatives and answerables
  answer_rate      = P(admitted | R0) = 1 - over-refusal, i.e. questions actually answered

Run: python 04_experiments/src/precision_metrics.py
Writes: 04_experiments/results/c1/precision_metrics.json
        04_experiments/results/c1_corrected/precision_metrics.json
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNS = {
    "as_run": ROOT / "04_experiments" / "results" / "c1" / "predictions.csv",
    "corrected": ROOT / "04_experiments" / "results" / "c1_corrected" / "predictions.csv",
}
OUT = {
    "as_run": ROOT / "04_experiments" / "results" / "c1" / "precision_metrics.json",
    "corrected": ROOT / "04_experiments" / "results" / "c1_corrected" / "precision_metrics.json",
}
POINTS = {"band": "band_refused", "exploratory_band": "expl_band_refused"}


def block(rows: list[dict], column: str) -> dict:
    pos = [r for r in rows if int(r["rung"]) == 0]
    n_pos = len(pos)
    refused_pos = sum(1 for r in pos if r[column] == "1")
    out = {"n_answerable": n_pos, "n_refused_answerable": refused_pos,
           "over_refusal": round(refused_pos / max(1, n_pos), 4),
           "answer_rate": round(1.0 - refused_pos / max(1, n_pos), 4),
           "per_rung": {}}
    tot_neg = tot_ref_neg = 0
    for k in ("1", "2", "3", "4"):
        neg = [r for r in rows if r["rung"] == k]
        if not neg:
            continue
        ref = sum(1 for r in neg if r[column] == "1")
        tot_neg += len(neg)
        tot_ref_neg += ref
        out["per_rung"][k] = {
            "n": len(neg),
            "n_refused": ref,
            "refusal_rate": round(ref / len(neg), 4),
            "precision": round(ref / (ref + refused_pos), 4) if (ref + refused_pos) else None,
            "precision_note": "P(negative of this rung | refused), denominator = this rung's refusals + "
                              "the refused answerable items",
        }
    out["pooled"] = {
        "n_negatives": tot_neg,
        "n_refused_negatives": tot_ref_neg,
        "refusal_rate": round(tot_ref_neg / max(1, tot_neg), 4),
        "precision": round(tot_ref_neg / (tot_ref_neg + refused_pos), 4)
        if (tot_ref_neg + refused_pos) else None,
    }
    return out


def main() -> int:
    for name, path in RUNS.items():
        if not path.exists():
            raise SystemExit(f"missing {path}")
        with open(path, encoding="utf-8", newline="") as fh:
            rows = [r for r in csv.DictReader(fh) if r["split"] == "test"]
        doc = {
            "experiment": "c1",
            "run": name,
            "source": str(path.relative_to(ROOT).as_posix()),
            "generated_by": "04_experiments/src/precision_metrics.py",
            "definitions": {
                "refusal_rate": "P(refused | negative of that rung) — a recall on the rung",
                "precision": "P(negative of that rung | refused), over that rung's items and the "
                             "answerable items together",
                "answer_rate": "P(admitted | answerable) — the share of questions actually answered",
            },
            "operating_points": {},
        }
        for point, column in POINTS.items():
            doc["operating_points"][point] = block(rows, column)
        OUT[name].parent.mkdir(parents=True, exist_ok=True)
        OUT[name].write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        b = doc["operating_points"]["band"]
        e = doc["operating_points"]["exploratory_band"]
        print(f"{name}: band refusal R2={b['per_rung']['2']['refusal_rate']:.4f} "
              f"precision R2={b['per_rung']['2']['precision']:.4f} pooled precision={b['pooled']['precision']:.4f} "
              f"answer_rate={b['answer_rate']:.4f} | exploratory refusal R2="
              f"{e['per_rung']['2']['refusal_rate']:.4f} precision R2={e['per_rung']['2']['precision']:.4f} "
              f"answer_rate={e['answer_rate']:.4f}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
