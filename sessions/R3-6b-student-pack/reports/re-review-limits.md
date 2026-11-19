# Re-review — plain language and support limits (post-correction, R3-6b)

Reviewer lane: independent limits / plain-language **re-reviewer** after the batch-3 correction pass.
Read-only. Written 2026-11-19.

Files judged on their **current bytes** (sizes at time of review):

| File | Bytes | Lines |
|---|---|---|
| `07_student/ROUND3-DIGEST.md` | 7737 | 85 |
| `07_student/VIVA-QA.md` | 8418 | 128 |
| `07_student/SOURCE-MAP.md` (label/limit notes only) | 23094 | 134 |

Authorities read in full: `sessions/R3-6b-student-pack/TASK.md`; `04_experiments/results/c1/r3/R3-3b/ANSWERS.md`;
`04_experiments/PREREGISTRATION.md` §1 (H1) and §10 (D1, D2, D3, D4 item 3, D5);
`orchestration/HEAD-REVIEW.md` checkpoints 9–11; `RULES.md` items 2/5/14; `sessions/R3/COMMON.md`.
Prior report read for continuity: `reports/review-limits.md` (batch 2, pre-correction).

**Verdict: DEFECTS FOUND — 3.** Nine of the ten checks pass. The support limits themselves are intact:
no frozen verdict is revised, no finding is promoted, H1 carries no verdict, D3 is not made per-rung, and the
gold indicator is still called a tautology everywhere it appears. The three remaining defects are one
readability ordering fault and two mislabelled statistics inside the answers a student says out loud.

---

## 1. Checks

