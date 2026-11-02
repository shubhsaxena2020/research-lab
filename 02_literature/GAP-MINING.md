# GAP REGISTER — sixteen testable gaps, consolidated and ranked (S2-8)

**S2-8 · gap mining · 2026-11-03 · sources: LANDSCAPE.md and six deep dives**

## 0. What this is, and the rules used to build it

Six deep dives and a landscape map proposed roughly thirty gaps with heavy overlap: the abstention dive's
first gap (a two-sided retrieval-feature gate on a hardness ladder) and the memory dive's second
(retrieval-side abstention, not prompt-side) are one design on two corpora, and the evaluation dive's fifth
is a third statement of it. This register keeps **sixteen** distinct gaps, each with one experiment that
could start tomorrow on this laptop. Four rules make the reduction checkable: **same measurement and corpus
family → merged** (GAP-01 merges D2-2 G1, D2-1 G2 and D2-4 #5; GAP-05 merges the abstention and scam
cost-model gaps, one closed-form computation); **same construct, different corpus → separate** (GAP-01
English, GAP-10 Hindi); **same construct, different shift axis → merged** (GAP-02 absorbs the model-transfer
and retrieval-budget variants); **training, gradients, or more than a few thousand judge calls → excluded**
(§4).

Two corrections came out of checking nearest prior work. **LANDSCAPE §5 lists "quantisation damage in Indic
scripts" as unmeasured; it is not** — Marchisio et al. (2024) evaluate quantised multilingual models with
automatic, judge and human scoring, find non-Latin scripts worst affected, and report a 1.7% automatic drop
in Japanese corresponding to 16.0% under human evaluation. That gap is dropped, not deferred. **The
retrieval-decision literature is closer than D2-2 implies but does not close GAP-01**: Wang et al. (2023)
and Jiang et al. (2023) trigger retrieval from the *model's* confidence rather than from retrieval evidence,
and neither reports refusal precision on answerables. Three gaps rest only on "the searches did not find it"
and are flagged where they occur.

---

## 1. The register

### GAP-01 — Two-sided retrieval gate on a hardness ladder

**Research question:** Does a logistic gate on retrieval features alone hold abstain precision ≥ 0.70 at
abstain recall ≥ 0.50 on the three hardest rungs of a five-rung negative ladder, retaining ≥ 80% of
answerables?

**Why it is unanswered:** Searched for by name and not found (D2-2 §3.4). Abdumalikov et al. (2024) report
classifier accuracy on constructed negatives — not a calibrated policy — and document a 98%→1% collapse on
high-overlap negatives; Peng et al. (2024) have the right metrics but sweep components, not thresholds; Wagner
(2026) fits two thresholds on a hidden-state probe without a dev/held-out protocol.

**Why it matters:** If it holds across rungs, refusal is an index-side decision and prompt instructions are
the wrong layer; if it breaks at premise violation, the gate is a missing-entity detector and the fix is
premise checking.

**Cheapest honest test:** SQuAD 2.0 validation (11,873 rows; Rajpurkar et al. 2018) plus 20,000 distractors;
five rungs of 400 negatives (random, same-entity, BM25 near-miss, premise-violating, underspecified) and 2,000
answerables; features BM25 top-1 and margin, bge-small cosine, MiniLM rerank, rank agreement, answer
log-probability; fit on half, test on half; report precision and recall per rung, retention, and the feature
range beside the threshold. **~45 min.**

**Expected effect and null:** ≥ 0.75 through rung 3, near-chance at rung 4. A flat curve means the ladder
measures nothing — itself a reportable negative.

**Failure modes:** Rung hardness tracks length and overlap — resample to matched distributions. SQuAD
answerables share vocabulary with their passages — report retention on a paraphrased subset.

**Evidence strength:** strong. **Cost:** M.
### GAP-02 — Threshold transfer across shift axes

**Research question:** Does a threshold fitted on one configuration keep its abstain precision within ±5
points when transferred to another model, another retrieval budget, or a contaminated index?

**Why it is unanswered:** Calibration is a property of a distribution pair, not a model (Wald et al. 2021),
and no one reports a gate's calibration after retrieval moves the feature distribution (D2-2 §3.3). Kamath et
al. (2020) recover coverage at fixed accuracy under domain shift — one axis, no threshold portability; Zhou et
al. (2025) show retrieval state alone flips refusal.

**Why it matters:** If thresholds do not transfer, every published gate number is configuration-specific and
the deliverable is a recalibration protocol; if they do, the lab's failure was an implementation bug.

**Cheapest honest test:** Reuse GAP-01's gate and features; vary k ∈ {1,3,5,10}, reranker on/off, clean versus
20%-contaminated index (4,000 injected distractors), and a second reader (Llama-3.2-3B) that moves only the
log-probability feature; report Δ abstain precision at fixed abstain recall, ECE, and risk–coverage per
condition. **~3 h.**

**Expected effect and null:** 10–25 points of precision loss at k=1 and on the contaminated index. A null —
transfer within ±5 points everywhere — is the more surprising paper.

