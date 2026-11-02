#!/usr/bin/env python
"""Drive verify_citations.py search over the S2-10 novelty pre-scan query list.

Appends one JSON object per query to S2-10-queries.jsonl:
  {family, query, source, results, date, top: [{title, year, id}...]}

Usage: python S2-10-run_queries.py <start> <end>
Reads the query list from S2-10-querylist.json.
Never invents a count: `results` is the number printed by the tool's
'-- N results' stderr line, or "ERROR: <message>" when the tool failed.
"""
import json
import os
import re
import subprocess
import sys
import time
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TOOL = os.path.join(ROOT, "02_literature", "tools", "verify_citations.py")
LOG = os.path.join(HERE, "S2-10-queries.jsonl")
LIST = os.path.join(HERE, "S2-10-querylist.json")
SOURCE = os.environ.get("S2_SOURCE", "arxiv")
LIMIT = 10


def run(family, query):
    cmd = [sys.executable, TOOL, "search", "--query", query,
           "--limit", str(LIMIT), "--source", SOURCE]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, timeout=300)
    out, err = p.stdout, p.stderr
    fail = re.search(r"(\d{3} on \w+|net error \w+|HTTP \d{3})", err)
    m = re.search(r"--\s*(\d+)\s+results", err)
    if fail:
        return {"family": family, "query": query, "source": SOURCE,
                "results": "ERROR: " + fail.group(1),
                "date": date.today().isoformat(), "top": []}
    if not m:
        return {"family": family, "query": query, "source": SOURCE,
                "results": "ERROR: no count line; " + err.strip()[-200:],
                "date": date.today().isoformat(), "top": []}
    top = []
    for line in out.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        top.append({"title": r.get("title", ""), "year": r.get("year", ""),
                    "id": r.get("id", "")})
    return {"family": family, "query": query, "source": SOURCE,
            "results": int(m.group(1)), "date": date.today().isoformat(),
            "top": top}


def main():
    a, b = int(sys.argv[1]), int(sys.argv[2])
    items = json.load(open(LIST, encoding="utf-8"))
    done = set()
    if os.path.exists(LOG):
        for ln in open(LOG, encoding="utf-8"):
            ln = ln.strip()
            if not ln:
                continue
            try:
                rec = json.loads(ln)
            except Exception:
                continue
            if not str(rec.get("results", "")).startswith("ERROR"):
                done.add(rec["query"])
    with open(LOG, "a", encoding="utf-8") as f:
        for fam, q in items[a:b]:
            if q in done:
                print(f"skip {q}")
                continue
            rec = run(fam, q)
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
            print(f"{fam}\t{rec['results']}\t{q}", flush=True)
            time.sleep(4.0)


if __name__ == "__main__":
    main()
