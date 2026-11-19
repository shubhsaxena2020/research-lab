# COMPLETENESS / CONSISTENCY RE-REVIEW (round 3, post-correction) — R3-6b student pack

Reviewer: independent completeness/consistency re-reviewer, batch 3. Date 2026-11-19. Read-only.
Judged on **current bytes** only; nothing grandfathered from batch-1/2 reviews.

Files: `07_student/ROUND3-DIGEST.md` (85 lines), `07_student/VIVA-QA.md` (128 lines),
`07_student/SOURCE-MAP.md` (134 lines, 32 table rows), `sessions/R3-6b-student-pack/CLAIM-INVENTORY.md`
(C13b now present as an accepted split of C13), `reports/fix-digest.md`, `reports/fix-viva.md`,
`reports/fix-source-map.md`.

Every stored value below was re-read here with `json.load` from the cited file.

---

## Check 1 — Deliverable 1 (digest) — PASS

- Word count: `wc -w 07_student/ROUND3-DIGEST.md` = **1289** → inside 1,100–1,350.
- What Round 3 changed: L9–L11 ("Round 3 is the repair round… 44 must-fix items (N8)… when data do not
  support a claim, the claim gets smaller"); the three findings at L17 (kappa), L29 (AUROC intervals),
  L39 (gold control + D3).
- Required limit explanations, all present: post-hoc/exploratory L3, L51; not human gold L5, L27, L53;
  no frozen verdict revised L4, L52; not in the draft L4, L52; kappa = modest agreement beyond chance,
  not accuracy L21–L25, L79; gold-indicator 1.0 tautological/construction artefact L43, L81; D3 pooled
  rung = −1 with no per-rung estimate L47, L82; H1 not exercisable and neither confirmed nor refuted
  L59–L63, L83; MF-14 registered vs exploratory with run labels L65–L73.
- Jargon gloss (batch-3 fix) present at L13: threshold, operating point, band, dev/held-out, discordant pair.

## Check 2 — Deliverable 2 (viva) — PASS (one flag)

- **13 Q&A** (Q1–Q13). Answer lengths (words, answer body only): 87, 94, 88, 84, 59, 98, 61, 61, 71, 47,
  52, 137, 66 → **max 137 (Q12), median 71**.
- **Flag:** Q12 ("Which claims must you refuse to make?") is 137 words (146 with its heading and lead-in)
  — the only answer over 120. It is an 8-bullet refusal list, ~1 min aloud, so not a TASK breach, but it
  is the one answer above the 120-word line.
- Coverage: MF-14 Q2 (L23–L32); H1 not exercisable Q3 (L34–L42); kappa 0.2802 Q4 (L44–L52); gold
  indicator 1.0 Q6 (L61–L71); must-not-say claims Q12 (L107–L120). Q5/Q8/Q9/Q10 reinforce numbers; Q11
  carries post-hoc + not-in-draft; Q13 carries scoping.

## Check 3 — Deliverable 3 (traceability) — PASS

Regex `\b([CN]\d{1,2}b?)\b` over each file; map rows `^\| (id) \|`.

- digest cites **28** IDs, viva **29**, map has **32** rows (C01–C23 + C13b + N1–N8).
- **digest-only:** N7, N8.
- **viva-only:** C08, C09, C18.
- **missing-from-map:** **none** (digest ∅, viva ∅).
- Reverse: map IDs ⊄ inventory = **∅** (C13b is now defined at `CLAIM-INVENTORY.md:48`); inventory
  claim IDs not in map = ∅ (the only extra regex hit, `C1`, is the path legend, not a claim).
- No invented IDs: both student documents use only IDs that exist as map rows.

## Check 4 — numeral ⇒ ID tag in the same clause — PASS, two quoted-form exceptions reported

Same-sentence audit (paragraphs flattened, IDs/metric/run/rung tokens blanked, sentence split on
`. ; —`), all numeral occurrences checked by hand afterwards:

- `ROUND3-DIGEST.md`: **no exception.** "Round 3" (L1/L9/L11) is a round name, not a measurement.
- `VIVA-QA.md`: **two exceptions**, both inside a quoted must-not-say phrase whose ID appears in the
  immediately following correction clause:
  - **VIVA-QA.md:113** — `"Kappa 0.2802 proves the labels are right, or that they are human gold"`; the
    tag `(C01)` follows at L114 in the refutation.
  - **VIVA-QA.md:116** — `"12.53% is the real R4 number now"`; the tag `(C22)` follows in the same bullet
    ("Spec-corrected, post-hoc (C22)"), and `100.00% (C20)` is tagged.
  Both are quotations of claims the student is told not to make, and each bullet's permitted rendering is
  tagged. Classed as acceptable, recorded here as required. (The digest's own don't-say table tags its
  quoted numerals inline — C15 at L81, C22 at L84 — so the viva is marginally looser than the digest on
  this one point.)

## Check 5 — eight required framings — all present

| # | Framing | Evidence (file:line) |
|---|---|---|
| 1 | exploratory / post-hoc | DIGEST:3, :51, :35; VIVA:103–105, :89 |
| 2 | not in the draft | DIGEST:4, :52; VIVA:105, :119 |
| 3 | no frozen verdict revised | DIGEST:4, :52; VIVA:28, :105 |
| 4 | kappa not accuracy / not human gold | DIGEST:25, :27, :53, :79; VIVA:49, :52, :113–114 |
| 5 | gold indicator tautological (deterministic from label) | DIGEST:43, :54, :81; VIVA:63–67, :71 |
| 6 | D3 pooled rung = −1, no per-rung R1–R3 | DIGEST:47, :55, :82; VIVA:91–93, :118 |
| 7 | H1 not exercisable, neither confirmed nor refuted | DIGEST:59, :63, :83; VIVA:34, :42, :111–112 |
| 8 | MF-14 three run labels (frozen D1 / as-run D1 / post-hoc D4) | DIGEST:69–71, :73; VIVA:26–27 |

## Check 6 — batch-3 editor claims — all five verified present

| Claim | Verdict | Evidence |
|---|---|---|
| (a) no "over-refus"/"declared cap" in either student document | **PRESENT** | `grep -n 'over-refus\|declared cap' 07_student/ROUND3-DIGEST.md 07_student/VIVA-QA.md` → no match. Viva Q2 now reads "That middle arm is exploratory: deviation D1 added it (C21), so it is not the registered number" (L29–30). The only surviving "over-refus" string in the pack is `SOURCE-MAP.md:55`, which quotes PREREG D1 verbatim inside the N2 row. |
| (b) SOURCE-MAP has no "561", C21 row cites 556 | **PRESENT** | `grep -n '561' 07_student/SOURCE-MAP.md` → exit 1, no match. `SOURCE-MAP.md:51` reads `"exploratory_band" (551) → "per_rung" (556) → "4" (596)`. |
| (c) C13b in inventory and annotated in the map | **PRESENT** | `CLAIM-INVENTORY.md:48` defines C13b; `SOURCE-MAP.md:43` is the C13b row, plus the explanatory note at `:63–65` ("C13b is not a new claim ID… accepted split of C13"). |
| (d) digest and viva each contain a SOURCE-MAP pointer | **PRESENT** | `ROUND3-DIGEST.md:7` (blockquote: every number carries an ID, `07_student/SOURCE-MAP.md` gives file/key/value); `VIVA-QA.md:3–4`. One mention each. |
| (e) viva Q3 ≤ 120 words | **PRESENT** | Q3 block (heading + answer + "If pushed") = 116 words; answer body 88. |

Other fix-report claims spot-checked and true: digest 0.755 clause deleted (grep → absent); digest L35
"recomputed post-hoc with no model retrained"; digest L54 `(C23, C10)`; digest L13 "A few words first"
gloss; viva Q4/Q5/Q6/Q9 post-hoc restatements; viva header no longer points at `CLAIM-INVENTORY.md`;
`SOURCE-MAP.md:32` C03 row now names the `contingency` key at line 87.

## Check 7 — cross-document consistency — PASS

44 numeral tokens appear in both documents. Ten sampled and byte-compared: `0.2802` (C01), `0.59` (C02),
`41` (C04), `56` and `56%` (C07), `0.43` (C03), `0.9824` (C10), `0.8738` (C11), `0.1085` (C12),
`1,879` (C13), `655`/`145`/`800`/`0.7327` (C17), `100.00%` (C20), `84.71%` (C21), `12.53%` (C22).
All identical in digits, rounding and separators. Same-value-different-rendering scan found no collision
(`100` item counts vs `100.00%` precision, `1.0` AUROC vs `1.00` precision are different quantities).
Only divergence of any kind: digest prints "95% interval", viva prints "interval" — no value differs.

## Check 8 — scope — PASS

`git status --short` / `git diff --stat` in the working tree show this lane's writes only under the two
owned roots: `07_student/` (3 files, untracked) and `sessions/R3-6b-student-pack/` (untracked).

Other modified paths, with attribution:

| path | state | mtime | reading |
|---|---|---|---|
| `04_experiments/results/summary_toy.json` | M | 01:56 | predates lane start 01:57:04; toy-run burst (R3-4f) |
| `04_experiments/toy/toy_runs.json` | M | 01:56 | same burst |
| `orchestration/HEAD-REVIEW.md` | M (+6) | 00:02 | predates lane; Checkpoint 11 text, read-only input here |
| `06_review/audits/numbers-audit.md` | M (741 lines) | 02:44 | numbers-audit lane; audits `sessions/R3-4f-bind-3b/repro/probe.md`; not R3-6b |
| `04_experiments/runs/20261118T2026*_toy_*` (8 dirs) | ?? | 01:56 | predate lane |
| `sessions/R3-4e-consistency/`, `sessions/R3-4f-bind-3b/` | ?? | 23:19 / 04:08 | other lanes |
| `sessions/R3/orch/*pass6*` | ?? | 00:02 | predates lane |

No path under `05_paper/**`, `04_experiments/results/c1/**`, `04_experiments/results/c1_corrected/**`,
`04_experiments/PREREGISTRATION.md` or `04_experiments/RESULTS-INDEX.json` is modified by this lane
(RESULTS-INDEX is now clean/staged-out compared with the batch-2 snapshot).

---

## Flags (non-blocking)

1. VIVA-QA.md Q12 is 137 words — the only answer over 120; it is a bulleted refusal list, ~1 min aloud.
2. VIVA-QA.md:113 and :116 quote must-not-say numerals without an inline tag; the ID lands in the
   correction clause of the same bullet.

## Verdict

**PACK COMPLETE** — 8/8 checks pass, 0 gaps, 2 recorded flags.