**Failure modes:** Changing k changes the answerability base rate — reweight every condition to a constant
base rate. Swapping the reader leaves retrieval features untouched — ablate the log-probability feature and
report both gates.

**Evidence strength:** medium. **Cost:** M.
### GAP-03 — Answerable-side hardness

**Research question:** At fixed abstain recall on negatives, does retention of answerables fall monotonically
across PopQA popularity quintiles, by ≥ 15 points from most popular to rarest?

**Why it is unanswered:** Gates are validated on easy answerables, so retention looks healthy while the gate
keys on difficulty (D2-2 §6 G3). PopQA builds exactly the stratum axis and shows models fail on the long tail
(Mallen et al. 2022), but no gate paper uses it; Kamath et al. (2020) report coverage with no difficulty axis
and AbstentionBench aggregates the curve away.

**Why it matters:** If retention falls from popular to rare entities, a gate silences the long-tail questions
retrieval was bought to answer — a harm no aggregate abstention rate expresses.

**Cheapest honest test:** PopQA test split, 2,000 items (400 per quintile); fetch each entity's Wikipedia
intro through the public API (2,000 cached requests) as the corpus; BM25 top-5 plus bge-small top-5; apply
GAP-01's threshold without refitting; report answered fraction and accuracy per quintile with Wilson
intervals. **~2 h.**

**Expected effect and null:** A 10–20 point Q5–Q1 retention gap. A flat curve would make the gate unusually
difficulty-invariant, strengthening the case for gates where retrieval is weakest.

**Failure modes:** Popularity correlates with retrieval score — condition on gold-in-top-5 and report both.
PopQA scoring is alias-noisy — use the released alias lists and hand-audit 100 items.

**Evidence strength:** medium. **Cost:** M.
### GAP-04 — Separating "I don't know" from "I won't answer"

**Research question:** On the same 600 outputs, does splitting epistemic from safety refusal change measured
gate precision by more than 10 points, and can a deterministic scorer reproduce the split at κ ≥ 0.6 against
150 hand labels?

**Why it is unanswered:** The behaviours are conflated almost everywhere: AbstentionBench scores abstention
with an LLM judge over 20 datasets (Kirichenko et al. 2025) and XSTest measures only the safety side (Röttger
et al. 2023). A 2026 SSRN note argues heuristic classifiers undercount refusals in Indic languages — the
instrument critique, without the confusion matrix.

**Why it matters:** If a third of "correct abstentions" on false-premise items are safety refusals, published
scores are inflated and the repair differs; it also decides whether a zero-budget lab can score abstention
without an API judge, on which GAP-01 depends.

**Cheapest honest test:** 600 outputs (300 unanswerable, 300 answerable) from GAP-01's best configuration;
labels answered / epistemic refusal / safety refusal / malformed; hand-code 150, score all 600 with a
regex-plus-entailment rule; report κ, the confusion matrix, and precision with and without safety refusals
counted as abstentions. **~4 h**, mostly labelling.

**Expected effect and null:** 5–15 points of precision inflation when pooled. A null means the conflation is
harmless here and the cheap scorer suffices.

**Failure modes:** The scorer penalises hedged partial answers, the category that matters — report
per-category confusion, not κ alone. One annotator cannot estimate label noise — double-code 100 items.

**Evidence strength:** medium. **Cost:** S–M.
### GAP-05 — The break-even cost ratio

**Research question:** At what false-negative-to-false-positive cost ratio does the highest-abstain-precision
gate stop being utility-optimal, and is that ratio inside a plausible range (1:1 to 50:1)?

**Why it is unanswered:** The machinery is old — learning to defer (Mozannar & Sontag 2020), risk-controlling
prediction sets — and no benchmark ships a cost model (D2-2 §3.6). A 2026 survey of 49 fraud sources finds
none of 18 reporting per-decision cost, latency, or calibration (Gabani 2026); X-MAP quotes one asymmetric
point (Zhang et al. 2026).

**Why it matters:** If rankings flip at 3:1, every single-threshold comparison here is an arbitrary slice and
F1 should stop being accepted as a summary; if flips need 50:1, F1 tuning is defensible.

**Cheapest honest test:** Closed-form on GAP-01's cached scores and the lab's UCI TF-IDF model (Almeida et al.
2011): sweep ratios 1:1–100:1, compute expected utility per gate, report flip ratios and their stability
across a parametric and a non-parametric ranker. No new inference. **~1 h.**

**Expected effect and null:** At least one flip inside 1:1–20:1 between the max-logit baseline and the
two-sided gate. A null is a permission slip for F1-based evaluation, worth reporting for the same reason.

**Failure modes:** A reviewer reads it as the ROC re-plotted in cost space — report the flip ratio as the
quantity and show it stable across two rankers. The costs are invented — publish only the sensitivity surface.

**Evidence strength:** strong. **Cost:** S.
### GAP-06 — Stale-hit rate as a memory metric

