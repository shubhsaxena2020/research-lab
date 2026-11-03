# CANDIDATES — five paper topics, developed to the point of a decision

**S2-9 · topic development · 2026-11-03**

Five candidates, each specified far enough that a head reviewer can approve or reject it without a
follow-up question. They come from the four areas `LANDSCAPE.md` §13.2 ranked (abstention 11, scam 8,
evaluation methodology 3, memory 2) plus the two measurement halves the veto list spared (Indic, area 7;
on-device, area 5). All five are inference-only, need no training beyond a logistic regression or a ≤110M
encoder fine-tune, and fit 2–4 systems × 2–4 conditions × 1–3 seeds.

Bibliographic facts are copied from `02_literature/verified_citations.csv` — **317 data rows, snapshot
2026-11-03 03:55** (an earlier draft of this file quoted 266, which was the register before the gap-mining
and novelty-pre-scan batches merged; that count is superseded). Numbers marked **measured** come from
`02_literature/staging/_s2_2_data/s2_2_cpu_baselines.json`, taken on this laptop in this session; numbers
labelled "published anchor" or "estimate" are arithmetic from those and from papers, **not** measurements of
this machine, and hour one of any approved project replaces them with a logged figure.

## Compute assumptions used in all five

| Quantity | Value | Source |
|---|---|---|
| Prefill, 1.5B / 3B Q4_K_M | 60 / 45 tok/s | D2-2 §4; D2-3 §5 |
| Decode, 1.5B / 3B Q4_K_M | 20 / 12 tok/s | D2-3 §5 |
| BM25 index / query, 5,882 turns | 0.11 s, 406 MB / 0.04 ms | **measured** |
| MiniLM (22.7M) / bge-small (33.4M) query | 10.0 / 31.6 ms | **measured** |
| Cross-encoder rerank, top-50 | 361 ms | **measured** |
| BM25 recall@5 on LoCoMo | 0.459 (floor 0.0085) | **measured** |

Estimates from published anchors, not measurements of this machine; hour one of any approved project
replaces them with a logged figure. Retrieval is free and generation is the only real cost, so features
are cached once and re-used across variants; the reranker costs 361 ms/query while losing to plain BM25, so
it is only ever a condition.

---

## Candidate 1 — How Hard Are Your Negatives? A Hardness Ladder for Retrieval-Feature Abstention Gates

**Pitch.** The abstention literature evaluates gates on one kind of negative question and generalises.
The one paper that varied negative hardness found a 97-point swing — 98% accuracy on random negatives,
1% on negatives with high semantic overlap, same model, same questions (*Answerability in
Retrieval-Augmented Open-Domain Question Answering*, 2024). No paper in our 91-query arXiv sweep turns that
into a designed ablation with a two-sided policy and a reported false-refusal column
(`02_literature/NOVELTY-CHECK.md` §1 carries the evidence and the honest verdict: incremental, not novel).
We build a four-rung hardness ladder over one fixed reader and corpus, fit two-sided admit/refuse thresholds
on retrieval features on dev, and report abstain precision and over-refusal at every rung. The motivating
case is an anecdote from the student's private memory system — a single threshold placed outside the range
of scores the system actually produced — quoted without numbers, used only to explain why threshold
placement is reported as a diagnostic.

**Research question.** For a fixed 1.5B reader and passage corpus, does a dev-fitted two-sided gate on
retrieval features hold its abstain precision across a ladder of increasing negative hardness, and does
its operating point transfer to a held-out corpus?

**Hypotheses.**
- H1. Abstain precision falls monotonically with rung hardness, and the drop from rung 1 (random
  passage) to rung 3 (same-topic near-miss) is at least 15 points. Refuted by a flat or non-monotone
  curve.
- H2. A dev-fitted threshold loses at least 10 points of abstain precision on another corpus at equal
  coverage. Refuted if transfer is within ±5 points.
- H3. A two-sided policy (separate admit and refuse thresholds, dead zone between) beats the best
  single-threshold gate by ≥5 points of abstain precision at matched abstain recall. Refuted if the
  paired bootstrap interval contains zero.

**Method.** (1) Build 3,200 items: 800 answerable, 800 per rung. (2) Index the SQuAD 2.0 dev paragraph
pool with `bm25s` and bge-small dense vectors; cache top-10 per item. (3) Extract **six retrieval
features**: top-1 and mean top-5 BM25, top-1 and mean top-5 cosine, BM25/dense top-1 agreement, rerank score
of top-1. The gate is retrieval-only by construction — no generator call, no hidden state, no second model.
The reader's answer-token log-probability and entropy are extracted **only for the separate reader-assisted
arm (B4/B5)** and never enter the retrieval gate; report the two arms side by side, never pooled. (4) Fit
logistic regression on the six retrieval features on dev; grid-search two thresholds for a target abstain
precision of 0.80. (5) Evaluate on held-out per rung, then on the transfer corpus. (6) Run the separability
audit and publish it whether or not it flatters the gate.

