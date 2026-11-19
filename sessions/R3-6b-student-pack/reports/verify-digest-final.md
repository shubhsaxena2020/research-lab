# verify-digest-final — independent final verification of `07_student/ROUND3-DIGEST.md`

Lane: R3-6b-student-pack (independent final verifier). Date: 2026-11-19.
Artifact verified: `07_student/ROUND3-DIGEST.md`, 85 lines, 7,737 bytes, `wc -w` = **1289**.
Method: every number re-read from the JSON/Markdown bytes in this session (`json.load` for the three R3-3b files and
both `results_full.json`; `sed -n` for the two preregistration sections and HEAD-REVIEW checkpoints 9–11).
Nothing was taken from the writer's or a reviewer's report.

Source-file hashes at verification time match `07_student/SOURCE-MAP.md` §3 exactly:

| file | sha256 (first 12) | matches map |
|---|---|---|
| `04_experiments/results/c1/r3/R3-3b/mf10_adjudication.json` | `2324d8605534` | yes |
| `04_experiments/results/c1/r3/R3-3b/mf17_auroc_intervals.json` | `07c3a0f8a54f` | yes |
| `04_experiments/results/c1/r3/R3-3b/mf7_gold_control.json` | `0728d92714d0` | yes |
| `04_experiments/results/c1/results_full.json` | `e4cf65cb0b2b` | yes |
| `04_experiments/results/c1_corrected/results_full.json` | `936ce0b89e22` | yes |

---

## Check 1 — every numeral maps to a stored value in a named file

**PASS.** 64 data numerals were traced; all 64 resolve to a stored value (or, for the single derived value, to a
labelled derivation). No numeral was unsourced.

JSON key prefixes below are shortened: `r10.` = `results['c1.r3_3b.mf10.…']`, `r17.` = `…mf17.…`, `r7.` = `…mf7.…`.

