#!/usr/bin/env python
"""Adversarial, fully offline tests for tools/verify_citations.py.

Companion to test_verify_citations.py (which covers the happy paths and the
"fake citation is not verified" property). This file attacks the *edges* that real
bibliographic APIs and real messy registers produce:

  1. hostile API bodies   — HTML error pages, truncated JSON, wrong JSON types,
                            huge whitespace blobs, BOMs, NULs, multi-entry Atom feeds;
  2. record edge cases    — unicode, punctuation-only and empty titles, identifier
                            spellings, duplicate keys, `and`-separated / trailing-`;`
                            author lists, 40 authors, particle surnames;
  3. comparison traps     — near-miss papers that must never verify;
  4. status plumbing      — FetchError vs empty-body, ERROR never counted as verified;
  5. write-path safety    — --no-write, provenance columns, no MISMATCH leakage.

No network: every response is injected through the tool's `fetch(url) -> str` seam, and
`main()` is driven by monkeypatching `netcache.make_fetcher`. Nothing here writes outside
`tmp_path`.

Run:  python -m pytest tools/tests/test_verify_citations_adversarial.py -q
"""

from __future__ import annotations

import csv
import io
import json
import sys
import time
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

import verify_citations as vc                     # noqa: E402
from lib import citation_schema
CANONICAL_FIELDS = citation_schema.CANONICAL_FIELDS
from lib import matchlib, netcache                # noqa: E402

# --------------------------------------------------------------------------- helpers


class StubFetcher:
    """URL-substring routed stub. A route value may be a string or an exception."""

    def __init__(self, routes=(), default=""):
        self.routes = list(routes)
        self.default = default
        self.calls = []

    def __call__(self, url: str) -> str:
        self.calls.append(url)
        for pattern, body in self.routes:
            if pattern in url:
                if isinstance(body, Exception):
                    raise body
                return body
        if isinstance(self.default, Exception):
            raise self.default
        return self.default

    def urls(self):
        return list(self.calls)


class _Perf:
    """Stand-in for PoliteFetcher: main() only reads these three attributes."""

    def __init__(self):
        self.n_requests = 0
        self.n_cache_hits = 0
        self.blocked_hosts = {}


def rec(**kw):
    base = dict(key="k", title="", authors=[], year=None, doi=None, arxiv_id=None, venue="")
    base.update(kw)
    return vc.Record(**base)


def _item(title, authors=(("Ashish", "Vaswani"),), year=2017, doi="10.1000/adv.1", venue="Journal"):
    return {
        "DOI": doi,
        "title": [title],
        "author": [{"given": g, "family": f} for g, f in authors],
        "issued": {"date-parts": [[year]]},
        "container-title": [venue],
    }


def cr_one(title, **kw):
    """A single-work Crossref body (/works/{doi})."""
    return json.dumps({"status": "ok", "message": _item(title, **kw)})


def cr_multi(*items):
    """A Crossref bibliographic-search body (/works?query...)."""
    return json.dumps({"status": "ok", "message": {"items": list(items)}})


def arxiv_feed(*entries):
    """entries: dicts with id/title/published/authors/doi."""
    parts = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<feed xmlns="http://www.w3.org/2005/Atom" '
             'xmlns:arxiv="http://arxiv.org/schemas/atom">']
    for e in entries:
        parts.append("  <entry>")
        parts.append(f"    <id>{e['id']}</id>")
        parts.append(f"    <published>{e.get('published', '2017-06-12T17:57:34Z')}</published>")
        parts.append(f"    <title>{e['title']}</title>")
        for a in e.get("authors", ["Ashish Vaswani"]):
            parts.append(f"    <author><name>{a}</name></author>")
        if e.get("doi"):
            parts.append(f"    <arxiv:doi>{e['doi']}</arxiv:doi>")
        parts.append("  </entry>")
    parts.append("</feed>")
    return "\n".join(parts)


def write_csv(path: Path, rows, header="key,title,authors,year,doi,arxiv_id,venue"):
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [header]
    for r in rows:
        lines.append(",".join('"' + str(v).replace('"', '""') + '"' for v in r))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


TITLE = "Attention Is All You Need"
SURVEY = (
    "Attention Is All You Need: A Comprehensive Survey of Transformer Architectures "
    "in Vision, Speech, Language, and Beyond"
)
RESNET = "Deep Residual Learning for Image Recognition"