| # | Check | Result | Document line |
|---|---|---|---|
| 1 | All three R3-3b findings labelled exploratory/post-hoc, early and repeatedly; "not yet in the draft" stated | **PASS** | Digest 3–5 ("all **exploratory / post-hoc** … None of them is in the draft yet (N6), and none changes a frozen verdict (N5)"); repeated at digest 15, 35 ("recomputed post-hoc"), 51, 52, 54; viva 46 ("In this post-hoc re-check"), 56 ("In the same post-hoc re-check"), 63 ("In this post-hoc control"), 89–90 ("post-hoc, not confirmatory"), 104–105 ("All three R3-3b items are labelled exploratory or post-hoc … And no — they are **not yet in the draft** (N6)"), 119. |
| 2 | κ 0.2802 = modest agreement beyond chance between these two LLM labellers; never accuracy / percent correct / human agreement / proof | **PASS** | Digest 25: "0.2802 (C01) is **modest agreement beyond chance between these two LLM labellers**. It is not accuracy, not human agreement, not proof the labels are true." Also digest 21, 27, 53, 79–80. Viva 48–50: "**modest agreement beyond chance between these two LLM labellers, in this particular setup**. Not accuracy, not agreement with a human, not evidence the labels are true." (Residual, counted separately as defect 3: viva 50 quotes per-rung κ as a min–max range with no n = 25.) |
| 3 | Gold-indicator AUROC 1.0 = tautological construction/label artefact; never evidence the gate works | **PASS** | Digest 43: "A perfect score looks like success, but it is **tautological**: the flag is a deterministic function of the label (C16). Restating the answer key, it cannot fail — so it cannot show the gate works (N7)." Also digest 54, 81. Viva 63–69 ("separation was guaranteed **by construction, not discovered**"), 71, 115. No sentence anywhere offers 1.0 as support for the gate. |
| 4 | D3 = pooled rung = −1 hit/miss only; no per-rung R1–R3 estimate implied | **PASS** | Digest 47: "**D3 is pooled only, at rung = −1** (C19); no per-rung R1–R3 estimate exists (C19)." Also digest 55, 82. Viva 91–93: "There is **no** per-rung R1 to R3 estimate: the file marks that estimand unavailable and the only rung value present is **−1**, pooled (C19). Never quote D3 as per-rung." The dev/test split at viva 90 is labelled "Split by half", not by rung. |
| 5 | H1 = not exercisable at the registered operating point; no text implies a verdict | **PASS** | Digest 63: "So: **H1 was not exercisable at the registered operating point.** Not \"confirmed\", and not \"refuted\" — not even if an exploratory ordering looks like a trend". Viva 40, 42, 111, 112. Every occurrence of "confirmed"/"refuted" in both files is a negation or a refused claim (digest 63, 83; viva 34, 40, 42, 111, 112). Grep for `rejected`, `failed the test`, `H1 holds`, `not supported` → zero hits. The one "supported" hit, digest 11 ("when data do not support a claim, the claim gets smaller"), is generic and does not name H1. |
| 6 | MF-14 always with all three run labels; nothing says one replaces another | **PASS** | Digest 69–71: "100.00% (C20) \| registered band, **frozen**, D1"; "84.71% (C21) \| frozen exploratory band, **as-run**, D1"; "12.53% (C22) \| spec-corrected exploratory band, **post-hoc**, D4"; digest 73: "Never print 12.53% (C22) as replacing 100.00% (C20), nor 84.71% (C21) as a clean point — that arm came from deviation D1." Viva 26–30: "None replaces another or revises a frozen verdict", each number carrying run + deviation label; viva 116–117 repeats the pairing. Viva 32's short "if pushed" line names only two of the three numbers but labels both and is preceded by the full three-row answer directly above — not a replacement claim. |
| 7 | No claim a frozen verdict was revised; no "novel" / "state of the art" / "proven" / "validated"; no generalisation past one corpus, one feature stack, one gate family | **PASS** | "none changes a frozen verdict (N5)" digest 4; "**no frozen verdict is revised** (N5)" digest 52; viva 27, 105. `novel`, `state of the art`, `proven`, `validated` occur only inside the *don't say* table (digest 85) and the refuse list (viva 113, 115). Scope held at viva 120 ("One corpus, one feature stack, one gate family") and 126–128 ("I would not generalise — no other corpus, feature stack or gate family was tested"). The digest contains no generalisation of its own. |
| 8 | Over-refusal / cap claims: NONE | **PASS** | Literal search for `cap`, `over-refus`, `feasible`, `coverage`, `saturat` over `07_student/*.md` returns **zero hits in `ROUND3-DIGEST.md` and zero in `VIVA-QA.md`**. All hits are in `SOURCE-MAP.md` and are reported verbatim in §2 below. The false "84.71% arm over-refused past its declared cap" clause is gone. See also defect 2: viva 38–39 now prints an over-refusal number under the wrong name ("refused share"), which is a mislabel rather than a cap claim. |
| 9 | Readability: terms defined at first use; no answer over ~120 words | **FAIL** | **`AUROC` is used before it is defined.** Viva 29, inside answer 2: "the two AUROCs *are*, **0.9824** and **0.8738** (C23), because AUROC ignores the threshold"; again in the question 6 heading (viva 61) and body (63–69). The definition does not arrive until viva 75: "**AUROC** is the chance a gate scores a random answerable item above a random negative." The preamble glossary (viva 6–10) defines threshold, operating point, band, dev, held-out, discordant pair — not AUROC. Also **`abstain precision` is never defined in the viva at all**: used at viva 25 and 36, and the reader first meets the same quantity at viva 21 under a second name, "refuse-precision". Everything else on the list is now defined at or before first use: band/operating point/dev/held-out/threshold/discordant pairs (digest 13; viva 6–10), rung and negative (digest 13; viva 18–19), kappa (digest 21; viva 46). Length: max answer 137 words (Q12, seven short bullets), all others 47–98 words; Q12 is at the edge but speakable in about a minute as a list, so length alone is not the failure. |
| 10 | Five mandatory traps present in the do-not-say / refused-claims material | **PASS** | Digest 77–85 table: κ "is percent correct" (79), "AUROC 1.0 shows the gate works" (81), "D3 holds at every rung" (82), "H1 was confirmed / H1 was refuted" (83), "12.53% is the real precision" (84). Viva 111–117 list: H1 refuted (111), H1 confirmed (112), "Kappa 0.2802 proves…" (113), "The gold control proves the gate works" (115), "12.53% is the real R4 number now" (116), "D3 gives a per-rung result" (118). All five present in both documents. |

Score: **9 PASS, 1 FAIL**, plus two defects that fall outside the ten checks (see §3).

---

## 2. Check 8 — every hit, verbatim

Search pattern `cap|over-refus|feasible|coverage|saturat`, case-insensitive, over `07_student/*.md`.

`ROUND3-DIGEST.md` — **no hits**.
`VIVA-QA.md` — **no hits**.

`SOURCE-MAP.md`, three hits:

1. Line 13 — "**Coverage.** C01–C23 (23 numeric claim IDs) plus N1–N8 (8 fact IDs) = 31 claim IDs, written as
   **32 table rows**…". False positive: "coverage" here means claim-ID coverage of the mapping table, not
   retrieval coverage.
