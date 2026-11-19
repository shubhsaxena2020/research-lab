# Viva questions and spoken answers — R3-6b student pack

Each answer is speakable in a minute. Every number carries an ID like `(C01)`; `07_student/SOURCE-MAP.md`
maps each ID to its exact source, and the IDs are stable. Say the qualifier with the number.

**Words used in these answers.** A **threshold** is one cut-off value. An **operating point** is the cut-off,
or pair of cut-offs, that decides answer-or-refuse; a **band** is the two-threshold form — answer inside a
middle range, refuse outside it. **Dev** is the half the cut-offs were fitted on; **held-out** is the half
they were never fitted on. A **discordant pair** is a pair of items where the two things compared disagree —
with none, a paired test has nothing to compare. **AUROC** is the chance the gate scores a random answerable
item above a random negative — threshold-free, not an accuracy. **Abstain precision** is, of the items the gate
refused, the share that really were negatives.

---

**1. What is this project testing?**

Answer: One narrow thing: does a gate that decides answer-or-refuse from retrieval signals alone keep its
promises as negatives harden? An **abstention gate** reads only the search step's scores and ranks, never the
reader model's confidence. A **negative item** is a question whose passage lacks the answer. Negatives form
four difficulty **rungs**, R1 to R4, easy to hard: random wrong paragraph, same-entity paragraph, the
paragraph next door, then the gold paragraph with its answer swapped out. The pre-registered hypothesis
**H1** said refuse-precision should not rise up that ladder.

**2. What did MF-14 change, and what are the registered versus exploratory numbers?**

Answer: MF-14 is one cell — abstain precision at the hardest rung, R4 — with three numbers, one per run.
Registered band, frozen run, D1: **100.00%** (C20). Frozen exploratory band, as run, still D1: **84.71%**
(C21). Spec-corrected exploratory band, post-hoc, deviation D4: **12.53%** (C22). None replaces another or
revises a frozen verdict. The last has refitted thresholds, so its precision is not comparable — but the two
AUROCs *are*, **0.9824** and **0.8738** (C23), because AUROC ignores the threshold. That middle arm is
exploratory: deviation D1 added it (C21), so it is not the registered number.

*If pushed, say:* "100.00% is the registered number (C20); 12.53% is post-hoc (C22) — different questions."

**3. Why is H1 not exercisable, and may you say it was confirmed or refuted?**

Answer: No to both. H1's criterion was that abstain precision must not rise across rungs 1 to 4, and fall by
at least **15** points from rung 1 to rung 3 (N1). At the degenerate registered operating point — t_lo
**0.907**, t_hi **0.948** (N2) — **92.9%** of dev items fell below the low threshold, and every gate reported
**1.00** in every rung (N2). The rung-1 minus rung-3 comparison had no discordant pair (N4). Neither confirmed
nor refuted; an exploratory arm cannot rescue it (N3).

*If pushed, say:* "Not exercisable, so neither confirmed nor refuted (N2, N4)."

**4. What does kappa 0.2802 (C01) mean?**

Answer: In this post-hoc re-check, **Cohen's kappa** compares how often two labellers agree with how often
luck alone would make them agree. Here it is **0.2802** (C01). Observed agreement was **0.59** (C02): **59**
of **100** items agreed. Luck alone would give about **0.43** (C03, derived from C01 and C02). So: **modest
agreement beyond chance between these two LLM labellers, in this particular setup**. Not accuracy, not
agreement with a human, not evidence the labels are true. Per rung it was **0.0**, **0.2991**, **0.026** and
**0.1379**, on **25** items each (C08) — with n = 25 those figures are unstable, and their order is not a
hardness ordering.

*If pushed, say:* "0.2802 (C01) is agreement between two LLMs — not accuracy, not human gold."

**5. What do the 41 disagreements and the 56 answerable mean (C04, C07)?**

Answer: In the same post-hoc re-check, the labellers were lopsided: A called **62** items answerable, B only
**21** (C05), disagreeing on **41** of **100** (C04). A strict resolver decided only the disagreements:
**35** answerable, **6** not, **0** ambiguous (C06). Final tally: **56** of **100** negatives answerable,
**56%** (C07). Models judged, not people, so this describes the sample, not the world.