# =========================================================================== 1. hostile bodies


def test_html_error_page_never_verifies_and_does_not_raise():
    """A 200-with-HTML 429 page is not metadata: no VERIFIED, no traceback."""
    f = StubFetcher([("api.crossref.org/works/", "<html><body>429 Too Many Requests</body></html>")])
    res = vc.verify_record(rec(key="html", title=TITLE, authors=["Ashish Vaswani"],
                               year=2017, doi="10.1000/adv.1"), vc.Resolver(f))
    assert res["status"] in {"NOT_FOUND", "ERROR"}, res
    assert res["status"] != "VERIFIED"
    assert res["evidence"].get("resolved_title") is None


def test_truncated_json_body_never_verifies():
    f = StubFetcher([("api.crossref.org/works/", '{"message": {"title": [')])
    res = vc.verify_record(rec(key="trunc", title=TITLE, year=2017, doi="10.1000/adv.2"),
                           vc.Resolver(f))
    assert res["status"] != "VERIFIED"
    assert res["status"] in {"NOT_FOUND", "ERROR", "MISMATCH"}


def test_crossref_message_without_title_never_verifies():
    """`{"message": {}}` carries no metadata; a candidate with an empty title must not pass."""
    f = StubFetcher([("api.crossref.org/works/", '{"message": {}}')])
    res = vc.verify_record(rec(key="emptymsg", title=TITLE, authors=["Ashish Vaswani"],
                               year=2017, doi="10.1000/adv.3"), vc.Resolver(f))
    assert res["status"] != "VERIFIED"
    # A DOI that resolves to *something* is a mismatch, not absence — both are acceptable,
    # VERIFIED is not.
    assert res["status"] in {"MISMATCH", "NOT_FOUND", "ERROR"}


def test_crossref_string_title_is_not_verified():
    """Real Crossref always sends title as a list; a string must not become a match."""
    body = json.dumps({"message": {"title": TITLE, "author": [{"given": "Ashish", "family": "Vaswani"}],
                                   "issued": {"date-parts": [[2017]]}}})
    f = StubFetcher([("api.crossref.org/works/", body)])
    res = vc.verify_record(rec(key="strtitle", title=TITLE, authors=["Ashish Vaswani"],
                               year=2017, doi="10.1000/adv.4"), vc.Resolver(f))
    assert res["status"] != "VERIFIED"


def test_crossref_string_title_parser_returns_none_not_a_single_character():
    """Documented contract: "Parsers ... never raise on bad input (return None instead)"."""
    body = json.dumps({"message": {"title": TITLE, "author": []}})
    parsed = vc.parse_crossref(body, "u")
    assert parsed is None or parsed["title"] == TITLE, f"title parsed as {parsed!r}"


def test_crossref_author_as_dict_does_not_crash():
    """`author` is a dict instead of a list: parser must degrade, not explode."""
    body = json.dumps({"message": {"title": [TITLE], "author": {"given": "Ashish", "family": "Vaswani"}}})
    f = StubFetcher([("api.crossref.org/works/", body)])
    res = vc.verify_record(rec(key="authdict", title=TITLE, year=2017, doi="10.1000/adv.5"),
                           vc.Resolver(f))
    assert res["status"] != "VERIFIED"


def test_arxiv_feed_without_entry_is_not_found():
    f = StubFetcher([("export.arxiv.org", '<?xml version="1.0"?>'
                                        '<feed xmlns="http://www.w3.org/2005/Atom"></feed>')])
    res = vc.verify_record(rec(key="noentry", title=TITLE, arxiv_id="1706.03762"), vc.Resolver(f))
    assert res["status"] in {"NOT_FOUND", "ERROR"}
    assert res["status"] != "VERIFIED"


def test_arxiv_uses_only_the_first_entry():
    """max_results=1 in real life; a multi-entry body must not let entry #2 vouch for a record."""
    body = arxiv_feed(
        {"id": "http://arxiv.org/abs/1706.03762v5", "title": TITLE,
         "authors": ["Ashish Vaswani"], "doi": "10.48550/arXiv.1706.03762"},
        {"id": "http://arxiv.org/abs/1512.03385v1", "title": RESNET,
         "published": "2015-12-10T18:18:14Z", "authors": ["Kaiming He"]},
    )
    first = vc.verify_record(rec(key="e1", title=TITLE, arxiv_id="1706.03762"), vc.Resolver(StubFetcher([("export.arxiv.org", body)])))
    second = vc.verify_record(rec(key="e2", title=RESNET, authors=["Kaiming He"], year=2016,
                                  arxiv_id="1706.03762"), vc.Resolver(StubFetcher([("export.arxiv.org", body)])))
    assert first["status"] == "VERIFIED", first["reasons"]
    assert first["evidence"]["resolved_title"] == TITLE
    assert second["status"] == "MISMATCH", second  # the feed said Transformer, not ResNet


