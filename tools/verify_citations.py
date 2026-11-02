#!/usr/bin/env python
"""verify_citations.py — resolve every citation against a real bibliographic API.

RULES.md #1 is the reason this tool exists: a citation may appear in a draft only if it has
been resolved against a live API, and the resolution evidence is recorded. This tool does
that and refuses to be generous about it.

    python tools/verify_citations.py --csv 02_literature/citations.csv --online
    python tools/verify_citations.py --bib 05_paper/template/refs.bib --online
    python tools/verify_citations.py --csv ... --offline      # cache-only, no network

Resolution order per record (first hit wins, later ones only fill gaps):
    1. DOI      -> Crossref  (10.48550/arXiv.* DOIs are routed to the arXiv API, because
                              arXiv registers them with DataCite and Crossref 404s them)
    2. arXiv id -> arXiv export API
    3. title    -> OpenAlex, then Semantic Scholar

Verdict rules (thresholds are CLI-tunable, defaults shown):
    title  : min(difflib ratio, token-set F1) >= 0.90   (containment >= 4 tokens -> >= 0.95)
    author : surname Jaccard >= 0.50 AND first author agrees, when both sides name authors
    year   : |delta| <= 1                                (preprint vs proceedings)
    VERIFIED    all applicable checks pass
    MISMATCH    a record was found that is close (title >= 0.55) but fails a check
    NOT_FOUND   nothing resembling the record exists (best title < 0.55)
    ERROR       network/parse failure -- never counted as verified

Outputs (see tools/CONTRACTS.md §1):
    02_literature/verified_citations.csv     VERIFIED rows only, with URL + retrieval date
    02_literature/verification_report.json   every record, every status, full evidence
    02_literature/verification_report.md     human-readable table

Exit codes: 0 all VERIFIED, 1 findings (MISMATCH/NOT_FOUND/ERROR), 2 usage error.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib import citation_schema, matchlib, netcache      # noqa: E402
from lib.bibtex_min import bibtex_to_records            # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = REPO_ROOT / "02_literature" / "citations.csv"
OUT_VERIFIED = REPO_ROOT / "02_literature" / "verified_citations.csv"
OUT_REPORT_JSON = REPO_ROOT / "02_literature" / "verification_report.json"
OUT_REPORT_MD = REPO_ROOT / "02_literature" / "verification_report.md"

CROSSREF = "https://api.crossref.org/works/{doi}"
CROSSREF_BIB = (
    "https://api.crossref.org/works?query.bibliographic={q}&rows=8"
    "&select=DOI,title,author,issued,container-title&mailto=" + netcache.CONTACT
)
DATACITE = "https://api.datacite.org/dois/{doi}"
ARXIV_QUERY = "http://export.arxiv.org/api/query?id_list={id}&max_results=1"
OPENALEX_SEARCH = (
    "https://api.openalex.org/works?search={q}&per-page=10&mailto=" + netcache.CONTACT
)
S2_SEARCH = (
    "https://api.semanticscholar.org/graph/v1/paper/search"
    "?query={q}&limit=10&fields=title,authors,year,externalIds,venue,url"
)

# ------------------------------------------------------------------ thresholds
TH = {
    "min_title": 0.90,
    "min_author": 0.60,
    "year_tolerance": 1,
    "not_found_below": 0.55,
}


class Record:
    __slots__ = ("key", "title", "authors", "year", "doi", "arxiv_id", "venue")

    def __init__(self, **kw):
        for s in self.__slots__:
            setattr(self, s, kw.get(s))

    def __repr__(self):
        return f"<Record {self.key!r} doi={self.doi!r} arxiv={self.arxiv_id!r}>"


def _norm_row(r: dict) -> dict:
    """Map a citation CSV row onto the internal record fields.

    Delegates to `lib.citation_schema.normalize_row` so that this tool, `claims_audit.py` and
    `05_paper/template/tools/citations_to_bib.py` cannot drift apart again: S2's register
    (`id,...,doi_or_arxiv,...`) and S3's older 12-column form both normalise identically.
    """
    n = citation_schema.normalize_row({k: v for k, v in r.items() if k})
    return {
        "key": n["key"] or "",
        "title": n["title"] or "",
        "authors": n["authors"] or "",
        "year": n["year"] or "",
        "doi": n["doi"] or "",
        "arxiv_id": n["arxiv_id"] or "",
        "venue": n["venue"] or "",
    }


def load_records(path: Path) -> List[Record]:
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() == ".bib" or text.lstrip().startswith("@"):
        rows = bibtex_to_records(text)
    else:
        rows = list(csv.DictReader(io.StringIO(text)))
    records: List[Record] = []
    seen = set()
    for i, r in enumerate(rows):
        row = _norm_row(r)
        key = row["key"] or f"row{i+1}"
        if key in seen:
            print(f"warning: duplicate key {key!r} — keeping the first", file=sys.stderr)
            continue
        seen.add(key)
        year_raw = str(row.get("year") or "").strip()
        year = int(year_raw) if re.fullmatch(r"\d{4}", year_raw) else None
        records.append(
            Record(
                key=key,
                title=row["title"],
                authors=matchlib.split_authors(row["authors"]),
                year=year,
                doi=netcache.normalize_doi(row["doi"]),
                arxiv_id=netcache.normalize_arxiv_id(row["arxiv_id"]),
                venue=row["venue"],
            )
        )
    return records


# ------------------------------------------------------------------ API parsers
# Each returns a normalized candidate dict or None:
#   {title, authors:[str], year:int|None, doi, arxiv_id, venue, source, source_url}
# Parsers accept raw response text and never raise on bad input (return None instead),
# because a broken API response must not be counted as a verification.

def parse_crossref(body: str, url: str) -> Optional[dict]:
    if not body.strip():
        return None
    try:
        msg = json.loads(body)["message"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return None
    if not isinstance(msg, dict):
        return None
    # Real Crossref always sends `title` as a list and `author` as a list of objects. Anything
    # else means the response is malformed, truncated or proxied — and a verifier that trusts
    # a malformed response can "verify" a citation against garbage. Fail closed: return None,
    # so the record is reported NOT_FOUND rather than VERIFIED (RULES.md #1).
    titles = msg.get("title") or []
    if not isinstance(titles, list):
        return None
    title = (titles[0] if titles else "") or ""
    if not isinstance(title, str):
        return None
    authors = []
    raw_authors = msg.get("author")
    if raw_authors is None:
        raw_authors = []
    if not isinstance(raw_authors, list):
        return None
    for a in raw_authors:
        if not isinstance(a, dict):
            return None
        name = " ".join(x for x in [a.get("given"), a.get("family")] if x)
        if name:
            authors.append(name)
    year = None
    for field in ("issued", "published-print", "published-online", "created"):
        dp = (msg.get(field) or {}).get("date-parts") or []
        if dp and dp[0] and dp[0][0]:
            year = int(dp[0][0])
            break
    return {
        "title": title,
        "authors": authors,
        "year": year,
        "doi": (msg.get("DOI") or "").lower() or None,
        "arxiv_id": None,
        "venue": (msg.get("container-title") or [""])[0],
        "source": "crossref",
        "source_url": url,
    }


def parse_arxiv(body: str, url: str) -> Optional[dict]:
    if not body.strip():
        return None
    try:
        root = ET.fromstring(body)
    except ET.ParseError:
        return None
    # Drop namespaces after parsing (safer than regex-editing the XML, which mangles
    # attributes like xsi:schemaLocation and any ':' in text).
    for el in root.iter():
        if isinstance(el.tag, str) and "}" in el.tag:
            el.tag = el.tag.split("}", 1)[1]
    entry = root.find("entry")
    if entry is None:
        return None
    title = (entry.findtext("title") or "").strip()
    if not title:
        return None
    title = re.sub(r"\s+", " ", title)
    authors = []
    for a in entry.findall("author"):
        name = (a.findtext("name") or "").strip()
        if name:
            authors.append(name)
    year = None
    published = entry.findtext("published") or ""
    if re.match(r"\d{4}", published):
        year = int(published[:4])
    eid = (entry.findtext("id") or "").strip()
    m = re.search(r"abs/([^v\s]+)", eid)
    arxiv_id = m.group(1) if m else None
    doi = None
    for child in entry:
        if child.tag == "doi" and child.text:
            doi = child.text.strip()
    return {
        "title": title,
        "authors": authors,
        "year": year,
        "doi": doi.lower() if doi else None,
        "arxiv_id": arxiv_id,
        "venue": "arXiv",
        "source": "arxiv",
        "source_url": url,
    }


def parse_openalex(body: str, url: str) -> List[dict]:
    try:
        data = json.loads(body)
    except (json.JSONDecodeError, TypeError):
        return []
    if not isinstance(data, dict):
        return []
    results = data.get("results") or []
    if not isinstance(results, list):
        return []
    out = []
    for w in results:
        if not isinstance(w, dict):
            continue
        title = (w.get("title") or w.get("display_name") or "").strip()
        if not title:
            continue
        authors = []
        authorships = w.get("authorships") or []
        if not isinstance(authorships, list):
            authorships = []
        for au in authorships:
            if not isinstance(au, dict):
                continue
            name = ((au.get("author") or {}).get("display_name") or "").strip()
            if name:
                authors.append(name)
        doi = (w.get("doi") or "")
        doi = doi.replace("https://doi.org/", "").lower() or None
        out.append(
            {
                "title": title,
                "authors": authors,
                "year": w.get("publication_year"),
                "doi": doi,
                "arxiv_id": None,
                "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "",
                "source": "openalex",
                "source_url": url,
                "openalex_id": w.get("id"),
            }
        )
    return out


def parse_crossref_multi(body: str, url: str) -> List[dict]:
    """Crossref bibliographic search returns the same item shape as /works/{doi}."""
    try:
        items = json.loads(body)["message"]["items"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return []
    out = []
    for item in items:
        # Reuse the single-work parser by wrapping the item back into a message envelope.
        cand = parse_crossref(json.dumps({"message": item}), url)
        if cand and cand.get("title"):
            out.append(cand)
    return out


def parse_datacite(body: str, url: str) -> Optional[dict]:
    if not body.strip():
        return None
    try:
        attrs = json.loads(body)["data"]["attributes"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return None
    titles = attrs.get("titles") or []
    title = ""
    for t in titles:
        if (t.get("titleType") or "Title").lower() == "title":
            title = (t.get("title") or "").strip()
            break
    if not title:
        return None
    authors = []
    for c in attrs.get("creators") or []:
        name = c.get("name") or " ".join(
            x for x in [c.get("givenName"), c.get("familyName")] if x
        )
        if name:
            authors.append(name.strip())
    year = attrs.get("publicationYear")
    return {
        "title": title,
        "authors": authors,
        "year": int(year) if year else None,
        "doi": (attrs.get("doi") or "").lower() or None,
        "arxiv_id": None,
        "venue": (attrs.get("publisher") or ""),
        "source": "datacite",
        "source_url": url,
    }


def parse_s2(body: str, url: str) -> List[dict]:
    try:
        data = json.loads(body)
    except (json.JSONDecodeError, TypeError):
        return []
    if not isinstance(data, dict):
        return []
    items = data.get("data") or []
    if not isinstance(items, list):
        return []
    out = []
    for w in items:
        if not isinstance(w, dict):
            continue
        title = (w.get("title") or "").strip()
        if not title:
            continue
        authors = [
            (a.get("name") or "").strip()
            for a in (w.get("authors") or [])
            if isinstance(a, dict) and a.get("name")
        ]
        ext = w.get("externalIds") or {}
        if not isinstance(ext, dict):
            ext = {}
        out.append(
            {
                "title": title,
                "authors": authors,
                "year": w.get("year"),
                "doi": (ext.get("DOI") or "").lower() or None,
                "arxiv_id": ext.get("ArXiv"),
                "venue": w.get("venue") or "",
                "source": "semanticscholar",
                "source_url": url,
            }
        )
    return out


# ------------------------------------------------------------------ resolver


class Resolver:
    """Resolves records through the API chain, using an injected `fetch(url) -> str`.

    Network failures are *collected*, not raised: a single dead endpoint must not abort a
    batch, but neither may it be silently reported as "the paper does not exist". The caller
    reads `errors` after each record and turns a NOT_FOUND-with-errors into ERROR.
    """

    def __init__(self, fetch: Callable[[str], str]):
        self.fetch = fetch
        self.errors: List[str] = []

    def _get(self, url: str) -> str:
        try:
            return self.fetch(url)
        except netcache.FetchError as err:
            self.errors.append(str(err))
            return ""

    def by_doi(self, doi: str) -> Tuple[Optional[dict], List[str]]:
        notes = []
        # Normalise here as well as in the loader: the resolver must not depend on its caller
        # having cleaned the identifier (arXiv DOIs are case-insensitive and often written
        # as 10.48550/arXiv.1706.03762).
        doi = netcache.normalize_doi(doi) or doi.strip().lower()
        if doi.startswith("10.48550/arxiv."):
            aid = doi.split("arxiv.", 1)[1]
            cand, n = self.by_arxiv(aid)
            notes += n
            if cand:
                cand["source"] = "arxiv"
                return cand, notes
            notes.append(f"arXiv DOI {doi} did not resolve at arXiv")
            return None, notes
        url = CROSSREF.format(doi=doi)
        body = self._get(url)
        cand = parse_crossref(body, url)
        if cand is None:
            notes.append(f"Crossref has no record for {doi}")
            # DataCite holds DOIs Crossref does not (arXiv's 10.48550/*, datasets, some
            # institutional repositories). Worth one attempt before declaring absence.
            durl = DATACITE.format(doi=doi)
            dcand = parse_datacite(self._get(durl), durl)
            if dcand is not None:
                return dcand, notes
            notes.append(f"DataCite has no record for {doi}")
        return cand, notes

    def by_arxiv(self, arxiv_id: str) -> Tuple[Optional[dict], List[str]]:
        url = ARXIV_QUERY.format(id=arxiv_id)
        body = self._get(url)
        cand = parse_arxiv(body, url)
        if cand is None:
            return None, [f"arXiv returned no entry for {arxiv_id}"]
        return cand, []

    def by_title(self, title: str) -> Tuple[List[dict], List[str]]:
        """Title search across every free index, in order of reliability from here.

        Crossref first: it is the registration agency for the DOIs a paper actually cites,
        it needs no API key, and it does not run a per-IP credit budget. OpenAlex and
        Semantic Scholar are better at *ranking* but both were returning 429 with a four-hour
        Retry-After from this network, so they are treated as optional extras: if a host is
        marked exhausted, the resolver skips it instead of burning the run on backoff sleeps.
        """
        notes = []
        q = re.sub(r"[^\w\s\-:]", " ", title).strip()
        q = re.sub(r"\s+", " ", q)

        url = CROSSREF_BIB.format(q=urllib_quote(q))
        cands = parse_crossref_multi(self._get(url), url)
        if not cands:
            notes.append("Crossref bibliographic search returned no candidates")

        if not cands:
            url = OPENALEX_SEARCH.format(q=urllib_quote(q))
            cands = parse_openalex(self._get(url), url)
            if not cands:
                notes.append("OpenAlex returned no candidates")

        if not cands:
            url = S2_SEARCH.format(q=urllib_quote(q))
            cands = parse_s2(self._get(url), url)
            if not cands:
                notes.append("Semantic Scholar returned no candidates")
        return cands, notes


def urllib_quote(s: str) -> str:
    from urllib.parse import quote_plus

    return quote_plus(s)


# ------------------------------------------------------------------ scoring


def evaluate(rec: Record, cand: dict) -> Tuple[str, float, dict, List[str]]:
    """Compare one record against one candidate. Returns (status, confidence, evidence, reasons).

    `status` here is 'VERIFIED' or 'MISMATCH' — NOT_FOUND is decided by the caller, which
    knows whether any candidate was close enough to call it a mismatch rather than absence.
    """
    t_score = matchlib.title_similarity(rec.title, cand.get("title") or "")
    a_score = matchlib.author_similarity(rec.authors, cand.get("authors") or [])
    first_ok = matchlib.first_author_agrees(rec.authors, cand.get("authors") or [])
    year_delta = None
    if rec.year and cand.get("year"):
        year_delta = abs(int(rec.year) - int(cand["year"]))

    reasons: List[str] = []
    checks: List[float] = []

    if rec.title:
        if t_score < TH["min_title"]:
            reasons.append(f"title too dissimilar: {t_score:.2f} < {TH['min_title']:.2f}")
        checks.append(t_score)
    if a_score is not None:
        if a_score < TH["min_author"]:
            reasons.append(f"author surname overlap too low: {a_score:.2f} < {TH['min_author']:.2f}")
        if first_ok is False:
            reasons.append("first author differs")
        checks.append(a_score)
    if year_delta is not None:
        if year_delta > TH["year_tolerance"]:
            reasons.append(f"year off by {year_delta} (> {TH['year_tolerance']})")
        checks.append(max(0.0, 1.0 - year_delta / 3.0))

    confidence = round(sum(checks) / len(checks), 4) if checks else 0.0
    status = "VERIFIED" if not reasons else "MISMATCH"
    evidence = {
        "title_ratio": t_score,
        "authors_ratio": a_score,
        "authors_recall": matchlib.author_recall(rec.authors, cand.get("authors") or []),
        "authors_jaccard": matchlib.author_jaccard(rec.authors, cand.get("authors") or []),
        "first_author_agrees": first_ok,
        "year_delta": year_delta,
        "resolved_title": cand.get("title"),
        "resolved_authors": cand.get("authors") or [],
        "resolved_year": cand.get("year"),
        "resolved_venue": cand.get("venue") or "",
        "source": cand.get("source"),
        "source_url": cand.get("source_url"),
        "matched_doi": cand.get("doi"),
        "matched_arxiv_id": cand.get("arxiv_id"),
    }
    return status, confidence, evidence, reasons


def verify_record(rec: Record, resolver: Resolver) -> dict:
    """Public entry point: run one record and never let a network failure look like absence."""
    resolver.errors.clear()
    res = _verify_record(rec, resolver)
    if res["status"] == "NOT_FOUND" and resolver.errors:
        res["status"] = "ERROR"
        res["reasons"] = res["reasons"] + [
            f"network/API failure during lookup ({len(resolver.errors)}): treat as UNVERIFIED"
        ] + resolver.errors[:3]
    return res


def _verify_record(rec: Record, resolver: Resolver) -> dict:
    notes: List[str] = []
    authoritative: Optional[dict] = None
    resolved_by = None

    if rec.doi:
        try:
            authoritative, n = resolver.by_doi(rec.doi)
            notes += n
        except netcache.FetchError as err:
            notes.append(f"DOI lookup failed: {err}")
            authoritative = None
        if authoritative:
            resolved_by = "doi"

    if authoritative is None and rec.arxiv_id:
        try:
            authoritative, n = resolver.by_arxiv(rec.arxiv_id)
            notes += n
        except netcache.FetchError as err:
            notes.append(f"arXiv lookup failed: {err}")
            authoritative = None
        if authoritative:
            resolved_by = "arxiv"

    if authoritative is not None:
        status, conf, ev, reasons = evaluate(rec, authoritative)
        return {
            "key": rec.key,
            "status": status,
            "confidence": conf,
            "resolved_by": resolved_by,
            "evidence": ev,
            "reasons": reasons + notes,
            "checked_at": now_iso(),
            "input": rec_input(rec),
        }

    # --- no identifier (or the identifier failed): title search
    if not rec.title:
        return {
            "key": rec.key,
            "status": "ERROR",
            "confidence": 0.0,
            "resolved_by": None,
            "evidence": {},
            "reasons": ["no doi, no arxiv id and no title — nothing to resolve"] + notes,
            "checked_at": now_iso(),
            "input": rec_input(rec),
        }

    try:
        cands, n = resolver.by_title(rec.title)
        notes += n
    except netcache.FetchError as err:
        return {
            "key": rec.key,
            "status": "ERROR",
            "confidence": 0.0,
            "resolved_by": None,
            "evidence": {},
            "reasons": [f"title search failed: {err}"] + notes,
            "checked_at": now_iso(),
            "input": rec_input(rec),
        }

    if not cands:
        return {
            "key": rec.key,
            "status": "NOT_FOUND",
            "confidence": 0.0,
            "resolved_by": None,
            "evidence": {},
            "reasons": ["no candidate returned by any index"] + notes,
            "checked_at": now_iso(),
            "input": rec_input(rec),
        }

    scored = []
    for c in cands:
        t = matchlib.title_similarity(rec.title, c.get("title") or "")
        scored.append((t, c))
    scored.sort(key=lambda x: x[0], reverse=True)
    best_t, best = scored[0]

    if best_t < TH["not_found_below"]:
        return {
            "key": rec.key,
            "status": "NOT_FOUND",
            "confidence": round(best_t, 4),
            "resolved_by": None,
            "evidence": {
                "closest_title": best.get("title"),
                "closest_title_ratio": round(best_t, 4),
                "closest_source": best.get("source"),
                "closest_source_url": best.get("source_url"),
            },
            "reasons": [
                f"nothing resembling this title exists: best match {best_t:.2f} < "
                f"{TH['not_found_below']:.2f}"
            ]
            + notes,
            "checked_at": now_iso(),
            "input": rec_input(rec),
        }

    status, conf, ev, reasons = evaluate(rec, best)
    return {
        "key": rec.key,
        "status": status,
        "confidence": conf,
        "resolved_by": "title",
        "evidence": ev,
        "reasons": reasons + notes,
        "checked_at": now_iso(),
        "input": rec_input(rec),
    }


def rec_input(rec: Record) -> dict:
    return {
        "title": rec.title,
        "authors": rec.authors,
        "year": rec.year,
        "doi": rec.doi,
        "arxiv_id": rec.arxiv_id,
        "venue": rec.venue,
    }


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


# ------------------------------------------------------------------ outputs

VERIFIED_FIELDS = list(citation_schema.CANONICAL_FIELDS)


def write_verified_csv(results: List[dict], path: Path) -> int:
    """Write the VERIFIED rows in the ONE canonical schema (tools/CONTRACTS.md §1).

    There is exactly one `verified_citations.csv` in this repo and S2's tool owns it. Writing
    a second, differently-shaped file to the same path is what broke `citations_to_bib.py` and
    `claims_audit.py` on 2026-11-03, so this writer emits the canonical nine columns and
    nothing else. The full evidence (ratios, source url, reasons) stays in the JSON report.
    """
    rows = []
    for r in results:
        if r["status"] != "VERIFIED":
            continue
        ev = r["evidence"]
        inp = r["input"]
        internal = {
            "key": r["key"],
            "title": ev.get("resolved_title") or inp["title"],
            "authors": "; ".join(ev.get("resolved_authors") or inp["authors"]),
            "year": ev.get("resolved_year") or inp["year"] or "",
            "venue": ev.get("resolved_venue") or inp.get("venue") or "",
            "doi": ev.get("matched_doi") or "",
            "arxiv_id": ev.get("matched_arxiv_id") or inp.get("arxiv_id") or "",
            "url": ev.get("source_url") or "",
            "retrieved_at": r["checked_at"],
        }
        command = (
            f"tools/verify_citations.py --online # source={ev.get('source') or '?'} "
            f"resolved_by={r.get('resolved_by') or '?'} url={ev.get('source_url') or ''}"
        )
        rows.append(citation_schema.to_canonical_row(internal, command))

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=VERIFIED_FIELDS)
        w.writeheader()
        for row in rows:
            w.writerow(row)
    return len(rows)


def write_report_md(results: List[dict], path: Path, n_total: int) -> None:
    counts = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    lines = [
        "# Citation verification report",
        "",
        f"Generated: {now_iso()}",
        "",
        f"Total {n_total} — " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())),
        "",
        "| # | key | status | conf | source | reason |",
        "|---|-----|--------|------|--------|--------|",
    ]
    for i, r in enumerate(results, 1):
        reason = "; ".join(r["reasons"])[:120].replace("|", "/")
        lines.append(
            f"| {i} | `{r['key']}` | **{r['status']}** | {r['confidence']:.2f} | "
            f"{r['evidence'].get('source') or '-'} | {reason} |"
        )
    lines += [
        "",
        "A record that is not VERIFIED must not appear in the draft (RULES.md #1).",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


# ------------------------------------------------------------------ main


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Resolve citations against Crossref / arXiv / OpenAlex.")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--csv", type=Path, default=None, help="citation CSV (default: 02_literature/citations.csv)")
    src.add_argument("--bib", type=Path, default=None, help="BibTeX file to check")
    ap.add_argument("--online", action="store_true", help="allow network calls (default: cache only)")
    ap.add_argument("--offline", action="store_true", help="cache only, never touch the network")
    ap.add_argument("--min-title", type=float, default=TH["min_title"])
    ap.add_argument("--min-author", type=float, default=TH["min_author"])
    ap.add_argument("--year-tolerance", type=int, default=TH["year_tolerance"])
    ap.add_argument("--not-found-below", type=float, default=TH["not_found_below"])
    ap.add_argument("--limit", type=int, default=0, help="only check the first N records (0 = all)")
    ap.add_argument(
        "--backoff",
        default="30,60,120",
        help="seconds to wait between 429/5xx retries, comma separated (RULES.md #11)",
    )
    ap.add_argument("--out-dir", type=Path, default=None, help="where to write outputs")
    ap.add_argument("--no-write", action="store_true", help="do not write output files")
    ap.add_argument("--json", action="store_true", help="print the full report JSON to stdout")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    TH["min_title"] = args.min_title
    TH["min_author"] = args.min_author
    TH["year_tolerance"] = args.year_tolerance
    TH["not_found_below"] = args.not_found_below

    src_path = args.bib or args.csv or DEFAULT_CSV
    if not src_path.exists():
        print(f"error: no such file: {src_path}", file=sys.stderr)
        return 2
    records = load_records(src_path)
    if not records:
        print(f"error: no records parsed from {src_path}", file=sys.stderr)
        return 2
    if args.limit:
        records = records[: args.limit]

    online = args.online and not args.offline
    backoff = tuple(float(x) for x in args.backoff.split(",") if x.strip())
    fetch, pf = netcache.make_fetcher(online=online, backoff=backoff)
    resolver = Resolver(fetch)

    results = []
    for i, rec in enumerate(records, 1):
        if not args.quiet:
            print(f"[{i}/{len(records)}] {rec.key} ... ", end="", flush=True, file=sys.stderr)
        res = verify_record(rec, resolver)
        results.append(res)
        if not args.quiet:
            print(res["status"], file=sys.stderr)

    out_dir = args.out_dir
    verified_path = (out_dir / "verified_citations.csv") if out_dir else OUT_VERIFIED
    report_json = (out_dir / "verification_report.json") if out_dir else OUT_REPORT_JSON
    report_md = (out_dir / "verification_report.md") if out_dir else OUT_REPORT_MD

    n_verified = sum(1 for r in results if r["status"] == "VERIFIED")
    report = {
        "generated_at": now_iso(),
        "source_file": str(src_path),
        "online": online,
        "thresholds": dict(TH),
        "n_total": len(results),
        "n_verified": n_verified,
        "n_mismatch": sum(1 for r in results if r["status"] == "MISMATCH"),
        "n_not_found": sum(1 for r in results if r["status"] == "NOT_FOUND"),
        "n_error": sum(1 for r in results if r["status"] == "ERROR"),
        "n_http_requests": pf.n_requests,
        "n_cache_hits": pf.n_cache_hits,
        "sources_unavailable": pf.blocked_hosts,
        "results": results,
    }

    if not args.no_write:
        n_rows = write_verified_csv(results, verified_path)
        report_json.parent.mkdir(parents=True, exist_ok=True)
        report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        write_report_md(results, report_md, len(results))
        if not args.quiet:
            print(f"\nwrote {n_rows} verified rows -> {verified_path}", file=sys.stderr)
            print(f"wrote report -> {report_json}", file=sys.stderr)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))

    ok = n_verified == len(results)
    if not args.quiet:
        if pf.blocked_hosts:
            for host, why in pf.blocked_hosts.items():
                print(f"note: {host} skipped — {why}", file=sys.stderr)
        verdict = "ALL VERIFIED" if ok else f"{len(results) - n_verified} NOT VERIFIED"
        print(f"\n{verdict} ({n_verified}/{len(results)})", file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
