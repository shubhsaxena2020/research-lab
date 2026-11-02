# Novelty pre-scan — four candidate topic families (S2-10)

**Status:** pre-scan, not the final novelty check. Its job is to kill a family early if someone has
already done it. Written 2026-11-03.

**One-line answer:** of the four families, one (memory staleness) is already done, two are heavily
crowded with only a narrow measurement slice left (retrieval-feature abstention gate, scam detection
under realistic prevalence), and one (Indic abstention) is crowded in a way that makes the planned
claim predictable. The most valuable finding is §6: four papers published in the last eight months
measure, almost exactly, what two of these families proposed to measure.

---

## 0. Method, and three limits you must read before trusting the counts

**What was run.** 91 distinct queries through the lab's own resolver,
`verify_citations.py search --query "..." --limit 10 --source arxiv`, on 2026-11-03. Every query, its
printed count and its date are in the audit table (§7); raw rows are in
`staging/S2-10-queries.jsonl`, produced by `staging/S2-10-run_queries.py`, which records the tool's own
`-- N results` line and marks a row `ERROR` when the tool logged a 429, so a dead request can never be
read as a genuine zero.

**Limit 1 — OpenAlex was down for the whole scan.** Every call returned HTTP 429: *"Insufficient
budget… counts against the free daily budget shared by everyone on your network's IP address… ($0
remaining; resets at midnight UTC)."* I registered a free key (`POST /api-keys`, lab contact address)
but it activates only when the student clicks the emailed link, which I cannot do. **This scan sees
arXiv only.** It under-samples ACL/EMNLP/NAACL papers that are not on arXiv, and cannot verify
DOI-only records. Absence of a hit means "absent from arXiv titles and abstracts", never "absent from
the literature". The six audited deep dives were used as a second discovery channel for exactly this
reason; every paper taken from them was re-resolved here.

**Limit 2 — the tool searches arXiv with a quoted phrase.** `cmd_search` sends
`search_query=all:"<query>"`, which arXiv treats as a phrase over titles and abstracts. A four-word
phrase such as `answerability classification retrieval` returns 0 because no abstract contains that
string, not because the topic is unstudied. I therefore ran two waves: long conceptual phrases (where 0
is weak evidence that the *framing* is unused) and short two-to-three-word phrases (where a hit is real
evidence of prior work). 42 of 91 queries returned 0, 49 returned at least one record. No verdict below
rests on a zero alone.

**Limit 3 — a count of 10 means "at least 10".** `--limit 10` caps `max_results`; the tool prints
records kept, not records held. Those rows are marked `10 (cap)`. Counts are a floor and are not
comparable across queries, which is why every verdict rests on what the returned papers *measure*.

**Screening.** ~500 records skimmed by title; ~90 opened at abstract level via `enrich`; 12 read
further into intro/results via `web_extract`. 72 papers resolved through `verify_citations.py add` into
`staging/S2-10-verified.csv` (72 VERIFIED, 0 MISMATCH, 0 FAIL). All author/year/venue fields below come
from that CSV, not from memory.

---

## 1. Family A — two-sided retrieval-evidence abstention: **CROWDED BUT A SPECIFIC SLICE IS OPEN**

The proposal: a gate over retrieval features (dense similarity, BM25 score/margin, rerank score,
retriever agreement), with separate admit and refuse thresholds fitted on dev, validated held out,
reporting abstain precision/recall on unanswerable items *and* false-refusal rate on answerable items,
negatives stratified random → same-topic near-miss → false premise → underspecified.

Every ingredient exists separately, and most combinations exist too.

The pre-generation gate is the most developed part. RINSE (arXiv:2609.37469, 2026) asks exactly our
question — can sufficiency be judged from question and evidence before an answer exists — using three
signals: whether every part of the question is covered, whether any passage offers an answer, and
whether a small model reading the passages together treats them as sufficient. It scores 0.837 against
0.746 for the best of ten prior methods and 0.784 for a frontier model asked the same question, at 36.5
ms per question. It also documents the trap our ladder would have to avoid: deleting the relevant
evidence or pairing evidence with an unrelated question leaks the label through lexical overlap and
evidence position, so their benchmark varies answer support by substitution, deletion and question-swap
while holding surface features fixed. That is a more careful ladder than ours, published.