def test_arxiv_entities_and_cdata_are_decoded():
    body = arxiv_feed({"id": "http://arxiv.org/abs/2001.00001v1",
                       "title": "Robust &amp; Efficient <![CDATA[Learning]]> of Things",
                       "published": "2020-01-01T00:00:00Z", "authors": ["A B"]})
    res = vc.verify_record(rec(key="ent", title="Robust & Efficient Learning of Things",
                               authors=["A B"], year=2020, arxiv_id="2001.00001"),
                           vc.Resolver(StubFetcher([("export.arxiv.org", body)])))
    assert res["status"] == "VERIFIED", res["reasons"]
    assert res["evidence"]["resolved_title"] == "Robust & Efficient Learning of Things"


def test_eight_megabyte_whitespace_body_is_fast_and_unverified():
    """A pathological 200 response must hit the strip/parse guard, not hang or verify."""
    blob = " " * (8 * 1024 * 1024)
    f = StubFetcher([("api.crossref.org/works/", blob)], default=blob)
    t0 = time.monotonic()
    res = vc.verify_record(rec(key="big", title=TITLE, year=2017, doi="10.1000/adv.6"),
                           vc.Resolver(f))
    elapsed = time.monotonic() - t0
    assert elapsed < 5.0, f"took {elapsed:.2f}s on a whitespace blob"
    assert res["status"] != "VERIFIED"
    assert vc.parse_crossref(blob, "u") is None


def test_polite_fetcher_max_bytes_guard(monkeypatch):
    """The tool-level guard behind the 8 MB case: oversized bodies raise FetchError."""

    class _Headers:
        @staticmethod
        def get_content_charset():
            return "utf-8"

    class _Resp:
        def __init__(self, payload):
            self.payload = payload
            self.headers = _Headers()

        def read(self, n=-1):
            return self.payload[:n] if n and n > 0 else self.payload

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    monkeypatch.setattr(netcache.urllib.request, "urlopen",
                        lambda req, timeout=30: _Resp(b" " * 2000))
    pf = netcache.PoliteFetcher(use_cache=False, max_bytes=1024,
                                sleeper=lambda s: None, backoff=(0,))
    with pytest.raises(netcache.FetchError, match="larger than"):
        pf.get("https://example.org/huge")

    # the cap must not reject ordinary bodies
    monkeypatch.setattr(netcache.urllib.request, "urlopen",
                        lambda req, timeout=30: _Resp(b"x" * 500))
    pf2 = netcache.PoliteFetcher(use_cache=False, max_bytes=1024,
                                 sleeper=lambda s: None, backoff=(0,))
    assert pf2.get("https://example.org/small") == "x" * 500


def test_utf8_bom_body_is_rejected_not_verified():
    body = "\ufeff" + cr_one(TITLE)
    f = StubFetcher([("api.crossref.org/works/", body)])
    res = vc.verify_record(rec(key="bom", title=TITLE, authors=["Ashish Vaswani"],
                               year=2017, doi="10.1000/adv.7"), vc.Resolver(f))
    assert res["status"] != "VERIFIED"
    assert vc.parse_crossref(body, "u") is None


def test_escaped_nul_in_title_does_not_crash_and_cannot_mint_a_false_match():
    """A JSON-escaped \\u0000 is legal JSON but not a title character."""
    body = json.dumps({"message": {"title": ["Attention\u0000Is All You Need"],
                                   "author": [{"given": "Ashish", "family": "Vaswani"}],
                                   "issued": {"date-parts": [[2017]]}}})
    parsed = vc.parse_crossref(body, "u")
    assert parsed is not None and "\x00" in parsed["title"]
    res = vc.verify_record(rec(key="nul", title=TITLE, authors=["Ashish Vaswani"], year=2017,
                               doi="10.1000/adv.8"),
                           vc.Resolver(StubFetcher([("api.crossref.org/works/", body)])))
    assert res["status"] in {"VERIFIED", "MISMATCH"}, res
    assert res["status"] != "ERROR"


