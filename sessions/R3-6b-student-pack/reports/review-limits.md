# Review — plain language and support limits (R3-6b student pack)

Reviewer lane: independent language + support-limit reviewer. Read-only. Written 2026-11-19.
Files reviewed: `07_student/ROUND3-DIGEST.md` (83 lines), `07_student/VIVA-QA.md` (128 lines),
`07_student/SOURCE-MAP.md` (label/limit notes only).
Authorities read in full: `sessions/R3-6b-student-pack/TASK.md`, `04_experiments/results/c1/r3/R3-3b/ANSWERS.md`,
`04_experiments/PREREGISTRATION.md` §1 (H1) and §10 D1/D2/D3/D4/D5, `orchestration/HEAD-REVIEW.md`
checkpoints 9–11, `sessions/R3/COMMON.md`, `RULES.md` items 2/5/14.

**Verdict: CHANGES REQUIRED.** Seven checks pass, one is partial, two fail. The support limits are
preserved almost everywhere — the failures are (a) one factual sentence about over-refusal that
attributes the corrected run's cap breach to the frozen exploratory arm, and (b) undefined jargon that a
first-semester BCA student cannot speak aloud.

---

## 1. Checks

| # | Check | Result | Evidence line |
|---|---|---|---|
| 1 | Every R3-3b finding labelled exploratory/post-hoc, early and often; pack says NOT YET IN THE DRAFT | **PARTIAL** | Digest line 3: "The three new analyses below are all **exploratory / post-hoc** — worked out *after* the results were known (N5). None of them is in the draft yet (N6)". Repeats at digest 13, 49, 50, 52; viva 105–106, 120. **Gap:** viva answers 4, 5, 6 and 9 (the three findings themselves) never restate the label; only Q11, which comes after all of them, does. |
| 2 | κ 0.2802 = modest agreement beyond chance; never accuracy / percent-correct / human agreement / proof | **PASS** | Digest 23: "0.2802 is **modest agreement beyond chance between these two LLM labellers**. It is not accuracy, not human agreement, not proof the labels are true." Also digest 51, 77–78; viva 45–50. |
| 3 | Gold-indicator AUROC 1.0 = tautological construction/label artefact; never evidence the gate works | **PASS** | Digest 41: "A perfect score looks like success, but it is **tautological**: the flag is a deterministic function of the label (C16). Restating the answer key, it cannot fail — so it cannot show the gate works (N7)." Also digest 52, 79; viva 61–68. |
| 4 | D3 = pooled rung = −1 hit/miss, no per-rung R1–R3 estimate | **PASS** | Digest 45: "**D3 is pooled only, at rung = −1**; no per-rung R1–R3 estimate exists (C19)." Viva 91–92: "There is **no** per-rung R1 to R3 estimate … Never quote D3 as per-rung." Viva 90 splits dev/test but explicitly labels it "Split by half", not by rung. |
| 5 | H1 = NOT EXERCISABLE at the registered operating point; never confirmed/refuted/"not supported"/"rejected"/"failed the test"/"H1 holds" | **PASS** | Digest 61: "**H1 was not exercisable at the registered operating point.** Not \"confirmed\", and not \"refuted\"". Viva 36–39. Grep for "not supported / rejected / failed the test / H1 holds" returns zero hits; every "confirmed"/"refuted" occurrence is inside a refusal (digest 81; viva 29, 112–113). |
| 6 | MF-14 always with all three run labels; nothing says one replaces another | **PASS** | Digest 67–69: "100.00% \| registered band, **frozen**, D1"; "84.71% \| frozen exploratory band, **as-run**, D1"; "12.53% \| spec-corrected exploratory band, **post-hoc**, D4". Digest 71: "Never print 12.53% as replacing 100.00%". Viva 20–24: "None replaces another and none revises a frozen verdict." |
| 7 | No frozen verdict revised; nothing called novel/SOTA/proven/validated; no generalisation past one corpus/one feature stack/one gate family | **PASS** | Digest 4, 50, 83; viva 104–106. "novel", "state of the art", "proven", "validated" appear only inside the *don't say* table (digest 83). Scoping at viva 121 ("One corpus, one feature stack, one gate family") and viva 125–128. |
| 8 | Readability for a first-semester BCA student: no unspeakable sentences, no undefined jargon, no answer over ~1 minute | **FAIL** | Undefined in both documents: **operating point** (digest 59, 61, 81; viva 32, 112), **band** (digest 67–69; viva 20–21), **dev** (digest 59; viva 33), **discordant pairs** (digest 59; viva 35–36). Digest line 11 glosses only four words ("negative", "abstention gate", "rung", "abstain precision"). Worst sentences quoted in §3. |
| 9 | Over-refusal / cap sentence accurate against both `results_full.json` files | **FAIL** | Viva 24–25: "The 84.71% arm over-refused past its declared cap — not a clean operating point." False for that arm. See §2 finding 1 for the four keys. |
| 10 | Digest "do not say" + viva refuse-list cover the five mandatory traps | **PASS** | κ: digest 77 / viva 114. Gold indicator: digest 79 / viva 116. D3 per-rung: digest 80 / viva 119. H1 confirmed-or-refuted: digest 81 / viva 112–113. 12.53% replacing 100.00%: digest 82 / viva 117. All five present in both documents. |

