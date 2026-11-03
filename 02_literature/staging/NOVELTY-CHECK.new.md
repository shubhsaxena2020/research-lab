# NOVELTY-CHECK — finalist C1 (hardness ladder for retrieval-feature abstention) and C3 (scam operating points)

S2b re-run · 2026-11-03 · sources: **OpenAlex (new this session, 84 queries)**, arXiv (91 queries, S2,
2026-11-03), Semantic Scholar (**requested, refused — see §2**), Crossref (identifier resolution only).

Verdict up front: **C1 — STILL INCREMENTAL, no collision found. C3 — STILL INCREMENTAL, no collision
found, but one of its supporting claims is now false and must be dropped (§4).** Nothing here licenses
the word "novel". The previous version of this document said the check was one index deep; it is now two,
with the second still partial because Semantic Scholar refused the request and OpenAlex's free tier is
metered (§2). What the evidence supports is this: no prior work among ~3,700 OpenAlex records and the
91-query arXiv sweep fits two thresholds on retrieval-side features and reports both directions at every
rung of one negative ladder. That is a statement about what these queries returned, not about the
literature.

---

## 1. What this session actually ran

| Source | Queries | Records returned | Unique works screened | Notes |
|---|---:|---:|---:|---|
| OpenAlex `works?search=` | **84** | 84 × 50 = 4,200, deduped to **3,681** | 3,681 | 48 re-runs of the family-A/family-D pre-scan queries + 36 new slice-wording queries (18 C1 + 18 C3) |
| arXiv API | 91 | — | ~500 skimmed, 72 verified | S2's original sweep, unchanged; see `NOVELTY-PRESCAN.md` |
| Semantic Scholar | 1 attempted | 0 | 0 | **HTTP 429 on the first unauthenticated request**, 00:08 UTC; recorded, not retried (§2) |
| Crossref | resolution only | — | 26 | used to resolve DOIs for the register, not for discovery |

Every OpenAlex query, its timestamp, its reported `meta.count` and the path of its cached raw JSON are in
`02_literature/staging/S2b-openalex-queries.jsonl`; the append-only record of every work returned is
`02_literature/staging/S2b-openalex-hits.jsonl`; raw bodies are under `02_literature/raw/openalex/`.
Counts in §6 are OpenAlex's own `meta.count` (its estimate over the whole index), not rows kept. Summed
across the 84 queries: 46,451,339 records — a measure of how crowded the neighbourhood is, not of how
many papers are relevant.

Screening path: 3,681 unique works → 387 (C1) and 241 (C3) passed a four-concept filter (abstention
vocabulary + retrieval vocabulary + threshold/gate vocabulary + hardness/prevalence vocabulary) → **49
papers read at abstract level by six independent readers in six batches**, each required to quote a
verbatim supporting sentence and to fetch the record when the abstract did not settle the question.
Their reports are in `02_literature/staging/S2b-reads/`. The verdicts below are the lead's, reconciled
against those reports and their quoted sentences.

## 2. Two coverage limits this session did not fix

**Semantic Scholar refused.** `GET /graph/v1/paper/search` with no key returned HTTP 429 on the first
request at 00:08 UTC ("Too Many Requests … apply for a key"). Per the prompt the endpoint was not polled
again, so **Semantic Scholar contributed zero queries**. A free key would fix this; creating one requires
signing up with the student's email address, which is the student's decision, not this session's. Until
then this is a two-source check, not a four-source one.

