#!/usr/bin/env python
"""S2b probe: is OpenAlex's daily budget back? Is Semantic Scholar reachable?

Writes nothing outside the lab. One request per source, printed verdict.
"""
import json
import sys
import time

import requests

UA = "research-lab-s2b/1.0 (mailto:shubh.saxena2020@gmail.com)"
H = {"User-Agent": UA, "Accept": "application/json"}

q = "two-threshold abstention retrieval"
t0 = time.time()
r = requests.get("https://api.openalex.org/works",
                 headers=H,
                 params={"search": q, "per_page": 2, "mailto": "shubh.saxena2020@gmail.com"},
                 timeout=40)
print("OPENALEX status", r.status_code, "elapsed %.2fs" % (time.time() - t0))
for k in ("X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Reset",
          "Retry-After", "x-ratelimit-remaining"):
    if k in r.headers:
        print("  header", k, "=", r.headers[k])
if r.status_code == 200:
    j = r.json()
    print("  meta.count =", j.get("meta", {}).get("count"))
    for w in j.get("results", [])[:2]:
        print("   -", w.get("publication_year"), "|", (w.get("title") or "")[:90])
else:
    print("  body:", r.text[:300])

time.sleep(3)
t0 = time.time()
r2 = requests.get("https://api.semanticscholar.org/graph/v1/paper/search",
                  headers=H,
                  params={"query": q, "limit": 2, "fields": "title,year,venue,externalIds"},
                  timeout=40)
print("SEMANTIC SCHOLAR status", r2.status_code, "elapsed %.2fs" % (time.time() - t0))
if r2.status_code == 200:
    j2 = r2.json()
    print("  total =", j2.get("total"))
    for p in j2.get("data", [])[:2]:
        print("   -", p.get("year"), "|", (p.get("title") or "")[:90])
else:
    print("  body:", r2.text[:300])

sys.exit(0)