**Research question:** For 300 superseded facts, does append-only retrieval return the stale value in the top
5 more often than a bi-temporal store by ≥ 15 points, with no difference in answer accuracy?

**Why it is unanswered:** Zep is the only system with an explicit supersede mechanism and validity intervals
(Rasmussen et al. 2025); Mem0 chooses ADD/UPDATE/DELETE with an LLM and keeps no audit trail (Chhikara et al.
2025). LongMemEval's knowledge-update number, 78.2% versus 83.3%, is five points on a fraction of 500,
judge-scored, on timestamp-ordered histories, so a reader preferring the latest session scores well without
update logic (Wu et al. 2024). D2-1 §3.5 states that no stale-hit rate is reported anywhere.

**Why it matters:** It decides whether memory stores need temporal invalidation at all, and gives the first
judge-free number for an ability every system claims; a store that merely appends can match on accuracy and
fail this metric completely.

**Cheapest honest test:** LoCoMo's released 10 conversations (5,882 turns; Maharana et al. 2024); 300
supersede pairs built semi-automatically (same entity and attribute, different value, session j > i), 100
hand-verified; three SQLite stores — append-only, delete-on-write, bi-temporal — over BM25 top-5; report
stale-hit@5 on the retrieved set before any reader sees it, plus accuracy on 150 date-conditioned questions.
**~4 h.**

**Expected effect and null:** Stale-hit@5 near 0.5 for append-only versus under 0.1 for bi-temporal, with a
much smaller accuracy gap. A null would mean the contradictions are too sparse to matter, which would explain
the metric's absence.

**Failure modes:** Reader position bias supplies the update for free — score the retrieved set only. Lexical
pair construction yields non-contradictions — report hand-verified pair precision.

**Evidence strength:** strong. **Cost:** M.
### GAP-07 — Report k/N beside recall@k

**Research question:** In memory benchmarks, how far does recall@5 exceed its random floor k/N, and does the
ranking of four retrieval methods change once the floor is subtracted?

**Why it is unanswered:** LoCoMo as released holds 5,882 turns and 1,986 questions retrieved per conversation
— a corpus of ~588 turns or 27 sessions, so session-level recall@5 is a hit rate over 18.5% of the corpus and
turn-level over 0.85%; LongMemEval-S is ~40–50 sessions, so k=5 covers 10–12%. BEIR is the only benchmark here
where nDCG@10 means something at 50M documents (Thakur et al. 2021), and the bound on distinct top-k sets
explains why the denominator decides (arXiv:2508.21038). No memory paper reports k/N.

**Why it matters:** If method differences shrink to noise after floor adjustment, comparison tables partly
measure corpus size; it also settles turn-versus-session granularity, which makes cross-paper LoCoMo numbers
incomparable.

**Cheapest honest test:** Recompute recall at both granularities for BM25, bge-small, MiniLM and RRF from
cached runs; report raw, floor, floor-adjusted, and Spearman correlation between raw and adjusted rankings;
add a synthetic corpus-size sweep (10–1,000 sessions). **~2 h.**

**Expected effect and null:** At turn level the correction is cosmetic (0.0085); at session level (0.185)
close methods should reorder. A null still publishes a convention: the field's numbers are safe at turn level,
which is not currently known.

**Failure modes:** At turn level the result looks like a nitpick — lead with the session-level number. Running
only our methods limits the claim — frame as protocol plus demonstration.

**Evidence strength:** strong. **Cost:** S.
### GAP-08 — Retrieval or reader? Attribution at fixed reader

**Research question:** With the reader held fixed, what share of memory-QA error is retrieval miss versus
reader failure, and does a note-taking prompt at fixed retrieval recover ≥ 10 points?

**Why it is unanswered:** Memory papers report answer accuracy, not retrieval quality; LongMemEval is the
exception and should be the template (D2-1 §3.3). Oracle retrieval 0.870 versus 0.606 with the full 115k-token
history is a 26-point reading failure, while Chain-of-Note at fixed retrieval buys up to 10 points (Wu et al.
2024).

**Why it matters:** If most residual error at fixed retrieval is reader-side, memory-system engineering is
misallocated and prompt work is the better buy — the opposite of the field's emphasis.

**Cheapest honest test:** 300 LongMemEval-S questions stratified across the five abilities; BM25 top-5; three
conditions (retrieved-only, oracle evidence sessions, full history truncated to 8k); reader Qwen3-1.7B at Q4;
score extractive abilities by containment against gold, hand-check 100, log recall@5 separately. **~7 h.**

**Expected effect and null:** A 15–30 point oracle-minus-retrieved gap that a note-taking prompt closes by
half. If the prompt recovers nothing, reader capability binds and the effort belongs in model choice.

**Failure modes:** A 1.7B reader floors every condition — repeat 200 items through the dev-time API model. The
8k truncation is arbitrary — report a 4k/8k curve.

**Evidence strength:** strong. **Cost:** L.
### GAP-09 — Native versus translated items inside one language