**OpenAlex's anonymous tier is metered, not free.** Measured here: `X-RateLimit-Limit: 1000` credits,
**10 credits per search call** (`?search=` = $0.001; filters = $0.0001; lookups by DOI/ID are free).
That is ~100 searches per day **for the whole IP**, shared with S1 and any other process on this machine.
84 queries consumed 840 credits and the account was left at ~80. A free API key raises the ceiling
tenfold and is the highest-value fix for the next pass. Two consequences, both disclosed: (a) the
anonymous search cluster returned 13 transient 429s ("temporarily rate-limited while the search cluster is
under elevated load … retry in Ns"), all timestamped in the query log; the harvester was re-tuned to pace
adaptively instead of hammering, and the three earlier scripts that stop at the first 429 are kept on disk
as evidence (`staging/S2b-harvest-openalex{,‑v2,‑v3}.py`) — that is a deliberate, documented deviation
from "stop on the first 429" made because the literal rule left 56 of 84 queries unrun; (b) OpenAlex
abstracts are sometimes truncated mid-sentence, which is why six papers needed their landing page fetched.

One more limit: `?search=` ranks by relevance over title+abstract+fulltext and the budget did not allow
`rerank=true`, so recall at rank 50 is good but not exhaustive. A miss here is "absent from the top 50 of
a relevance search", never "absent from the literature".

## 3. C1 — "How Hard Are Your Negatives?" — no collision, still incremental

The slice C1 claims is unchanged and still unoccupied in both indexes:

> two separate thresholds fitted on dev **using retrieval-side features only** (no generator call, no
> hidden-state probe, no second model), with a dead zone between them, evaluated held out and reported
> as abstain precision, abstain recall **and** a false-refusal rate **at every rung of one
> negative-hardness ladder**, with the band's position relative to the observed dev feature range
> printed as a diagnostic.

### New closest prior work found by the OpenAlex pass (none of these rows existed in the S2 version)

| # | Paper (year, identifier) | What it occupies | Verdict |
|---|---|---|---|
| N1 | *Beyond Confidence: Adaptive Abstention in Dual-Threshold Conformal Prediction for Autonomous System Perception* (2025, arXiv:2502.07255) | **The two-threshold idea itself**: a conformal threshold plus a separately optimised abstention threshold, with an abstention band between them, distribution-free. Object is camera/LiDAR perception (CIFAR-100, ImageNet1K, ModelNet40); features are model scores, not retrieval scores; no ladder, no false-refusal column. | CLOSE — the nearest thing to "two thresholds" in 3,681 records, and the reason C1 cannot claim the band as its own idea |
| N2 | *Predictable Failure in Multi-Hop Retrieval: Score-Distributional Confidence Scoring and Abstention* (2026, arXiv:2609.22056) | Retrieval-features-only confidence score with **no LLM call**, abstention evaluated across five named failure regimes with a coverage sweep. Regimes are failure types, not a hardness ladder; one policy, no dead zone, no over-refusal rate. | CLOSE — occupies "cheap retrieval-side signal + abstention per failure category" |
| N3 | *Sufficiency-Gated Retrieval-Augmented Generation: Reducing Hallucination via Context Adequacy Estimation* (2026, doi:10.32604/cmc.2026.088937) | Retrieval-side sufficiency gate at a calibrated single operating point, **reporting wrongful refusal of sufficient contexts (7.0%)** — one half of the false-refusal column. | CLOSE — the false-refusal idea is published, as a single number |
| N4 | *Before Answering: Evidence Sufficiency under Size-Matched Memory Construction* (2026, arXiv:2609.32269) | The negative-construction half of the ladder: passage deletion leaks the label, and a surface-only adversary reaches AUROC 0.979 from paragraph count alone. | CLOSE — occupies the separability finding C1 calls its hard gate |
| N5 | *Learning When to Remember: Risk-Sensitive Contextual Bandits for Abstention-Aware Memory Retrieval* (2026, arXiv) | Retrieval-feature-only abstention with an explicit false-positive penalty and a graded action set that subsumes a dead zone. | CLOSE — a learned bandit policy, not dev-fitted thresholds; no ladder, no per-rung table |
| N6 | *BalanceRAG: Joint Risk Calibration for Cascaded Retrieval-Augmented Generation* (2026, Findings of ACL) | Two-threshold-style "operating point" with admit / escalate / refuse and coverage reporting. | ADJACENT — cut points sit on generator uncertainty in the LLM branch, not on retrieval features |
| N7 | *The Confidence Gate Theorem: When Should Ranked Decision Systems Abstain?* (2026, arXiv:2603.09947) | Theory of when confidence-based abstention is monotone, plus a deployment diagnostic. | ADJACENT — ranked recommenders/ads/triage, no retrieval features |
| N8 | *Training Negatives Still Matter After Calibrating Answerability Readouts* (2026, arXiv:2610.26461) | Controlled study of training-negative construction on answerability readouts (SQuAD 2.0, RepLiQA) with post-hoc AUROC. | ADJACENT — training negatives, not evaluation-time rungs; one readout policy |
| N9 | *RCL: A Retrieval-Confidence Layer for Detecting Insufficient Context in Enterprise RAG* (2026, arXiv) | Retrieval-confidence gate before generation with three actions. | ADJACENT — one threshold, three actions, no per-rung metrics |
| N10 | *Reliable Biomedical RAG with Answerability-Aware Hybrid Retrieval* (2026) | Retrieval-score gate on a fused BM25+dense score, trained with domain-similar hard negatives. | CLOSE — nearest on "retrieval-score gate + hard negatives"; no threshold pair, no rungs |
| N11 | *Do LLMs Know When Evidence is Insufficient? An Evidence Sufficiency Benchmark for Answer-Abstention Calibration* (2026, Comput. Mater. Contin.) | A five-level evidence gradient (L1–L5) with abstention calibration — a ladder, done prompt-side. | ADJACENT — the ladder exists; the object is model behaviour, not a fitted gate |
| N12 | *Cost-Aware Gated Retrieval* (2026, Research Square) | Two decision points, cost-aware, decoupling retrieval initiation from escalation. | ADJACENT — both decisions sit on model logit-gap features, not on one retrieval scale |
| N13 | *Where Abstention Lives* (2026, Research Square, doi:10.21203/rs.3.rs-10839567/v1) | Pre-registered four-way comparison of abstention interfaces in one small model. | ADJACENT — interface placement; no retrieval features, no ladder. **Flag: preprint, not peer-reviewed** |

### The wording sweep — the check that tests the slice rather than the family

Over all 3,681 unique records, counting title+abstract matches (`staging/S2b-phrase-sweep.json`):

| Slice phrase | Records | What they are |
|---|---:|---|
| "dead zone" / "dead-zone" / "dead band" | **0** | the term is not in use |
| "two threshold" / "two-threshold" | 3 | 2007–2008 SVM-with-reject-option papers and one vaccination-policy survey — none about retrieval |
| "dual threshold" | 1 | N1 (perception, conformal) |
| "admit and refuse" / "admit/refuse" | 0 | — |
| "abstain precision" / "abstain recall" | 0 | C1's metric names are not in use in this corpus |
| "negative hardness" / "per rung" / "retrieval-side feature" / "retrieval-only feature" | 0 | — |
| "false refusal" | 17 | almost all LLM safety over-refusal (persona prompts, XSTest); none per-rung retrieval |
| "threshold placement" / "outside the observed range" | 1 / 0 | a 2014 paper on where to place alert thresholds on abnormality scores |

Read it for what it is: the *vocabulary* of the C1 slice is unused. That is weak evidence for the idea
being unoccupied (a paper can do the thing without the words) and strong evidence that C1 must define its
terms before using them — a reviewer searching for "dead zone" finds nothing, which cuts both ways.

### Verdict for C1: STILL INCREMENTAL

No COLLISION. Nearest neighbours: N1 (the two-threshold construct, in perception), N2 and N3 (cheap
retrieval-side abstention with partial two-sided reporting), N4 (the separability finding), N10 (a
retrieval-score gate trained on hard negatives). The delta that survives all of them must be stated
exactly: *a four-rung negative ladder, held out per rung, with two dev-fitted thresholds on six retrieval
features, reporting abstain precision, abstain recall and false-refusal rate per rung, plus where the band
sits relative to the observed dev feature range.* That is a one-page measurement contribution — a workshop
paper — and the introduction must say so. **C1 is not dead.**

## 4. C3 — operating points for a small scam detector — no collision, still incremental

The slice: an operating-point table (precision, recall, alerts per 10,000 messages) at 0.1%–1% base
rates, threshold chosen from a stated cost ratio, on code-mixed Indian English SMS.

### New closest prior work found by the OpenAlex pass

| # | Paper (year, identifier) | What it occupies | Verdict |
|---|---|---|---|
| M1 | *Default Zero-Shot LLM APIs Over-Flag Indian Financial SMS: A Policy-Aligned Benchmark and Template-Level Analysis* (2026, GroundLM, doi:10.18653/2026.groundlm-1.79) | **Hinglish/Indian financial SMS with an explicit false-positive rate at a fixed operating point** (0.4% FPR at 0.980 recall, against a 1% FPR gate). | CLOSE — the nearest rival; single operating point, no cost ratio, no alert-volume table |
| M2 | *Anonymous Supplementary Artifact — EMNLP 2026 Industry Track (Multilingual Indian SMS Scam Detection)* (2026, Zenodo) | Indian SMS with a real threshold sweep τ∈{0.30…0.90}. | CLOSE — FPR-only: no recall at base rate, no alert volume, no cost ratio. Anonymous artefact: evidence of a live submission, not a citable result |
| M3 | *The Fragility of Phishing Detection Models: Evidence from Cross-Corpus Transfer, Prevalence Shift, Artifact Learning, and Evasion Risk* (2026, Big Data Cogn. Comput., doi:10.3390/bdcc10070211) | Prevalence shift and threshold dependence as the subject. | CLOSE — phishing **email**; alert-budget cap rather than cost ratio; no per-10,000 table |
| M4 | *ConformalGuard: False-Positive-Controlled Action Gating for LM Classifiers* (2026, arXiv:2610.14365) | Finite-sample control of the deployment false-positive rate for phishing screening, moderation and fraud triage, comparing conformal, isotonic and raw thresholds. | CLOSE — the deployment-FPR half, empirically; no prevalence sweep, no cost ratio, no alert volume |
| M5 | *Cost-Sensitive Conformal Prediction and Human-in-the-Loop Abstention for Imbalanced High-Stakes Decisions* (2026, arXiv) | Cost-controlled thresholds and break-even deferral costs under imbalance. | CLOSE — cost machinery without a prevalence table |
| M6 | *Distribution-Free Error Control for Fraud Alert Triage* (2026) | Sweeps 20–200 bp prevalence, alert precision 0.86–0.93. | CLOSE — the prevalence sweep exists in fraud; the threshold is a 10% FDR level, not a cost ratio |
| M7 | *Objective over Architecture: Fraud Detection Under Extreme Imbalance in Bank Account Opening* (2025) | Operating points at 1.10% prevalence. | CLOSE — one point per model, selected by f1_weighted |
| M8 | *Explainable fraud detection under fixed false positive rate* (2026, PeerJ CS) | Threshold set by a hard FPR ≤ 1% at 0.172% prevalence; recall 0.79–0.83. | CLOSE — a constraint, not a cost ratio; credit card |
| M9 | *The Threshold, Not the Model: A Cost-Sensitive Re-Evaluation of Offensive Language Detection* (2026) | The framing "the threshold, not the model", cost-sensitive. | ADJACENT — different task, no alert volume |
| M10 | *Beyond Keywords: Attack Signatures and a Diagnostic Benchmark for Multilingual Scam Detection in Indian Languages* (2026, Zenodo, doi:10.5281/zenodo.22867073) | In-distribution evaluation is the wrong unit; Indian multilingual (incl. code-mixed) scam benchmark. | ADJACENT — an evaluation critique plus benchmark, not an operating-point table |
| M11 | *A Hybrid Context-Aware Hinglish Spam And Scam Detection System Using Ensemble Machine Learning* (2026, Zenodo, doi:10.5281/zenodo.20153347) | **A Hinglish spam/scam corpus of 5,200 messages**, soft-voting ensemble, accuracy/F1 reported. | CLOSE on the domain claim, ADJACENT on the slice — see below |

### Verdict for C3: STILL INCREMENTAL, with one claim retired

No COLLISION: nothing found publishes precision, recall **and** alerts-per-10,000 across several
0.1%–1% base rates with a threshold set from a stated cost ratio. The two halves of the ideal stay
separate — cost-aware thresholds and alert volume in credit-card fraud (M5–M8), Indian code-mixed SMS
under FPR gates with no cost term (M1, M2).

**One supporting claim is now false and is retired here.** C3's pitch argued the corpus itself was the
asset: that English UCI-SMS-style data cannot carry "aapka KYC expire ho gaya hai" constructions and that
no Indian code-mixed SMS corpus exists. M11 (5,200 Hinglish messages) and M1/M2 exist. The corpus is no
longer the novel part. What survives is narrower and still real: the operating-point table with a
cost-ratio threshold and alert volume at deployment prevalence. If C3 is used, it must cite M1/M2/M11
instead of asserting an empty corpus — and it inherits a live competitor (M1) publishing exactly the
false-positive rate C3 would headline.

## 5. What this check licenses, and what it does not

**Licensed.** The introductions of both topics may write: "84 OpenAlex queries plus 91 arXiv queries
(documented here, with per-query counts) found no prior work that [the specific slice]", citing the
nearest neighbours by name in the same paragraph. They may not write "novel", "first", "no one has", or
"state of the art" (RULES.md 5).

**Not licensed.** (a) Any claim resting on Semantic Scholar — it returned zero results because it refused
the request, which is not the same as returning nothing. (b) Any claim about ACL-anthology papers absent
from OpenAlex titles/abstracts and from arXiv; coverage is uneven and this was a top-50 relevance pull per
query. (c) Any claim that the C1 vocabulary is unused outside this corpus. (d) The corpus-exclusivity claim
for C3, retired above.

**What would change the verdict.** For C1: a paper that (i) fits two thresholds on retrieval-side features
alone, (ii) evaluates per negative-hardness level, and (iii) reports a false-refusal or over-abstention
rate per level. N1 supplies (i) in another domain, N4 supplies the audit, nobody supplies (iii) per rung.
If such a paper appears, C1 is dead and the lab moves to C3 — that rule stands and is in
`orchestration/HEAD-REVIEW.md` condition 1.

## 6. Register and files

26 records from this session were resolved and appended to `02_literature/verified_citations.csv` by
`verify_citations.py add` (bibliographic fields from the resolving API, title-vs-record similarity ≥ 0.90,
command recorded per row). Reading reports: `02_literature/staging/S2b-reads/R1-C1.md` … `R6-C3.md`.
Query audit and per-query counts: §7 below; raw JSON per query in `02_literature/raw/openalex/`.

## 7. Appendix — all 84 OpenAlex queries with the count OpenAlex reported
