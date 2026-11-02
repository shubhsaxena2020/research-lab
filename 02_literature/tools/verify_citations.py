#!/usr/bin/env python
"""Citation resolution + verification for research-lab (RULES.md rule 1).

Every citation that appears in ANY draft must first be resolved against a real
bibliographic API and appended to 02_literature/verified_citations.csv.  This
tool is the only sanctioned way to do that.

Modes
-----
search   --query "..." [--limit N] [--source openalex|arxiv]
         Print compact candidate records (id, title, year, venue, cites, doi).
enrich   --in ids.txt --out enriched.jsonl
         Given arXiv ids / DOIs / OpenAlex ids (one per line), print and save
         title + abstract + authors + venue + year + citation count.
add      --in papers.jsonl --out staging/<agent>.csv [--strict]
         Verify each claimed paper.  Bibliographic fields in the output are
         taken FROM THE API, never from the claim.  A claim whose title does
         not match the resolved record is rejected, not repaired.
spotcheck --csv 02_literature/verified_citations.csv --n 20 [--seed 7]
         Re-resolve a random sample and report failures.

Polite-pool rules: one request at a time, 1 req/s to arXiv, 0.25 req/s to
OpenAlex, descriptive UA with mailto, exponential backoff on 429/5xx.
"""
from __future__ import annotations

import argparse
import csv
import difflib
import json
import os
import random
import re
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import date

import requests

UA = "research-lab/1.0 (mailto:shubh.saxena2020@gmail.com)"
HEADERS = {"User-Agent": UA, "Accept": "application/json"}
ARXIV_API = "http://export.arxiv.org/api/query"
OPENALEX = "https://api.openalex.org"
CROSSREF = "https://api.crossref.org"
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV_NS = "{http://arxiv.org/schemas/atom}"

CSV_FIELDS = [
    "id", "title", "authors", "year", "venue",
    "url", "doi_or_arxiv", "retrieved_on", "verified_by_command",
]

_last = {"arxiv": 0.0, "openalex": 0.0, "crossref": 0.0}


def _throttle(kind: str, gap: float) -> None:
    dt = time.time() - _last[kind]
    if dt < gap:
        time.sleep(gap - dt)
    _last[kind] = time.time()


def _get(url: str, kind: str = "openalex", tries: int = 4, **params):
    """GET with throttle + exponential backoff. Returns requests.Response or None."""
    gap = {"arxiv": 3.0, "openalex": 1.0, "crossref": 1.0}[kind]
    for attempt in range(tries):
        _throttle(kind, gap)
        try:
            r = requests.get(url, headers=HEADERS, params=params or None, timeout=40)
        except requests.RequestException as e:
            sys.stderr.write(f"  net error {type(e).__name__}: {e}\n")
            time.sleep(2 ** attempt * 3)
            continue
        if r.status_code == 200:
            return r
        if r.status_code in (429, 500, 502, 503, 504):
            wait = 2 ** attempt * 5
            sys.stderr.write(f"  {r.status_code} on {kind}; backoff {wait}s\n")
            time.sleep(wait)
            continue
        if r.status_code == 404:
            return None
        sys.stderr.write(f"  HTTP {r.status_code} on {url}\n")
        return None
    return None


# ---------------------------------------------------------------- normalisation
def norm(s: str) -> str:
    s = (s or "").lower()
    s = s.replace("\u2019", "'").replace("\u2018", "'")
    s = s.replace("\u2013", "-").replace("\u2014", "-")
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def sim(a: str, b: str) -> float:
    a, b = norm(a), norm(b)
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def arxiv_id_of(s: str) -> str | None:
    s = (s or "").strip()
    if not s:
        return None
    m = re.search(r"(?:arxiv[:./]|10\.48550/arxiv\.)\s*(\d{4}\.\d{4,6})(v\d+)?", s, re.I)
    if m:
        return m.group(1)
    m = re.search(r"(\d{4}\.\d{4,6})(v\d+)?", s)
    if m:
        return m.group(1)
    m = re.search(r"([a-z\-]+(?:\.[A-Z]{2})?/\d{7})(v\d+)?", s, re.I)  # old style cs/0701001
    if m:
        return m.group(1)
    return None


def doi_of(s: str) -> str | None:
    s = (s or "").strip()
    m = re.search(r"(10\.\d{4,9}/[^\s\"<>]+)", s)
    return m.group(1).rstrip(".,;") if m else None


