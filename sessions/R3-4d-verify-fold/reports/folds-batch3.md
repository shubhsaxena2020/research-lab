# Folds batch 3 — wording/structure partials (R3-MF-39, MF-29, MF-13, MF-35)

Scope of writes: `05_paper/template/draft_template.md`, `04_experiments/src/make_paper_assets.py`,
`04_experiments/RESULTS-INDEX.json` (regenerated only by the generator), generated tables under
`05_paper/tables/generated/`, and generated `05_paper/draft/paper.md`. This report file was created.
`06_review/RESPONSE-LETTER-R3.md` and `05_paper/latex-build/**` were not touched.
`06_review/audits/numbers-audit.md` was rewritten only as the automatic side effect of the required
`check_numbers.py` command (the draft sha was unchanged across that check).

The round-2 MF-14 fix from batch 2 (`sessions/R3-4d-verify-fold/reports/mf14-fix.md`) remains intact:
the abstract and §4.6 still carry the registered band R4 `c1.band.precision.r4.run` and frozen
exploratory R4 `c1.expl.precision.r4.run` figures beside `c1.expl.precision.r4.corr`, and §5.2 still
opens with the corpus/feature-stack/gate-family scope restriction. Verified in both template and draft.

---

## Fold 1 — R3-MF-39: remove the undefined term "abstain recall" (all 5 occurrences)

All five occurrences were in the template; zero remain in the template or the generated draft
(`grep -i "abstain recall"` returns no matches in either file). Definitions of refusal rate
`P(refused | negative)` and precision `P(negative | refused)` were preserved.

**Abstract (template line 17).**
Before:
> maximise abstain recall (the refusal rate, P(refused | negative)) subject to a dev abstain precision of

After:
> maximise the refusal rate P(refused | negative) subject to a dev abstain precision of

**§1, H2 (template line 79).**
Before:
>   precision at equal abstain recall when applied to a disjoint held-out half and to a second corpus.

After:
>   precision at equal refusal rate when applied to a disjoint held-out half and to a second corpus.

**§1, H3 (template line 81).**
Before:
>   score, by at least five points, at matched abstain recall.

After:
>   score, by at least five points, at matched refusal rate.

**§3.3 (template line 178).**
Before:
> a single threshold that admits above one. Both maximise dev abstain recall (the refusal rate, P(refused | negative)) subject to a dev abstain

After:
> a single threshold that admits above one. Both maximise the dev refusal rate P(refused | negative) subject to a dev abstain

**§3.5 (template line 217).**
Before:
> called abstain precision (its 'abstain recall' is the same refusal rate), and **precision** for P(negative | refused), computed over the rung's items and

After:
> called abstain precision (the same quantity as the refusal rate defined above), and **precision** for P(negative | refused), computed over the rung's items and

No num keys were added or removed by this fold.

---

## Fold 2 — MF-29: §4.7 zero-difference sentence states what the construction guarantees

