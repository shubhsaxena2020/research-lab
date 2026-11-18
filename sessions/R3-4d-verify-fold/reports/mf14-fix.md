# MF-14 (round 2) fix report

Scope: only `05_paper/template/draft_template.md` was edited (three passages); the generated draft
was rebuilt with `python 05_paper/build_draft.py`; this report was created. No other file was edited.

## Result keys used (all pre-existing in `04_experiments/RESULTS-INDEX.json`)

| Marker | Value | Index description |
| --- | --- | --- |
| `c1.band.precision.r4.run` | 100.00% | Band abstain precision, R4 (as run) — registered/frozen band R4 |
| `c1.expl.precision.r4.run` | 84.71% | Exploratory precision, R4 (as run) — frozen exploratory R4 |
| `c1.expl.precision.r4.corr` | 12.53% | Exploratory precision, R4 (spec-corrected, D4) — exploratory/post-hoc |

No new numeric claims and no new result keys were added. The two markers newly placed in the Abstract
and §4.6 (`c1.band.precision.r4.run`, `c1.expl.precision.r4.run`) are existing registered keys.

## Template edits (quoted from `05_paper/template/draft_template.md`)

### 1. Abstract (edited lines 46–52)

```
rather than how much of it overlaps (R4, one answer span replaced inside the gold passage) breaks the gate
once the dense features are implemented as specified — on R4, refusal is
<!-- num:c1.band.precision.r4.run -->100.00%<!-- /num --> in the registered band (frozen, D1) run and
<!-- num:c1.expl.precision.r4.run -->84.71%<!-- /num --> in the frozen exploratory (as-run, D1) run, and falls to
<!-- num:c1.expl.precision.r4.corr -->12.53%<!-- /num --> in the spec-corrected exploratory (post-hoc, D4) run —
an exploratory/post-hoc figure that does not replace the registered result — with discrimination from
<!-- num:c1.auroc.test.run -->0.982<!-- /num --> to <!-- num:c1.auroc.test.corr -->0.874<!-- /num --> AUROC.
```

The corrected 12.53% now sits beside the registered band R4 100.00% and frozen exploratory R4 84.71%,
each with its own marker and explicit run label; the corrected figure is marked exploratory/post-hoc and
not a replacement of the registered result.

### 2. §4.6 (edited lines 425–431)

```
(<!-- num:c1.expl.precision.r1.corr -->99.75%<!-- /num -->,
<!-- num:c1.expl.precision.r2.corr -->92.86%<!-- /num -->,
<!-- num:c1.expl.precision.r3.corr -->95.50%<!-- /num -->) and R4 collapses to
<!-- num:c1.expl.precision.r4.corr -->12.53%<!-- /num --> in the spec-corrected exploratory (post-hoc, D4) run —
an exploratory/post-hoc figure that does not replace the registered result — beside
<!-- num:c1.band.precision.r4.run -->100.00%<!-- /num --> in the registered band (frozen, D1) run and
<!-- num:c1.expl.precision.r4.run -->84.71%<!-- /num --> in the frozen exploratory (as-run, D1) run. R4 is the rung whose passage is the gold
```

### 3. §5.2 (edited lines 528–540)

```
### 5.2 What a retrieval-feature gate measures

The claim in this section is scoped to the corpus, feature stack and gate family measured here; it is not
a claim about abstention gates in general. The audit, the overlap-matched rung and the top-1 variant agree on one description: these features
measure how well the presented passage matches the question and how likely it is to be the document
retrieval wanted. On negatives constructed by substituting paragraphs, those quantities and answerability
move together, which is why the ladder looks like a hardness ladder. When they come apart — R4, where the
passage matches perfectly and one span is wrong — the gate has nothing to work with, and the corrected run
shows it; the corrected R4 result is an exploratory/post-hoc re-implementation (deviation D4), reported
beside the registered and frozen results and not in place of them. The practical implication is not that abstention gates are useless. It is that a ladder of
substituted paragraphs measures overlap, and that the rung which changes what the passage says must be in
the ladder or the ladder is measuring the wrong thing.
```

Diff scope (`git diff --stat -- 05_paper/template/draft_template.md`):
`1 file changed, 13 insertions(+), 5 deletions(-)`. All other wording is preserved.

## Generated draft passages (quoted from `05_paper/draft/paper.md` after rebuild)

### Abstract (lines 46–52)

```
rather than how much of it overlaps (R4, one answer span replaced inside the gold passage) breaks the gate
once the dense features are implemented as specified — on R4, refusal is
<!-- num:c1.band.precision.r4.run -->100.00%<!-- /num --> in the registered band (frozen, D1) run and
<!-- num:c1.expl.precision.r4.run -->84.71%<!-- /num --> in the frozen exploratory (as-run, D1) run, and falls to
<!-- num:c1.expl.precision.r4.corr -->12.53%<!-- /num --> in the spec-corrected exploratory (post-hoc, D4) run —
an exploratory/post-hoc figure that does not replace the registered result — with discrimination from
<!-- num:c1.auroc.test.run -->0.982<!-- /num --> to <!-- num:c1.auroc.test.corr -->0.874<!-- /num --> AUROC.
```

