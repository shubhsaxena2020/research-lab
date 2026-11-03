#!/usr/bin/env python
"""S2b OpenAlex harvest v3 — polite, cached, bounded.

Measured facts (2026-11-03, this IP):
  * ?search= costs 10 credits of a 1000-credit anonymous daily budget -> ~100 searches/day.
  * The anonymous *search cluster* intermittently returns 429 "temporarily rate-limited while
    the search cluster is under elevated load ... retry in Ns". That 429 costs nothing.
Policy: pace at 2.5 s/request; on such a 429 wait the server's own N (+3 s) and retry the SAME
query at most 3 times; after 3 consecutive 429s stop the whole run and record the timestamp.
A budget 429 (remaining == 0) stops immediately.
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
GAP = 2.5
MIN_CREDITS = 80


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
    last, fresh, consecutive_429, remaining = 0.0, 0, 0, None

    for fam, kind, q in jobs:
        if q in done:
            continue
        for attempt in range(1, 4):
            dt = time.time() - last
            if dt < GAP:
                time.sleep(GAP - dt)
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
                       "n_returned": len(j.get("results") or []),
                       "remaining": remaining,
                       "cache": os.path.relpath(path, ROOT).replace("\\", "/"),
                       "attempts": attempt}
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
                consecutive_429 = 0
                print(f"200 {fam}/{kind} count={row['count']} rem={remaining} "
                      f"att={attempt} :: {q}")
                try:
                    if remaining is not None and int(remaining) < MIN_CREDITS:
                        print("LOW BUDGET — stop.")
                        qf.close(); hf.close(); return 4
                except ValueError:
                    pass
                break
            if r.status_code == 401 or r.status_code == 403:
                print("AUTH", r.status_code, r.text[:150])
                qf.close(); hf.close(); return 3
            consecutive_429 += 1
            m = re.search(r"retry in (\d+)s", r.text)
            wait = int(m.group(1)) + 3 if m else 20
            print(f"{r.status_code} {fam}/{kind} attempt={attempt} rem={remaining} "
                  f"wait={wait}s :: {q} :: {r.text[:110]}")
            qf.write(json.dumps({"family": fam, "kind": kind, "query": q,
                                 "status": r.status_code, "at": ts, "remaining": remaining,
                                 "attempt": attempt, "wait_s": wait}) + "\n")
            qf.flush()
            if remaining == "0":
                qf.close(); hf.close(); print("BUDGET 429 — stop."); return 5
            if attempt < 3:
                time.sleep(wait)
                continue
            qf.write(json.dumps({"family": fam, "kind": kind, "query": "<STOP>",
                                 "status": "ABORTED_429", "at": ts}) + "\n")
            qf.close(); hf.close()
            print("three 429s in a row — stopping and recording.")
            return 2
    qf.close(); hf.close()
    print(f"done: {fresh} fresh, {len(seen)} unique works")
    return 0


if __name__ == "__main__":
    sys.exit(main())