**Research question:** Within Punjabi (83% translated) and Hindi (under 1%), does accuracy on native items
exceed translated items by ≥ 5 points at n=1,000 per language?

**Why it is unanswered:** MILU publishes per-item translation flags — Hindi 14,837 items of which 115 are
translated, Punjabi 4,099 of which 3,411 are — and reports no within-language split, so its headline "models
do better in high-resource languages" is confounded with "the low-resource languages are mostly translations"
(D2-5 §3.1). Global MMLU shows provenance moves rankings by 3.7–7.3 positions, across languages rather than
within one item pool (Singh et al. 2025).

**Why it matters:** If the gap is ≥ 5 points, every Indic benchmark built by translation inherits a bias of
known magnitude and gains a correction; if it is near zero, MILU's headline survives a serious objection.

**Cheapest honest test:** 1,000 Punjabi items stratified by provenance and subject, 1,000 Hindi items;
Qwen3-1.7B; likelihood scoring over four options; accuracy delta with intervals per subject. **~4 h**, ~2.5 h
at 600-item cells.

**Expected effect and null:** 5–10 points favouring native items in Punjabi. A null is the more publishable
result, because it defends the dominant benchmark-construction practice.

**Failure modes:** Provenance correlates with subject and difficulty — stratify by subject and recheck on
items a second model finds equally hard. Translation quality varies by translator — report per-subject deltas.

**Evidence strength:** strong. **Cost:** M.
### GAP-10 — Abstention in Hindi, and the language of refusal

**Research question:** Does a 1.7B model refuse unanswerable Hindi questions at above-chance rates (AUC ≥
0.65), and does the language the refusal appears in change the measured refusal rate by ≥ 15 points?

**Why it is unanswered:** The Indic dive found no dataset, benchmark or paper measuring whether a model knows
it does not know in Hindi, Hinglish or any Indic language; every candidate benchmark is answerable by
construction (D2-5 §3.2). The nearest work is English (AbstentionBench, XSTest); two 2026 preprints are
adjacent but not the measurement — an SSRN note on undercounted Indic refusals and an English-only comparison
of abstention interfaces.

**Why it matters:** If refusals come out in English while the prompt is Hindi, every English-lexicon refusal
metric mis-scores an Indic deployment enough to reverse a comparison; near-chance AUC would make this a
capability gap, not a calibration problem.

**Cheapest honest test:** 400 answerable Hindi items from Belebele (900 per variant; Bandarkar et al. 2024),
200 constructed unanswerables (question paired with an unrelated passage), 100 invented-entity items;
Qwen3-1.7B; report refusal rate, over-refusal, AUC, refusal-language distribution and ECE on option logits;
100 hand labels for the language-aware rule. **~3 h** plus labelling.

**Expected effect and null:** AUC 0.6–0.75 with 10–30% of refusals in English. Near-chance AUC would make this
a documented capability gap rather than a measurement gap.

**Failure modes:** "Unanswerable from the passage" is not "unanswerable", since parametric memory turns a good
refusal into a false answer — the invented-entity arm. Refusal-language detection is itself a classifier —
hand-label 100 and report agreement.

**Evidence strength:** strong. **Cost:** M.
### GAP-11 — The style-only control for scam detection

**Research question:** How much of a scam detector's F1 survives when content words are removed and only
surface form remains — length, punctuation, capitalisation, digits, currency symbols, emoji, URL shape?

**Why it is unanswered:** The misinformation literature ran this control and its detectors collapsed:
injecting sentiment, style, topic and perplexity shortcuts drops accuracy by roughly 80% on average and to 0%
in the worst case (Wan et al. 2025). D2-6 §3 states the scam analogue as unresolved and no published version
was found; the absence claim rests on that search, not on a named paper.

**Why it matters:** It decides whether "scam detection" is a fraud-intent classifier or a genre classifier — a
regulatory distinction, since a system sold as detecting fraud while detecting promotional register is making
a false claim.

**Cheapest honest test:** UCI SMS Spam (5,574 messages, deduplicated; Almeida et al. 2011) plus Smishing
Dataset I (1,062 positives, 1,062 sampled negatives); TF-IDF+LR and MuRIL; three arms — full, style-only,
content-only; permutation test on style features. **~2 h.**

**Expected effect and null:** Style-only F1 of 0.7–0.85, i.e. most of the headline survives. A low style-only
score would not by itself prove content-driven detection — hence the content-only arm — but it would let the
field keep claiming fraud detection.

**Failure modes:** The ablation also removes legitimate signal, since urgency lexicon is content — report all
three arms. Near-duplicates inflate both arms — deduplicate first.

**Evidence strength:** strong. **Cost:** S–M.
### GAP-12 — Evasion priced in attacker tokens

**Research question:** What does one successfully evaded scam message cost in tokens, and does F1 fall below
0.6 before that cost exceeds 100 tokens?