def decode_abstract(inv: dict | None) -> str:
    if not inv:
        return ""
    pos: list[tuple[int, str]] = []
    for word, idxs in inv.items():
        for i in idxs:
            pos.append((i, word))
    pos.sort()
    return " ".join(w for _, w in pos)


# ---------------------------------------------------------------- resolvers
def arxiv_lookup(ids: list[str]) -> dict[str, dict]:
    """Batch-resolve arXiv ids -> record dicts keyed by bare id."""
    out: dict[str, dict] = {}
    for i in range(0, len(ids), 20):
        chunk = ids[i:i + 20]
        r = _get(ARXIV_API, "arxiv", id_list=",".join(chunk), max_results=len(chunk))
        if r is None:
            continue
        try:
            root = ET.fromstring(r.text)
        except ET.ParseError:
            continue
        for e in root.findall(f"{ATOM}entry"):
            raw_id = (e.findtext(f"{ATOM}id") or "").rsplit("/", 1)[-1]
            bare = re.sub(r"v\d+$", "", raw_id)
            title = " ".join((e.findtext(f"{ATOM}title") or "").split())
            authors = "; ".join(
                (a.findtext(f"{ATOM}name") or "").strip()
                for a in e.findall(f"{ATOM}author")
            )
            pub = (e.findtext(f"{ATOM}published") or "")[:4]
            journal = (e.findtext(f"{ARXIV_NS}journal_ref") or "").strip()
            doi = (e.findtext(f"{ARXIV_NS}doi") or "").strip()
            summary = " ".join((e.findtext(f"{ATOM}summary") or "").split())
            if not title or title.lower().startswith("error"):
                continue
            out[bare] = {
                "id": f"arxiv:{bare}",
                "title": title,
                "authors": authors,
                "year": pub,
                "venue": journal or "arXiv preprint",
                "url": f"https://arxiv.org/abs/{bare}",
                "doi_or_arxiv": doi or f"arXiv:{bare}",
                "abstract": summary,
                "cites": None,
                "source": "arxiv",
            }
    return out


def _openalex_record(w: dict) -> dict:
    src = ((w.get("primary_location") or {}).get("source") or {})
    venue = src.get("display_name") or ""
    doi = (w.get("doi") or "").replace("https://doi.org/", "")
    authors = "; ".join(
        (a.get("author") or {}).get("display_name", "")
        for a in (w.get("authorships") or [])
    )
    return {
        "id": w.get("id", "").rsplit("/", 1)[-1],
        "title": w.get("title") or w.get("display_name") or "",
        "authors": authors,
        "year": str(w.get("publication_year") or ""),
        "venue": venue,
        "url": w.get("id") or (f"https://doi.org/{doi}" if doi else ""),
        "doi_or_arxiv": doi or w.get("id", ""),
        "abstract": decode_abstract(w.get("abstract_inverted_index")),
        "cites": w.get("cited_by_count"),
        "source": "openalex",
    }


def openalex_by_doi(doi: str) -> dict | None:
    r = _get(f"{OPENALEX}/works/doi:{urllib.parse.quote(doi)}")
    if r is None:
        return None
    try:
        return _openalex_record(r.json())
    except Exception:
        return None


def openalex_search(title: str, limit: int = 5) -> list[dict]:
    r = _get(f"{OPENALEX}/works", search=title, per_page=limit,
             select="id,doi,title,display_name,publication_year,primary_location,"
                    "authorships,cited_by_count,abstract_inverted_index,type")
    if r is None:
        return []
    try:
        return [_openalex_record(w) for w in r.json().get("results", [])]
    except Exception:
        return []


def crossref_by_doi(doi: str) -> dict | None:
    r = _get(f"{CROSSREF}/works/{urllib.parse.quote(doi)}", "crossref")
    if r is None:
        return None
    try:
        m = r.json()["message"]
    except Exception:
        return None
    authors = "; ".join(
        f"{a.get('given','')} {a.get('family','')}".strip()
        for a in m.get("author", [])
    )
    parts = (m.get("issued", {}).get("date-parts") or [[None]])[0]
    return {
        "id": "doi:" + m.get("DOI", doi),
        "title": (m.get("title") or [""])[0],
        "authors": authors,
        "year": str(parts[0]) if parts and parts[0] else "",
        "venue": (m.get("container-title") or [""])[0],
        "url": f"https://doi.org/{m.get('DOI', doi)}",
        "doi_or_arxiv": m.get("DOI", doi),
        "abstract": re.sub(r"<[^>]+>", " ", m.get("abstract", "") or "").strip(),
        "cites": m.get("is-referenced-by-count"),
        "source": "crossref",
    }