### §4.6 (lines 483–489)

```
(<!-- num:c1.expl.precision.r1.corr -->99.75%<!-- /num -->,
<!-- num:c1.expl.precision.r2.corr -->92.86%<!-- /num -->,
<!-- num:c1.expl.precision.r3.corr -->95.50%<!-- /num -->) and R4 collapses to
<!-- num:c1.expl.precision.r4.corr -->12.53%<!-- /num --> in the spec-corrected exploratory (post-hoc, D4) run —
an exploratory/post-hoc figure that does not replace the registered result — beside
<!-- num:c1.band.precision.r4.run -->100.00%<!-- /num --> in the registered band (frozen, D1) run and
<!-- num:c1.expl.precision.r4.run -->84.71%<!-- /num --> in the frozen exploratory (as-run, D1) run. R4 is the rung whose passage is the gold
```

### §5.2 (lines 587–598)

```
### 5.2 What a retrieval-feature gate measures

The claim in this section is scoped to the corpus, feature stack and gate family measured here; it is not
a claim about abstention gates in general. The audit, the overlap-matched rung and the top-1 variant agree on one description: these features
measure how well the presented passage matches the question and how likely it is to be the document
retrieval wanted. On negatives constructed by substituting paragraphs, those quantities and answerability
move together, which is why the ladder looks like a hardness ladder. When they come apart — R4, where the
passage matches perfectly and one span is wrong — the gate has nothing to work with, and the corrected run
shows it; the corrected R4 result is an exploratory/post-hoc re-implementation (deviation D4), reported
beside the registered and frozen results and not in place of them. The practical implication is not that abstention gates are useless. It is that a ladder of
substituted paragraphs measures overlap, and that the rung which changes what the passage says must be in
the ladder or the ladder is measuring the wrong thing.
```

## Gate commands and exact outputs

Baseline before edits (for reference — build and check both passed):

```
$ python 05_paper/build_draft.py
wrote 05_paper/draft/paper.md from 7 tables (T7_prior_work, T3_audit, T1_per_rung, T2_hypotheses, T5_arms, T4_frozen_vs_corrected, T6_ablations_corrected); 60295 bytes; sha256 89e92e7990a4
$ sha256sum 05_paper/draft/paper.md
89e92e7990a451ff49ac14f11d016bf8b44d4b85906d0bba64f6d9cc3b7a9ca8 *05_paper/draft/paper.md
$ python tools/check_numbers.py --draft 05_paper/draft/paper.md
505 number(s) in 1 file(s): 318 matched, 187 exempt, 0 finding(s)
report -> C:\Users\shubh\research-lab\06_review\audits\numbers-audit.md
PASS — every number is accounted for
```

Post-edit required commands:

```
$ python 05_paper/build_draft.py
wrote 05_paper/draft/paper.md from 7 tables (T7_prior_work, T3_audit, T1_per_rung, T2_hypotheses, T5_arms, T4_frozen_vs_corrected, T6_ablations_corrected); 61306 bytes; sha256 1679b75fe7db

$ sha256sum 05_paper/draft/paper.md
1679b75fe7db7cfc734a44d2ed1b4d7b94214351950377585d00bdd95ebe80d0 *05_paper/draft/paper.md

$ python tools/check_numbers.py --draft 05_paper/draft/paper.md
509 number(s) in 1 file(s): 322 matched, 187 exempt, 0 finding(s)
report -> C:\Users\shubh\research-lab\06_review\audits\numbers-audit.md
PASS — every number is accounted for
(exit code 0)

$ python 05_paper/build_draft.py
wrote 05_paper/draft/paper.md from 7 tables (T7_prior_work, T3_audit, T1_per_rung, T2_hypotheses, T5_arms, T4_frozen_vs_corrected, T6_ablations_corrected); 61306 bytes; sha256 1679b75fe7db

$ sha256sum 05_paper/draft/paper.md
1679b75fe7db7cfc734a44d2ed1b4d7b94214351950377585d00bdd95ebe80d0 *05_paper/draft/paper.md
```

## SHA-256 determinism

- Build 1 draft sha256: `1679b75fe7db7cfc734a44d2ed1b4d7b94214351950377585d00bdd95ebe80d0`
- Draft sha256 immediately after numbers check (unchanged): `1679b75fe7db7cfc734a44d2ed1b4d7b94214351950377585d00bdd95ebe80d0`
- Build 2 draft sha256: `1679b75fe7db7cfc734a44d2ed1b4d7b94214351950377585d00bdd95ebe80d0`
- Byte size both builds: 61306 bytes.

Build 1 and build 2 are byte-identical. Numbers audit: 0 findings, exit 0.
Note: `tools/check_numbers.py` writes its default report to `06_review/audits/numbers-audit.md`; that
write is an automatic side effect of the required command, not a manual edit, and it did not alter the
draft (sha unchanged across the check).
