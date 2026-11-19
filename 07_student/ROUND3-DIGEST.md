# Round 3: the three new post-hoc analyses, in plain English

> **Read this first.** The three new analyses below are all **exploratory / post-hoc** — worked out *after* the results were known (N5).
> None of them is in the draft yet (N6), and none changes a frozen verdict (N5).
> Always quote the label with the number: post-hoc, not human gold.

> **Where the numbers come from.** Every number carries an ID like (C01), and `07_student/SOURCE-MAP.md` gives the exact file, JSON key and stored value behind each ID. If a number is not in that table, it does not belong here.

## What Round 3 is

Round 3 is the repair round. A simulated peer review produced 44 must-fix items (N8), and each now has one lane to answer it — with evidence, or a narrower claim. The framing stays honest: when data do not support a claim, the claim gets smaller.

A few words first. A **negative** is a retrieval item that does not contain the answer, so the gate should refuse it. An **abstention gate** is a small rule deciding, before answering, whether to answer or refuse ("abstain"), using only retrieval-side signals. A **rung** is one difficulty level of negatives, easy to hard, R1 to R4. **Abstain precision** is: among refused items, the share that really were negatives. A **threshold** is one cut-off value. The **operating point** is the cut-off — or pair of cut-offs — that decides answer-or-refuse, and a **band** is the two-threshold form of that rule: answer inside the middle range, refuse outside it. **Dev** is the half the cut-offs were fitted on; **held-out** is the untouched half they were never fitted on. A **discordant pair** is a pair of items where the two things being compared disagree — with none, a paired test has nothing to do.

## The three new post-hoc analyses

### 1. Kappa: do two LLM labellers agree? (MF-10)

**The question.** The 100 seeded negatives (C02) may not all be unanswerable. Two independent large-language-model labellers, A and B, judged them; a stricter pass settled ties.

**What kappa means.** Cohen's kappa measures agreement **beyond chance**, after subtracting what two raters would get by luck. One is perfect; zero is chance level.

**The result.** Kappa was 0.2802 (C01). Raw agreement was 0.59 (C02): 59 of the 100 items, so 41 were contested (C04). Labeller A called 62 answerable and labeller B 21 (C05). On the 41 contested items (C04), the strict resolver chose answerable 35 times and not-answerable 6, with 0 ambiguous (C06). The resolved label marks 56 of the 100 answerable, which is 0.56, or 56% (C07).

**How to read it.** 0.2802 (C01) is **modest agreement beyond chance between these two LLM labellers**. It is not accuracy, not human agreement, not proof the labels are true. Chance agreement implied by their own counts is about 0.43 (C03, **derived from C01 and C02**), which is why raw agreement of 0.59 (C02) still leaves kappa small.

**Not human gold.** These are model judgements (N5): nothing says the negatives are wrong — only that the models disagreed about some.

### 2. AUROC intervals: how precise, and is the gap real? (MF-17)

**What an AUROC is.** A ranking score: the chance the gate scores an answerable item above a negative. It is **threshold-free** (it never asks where the cut-off sits) and **not an accuracy**: it does not say how many questions the gate answers.

**What a bootstrap interval is.** A range of plausible values for the true score, from resampling many times.

**The result.** The frozen run's held-out AUROC, recomputed post-hoc with no model retrained, is 0.9824 (C10), 95% interval 0.9776 to 0.9867 (C10). The spec-corrected run's is 0.8738 (C11), 95% interval 0.8587 to 0.8893 (C11). The paired difference (frozen minus corrected) is 0.1085 (C12), 95% interval 0.0946 to 0.1225 (C12), which excludes zero — so sampling noise alone does not explain the gap (C12).

**What was counted.** 1,879 held-out items (C13): 400 answerable at rung 0 plus 1,479 negatives across rungs 1 to 4, 18 article clusters, 10,000 resamples, seed 20261118 (C13). No model was retrained (N7).

### 3. The gold-indicator control and D3 (MF-7)

**The worry.** Answerable items always present the gold paragraph; negatives never do — so the gate might detect the gold paragraph, not answerability.

**The gold-indicator result is a tautology.** Add that flag and AUROC becomes 1.0 (C15); the flag alone, oriented so answerable scores higher, is also 1.0 (C16). A perfect score looks like success, but it is **tautological**: the flag is a deterministic function of the label (C16). Restating the answer key, it cannot fail — so it cannot show the gate works (N7).

**The honest comparison.** Without the flag, the same lexical (surface-word) features reach 0.9762 on dev rung 1 (C14) — the number worth reading.

**D3.** D3 presents the retriever's top-ranked passage to every question and records a hit or miss: 655 hits, 145 misses, 800 observations (C17), separated at AUROC 0.7327 (C17). **D3 is pooled only, at rung = −1** (C19); no per-rung R1–R3 estimate exists (C19).

## What these results can and cannot mean

- **Exploratory / post-hoc, all three** (N5), computed after the results were seen.
- **Not in the draft yet** (N6); **no frozen verdict is revised** (N5).
- **Not human gold; kappa is agreement, not correctness** (N5, C01).
- **AUROC is threshold-free, not an accuracy** (C23, C10); the gold-indicator 1.0 is a construction artefact (C16, N7).
- **D3 is pooled only** (C19).

## H1 and MF-14: the two caveats you must get right

### H1 was **not exercisable** — say exactly that

H1 was the registered test that abstain precision does not improve as negatives get harder: never increasing across rungs 1 to 4, with at least a 15-point drop from rung 1 to rung 3 (N1). It could not run at the registered point: the gate refused almost everything, with 92.9% of dev items below the lower cut-off on its own (N2). Precision then sat at 1.00 in every rung (N2), and the rung-1 minus rung-3 comparison had no discordant pairs (N4). Nothing varied, so nothing could be compared.

So: **H1 was not exercisable at the registered operating point.** Not "confirmed", and not "refuted" — not even if an exploratory ordering looks like a trend: an exploratory arm cannot rescue a hypothesis (N3).

### MF-14: three numbers, always with their run labels

| Number | What it is |
|---|---|
| 100.00% (C20) | registered band, **frozen**, D1 |
| 84.71% (C21) | frozen exploratory band, **as-run**, D1 |
| 12.53% (C22) | spec-corrected exploratory band, **post-hoc**, D4 |

Never print 12.53% (C22) as replacing 100.00% (C20), nor 84.71% (C21) as a clean point — that arm came from deviation D1. Thresholds are **not comparable between runs**, but **AUROC is** (C23), because it ignores where the cut-off sits: so 0.9824 (C10) and 0.8738 (C11) may be compared, while those three precision figures may not (C23).

## Words you can use and words you must not

| Don't say | Say instead |
|---|---|
| "kappa is percent correct" | "modest agreement beyond chance, 0.2802 (C01)" |
| "the labels are true" / "the labels are false" | "the LLM labellers disagreed on 41 items (C04)" |
| "AUROC 1.0 shows the gate works" (C15) | "the gold indicator is a label-construction artefact (C16)" |
| "D3 holds at every rung" | "D3 is pooled, rung = −1, no per-rung estimate (C19)" |
| "H1 was confirmed" / "H1 was refuted" | "H1 was not exercisable at the registered point (N2, N4)" |
| "12.53% is the real precision" (C22) | "12.53% is the post-hoc spec-corrected band (C22)" |
| "proves" or "validated" | "exploratory", "post-hoc", "consistent with" |
