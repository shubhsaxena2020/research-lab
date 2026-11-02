# STUDENT DIGEST — S2 (one page, plain language)

## The field, quickly
The part of AI research this lab is entering is not "make a bigger model". It is "work out when a model
should keep its mouth shut". A system that answers from documents will sometimes be handed documents that
do not contain the answer. Two behaviours are possible: answer anyway (hallucinate) or refuse. Refusing
wrongly is also a failure — a system that says "I don't know" to everything is useless, and a system that
refuses the questions it could have answered is worse than useless because it hides its competence.

Researchers call this **abstention**. The gate that decides is either in the prompt ("if you are not sure,
say so") or in a separate classifier that reads signals and decides. Prompt-side gating is known to fail:
models refuse things they know and answer things they do not. Classifier-side gating works better but is
evaluated almost always on one kind of trick question.

## The one finding that made this topic
In 2024 a team trained a classifier to spot when a retrieved passage does not answer the question. On
randomly chosen wrong passages it scored **98%**. On wrong passages that shared vocabulary with the
question it scored **1%**. Same model, same questions — only the choice of wrong passage changed. That is
a 97-point drop caused entirely by how the test was built. Almost every abstention paper since reports one
kind of wrong passage and generalises.

Your own memory system did the same thing in a different way: its gate refused 47 of 82 questions it could
have answered, because the threshold was set outside the range of scores the system actually produced. You
measured that. Nobody in the literature writes about that specific failure, and it has a simple repair: use
two thresholds (one to answer confidently, one to refuse confidently, a gap in between) and *report where
they sit relative to the scores you actually observed*.

## The paper you are going to write
One small model (1.5B, runs on your laptop), a fixed pile of Wikipedia paragraphs, and 3,200 questions:
800 answerable, and 800 in each of four kinds of trap — a random wrong paragraph, a paragraph about the
same person, the paragraph right next to the correct one, and a paragraph where the answer has been
swapped for a wrong value so the text is confidently false.

Then build a gate from cheap retrieval signals only (how well the top passage matches, whether keyword and
embedding search agree, etc.), fit two thresholds on half the data, and test on the other half. The
question is whether the gate's precision survives as the traps get harder, and whether the thresholds still
work on a different dataset.

Whatever happens is a result. If precision collapses as traps harden, that quantifies a known suspicion for
the first time at small scale. If it holds, that is good news and also a result. If the two-threshold gate
is no better than one threshold, that is a negative result and we publish it as one.

## Why this and not the obvious alternatives
- Not "build a better agent memory" — three papers in 2026 already did the exact experiment we had planned
  (that is what our novelty scan caught on day one, which is why we are not doing it).
- Not "Hindi abstention" — a 2026 paper already measured the English-to-Hindi gap and a second explained it.
- Not "scam detection" — strong second choice, and we keep it as the fallback if day 3 goes wrong, but its
  headline claim (low base rates destroy precision) is already published in another domain.

## What to read first, in this order
1. `SQuAD 2.0` paper (arXiv:1806.03822) — where "unanswerable" questions became a standard task.
2. `Answerability in Retrieval-Augmented Open-Domain QA` (arXiv:2403.01461) — the 98%→1% result. Read this
   one twice; it is the reason the paper exists.
3. `Two Axes of LLM Abstention` (arXiv:2607.08456) — why "is it correct" and "is it answerable" are
   different questions.
4. `Relevance Is Not Sufficient Evidence` (arXiv:2609.37469) — the closest prior work; know exactly what it
   does that we do not, so you can answer the reviewer who says we copied it.
5. `AbstentionBench` (arXiv:2506.09038) — the big picture of how badly models do this.

## Five questions a reviewer will ask you, and the honest answers
1. *Isn't this already known?* The 98%→1% result is known. Turning it into a designed ladder with a
   two-threshold gate and a false-refusal column is not published in our sweep, but it is incremental work.
   Say that.
2. *Why only 1.5B?* Because that is what runs on the laptop, and because the claim is about the gate, not
   the model. We check whether it changes on a strong model with 400 items.
3. *How do you know your traps aren't trivially detectable?* We test that explicitly: a classifier using
   only surface features must stay below 0.75 AUROC per rung, otherwise we rebuild the rung.
4. *What is the practical value?* A gate you can fit on one dataset and deploy on another, with a number
   telling you how much you lose when you do.
5. *What would prove you wrong?* A flat precision curve across rungs (H1), transfer within ±5 points (H2),
   or no gain from two thresholds (H3). All three are pre-stated.

## What you must be able to defend line by line
The negative construction (rung 1–4 definitions), why passage length is matched, why the audit threshold is
0.75, what abstain precision means as a fraction, why the bootstrap is paired, and why the frozen-transfer
number is the one the hypothesis is about. If any of those five is fuzzy, fix it before submission.