Score: **7 PASS, 1 PARTIAL, 2 FAIL.**

### Check 9 — what the source files actually say

| Key | `results/c1/results_full.json` | `results/c1_corrected/results_full.json` |
|---|---|---|
| `test.exploratory_band.over_refusal` | **0.095** | **0.11** |
| `test.band_primary.over_refusal` | 0.755 | 0.915 |
| `exploratory.operating_point.band.dev_over_refusal` (the D1 cap in force) | 0.100 (`max_over_refusal` 0.100, `feasible: true`) | 0.095 (`max_over_refusal` 0.100, `feasible: true`) |
| `test.exploratory_band.per_rung.4.abstain_precision` | 0.8471 (= 84.71%, C21) | 0.1253 (= 12.53%, C22) |

Truth: the **84.71% arm is the frozen, as-run exploratory band. It sat exactly on its 10% dev cap (0.100)
and came in at 9.5% over-refusal on the held-out half — at the cap, not past it.** The arm that goes
**past** the same 10% cap is the **spec-corrected 12.53% arm, at 11% over-refusal** on the held-out half.
The viva therefore assigns the corrected run's cap breach to the wrong arm. (SOURCE-MAP line 51's note for
C21 — "do not present it as a clean operating point" — is correct and is not the problem; the problem is
the factual "past its declared cap" mechanism attached to it.)

---

## 2. Findings and exact replacement sentences

### Finding 1 (blocking) — viva Q2 assigns the cap breach to the wrong arm

Current, `VIVA-QA.md` lines 23–25: "…because AUROC ignores the threshold. The 84.71% arm over-refused past
its declared cap — not a clean operating point."

Replace with:

> "(C23), because AUROC ignores the threshold. The 84.71% arm sits exactly on its declared 10% over-refusal
> cap — not a clean operating point either. The arm that actually goes **past** the cap is the 12.53% one:
> 11% of held-out items refused, against the same 10% cap."

### Finding 2 (blocking) — "dev over-refusal 0.755" mislabels a held-out number