The ladder is published twice more. GRAB-RAG (arXiv:2608.22228, 2026) tests the same questions under
four context conditions — supportive, degraded, missing, misleading — and finds three small frozen
models (3.8B–8B) abstain reliably when evidence is missing but still answer 41.6% of misleading
questions under explicit abstention prompting. RefusalBench (arXiv:2510.10390, 2025) generates cases
from 176 perturbation strategies across six uncertainty categories at three intensity levels, and
reports refusal accuracy below 50% on multi-document tasks for frontier models.

Both directions are published. DeclineCraft (arXiv:2610.28340, 2026) reports Correct Abstention Rate
alongside Answerable Attempt Rate and Answer Accuracy across 27 LLMs, finding single-shot retrieval
raises abstention in 38 of 40 configurations while iterative retrieval lowers it. "Two Axes of LLM
Abstention" (arXiv:2607.08456, 2026) makes the sharper version of our argument: correctness and
answerability are separable axes, one threshold cannot serve both, and on false-premise questions
answer-confidence, P(IK), P(True) and direct premise-checking all sit near chance while a hidden-state
probe reaches 0.69–0.77 AUROC; it then builds a calibrated policy from the two axes. If our thesis is
"one threshold is the wrong shape", that thesis is taken.

The negative-sampling result is taken too. Abdumalikov et al. (arXiv:2403.01461, 2024) show a model
trained on random negative passages scores 98% in-distribution and 1% on irrelevant passages with high
semantic overlap, and that SQuAD 2.0-style unanswerable pairs restore it to near 100%.

**What is left.** No paper here fits two *separate* thresholds on dev, evaluates them held out, uses
only cheap retrieval-side features (no generator call, no probe, no second model), and reports abstain
precision/recall with a false-refusal rate across a four-rung negative ladder. RINSE optimises a ranking
score, not a policy with an uncertain band. GRAB-RAG is prompt-based. DeclineCraft reports rates but no
feature gate. Two Axes uses probes.

**Slice that remains open:** a two-threshold admit/refuse band fitted on dev and evaluated held out,
computed only from retrieval-side signals, reported jointly as abstain precision/recall and
false-refusal rate across a four-rung negative ladder.

**Honest risk.** That is a measurement contribution, not a capability. A reviewer will ask how it
differs from RINSE plus GRAB-RAG, and the true answer is "cheaper signals, a band instead of a score,
and an FRA column" — a workshop paper. It is also the only family where the student's measured failure
(a gate that refused 47 of 82 answerable questions because the threshold sat outside the observed
feature range) maps onto an unoccupied gap: no paper here reports that specific pathology, and a band
fitted over the observed dev range is precisely its repair.

### Closest prior work, Family A

| # | Paper (year, arXiv) | Why it is close | Verdict |
|---|---|---|---|
| A1 | Relevance Is Not Sufficient Evidence: Detecting Evidence Gaps Before Generation in RAG (2026, 2609.37469) | Pre-generation sufficiency gate, three signals, documents label-leak traps in hard negatives | CLOSE |
| A2 | Prompt-Based Abstention Fails Under Misleading Context (2026, 2608.22228) | Four-rung context ladder; 41.6% answered on the misleading rung | CLOSE |
| A3 | Two Axes of LLM Abstention: Answer Correctness and Question Answerability (2026, 2607.08456) | Two-sided argument plus calibrated two-score policy; false-premise axis | CLOSE |
| A4 | DeclineCraft: A RAG Abstention Benchmark (2026, 2610.28340) | Abstention on unanswerable *and* answerable attempt rate, 27 LLMs | CLOSE |
| A5 | RefusalBench: Generative Evaluation of Selective Refusal (2025, 2510.10390) | 176 perturbations, six categories, three intensities — stronger ladder | CLOSE |
| A6 | Answerability in Retrieval-Augmented Open-Domain QA (2024, 2403.01461) | Random negatives 98%→1% under semantic overlap; the near-miss finding | CLOSE |
| A7 | Do Retrieval Augmented Language Models Know When They Don't Know? (2025, 2509.01476) | Over-refusal of RALMs when retrieved documents are irrelevant | ADJACENT |
| A8 | Sufficient Context: A New Lens on RAG Systems (2024, 2411.06037) | Sufficiency stratification; large models answer rather than abstain | ADJACENT |

