"""S2-6 discovery helper: Crossref bibliographic search only.

Discovery is not verification. Everything found here is fed to
verify_citations.py add, which re-resolves each DOI through Crossref and
applies the 0.90 title-similarity gate. Writes JSONL of raw candidates.
"""
import json
import sys
import time
import urllib.parse
import urllib.request

UA = "research-lab/1.0 (mailto:shubh.saxena2020@gmail.com)"
BASE = "https://api.crossref.org/works"


def q(query, rows=8, extra=None):
    params = {"query.bibliographic": query, "rows": str(rows),
              "select": "DOI,title,issued,container-title,author,is-referenced-by-count,type",
              "mailto": "shubh.saxena2020@gmail.com"}
    if extra:
        params.update(extra)
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                data = json.load(r)
            return data["message"]["items"]
        except Exception as e:
            wait = 5 * (2 ** attempt)
            sys.stderr.write(f"  retry {attempt} {e} wait {wait}s\n")
            time.sleep(wait)
    return []


def show(query, rows=8):
    print(f"=====Q: {query}")
    for it in q(query, rows):
        title = (it.get("title") or [""])[0]
        year = ""
        try:
            year = str(it["issued"]["date-parts"][0][0])
        except Exception:
            pass
        venue = (it.get("container-title") or [""])[0]
        print(json.dumps({"doi": it.get("DOI"), "title": " ".join(title.split()),
                          "year": year, "venue": venue[:90],
                          "cites": it.get("is-referenced-by-count")},
                         ensure_ascii=False))
    time.sleep(1.2)


if __name__ == "__main__":
    for line in sys.stdin.read().splitlines():
        line = line.strip()
        if line:
            show(line)
