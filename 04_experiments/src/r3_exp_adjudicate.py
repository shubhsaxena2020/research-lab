"""R3 exploratory: adjudication sample — do rung 1-4 negatives really lack an answer?

Owned file: 04_experiments/src/r3_exp_adjudicate.py
Writes (under 04_experiments/results/c1/r3/exp/adjudication/):
    sample.csv      — 100 adjudication items: (item_id, rung, split, question, context, gold_answer)
    rubric.md       — written rubric for the annotation task
    label_A.csv     — template: (item_id, label, notes), label blank
    label_B.csv     — template: (item_id, label, notes), label blank
    resolve.csv     — template: (item_id, label, notes), label blank

Run:
    python 04_experiments/src/r3_exp_adjudicate.py           
    python 04_experiments/src/r3_exp_adjudicate.py --kappa

Sampling: negatives only (label == 0 and rung >= 1), stratified by rung:
25 items from each of rungs 1, 2, 3, 4 (100 total), seeded
``random.Random(20261103)``. Within each rung, items are sorted by
``item_id`` and then drawn with that RNG, so the sample is reproducible
regardless of the order of lines in items.jsonl.

--kappa reads label_A.csv and label_B.csv from the adjudication directory,
checks every sample item_id is labelled by both annotators, and prints
Cohen's kappa (overall and per rung) over the overlap. Labels are
``1`` (answerable), ``0`` (not answerable) or ``ambiguous`` (see rubric.md).

Note on interpretation: this adjudication is exploratory / post-hoc. The
positives (rung 0) are NOT sampled as controls, so this kappa does not
estimate false-unanswerable rates on answerable items.

Annotation disclosure: the labels in label_A.csv / label_B.csv / resolve.csv
are to be produced by independent annotators — which may be LLMs. If LLM
annotators are used, their identity (model name, version, prompt) must be
recorded alongside the labels; this script itself does not label anything
and must not be cited as an annotator.
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "04_experiments" / "data"
ITEMS_PATH = DATA / "items.jsonl"
OUT_DIR = ROOT / "04_experiments" / "results" / "c1" / "r3" / "exp" / "adjudication"
SAMPLE_CSV = OUT_DIR / "sample.csv"
RUBRIC_MD = OUT_DIR / "rubric.md"
LABEL_A_CSV = OUT_DIR / "label_A.csv"
LABEL_B_CSV = OUT_DIR / "label_B.csv"
RESOLVE_CSV = OUT_DIR / "resolve.csv"

SEED = 20261103
N_PER_RUNG = 25
RUNGS = (1, 2, 3, 4)

SAMPLE_COLUMNS = ["item_id", "rung", "split", "question", "context", "gold_answer"]
LABEL_COLUMNS = ["item_id", "label", "notes"]
VALID_LABELS = ("1", "0", "ambiguous")

RUBRIC_TEXT = """\
# Adjudication rubric — does the passage answer the question?

## Task

For each item in `sample.csv` you are shown a `question` and a `context`
(passage). Decide whether the passage, **on its own**, contains an answer
to the question.

## Labels

| label       | meaning                                                                 |
|-------------|-------------------------------------------------------------------------|
| `1`         | **answerable** — the passage states (or unambiguously entails) an answer to the question |
| `0`         | **not answerable** — the passage does not contain an answer to the question |
| `ambiguous` | the passage arguably contains a partial, indirect, or contradictory answer; you cannot decide confidently |

Record your decision in `label_A.csv` / `label_B.csv` as `label` and add a
short `notes` entry for every `ambiguous` item (cite the relevant span or
explain why it is partial / indirect / contradictory).

## Rules

1. Judge **only** from the passage. External knowledge does not count:
   if the correct answer is *true* but *not stated* in the passage, the
   label is `0`.
2. Paraphrase counts. The passage need not use the exact words of the
   answer — if a reader can extract the answer from the passage alone,
   the label is `1`. (For reference, `sample.csv` also carries the
   `gold_answer` from the source dataset; do not let it overrule the
   passage: a gold answer that is absent from the passage is `0`.)
3. A passage that answers a *different* question, or is on an unrelated
   topic, is `0`.
