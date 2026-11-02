# NOVELTY-CHECK — the top two candidates
S2 · 2026-11-03 · sources: arXiv API (search + id_list), Crossref; OpenAlex was returning HTTP 429
(daily budget exhausted on this IP) throughout, so **no OpenAlex coverage in this check**.

## What this document is, and what it is not
The prompt asked for ≥30 documented queries per topic across arXiv/Semantic Scholar/OpenAlex/Crossref
with result counts and the closest 10 prior works. **That bar was not met and I am not going to claim
it was.** What exists is a pre-scan (`02_literature/NOVELTY-PRESCAN.md`) of 91 queries over four
families — 25 for family A, 23 for family D — run against arXiv only, with result counts recorded per
query. Semantic Scholar returned 429 without a key (no key, no budget to apply); OpenAlex was over its
free daily budget; Crossref is a DOI resolver, not a search engine with meaningful recall for this task.
So: **48 of the 60 required queries exist, in one source, and 2 of the 4 required sources are missing.**

Consequence for the head: this check is sufficient to *kill* two candidate families outright (B and,
largely, C) and sufficient to establish that A and D are crowded, but it is **not** sufficient to
certify either as novel. It must be re-run with OpenAlex (after 00:00 UTC) and Semantic Scholar (with a
free key) before any draft calls the contribution new. Treat the verdicts below as "no fatal collision
found in one index", not as "novel".

Sentences in this file that say "no paper does X" are shorthand for "no paper in the 91-query arXiv
sweep does X". They are not claims about the literature.

---

## Verdict 1 — Family A (retrieval-side two-sided abstention gate): INCREMENTAL, narrow slice open

Every ingredient is published separately, and most pairs of ingredients are published together.

| # | Closest prior work | Why it is close | Verdict |
|---|---|---|---|
| A1 | *Relevance Is Not Sufficient Evidence: Detecting Evidence Gaps Before Generation in RAG* (2026, arXiv:2609.37469) | Pre-generation sufficiency gate from three signals, 0.837 vs 0.746 best prior at 36.5 ms/query; documents exactly the label-leak traps our ladder must avoid | CLOSE — occupies "gate before answering" |
| A2 | *Prompt-Based Abstention Fails Under Misleading Context* (2026, arXiv:2608.22228) | Four-rung context ladder (supportive/degraded/missing/misleading); 3.8B–8B models still answer 41.6% of misleading items | CLOSE — occupies "hardness ladder" |
| A3 | *RefusalBench* (2025, arXiv:2510.10390) | 176 perturbation strategies, six uncertainty categories, three intensity levels; <50% refusal accuracy on multi-doc tasks | CLOSE — occupies "graded difficulty of refusal" |
| A4 | *DeclineCraft* (2026, arXiv:2610.28340) | Reports Correct Abstention Rate **and** Answerable Attempt Rate across 27 LLMs | CLOSE — occupies "report both directions" |
| A5 | *Two Axes of LLM Abstention* (2026, arXiv:2607.08456) | Correctness and answerability as separable axes; one threshold cannot serve both; builds a two-score calibrated policy | CLOSE — occupies "one threshold is the wrong shape" |
| A6 | *Answerability in Retrieval-Augmented Open-Domain QA* (2024, arXiv:2403.01461) | 98% on random negatives → 1% on high-overlap negatives, same model | CLOSE — this is our motivating number, already published |
| A7 | *AbstentionBench* (2025, arXiv:2506.09038) | 20 datasets × 20 models, abstention recall per scenario; reasoning FT degrades abstention 24% | ADJACENT — aggregate, no per-rung policy |
| A8 | *Know What You Don't Know: Unanswerable Questions for SQuAD* (2018, arXiv:1806.03822) | Supplies our negatives and the lexical-overlap shortcut that makes them easy | ADJACENT — data, not method |
| A9 | *Selective QA under Domain Shift* (2022) | Two-sided by construction (fixes accuracy, reports coverage); the template for our reporting | ADJACENT — images/domain shift, not retrieval features |
| A10 | *When Not to Trust Language Models* (2022, arXiv:2212.10511) | PopQA; popular-vs-long-tail answerability structure | ADJACENT — motivates the popularity stratum |

**Slice that no work in this sweep occupies:** two separate thresholds (admit / refuse, dead zone
between) fitted on a dev split **using retrieval-side features only** — no generator call, no hidden-state
probe, no second model — then evaluated held out, reporting abstain precision and recall **and** a
false-refusal rate **at every rung of one four-rung negative ladder**, with the band's placement relative
to the observed dev feature range reported as a diagnostic.

