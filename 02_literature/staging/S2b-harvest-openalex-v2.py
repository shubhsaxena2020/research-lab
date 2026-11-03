#!/usr/bin/env python
"""S2b OpenAlex harvest — one request at a time, >=1.2 s apart, cache every body.

Reads 02_literature/staging/S2b-querylist.json, writes
  02_literature/raw/openalex/<slug>.json          raw response per query
  02_literature/staging/S2b-openalex-queries.jsonl one row per query (status, count)
  02_literature/staging/S2b-openalex-hits.jsonl    one row per unique work (deduped)

On HTTP 429: record the time in the queries file and STOP (prompt rule: do not retry in a loop).
"""
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone

import requests

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 02_literature/
ROOT = os.path.dirname(LAB)
RAW = os.path.join(LAB, "raw", "openalex")
STAGE = os.path.join(LAB, "staging")
os.makedirs(RAW, exist_ok=True)

UA = "research-lab-s2b/1.0 (mailto:shubh.saxena2020@gmail.com)"
H = {"User-Agent": UA, "Accept": "application/json"}
MAIL = "shubh.saxena2020@gmail.com"
SELECT = ("id,doi,title,publication_year,publication_date,primary_location,authorships,"
          "cited_by_count,abstract_inverted_index,type,language,open_access")
GAP = 1.2          # seconds between requests
MIN_CREDITS = 80   # stop before spending the IP's remaining budget on nothing


def slug(q: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-")[:60]
    h = hashlib.sha1(q.encode()).hexdigest()[:8]
    return f"{s}-{h}"


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
    return {
        "openalex_id": (w.get("id") or "").rsplit("/", 1)[-1],
        "title": w.get("title") or "",
        "year": w.get("publication_year"),
        "date": w.get("publication_date"),
        "venue": src.get("display_name") or "",
        "doi": doi,
        "url": w.get("id") or "",
        "cites": w.get("cited_by_count"),
        "type": w.get("type"),
        "language": w.get("language"),
        "oa": ((w.get("open_access") or {}).get("oa_url") or ""),
        "authors": "; ".join((a.get("author") or {}).get("display_name", "")
                             for a in (w.get("authorships") or [])),
        "abstract": decode(w.get("abstract_inverted_index")),
    }


def main():
    ql = json.load(open(os.path.join(STAGE, "S2b-querylist.json"), encoding="utf-8"))
    jobs = []
    for fam in ("A", "D"):
        for kind in ("base", "new"):
            for q in ql["families"][fam][kind]:
                jobs.append((fam, kind, q))

    qfile = os.path.join(STAGE, "S2b-openalex-queries.jsonl")
    hfile = os.path.join(STAGE, "S2b-openalex-hits.jsonl")
    done = set()
    if os.path.exists(qfile):
        for ln in open(qfile, encoding="utf-8"):
            try:
                r = json.loads(ln)
            except Exception:
                continue
            if r.get("status") == 200:
                done.add(r["query"])
    seen_works = set()
    if os.path.exists(hfile):
        for ln in open(hfile, encoding="utf-8"):
            try:
                seen_works.add(json.loads(ln)["openalex_id"])
            except Exception:
                pass

    qf = open(qfile, "a", encoding="utf-8")
    hf = open(hfile, "a", encoding="utf-8")
    last = 0.0
    fresh = 0
    for fam, kind, q in jobs:
        if q in done:
            print(f"SKIP (cached) {fam}/{kind}: {q}")
            continue
        dt = time.time() - last
        if dt < GAP:
            time.sleep(GAP - dt)
        last = time.time()
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        params = {"search": q, "per_page": 50, "select": SELECT, "mailto": MAIL}
        try:
            r = requests.get("https://api.openalex.org/works", headers=H, params=params, timeout=45)
        except requests.RequestException as e:
            qf.write(json.dumps({"family": fam, "kind": kind, "query": q, "status": "NETERR",
                                 "error": type(e).__name__, "at": ts}) + "\n")
            qf.flush()
            print(f"NETERR {q}")
            continue
        row = {"family": fam, "kind": kind, "query": q, "status": r.status_code, "at": ts,
               "remaining": r.headers.get("X-RateLimit-Remaining")}
        if r.status_code == 200:
            j = r.json()
            path = os.path.join(RAW, slug(q) + ".json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(j, f)
            row["count"] = (j.get("meta") or {}).get("count")
            row["n_returned"] = len(j.get("results") or [])
            row["cache"] = os.path.relpath(path, ROOT).replace("\\", "/")
            for w in j.get("results") or []:
                d = rec(w)
                if not d["openalex_id"] or d["openalex_id"] in seen_works:
                    continue
                seen_works.add(d["openalex_id"])
                d["found_by"] = [q]
                hf.write(json.dumps(d, ensure_ascii=False) + "\n")
            fresh += 1
        qf.write(json.dumps(row) + "\n")
        qf.flush()
        hf.flush()
        print(f"{r.status_code} {fam}/{kind} count={row.get('count')} rem={row.get('remaining')} :: {q}")
        if r.status_code == 429:
            print("429 — recording and stopping OpenAlex use (prompt rule). body:", r.text[:200])
            qf.write(json.dumps({"family": fam, "kind": kind, "query": "<STOP>",
                                 "status": "ABORTED_429", "at": ts}) + "\n")
            qf.close(); hf.close()
            return 2
        try:
            if r.status_code == 200 and int(row.get("remaining") or 9999) < MIN_CREDITS:
                print("LOW BUDGET — stopping so the IP keeps a reserve.")
                qf.close(); hf.close()
                return 4
        except ValueError:
            pass
        if r.status_code in (401, 403):
            print("AUTH/403 — stopping:", r.text[:200])
            qf.close(); hf.close()
            return 3
    qf.close(); hf.close()
    print(f"done: {fresh} fresh queries, {len(seen_works)} unique works cached")
    return 0


if __name__ == "__main__":
    sys.exit(main())