def test_raw_nul_byte_makes_the_body_unparsable():
    body = '{"message":{"title":["Attention\x00Is All You Need"]}}'
    assert vc.parse_crossref(body, "u") is None
    res = vc.verify_record(rec(key="rawnul", title=TITLE, year=2017, doi="10.1000/adv.9"),
                           vc.Resolver(StubFetcher([("api.crossref.org/works/", body)])))
    assert res["status"] != "VERIFIED"


# =========================================================================== 2. record edges


def test_accented_title_round_trips_and_verifies(tmp_path):
    title = "R\u00e9sum\u00e9 of Na\u00efve B\u00e4yes"
    p = write_csv(tmp_path / "acc.csv", [("acc", title, "Ana M\u00fcller", "2021", "10.1000/acc.1", "", "")])
    records = vc.load_records(p)
    assert records[0].title == title
    body = cr_one(title, authors=(("Ana", "M\u00fcller"),), year=2021, doi="10.1000/acc.1")
    res = vc.verify_record(records[0], vc.Resolver(StubFetcher([("api.crossref.org/works/", body)])))
    assert res["status"] == "VERIFIED", res["reasons"]


def test_cjk_title_verifies_against_identical_candidate(tmp_path):
    title = "\u6ce8\u610f\u529b\u673a\u5236\u7efc\u8ff0"
    p = write_csv(tmp_path / "cjk.csv", [("cjk", title, "San Zhang", "2022", "10.1000/cjk.1", "", "")])
    records = vc.load_records(p)
    assert records[0].title == title
    assert matchlib.title_similarity(title, title) == 1.0
    body = cr_one(title, authors=(("San", "Zhang"),), year=2022, doi="10.1000/cjk.1")
    res = vc.verify_record(records[0], vc.Resolver(StubFetcher([("api.crossref.org/works/", body)])))
    assert res["status"] == "VERIFIED", res["reasons"]


def test_punctuation_only_title_never_verifies(tmp_path):
    p = write_csv(tmp_path / "punct.csv", [("p", "!!! ??? ---", "", "", "", "", "")])
    records = vc.load_records(p)
    assert matchlib.normalize_title(records[0].title) == ""
    res = vc.verify_record(records[0], vc.Resolver(StubFetcher()))
    assert res["status"] in {"NOT_FOUND", "ERROR", "MISMATCH"}
    assert res["status"] != "VERIFIED"


def test_empty_title_without_identifiers_is_error(tmp_path):
    p = write_csv(tmp_path / "empty.csv", [("empty", "", "", "", "", "", "")])
    records = vc.load_records(p)
    res = vc.verify_record(records[0], vc.Resolver(StubFetcher()))
    assert res["status"] == "ERROR"
    assert any("nothing to resolve" in r for r in res["reasons"])


def test_doi_with_prefix_is_normalised_before_the_crossref_call(tmp_path):
    p = write_csv(tmp_path / "doi.csv", [("d", TITLE, "Ashish Vaswani", "2017", "doi:10.1000/XYZ", "", "")])
    records = vc.load_records(p)
    assert records[0].doi == "10.1000/xyz"
    f = StubFetcher([("api.crossref.org/works/", cr_one(TITLE, doi="10.1000/xyz"))])
    res = vc.verify_record(records[0], vc.Resolver(f))
    assert any(u.endswith("api.crossref.org/works/10.1000/xyz") for u in f.urls()), f.urls()
    assert res["status"] == "VERIFIED", res["reasons"]


def test_modern_arxiv_id_with_version_suffix_is_queried_clean(tmp_path):
    p = write_csv(tmp_path / "ax.csv", [("a", TITLE, "Ashish Vaswani", "2017", "", "arXiv:1706.03762v5", "")])
    records = vc.load_records(p)
    assert records[0].arxiv_id == "1706.03762"
    body = arxiv_feed({"id": "http://arxiv.org/abs/1706.03762v5", "title": TITLE,
                       "authors": ["Ashish Vaswani"]})
    f = StubFetcher([("export.arxiv.org", body)])
    res = vc.verify_record(records[0], vc.Resolver(f))
    assert any("id_list=1706.03762" in u for u in f.urls()), f.urls()
    assert not any("v5" in u for u in f.urls()), f.urls()
    assert res["status"] == "VERIFIED"


