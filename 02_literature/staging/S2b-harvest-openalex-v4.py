#!/usr/bin/env python
"""S2b OpenAlex harvest v4 — adaptive pacing against the anonymous search-cluster 429.

What the 429s actually are (observed, 2026-11-03 00:12-00:22 UTC):
  {"error":"Rate limit exceeded","message":"Anonymous search is temporarily rate-limited while
   the search cluster is under elevated load. Please retry in Ns ..."}   (no quota header)
That is a cluster-load throttle on anonymous *search* calls, not the daily budget: successful
calls report X-RateLimit-Remaining and cost 10 credits each. It clears if you wait the N seconds.
Policy, written down so it can be audited: adaptive gap 6->20 s (grow on failure, shrink on
success), max 4 attempts per query with the server's own wait, a query that fails 4 times is
recorded SKIP429 and the run continues; 5 consecutive such queries stops the run for good.
"""
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone

import requests

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(LAB)
RAW = os.path.join(LAB, "raw", "openalex")
STAGE = os.path.join(LAB, "staging")
os.makedirs(RAW, exist_ok=True)

H = {"User-Agent": "research-lab-s2b/1.0 (mailto:shubh.saxena2020@gmail.com)",
     "Accept": "application/json"}
MAIL = "shubh.saxena2020@gmail.com"
SELECT = ("id,doi,title,publication_year,publication_date,primary_location,authorships,"
          "cited_by_count,abstract_inverted_index,type,language,open_access")
MIN_CREDITS = 40


def slug(q):
    s = re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-")[:60]
    return f"{s}-{hashlib.sha1(q.encode()).hexdigest()[:8]}"


def decode(inv):
    if not inv:
        return ""
    pos = []
    for w, idxs in inv.items():
        for i in idxs:
            pos.append((i, w))
    pos.sort()
    return " ".join(w for _, w in pos)


def rec(w):
    src = ((w.get("primary_location") or {}).get("source") or {})
    doi = (w.get("doi") or "").replace("https://doi.org/", "")
    return {"openalex_id": (w.get("id") or "").rsplit("/", 1)[-1],
            "title": w.get("title") or "", "year": w.get("publication_year"),
            "date": w.get("publication_date"), "venue": src.get("display_name") or "",
            "doi": doi, "url": w.get("id") or "", "cites": w.get("cited_by_count"),
            "type": w.get("type"), "language": w.get("language"),
            "oa": ((w.get("open_access") or {}).get("oa_url") or ""),
            "authors": "; ".join((a.get("author") or {}).get("display_name", "")
                                 for a in (w.get("authorships") or [])),
            "abstract": decode(w.get("abstract_inverted_index"))}


def main():
    ql = json.load(open(os.path.join(STAGE, "S2b-querylist.json"), encoding="utf-8"))
    jobs = [(fam, kind, q) for fam in ("A", "D") for kind in ("base", "new")
            for q in ql["families"][fam][kind]]
    qfile = os.path.join(STAGE, "S2b-openalex-queries.jsonl")
    hfile = os.path.join(STAGE, "S2b-openalex-hits.jsonl")

    done, seen = set(), set()
    if os.path.exists(qfile):
        for ln in open(qfile, encoding="utf-8"):
            try:
                r = json.loads(ln)
                if r.get("status") == 200:
                    done.add(r["query"])
            except Exception:
                pass
    if os.path.exists(hfile):
        for ln in open(hfile, encoding="utf-8"):
            try:
                seen.add(json.loads(ln)["openalex_id"])
            except Exception:
                pass

    qf = open(qfile, "a", encoding="utf-8")
    hf = open(hfile, "a", encoding="utf-8")
    gap, last, fresh, skipped_streak, remaining = 5.0, 0.0, 0, 0, None

    for fam, kind, q in jobs:
        if q in done:
            continue
        got = False
        for attempt in range(1, 5):
            dt = time.time() - last
            if dt < gap:
                time.sleep(gap - dt)
            last = time.time()
            ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            try:
                r = requests.get("https://api.openalex.org/works", headers=H,
                                 params={"search": q, "per_page": 50, "select": SELECT,
                                         "mailto": MAIL}, timeout=45)
            except requests.RequestException as e:
                qf.write(json.dumps({"family": fam, "kind": kind, "query": q,
                                     "status": "NETERR", "error": type(e).__name__, "at": ts}) + "\n")
                qf.flush()
                print("NETERR", q)
                break
            remaining = r.headers.get("X-RateLimit-Remaining")
            if r.status_code == 200:
                j = r.json()
                path = os.path.join(RAW, slug(q) + ".json")
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(j, f)
                row = {"family": fam, "kind": kind, "query": q, "status": 200, "at": ts,
                       "count": (j.get("meta") or {}).get("count"),
                       "n_returned": len(j.get("results") or []), "remaining": remaining,
                       "gap_s": round(gap, 1), "attempts": attempt,
                       "cache": os.path.relpath(path, ROOT).replace("\\", "/")}
                for w in j.get("results") or []:
                    d = rec(w)
                    if not d["openalex_id"] or d["openalex_id"] in seen:
                        continue
                    seen.add(d["openalex_id"])
                    d["found_by"] = q
                    hf.write(json.dumps(d, ensure_ascii=False) + "\n")
                qf.write(json.dumps(row) + "\n")
                qf.flush(); hf.flush()
                fresh += 1
                got = True
                skipped_streak = 0
                gap = max(5.0, gap - 1.0)
                print(f"200 {fam}/{kind} count={row['count']} rem={remaining} "
                      f"gap={gap:.0f} att={attempt} :: {q}")
                if remaining is not None and remaining.isdigit() and int(remaining) < MIN_CREDITS:
                    print("LOW BUDGET — stop.")
                    qf.close(); hf.close(); return 4
                break
            if r.status_code in (401, 403):
                print("AUTH", r.status_code, r.text[:150])
                qf.close(); hf.close(); return 3
            m = re.search(r"retry in (\d+)s", r.text)
            wait = int(m.group(1)) + 4 if m else 30
            gap = min(20.0, gap + 3.0)
            qf.write(json.dumps({"family": fam, "kind": kind, "query": q, "status": r.status_code,
                                 "at": ts, "attempt": attempt, "wait_s": wait,
                                 "remaining": remaining}) + "\n")
            qf.flush()
            print(f"{r.status_code} att={attempt} wait={wait}s gap->{gap:.0f} :: {q}")
            if r.status_code == 429 and remaining == "0":
                print("BUDGET EXHAUSTED — stop.")
                qf.close(); hf.close(); return 5
            if attempt < 4:
                time.sleep(wait)
        if not got:
            skipped_streak += 1
            qf.write(json.dumps({"family": fam, "kind": kind, "query": q, "status": "SKIP429",
                                 "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}) + "\n")
            qf.flush()
            print(f"SKIP after 4 attempts: {q} (streak {skipped_streak})")
            if skipped_streak >= 5:
                qf.write(json.dumps({"family": fam, "kind": kind, "query": "<STOP>",
                                     "status": "ABORTED_429_STREAK",
                                     "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}) + "\n")
                qf.close(); hf.close()
                print("5 consecutive skipped queries — stopping OpenAlex use for this session.")
                return 2
    qf.close(); hf.close()
    print(f"done: {fresh} fresh this run, {len(seen)} unique works, {len(done)+fresh}/{len(jobs)} queries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