**6. What does the gold-indicator AUROC of 1.0 (C15) mean?**

Answer: In this post-hoc control, the feature restates the label: a tautology. A lexical-surface gate alone
gives **0.9762** on dev rung 1 (C14); adding a "is this the gold paragraph?" indicator gives **1.0** (C15).
The indicator alone, flipped so answerable scores higher, is also **1.0** (C16); `is_gold` is deterministic
from the label (C16). An answerable item always presents the gold paragraph and a negative never does —
separation was guaranteed **by construction, not discovered**. On pooled D3 the same features separate hits
from misses at only **0.7327** (C17) — a different question, neither confirming nor correcting the 1.0
(C15).

*If pushed, say:* "1.0 (C15) is tautological (C16) — a construction artefact, not evidence."

**7. What is an AUROC, and is it the same as accuracy?**

Answer: No. **AUROC** is the chance a gate scores a random answerable item above a random negative. It is
**threshold-free** — it never asks how many items were refused; accuracy and precision move with the
threshold. Frozen run **0.9824**, interval **0.9776 to 0.9867** (C10); spec-corrected **0.8738**, interval
**0.8587 to 0.8893** (C11). A **bootstrap interval** only says how much the number would wobble.

**8. What does the paired difference 0.1085 (C12) [0.0946, 0.1225] mean?**

Answer: It compares the two runs on the same items. The gap is **0.1085**, interval **0.0946 to 0.1225**
(C12), and the interval **excludes zero** (C12), so the drop is not plausibly sampling noise. It rests on
**1,879** held-out items (C13): **400** answerable at rung 0, **1,479** negatives, **18** article clusters,
**10,000** resamples, seed **20261118** (C13). No model was retrained; this is post-hoc.

**9. What is D3, and is there a per-rung number for it?**

Answer: D3 presents the top-ranked passage to every question and records hit or miss — post-hoc, not
confirmatory (N5). Pooled: **655** hits, **145** misses of **800** (C17). Split by half: dev **342** hits
and **58** misses, test **313** hits and **87** misses (C18). There is **no** per-rung R1 to R3 estimate: the
file marks that estimand unavailable and the only rung value present is **−1**, pooled (C19). Never
quote D3 as per-rung.

**10. Why are the two adjudication runs only cautiously comparable?**

Answer: They are not the same instrument. The earlier run had kappa **0.1975** and its resolver called only
**5** of **100** items answerable (C09). The new run has kappa **0.2802** (C01) and called **56** (C07).
Different models, resolver and provenance — not a repeat, not a clean improvement.

**11. What does "exploratory / post-hoc" mean, and are these results in the paper?**

Answer: **Post-hoc** means the analysis was chosen after the results were seen. It can describe and raise a
question, but it cannot confirm a pre-registered hypothesis. All three R3-3b items are labelled exploratory
or post-hoc and none revises a frozen verdict (N5). And no — they are **not yet in the draft** (N6).

**12. Which claims must you refuse to make?**

Answer: Roughly in this order.

- "H1 was refuted" — no. Not exercisable at the registered operating point (N2, N4).
- "H1 was confirmed" — no, same reason (N2, N3).
- "Kappa 0.2802 proves the labels are right, or that they are human gold" — no. Modest agreement beyond
  chance between two LLM labellers (C01); there is no human gold (N5).
- "The gold control proves the gate works" — no. 1.0 is a construction artefact (C15, C16).
- "12.53% is the real R4 number now" — no. Spec-corrected, post-hoc (C22); the registered number stays
  100.00% (C20).
- "D3 gives a per-rung result" — no. Pooled only (C19).
- "This is in the paper" — no. Not yet in the draft (N6).
- "The gate is broken everywhere" — no. One corpus, one feature stack, one gate family.

**13. If the examiner says "so your gate fails" — what do you say?**

Answer: I would scope it, not agree or deny. On this corpus, the ladder appears to have measured
question-passage overlap more than answerability; the gate looks strong because these negatives separate
easily. The rung-4 collapse appears in the spec-corrected run, post-hoc (C22). I would not generalise — no
other corpus, feature stack or gate family was tested. The defensible line: "this design cannot separate
hardness from overlap."
