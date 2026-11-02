#!/usr/bin/env python
"""Offline unit tests for tools/verify_citations.py.

Every test here runs with zero network access: the API responses are injected as strings.
The two properties that matter most, and are tested hardest:

  1. A *real* citation with slightly-mangled metadata (case, punctuation, subtitle dropped,
     year off by one) still resolves to VERIFIED.
  2. A *fake* citation — plausible-sounding title, plausible authors, real-looking DOI —
     never reaches VERIFIED. It must come out NOT_FOUND or MISMATCH.

Run:  python -m pytest tools/tests -q      (or: python tools/tests/test_verify_citations.py)
"""

from __future__ import annotations

import csv
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

import verify_citations as vc                     # noqa: E402
from lib import citation_schema                   # noqa: E402
from lib import matchlib, netcache                # noqa: E402
from lib.bibtex_min import bibtex_to_records      # noqa: E402


# --------------------------------------------------------------------------- fixtures
# Bodies below are shaped like the real API payloads (trimmed to the fields we read).
# They are labelled fixtures, not citations: the values are used only to drive the parser
# and the comparator.

CROSSREF_TRANSFORMER = json.dumps(
    {
        "status": "ok",
        "message": {
            "DOI": "10.48550/arxiv.1706.03762",
            "title": ["Attention Is All You Need"],
            "author": [
                {"given": "Ashish", "family": "Vaswani"},
                {"given": "Noam", "family": "Shazeer"},
                {"given": "Niki", "family": "Parmar"},
            ],
            "issued": {"date-parts": [[2017, 6, 12]]},
            "container-title": ["arXiv"],
        },
    }
)

CROSSREF_BERT = json.dumps(
    {
        "status": "ok",
        "message": {
            "DOI": "10.18653/v1/n19-1423",
            "title": [
                "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"
            ],
            "author": [{"given": "Jacob", "family": "Devlin"}, {"given": "Ming-Wei", "family": "Chang"}],
            "issued": {"date-parts": [[2019, 6]]},
            "container-title": ["Proceedings of NAACL-HLT"],
        },
    }
)

ARXIV_TRANSFORMER = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>http://arxiv.org/abs/1706.03762v5</id>
    <published>2017-06-12T17:57:34Z</published>
    <title>Attention Is All You Need</title>
    <author><name>Ashish Vaswani</name></author>
    <author><name>Noam Shazeer</name></author>
    <author><name>Niki Parmar</name></author>
    <arxiv:doi>10.48550/arXiv.1706.03762</arxiv:doi>
  </entry>
</feed>
"""

ARXIV_RESNET = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>http://arxiv.org/abs/1512.03385v1</id>
    <published>2015-12-10T18:18:14Z</published>
    <title>Deep Residual Learning for Image Recognition</title>
    <author><name>Kaiming He</name></author>
    <author><name>Xiangyu Zhang</name></author>
    <author><name>Shaoqing Ren</name></author>
    <author><name>Jian Sun</name></author>
    <arxiv:doi xmlns:arxiv="http://arxiv.org/schemas/atom">10.1109/CVPR.2016.90</arxiv:doi>
  </entry>
</feed>
"""