def test_old_style_arxiv_id_is_kept_intact(tmp_path):
    p = write_csv(tmp_path / "old.csv", [("a", "Learning to Parse Natural Language", "A B", "2001", "", "cs/0112017", "")])
    records = vc.load_records(p)
    assert records[0].arxiv_id == "cs/0112017"
    body = arxiv_feed({"id": "http://arxiv.org/abs/cs/0112017v1",
                       "title": "Learning to Parse Natural Language",
                       "published": "2001-12-03T00:00:00Z", "authors": ["A B"]})
    f = StubFetcher([("export.arxiv.org", body)])
    res = vc.verify_record(records[0], vc.Resolver(f))
    assert any("id_list=cs/0112017" in u for u in f.urls()), f.urls()
    assert res["status"] == "VERIFIED", res["reasons"]


def test_duplicate_csv_key_warns_on_stderr_and_checks_one_record(tmp_path, capsys, monkeypatch):
    p = write_csv(tmp_path / "dup.csv", [
        ("dup", TITLE, "Ashish Vaswani", "2017", "", "", ""),
        ("dup", RESNET, "Kaiming He", "2016", "", "", ""),
    ])
    records = vc.load_records(p)
    err = capsys.readouterr().err
    assert "duplicate key 'dup'" in err and "keeping the first" in err
    assert len(records) == 1 and records[0].title == TITLE

    fake = StubFetcher([("api.crossref.org/works?query", cr_multi(_item(TITLE)))])
    monkeypatch.setattr(vc.netcache, "make_fetcher", lambda online, **kw: (fake, _Perf()))
    code = vc.main(["--csv", str(p), "--offline", "--json", "--no-write", "--quiet"])
    report = json.loads(capsys.readouterr().out)
    assert report["n_total"] == 1
    assert code == 0


def test_author_string_with_and_separators(tmp_path):
    p = write_csv(tmp_path / "and.csv", [("a", TITLE, "Ashish Vaswani and Noam Shazeer", "2017", "10.1000/adv.1", "", "")])
    records = vc.load_records(p)
    assert records[0].authors == ["Ashish Vaswani", "Noam Shazeer"]
    body = cr_one(TITLE, authors=(("Ashish", "Vaswani"), ("Noam", "Shazeer")), year=2017)
    res = vc.verify_record(records[0], vc.Resolver(StubFetcher([("api.crossref.org/works/", body)])))
    assert res["status"] == "VERIFIED", res["reasons"]


def test_author_string_with_trailing_semicolon(tmp_path):
    p = write_csv(tmp_path / "semi.csv", [("a", TITLE, "Ashish Vaswani; Noam Shazeer;", "2017", "", "", "")])
    records = vc.load_records(p)
    assert records[0].authors == ["Ashish Vaswani", "Noam Shazeer"]
    assert all(a.strip() for a in records[0].authors)


def test_forty_authors_are_all_kept_and_match(tmp_path):
    names = [f"Given{i} Surname{i}" for i in range(40)]
    p = write_csv(tmp_path / "many.csv", [("m", TITLE, "; ".join(names), "2022", "10.1000/many.1", "", "")])
    records = vc.load_records(p)
    assert len(records[0].authors) == 40
    assert len(matchlib.surname_set(records[0].authors)) == 40
    body = cr_one(TITLE, authors=[(f"Given{i}", f"Surname{i}") for i in range(40)], year=2022,
                  doi="10.1000/many.1")
    res = vc.verify_record(records[0], vc.Resolver(StubFetcher([("api.crossref.org/works/", body)])))
    assert res["status"] == "VERIFIED", res["reasons"]


def test_particle_surname_keeps_its_particles(tmp_path):
    assert matchlib.surname("Johannes van der Waals") == "van der waals"
    assert matchlib.first_author_agrees(["Johannes van der Waals"], ["J. van der Waals"]) is True
    p = write_csv(tmp_path / "vdw.csv", [("v", "On the Equation of State", "Johannes van der Waals", "1873", "10.1000/vdw.1", "", "")])
    records = vc.load_records(p)
    body = cr_one("On the Equation of State", authors=(("Johannes", "van der Waals"),), year=1873,
                  doi="10.1000/vdw.1")
    res = vc.verify_record(records[0], vc.Resolver(StubFetcher([("api.crossref.org/works/", body)])))
    assert res["status"] == "VERIFIED", res["reasons"]
    # ... and a different first author with the same surname must not pass
    other = cr_one("On the Equation of State", authors=(("Diederik", "van der Waals"),), year=1873)
    res2 = vc.verify_record(records[0], vc.Resolver(StubFetcher([("api.crossref.org/works/", other)])))
    assert res2["status"] == "MISMATCH"