| # | line | numeral | source key / section | stored value | verdict |
|---|---|---|---|---|---|
| 1 | 11 | 44 | N8 → `sessions/R3/TRIAGE.md` L1 + rows 8–51; `HEAD-REVIEW.md` CK5 L46 | 44 review items | OK |
| 2 | 19 | 100 | `r10.n_items` | 100 | OK |
| 3 | 23 | 0.2802 | `r10.cohen_kappa_overall` | 0.2802 (full: 0.2801966292134831) | OK |
| 4 | 23 | 0.59 | `r10.raw_agreement_po` | 0.59 | OK |
| 5 | 23 | 59 | `r10.n_agreed` | 59 | OK |
| 6 | 23 | 100 | `r10.n_items` | 100 | OK |
| 7 | 23 | 41 | `r10.n_disagreed` | 41 | OK |
| 8 | 23 | 62 | `r10.labeller_A_answerable_n` | 62 | OK |
| 9 | 23 | 21 | `r10.labeller_B_answerable_n` | 21 | OK |
| 10 | 23 | 41 | `r10.resolver_on_disagreements_n` | 41 | OK |
| 11 | 23 | 35 | `r10.resolver_resolved_1_n` | 35 | OK |
| 12 | 23 | 6 | `r10.resolver_resolved_0_n` | 6 | OK |
| 13 | 23 | 0 | `r10.resolver_resolved_ambiguous_n` | 0 | OK |
| 14 | 23 | 56 | `r10.resolved_answerable_n` | 56 | OK |
| 15 | 23 | 100 | `r10.n_items` | 100 | OK |
| 16 | 23 | 0.56 | `r10.resolved_answerable_share` | 0.56 | OK |
| 17 | 23 | 56% | same as #16 (0.56 share) | 0.56 | OK |
| 18 | 25 | 0.2802 | `r10.cohen_kappa_overall` | 0.2802 | OK |
| 19 | 25 | 0.43 | C03 — **derived**, no stored key; labelled "derived from C01 and C02" | 0.4304 (see Check 8) | OK (labelled) |
| 20 | 25 | 0.59 | `r10.raw_agreement_po` | 0.59 | OK |
| 21 | 35 | 0.9824 | `r17.frozen_heldout_auroc.point` | 0.9823630831643002 | OK |
| 22 | 35 | 95% | CI level: keys `ci95_lo`/`ci95_hi`; `resampling.alpha`=0.05, `interval`="percentile 2.5 / 97.5" | 0.95 | OK |
| 23 | 35 | 0.9776 | `r17.frozen_heldout_auroc.ci95_lo` | 0.9776211411662427 | OK |
| 24 | 35 | 0.9867 | `r17.frozen_heldout_auroc.ci95_hi` | 0.9866543835742593 | OK |
| 25 | 35 | 0.8738 | `r17.corrected_heldout_auroc.point` | 0.8738488843813388 | OK |
| 26 | 35 | 95% | as #22 (`ci95_*` on corrected) | 0.95 | OK |
| 27 | 35 | 0.8587 | `r17.corrected_heldout_auroc.ci95_lo` | 0.8586833140203312 | OK |
| 28 | 35 | 0.8893 | `r17.corrected_heldout_auroc.ci95_hi` | 0.8893003500532195 | OK |
| 29 | 35 | 0.1085 | `r17.paired_auroc_diff.diff` | 0.10851419878296142 | OK |
| 30 | 35 | 95% | as #22 (`paired_auroc_diff.ci95_*`) | 0.95 | OK |
| 31 | 35 | 0.0946 | `r17.paired_auroc_diff.ci95_lo` | 0.09458017350090517 | OK |
| 32 | 35 | 0.1225 | `r17.paired_auroc_diff.ci95_hi` | 0.12252082237972457 | OK |
| 33 | 37 | 1,879 | `denominators.held_out_common.n_items` | 1879 | OK |
| 34 | 37 | 400 | `…n_positive_rung0` | 400 | OK |
| 35 | 37 | 1,479 | `…n_negative_rungs1to4` | 1479 | OK |
| 36 | 37 | 18 | `…n_article_clusters` | 18 | OK |
| 37 | 37 | 10,000 | top-level `n_boot` (map row C13b) | 10000 | OK |
| 38 | 37 | 20261118 | top-level `seed` (map row C13b) | 20261118 | OK |
| 39 | 43 | 1.0 | `r7.gold_control.dev.r1.auroc_plus_is_gold` | 1.0 | OK |
| 40 | 43 | 1.0 | `r7.gold_control.dev.r1.auroc_is_gold_alone_answerable_oriented` | 1.0 | OK |
| 41 | 45 | 0.9762 | `r7.gold_control.dev.r1.auroc_surface_lex` | 0.9762 | OK |
| 42 | 47 | 655 | `r7.d3_pooled.all.n_hit` | 655 | OK |
| 43 | 47 | 145 | `r7.d3_pooled.all.n_miss` | 145 | OK |
| 44 | 47 | 800 | `r7.d3_pooled.all.n` | 800 | OK |
| 45 | 47 | 0.7327 | `r7.d3_pooled.all.auroc_surface_lex_hit_vs_miss` | 0.7327 | OK |
| 46 | 47 | −1 | `r7.d3_pooled.rungs_present_value` | -1 | OK |
| 47 | 54 | 1.0 | `r7.gold_control.dev.r1.auroc_plus_is_gold` | 1.0 | OK |
| 48 | 61 | 15 | N1 → `PREREGISTRATION.md` §1 H1, lines 22–25 ("drop from rung 1 to rung 3 is ≥ 15 points") | 15 points | OK |
| 49 | 61 | 92.9% | N2 → §10 **D1**, lines 167–172 ("refuse 92.9% of dev items below t_lo alone") | 92.9 | OK |
| 50 | 61 | 1.00 | N2 → same D1 paragraph ("abstain precision 1.00 in every rung") | 1.00 | OK |
| 51 | 69 | 100.00% | `test.band_primary.per_rung["4"].abstain_precision` (c1) | 1.0 | OK |
| 52 | 70 | 84.71% | `test.exploratory_band.per_rung["4"].abstain_precision` (c1) | 0.8471 | OK |
| 53 | 71 | 12.53% | `test.exploratory_band.per_rung["4"].abstain_precision` (c1_corrected) | 0.1253 | OK |
| 54 | 73 | 12.53% | as #53 | 0.1253 | OK |
| 55 | 73 | 100.00% | as #51 | 1.0 | OK |
| 56 | 73 | 84.71% | as #52 | 0.8471 | OK |
| 57 | 73 | 0.9824 | `r17.frozen_heldout_auroc.point` | 0.9823630831643002 | OK |
| 58 | 73 | 0.8738 | `r17.corrected_heldout_auroc.point` | 0.8738488843813388 | OK |
| 59 | 79 | 0.2802 | `r10.cohen_kappa_overall` | 0.2802 | OK |
| 60 | 80 | 41 | `r10.n_disagreed` | 41 | OK |
| 61 | 81 | 1.0 | `r7…auroc_plus_is_gold` | 1.0 | OK |
| 62 | 82 | −1 | `r7.d3_pooled.rungs_present_value` | -1 | OK |
| 63 | 84 | 12.53% | as #53 | 0.1253 | OK |
| 64 | 84 | 12.53% | as #53 | 0.1253 | OK |