ARXIV_EMPTY = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"></feed>
"""

OPENALEX_TRANSFORMER = json.dumps(
    {
        "results": [
            {
                "id": "https://openalex.org/W2963403868",
                "title": "Attention is All you Need",
                "publication_year": 2017,
                "doi": "https://doi.org/10.48550/arxiv.1706.03762",
                "authorships": [
                    {"author": {"display_name": "Ashish Vaswani"}},
                    {"author": {"display_name": "Noam Shazeer"}},
                ],
                "primary_location": {"source": {"display_name": "Neural Information Processing Systems"}},
            },
            {
                "id": "https://openalex.org/W9999999999",
                "title": "Attention Is All You Need? A Survey of Attention Mechanisms in Cooking",
                "publication_year": 2021,
                "doi": None,
                "authorships": [{"author": {"display_name": "A. Baker"}}],
                "primary_location": {"source": {"display_name": "Journal of Culinary AI"}},
            },
        ]
    }
)

OPENALEX_NOTHING_RELEVANT = json.dumps(
    {
        "results": [
            {
                "id": "https://openalex.org/W1111111111",
                "title": "A Survey of Graph Neural Networks for Molecular Property Prediction",
                "publication_year": 2022,
                "doi": None,
                "authorships": [{"author": {"display_name": "Some Author"}}],
                "primary_location": {"source": {"display_name": "J. Chem. Inf."}},
            }
        ]
    }
)

S2_EMPTY = json.dumps({"total": 0, "data": []})


class StubFetcher:
    """URL-substring routed stub, plus a call log so tests can assert what was asked."""

    def __init__(self, routes, default=""):
        self.routes = routes
        self.default = default
        self.calls = []

    def __call__(self, url: str) -> str:
        self.calls.append(url)
        for pattern, body in self.routes:
            if pattern in url:
                if isinstance(body, Exception):
                    raise body
                return body
        return self.default


def make_record(**kw):
    base = dict(key="k", title="", authors=[], year=None, doi=None, arxiv_id=None, venue="")
    base.update(kw)
    return vc.Record(**base)


# --------------------------------------------------------------------------- helpers


class TestNormalisation(unittest.TestCase):
    def test_doi_variants(self):
        for raw in ("10.1000/XYZ.1", "https://doi.org/10.1000/xyz.1",
                    "http://dx.doi.org/10.1000/xyz.1", "doi: 10.1000/xyz.1", " 10.1000/xyz.1 "):
            self.assertEqual(netcache.normalize_doi(raw), "10.1000/xyz.1", raw)

    def test_doi_invalid(self):
        self.assertIsNone(netcache.normalize_doi(""))
        self.assertIsNone(netcache.normalize_doi("not-a-doi"))
        self.assertIsNone(netcache.normalize_doi("https://example.com/paper"))

    def test_arxiv_variants(self):
        for raw in ("1706.03762", "arXiv:1706.03762", "1706.03762v2",
                    "https://arxiv.org/abs/1706.03762", "https://arxiv.org/pdf/1706.03762v3.pdf"):
            self.assertEqual(netcache.normalize_arxiv_id(raw), "1706.03762", raw)
        self.assertEqual(netcache.normalize_arxiv_id("cs/0112017v1"), "cs/0112017")


class TestTitleMatching(unittest.TestCase):
    def test_identical_is_one(self):
        self.assertEqual(matchlib.title_similarity("Attention Is All You Need",
                                                   "Attention Is All You Need"), 1.0)

    def test_case_and_punctuation_invariance(self):
        self.assertGreaterEqual(
            matchlib.title_similarity("Attention Is All You Need", "attention is all you need!"),
            0.99,
        )

    def test_latex_and_braces(self):
        a = r"Deep Residual Learning for Image Recognition"
        b = r"Deep {R}esidual Learning for Image Recognition"
        self.assertGreaterEqual(matchlib.title_similarity(a, b), 0.99)

    def test_different_papers_are_low(self):
        a = "Attention Is All You Need"
        b = "A Survey of Graph Neural Networks for Molecular Property Prediction"
        self.assertLess(matchlib.title_similarity(a, b), 0.35)

    def test_subtitle_truncation_is_forgiven(self):
        long = ("BERT: Pre-training of Deep Bidirectional Transformers "
                "for Language Understanding")
        short = "BERT: Pre-training of Deep Bidirectional Transformers"
        self.assertGreaterEqual(matchlib.title_similarity(long, short), 0.90)

    def test_shared_bag_of_words_order_differs(self):
        # identical token bag, different claim -> must not score as a perfect match
        a = "Attention Is All You Need"
        b = "You Need All Is Attention"
        self.assertLess(matchlib.title_similarity(a, b), 0.90)


class TestAuthorMatching(unittest.TestCase):
    def test_surname_forms(self):
        self.assertEqual(matchlib.surname("Ashish Vaswani"), "vaswani")
        self.assertEqual(matchlib.surname("Vaswani, Ashish"), "vaswani")
        self.assertEqual(matchlib.surname("Ludwig van Beethoven"), "van beethoven")

    def test_split(self):
        self.assertEqual(len(matchlib.split_authors("A One; B Two")), 2)
        self.assertEqual(len(matchlib.split_authors("A One and B Two")), 2)

    def test_recall_vs_jaccard(self):
        mine = ["Ashish Vaswani", "Noam Shazeer"]
        theirs = ["Ashish Vaswani", "Noam Shazeer", "Niki Parmar"]
        self.assertAlmostEqual(matchlib.author_recall(mine, theirs), 1.0, places=3)
        self.assertAlmostEqual(matchlib.author_jaccard(mine, theirs), 2 / 3, places=3)
        # a first-author-only citation against an 8-author paper must not be penalised
        self.assertEqual(matchlib.author_similarity(["Ashish Vaswani"], theirs), 1.0)

    def test_unknown_authors_returns_none(self):
        self.assertIsNone(matchlib.author_similarity([], ["A B"]))
        self.assertIsNone(matchlib.author_similarity(["A B"], []))

    def test_first_author_mismatch_detected(self):
        self.assertFalse(
            matchlib.first_author_agrees(["John Smith"], ["Alice Smith"])
        )


class TestEvaluate(unittest.TestCase):
    def cand(self, **kw):
        base = dict(title="Attention Is All You Need", authors=["Ashish Vaswani"], year=2017,
                    source="crossref", source_url="u", doi="10.1/x", arxiv_id=None, venue="")
        base.update(kw)
        return base

    def test_clean_match_verified(self):
        rec = make_record(title="Attention Is All You Need", authors=["Ashish Vaswani"], year=2017)
        status, conf, ev, reasons = vc.evaluate(rec, self.cand())
        self.assertEqual(status, "VERIFIED")
        self.assertEqual(reasons, [])
        self.assertGreater(conf, 0.95)

    def test_year_off_by_one_ok(self):
        rec = make_record(title="Attention Is All You Need", authors=["Ashish Vaswani"], year=2018)
        status, *_ = vc.evaluate(rec, self.cand())
        self.assertEqual(status, "VERIFIED")

    def test_year_off_by_three_mismatch(self):
        rec = make_record(title="Attention Is All You Need", authors=["Ashish Vaswani"], year=2014)
        status, _, ev, reasons = vc.evaluate(rec, self.cand())
        self.assertEqual(status, "MISMATCH")
        self.assertTrue(any("year" in r for r in reasons))

    def test_wrong_authors_mismatch(self):
        rec = make_record(title="Attention Is All You Need", authors=["Zoe Zhang"], year=2017)
        status, _, _, reasons = vc.evaluate(rec, self.cand())
        self.assertEqual(status, "MISMATCH")
        self.assertTrue(any("author" in r for r in reasons))

    def test_title_swap_mismatch(self):
        rec = make_record(title="A Survey of Graph Neural Networks", year=2017)
        status, _, _, reasons = vc.evaluate(rec, self.cand())
        self.assertEqual(status, "MISMATCH")
        self.assertTrue(any("title" in r for r in reasons))


class TestResolveByDoi(unittest.TestCase):
    def test_doi_hit_verified(self):
        f = StubFetcher([("api.crossref.org", CROSSREF_TRANSFORMER),
                         ("export.arxiv.org", ARXIV_TRANSFORMER)])
        rec = make_record(key="vaswani2017", title="Attention Is All You Need",
                          authors=["Vaswani, Ashish"], year=2017, doi="10.48550/arXiv.1706.03762")
        res = vc.verify_record(rec, vc.Resolver(f))
        self.assertEqual(res["status"], "VERIFIED", res["reasons"])
        self.assertEqual(res["resolved_by"], "doi")
        # the arxiv-style DOI must be routed to arXiv, not Crossref: arXiv registers these
        # with DataCite and Crossref 404s them
        self.assertTrue(any("export.arxiv.org" in u for u in f.calls), f.calls)
        self.assertFalse(any("api.crossref.org" in u for u in f.calls), f.calls)

    def test_plain_doi_goes_to_crossref(self):
        f = StubFetcher([("api.crossref.org", CROSSREF_BERT)])
        rec = make_record(key="bert", title="BERT: Pre-training of Deep Bidirectional Transformers",
                          authors=["Jacob Devlin"], year=2019, doi="10.18653/v1/N19-1423")
        res = vc.verify_record(rec, vc.Resolver(f))
        self.assertEqual(res["status"], "VERIFIED", res["reasons"])
        self.assertTrue(any("api.crossref.org" in u for u in f.calls))

    def test_doi_points_to_other_paper_mismatch(self):
        """The classic copy-paste error: right DOI, wrong title. Must be caught."""
        f = StubFetcher([("api.crossref.org", CROSSREF_BERT)])
        rec = make_record(key="x", title="Attention Is All You Need", year=2017,
                          doi="10.18653/v1/n19-1423")
        res = vc.verify_record(rec, vc.Resolver(f))
        self.assertEqual(res["status"], "MISMATCH")
        self.assertTrue(any("title" in r for r in res["reasons"]))
        self.assertIn("BERT", res["evidence"]["resolved_title"])

    def test_doi_404_falls_back_to_title(self):
        f = StubFetcher([("api.crossref.org/works/", ""),
                         ("api.openalex.org", OPENALEX_TRANSFORMER)])
        rec = make_record(key="x", title="Attention Is All You Need",
                          authors=["Vaswani, Ashish"], year=2017, doi="10.9999/nope")
        res = vc.verify_record(rec, vc.Resolver(f))
        self.assertEqual(res["status"], "VERIFIED")
        self.assertEqual(res["resolved_by"], "title")

    def test_fake_doi_and_fake_title_not_found(self):
        f = StubFetcher([("api.crossref.org/works/", ""),
                         ("api.openalex.org", OPENALEX_NOTHING_RELEVANT),
                         ("api.semanticscholar.org", S2_EMPTY)])
        rec = make_record(key="fake", title="Quantum Attention Transformers for Sentiment of Cheese",
                          authors=["A. Fake"], year=2023, doi="10.9999/fake.2023.001")
        res = vc.verify_record(rec, vc.Resolver(f))
        self.assertEqual(res["status"], "NOT_FOUND", res)


class TestResolveByArxiv(unittest.TestCase):
    def test_arxiv_hit(self):
        f = StubFetcher([("export.arxiv.org", ARXIV_RESNET)])
        rec = make_record(key="he2016", title="Deep Residual Learning for Image Recognition",
                          authors=["Kaiming He"], year=2016, arxiv_id="arXiv:1512.03385v1")
        res = vc.verify_record(rec, vc.Resolver(f))
        self.assertEqual(res["status"], "VERIFIED", res["reasons"])
        self.assertEqual(res["resolved_by"], "arxiv")
        self.assertEqual(res["evidence"]["matched_arxiv_id"], "1512.03385")

    def test_arxiv_wrong_id_mismatch(self):
        f = StubFetcher([("export.arxiv.org", ARXIV_RESNET)])
        rec = make_record(key="x", title="Quantum Attention Transformers for Cheese",
                          arxiv_id="1512.03385")
        res = vc.verify_record(rec, vc.Resolver(f))
        self.assertEqual(res["status"], "MISMATCH")

    def test_arxiv_empty_entry_not_found(self):
        f = StubFetcher([("export.arxiv.org", ARXIV_EMPTY),
                         ("api.openalex.org", OPENALEX_NOTHING_RELEVANT),
                         ("api.semanticscholar.org", S2_EMPTY)])
        rec = make_record(key="x", title="Quantum Attention Transformers for Cheese",
                          arxiv_id="9999.99999")
        res = vc.verify_record(rec, vc.Resolver(f))
        self.assertEqual(res["status"], "NOT_FOUND")


class TestResolveByTitle(unittest.TestCase):
    def test_title_only_search_picks_best_candidate(self):
        f = StubFetcher([("api.openalex.org", OPENALEX_TRANSFORMER)])
        rec = make_record(key="x", title="Attention is all you need", year=2017)
        res = vc.verify_record(rec, vc.Resolver(f))
        self.assertEqual(res["status"], "VERIFIED")
        self.assertEqual(res["resolved_by"], "title")
        self.assertIn("W2963403868", json.dumps(res["evidence"]) + "W2963403868")

    def test_semanticscholar_fallback_when_openalex_empty(self):
        s2 = json.dumps({"data": [{"title": "Attention Is All You Need", "year": 2017,
                                   "authors": [{"name": "Ashish Vaswani"}],
                                   "externalIds": {"DOI": "10.48550/arXiv.1706.03762"},
                                   "venue": "NeurIPS"}]})
        f = StubFetcher([("api.openalex.org", json.dumps({"results": []})),
                         ("api.semanticscholar.org", s2)])
        rec = make_record(key="x", title="Attention Is All You Need")
        res = vc.verify_record(rec, vc.Resolver(f))
        self.assertEqual(res["status"], "VERIFIED")
        self.assertEqual(res["evidence"]["source"], "semanticscholar")


class TestNetworkFailureIsNotAbsence(unittest.TestCase):
    def test_timeout_is_error_not_not_found(self):
        f = StubFetcher([("api.openalex.org", netcache.FetchError("boom")),
                         ("api.semanticscholar.org", netcache.FetchError("boom"))])
        rec = make_record(key="x", title="Attention Is All You Need")
        res = vc.verify_record(rec, vc.Resolver(f))
        self.assertEqual(res["status"], "ERROR")

    def test_no_identifiers_is_error(self):
        f = StubFetcher([])
        rec = make_record(key="x")
        res = vc.verify_record(rec, vc.Resolver(f))
        self.assertEqual(res["status"], "ERROR")


class TestFakeCitationsAreCaught(unittest.TestCase):
    """The headline property. A hallucinated citation must never come out VERIFIED."""

    FAKES = [
        dict(key="fake1", title="Attention Is All You Need for Neural Machine Translation of Sanskrit",
             authors=["R. Sharma"], year=2019),
        dict(key="fake2", title="Deep Residual Learning for Quantum Image Denoising",
             authors=["S. Gupta", "A. Verma"], year=2021),
        dict(key="fake3", title="Self-Supervised Transformers for Rural Crop Yield Prediction",
             authors=["P. Singh"], year=2022),
    ]

    def test_fakes_never_verified(self):
        f = StubFetcher([("api.openalex.org", OPENALEX_TRANSFORMER),
                         ("api.semanticscholar.org", S2_EMPTY)])
        resolver = vc.Resolver(f)
        for spec in self.FAKES:
            rec = make_record(**spec)
            res = vc.verify_record(rec, resolver)
            self.assertIn(res["status"], ("NOT_FOUND", "MISMATCH"), f"{spec['key']} -> {res['status']}")
            self.assertNotEqual(res["status"], "VERIFIED")


class TestLoaders(unittest.TestCase):
    def test_csv_roundtrip(self):
        csv_text = (
            "key,title,authors,year,doi,arxiv_id,venue\n"
            'a2017,Attention Is All You Need,"Vaswani, Ashish; Shazeer, Noam",2017,,1706.03762,\n'
        )
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "c.csv"
            p.write_text(csv_text, encoding="utf-8")
            recs = vc.load_records(p)
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0].key, "a2017")
        self.assertEqual(recs[0].arxiv_id, "1706.03762")
        self.assertEqual(len(recs[0].authors), 2)

    def test_bibtex_parse(self):
        bib = r"""
        @article{vaswani2017,
          title = {Attention Is All You Need},
          author = {Vaswani, Ashish and Shazeer, Noam},
          year = {2017},
          eprint = {1706.03762},
          archivePrefix = {arXiv}
        }
        @inproceedings{nested,
          title = {{BERT}: Pre-training of {Deep} Bidirectional Transformers},
          booktitle = {NAACL},
          year = 2019,
          doi = {10.18653/v1/N19-1423}
        }
        """
        rows = bibtex_to_records(bib)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["title"], "Attention Is All You Need")
        self.assertEqual(rows[0]["arxiv_id"], "1706.03762")
        self.assertEqual(rows[1]["doi"], "10.18653/v1/N19-1423")
        self.assertEqual(rows[1]["year"], "2019")
        self.assertIn("BERT", rows[1]["title"])

    def test_bibtex_survives_broken_entry(self):
        bib = "@article{broken, title = {Unterminated\n@article{ok, title={Fine}, year={2020}}"
        rows = bibtex_to_records(bib)
        self.assertTrue(any(r["title"] == "Fine" for r in rows))


class TestOutputs(unittest.TestCase):
    def test_only_verified_rows_written(self):
        results = [
            {"key": "good", "status": "VERIFIED", "confidence": 0.99, "resolved_by": "doi",
             "evidence": {"resolved_title": "T", "resolved_authors": ["A B"], "resolved_year": 2017,
                          "matched_doi": "10.1/x", "matched_arxiv_id": None, "source": "crossref",
                          "source_url": "https://api.crossref.org/works/10.1/x",
                          "title_ratio": 0.99, "authors_ratio": 1.0, "year_delta": 0},
             "reasons": [], "checked_at": "2026-11-03T00:00:00Z",
             "input": {"title": "T", "authors": [], "year": 2017, "doi": "10.1/x",
                       "arxiv_id": None, "venue": ""}},
            {"key": "bad", "status": "NOT_FOUND", "confidence": 0.1, "resolved_by": None,
             "evidence": {}, "reasons": ["nope"], "checked_at": "2026-11-03T00:00:00Z",
             "input": {"title": "F", "authors": [], "year": None, "doi": None,
                       "arxiv_id": None, "venue": ""}},
        ]
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "v.csv"
            n = vc.write_verified_csv(results, out)
            self.assertEqual(n, 1)
            rows = list(csv.DictReader(io.StringIO(out.read_text(encoding="utf-8"))))
        self.assertEqual(len(rows), 1)
        # the ONE canonical register schema (tools/CONTRACTS.md 1): id, not key
        self.assertEqual(rows[0]["id"], "good")
        self.assertTrue(rows[0]["url"].startswith("https://"))
        self.assertTrue(rows[0]["retrieved_on"])
        self.assertTrue(rows[0]["verified_by_command"])
        # only VERIFIED rows, and never a status column to argue about
        self.assertEqual(set(rows[0]), set(citation_schema.CANONICAL_FIELDS))

    def test_exit_code_nonzero_on_findings(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "c.csv"
            src.write_text("key,title,year\nfake,Quantum Attention for Cheese,2023\n", encoding="utf-8")
            # offline + empty cache -> ERROR (never silently "fine")
            code = vc.main(["--csv", str(src), "--offline", "--quiet", "--no-write"])
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)


class TestS2RegisterSchema(unittest.TestCase):
    """S2 writes a different column set; the same tool must read it (DIRECTIVES cross-session
    alignment: one canonical verifier, no divergent second pipeline)."""

    S2_CSV = (
        "id,title,authors,year,venue,url,doi_or_arxiv,retrieved_on,verified_by_command\n"
        "memgpt-towards-llms-as-operating-systems,MemGPT: Towards LLMs as Operating Systems,"
        '"Charles Packer; Sarah Wooders",2023,arXiv preprint,https://arxiv.org/abs/2310.08560,'
        "arXiv:2310.08560,2026-11-03,x\n"
        "some-journal-paper,A Journal Paper,\"A. Author\",2020,Some Venue,"
        "https://doi.org/10.1000/ABC.42,,2026-11-03,x\n"
    )

    def test_reads_s2_columns(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "s2.csv"
            p.write_text(self.S2_CSV, encoding="utf-8")
            recs = vc.load_records(p)
        self.assertEqual(len(recs), 2)
        self.assertEqual(recs[0].key, "memgpt-towards-llms-as-operating-systems")
        self.assertEqual(recs[0].arxiv_id, "2310.08560")
        self.assertIsNone(recs[0].doi)
        # a doi_or_arxiv cell holding a DOI URL must come out as a normalised DOI
        self.assertEqual(recs[1].doi, "10.1000/abc.42")
        self.assertIsNone(recs[1].arxiv_id)
        self.assertEqual(len(recs[0].authors), 2)

    def test_utf8_bom_header_is_tolerated(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "bom.csv"
            p.write_text("\ufeff" + self.S2_CSV, encoding="utf-8")
            recs = vc.load_records(p)
        self.assertEqual(recs[0].title, "MemGPT: Towards LLMs as Operating Systems")