def resolve(claim: dict) -> tuple[str, dict | None, float, str]:
    """Resolve one claim -> (status, record, title_similarity, command_string)."""
    key = claim.get("doi_or_arxiv") or claim.get("doi") or claim.get("arxiv") or ""
    axid = arxiv_id_of(key) or arxiv_id_of(claim.get("url", "")) or arxiv_id_of(claim.get("title", ""))
    doi = doi_of(key) or doi_of(claim.get("url", ""))

    if axid:
        rec = arxiv_lookup([axid]).get(axid)
        cmd = f"verify_citations.py add # arXiv id_list={axid}"
        if rec:
            s = sim(claim.get("title", ""), rec["title"])
            return ("VERIFIED" if s >= 0.90 else "MISMATCH"), rec, s, cmd
        # fall through to DOI/OpenAlex if arXiv entry vanished
    if doi:
        rec = openalex_by_doi(doi) or crossref_by_doi(doi)
        cmd = f"verify_citations.py add # doi={doi}"
        if rec:
            s = sim(claim.get("title", ""), rec["title"]) if claim.get("title") else 1.0
            return ("VERIFIED" if s >= 0.90 else "MISMATCH"), rec, s, cmd
        return "FAIL", None, 0.0, cmd

    title = claim.get("title", "")
    if not title:
        return "FAIL", None, 0.0, "verify_citations.py add # no identifier and no title"
    cands = openalex_search(title, limit=5)
    cmd = f"verify_citations.py add # openalex search={title[:70]!r}"
    if not cands:
        return "FAIL", None, 0.0, cmd
    best = max(cands, key=lambda c: sim(title, c["title"]))
    s = sim(title, best["title"])
    if claim.get("year"):
        try:
            if abs(int(str(claim["year"])[:4]) - int(best["year"])) > 1:
                s -= 0.05
        except Exception:
            pass
    return ("VERIFIED" if s >= 0.90 else "MISMATCH"), best, s, cmd


def make_row(rec: dict, cmd: str) -> dict:
    slug = re.sub(r"[^a-z0-9]+", "-", norm(rec["title"])[:60]).strip("-")
    return {
        "id": slug or rec["id"],
        "title": rec["title"],
        "authors": rec["authors"][:400],
        "year": rec["year"],
        "venue": rec["venue"][:200],
        "url": rec["url"],
        "doi_or_arxiv": rec["doi_or_arxiv"],
        "retrieved_on": date.today().isoformat(),
        "verified_by_command": cmd,
    }


# ---------------------------------------------------------------- commands
def cmd_search(a) -> None:
    rows: list[dict] = []
    if a.source in ("openalex", "both"):
        rows += openalex_search(a.query, limit=a.limit)
    if a.source in ("arxiv", "both"):
        r = _get(ARXIV_API, "arxiv", search_query=f'all:"{a.query}"',
                 max_results=a.limit, sortBy="relevance")
        if r is not None:
            try:
                root = ET.fromstring(r.text)
                for e in root.findall(f"{ATOM}entry"):
                    raw_id = (e.findtext(f"{ATOM}id") or "").rsplit("/", 1)[-1]
                    rows.append({
                        "id": "arxiv:" + re.sub(r"v\d+$", "", raw_id),
                        "title": " ".join((e.findtext(f"{ATOM}title") or "").split()),
                        "authors": "; ".join(
                            (x.findtext(f"{ATOM}name") or "")
                            for x in e.findall(f"{ATOM}author")),
                        "year": (e.findtext(f"{ATOM}published") or "")[:4],
                        "venue": "arXiv preprint",
                        "doi_or_arxiv": "arXiv:" + re.sub(r"v\d+$", "", raw_id),
                        "abstract": "", "cites": None, "source": "arxiv",
                    })
            except ET.ParseError:
                pass
    for r in rows:
        print(json.dumps({k: r.get(k) for k in
                          ("id", "title", "year", "venue", "doi_or_arxiv", "cites")},
                         ensure_ascii=False))
    print(f"-- {len(rows)} results", file=sys.stderr)