`0.755` is `test.band_primary.over_refusal` — the held-out half — but both documents call it "dev".
The source sentence in PREREGISTRATION D1 has the same defect ("refuse 92.9% of dev items below t_lo alone
— dev over-refusal is 0.755 on the held-out half"), so this is inherited, not invented. It still mislabels
a number in a document a student will read aloud.

`ROUND3-DIGEST.md` line 59, current: "It could not run at the registered point: the gate refused almost
everything — 92.9% of dev items fell below the lower cut-off alone — with dev over-refusal 0.755 (N2)."

Replace with:

> "It could not run at the registered point. The single cut-off refused 92.9% of dev items on its own, and
> the registered band over-refused 75.5% of held-out items (N2): the gate said 'refuse' to almost
> everything, so there was nothing left to compare."

`VIVA-QA.md` lines 33–34, current: "**92.9%** of dev items fell below the low threshold alone, dev
over-refusal **0.755** (N2)."

Replace with:

> "**92.9%** of dev items fell below the low threshold on its own, and **75.5%** of held-out items were
> over-refused (N2)."

### Finding 3 (blocking) — five undefined terms

`operating point`, `band`, `dev`, `threshold` and `discordant pairs` are used as if already known. Add one
line to the digest's "Four words first" paragraph (line 11) and change the heading to "A few words first":

> "An **operating point** is the cut-off (or pair of cut-offs) a gate uses; the **band** is the two-threshold
> version of that rule, which answers inside a middle range and refuses outside it. **Dev** is the half the
> cut-offs were fitted on; **held-out** is the half they were never fitted on. A **discordant pair** is a
> pair of items where the two rungs give different answers — with none, there is nothing for a paired test
> to compare."

### Finding 4 (blocking) — three viva answers never restate the label

Q4, Q5 and Q6 are the three findings; an examiner can stop there and never reach Q11. Add four words to
each opening, and keep the rest unchanged:

- Q4 (line 43), prepend: "In this post-hoc re-check, **Cohen's kappa** compares…"
- Q5 (line 54), prepend: "In the same post-hoc re-check, the labellers were lopsided…"
- Q6 (line 61), prepend: "In this post-hoc control, the answer is that the feature restates the label…"

### Finding 5 (advisory) — "weaker, more believable" invites the wrong inference

`VIVA-QA.md` line 66: "On pooled D3 the same score separates hits from misses at only **0.7327** (C17) —
weaker, more believable." D3 is a *different* measurement (hit vs miss, top-1 presented, fresh gate), not a
de-biased version of 1.0 or of 0.9824. Replace with:

> "On pooled D3 the same features separate retrieval hits from misses at **0.7327** (C17) — a different
> question, so it neither confirms nor corrects the 1.0."

### Finding 6 (advisory) — one defensive sentence for the `supported: false` field

`results/c1/results_full.json` stores `hypotheses.H1.supported = false` alongside
`sign_test.n_note = "no discordant pairs (all differences zero)"` and `diff_r1_minus_r3 = 0.0`. An examiner
who opens the file will find that field. Add to viva Q3 after "neither passed nor failed":

> "If someone quotes the file: the field says 'not supported' because a test with zero discordant pairs and
> 400 identical pairs produces that value mechanically — not because the data gave a verdict."

### Finding 7 (advisory) — 0.9824 read as a frozen result

Digest line 33 opens "The frozen run's AUROC is 0.9824". The number is the frozen run's held-out scores,
recomputed post-hoc. Replace with: "The frozen run's held-out AUROC, recomputed post-hoc with no model
retrained, is 0.9824 (C10)."

---

## 3. Three worst readability quotes

**(a) `VIVA-QA.md` lines 20–25 — the MF-14 answer, unsayable in one breath.**
> "Registered band, frozen run, D1: **100.00%** (C20). Frozen exploratory band, as run, still D1: **84.71%**
> (C21). Spec-corrected exploratory band, post-hoc, deviation D4: **12.53%** (C22). None replaces another
> and none revises a frozen verdict. The last has refitted thresholds, so its precision is not comparable —
> but the two AUROCs *are*…"

Three noun-stacks in a row, no verbs, three label systems (band / run / deviation) braided into one
sentence; a student will say "registered band frozen run D1" as a chant and lose the audience. Shorter:

> "Same cell, three runs. Frozen registered: 100.00% (C20). Frozen exploratory, as we ran it: 84.71% (C21).
> Corrected, post-hoc: 12.53% (C22). They answer different questions, so none replaces another."

**(b) `ROUND3-DIGEST.md` line 59 — three numbers and an undefined "cut-off" in one clause.**
> "It could not run at the registered point: the gate refused almost everything — 92.9% of dev items fell
> below the lower cut-off alone — with dev over-refusal 0.755 (N2)."

Two percentages in one breath, "lower cut-off" undefined, and the halves are mixed. Shorter: see Finding 2.

**(c) `VIVA-QA.md` lines 31–37 — 138 words and ~65 s aloud, ending on three abstractions.**
> "H1's registered test was a shape: abstain precision must not rise across rungs, and must fall by at least
> **15** points from rung 1 to rung 3 (N1). At the registered operating point the band sat at t_lo **0.907**
> and t_hi **0.948** (N2)… With no discordant pairs the test was never exercised…"

"H1's registered test was a shape" is a metaphor a first-year student cannot defend under questioning, and
the answer closes on "discordant pairs", an undefined term. Shorter:

> "The test needed precision to change between rungs. It never did: every rung scored 1.00, and all 400
> paired differences were exactly zero (N2, N4). You cannot measure a change that is not there — so the test
> never ran. That is why I say 'not exercisable', not 'confirmed' and not 'refuted'."

Note on the viva header, line 3: "Each answer is speakable aloud in well under a minute" overstates Q3 and
Q12 (150 words of bullets). Either shorten Q3 as above or soften to "in about a minute".

---

## 4. What this review did not change

No student file was edited. Nothing here disputes a number: every value quoted in the pack matched its
source key, and the arithmetic is another reviewer's lane. The two FAILs are wording — one wrong
attribution of an over-refusal figure, one layer of undefined vocabulary — and both are fixable in five
sentences.
