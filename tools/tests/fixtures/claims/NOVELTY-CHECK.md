# NOVELTY CHECK (fixture — synthetic, not a real literature search)

TOY/FIXTURE file used by `tools/tests/test_claims_audit.py`. It exists so the validator can
test the "state of the art / novel / first needs a novelty row" rule without network access.
Do not cite this file as evidence in a real paper.

Searches run (would be OpenAlex + Crossref + arXiv in a real check, 1 request/second):

1. query: "compact cross-encoder reranker 5.3 point gain"
   result: closest work is a 2023 reranking survey; no 5.3-point claim on this benchmark.
2. query: "audit claim binding abstract evidence table"
   result: no prior audit binds every abstract claim to a stored result.

Verdict: no prior audit binds every abstract claim to a stored result. The contribution claimed
in the fixture draft is the audit procedure, not the reranker. Recorded by: fixture, not a human.