# =========================================================================== 3. comparison traps


def test_same_title_and_year_but_different_first_author_is_mismatch():
    body = cr_one(TITLE, authors=(("Alice", "Smith"),), year=2017)
    res = vc.verify_record(rec(key="fa", title=TITLE, authors=["John Smith"], year=2017,
                               doi="10.1000/adv.10"),
                           vc.Resolver(StubFetcher([("api.crossref.org/works/", body)])))
    assert res["status"] == "MISMATCH", res
    assert any("first author" in r for r in res["reasons"])


def test_anagram_title_is_not_verified():
    """Same bag of words, different claim: 'All You Need Is Attention' is not the paper."""
    body = cr_multi(_item("All You Need Is Attention", authors=(("Zoe", "Zhang"),), year=2021))
    res = vc.verify_record(rec(key="ana", title=TITLE, year=2017),
                           vc.Resolver(StubFetcher([("api.crossref.org/works?query", body)])))
    assert res["status"] in {"MISMATCH", "NOT_FOUND"}, res
    assert res["status"] != "VERIFIED"


def test_survey_that_prefixes_the_target_title_is_not_verified():
    """A survey title containing the target title as a prefix (+6 words) is a different work."""
    # Same year, different authors, title-only record: only the title check can catch this.
    body = cr_multi(_item(SURVEY, authors=(("Maria", "Gomez"),), year=2017, doi="10.1000/survey.1"))
    res = vc.verify_record(rec(key="surv", title=TITLE, year=2017),
                           vc.Resolver(StubFetcher([("api.crossref.org/works?query", body)])))
    assert res["status"] in {"MISMATCH", "NOT_FOUND"}, res


def test_arxiv_retracted_variant_differing_by_one_word_is_mismatch():
    """Policy: '... for Image Super-Resolution' is a different (withdrawn) paper, not '... for
    Image Recognition'. One word of difference is enough to be a different claim."""
    assert matchlib.title_similarity(RESNET, "Deep Residual Learning for Image Super-Resolution") < 0.90
    body = arxiv_feed({"id": "http://arxiv.org/abs/1512.03385v1",
                       "title": "Deep Residual Learning for Image Super-Resolution",
                       "published": "2015-12-10T18:18:14Z", "authors": ["Kaiming He"]})
    res = vc.verify_record(rec(key="retr", title=RESNET, authors=["Kaiming He"], year=2016,
                               arxiv_id="1512.03385"),
                           vc.Resolver(StubFetcher([("export.arxiv.org", body)])))
    assert res["status"] == "MISMATCH", res
    assert any("title too dissimilar" in r for r in res["reasons"])


def test_correct_title_with_year_off_by_five_is_mismatch():
    body = cr_one(TITLE, year=2017)
    res = vc.verify_record(rec(key="y5", title=TITLE, authors=["Ashish Vaswani"], year=2012,
                               doi="10.1000/adv.11"),
                           vc.Resolver(StubFetcher([("api.crossref.org/works/", body)])))
    assert res["status"] == "MISMATCH", res
    assert any("year off by 5" in r for r in res["reasons"])


def test_doi_resolving_to_a_different_paper_is_mismatch_not_verified():
    """Copy-paste DOI error: the DOI is real, the paper is not the one cited."""
    body = cr_one("Deep Residual Learning for Image Super-Resolution",
                  authors=(("Kaiming", "He"),), year=2016, doi="10.1109/cvpr.2016.90")
    f = StubFetcher([("api.crossref.org/works/", body)])
    res = vc.verify_record(rec(key="wrongdoi", title=RESNET, authors=["Kaiming He"], year=2016,
                               doi="10.1109/CVPR.2016.90"), vc.Resolver(f))
    assert res["status"] == "MISMATCH", res
    assert res["resolved_by"] == "doi"
    assert res["evidence"]["matched_doi"] == "10.1109/cvpr.2016.90"
    assert any("title" in r for r in res["reasons"])


# =========================================================================== 4. status plumbing