---

## 2. Family B — memory staleness and the miss-vs-wrong split: **ALREADY DONE**

The clearest negative in the scan; it should stop the family.

The proposed headline metric was a stale-hit rate: fraction of top-k retrieved items containing a
superseded fact. MemStrata (arXiv:2606.26511, 2026) defines and reports the answer-level version,
calling it the stale-fact-error rate — RAG serves the superseded value 15–40% of the time across four
evolving-knowledge benchmarks — and argues the failure is structural, since cosine similarity separates
a contradicted fact from a duplicated one at AUROC 0.59. That number is the family's motivation, in
print.

The split is published even more directly. "When Retrieval Is Not Enough: Obsolete Facts in Agent
Memory" (arXiv:2610.36308, 2026) opens by naming our confound: memory benchmarks collapse retrieval and
generation into one score, so you cannot tell whether a failure came from missing an update or from not
using one already retrieved. It separates them with a gold-assisted audit and shows the second
dominates: with the newest statement present in every retrieved set, swapping one unrelated statement
for the obsolete competing statement drops accuracy from 100% to 44.6% (Qwen2.5-7B) and 100% to 87.8%
(Qwen3-14B), while growing the retrieved budget from 64 to 512 tokens *lowers* BM25 accuracy from 45%
to 32%. "Retrieved something contradicting" as a distinct refusal cause with a distinct repair is that
paper's contribution.

The pre-generation version is taken. "Stale, Misattributed, or Late" (arXiv:2610.10265, 2026) measures
failures occurring before generation, reports 70.3% of prompts exposing a superseded value without
update resolution, and adds two causes we had not considered: misattribution to the wrong person, and
lateness.

The benchmark layer is crowded: STALE (arXiv:2605.06527, 2026), 400 expert-validated conflict
scenarios and 1,200 queries over contexts up to 150K tokens, best model 55.2%; MoM (arXiv:2609.25054,
2026), stale-answer rate 19.4%→10.9%; RD-Forget (arXiv:2609.10263, 2026), separating what is stored
from what is used because a superseded fact can still be needed for a historical query; and retrieval
admissibility (arXiv:2610.07309, 2026), three statuses at matched required-evidence recall.

**Verdict: ALREADY DONE.** Metric, split, pre-generation measurement and the stale-versus-missing
ladder all have 2026 papers. What survives is a replication on a different memory stack — an
engineering note, not a paper.

### Closest prior work, Family B

| # | Paper (year, arXiv) | Why it is close | Verdict |
|---|---|---|---|
| B1 | When Retrieval Is Not Enough: Obsolete Facts in Agent Memory (2026, 2610.36308) | Separates "missed the update" from "had it and didn't use it"; 100%→44.6% | SAME IDEA |
| B2 | Temporal Validity in Retrieval Memory (2026, 2606.26511) | Defines the stale-fact-error rate (15–40%); cosine AUROC 0.59 contradicted vs duplicate | SAME IDEA |
| B3 | Stale, Misattributed, or Late: Where Personal Memory Fails Before Generation (2026, 2610.10265) | Measures stale exposure pre-generation; 70.3% of prompts | SAME IDEA |
| B4 | STALE: Can LLM Agents Know When Their Memories Are No Longer Valid? (2026, 2605.06527) | 400 scenarios, 1,200 queries, best model 55.2%; premise resistance | CLOSE |
| B5 | MoM: Memory of Memory (2026, 2609.25054) | Stale-answer rate 19.4%→10.9%; supersession with provenance | CLOSE |
| B6 | What Should an Agent Forget? Separating What Is Stored from What Is Used (2026, 2609.10263) | Same split, framed as storage vs use | CLOSE |
| B7 | The Right Memory in the Wrong Context (2026, 2610.07309) | Three-status admissibility at matched recall | ADJACENT |
| B8 | ConflictBank (2024, 2408.12076) | Knowledge-conflict benchmark preceding the 2026 wave | ADJACENT |

---