**Why it is unanswered:** The collapse is measured for machine-text detection — recursive paraphrasing drops
watermark TPR at 1% FPR from 99.3% to 9.7% and zero-shot detector AUROC from 96.5% to 25.2% (Sadasivan et al.
2023; Krishna et al. 2023) — and for SMS spam under delivery-verified perturbations (Salman et al. 2024).
Nobody converts the collapse into a price; D2-6 §3 names the gap.

**Why it matters:** At ~30 tokens per evasion, classifier defence is economically dead and the right
investment is provenance and allow-lists; at ~3,000, classifiers ration attacks and current deployment is
defensible.

**Cheapest honest test:** 500 UCI spam and 500 ham; paraphraser Qwen3-1.7B at three strengths; count tokens
per generated message; detectors TF-IDF+LR and MuRIL; report F1 drop against tokens per successful evasion,
plus 100 human paraphrases as an upper bound on attacker quality. **~3 h.**

**Expected effect and null:** F1 falls 20–40 points at under 200 tokens per message. A null — high cost for
small degradation — would vindicate classifier defence and be the more useful result for deployers.

**Failure modes:** A local paraphraser is weaker than a motivated attacker, overstating cost — state it as an
upper bound and pair it with the human arm. Paraphrase also moves ham — report both classes' deltas.

**Evidence strength:** strong. **Cost:** M.
### GAP-13 — What "2 GB" means

**Research question:** For six models between 0.3B and 4B, how far apart are the four candidate definitions of
"fits in 2 GB" — weight file, llama.cpp allocation at declared context, peak private working set, peak total
including mapped file — and does any model change category?

**Why it is unanswered:** The three papers that use a memory number mean three different things: model
footprint, process peak RSS, and llama.cpp's allocation at a fixed context, the last allocating KV cache by
the model's maximum context unless overridden (D2-3 §3). MLPerf-style suites define no laptop RAM scenario, so
"runs in 2 GB" is one of at least four claims.

**Why it matters:** Any claim that a model runs on a low-cost Indian device is unfalsifiable until the
definition is fixed; a measured table plus a definition is a citable convention and the cheapest credibility
item in the efficiency area.

**Cheapest honest test:** Gemma-3-270M, Qwen3-0.6B, Llama-3.2-1B, Qwen3-1.7B, Llama-3.2-3B, Qwen3-4B; four
definitions; context 2,048 and 8,192; three repeats; report GB per definition and the max/min ratio. **~2 h**,
mostly downloads.

**Expected effect and null:** A 2–4× spread between the smallest and largest definition, with at least one
model changing category. A narrow spread would make the convention easy to fix and the discrepancy a
non-issue.

**Failure modes:** Windows accounts for mapped files differently from Linux — report private working set and
total separately. Page-cache noise — three repeats, report the range not the mean.

**Evidence strength:** medium. **Cost:** S–M.
### GAP-14 — Does speculative decoding help on an x86 CPU?

**Research question:** At batch 1 with llama.cpp on x86, does a 0.6B draft against a 1.7B target ever exceed
1.15×, and does measured verify cost scale sub-linearly with batch size?

**Why it is unanswered:** The consumer-hardware anatomy finds three of five configurations decelerate and
locates the mechanism: at small batch the quantised backend verifies as per-position matrix–vector products,
so a 7-token verify costs 218.5 ms against 51.0 ms for two (2026, arXiv:2607.17283). The CPU systems paper
attributes 35.0% of its throughput gain to systems work against 6.0% for its kernel (2026, arXiv:2610.28671).
Both predict a negative result for vanilla x86; neither runs it.

**Why it matters:** It decides whether CPU deployment should use draft models at all, and whether the
bottleneck is numerical or operating-system level — different fixes at different costs.

**Cheapest honest test:** Qwen3-0.6B draft, Qwen3-1.7B target, K ∈ {1,2,4,8}, 200 prompts × 128 tokens, fixed
threads; plus a synthetic timing of one n_batch pass at batch 1–16; report tokens/s, acceptance, and verify
time per position. **~3 h.**

**Expected effect and null:** ≤ 1.1× with acceptance falling as K rises, and flat verify cost per position. A
real speedup would contradict the published mechanism and demand an explanation, likely a backend version
difference.

**Failure modes:** llama.cpp changes the internal batch, so configured K is not executed K — instrument actual
verified token counts. Acceptance differences confound kernel effects — report acceptance and per-token verify
cost separately.

**Evidence strength:** medium. **Cost:** M.
### GAP-15 — Variance decomposition at the scale people actually work

**Research question:** At n=500, what share of total variance in a two-model comparison is item, seed and
prompt format, and is the seed share larger than half the effect being claimed?

**Why it is unanswered:** The variance study measures 13 benchmarks and 280 models and finds papers reporting
one number per benchmark, but decomposes benchmark-level variance, not seed × format × item at 1–3B (2024,
arXiv:2406.10229). The error-bars paper supplies the power formula and recommends 1,000 items (Miller 2024);
D2-4 §5 derives that n=500 defends 5.6 points. Nobody has checked that derivation by measuring the components.

