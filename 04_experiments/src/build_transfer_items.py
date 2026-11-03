"""Build the second-corpus transfer arm (2WikiMultihopQA dev -> 400 items).

Output: 04_experiments/data/transfer_items.jsonl
Schema: byte-identical field set to 04_experiments/data/items.jsonl.

Rung 0: question + the gold supporting paragraph (label 1).
Rung 3: question + a paragraph from the SAME question's article set that is NOT a
        gold/supporting paragraph and does not contain the gold answer (label 0).

2WikiMultihopQA has no "section" grouping: each question ships a candidate set of
independent Wikipedia articles (`context`: list of [title, [sentences]]). The
rung-3 "same article / near-miss" criterion is therefore operationalised as
"another paragraph drawn from the same question's context set" (i.e. the same
multi-hop article pool: gold articles plus distractors mined from them).

Deterministic: seed 20261103, questions iterated in sha1-sorted id order, single
shuffled pass, first 200 qualifying questions per rung.

Run: python 04_experiments/src/build_transfer_items.py
"""
import hashlib
import json
import random
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "04_experiments" / "data" / "raw" / "2wiki" / "2wikimultihop_dev.json"
OUT = ROOT / "04_experiments" / "data" / "transfer_items.jsonl"

SEED = 20261103
N_PER_RUNG = 200
MIN_CHARS, MAX_CHARS = 120, 1200
WS = re.compile(r"\s+")


def norm(s: str) -> str:
    return WS.sub(" ", s.replace("\u2013", "-").replace("\u2014", "-")).strip().casefold()


def para_text(sentences) -> str:
    return WS.sub(" ", " ".join(s.strip() for s in sentences)).strip()


def main() -> int:
    data = json.loads(SRC.read_text(encoding="utf-8"))
    order = sorted(data, key=lambda r: hashlib.sha1(r["_id"].encode()).hexdigest())
    random.Random(SEED).shuffle(order)

    rows, seen_q = [], set()
    stats = {"questions": len(data), "skipped_no_gold": 0, "skipped_no_distractor": 0}
    examples = {0: [], 3: []}

    for rec in order:
        if len([r for r in rows if r["rung"] == 0]) >= N_PER_RUNG and \
           len([r for r in rows if r["rung"] == 3]) >= N_PER_RUNG:
            break
        qid = rec["_id"]
        if qid in seen_q:
            continue
        answer = (rec.get("answer") or "").strip()
        question = (rec.get("question") or "").strip()
        if not answer or not question or len(answer) > 80 or answer.casefold() in {"yes", "no"}:
            stats["skipped_no_gold"] += 1
            continue

        paras = [(t, para_text(s)) for t, s in rec["context"]]
        sf_titles = [t for t, _ in rec["supporting_facts"]]
        nans = norm(answer)

        # ---- rung 0: the supporting paragraph that actually carries the answer
        gold = None
        for t, txt in paras:
            if t in sf_titles and nans in norm(txt) and MIN_CHARS <= len(txt) <= MAX_CHARS:
                gold = (t, txt)
                break
        if gold is None:
            stats["skipped_no_gold"] += 1
            continue

        gold_title, gold_txt = gold
        assert gold_title is not None

        # ---- rung 3: same article pool, not a supporting paragraph, no answer
        cands = [(t, txt) for t, txt in paras
                 if t != gold_title and t not in sf_titles
                 and MIN_CHARS <= len(txt) <= MAX_CHARS
                 and norm(txt) != norm(gold_txt)
                 and (len(nans) < 4 or nans not in norm(txt))]
        if not cands:
            stats["skipped_no_distractor"] += 1
            continue

        cands.sort(key=lambda p: (abs(len(p[1]) - len(gold_txt)), p[0]))
        dist = cands[0]
        seen_q.add(qid)

        if len([r for r in rows if r["rung"] == 0]) < N_PER_RUNG:
            rows.append(dict(anchor_token=None, context=gold[1], gold_answer=answer,
                             item_id=f"transfer:{qid}:r0", label=1,
                             n_context_chars=len(gold[1]), qid=qid, question=question,
                             replacement=None, rung=0, split="transfer", title=gold[0]))
        if len([r for r in rows if r["rung"] == 3]) < N_PER_RUNG:
            rows.append(dict(anchor_token=None, context=dist[1], gold_answer=None,
                             item_id=f"transfer:{qid}:r3", label=0,
                             n_context_chars=len(dist[1]), qid=qid, question=question,
                             replacement=None, rung=3, split="transfer", title=dist[0]))

    rows.sort(key=lambda r: (r["qid"], r["rung"]))
    # ---- integrity checks
    by_q = {}
    for r in rows:
        by_q.setdefault(r["qid"], {})[r["rung"]] = r
    assert len({r["item_id"] for r in rows}) == len(rows), "duplicate item_id"
    assert len(rows) == 2 * N_PER_RUNG, f"expected 400 rows, got {len(rows)}"
    assert len(by_q) == N_PER_RUNG, f"expected {N_PER_RUNG} qids, got {len(by_q)}"
    for qid, d in by_q.items():
        assert set(d) == {0, 3}, f"{qid} missing rung"
        assert norm(d[0]["context"]) != norm(d[3]["context"]), f"{qid} identical passages"
        assert norm(d[0]["question"]) == norm(d[3]["question"])
        assert d[0]["label"] == 1 and d[3]["label"] == 0
        ans = norm(d[0]["gold_answer"])
        assert ans in norm(d[0]["context"]), f"{qid} gold answer absent from rung0"
        assert len(ans) < 4 or ans not in norm(d[3]["context"]), f"{qid} answer leaks into rung3"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")

    digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
    # ---- how close do the rung-3 distractors get? (reported, not filtered)
    tok = re.compile(r"[a-z0-9]{4,}")

    def toks(s):
        return set(tok.findall(norm(s)))

    partial = 0
    for qid, d in by_q.items():
        shared = (toks(d[0]["gold_answer"]) - toks(d[0]["question"])) & toks(d[3]["context"])
        partial += bool(shared)
    print(f"rung3 passages sharing a >=4-char token with the gold answer "
          f"(excluding question tokens): {partial}/{len(by_q)}; full-answer leaks: 0")
    l0 = [r["n_context_chars"] for r in rows if r["rung"] == 0]
    l3 = [r["n_context_chars"] for r in rows if r["rung"] == 3]
    print(f"wrote {OUT} rows={len(rows)} sha256={digest}")
    print(f"rung0 n={len(l0)} chars median={statistics.median(l0):.0f} "
          f"rung3 n={len(l3)} chars median={statistics.median(l3):.0f}")
    print(f"unique qids={len(by_q)} skipped_no_gold={stats['skipped_no_gold']} "
          f"skipped_no_distractor={stats['skipped_no_distractor']}")
    print()
    for rung in (0, 3):
        print(f"--- rung {rung} examples ---")
        for r in [x for x in rows if x["rung"] == rung][:3]:
            print(f"[{r['item_id']}] label={r['label']} title={r['title']!r}")
            print(f"  Q: {r['question']}")
            print(f"  gold_answer: {r['gold_answer']}")
            print(f"  passage[:200]: {r['context'][:200]}")
            print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