The replacement uses the structural fact already stated in §4.2 (template lines 306–308: "the
recall-matched single threshold is the band's own lower threshold to five decimal places, so the
upper threshold never binds"). Existing result file check: `thresholds.band.t_lo` and
`thresholds.single_matched_recall.t` are both `0.90722098925` (round to `0.90722`). No new number is
printed; the existing `<!-- num:c1.st.match.maxdiff -->0.00<!-- /num -->` marker is retained.

**§4.7 (template lines 482–484).**
Before:
> test. On the held-out negatives the band and the matched single refuse the same items to within
> <!-- num:c1.st.match.maxdiff -->0.00<!-- /num --> points, with zero discordant pairs, so H3's zero is not a
> binning artefact.

After:
> test. On the held-out negatives the band and the matched single refuse the same items to within
> <!-- num:c1.st.match.maxdiff -->0.00<!-- /num --> points: the recall-matched single threshold is the band's own
> lower threshold (to five decimal places), so the upper threshold never binds and the zero difference is
> degenerate by construction.

---

## Fold 3 — MF-13: §3.4 makes the inverted-separation treatment explicit

One sentence was added between the one-sided-rule sentence and the existing R4 sentence, which keeps
the existing marker `c1.audit.surface.r4` on R4's inverted value. The chance baseline of AUROC is
written as the word "chance" rather than a bare `0.5`: a probe of `tools/check_numbers.py` confirms a
bare `0.5` is UNTRACEABLE (no non-toy index entry has that value), and the task forbids new numbers
and new keys. The phrase `|AUROC − chance|` is the absolute deviation from the chance baseline,
i.e. |AUROC − 0.5|, stated without introducing an untraceable numeral.

**§3.4 (template lines 201–206).**
Before:
> The audit is one-sided by design: it flags a rung when surface features separate it from answerable items
> in the expected direction, not when they separate it inverted. R4 comes out at
> <!-- num:c1.audit.surface.r4 -->0.415<!-- /num -->, which is separation of the same magnitude with the
> sign flipped, and is reported as that rather than as a clean pass.

After:
> The audit is one-sided by design: it flags a rung when surface features separate it from answerable items
> in the expected direction, not when they separate it inverted. A two-sided reading of |AUROC − chance|
> would flag both directions, inverted separation included, so an inverted value is treated as reverse
> separation rather than a clean pass, and we keep the pre-registered one-sided rule. R4 comes out at
> <!-- num:c1.audit.surface.r4 -->0.415<!-- /num -->, which is separation of the same magnitude with the
> sign flipped, and is reported as that rather than as a clean pass.

No num keys were added or removed by this fold.

---

## Fold 4 — MF-35: table prefixes follow the appearance order of the captions

Generator write paths in `04_experiments/src/make_paper_assets.py` (`main()`, lines 588–594) and
`{{TABLE:...}}` placeholders in the template were renamed together. Stale old generated files remain
on disk, but no template placeholder references them (build output lists only the seven new names).

| Caption / appearance order | Old generated name | New generated name |
|---|---|---|
| Table 1 | `T7_prior_work` | `T1_prior_work` |
| Table 2 | `T3_audit` | `T2_audit` |
| Table 3 | `T1_per_rung` | `T3_per_rung` |
| Table 4 | `T2_hypotheses` | `T4_hypotheses` |
| Table 5 | `T5_arms` | `T5_arms` (unchanged) |
| Table 6 | `T4_frozen_vs_corrected` | `T6_frozen_vs_corrected` |
| Table 7 | `T6_ablations_corrected` | `T7_ablations_corrected` |

**Generator write paths.**
Before:
>     (TAB / "T1_per_rung.md").write_text(table_per_rung(pm), encoding="utf-8")
>     (TAB / "T2_hypotheses.md").write_text(table_hypotheses(fz), encoding="utf-8")
>     (TAB / "T3_audit.md").write_text(table_audit(fz, r5), encoding="utf-8")
>     (TAB / "T4_frozen_vs_corrected.md").write_text(table_frozen_vs_corrected(fz, cx), encoding="utf-8")
>     (TAB / "T5_arms.md").write_text(table_arms(r5, tr, t1), encoding="utf-8")
>     (TAB / "T6_ablations_corrected.md").write_text(table_ablations(abl), encoding="utf-8")
>     (TAB / "T7_prior_work.md").write_text(table_prior_work(), encoding="utf-8")

After:
>     (TAB / "T3_per_rung.md").write_text(table_per_rung(pm), encoding="utf-8")
>     (TAB / "T4_hypotheses.md").write_text(table_hypotheses(fz), encoding="utf-8")
>     (TAB / "T2_audit.md").write_text(table_audit(fz, r5), encoding="utf-8")
>     (TAB / "T6_frozen_vs_corrected.md").write_text(table_frozen_vs_corrected(fz, cx), encoding="utf-8")
>     (TAB / "T5_arms.md").write_text(table_arms(r5, tr, t1), encoding="utf-8")
>     (TAB / "T7_ablations_corrected.md").write_text(table_ablations(abl), encoding="utf-8")
>     (TAB / "T1_prior_work.md").write_text(table_prior_work(), encoding="utf-8")

**Template placeholders (in appearance order).**
Before:
> {{TABLE:T7_prior_work}}   (line 132)
> {{TABLE:T3_audit}}        (line 242)
> {{TABLE:T1_per_rung}}     (line 257)
> {{TABLE:T2_hypotheses}}   (line 261)
> {{TABLE:T5_arms}}         (line 363)
> {{TABLE:T4_frozen_vs_corrected}} (line 415)
> {{TABLE:T6_ablations_corrected}} (line 419)

After:
> {{TABLE:T1_prior_work}}   (line 132)
> {{TABLE:T2_audit}}        (line 244)
> {{TABLE:T3_per_rung}}     (line 259)
> {{TABLE:T4_hypotheses}}   (line 263)
> {{TABLE:T5_arms}}         (line 365)
> {{TABLE:T6_frozen_vs_corrected}} (line 417)
> {{TABLE:T7_ablations_corrected}} (line 421)

Internal generator references: the only references to the old names were the seven write paths above;
`TABLE7_PATH` / `TABLE7_SEED` / `05_paper/tables/table7_data.json` are the *source* data file and seed
for the prior-work table, not a generated table file, so they were deliberately left unchanged.

---

## Required gates — exact outputs

Baseline before edits (already passing, for reference):
```
$ sha256sum 05_paper/draft/paper.md
1679b75fe7db7cfc734a44d2ed1b4d7b94214351950377585d00bdd95ebe80d0 *05_paper/draft/paper.md
$ python tools/check_numbers.py --draft 05_paper/draft/paper.md
509 number(s) in 1 file(s): 322 matched, 187 exempt, 0 finding(s)
report -> C:\Users\shubh\research-lab\06_review\audits\numbers-audit.md
PASS — every number is accounted for
(exit code 0)
```

Run 1:
```
$ python 04_experiments/src/make_paper_assets.py
tables: 13 md files; figure: 1; c1 index entries: 199
exit=0
```
(13 = 7 newly named generated tables + 6 stale old files left on disk as permitted; no stale file is
referenced by the template.)

```
$ python 05_paper/build_draft.py
wrote 05_paper/draft/paper.md from 7 tables (T1_prior_work, T2_audit, T3_per_rung, T4_hypotheses, T5_arms, T6_frozen_vs_corrected, T7_ablations_corrected); 61620 bytes; sha256 d81cc90ffe60
exit=0

$ sha256sum 05_paper/draft/paper.md
d81cc90ffe60a9e58c86aff04cb6fcea0958cc25de5ea512574a05c04a679500 *05_paper/draft/paper.md
```

```
$ python tools/check_numbers.py --draft 05_paper/draft/paper.md
509 number(s) in 1 file(s): 322 matched, 187 exempt, 0 finding(s)
report -> C:\Users\shubh\research-lab\06_review\audits\numbers-audit.md
PASS — every number is accounted for
exit=0

$ sha256sum 05_paper/draft/paper.md
d81cc90ffe60a9e58c86aff04cb6fcea0958cc25de5ea512574a05c04a679500 *05_paper/draft/paper.md
```
Counts are identical to baseline (509/322/187), i.e. no new numeric claims were introduced.

Run 2 (second build after the numbers check):
```
$ python 05_paper/build_draft.py
wrote 05_paper/draft/paper.md from 7 tables (T1_prior_work, T2_audit, T3_per_rung, T4_hypotheses, T5_arms, T6_frozen_vs_corrected, T7_ablations_corrected); 61620 bytes; sha256 d81cc90ffe60
exit=0

$ sha256sum 05_paper/draft/paper.md
d81cc90ffe60a9e58c86aff04cb6fcea0958cc25de5ea512574a05c04a679500 *05_paper/draft/paper.md
```

## Determinism / gate summary

| Check | Value |
|---|---|
| Build 1 sha256 | `d81cc90ffe60a9e58c86aff04cb6fcea0958cc25de5ea512574a05c04a679500` |
| sha256 after `check_numbers.py` | `d81cc90ffe60a9e58c86aff04cb6fcea0958cc25de5ea512574a05c04a679500` |
| Build 2 sha256 | `d81cc90ffe60a9e58c86aff04cb6fcea0958cc25de5ea512574a05c04a679500` |
| Bytes, both builds | 61620 |
| Numbers audit | 0 findings, 322 matched, 187 exempt, exit 0 |

Build 1 and build 2 are byte-identical. All four required commands returned exit code 0.
`grep -i "abstain recall"` on the generated draft: no matches. `grep "{{TABLE:"` on the generated
draft: no matches. The MF-14 passages remain present in the regenerated draft (lines 48–50, 488–491,
592). `04_experiments/RESULTS-INDEX.json` changed only through regeneration by the generator
(an `updated_at` refresh and toy `run_id` values picked up from the current toy summary); all c1
result entries and values are unchanged.

Additional non-required sanity gate (test suites only, no toy pipeline, runner writes nothing):
```
$ python tools/check_all.py --fast --timeout 180
repo root: C:\Users\shubh\research-lab
python:    C:\Users\shubh\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe
running 3 step(s), timeout 180s per step

.. tools-tests: python -m pytest tools/tests -q
   -> PASS in 42.1s
.. harness-tests: python -m pytest 04_experiments/harness/tests -q
   -> PASS in 35.5s
.. paper-tests: python -m pytest 05_paper/template/tests -q
   -> PASS in 6.2s

step           command                                           exit  duration  result
---------------------------------------------------------------------------------------
tools-tests    python -m pytest tools/tests -q                   0     42.1s     PASS
harness-tests  python -m pytest 04_experiments/harness/tests -q  0     35.5s     PASS
paper-tests    python -m pytest 05_paper/template/tests -q       0     6.2s      PASS
---------------------------------------------------------------------------------------
3/3 steps passed
exit=0
```