**Why it matters:** It sets the minimum defensible effect for every later claim in this lab, and for
small-model papers generally; if format variance dominates, published small-model comparisons are prompt
artefacts.

**Cheapest honest test:** Qwen2.5-3B and Llama-3.2-3B × three formats (0-shot, 5-shot, CoT) × three seeds ×
500 MMLU items (fixed list) plus 300 ARC-Challenge; variance components from a linear mixed model; MDE at 80%
power. **~9 h.**

**Expected effect and null:** Format explains more variance than seed, and the seed share sits below the
5.6-point MDE. If seeds dominate, three-seed evaluation at n=500 is not worth running — a direct saving.

**Failure modes:** Three seeds estimate seed variance poorly — report intervals on the components and frame
them as bounds. Small models sit near chance on many MMLU subjects — stratify by subject.

**Evidence strength:** strong. **Cost:** L.
### GAP-16 — How far can a small judge be trusted?

**Research question:** On 300 items, does a 3B local judge rank two systems as a frontier judge and 100 human
labels do (κ ≥ 0.6), and does order-swap averaging fix or entrench its bias?

**Why it is unanswered:** JudgeBench puts a vanilla GPT-4o judge at 50.86% on correctness-style pairs, the
best fine-tuned judge at 57.43%, and an open 7B evaluator at 34.86%, below chance (Tan et al. 2024). The
position-bias study finds the best judge at 0.828 consistency, with disagreement concentrated on near-ties
(Shi et al. 2024). None reports whether averaging both orders works when the judge is small.

**Why it matters:** It decides whether a zero-budget lab may use any judge, and whether the usual debias is
safe; if order-swap averaging yields confidently wrong verdicts for weak judges, much student-scale evaluation
is invalid.

**Cheapest honest test:** 300 pairs from RAGTruth's QA subset (5,767 human-labelled responses, 29.6%
hallucinated), 150 deliberately near-tied; judges Qwen2.5-3B and Llama-3.2-3B at Q4 plus 300 dev-time API
calls; reference 100 hand labels; report κ, rank agreement, verdict-flip rate under swap, and a simulated MDE
versus agreement. **~5 h.**

**Expected effect and null:** κ 0.4–0.6 for the small judge, errors concentrated on near-ties, and order-swap
averaging raising consistency without accuracy; a high κ would make local judging viable.

**Failure modes:** 100 labels give a wide κ interval — report the interval and treat the result as a screen.
Obvious pairs flatter the judge — the near-tie half is mandatory.

**Evidence strength:** strong. **Cost:** M.
---

## 2. Ranked table

Score = evidence (strong 3, medium 2, weak 1) × feasibility (S 3, M 2, L 1) × distinctness (no prior
measurement 3, partial 2, replication 1). The formula rewards cheapness because every gap must be runnable;
cheapness is not the same as a paper, and §3 says which combinations carry one.

| Rank | Gap | Evidence | Feasibility | Distinctness | Score | Best used as |
|---:|---|---|:---:|:---:|---:|---|
| 1 | GAP-07 k/N floor | strong | S | 3 | **27** | section of a memory paper |
| 2 | GAP-05 break-even ratio | strong | S | 3 | **27** | section of GAP-01's paper |
| 3 | GAP-13 what "2 GB" means | medium | S–M | 3 | **18** | standalone short note |
| 4 | GAP-01 hardness ladder ★ | strong | M | 3 | **18** | the paper |
| 5 | GAP-06 stale-hit rate ★ | strong | M | 3 | **18** | the paper (memory) |
| 6 | GAP-09 MILU native/translated | strong | M | 3 | **18** | the paper (Indic) |
| 7 | GAP-10 Hindi abstention | strong | M | 3 | **18** | the paper (Indic) |
| 8 | GAP-12 evasion priced | strong | M | 3 | **18** | the paper (scam) |
| 9 | GAP-02 threshold transfer | medium | M | 3 | 12 | second experiment in GAP-01 |
| 10 | GAP-03 answerable hardness | medium | M | 3 | 12 | third experiment in GAP-01 |
| 11 | GAP-16 small judge | strong | M | 2 | 12 | standalone methods paper |
| 12 | GAP-11 style-only control | strong | S–M | 2 | 12 | with GAP-12 |
| 13 | GAP-04 abstain vs refuse | medium | S–M | 2 | 8 | section, needs labels |
| 14 | GAP-14 spec decoding | medium | M | 2 | 8 | standalone efficiency note |
| 15 | GAP-08 attribution | strong | L | 2 | 6 | only with API reader access |
| 16 | GAP-15 variance | strong | L | 2 | 6 | standalone, one week |

★ Top five by score are GAP-07, GAP-05, GAP-13, GAP-01 and GAP-06; two of them (GAP-07, GAP-05) are hours
of arithmetic that belong inside another paper, and GAP-13 survives as a short standalone note. The two
with the strongest claim to *carry* a paper are GAP-01 and GAP-06, which is why the stars sit there.

---

## 3. Which gaps combine, and which must stay apart