2. Line 50, C20 note — "**registered band (frozen, D1)** — the pre-registered operating point, and the arm H1
   was registered on; it is saturated (see N2)." True hit. It is not a claim about the pack's own findings; it
   restates PREREGISTRATION D1 ("the thresholds sit in the saturated region where precision is bought with
   coverage") and is correctly tied to N2.
3. Line 55, N2 note — "92.9% of dev items are refused below t_lo alone; dev over-refusal 0.755; \"Every gate then
   reports abstain precision 1.00 in every rung, so H1 and H3 cannot be tested at that operating point\"". True
   hit, and a verbatim quote of the frozen deviation text. No cap claim.

No sentence in either student document claims a ceiling, a cap, an infeasibility, or an over-refusal finding.
Check 8 passes.

---

## 3. Defects to correct

### Defect 2 (viva 38–39) — `0.755` is over-refusal, not "the refused share"

Current: "**92.9%** of dev items fell below the low threshold, the refused share was **0.755**, and every gate
reported **1.00** in every rung (N2)."

`0.755` is `results/c1/results_full.json` → `test.band_primary.over_refusal`, and the code defines that field as
`refused[hit].mean()` (`04_experiments/src/eval_top1.py:130`) — the share of **answerable** items refused. It is
not the share of items refused. The held-out refused share is `1 − coverage` = `1 − 0.0527` = **0.9473**. As
written the sentence contradicts itself in one breath (92.9% fell below the cut-off, so at least 92.9% were
refused, not 75.5%), and it disagrees with the pack's own mapping card, which calls the same number
"dev over-refusal 0.755" (SOURCE-MAP 55).

Replace with:

> "**92.9%** of dev items fell below the low threshold on its own, and the registered band refused **75.5%** of
> the answerable held-out items (N2); every gate still reported **1.00** in every rung (N2)."

### Defect 3 (viva 50) — per-rung κ quoted without n = 25

Current: "Per rung it ran from **0.0** to **0.2991** (C08)."

SOURCE-MAP C08 is explicit: "25 items per rung: per-rung κ is unstable and must never be quoted without
\"n = 25\". The spread is **not** a hardness ordering." The values are R1 0.0, R2 0.2991, R3 0.026, R4 0.1379 —
non-monotone. "It ran from 0.0 to 0.2991" reads as a progression, which is the exact inference C08 forbids, and it
drops the n that makes the numbers interpretable.

Replace with:

> "Per rung κ was **0.0**, **0.2991**, **0.026**, **0.1379** on only **25** items each (C08) — too few to read as a
> hardness trend."

Or, if the answer must stay short, delete the sentence: it carries no claim the answer needs.

---

## 4. What was checked and found clean

- **Frozen verdicts.** No sentence says a verdict moved. `exploratory` arms are never promoted: digest 63 cites
  N3 ("an exploratory arm cannot rescue a hypothesis"); viva 40 repeats it; viva 27 says "None replaces another or
  revises a frozen verdict".
- **H1 against the registered text.** Digest 61 states both limbs of H1 ("never increasing across rungs 1 to 4,
  with at least a 15-point drop from rung 1 to rung 3 (N1)"), matching PREREGISTRATION §1 lines 22–23. The
  non-exercisability reason matches D1 ("refuse 92.9% of dev items below t_lo alone … Every gate then reports
  abstain precision 1.00 in every rung, so H1 and H3 cannot be tested at that operating point") and N4's
  "no discordant pairs (all differences zero)". Both documents take the not-exercisable line that HEAD-REVIEW
  checkpoint 10 endorses over the draft's contradictory "remains refuted" (§4.6).
- **MF-14 against D4 item 3.** Digest 73 and viva 28–29 reproduce the rule exactly: thresholds not comparable
  between runs, AUROC comparable because threshold-free. No fourth operating point was smuggled in; the
  deliberately excluded 90.73% (SOURCE-MAP §4) appears nowhere.
- **The gold-indicator limit survives paraphrase.** Digest 43 and viva 65–67 both give the mechanism
  ("`is_gold` is deterministic from the label"; "answerable item always presents the gold paragraph and a negative
  never does"), not just the conclusion, so the student can defend it.
- **D3.** No table, sentence or implied estimate gives D3 a rung other than −1. The dev/test split is labelled as
  a split by half.

### Advisory (not counted as defects)

- `hypotheses.H1.supported = false` still sits in the frozen `results_full.json` and the pack never pre-empts it.
  An examiner who opens the file will find a field that reads like a verdict. One defensive sentence in viva Q3
  would close it (this was advisory in the batch-2 report and remains unapplied).
- Viva 32 ("100.00% is the registered number (C20); 12.53% is post-hoc (C22) — different questions") names two of
  the three MF-14 numbers. Both carry labels and it follows the full three-row answer, so it does not violate
  check 6, but a third clause would cost four words.
- SOURCE-MAP N2 still calls `0.755` "dev over-refusal" because it quotes the deviation text verbatim, while the
  value lives at `test.band_primary.over_refusal`. The quote is faithful; the row could add the JSON key so a
  student checking the number does not land on prose that calls it "dev".

---

## 5. What this review changed

Nothing. No student file was edited; the only write is this report. The three defects above are for the lead to
route back to the viva editor (`07_student/VIVA-QA.md`, lines 38–39 and 50) and, for the AUROC ordering, to
either editor — the cheapest fix is one clause in the viva preamble glossary.

**Final verdict: DEFECTS FOUND — 3** (1 failed check: readability/definition order; 2 mislabelled statistics).
Limits preserved otherwise.