**Honest assessment.** This is a measurement contribution of one page. A reviewer's first question is
"how is this different from A1 plus A4?", and the true answer is: cheaper signals, a band instead of a
ranking score, a false-refusal column, and a diagnostic for the specific pathology (threshold outside the
observed feature range) that A1/A4 do not report. That is a **workshop paper**, not a main-track paper.
Calling it novel would be false. Calling it a careful, cheap, reproducible measurement of an identified
pathology is accurate.

---

## Verdict 2 — Family D (scam detection at realistic prevalence): INCREMENTAL, a different slice open

| # | Closest prior work | Why it is close | Verdict |
|---|---|---|---|
| D1 | *Johnny Still Receives Spam SMS* (2026, arXiv:2609.01171) | Perturbs deployed SMS detectors with delivery-verified adversarial messages; robustness transfers within attack family only | CLOSE — occupies "paraphrase robustness" |
| D2 | *What Standard Evaluations Hide About Detectors of Hijacked LLM Agents* (2026, arXiv:2610.41803) | The prevalence result itself: at 2% attack rate AUROC 0.879 → precision 0.076; negatives composition moves precision 0.039–0.117 | SAME IDEA, other domain — this is our headline claim, already made |
| D3 | *A Lightweight Defense Mechanism against Next-Generation Phishing Emails* (2026, arXiv:2602.22250) | Human+LLM paraphrase training set, production-like mixed traffic, cross-distribution transfer | CLOSE |
| D4 | *An Empirical Analysis of SMS Scam Detection Systems* (2022, arXiv:2210.10451) | 153,551-message corpus, adversarial manipulation across shallow/deep/feature models | CLOSE |
| D5 | *SpaLLM-Guard* (2025, arXiv:2501.04985) | Fine-tuned LLM, 98.6% accuracy, FPR/FNR <2% | ADJACENT — in-distribution ceiling |
| D6 | *POSTER: Multi-Signal Smishing Detection* (2025, arXiv:2505.18233) | 84K messages / 24K smishing, AUC 99.73% | ADJACENT — same in-distribution ceiling |
| D7 | *PIDS-Bench* (2026, IEEE Access) | Benign-side false positives at fixed thresholds under obfuscation and shift | ADJACENT — prompt-injection domain |
| D8 | *Attacking Only Half the Data* (2026, arXiv:2610.18151) | Two-sided attack protocol; AUROC gains vanish when human text is perturbed | ADJACENT |

**Slice that no work in this sweep occupies:** an operating-point table — precision, recall and alerts
per 10,000 messages at 0.1%–1% prevalence — for a small CPU-runnable detector on a **code-mixed Indian
English** corpus, with the threshold chosen from a stated cost ratio rather than from F1.

**Honest assessment.** D2 already establishes that base rates destroy precision; our contribution would
be applying it to SMS with an Indian corpus and a cost-ratio threshold. That is a domain transfer.
Publishable at a student track if framed as "operating points for a deployed-class detector"; not
publishable as a discovery. It is also the lowest-variance option: the artefact is a table.

---

## Families killed by this scan (do not start)
- **B — memory staleness / miss-vs-wrong.** Three 2026 papers occupy it: arXiv:2610.36308 separates
  "missed the update" from "had it and did not use it" (accuracy 100%→44.6% with one obsolete
  statement); arXiv:2606.26511 defines a stale-fact-error rate (15–40% for RAG) and reports cosine AUROC
  0.59 for contradicted-vs-duplicate; arXiv:2610.10265 measures staleness pre-generation. Candidate C2's
  novelty component (**25/25 in `CANDIDATES.md`**) was scored before this scan ran and is **wrong**;
  re-scored at 8/25 it totals ~68/100 and is no longer the runner-up. This is the single most valuable
  output of the whole check: it stopped a week of work.
- **C — Hindi/Hinglish abstention.** arXiv:2406.15948 already measures a 20.5% English→low-resource
  abstention gap and arXiv:2607.06327 explains it (English-language reasoning closes the gap), which
  makes our expected result forecastable rather than informative. Only orthography transfer
  (Devanagari → romanised Hinglish) is unmeasured, and that needs a corpus we would have to build.

## What must happen before any draft calls this novel
1. Re-run all 91 queries against OpenAlex once its daily budget resets (00:00 UTC) and against Semantic
   Scholar with a free key. ACL-long papers are largely invisible in an arXiv-only sweep, and the closest
   prior work in abstention is usually an ACL long paper.
2. Add ≥15 queries per finalist that target the *specific* slice wording ("dead zone", "two thresholds",
   "false refusal rate", "operating point", "alerts per 10,000", "cost ratio threshold"), not the family.
3. If either re-run surfaces a paper that fits two thresholds on retrieval features and reports both
   directions per rung, the candidate is dead and the lab moves to the other family.