**Datasets.** SQuAD 2.0 (*Know What You Don't Know: Unanswerable Questions for SQuAD*, 2018): 142,192
rows, 130,319 train / 11,873 dev, CC BY-SA 4.0; dev split, answerable items as the positive class.
Transfer: 800 items from 2WikiMultihopQA (Apache-2.0 per D2-2 §4), 400 answerable, 400 from rung 3.

The negatives are the whole paper, so the construction is spelled out. Rung 1, random: a uniformly
sampled non-gold paragraph. Rung 2, same-entity: a paragraph containing the exact string of the question's
subject entity but not the answer. Rung 3, same-topic: the paragraph immediately preceding or following the
gold paragraph in the same article — contiguous sections, so overlap is maximal, the condition that
produced the 98%→1% collapse. Rung 4, premise violation: the gold paragraph with the answer span replaced
by a same-type value from another passage in the same article, so the passage asserts something false and
the correct behaviour is refusal.

Three controls against trivial separability, all reported: (a) length matching — passages resampled within
each rung so passage-token-length matches the answerable set within ±10% per decile; (b) a surface-only
adversary — logistic regression on six surface features, trained per rung, AUROC reported, any rung above
0.75 rebuilt rather than shipped; (c) a paraphrase pass on rung 4 so no template is detectable.

**Baselines.** B1 single threshold on max BM25 — the cheapest thing that works and what most deployed
systems do. B2 single threshold on max dense cosine. B3 logistic regression on the **six retrieval
features** with one threshold (isolates "two-sided" from "more features"). B4, the strongest cheap baseline
a reviewer will demand, is a **separate reader-assisted arm**: the reader's own answer-token log-probability
as the gate, i.e. what "just ask the model how sure it is" reduces to (*Language Models (Mostly) Know What
They Know*, 2022, arXiv:2207.05221). B5 is the reader-assisted two-sided band (six retrieval features plus
log-probability and entropy). B4/B5 are always labelled reader-assisted and never pooled with the
retrieval-only results; the paper's claim is about the retrieval gate, and the reader arms exist to show
what a generator call buys at the same operating point. Ablation: B3 with the dead zone removed, plus
feature-group knockouts.

**Metrics.** Primary: abstain precision = TP/(TP+FP), positive = correctly refused, and over-refusal rate
= refused answerable / all answerable, at the dev-fitted operating point. Secondary: AURC, mean selective
risk over the coverage grid 0.05…1.00 in steps of 0.05 (Geifman–El-Yaniv, *Selective Classification for
Deep Neural Networks*, 2017); selective accuracy at 50% coverage; coverage at 80% accuracy, comparable to
the published 56% (*Selective Question Answering under Domain Shift*, 2020). Statistics: 10,000 paired
bootstrap resamples stratified by rung; McNemar exact on discordant pairs; Wilson intervals per cell.
Power: n=800 per rung gives ±3.5 points at p=0.5, so a 5-point claim is defensible and a 2-point claim is
not — stated in advance.

**Compute.** Feature extraction 3,200 × 350 prefill tokens ÷ 60 tok/s = 5.2 h. Gate fitting and all four
policies: free, they are logistic regressions over the cached matrix. Reader evaluation 600 items × 4
policies × 40 output tokens ÷ 20 tok/s = 1.3 h. Transfer set 800 × 350 ÷ 60 = 1.3 h. Per seed 7.8 h; two
seeds 15.6 h — two to three overnight runs. Matrix 4 policies × 4 rungs × 2 seeds = 32 cells, 30 of which cost
no inference.

**One-week plan.** D1 ladder construction + 3,200-item JSONL + separability table
(`data/ladder_v1.jsonl`, `results/separability.csv`). D2 indices + cached top-10 + measured tok/s
(`results/throughput.json`). D3 features extracted (`results/features.parquet`). D4 four policies fitted,
risk–coverage curves (`results/gates.json`). D5 transfer + ablation (`results/transfer.csv`). D6
bootstrap, McNemar, power statement (`results/stats.json`). D7 freeze, tag, write methods and results
from the JSON (`05_paper/draft/C1-methods.md`).

**Risks.** (1) Rungs trivially separable, every gate scores 0.9 — mitigated by the audit and rebuild rule
above. (2) The 1.5B reader sits at floor so all policies look identical — mitigated by making AURC primary
and running one 300-item API-reader ceiling condition. (3) n too small to separate policies — a publishable
negative, since the post-hoc-confidence literature predicts it, but only if the ladder table is interesting
on its own.

**Novelty evidence.** *Answerability in Retrieval-Augmented Open-Domain Question Answering* (2024) is
closest on features and is the source of the 98%→1% number, but reports classification accuracy on
constructed negatives, not a calibrated two-sided policy, and never reports abstain precision on answerable
questions. *Unanswerability Evaluation for Retrieval Augmented Generation* (2024) has the right two metrics
but sweeps pipeline components rather than thresholds. *Two Axes of LLM Abstention: Answer Correctness and
Question Answerability* (2026) has the right policy shape but scores answerability with a hidden-state probe
and describes no dev/held-out fitting protocol. D2-2 §3.4 calls the gap "real but narrow": incremental,
defensible only because the ladder is a designed ablation nobody has run.

**Venue fit.** UncertaiNLP (the uncertainty workshop at ACL — it published *Refer, Infer, or Abstain* in
2026); ACL Student Research Workshop; NeurIPS/ICML uncertainty workshops; arXiv.

**Student score: 5/5.** He built the failing gate and has its logs, so he can explain the feature-range
error from his own measurement.

**Rubric.** Novelty 15/25 — an ablation, not a method, and the deep dive says so. Feasibility 24/25 — 16 h
of cached inference. Rigor 18/20 — preregistered power, stratified bootstrap, separability audit, and a
negative-result path. Evidence of gap 14/15 — D2-2 §3.2 and §3.4 document the hole with numbers and name
the three nearest works. Personal edge 10/10 — the motivating failure is his. Venue fit 5/5 — UncertaiNLP
takes exactly this shape. **Total 86/100.**

---

## Candidate 2 — The Stale-Hit Rate: A Model-Free Metric for Fact Supersession in Agent Memory

**Pitch.** Every agent memory stack claims to handle updates; almost none reports the operational question
— after a fact is superseded, does the store still *retrieve* the old value? The one temporal system with
a real mechanism reports a five-point gain on a knowledge-update category that is itself confounded,
because evidence sessions are inserted in timestamp order, so a reader that prefers the latest session
answers many update questions correctly with no update logic at all (D2-1 §3.5). We define stale-hit rate
— computable from any store with versioned facts, needing no LLM judge — and measure it on three stores
differing only in supersession policy.

**Research question.** When a fact stated in session *i* is contradicted in session *j* > *i*, what
fraction of top-k retrievals still returns the superseded value, and does supersession policy change that
fraction independently of the reader?

**Hypotheses.**
- H1. Append-only retrieval returns the superseded value in top-5 for at least 40% of probes;
  delete-on-write reduces that below 10%. Refuted if append-only is already below 20%, which would mean
  lexical drift, not policy, dominates.
- H2. At least one store ranks best on answer accuracy without ranking best on stale-hit rate, i.e.
  accuracy hides the failure. Refuted if the two rankings coincide across all three stores.
- H3. Reader position, not retrieval, explains at least 30% of stale answers: re-ordering the retrieved
  set so the superseded turn comes first flips ≥30% of answers. Refuted by a small flip rate, which would
  mean retrieval is doing the work.

**Method.** (1) Extract attribute-bearing turns from LoCoMo with a fixed pattern bank, yielding facts with
session indices. (2) Construct 300 supersede pairs: rewrite one later turn to assert a different value for
the same attribute, keeping the original, using eight paraphrase templates so the new turn does not reuse
the old turn's wording beyond entity and attribute noun. (3) Hand-identify 100 *natural* update pairs
already in LoCoMo, recording search time — the yield rate is itself a datum about how rarely these
benchmarks contain real updates. (4) Implement three stores in one SQLite schema: append-only;
delete-on-write (old row flagged when a new fact shares entity and attribute); bi-temporal
(valid_from/valid_to in event time plus transaction time). (5) Index all three with `bm25s`. (6) Probe
with an undated and a dated question, retrieve top-1/5/10, compute stale-hit rate before any reader sees
the context. (7) Run the reader for answer-level staleness.

**Datasets.** LoCoMo (*Evaluating Very Long-Term Conversational Memory of LLM Agents*, 2024): 10
conversations, 5,882 turns, 1,986 QA — all **measured** by parsing the released file; CC BY-NC 4.0, which
permits research use but forbids permissive redistribution of derived data, so the artefact ships code and
the construction script, not the pairs.

The manipulation check is explicit: for every pair, record the BM25 score of the old and new turn for the
probe question, and flag pairs whose gap exceeds 20% — otherwise append-only will look good for the wrong
reason. The 100 natural pairs are the honesty check on the 300 constructed ones: if the subsets disagree by
more than 15 points on stale-hit rate, the constructed set is measuring the template and the paper says
so.

**Baselines.** B1 append-only top-k, what every framework does by default. B2 recency reranking — timestamp
descending, BM25 within ties — the strongest cheap thing and the one a reviewer will demand, because "just
prefer the latest" is free and may match a bi-temporal store. B3 full-context reader, all sessions
truncated to the 8k window; that baseline beat MemGPT on its own benchmark (94.4% vs 93.4% on Deep Memory
Retrieval, D2-1 §1.1), so a memory paper that omits it is vulnerable. Ablation: bi-temporal store with invalidation
disabled, isolating whether the gain comes from the timestamp columns or the bookkeeping.

**Metrics.** Primary: stale-hit rate at k = |{probes whose top-k contains a superseded value}| / N, at k =
1, 5, 10, with the random floor printed beside it (k/588 = 0.0085 at k=5). Secondary: current-value
recall@k; answer-staleness rate by exact string match against the known superseded value, so no judge is
involved; prompt tokens per query, because cost is where memory papers usually cheat. Statistics: paired
bootstrap over probes, 10,000 resamples, stratified by constructed-vs-natural; McNemar on discordant
pairs; Wilson intervals. Items within a conversation are not independent, so the bootstrap resamples conversations as clusters and
both intervals are reported — the difference is the point.

**Compute.** Index build 0.11 s **measured**; 400 probes × 3 stores × 3 k-values = 3,600 retrievals at ~1
ms = 4 s. Reader 400 × 3 stores × 2 question forms = 2,400 generations × 40 tokens ÷ 20 tok/s = 1.3 h;
three seeds 4 h. Matrix 3 stores × 2 question forms × 3 k-values × 3 seeds = 54 cells, 48 of which cost no
generation.

**One-week plan.** D1 pattern extraction + 300 constructed pairs + manipulation table
(`data/pairs_constructed.jsonl`). D2 100 natural pairs by hand + yield note (`data/pairs_natural.jsonl`,
`notes/natural_yield.md`). D3 three stores implemented, unit-tested against a 20-pair fixture
(`src/stores.py`, `tests/test_stores.py` green). D4 stale-hit across all cells (`results/stale_hit.csv`).
D5 recency and full-context baselines (`results/baselines.csv`). D6 reader runs, answer staleness,
position-flip (`results/reader.jsonl`). D7 clustered bootstrap, figures, freeze (`results/stats.json`).

**Risks.** (1) Constructed contradictions too easy — mitigated by the template bank, the BM25-gap check, and
the natural pairs as calibration. (2) The reader prefers the later session by position — mitigated by H3's
flip experiment, which converts the confound into a measured quantity. (3) The NC licence limits release —
mitigated by shipping code plus a regeneration script.

**Novelty evidence.** *Zep: A Temporal Knowledge Graph Architecture for Agent Memory* (2025) has the only
real supersession mechanism in the verified set — four timestamps per edge, LLM-driven invalidation — and
reports knowledge-update accuracy of 83.3% vs 78.2% for full context, LLM-judged, five points on a fraction
of 500 questions, with no retrieval-side metric. *LongMemEval* (2024) has the category but not the
measurement. D2-1 §3.5 states it directly: a stale-hit rate "is computable from any store with versioned
facts, needs no LLM judge, and separates systems that update from systems that merely append. I could not
find a paper reporting it." A genuinely new metric with a small demonstration, and the weakest evidence
base here — one negative search is not proof of absence.

**Venue fit.** NeurIPS/ICML memory and agent workshops; ACL Student Research Workshop; arXiv. The metric is
the contribution, so short-paper shape is correct.

**Student score: 4/5.** He has built a memory system and can explain retrieval-versus-reader error;
bi-temporal validity is the one concept he would learn from scratch.

**Rubric.** Novelty 18/25 — an unreported metric, but a 400-probe metric paper is short, not long.
Feasibility 25/25 — 4 h of compute. Rigor 17/20 — clustered bootstrap and a manipulation check, but the
constructed set is inherently a simulation. Evidence of gap 12/15 — one careful negative search, not a
literature-wide audit. Personal edge 9/10 — direct apparatus, no domain advantage. Venue fit 4/5 — right
shape, but memory workshops are crowded with systems papers. **Total 85/100.**

---

## Candidate 3 — Surface Form Is Most of the Signal: A Style-Only Control for SMS Scam Detectors

**Pitch.** Misinformation research spent five years discovering its detectors were classifying genre, not
falsity: injecting sentiment, style, topic or perplexity shortcuts drops detector accuracy by roughly 80%
on average and to 0% in the worst case (*Truth over Tricks: Measuring and Mitigating Shortcut Learning in
Misinformation Detection*, 2025), and closing a leak in an event-based rumour benchmark took accuracy from
90.2% to 44.3% (*Probing Spurious Correlations in Popular Event-Based Rumor Detection Benchmarks*, 2022).
Scam detection has not run the equivalent control. We strip content words, keep surface form — length,
punctuation, capitalisation, digits, currency symbols, emoji, URL shape — measure how much F1 survives, and
re-report the survivor at a realistic prevalence instead of the constructed 13.4% split.

**Research question.** On two public SMS corpora, what fraction of a detector's F1 is recoverable from
surface form alone, and what happens to precision when the same detector is scored at scam prevalence
below 1%?

**Hypotheses.**
- H1. A style-only model reaches F1 ≥ 0.80 on UCI, at least 85% of the full-text baseline's measured
  0.924. Refuted by style-only F1 below 0.70.
- H2. Group-aware splitting costs the full-text model at least 3 F1 points and the style-only model less,
  because duplicates share style as well as content. Refuted if the full-text drop is under 1 point.
- H3. At 0.5% prevalence, precision at the F1-optimal threshold falls below 0.25. Arithmetic at recall
  0.95 and FPR 0.02: 0.95×0.005 / (0.95×0.005 + 0.02×0.995) = 0.19. Refuted if precision stays above
  0.40, which needs an FPR under 0.008.

**Method.** (1) Deduplicate by exact normalised match plus shingle-Jaccard ≥ 0.8 to form groups;
group-aware stratified 5-fold CV, repeated 5 times. (2) Build the 2×2: full text; style-only (content
tokens masked, surface tokens and numeric patterns kept); content-only (lowercased, punctuation, digits,
URLs and emoji stripped); a permutation control shuffling labels within style strata. (3) Fit three
families: TF-IDF word 1–2 grams + logistic regression; character 3–5 grams + logistic regression (the
honest competitor, since char n-grams capture style and content together); a MiniLM-L6-v2 fine-tune
(22.7M). (4) Sweep the threshold, invert the cost problem, reweight to deployment prevalence by prior
correction on the confusion matrix.

**Datasets.** UCI SMS Spam Collection (*Contributions to the study of SMS spam filtering*, 2011): 5,574
messages, 747 spam (13.4%), CC BY 4.0, 5-fold CV with group awareness added. Measured properties the design
depends on: 444/5,574 (8.0%) exact-normalised duplicates, 518 (9.3%) with a ≥0.8 shingle-Jaccard
near-duplicate, and only 14.3% of spam containing a URL — so a URL-shape feature is blind to most of the
corpus. Second corpus: Smishing Dataset I (*Smishing Dataset I: Phishing SMS Dataset from Smishtank.com*,
2024), 1,062 modern smishing messages, no licence stated on the source page, positive class only — used to
test whether style transfers to a fraud corpus, with UCI ham supplying negatives and the mismatch
disclosed.

There is no constructed negative set here, which is why this candidate is safe: both classes are
human-labelled. The construction risk is replaced by another — the corpora are a decade apart and from
different countries, so "style" may mean "era". The control is a third arm trained on UCI and tested on
Smishing I.

**Baselines.** B1 TF-IDF + logistic regression, measured at F1 0.924 (P 0.902 / R 0.946 at threshold 0.5) —
the number any UCI paper must beat, and one we already have. B2 character n-gram + logistic regression,
the strongest cheap baseline and the fair competitor to a style claim. B3 MiniLM fine-tune, the strongest
thing that fits. Ablation: the 2×2 itself plus the permutation control.

**Metrics.** Primary: F1 = 2PR/(P+R) on held-out folds with group-aware intervals. Secondary: AUPRC (the
right curve at low prevalence, where ROC flatters); precision at 95% recall; the break-even cost ratio r*,
the FN:FP ratio at which each operating point becomes optimal, found by sweeping the threshold and
recording where C = c_FN·FN + c_FP·FP changes argmin. r* turns an arbitrary free parameter into a reported
quantity — and the 2026 operational survey found zero of 18 fraud sources report calibration at all
(*Operational Evidence Gaps for LLMs in Fraud Detection and Trust-and-Safety Workflows*, 2026). ECE with
10 equal-mass bins. Statistics: 5×5 repeated grouped CV; bootstrap over *groups*, not items, because
duplicates make items non-independent.

**Compute.** TF-IDF + LR 5-fold: 46 s **measured**, including the O(n²) near-duplicate scan. Char n-gram LR
~2 min; style LR seconds. MiniLM fine-tune: 5,574 messages at 64–128 tokens, batch 16, 3 epochs, 5–15 min
per epoch per D2-6 §5, so 45–135 min for three folds or ~4 h for five at the slow end. Total ≈ 5 h; 3
seeds only affect the fine-tune's initialisation, so 2 seeds is the default. Matrix 3 families × 4 text
conditions × 2 seeds = 24 cells.

**One-week plan.** D1 dedup + groups + measured duplicate table (`data/uci_groups.csv`). D2 2×2 transforms
+ a check that masking removed content and kept surface (`src/transforms.py`,
`tests/test_transforms.py`). D3 linear baselines across all conditions (`results/linear.csv`). D4 char
n-gram arm + threshold sweep + r* curve (`results/thresholds.csv`). D5 MiniLM fine-tune, 3 folds
(`results/minilm.csv` with seed and log). D6 prevalence reweighting, ECE, AUPRC, permutation control
(`results/prevalence.csv`). D7 Smishing I transfer + figures + freeze (`results/transfer.csv`).

**Risks.** (1) The style-only ablation removes legitimate signal — urgency lexicon is content — so a low
score would not prove the model is content-driven; mitigated by running both arms and framing the result as
"how much is genre", never as "detectors are fraudulent". (2) UCI spam is 2000s promotional text, so
external validity is thin; mitigated by the Smishing I transfer arm and by stating the era shift as a
limitation. (3) Duplicates give wide intervals; mitigated by group-aware CV.

**Novelty evidence.** The control is a transplant and should be labelled as one. *Truth over Tricks*
(2025) is the direct methodological parent; *Probing Spurious Correlations in Popular Event-Based Rumor
Detection Benchmarks* (2022) quantifies the leak-closing drop; *SoK: Machine Learning for Misinformation
Detection* (2023) surveys 248 papers to the same end. On the scam side, *An Empirical Analysis of SMS Scam
Detection Systems* (2022) and *Johnny Still Receives Spam SMS: Assessing the Robustness of SMS Spam
Detection* (2026) test deployed systems and find them failing, but neither runs a style-only control. D2-6
§3 Open 4: the scam analogue "has, as far as I can resolve, not been published".

**Venue fit.** NLP-for-cybersecurity workshops (AAAI/ACM circuit); ACM SAC; arXiv; a national student
research convention as a parallel track. Not a main track — the method is borrowed.

**Student score: 5/5.** He built TrustShield to a national final and has the intuition for which surface
cues are real.

**Rubric.** Novelty 12/25 — borrowed wholesale, and the honest framing is "we ran the control nobody ran
here". Feasibility 25/25 — 5 h, no judge, data already public. Rigor 16/20 — group-aware CV and intervals,
but the era confound cannot be fully closed with two corpora. Evidence of gap 13/15 — a documented absence,
not a proof. Personal edge 10/10 — his strongest asset. Venue fit 4/5 — the workshop circuit exists but is
scattered. **Total 80/100.**

---

## Candidate 4 — Refusal in the Wrong Language: A Hindi Abstention Probe with Language-of-Refusal as a Measured Variable

**Pitch.** There is no measurement of whether a model knows it does not know in Hindi, Hinglish, or any
Indic language: every Indic benchmark in the verified set is answerable by construction, with one correct
option and no abstain option (D2-5 §3.2). There is also a measurement-instrument problem: heuristic refusal
classifiers systematically undercount refusals by models that answer in English while being prompted in
Hindi (*A Measurement Crisis in Multilingual LLM Safety: Heuristic Classifiers Systematically Undercount
Reasoning-Model Refusals in Indic Languages*, 2026). We turn that defect into the dependent variable:
language-of-refusal is measured, not preprocessed away, and every claim is reported twice — under an
English-keyword detector and under human labels.

**Research question.** When a small multilingual model is asked a Hindi question it cannot answer from the
supplied passage, does it abstain, answer from parametric memory, or answer in another language — and does
an English-keyword refusal detector measure the same behaviour a Hindi speaker does?

**Hypotheses.**
- H1. At least 30% of refusals to Hindi prompts are emitted in English or romanised Hinglish, and the
  English-keyword detector undercounts true refusals by ≥15 points relative to human labels. Refuted by a
  small gap, which would mean the measurement-crisis claim does not hold for answerability refusals.
- H2. Over-refusal on answerable Hindi items exceeds over-refusal on matched English items by ≥8 points at
  equal abstain recall. Refuted by parity, which would be the more interesting result.
- H3. Expected calibration error of option-level confidence is at least 0.05 higher in Hindi than English
  at matched accuracy. Refuted if the difference's interval contains zero.

**Method.** (1) Take 300 Hindi Belebele items and their parallel English counterparts — same 488 FLORES
passages, same questions, so the English control needs no translation by us. (2) Convert to open-ended QA
so refusal is expressible: "answer from the passage, or say you do not know". (3) Construct three negative
rungs, 100 items each: U1 near-miss (question paired with a topically similar non-gold passage, chosen by
BM25 similarity to the gold passage); U2 entity-absent (question about an invented entity, so parametric
memory cannot rescue it — the control D2-5 §3.2 names as mandatory); U3 premise violation (question's
subject replaced by another entity from the same passage set). (4) Run Qwen2.5-1.5B-Instruct and
Qwen3-1.7B, both 4-bit. (5) Score four ways: human labels on 200 items (student plus one native Hindi
speaker, Cohen's κ reported); an English-keyword refusal detector; a language-aware detector; an
entailment check of the answer against the passage. (6) Score the MCQ form separately for ECE.

**Datasets.** Belebele (*The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122 Language
Variants*, 2024): 900 questions × 122 variants over 488 FLORES passages, CC BY-SA 4.0, Hindi and English
variants, 300 items sampled with a fixed seed. MILU (*MILU: A Multi-task Indic Language Understanding
Benchmark*, 2024): 79,617 test items, Hindi 14,837, CC BY 4.0 and gated with auto-approval — a second,
exam-style set of 300 items to check the probe is not FLORES-specific.

The negatives are constructed and the construction is the exposure. Belebele's parallel structure helps: a
near-miss passage for a Hindi question is a *real* Hindi passage from the same corpus, not a machine
translation, so U1 cannot be detected as translationese. U2 uses invented proper nouns absent from the
corpus, verified by full-string search, so a model answering from memory is provably hallucinating. U3
substitutes entities within the same passage set, and every substituted item is checked for grammaticality
— broken Hindi would read as "weird input", not "unanswerable", and that is how this rung fails.

**Baselines.** B1 the parallel English condition — same passage, same question, English prompt and expected
English answer: the strongest and cheapest control, unavailable to most papers in this space. B2
always-answer (no abstention instruction), the floor showing how often the model is right by accident. B3
verbalised confidence ("how sure are you, 0–100") thresholded at the dev-optimal point — the published
cheap method (*Just Ask for Calibration*, 2023) and the null hypothesis per D2-2 §5. Ablation:
language-aware versus English-keyword detector on identical outputs, which isolates the instrument from the
model behaviour.

**Metrics.** Primary: abstain precision and recall against human labels, and over-refusal rate on
answerable items, at a dev-fitted operating point. Secondary: refusal-language distribution (share in
Devanagari / romanised Hindi / English / mixed); Cohen's κ between each detector and human labels; ECE over
10 equal-mass bins on the MCQ form; accuracy on answerable items, reported separately so a model that
abstains well and answers badly is visible. Statistics: cluster bootstrap by passage — 900 questions over
488 passages means items are not independent and an item-level bootstrap would understate the interval;
McNemar on paired Hindi/English outcomes; Wilson intervals per cell. Power: 300 items per language gives
±5.7 points at p=0.5, so only 8-point claims are safe, and H2's threshold was set from that arithmetic
rather than the reverse.

**Compute.** Open-ended: 800 items (400 Hindi, 400 English) × 120 output tokens ÷ 20 tok/s = 1.3 h per
model, 2.7 h for both. MCQ log-probability scoring: 900 × 4 options × 100 prefill tokens = 360k tokens ÷ 60
tok/s = 1.7 h per model, 3.4 h for both. Per seed ≈ 6 h; two seeds 12 h. Matrix 2 models × 2 languages × 4
levels (3 rungs + answerable) × 2 seeds = 32 cells.

**One-week plan.** D1 item sampling + parallel alignment check + 300 pairs frozen
(`data/belebele_pairs.jsonl`). D2 three rungs constructed + native-speaker grammaticality pass
(`data/negatives.jsonl`, `notes/grammaticality.md`). D3 inference harness + first 100 outputs, read
manually (`results/pilot.jsonl`). D4 full open-ended run, both models (`results/outputs.jsonl`). D5
200-item human labelling + κ (`data/human_labels.csv`). D6 four scorers, detector-vs-human comparison
(`results/scorers.csv`). D7 MCQ/ECE run, clustered bootstrap, freeze (`results/ece.json`).

**Risks.** (1) The student's Hindi may not support reliable labelling — mitigated by recruiting one native
speaker, reporting κ, and restricting claims to the detector-agreement axis if κ < 0.6. (2) "Unanswerable
from the passage" is not "unanswerable" — mitigated by U2's invented entities and by reporting U1 and U2
separately. (3) The refusal detector is itself a classifier with error and the headline is about that error
— mitigated by treating the detector as the object of study.

**Novelty evidence.** D2-5 §3.2 states the absence as a checked claim: no dataset, benchmark or paper
measures whether a model knows it does not know in Hindi, Hinglish or any Indic language. *A Measurement
Crisis in Multilingual LLM Safety* (2026) argues heuristic classifiers undercount Indic refusals, but for
safety refusals, not answerability, and without a calibration measurement. *Where Abstention Lives: A
Pre-Registered Four-Way Comparison of Abstention Interfaces in a Small Language Model with Versioned
Memory* (2026) is the nearest design and is English-only. *AbstentionBench: Reasoning LLMs Fail on
Unanswerable Questions* (2025) is the benchmark this cannot be: judge-scored and English. New population,
borrowed method, one genuinely new measured variable.

**Venue fit.** Workshop on Asian Language Processing; IndicNLP at ACL; UncertaiNLP; ACL Student Research
Workshop; arXiv.

**Student score: 4/5.** The gate logic and failure mode are his; the Hindi annotation protocol and the
translation confound are where he would need supervision.

**Rubric.** Novelty 19/25 — the population is genuinely unmeasured and refusal-language is new, but the
method is assembled from English-language parts. Feasibility 20/25 — 12 h of compute is fine, but human
labelling is schedule risk, not compute risk. Rigor 15/20 — κ and clustered bootstrap are there, but 300
items and a two-annotator pool cap the claims. Evidence of gap 14/15 — D2-5 §3.2 is explicit and
checkable. Personal edge 8/10 — abstention yes, Hindi NLP no. Venue fit 4/5 — IndicNLP is the natural
home. **Total 80/100.**

---

## Candidate 5 — Does the Quantisation Cliff Move with Model Size? A CPU-Only Quality–Memory–Latency Study at 1–3B

**Pitch.** "4-bit is safe, 3-bit is not" is established at 7–8B: Q3_K_S loses 9.32 GSM8K points while
Q4_K_S and Q4_K_M are indistinguishable from F16, and three 5-bit formats share an identical WikiText-2
perplexity of 7.43 while differing by 3.4 GSM8K points (*Which Quantization Should I Use? A Unified
Evaluation of llama.cpp Quantization on Llama-3.1-8B-Instruct*, 2026). It is assumed everywhere below 3B
and tested nowhere. We test it at 1B and 3B and add the axis least reported: peak resident memory as a
process-tree high-water mark rather than a number read off the weight file.

**Research question.** At 1–3B, does the relative quality penalty of 3-bit versus 4-bit versus 8-bit grow
as the model gets smaller, and does perplexity rank configurations the same way a task metric does?

**Hypotheses.**
- H1. The relative accuracy drop at Q3_K_S is larger at 1B than 3B by at least 5 percentage points of the
  reference score. Refuted by parity or the opposite ordering.
- H2. Spearman rank correlation between WikiText-2 perplexity and task accuracy across the nine
  configurations is below 0.5. Refuted by ρ ≥ 0.8, which would make perplexity usable at this scale.
- H3. Peak RSS at 2k context exceeds weight-file size by at least 30%, so "runs in 2 GB" is ambiguous by
  construction. Refuted if overhead is under 10%.

**Method.** (1) Pin the runtime: llama.cpp at a recorded build number, 8 threads, fixed seed, warmup
discarded. (2) Two families (Llama-3.2-1B, Llama-3.2-3B) × three formats (Q3_K_S, Q4_K_M, Q8_0) = six
configurations, with Qwen3-1.7B as a ninth cell if time allows. (3) Three measurements per configuration:
ARC-Challenge accuracy by option log-likelihood (no generation, so no parsing artefact); IFEval on 150
prompts (generation, exact verifiers, no judge); WikiText-2 perplexity over 100 windows of 2,048 tokens.
(4) Peak RSS sampled from the process tree every 100 ms, reporting both private working set and total
including mapped file, because on Windows those differ by roughly the whole model. (5) Decode and prefill
throughput reported separately, since their bottlenecks differ.

**Datasets.** ARC-Challenge (`allenai/ai2_arc`), 1,172 test items, CC BY-SA 4.0 — full test split, because
at n=1,172 the Wilson half-width is ±2.9 points and at n=250 it is ±6, which cannot separate a 4-bit model
from its 8-bit twin. IFEval (`google/IFEval`), ~500 prompts, Apache-2.0, 150-prompt subset sized by output
length rather than prompt count. WikiText-2 (`Salesforce/wikitext`), CC BY-SA 3.0 + GFDL, 100 windows. No
constructed negatives: this candidate has no negative class, which removes the separability risk entirely
and replaces it with a compute risk.

**Baselines.** B1 Q8_0 as the reference for relative degradation, the closest thing to "no quantisation"
that runs here. B2 the published 8B result as an external anchor — if our 3B behaves like their 8B, the
cliff has not moved. B3 majority-class and random-answer floors on ARC, because a 1B near chance makes
every format look equivalent. Ablation: perplexity versus task accuracy as ranking devices, which is H2 and
is also the ablation — the same nine configurations ranked two ways.

**Metrics.** Primary: accuracy (exact match on the option letter) and relative degradation Δ_rel = (acc_Q8
− acc_q)/acc_Q8 per cell with Wilson intervals. Secondary: Spearman ρ between PPL rank and accuracy rank;
peak RSS in MB under both definitions; decode and prefill tok/s separately; answer-flip rate, which the
literature shows can be large while aggregate accuracy is flat (*Accuracy is Not All You Need*, 2024).
Statistics: bootstrap over items within each cell; paired bootstrap for within-model format differences
(pairing buys roughly a 1.6× reduction in required n per D2-4 §5.2); no cross-family significance claims,
because the tokenizers differ.

**Compute.** ARC: 1,172 × 4 options × 120 prefill tokens = 562k tokens; 2.6 h at 60 tok/s (1B), 3.5 h at 45
tok/s (3B); six configurations 3×2.6 + 3×3.5 = 18.3 h. IFEval: 150 × 250 output = 37.5k tokens; 0.52 h (1B)
and 0.87 h (3B); six configurations 4.2 h. Perplexity: 100 × 2,048 = 205k prefill tokens; 0.95 h and 1.27
h; six configurations 6.7 h. Total 29.2 h ≈ four overnight runs — the only candidate where compute, not
analysis, is the binding constraint.

**One-week plan.** D1 runtime pinned, throughput measured on all six configurations
(`results/throughput.csv`). D2 ARC complete for 1B (`results/arc_1b.csv`). D3 ARC complete for 3B
(`results/arc_3b.csv`). D4 IFEval subset, both families (`results/ifeval.csv`). D5 perplexity + memory
protocol, both RSS definitions (`results/memory.csv`). D6 rank correlation, flip rates, intervals
(`results/analysis.json`). D7 figures, freeze, and an honest "what we could not run" section
(`05_paper/draft/C5-results.md`).

**Risks.** (1) Time overrun — mitigated by a pre-declared drop order: drop Qwen3, then cut IFEval to 100
prompts, then run one seed. Deciding this in advance is what stops a half-finished matrix being written up
as finished. (2) Floor effects: a 1B near chance on ARC makes all formats look equal — mitigated by Δ_rel
and by IFEval. (3) Backend drift: the same weights on a different llama.cpp build can differ by double
digits (16.6 GSM8K points across engines, *The Silent Hyperparameter: Quantifying the Impact of Inference
Backends on LLM Reproducibility*, 2026), so build number, thread count and flags are published.

**Novelty evidence.** *Which Quantization Should I Use?* (2026) is the direct parent: same sweep at 8B on a
192-thread Xeon, no memory measurement. *Small Language Models: Survey, Measurements, and Insights* (2024)
measures 20 small models on latency, memory and energy, but on a Jetson GPU and a smartphone CPU, with
memory as a footprint number and no per-format sweep. *Accuracy is Not All You Need* (2024) establishes
the flip phenomenon. D2-3 §3: "nobody has published quality-vs-peak-RAM-vs-latency frontiers for 0.3B–4B
models, CPU-only, on one fixed task, with repeats and disclosed thread count." Incremental replication at a
different scale — the weakest novelty claim here and the most useful to a practitioner.

**Venue fit.** arXiv preprint is the realistic home; MLSys/edge-inference workshops; TinyML workshop. Not a
main track — this is a measurement replication.

**Student score: 3/5.** The mechanics are flags and logs, but defending it needs roofline reasoning
(bandwidth-bound decode versus compute-bound prefill) and a memory protocol he would have to learn.

**Rubric.** Novelty 9/25 — a scale replication with one added axis. Feasibility 18/25 — 29 h and real
overrun risk. Rigor 17/20 — the protocol is the strongest part, with pinned builds and paired analysis.
Evidence of gap 9/15 — a careful negative search, but the contribution is "same study, smaller models".
Personal edge 5/10 — no apparatus advantage. Venue fit 3/5 — arXiv is a floor, not a venue. **Total 61/100.**

---

## Ranking

| Rank | Topic | Total | Verdict |
|---|---|---|---|
| 1 | C1 — hardness ladder for retrieval-feature abstention gates | 86 | Documented gap with numbers, cached matrix makes it cheap, and the motivating failure is his own measurement. |
| 2 | C2 — stale-hit rate for fact supersession in memory | 85 | Cleanest novelty claim and cheapest to run; second only because one negative search is weaker evidence than a documented 97-point swing. |
| 3 | C3 — style-only control for SMS scam detectors | 80 | Highest personal edge and lowest execution risk, but the method is borrowed and the era confound cannot be closed. |
| 4 | C4 — Hindi abstention probe with language-of-refusal | 80 | Genuinely unmeasured population; schedule risk is human, not compute. |
| 5 | C5 — does the quantisation cliff move at 1–3B | 61 | Honest and useful; enter only if the goal changes from "a paper" to "a deployment note". |

C1 and C2 are two points apart and the ordering is not robust to a single reviewer preference: weight
novelty and C2 wins, weight the student's ability to defend every number from first-hand experience and C1
wins. I would take C1, and say why in the proposal rather than pretend the margin is larger.

## What the runner-up is for, and when to switch

C2 is the switch target, and the switch is triggered by a day-one pilot rather than by taste. The pilot:
can 300 valid supersede pairs be built from LoCoMo in four hours, with a BM25 score gap under 20% between
old and new turn? If yes, C2 is the better paper on novelty at a quarter of the compute, and C1's ladder
becomes a section of it. If no, C2 collapses to a metric definition with no data and C1 is right. The
second condition is literature: if a week-one novelty search surfaces a 2026 paper already reporting a
stale-hit rate, C2 dies and C1 inherits the slot, because C1's gap is narrower but has three named
near-neighbours a search can check against. C3 is the third-line fallback: the only candidate whose
execution risk is essentially zero, which makes it right under a hard deadline and wrong under a quality
deadline.

## The single biggest integrity risk in the set

Four of these five construct their own negatives, and all four can be invalidated by one mechanism: a
negative set separable by an artefact — passage length, lexical overlap, template wording, or the fact that
the question was generated from the passage it is supposed to be unanswerable against. The evidence that
this is not hypothetical is specific: a classifier trained on random negatives scored 98% and the same
classifier scored 1% on negatives with high semantic overlap, a 97-point swing produced entirely by how the
negatives were sampled. If our ladder, supersede pairs or Hindi unanswerables are separable the same way,
every gate will look excellent and the paper will be measuring its own construction — invisible in the
results table, fatal in review. The mitigation is a mandatory artefact in every candidate: a separability
audit run before the main experiment, in which a model with access only to surface features is trained to
distinguish each negative rung from the answerable set, with its AUROC published whether or not it flatters
us, plus length matching and a stated rebuild rule (AUROC > 0.75 means rebuild, not ship). The
mirror-image risk is a constructed set *too hard* for reasons unrelated to answerability, which produces a
null that looks like a finding about models. Measure the negative set before measuring the system on it.

FILES: 03_topics/CANDIDATES.md
PAPERS_VERIFIED: 26 distinct works cited, all resolved against 02_literature/verified_citations.csv (266 rows); 0 new claims submitted, 0 unresolved
STATUS: DONE