def test_crossref_failure_falls_back_to_title_search_and_verifies():
    f = StubFetcher([
        ("api.crossref.org/works/", netcache.FetchError("429 from Crossref")),
        ("api.crossref.org/works?query", cr_multi(_item(TITLE, year=2017))),
    ])
    resolver = vc.Resolver(f)
    res = vc.verify_record(rec(key="fallback", title=TITLE, authors=["Ashish Vaswani"],
                               year=2017, doi="10.1000/adv.12"), resolver)
    assert res["status"] == "VERIFIED", res["reasons"]
    assert res["resolved_by"] == "title"
    assert resolver.errors, "the DOI failure should still be recorded as a note"


def test_only_fetch_failures_are_error():
    """Nothing could be checked at all -> ERROR, not NOT_FOUND."""
    f = StubFetcher(default=netcache.FetchError("connection reset"))
    res = vc.verify_record(rec(key="dead", title=TITLE, authors=["Ashish Vaswani"],
                               year=2017, doi="10.1000/adv.13"), vc.Resolver(f))
    assert res["status"] == "ERROR", res
    assert any("network/API failure" in r for r in res["reasons"])


def test_empty_body_everywhere_never_verifies():
    """'' is the tool's 404 signal: absence, not a crash and never a verification."""
    res = vc.verify_record(rec(key="e404", title=TITLE, authors=["Ashish Vaswani"],
                               year=2017, doi="10.1000/nope.404"),
                           vc.Resolver(StubFetcher(default="")))
    assert res["status"] in {"NOT_FOUND", "ERROR"}, res
    assert res["status"] != "VERIFIED"


def test_main_reports_error_as_unverified_and_exits_1(tmp_path, capsys):
    """Offline run with a guaranteed cache miss: every record is ERROR, none is verified."""
    p = write_csv(tmp_path / "err.csv", [
        ("e1", "Quantum Cheese Transformers for Rural Cows", "A Fake", "2022", "10.9999/nocache.1", "", ""),
        ("e2", TITLE, "Ashish Vaswani", "2017", "10.9999/nocache.2", "", ""),
    ])
    code = vc.main(["--csv", str(p), "--offline", "--no-write", "--json", "--quiet"])
    out = capsys.readouterr().out
    report = json.loads(out)
    assert code == 1
    assert report["n_total"] == 2
    assert report["n_verified"] == 0
    assert report["n_error"] == report["n_total"]
    assert report["n_mismatch"] == report["n_not_found"] == 0


# =========================================================================== 5. write path


def test_no_write_leaves_no_files(tmp_path, monkeypatch):
    p = write_csv(tmp_path / "src.csv", [("ok", TITLE, "Ashish Vaswani", "2017", "", "", "")])
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    fake = StubFetcher([("api.crossref.org/works?query", cr_multi(_item(TITLE)))])
    monkeypatch.setattr(vc.netcache, "make_fetcher", lambda online, **kw: (fake, _Perf()))
    code = vc.main(["--csv", str(p), "--offline", "--no-write", "--quiet", "--out-dir", str(out_dir)])
    assert code == 0
    assert list(out_dir.iterdir()) == []