**64 numerals, 0 defects.** Internal arithmetic also holds wherever two stored numbers are combined in the text:
100 − 59 = 41 (line 23); 400 + 1,479 = 1,879 (line 37); 655 + 145 = 800 (line 47); 56/100 = 0.56 = 56% (line 23).
One acceptable compression: line 37 cites `(C13)` once for the two resampling-config fields that `SOURCE-MAP.md`
row `C13b` splits out — the map itself states C13b is "a split of C13, not a new claim ID", so the single ID is
correct, not a mis-citation.

## Check 2 — every numeral carries a claim ID in the same clause

**PASS with 1 listed exception (not a defect).**

- Exceptions, data numerals: none. All 64 numerals in Check 1 sit in a clause containing `(Cxx)`, `(Nx)`, or an
  equivalent citation.
- Exception, non-data numerals (line 21): "One is perfect; zero is chance level." These two numerals state the
  textbook endpoints of Cohen's kappa's range — a definition of the scale, not a measurement — and the paragraph's
  actual value (0.2802) carries `(C01)` on the same line.
- Structural numerals deliberately not counted as claims: heading ordinals (lines 1, 9, 17, 29, 39, 59: "Round 3",
  "1.", "2.", "3."), rung labels (`R1`–`R4`, "rung 0", "rung 1", "rung 3", "rungs 1 to 4" on lines 13, 37, 45, 47,
  61), and prose counts ("three new analyses" line 3, "one lane" line 11, "two-threshold" line 13). Rung labels
  identify a rung; they are not values. The one rung label that *is* a value, "rung = −1" (lines 47, 82), carries
  `(C19)`.

## Check 3 — the eight required framings

**PASS — 8/8 present.**

| framing | present | evidence (digest line) |
|---|---|---|
| (a) all three findings exploratory/post-hoc | yes | L3 "The three new analyses below are all **exploratory / post-hoc**"; L51 "Exploratory / post-hoc, all three (N5)"; each section repeats it (L25, L35, L43) |
| (b) not yet in the draft | yes | L4 "None of them is in the draft yet (N6)"; L52 "**Not in the draft yet** (N6)" — matches HEAD-REVIEW CK11 L94 |
| (c) no frozen verdict revised | yes | L4 "none changes a frozen verdict (N5)"; L52; L73 "Revises no frozen verdict" is in the map; digest L63 "an exploratory arm cannot rescue a hypothesis (N3)" |
| (d) kappa = agreement, not accuracy, not human gold | yes | L25 "It is not accuracy, not human agreement, not proof the labels are true"; L27 "Not human gold… These are model judgements (N5)"; L53 |
| (e) gold indicator tautological / construction artefact | yes | L43 "**tautological**: the flag is a deterministic function of the label (C16)… cannot show the gate works"; L54 "construction artefact (C16, N7)" |
| (f) D3 pooled rung = −1, no per-rung R1–R3 estimate | yes | L47 "**D3 is pooled only, at rung = −1** (C19); no per-rung R1–R3 estimate exists (C19)"; L55; L82 |
| (g) H1 not exercisable, neither confirmed nor refuted | yes | L61 heading "**not exercisable**"; L63 "Not \"confirmed\", and not \"refuted\""; L83 |
| (h) MF-14 with all three run labels | yes | L69 "registered band, **frozen**, D1" 100.00% (C20); L70 "frozen exploratory band, **as-run**, D1" 84.71% (C21); L71 "spec-corrected exploratory band, **post-hoc**, D4" 12.53% (C22); L73 repeats that the three are not interchangeable |

