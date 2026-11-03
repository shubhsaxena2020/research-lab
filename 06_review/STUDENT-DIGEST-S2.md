# STUDENT DIGEST — S2 (one page)

## The field, quickly
The corner of AI research this lab enters is not "build a bigger model". It is "decide when a system
should keep its mouth shut". A system answering from documents is sometimes handed documents that do not
contain the answer. It can answer anyway (hallucinate) or refuse. Refusing wrongly is also a failure: a
system that says "I don't know" to everything is useless, and one that refuses what it could have answered
is worse, because it hides its competence. Researchers call this **abstention**. The gate can live in the
prompt ("if unsure, say so") or in a separate classifier that reads signals. Prompt-side gating is known to
fail in both directions; classifier-side gating works better but is almost always evaluated on one kind of
trick question.

## The one finding that made this topic
In 2024 a team trained a classifier to spot when a retrieved passage does not answer the question. On
randomly chosen wrong passages it scored **98%**. On wrong passages that shared vocabulary with the
question it scored **1%**. Same model, same questions — only the choice of wrong passage changed. That is a
97-point drop caused entirely by how the test was built, and almost every abstention paper since reports one
kind of wrong passage and generalises.

Your own memory system hit a version of this: its gate over-refused because a single threshold sat outside
the range of scores the system actually produced. That is an anecdote from a private evaluation you cannot
publish and must not quote numbers from — but it is exactly why this paper reports *where* the thresholds sit
relative to the scores actually observed.

## The paper you are going to write
One small model (1.5B, runs on your laptop), a fixed pile of Wikipedia paragraphs, 3,200 questions: 800
answerable and 800 in each of four trap types — a random wrong paragraph, one about the same person, the
paragraph next to the correct one, and a paragraph where the answer has been swapped for a wrong value so
the text is confidently false.

Build a gate from six cheap retrieval signals only (how well the top passage matches, whether keyword and
embedding search agree, rerank score), fit two thresholds on half the data, test on the other half. Does
precision survive as traps harden, and do the thresholds still work on a different dataset? Whatever
happens is a result, including a null.

## Why not the obvious alternatives
- Not "better agent memory": three 2026 papers already did the exact experiment we planned — our novelty
  scan caught that on day one, which is why we dropped it.
- Not "Hindi abstention": a 2026 paper measured the English-to-Hindi gap, another explained it.
- Not "scam detection": strong fallback if day 3 goes wrong, but its headline claim (low base rates destroy
  precision) is already published in another domain.

## Read first, in this order
1. SQuAD 2.0 (arXiv:1806.03822) — where "unanswerable" became a standard task.
2. Answerability in Retrieval-Augmented Open-Domain QA (arXiv:2403.01461) — the 98%→1% result. Read twice;
   it is why the paper exists.
3. Two Axes of LLM Abstention (arXiv:2607.08456) — "is it correct" and "is it answerable" are different
   questions.
4. Relevance Is Not Sufficient Evidence (arXiv:2609.37469) — closest prior work; know what it does that we
   do not.
5. AbstentionBench (arXiv:2506.09038) — how badly models do this at frontier scale.

## Five questions a reviewer will ask, and the honest answers
1. *Isn't this known?* The 98%→1% effect is known. A designed ladder with a two-threshold gate and a
   false-refusal column is not published in our sweep — but it is incremental. Say that word.
2. *Why 1.5B?* That is what runs on the laptop, and the claim is about the gate, not the model. We check a
   strong model on 400 items.
3. *Aren't your traps trivially detectable?* We test it: a surface-feature classifier must stay under 0.75
   AUROC per rung, or the rung is rebuilt.
4. *What is it good for?* A gate you can fit on one dataset and deploy on another, with a measured cost for
   transferring.
5. *What would prove you wrong?* Flat precision across rungs (H1), transfer within ±5 points (H2), or no
   gain from two thresholds (H3). All three are pre-stated.

## Defend line by line
The rung definitions, why passage lengths are matched, why the audit threshold is 0.75, what abstain
precision means as a fraction, why the bootstrap is paired, and why the frozen-transfer number is the one
H2 is about. If any is fuzzy, fix it before submission.
