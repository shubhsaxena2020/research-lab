# NOVELTY-R3 — round-3 novelty refresh (R3-5, 2026-11-08)

Scope: HEAD-REVIEW.md condition 1 — re-check the C1 slice beyond arXiv: gate on retrieval features,
two thresholds, both directions per rung. Sources: OpenAlex (live this session), Crossref, Semantic Scholar.

## 1. What was run

- OpenAlex `works?search=`: 18 slice-wording queries, 2026-11-08 (UTC 08:41-08:43), all HTTP 200, raw JSON cached in
  `02_literature/related-work-r3/raw/openalex_r3/q01.json` .. `q18.json` (query log `openalex_r3_log.json`).
- Semantic Scholar `GET /graph/v1/paper/search`: **refused again** — HTTP 429 on the first request at 08:43 UTC
  ("Too Many Requests ... apply for a key"), same as NOVELTY-CHECK.md §2. Recorded, not retried. Contribution: zero queries.
- Crossref `works?query=...`: one exploratory query run (2026-11-08); returns bibliographic matches only, none relevant
  to the C1 slice. Crossref is used for DOI resolution, not discovery.

Rate-limit state: OpenAlex `X-RateLimit-Remaining` ~980 credits after 18 searches (10 credits/search). Polite pacing 1.2 s.

## 2. Query log (OpenAlex, 2026-11-08)

| # | Query | meta.count | Top candidate checked |
|---:|---|---:|---|
| 1 | abstention gate retrieval features two thresholds | 765 | DeclineCraft (W7223089569) — no retrieval-feature thresholds |
| 2 | retrieval feature abstention both directions per rung | 20 | none relevant |
| 3 | hard negative ladder abstention precision false refusal | 57 | "Better Retrievers, Worse Labels" — evaluation critique, no gate |
| 4 | negative hardness ladder retrieval gate | 66 | none relevant |
| 5 | two threshold abstention band retrieval | 639 | "Where Abstention Lives" — interface placement, no retrieval features |
| 6 | abstain precision abstain recall false refusal rung | 38 | none relevant |
| 7 | overlap matched negatives abstention gate | 1526 | none relevant |
| 8 | surface features abstention audit AUROC | 180 | "Two Axes of LLM Abstention" — probes, not retrieval features |
| 9 | retrieval score gate answerability ladder | 118 | none relevant |
| 10 | dead zone abstention retrieval | 83 | none relevant |
| 11 | per rung abstention precision coverage | 67 | none relevant |
| 12 | retrieval-only features abstention calibration | 1361 | "Geometry-Calibrated Conformal Abstention" — confidence, not retrieval features |
| 13 | hardness ladder negatives abstention | 103 | none relevant |
| 14 | answerability gate retrieval features false refusal | 127 | none relevant |
| 15 | negative construction abstention gate both directions | 1100 | "Where Abstention Lives" — already checked |
| 16 | separability audit retrieval features | 2830 | none relevant |
| 17 | overlap matched negatives retrieval abstention | 1384 | "Claim-Aware Scientific RAG" — single confidence gate, SciFact |
| 18 | two thresholds retrieval features abstention gate | 765 | DeclineCraft (re-appeared) — same verdict |

## 3. Candidate collisions checked (abstracts fetched, see raw/)

- DeclineCraft (arXiv:2610.28340): reports CAR + Answerable Attempt Rate, no retrieval-feature thresholds, no per-rung table. Already in register.
- Where Abstention Lives (W7204496982): interface placement in a 863k-param model; no retrieval features, no ladder.
- Two Axes of LLM Abstention (arXiv:2607.08456): two thresholds, but on correctness/answerability scores from hidden-state probes, not retrieval features; reports wrong-answer and unanswerable-answer rates. Adjacent, not a collision.
- Claim-Aware Scientific RAG (W7131412174): single confidence gate on SciFact; no threshold pair, no per-rung reporting.
- Better Retrievers, Worse Labels (W7225120617): evaluation critique of sufficiency labels; no gate.
- Cost-Aware Abstention (W7223406000): cost-conditional threshold on ticket classifiers; no retrieval features, no ladder.
- Geometry-Calibrated Conformal Abstention (W7159578267): confidence-based conformal abstention; no retrieval features.
- HALT-RAG (W4416066396): NLI-ensemble hallucination detector; no retrieval features, no ladder.
- Bandits with Abstention (W4415795294): bandit aggregation; unrelated domain.

None of these fits two thresholds on retrieval-side features alone AND reports both directions at every rung of one negative ladder.

## 4. Verdict

Still "incremental". No collision found in OpenAlex (18 slice queries, ~11,000 records screened at the top-5 level)
or in the prior arXiv sweep (91 queries). Semantic Scholar remains unavailable (HTTP 429) and contributes zero
queries, as before; Crossref contributed identifier resolution only. The C1 slice — two dev-fitted thresholds
on six retrieval features with a dead zone, evaluated held out, reporting abstain precision, abstain recall and
false-refusal rate at every rung of one negative-hardness ladder, plus where the band sits relative to the
observed dev feature range — remains unoccupied in the two sources reachable this session.

C1 is not dead. The rule in HEAD-REVIEW.md condition 1 (move to C3 if a paper fits two thresholds on
retrieval features AND reports both directions per rung) did not fire.

No new citations were added (all nearest neighbours already in 02_literature/verified_citations.csv); see
`new_citations.csv` (header only).

## 5. Limits disclosed

- Semantic Scholar refused (HTTP 429); zero queries. Creating a key is the student's decision.
- OpenAlex `?search=` ranks by relevance over title+abstract+fulltext; top-5 per query only, so a miss here
  means "absent from the top 5 of a relevance search", not "absent from the literature".
- Crossref used for DOI resolution and one exploratory search, not discovery.
- No ACL-anthology-only papers are visible unless indexed in OpenAlex.