def test_verified_csv_keeps_only_verified_rows_and_carries_provenance(tmp_path):
    results = [
        {"key": "good", "status": "VERIFIED", "confidence": 0.99, "resolved_by": "doi",
         "evidence": {"resolved_title": TITLE, "resolved_authors": ["Ashish Vaswani"],
                      "resolved_year": 2017, "matched_doi": "10.1000/adv.1",
                      "matched_arxiv_id": None, "source": "crossref",
                      "source_url": "https://api.crossref.org/works/10.1000/adv.1",
                      "title_ratio": 1.0, "authors_ratio": 1.0, "year_delta": 0},
         "reasons": [], "checked_at": "2026-11-03T00:00:00Z",
         "input": {"title": TITLE, "authors": ["Ashish Vaswani"], "year": 2017,
                   "doi": "10.1000/adv.1", "arxiv_id": None, "venue": ""}},
        {"key": "mismatch", "status": "MISMATCH", "confidence": 0.7, "resolved_by": "doi",
         "evidence": {"resolved_title": "Deep Residual Learning for Image Super-Resolution",
                      "resolved_authors": ["Kaiming He"], "resolved_year": 2016,
                      "matched_doi": "10.1109/cvpr.2016.90", "source": "crossref",
                      "source_url": "https://api.crossref.org/works/10.1109/cvpr.2016.90",
                      "title_ratio": 0.73, "authors_ratio": 1.0, "year_delta": 0},
         "reasons": ["title too dissimilar: 0.73 < 0.90"], "checked_at": "2026-11-03T00:00:00Z",
         "input": {"title": RESNET, "authors": ["Kaiming He"], "year": 2016,
                   "doi": "10.1109/CVPR.2016.90", "arxiv_id": None, "venue": ""}},
        {"key": "err", "status": "ERROR", "confidence": 0.0, "resolved_by": None,
         "evidence": {}, "reasons": ["network"], "checked_at": "2026-11-03T00:00:00Z",
         "input": {"title": "Something", "authors": [], "year": None, "doi": None,
                   "arxiv_id": None, "venue": ""}},
    ]
    out = tmp_path / "verified_citations.csv"
    n = vc.write_verified_csv(results, out)
    rows = list(csv.DictReader(io.StringIO(out.read_text(encoding="utf-8"))))
    assert n == 1
    # canonical register schema (tools/CONTRACTS.md 1): id, url, retrieved_on, command
    assert [r["id"] for r in rows] == ["good"]
    assert set(rows[0]) == set(CANONICAL_FIELDS)
    assert all(r["url"].strip() for r in rows)
    assert all(r["retrieved_on"].strip() for r in rows)
    assert all(r["verified_by_command"].strip() for r in rows)
    assert "mismatch" not in {r["id"] for r in rows}
    assert "10.1109/cvpr.2016.90" not in out.read_text(encoding="utf-8")


def test_main_end_to_end_writes_only_the_verified_row(tmp_path, monkeypatch):
    """One DOI-resolved VERIFIED, one MISMATCH, one NOT_FOUND, one ERROR -> one CSV row."""
    p = write_csv(tmp_path / "mix.csv", [
        ("ok", TITLE, "Ashish Vaswani", "2017", "10.1000/adv.1", "", ""),
        ("wrongdoi", RESNET, "Kaiming He", "2016", "10.1109/CVPR.2016.90", "", ""),
        ("ghost", "Quantum Cheese Transformers for Rural Cows", "A Fake", "2022", "", "", ""),
        ("dead", "Some Other Paper About Things", "B Real", "2020", "", "", ""),
    ])

    def route(url):
        if "works/10.1000/adv.1" in url:
            return cr_one(TITLE, year=2017, doi="10.1000/adv.1")
        if "works/10.1109/cvpr.2016.90" in url:
            return cr_one("Deep Residual Learning for Image Super-Resolution",
                          authors=(("Kaiming", "He"),), year=2016, doi="10.1109/cvpr.2016.90")
        if "api.datacite.org" in url:
            return ""
        if "works?query" in url:
            # title search: nothing relevant for the ghost, a dead host for the last record
            if "Some+Other+Paper" in url:
                raise netcache.FetchError("connection reset")
            return cr_multi(_item("A Survey of Graph Neural Networks for Molecular Property Prediction",
                                  authors=(("Some", "Author"),), year=2022, doi="10.1000/irrelevant"))
        return ""

    monkeypatch.setattr(vc.netcache, "make_fetcher", lambda online, **kw: (route, _Perf()))
    out_dir = tmp_path / "out"
    code = vc.main(["--csv", str(p), "--offline", "--quiet", "--out-dir", str(out_dir)])
    assert code == 1

    rows = list(csv.DictReader(io.StringIO(
        (out_dir / "verified_citations.csv").read_text(encoding="utf-8"))))
    assert [r["id"] for r in rows] == ["ok"]
    row = rows[0]
    assert row["url"].startswith("https://api.crossref.org/")
    assert row["retrieved_on"].strip()
    assert row["doi_or_arxiv"] == "10.1000/adv.1"
    assert set(row) == set(CANONICAL_FIELDS)

    report = json.loads((out_dir / "verification_report.json").read_text(encoding="utf-8"))
    assert report["n_total"] == 4
    assert report["n_verified"] == 1
    assert report["n_verified"] + report["n_mismatch"] + report["n_not_found"] + report["n_error"] == 4
    statuses = {r["key"]: r["status"] for r in report["results"]}
    assert statuses == {"ok": "VERIFIED", "wrongdoi": "MISMATCH", "ghost": "NOT_FOUND", "dead": "ERROR"}