Observation (not a defect): the `D1` tag on the 100.00% row (L69) reads as "documented in deviation D1", which is
how `SOURCE-MAP.md` row C20 words it and how D1 itself describes the degeneracy. D1 explicitly keeps the
confirmatory analysis "exactly as pre-registered", and the digest never calls 100.00% exploratory — so the
frozen/exploratory/post-hoc ordering the student must preserve is intact.

## Check 4 — no over-refusal / cap / feasibility claim

**PASS — zero hits.** Case-insensitive search over the current bytes:

| pattern | hits |
|---|---|
| `cap` | 0 |
| `over-refus` / `overrefus` / `over refus` | 0 |
| `feasib` | 0 |
| `755` / `0.755` | 0 |

The H1 paragraph describes D1's saturation without importing D1's over-refusal metric: L61 says "the gate refused
almost everything, with 92.9% of dev items below the lower cut-off on its own (N2)", which is a faithful paraphrase
of the D1 sentence and avoids the `0.755` figure entirely.

## Check 5 — no overclaiming

**PASS.** Searches: `novel` 0, `state of the art` / `state-of-the-art` 0, `proven` 0, `90.73` / `9073` 0.

Two hits that are *not* claims:

- L25 "not proof the labels are true" — a negation, in the sentence that denies kappa is accuracy.
- L85 `| "proves" or "validated" | "exploratory", "post-hoc", "consistent with" |` — the must-not-say table, i.e. an
  instruction to the student *not* to use those words. No declarative sentence in the digest claims proof or
  validation.

No generalisation beyond one corpus / one feature stack / one gate family: the digest never says "in general",
"any corpus", or "all gates". Its general statements (L21, L31, L33) define kappa, AUROC and bootstrap intervals as
concepts; every result sentence is scoped to "the frozen run" / "the spec-corrected run" / "the same lexical
features". 90.73% is absent, as `SOURCE-MAP.md` §4 requires.

## Check 6 — length

**1289 words** (`wc -w`). Under the lead's 1,300-word ceiling by 11 words, and within the "at most about two pages"
brief for a dense A4/Letter page pair at normal student-pack density. Defensible, but with no headroom — any
addition needs a deletion.

## Check 7 — pointer to the source map

**PASS.** L7: "Every number carries an ID like (C01), and `07_student/SOURCE-MAP.md` gives the exact file, JSON key
and stored value behind each ID. If a number is not in that table, it does not belong here." The path is the exact
relative path `07_student/SOURCE-MAP.md`, which exists (134 lines, 23,094 bytes).

## Check 8 — kappa paragraph arithmetic

**PASS.** Re-computed in this session from the stored values, two independent ways:

- From `κ` and `Po` alone: `Pe = (Po − κ)/(1 − κ) = (0.59 − 0.2801966292134831)/(1 − 0.2801966292134831) =
  0.4304`.
- From the stored marginals (`mf10.agreement.contingency` = `{both_0: 38, both_1: 21, A1_B0: 41, A0_B1: 0}`, and
  A = 62 / B = 21 answerable): `Pe = (62×21 + 38×79)/100² = 0.4304`.
- Round trip: `(0.59 − 0.4304)/(1 − 0.4304) = 0.280197` → the published `0.2802`.

So: 0.2802 (L23, L25) = stored `0.2802`; 0.59 raw agreement (L23, L25) = stored `0.59`; ~0.43 (L25) is correctly
rounded from 0.4304 and is **explicitly labelled "derived from C01 and C02"**, which is exactly what
`SOURCE-MAP.md` row C03 demands for the only derived value in the pack. Nothing in the paragraph implies kappa is
accuracy: L25 names it "modest agreement beyond chance between these two LLM labellers" and then states "not
accuracy, not human agreement, not proof the labels are true"; L27 says the judgements are model judgements, and
that disagreement does not make the negatives wrong.

---

## Defects

None. No numeral is unsourced, misrounded, or mislabelled; all eight required framings are present; no over-refusal,
cap, feasibility, novelty or validation claim appears; the source-map pointer is present; the kappa arithmetic is
internally consistent and its derived value is labelled.

Non-blocking observation carried forward (not counted as a defect): the digest sits 11 words under the 1,300-word
ceiling, so any later wording addition must be paired with a deletion.

**DIGEST VERIFIED**