**Paper A — recommended: GAP-01 + GAP-02 + GAP-03 + GAP-05.** One gate, one feature cache, one corpus
family, four measurements: does it hold on a ladder, does it transfer, does it silence the long tail, in
what cost regime is it the right gate. About 1.5 days of compute, one day of writing. The lab's measured
failure (47 of 82 answerables refused at precision 0.30, threshold outside the observed range) becomes the
motivating case rather than a hidden embarrassment, and the paper closes on the diagnostic that would have
caught it: print the observed feature range beside every fitted threshold. That diagnostic is a line of code
and the most quotable thing here.

**Paper B — memory: GAP-06 + GAP-07.** GAP-06 is the headline, a judge-free metric for an ability every
system claims; GAP-07 is not decoration, because at session granularity the random floor is 18.5% and the
reader needs that denominator before believing a 15-point stale-hit difference. GAP-08 stays out: it needs
an API reader to avoid a floor effect.

**Paper C — Indic: GAP-09 + GAP-10.** One model, two datasets, about a day. GAP-10's refusal-language
finding is interpretable only alongside GAP-09's translation accounting: if Punjabi items are 83%
translated, a low Punjabi refusal rate has two explanations and the paper must separate them.

**Paper D — scam: GAP-11 → GAP-12.** Deduplicate first or both arms are inflated; then the style control,
which reframes the field; then the evasion price, which generalises. Do not repeat GAP-05's cost analysis
here.

**Paper E — evaluation noise: GAP-16 (+ GAP-15 if a week is free).** GAP-16 alone is thin, GAP-15 alone is a
week.

**Must stay apart.** (i) Papers A and D share the word "gate" and nothing else — selective prediction over
retrieval evidence versus classification under attack; bundling reads as a grab bag and doubles the
annotation. (ii) GAP-07 must not be folded into Paper A: different corpus, different claim. (iii) GAP-10
must not enter GAP-01 until the English gate is frozen, because refusal-language detection is a second
instrument whose error would be attributed to the gate. (iv) GAP-04 changes the labelling protocol for every
other item; run it after Paper A.

---

## 4. Gaps excluded, and why

**Already answered by others.** Quantisation damage per script — Marchisio et al. (2024) measured it and
showed automatic metrics understating human-evaluated damage by an order of magnitude. Perplexity as a proxy
for task quality at small scale — the 2026 format sweep already shows identical perplexity with a 3.4-point
GSM8K spread at 8B, and extending it to 1–3B is a replication with a floor-effect problem. Base rates at
realistic prevalence — textbook arithmetic, worth a paragraph in GAP-11. Deduplicated splits — Wu and Hooi
(2022) show 90.2%→44.3% after event-separated re-splitting; re-running that on SMS is a prerequisite, built
into GAP-11 and GAP-12 as a control.

**Needs compute or access we lack.** Training-based contamination injection needs fine-tuning runs; the
inference-only version was judged too weak to rank. Cost-normalised agent comparison needs API spend
proportional to a real trajectory. pass@k versus pass^k recomputation depends on third-party HAL logs we do
not control. The CPU quality/RAM/latency frontier for 0.3–4B costs 15–25 model-hours and collides with the
shared-laptop rule — deferred, not rejected. Training anything, including LoRA on a 3B, is out of scope.

**High scoop risk or circular.** Token budget versus information budget in Indic evaluation is a good
experiment in a crowded lane: four 2026 papers on Indic tokenisation are moving through it. Chunking under
fertility has a structural problem — gold passages would have to be defined at chunk level, making chunking
and ground truth dependent, and document-level gold is a week of annotation.

**Annotation-blocked or ethically fraught.** A bibliometric audit of variance reporting needs two
independent annotators for a meaningful κ; one student plus agents produces a number that means nothing. The
Hinglish annotation-ceiling study needs three annotators from a comparable dialect range; one coder's
disagreement with 2020 labels measures the coder. Building an Indian scam corpus from real victim messages
raises consent and re-identification problems a workshop paper cannot discharge, and a template-generated
corpus measures the template space rather than the world.

---

## 5. What this register does not claim

GAP-11, GAP-12 and GAP-13 rest partly on "the deep dives' searches did not find it" and are weaker than the
ten where a specific adjacent paper is named and shown to omit the measurement. Nothing here is a novelty
claim; that needs NOVELTY-CHECK.md with logged queries. No timing is a result — all are arithmetic from
measured throughput (136 paragraphs/s for bge-small, 361 ms per reranked query, 15–40 tokens/s decode) and
must be replaced by a measured figure in the first hour of work.

---

## References

Each entry resolved through `02_literature/tools/verify_citations.py`; four new rows in `S2-8-verified.csv`,
the rest in the merged canonical `verified_citations.csv` (270 rows). Retrieved 2026-11-03.