## 3. Family C — abstention and calibration in Hindi/Hinglish: **CROWDED, AND THE CLAIM IS PREDICTABLE**

The proposal: does an English-calibrated abstention gate transfer to Hindi/Hinglish, with a
cross-lingual hardness ladder, both directions reported.

The transfer question is answered. "Teaching LLMs to Abstain across Languages via Multilingual
Feedback" (arXiv:2406.15948, 2024) starts from the same premise — abstention work is English-centric
and applying English solutions elsewhere leaves up to a 20.5% gap between high- and low-resource
languages, attributed to calibration and reasoning degradation — and proposes a multilingual-feedback
fix worth up to 9.2% on low-resource languages across three datasets. A 2026 paper supplies the
mechanism: "Estimating Uncertainty from Reasoning" (arXiv:2607.06327, 2026) evaluates nine uncertainty
methods across 22 languages and finds that reasoning in English while keeping the question in a
low-resource language substantially improves uncertainty estimation and closes most of the gap —
comprehension survives, generation is the bottleneck. Our headline result ("English-calibrated
abstention degrades in Hindi, by this much") is therefore in print with a mechanism attached.

Calibration is covered too. arXiv:2311.08669 (2023) benchmarks calibration across encoder-only,
encoder-decoder and decoder-only models from 110M to 7B in-distribution, out-of-distribution and
cross-lingual transfer, including post-hoc fixes. Cross-lingual probe transfer is measured in
arXiv:2610.06216 (2026): English-trained probes keep discrimination but lose calibration, and pooled
multilingual supervision restores both. Cross-lingual consensus as an abstention signal is
arXiv:2503.23687 (2025), with +71.2% on Bengali and +15.5% even on English. Multilingual refusal
alignment has its own dataset (RefusEU, 12 European languages, arXiv:2606.07535, 2026) and its own
finding that English-only alignment does not transfer.

**What is left, narrowly.** Code-mixing. Every paper above treats languages as separate monolingual
inputs; none measures a gate on romanized Hindi-English mixing, where scripts change mid-utterance and
tokenizer behaviour changes with them. The Devanagari-versus-romanized contrast on the *same* items is
also unmeasured, and it is the one manipulation separating "the model does not know" from "the model
cannot read this orthography".

**Why I would still not pick it.** arXiv:2607.06327 makes our result predictable: if reasoning language
dominates question language, a Hinglish gate behaves like a Hindi gate plus tokenization noise, and the
paper becomes "we confirm a 2026 result in a new orthography". It is also the most expensive family for
a CPU-only lab — a four-rung Hinglish ladder with human-checked false premises is a week of annotation.

**Slice that remains open:** whether a gate fitted on Devanagari Hindi transfers to romanized Hinglish
for the same items — orthography transfer, not language transfer.

### Closest prior work, Family C

| # | Paper (year, arXiv) | Why it is close | Verdict |
|---|---|---|---|
| C1 | Teaching LLMs to Abstain across Languages via Multilingual Feedback (2024, 2406.15948) | English abstention does not transfer; 20.5% gap; fix worth 9.2% | SAME IDEA |
| C2 | Estimating Uncertainty from Reasoning: Multi- and Crosslingual MCQA (2026, 2607.06327) | Nine UE methods, 22 languages; English reasoning closes the gap — predicts our result | CLOSE |
| C3 | On the Calibration of Multilingual Question Answering LLMs (2023, 2311.08669) | Calibration under cross-lingual transfer, 110M–7B, with post-hoc fixes | CLOSE |
| C4 | Cross-lingual Calibration of Pre-Generation Success Probes (2026, 2610.06216) | English-trained probes lose calibration after transfer; pooled restores it | CLOSE |
| C5 | MKA: Leveraging Cross-Lingual Consensus for Model Abstention (2025, 2503.23687) | Cross-lingual consensus as an abstention signal; +71.2% Bengali | ADJACENT |
| C6 | Multilingual Refusal Alignment for Safer LLMs (2026, 2606.07535) | RefusEU, 12 languages; English-only alignment insufficient | ADJACENT |
| C7 | Multilingual Hallucination Gaps in LLMs (2024, 2410.18270) | 19 languages, FactScore-based hallucination gap | ADJACENT |
| C8 | XTRUST: Multilingual Trustworthiness of LLMs (2024, 2409.15762) | 10-language trustworthiness incl. hallucination and OOD | UNRELATED to abstention |

---

## 4. Family D — scam detection under realistic prevalence and paraphrase attack: **CROWDED BUT A SLICE IS OPEN**

The proposal: performance at sub-1% base rates, degradation under LLM paraphrasing, cost-sensitive
threshold calibration, on public SMS/phishing corpora with a documented synthetic paraphrasing
procedure.

Paraphrase robustness is the saturated part. "Johnny Still Receives Spam SMS" (arXiv:2609.01171,
2026) evaluates the detectors people actually use — commercial messaging apps, third-party anti-spam
services, open-weight models — under perceptible and imperceptible perturbations verified to survive
real SMS/RCS delivery, and finds robustness transfers within a perturbation family but degrades sharply
against structurally distinct encoding-level attacks, with adversarial training insufficient alone.
That is a stronger version of our experiment, run against deployed systems. Earlier work released
153,551 SMS messages and measured adversarial robustness across shallow, deep and feature-based models
(arXiv:2210.10451, 2022); fine-tuned LLMs reach 98.6% accuracy with balanced FPR/FNR below 2%
(arXiv:2501.04985, 2025); and a 4.5M-parameter distilled model trained on a hybrid human-plus-LLM-
paraphrase set is evaluated under five protocols including two cross-distribution transfers and a
production-like mixed-traffic test (arXiv:2602.22250, 2026). A documented synthetic paraphrasing
procedure is standard practice.

Prevalence is not saturated for this domain, but the method is. arXiv:2610.41803 (2026) audits eleven
detector evaluations, finds attacks make up 16%–86% of test samples with no evaluation varying that
share, and shows what this hides: at a 2% attack rate, AUROC 0.879 yields precision 0.076, and the
composition of negatives alone moves precision between 0.039 and 0.117. PIDS-Bench (2026, IEEE Access,
DOI 10.1109/access.2026.3728186) makes the benign-side version for prompt-injection detectors: a
detector above F1 0.98 in-distribution still fails once false positives at fixed thresholds are measured
under obfuscation and shift.

**What is left.** Nobody here reports precision, recall and alert volume for SMS/smishing detection at
a base rate below 1%, with the threshold chosen from an explicit cost ratio rather than F1, on an Indian
or code-mixed corpus. The corpus matters: English UCI-SMS-style messages do not contain "aapka KYC
expire ho gaya hai" constructions, and the shortcut features a detector learns (URL presence, sender ID
format) do not transfer to them.

