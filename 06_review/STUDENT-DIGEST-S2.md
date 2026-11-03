# STUDENT DIGEST — S2 + S2b (one page)

**The field.** A system that answers from documents is sometimes handed passages that do not contain the
answer. It can answer anyway (hallucinate) or refuse. Refusing wrongly is also a failure — a system that
says "I don't know" to everything is useless, and one that refuses what it could have answered hides its
competence. Researchers call this **abstention**. Prompt-side gating ("if unsure, say so") fails in both
directions; classifier-side gating works better but is almost always evaluated on one kind of trick
question.

**Why this topic.** In 2024 a team trained a classifier to spot when a retrieved passage does not answer
the question. On random wrong passages it scored **98%**; on wrong passages sharing vocabulary with the
question, **1%**. Same model, only the choice of wrong passage changed (arXiv:2403.01461). Your own build
failed the same way in miniature: its gate over-refused because one threshold sat outside the range of
scores the system actually produced. You cannot publish that evaluation or quote numbers from it — it is
one sentence of motivation at most — but it is why this paper reports *where* the thresholds sit relative
to the scores actually observed. No paper found in either index reports that placement.

**The paper.** One 1.5B reader, one paragraph corpus, 3,200 questions: 800 answerable plus 800 in each of
four trap types (random wrong paragraph; same-entity; the paragraph next to the correct one; a paragraph
with the answer swapped for a wrong value). Gate built from six cheap retrieval signals only (top-1 and
top-5 BM25, top-1 and top-5 dense cosine, BM25/dense agreement, rerank score) — no generator call. Two
thresholds fitted on half the data, tested on the other half, per rung, reporting abstain precision,
abstain recall and false-refusal rate. Then the frozen band on a second corpus.

**What this morning's second sweep changed.** The first check saw arXiv only. The second added OpenAlex —
3,681 more abstracts from 84 queries — and found no paper doing your experiment, but three neighbours to
cite by name:

- A 2025 paper already builds a **two-threshold** abstention framework (conformal + abstention threshold,
  arXiv:2502.07255). Perception, not retrieval, but "two thresholds" is not ours to call new.
- A 2026 paper already abstains from **retrieval features alone with no model call** and breaks results
  down by failure type (arXiv:2609.22056). No ladder, no dead zone, no false-refusal column.
- A 2026 paper already reports **wrongful refusal of sufficient context (7.0%)**
  (doi:10.32604/cmc.2026.088937). Over-refusal is published as a single number; yours must be per rung.

What survives all three: two dev-fitted thresholds on retrieval features, held out at every rung of one
negative-hardness ladder, reporting both directions per rung, plus the band's position against the dev
feature range. Narrow, finishable, checkable — and explicitly **incremental**. Say that word.

A sweep of all 3,681 abstracts found **zero** uses of "dead zone", "abstain precision", "negative hardness"
or "per rung". That does not prove the idea is free; it does mean you must define your terms, because
nobody will find you by searching for them.

**Limits of the check.** Semantic Scholar refused (rate limit, no key), so this is two indexes, not four.
OpenAlex's "free" tier turned out to be metered: ~100 searches/day for the whole network address, and we
spent 84. A free key needs your email — your call, not the lab's.

**Why not the alternatives.** Memory staleness: three 2026 papers did the exact experiment. Hindi
abstention: one paper measured the English→Hindi gap, another explained it. Scam detection: the fallback,
now weaker than it looked — its "no Indian code-mixed corpus" claim is false (a 2026 paper has 5,200
Hinglish messages, another already publishes an Indian-SMS false-positive rate), so it would claim only
the operating-point table.

**Read first, in order.** (1) Answerability in Retrieval-Augmented Open-Domain QA (arXiv:2403.01461) — the
98%→1% result; read twice. (2) Relevance Is Not Sufficient Evidence (arXiv:2609.37469) — closest gate
paper. (3) Predictable Failure in Multi-Hop Retrieval (arXiv:2609.22056) — closest method. (4) Beyond
Confidence: Dual-Threshold Conformal Prediction (arXiv:2502.07255) — the two-threshold idea. (5) Before
Answering (arXiv:2609.32269) — why building hard negatives is a trap; your audit's justification.

**Five reviewer questions.** *Isn't this known?* The 98%→1% effect and the two-threshold construct are;
the ladder plus per-rung false refusals is not in either index. It is incremental. *Why 1.5B?* It is what
runs on the laptop; the claim is about the gate. *Aren't the traps trivially detectable?* We test it —
surface-only AUROC must stay under 0.75 per rung or the rung is rebuilt (a 2026 paper shows this trap at
0.979). *What is it good for?* A gate fit on one corpus and deployed on another, with the transfer cost
measured. *What proves you wrong?* Flat precision across rungs, transfer within ±5 points, or no gain from
two thresholds — all three pre-stated.