1. Abdumalikov et al. Answerability in Retrieval-Augmented Open-Domain Question Answering (2024). arXiv:2403.01461
2. Almeida, Gómez Hidalgo, Yamakami. Contributions to the study of SMS spam filtering (2011). 10.1145/2034691.2034742
3. Bandarkar et al. The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122 Language Variants (2024). 10.18653/v1/2024.acl-long.44
4. Chhikara et al. Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory (2025). arXiv:2504.19413
5. Gabani. Operational Evidence Gaps for LLMs in Fraud Detection and Trust-and-Safety Workflows (2026). arXiv:2607.13078
6. Jiang et al. Active Retrieval Augmented Generation (2023). arXiv:2305.06983
7. Kamath, Jia, Liang. Selective Question Answering under Domain Shift (2020). arXiv:2006.09462
8. Kirichenko et al. AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions (2025). arXiv:2506.09038
9. Krishna et al. Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense (2023). arXiv:2303.13408
10. Maharana et al. Evaluating Very Long-Term Conversational Memory of LLM Agents (2024). arXiv:2402.17753
11. Mallen et al. When Not to Trust Language Models: Investigating Effectiveness of Parametric and Non-Parametric Memories (2022). arXiv:2212.10511
12. Marchisio et al. How Does Quantization Affect Multilingual LLMs? (2024). arXiv:2407.03211
13. Miller. Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations (2024). arXiv:2411.00640
14. Mozannar, Sontag. Consistent Estimators for Learning to Defer to an Expert (2020). arXiv:2006.01862
15. Peng et al. Unanswerability Evaluation for Retrieval Augmented Generation (2024). arXiv:2412.12300
16. Rajpurkar, Jia, Liang. Know What You Don't Know: Unanswerable Questions for SQuAD (2018). arXiv:1806.03822
17. Rasmussen et al. Zep: A Temporal Knowledge Graph Architecture for Agent Memory (2025). arXiv:2501.13956
18. Röttger et al. XSTest: A Test Suite for Identifying Exaggerated Safety Behaviours in Large Language Models (2023). arXiv:2308.01263
19. Sadasivan et al. Can AI-Generated Text be Reliably Detected? (2023). arXiv:2303.11156
20. Salman et al. Investigating Evasive Techniques in SMS Spam Filtering: A Comparative Analysis of Machine Learning Models (2024). 10.1109/access.2024.3364671
21. Shi et al. Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge (2024). arXiv:2406.07791
22. Singh et al. Global MMLU: Understanding and Addressing Cultural and Linguistic Biases in Multilingual Evaluation (2025). 10.18653/v1/2025.acl-long.919
23. Tan et al. JudgeBench: A Benchmark for Evaluating LLM-based Judges (2024). arXiv:2410.12784
24. Thakur et al. BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models (2021). arXiv:2104.08663
25. Verma et al. MILU: A Multi-task Indic Language Understanding Benchmark (2024). arXiv:2411.02538
26. Wagner. Two Axes of LLM Abstention: Answer Correctness and Question Answerability (2026). 10.48550/arxiv.2607.08456
27. Wald et al. On Calibration and Out-of-domain Generalization (2021). arXiv:2102.10395
28. Wan et al. Truth over Tricks: Measuring and Mitigating Shortcut Learning in Misinformation Detection (2025). arXiv:2506.02350
29. Wang, Li, Sun, Liu. Self-Knowledge Guided Retrieval Augmentation for Large Language Models (2023). arXiv:2310.05002
30. Wu, Hooi. Probing Spurious Correlations in Popular Event-Based Rumor Detection Benchmarks (2022). arXiv:2209.08799
31. Wu et al. LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory (2024). arXiv:2410.10813
32. Zhang et al. X-MAP: eXplainable Misclassification Analysis and Profiling for Spam and Phishing Detection (2026). arXiv:2602.15298
33. Zhou et al. Do Retrieval Augmented Language Models Know When They Don't Know? (2025). arXiv:2509.01476
34. Which Quantization Should I Use? A Unified Evaluation of llama.cpp Quantization on Llama-3.1-8B-Instruct (2026). arXiv:2601.14277
35. Lossless but Not Free: An Empirical Anatomy of Speculative Decoding on Consumer Hardware (2026). arXiv:2607.17283
36. Accelerating CPU Speculative Decoding via Unified Graph Execution and Transactional KV Isolation (2026). arXiv:2610.28671
37. Quantifying Variance in Evaluation Benchmarks (2024). arXiv:2406.10229
38. On the Theoretical Limitations of Embedding-Based Retrieval (2025). arXiv:2508.21038
39. A Measurement Crisis in Multilingual LLM Safety: Heuristic Classifiers Systematically Undercount Reasoning-Model Refusals in Indic Languages (2026). 10.2139/ssrn.7152058
40. Where Abstention Lives: A Pre-Registered Four-Way Comparison of Abstention Interfaces in a Small Language Model with Versioned Memory (2026). 10.21203/rs.3.rs-10839567/v1

FILES: 02_literature/GAP-MINING.md
PAPERS_VERIFIED: 4 (02_literature/staging/S2-8-verified.csv); 270 rows in the merged canonical register
STATUS: DONE