4. A passage that *mentions* the topic but omits the specific fact the
   question asks for is `0`.
5. Use `ambiguous` sparingly: only when the passage is partially,
   indirectly, or contradictorily responsive — not for items you merely
   find difficult. If you can point to a sentence that gives the answer,
   it is `1`.
6. Rung numbers in `sample.csv` are metadata about how the negative was
   constructed; they are not evidence for or against answerability.

## Quality checks

- Annotators label independently; do not discuss items before labelling.
- `resolve.csv` is completed afterwards: for every disagreement between
  the two annotators, record the final label and a one-line rationale in
  `notes`.
- Agreement is reported as Cohen's kappa (`--kappa` in
  `04_experiments/src/r3_exp_adjudicate.py`) and is exploratory / post-hoc.

## Annotator disclosure

If LLM annotators are used, record the model name, version and prompt
alongside the labels. An LLM is not a human gold standard; any
contradiction between an LLM label and the source dataset is resolved by
human adjudication.
"""


# --------------------------------------------------------------------- #
# pure helpers (unit-tested synthetically)
# --------------------------------------------------------------------- #
def load_items_jsonl(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def sample_negatives(items: list[dict], seed: int = SEED,
                     n_per_rung: int = N_PER_RUNG,
                     rungs: tuple[int, ...] = RUNGS) -> list[dict]:
    """Stratified sample of negatives (label == 0, rung >= 1).

    Deterministic: candidates within a rung are sorted by ``item_id`` before
    drawing, and one shared ``random.Random(seed)`` is used across rungs in
    ascending rung order.
    """
    rng = random.Random(int(seed))
    out: list[dict] = []
    for rung in rungs:
        cands = sorted(
            (it for it in items if it.get("label") == 0 and int(it.get("rung", -1)) == int(rung)),
            key=lambda it: str(it.get("item_id", "")),
        )
        if len(cands) < int(n_per_rung):
            raise ValueError(
                f"only {len(cands)} negative items at rung {rung}; need {n_per_rung}"
            )
        drawn = rng.sample(cands, int(n_per_rung))
        out.extend(drawn)
    return out


def cohens_kappa(a: list[str], b: list[str]) -> float | None:
    """Cohen's kappa for two paired label lists (any categorical labels).

    Returns None for an empty list. Returns 1.0 when both raters agree
    everywhere and there is a single category (pe = 1, po = 1).
    """
    if len(a) != len(b):
        raise ValueError(f"paired label lists differ in length: {len(a)} vs {len(b)}")
    n = len(a)
    if n == 0:
        return None
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    cats = set(a) | set(b)
    pa = collections.Counter(a)
    pb = collections.Counter(b)
    pe = sum((pa[c] / n) * (pb[c] / n) for c in cats)
    if pe >= 1.0:
        return 1.0 if po >= 1.0 else 0.0
    return (po - pe) / (1.0 - pe)


def agreement_report(labels_a: dict[str, str], labels_b: dict[str, str],
                     rung_by_id: dict[str, int] | None = None) -> dict:
    """Kappa over items labelled by both, overall and per rung."""
    common = sorted(set(labels_a) & set(labels_b))
    report: dict = {
        "n_common": len(common),
        "n_disagreed": sum(1 for i in common if labels_a[i] != labels_b[i]),
        "disagreements": [i for i in common if labels_a[i] != labels_b[i]],
        "kappa": cohens_kappa([labels_a[i] for i in common],
                               [labels_b[i] for i in common]),
    }
    if rung_by_id is not None:
        per_rung = {}
        rungs = sorted({int(rung_by_id[i]) for i in common if i in rung_by_id})
        for rung in rungs:
            ids = [i for i in common if int(rung_by_id[i]) == rung]
            per_rung[str(rung)] = {
                "n_common": len(ids),
                "n_disagreed": sum(1 for i in ids if labels_a[i] != labels_b[i]),
                "kappa": cohens_kappa([labels_a[i] for i in ids],
                                       [labels_b[i] for i in ids]),
            }
        report["per_rung"] = per_rung
    return report


# --------------------------------------------------------------------- #
# IO
# --------------------------------------------------------------------- #
def read_labels(path: Path) -> dict[str, str]:
    labels: dict[str, str] = {}
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != LABEL_COLUMNS:
            raise ValueError(f"{path.name}: columns {reader.fieldnames} != {LABEL_COLUMNS}")
        for row in reader:
            iid = (row.get("item_id") or "").strip()
            lab = (row.get("label") or "").strip()
            if not iid:
                continue
            if lab and lab not in VALID_LABELS:
                raise ValueError(f"{path.name}: invalid label {lab!r} for {iid!r}")
            labels[iid] = lab
    return labels


def read_sample_ids(path: Path) -> tuple[list[str], dict[str, int]]:
    ids: list[str] = []
    rung_by_id: dict[str, int] = {}
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            ids.append(row["item_id"])
            rung_by_id[row["item_id"]] = int(row["rung"])
    return ids, rung_by_id


def build_sample(items: list[dict]) -> list[dict]:
    """Project sampled items onto the sample.csv schema."""
    sampled = sample_negatives(items)
    return [
        {
            "item_id": it["item_id"],
            "rung": int(it["rung"]),
            "split": it["split"],
            "question": it.get("question") or "",
            "context": it.get("context") or "",
            "gold_answer": it.get("gold_answer") or "",
        }
        for it in sampled
    ]


def create_sample(out_dir: Path = OUT_DIR) -> list[dict]:
    """Write sample.csv (+ rubric + label templates) and return the rows."""
    items = load_items_jsonl(ITEMS_PATH)
    rows = build_sample(items)
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(out_dir / "sample.csv", "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=SAMPLE_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    (out_dir / "rubric.md").write_text(RUBRIC_TEXT, encoding="utf-8")

    for name in ("label_A.csv", "label_B.csv", "resolve.csv"):
        with open(out_dir / name, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=LABEL_COLUMNS)
            writer.writeheader()
            for row in rows:
                writer.writerow({"item_id": row["item_id"], "label": "", "notes": ""})
    return rows


def kappa_from_dir(out_dir: Path = OUT_DIR) -> dict:
    ids, rung_by_id = read_sample_ids(out_dir / "sample.csv")
    labels_a = read_labels(out_dir / "label_A.csv")
    labels_b = read_labels(out_dir / "label_B.csv")
    for name, labels in (("label_A.csv", labels_a), ("label_B.csv", labels_b)):
        missing = [i for i in ids if not labels.get(i)]
        extra = [i for i in labels if i not in set(ids)]
        if missing:
            raise ValueError(f"{name}: {len(missing)} of {len(ids)} items unlabelled, e.g. {missing[:5]}")
        if extra:
            raise ValueError(f"{name}: {len(extra)} unknown item_ids, e.g. {extra[:5]}")
    return agreement_report(labels_a, labels_b, rung_by_id=rung_by_id)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Adjudication sample (exploratory/post-hoc): create sample + templates, or --kappa.")
    ap.add_argument("--kappa", action="store_true",
                    help="read label_A.csv / label_B.csv and print Cohen's kappa")
    ap.add_argument("--out-dir", type=str, default=None,
                    help="adjudication output directory (default: results/c1/r3/exp/adjudication)")
    args = ap.parse_args(argv)
    out_dir = Path(args.out_dir) if args.out_dir else OUT_DIR
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir

    if args.kappa:
        report = kappa_from_dir(out_dir)
        print(f"n_common={report['n_common']} disagreements={report['n_disagreed']} "
              f"kappa={report['kappa']}")
        for rung, block in report.get("per_rung", {}).items():
            print(f"  rung {rung}: n={block['n_common']} disagreements={block['n_disagreed']} "
                  f"kappa={block['kappa']}")
        if report["disagreements"]:
            print("disagreed item_ids:", ", ".join(report["disagreements"]))
        return 0

    rows = create_sample(out_dir)
    print(f"wrote {out_dir / 'sample.csv'} ({len(rows)} rows)")
    for rung in RUNGS:
        print(f"  rung {rung}: {sum(1 for r in rows if r['rung'] == rung)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