**Slice that remains open:** the operating-point table — precision, recall and alerts per 10,000
messages for a small CPU-runnable SMS scam detector at 0.1%–1% prevalence, threshold set from a stated
cost ratio, corpus code-mixed Indian English.

**Honest risk.** This transfers a known measurement to a new domain: publishable at a student track,
not a new idea. The compensating asset is real — TrustShield exists, the student has domain knowledge,
and the table is cheap. Lowest-variance path to a defensible paper, provided the framing is "operating
points for a deployed-class detector", not "we discover that base rates matter".

### Closest prior work, Family D

| # | Paper (year, arXiv/DOI) | Why it is close | Verdict |
|---|---|---|---|
| D1 | Johnny Still Receives Spam SMS: Assessing the Robustness of SMS Spam Detection (2026, 2609.01171) | Paraphrase/perturbation of deployed SMS detectors, held-out protocol, delivery-verified attacks | CLOSE |
| D2 | What Standard Evaluations Hide About Detectors of Hijacked LLM Agents (2026, 2610.41803) | The prevalence result: AUROC 0.879 → precision 0.076 at 2% | SAME IDEA (different domain) |
| D3 | A Lightweight Defense Mechanism against Next-Generation Phishing Emails (2026, 2602.22250) | LLM-paraphrase hybrid training set, production-like mixed traffic, cross-distribution tests | CLOSE |
| D4 | An Empirical Analysis of SMS Scam Detection Systems (2022, 2210.10451) | 153,551-message corpus plus adversarial manipulation | CLOSE |
| D5 | SpaLLM-Guard (2025, 2501.04985) | Fine-tuned LLM, 98.6% accuracy, FPR/FNR <2%, adversarial resilience | ADJACENT |
| D6 | POSTER: A Multi-Signal Model for Detecting Evasive Smishing (2025, 2505.18233) | 84K messages, 24K smishing, AUC 99.73% — in-distribution ceiling | ADJACENT |
| D7 | PIDS-Bench: Detectors Under Over-Defense, Obfuscation, Distribution Shift (2026, IEEE Access) | Benign-side false positives at fixed thresholds; F1 0.98 detector still fails | ADJACENT |
| D8 | Attacking Only Half the Data: Two-Sided Evaluation of Detector Robustness (2026, 2610.18151) | Two-sided attack protocol; AUROC gains vanish when human text is perturbed | ADJACENT |

