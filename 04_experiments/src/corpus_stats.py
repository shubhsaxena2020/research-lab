"""Corpus facts quoted in the paper, computed from the downloaded SQuAD v2.0 dev file.

Run: python 04_experiments/src/corpus_stats.py
Writes: 04_experiments/data/squad_dev_stats.json
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "04_experiments" / "data" / "raw" / "dev-v2.0.json"
OUT = ROOT / "04_experiments" / "data" / "squad_dev_stats.json"


def main() -> int:
    blob = RAW.read_bytes()
    data = json.loads(blob)["data"]
    paragraphs = [p for a in data for p in a["paragraphs"]]
    qas = [q for p in paragraphs for q in p["qas"]]
    stats = {
        "generated_by": "04_experiments/src/corpus_stats.py",
        "source": "04_experiments/data/raw/dev-v2.0.json",
        "sha256": hashlib.sha256(blob).hexdigest(),
        "articles": len(data),
        "paragraphs": len(paragraphs),
        "questions": len(qas),
        "answerable": sum(1 for q in qas if not q["is_impossible"]),
        "impossible": sum(1 for q in qas if q["is_impossible"]),
    }
    OUT.write_text(json.dumps(stats, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(stats, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