def cmd_enrich(a) -> None:
    ids = [ln.strip() for ln in open(a.inp, encoding="utf-8") if ln.strip()
           and not ln.startswith("#")]
    axids = [x for x in (arxiv_id_of(i) for i in ids) if x]
    got = arxiv_lookup(sorted(set(axids)))
    records: list[dict] = []
    seen_titles: set[str] = set()
    for i in ids:
        ax = arxiv_id_of(i)
        rec = got.get(ax) if ax else None
        if rec is None:
            d = doi_of(i)
            rec = (openalex_by_doi(d) or crossref_by_doi(d)) if d else openalex_by_doi(i)
        if rec is None:
            print(json.dumps({"id": i, "error": "unresolved"}), file=sys.stderr)
            continue
        if norm(rec["title"]) in seen_titles:
            continue
        seen_titles.add(norm(rec["title"]))
        records.append(rec)
    with open(a.out, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"-- enriched {len(records)}/{len(ids)} -> {a.out}", file=sys.stderr)


def cmd_add(a) -> None:
    claims = []
    with open(a.inp, encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln or ln.startswith("#"):
                continue
            claims.append(json.loads(ln))
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    new_file = not os.path.exists(a.out)
    stats = {"VERIFIED": 0, "MISMATCH": 0, "FAIL": 0, "DUPLICATE": 0}
    seen = set()
    if os.path.exists(a.out):
        with open(a.out, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                seen.add(norm(row.get("title", "")))
    with open(a.out, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if new_file:
            w.writeheader()
        for c in claims:
            status, rec, s, cmd = resolve(c)
            if status != "VERIFIED" or rec is None:
                stats[status] += 1
                print(json.dumps({"status": status, "claim": c.get("title", "")[:90],
                                  "sim": round(s, 3),
                                  "resolved": (rec or {}).get("title", "")[:90]},
                                 ensure_ascii=False))
                continue
            if norm(rec["title"]) in seen:
                stats["DUPLICATE"] += 1
                continue
            seen.add(norm(rec["title"]))
            w.writerow(make_row(rec, cmd))
            stats["VERIFIED"] += 1
    print(json.dumps(stats), file=sys.stderr)


def cmd_spotcheck(a) -> None:
    with open(a.csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    rng = random.Random(a.seed)
    sample = rng.sample(rows, min(a.n, len(rows)))
    bad = []
    for row in sample:
        key = row["doi_or_arxiv"]
        ax = arxiv_id_of(key) or arxiv_id_of(row["url"])
        rec = None
        if ax:
            rec = arxiv_lookup([ax]).get(ax)
            if rec is None:
                d = doi_of(key)
                rec = (openalex_by_doi(d) or crossref_by_doi(d)) if d else None
        else:
            d = doi_of(key) or doi_of(row["url"])
            rec = (openalex_by_doi(d) or crossref_by_doi(d)) if d else None
            if rec is None:
                cands = openalex_search(row["title"], limit=3)
                rec = max(cands, key=lambda c: sim(row["title"], c["title"])) if cands else None
        if rec is None:
            bad.append((row["title"][:80], "UNRESOLVED", 0.0))
            continue
        s = sim(row["title"], rec["title"])
        flag = "OK" if s >= 0.90 else "FAIL"
        if flag == "FAIL":
            bad.append((row["title"][:80], rec["title"][:80], round(s, 3)))
        print(f"{flag}\t{round(s,3)}\t{row['title'][:70]}")
    print(json.dumps({"checked": len(sample), "failed": len(bad),
                      "failures": bad}, ensure_ascii=False, indent=1))


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="mode", required=True)

    s = sub.add_parser("search")
    s.add_argument("--query", required=True)
    s.add_argument("--limit", type=int, default=10)
    s.add_argument("--source", default="openalex", choices=["openalex", "arxiv", "both"])
    s.set_defaults(fn=cmd_search)

    s = sub.add_parser("enrich")
    s.add_argument("--in", dest="inp", required=True)
    s.add_argument("--out", required=True)
    s.set_defaults(fn=cmd_enrich)

    s = sub.add_parser("add")
    s.add_argument("--in", dest="inp", required=True)
    s.add_argument("--out", required=True)
    s.set_defaults(fn=cmd_add)

    s = sub.add_parser("spotcheck")
    s.add_argument("--csv", required=True)
    s.add_argument("--n", type=int, default=20)
    s.add_argument("--seed", type=int, default=7)
    s.set_defaults(fn=cmd_spotcheck)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