---

## 5. Cross-family read

Ranked by (chance of surviving review) × (chance the lab finishes):

1. **Family D** — the slice is a table, the table is cheap, the domain asset is real. Weakest novelty,
   strongest executability. Frame as operating points, not discovery.
2. **Family A** — the honest fit to the student's own measured failure, and the slice is unoccupied.
   Highest variance: the delta over RINSE is small and a reviewer may call it incremental.
3. **Family C** — a real gap in orthography transfer, but the result is predictable from a 2026 paper
   and the data construction is expensive. Only if a Hinglish corpus can be sourced, not built.
4. **Family B** — do not start.

Two constraints apply to whichever is chosen. All four are crowded, so the paper cannot be sold as
"first to study X"; it must be sold as a specific measurement with a number in the abstract. And this
scan is arXiv-only: before the final novelty check, someone must re-run these 91 queries against
OpenAlex after the daily budget resets (00:00 UTC) or with an activated key, because venue-only ACL
papers are invisible here and the closest prior work in an abstention paper is often an ACL long paper.

---

## 6. Papers that look like they ARE our idea — flagged

Each is flagged with the specific measurement we planned that it already reports.

1. **When Retrieval Is Not Enough: Obsolete Facts in Agent Memory (2026, arXiv:2610.36308).** Measures
   the memory-miss versus memory-wrong split directly and shows retrieved-but-obsolete is the dominant
   failure (100%→44.6%). Family B's core contribution.
2. **Temporal Validity in Retrieval Memory (2026, arXiv:2606.26511).** Defines the stale-fact-error
   rate — the answer-level version of our stale-hit rate — and reports 15–40% for RAG. Family B's
   headline metric.
3. **Stale, Misattributed, or Late (2026, arXiv:2610.10265).** Measures staleness before generation
   rather than in the final answer — the stricter version of what we proposed — and adds
   misattribution as a third cause.
4. **Prompt-Based Abstention Fails Under Misleading Context (2026, arXiv:2608.22228).** Its four
   context conditions are our four-rung ladder, with the over-answer rate (41.6%) on the hardest rung.
   Family A's ladder.
5. **DeclineCraft (2026, arXiv:2610.28340).** Reports abstention on unanswerable items and answerable
   attempt rate together, across 27 models. Family A's "both directions".
6. **Teaching LLMs to Abstain across Languages (2024, arXiv:2406.15948).** Measures whether English
   abstention transfers to lower-resource languages and puts a number on the gap (20.5%). Family C's
   central question.
7. **What Standard Evaluations Hide About Detectors of Hijacked LLM Agents (2026, arXiv:2610.41803).**
   Reports the precision collapse at low prevalence (AUROC 0.879 → precision 0.076 at 2%) and shows
   the negative mix alone moves precision 3×. Family D's method, on another detector class.

None is a complete match to a family as worded, but four of them (1, 2, 4, 6) are close enough that the
family would have to be re-scoped before any experiment starts.

---

## 7. Audit table — all 91 queries

Counts are the tool's `-- N results` line, verbatim. `10 (cap)` means the `--limit 10` ceiling was hit,
so the true count is ≥10. `0` means arXiv returned no record whose title or abstract contains the query
as a phrase (§0, Limit 2). Source is arXiv for every row because OpenAlex returned HTTP 429 all window
(§0, Limit 1). Three queries failed with a 429 mid-run and were re-run successfully; only successful
counts appear.

