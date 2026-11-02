#!/usr/bin/env python3
"""Discovery-only helper: arXiv title-phrase search via the frozen tool, paced,
appending every hit to a JSONL so progress survives failures."""
import json, subprocess, sys, time, os

QUERIES = [q.strip() for q in open(sys.argv[1], encoding="utf-8") if q.strip()]
OUT = sys.argv[2]
seen = set()
if os.path.exists(OUT):
    for ln in open(OUT, encoding="utf-8"):
        try:
            seen.add(json.loads(ln)["id"])
        except Exception:
            pass

for q in QUERIES:
    for attempt in (1, 2, 3):
        p = subprocess.run(
            [sys.executable, "02_literature/tools/verify_citations.py", "search",
             "--source", "arxiv", "--query", q, "--limit", "6"],
            capture_output=True, text=True, timeout=180)
        rows = []
        for ln in p.stdout.splitlines():
            ln = ln.strip()
            if ln.startswith("{"):
                try:
                    rows.append(json.loads(ln))
                except Exception:
                    pass
        if rows:
            break
        time.sleep(15 * attempt)
    with open(OUT, "a", encoding="utf-8") as f:
        for r in rows:
            if r["id"] in seen:
                continue
            seen.add(r["id"])
            r["_q"] = q
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            print(f'{r["id"]}\t{r["year"]}\t{r["title"][:95]}')
    if not rows:
        print(f"!! none for: {q}")
    time.sleep(2)
print(f"-- total unique: {len(seen)}")
