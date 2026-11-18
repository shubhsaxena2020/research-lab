# Review — batch-2 outputs (MF-14 fix, VERIFY-RESOLVED, response-letter downgrades, gates)

Independent re-review of the R3-4d batch-2 deliverables. Workdir `C:\Users\shubh\research-lab`.
Files read: `sessions/R3-4d-verify-fold/reports/mf14-fix.md`, `sessions/R3-4d-verify-fold/reports/verify-consolidate.md`, `sessions/R3-4d-verify-fold/VERIFY-RESOLVED.md`, generated draft `05_paper/draft/paper.md`, response letter `06_review/RESPONSE-LETTER-R3.md`. No source/template/letter file was edited by this review.

## (a) MF-14 fix in the generated draft — CONFIRMED

Line numbers below are current in `05_paper/draft/paper.md` (704 lines, 61306 bytes).

Three R4 figures, each with its own `<!-- num:... -->` marker and explicit run label, appear together in the Abstract (L46–52) and again in §4.6 (L482–491):

- **100.00%** — marker `c1.band.precision.r4.run`, label "registered band (frozen, D1) run" — Abstract L48, §4.6 L488.
- **84.71%** — marker `c1.expl.precision.r4.run`, label "frozen exploratory (as-run, D1) run" — Abstract L49, §4.6 L489.
- **12.53%** — marker `c1.expl.precision.r4.corr`, label "spec-corrected exploratory (post-hoc, D4) run" — Abstract L50, §4.6 L486.

Exact Abstract quote (L46–52):

```
concrete: an overlap-matched rung (R5, exploratory) is still refused at
<!-- num:c1.r5.precision.expl -->89.25%<!-- /num -->, while the rung that changes what the passage *says*
rather than how much of it overlaps (R4, one answer span replaced inside the gold passage) breaks the gate
once the dense features are implemented as specified — on R4, refusal is
<!-- num:c1.band.precision.r4.run -->100.00%<!-- /num --> in the registered band (frozen, D1) run and
<!-- num:c1.expl.precision.r4.run -->84.71%<!-- /num --> in the frozen exploratory (as-run, D1) run, and falls to
<!-- num:c1.expl.precision.r4.corr -->12.53%<!-- /num --> in the spec-corrected exploratory (post-hoc, D4) run —
an exploratory/post-hoc figure that does not replace the registered result — with discrimination from
<!-- num:c1.auroc.test.run -->0.982<!-- /num --> to <!-- num:c1.auroc.test.corr -->0.874<!-- /num --> AUROC.
```

Exact §4.6 quote (L482–491, key lines 485–489):

```
(<!-- num:c1.expl.precision.r1.corr -->99.75%<!-- /num -->,
<!-- num:c1.expl.precision.r2.corr -->92.86%<!-- /num -->,
<!-- num:c1.expl.precision.r3.corr -->95.50%<!-- /num -->) and R4 collapses to
<!-- num:c1.expl.precision.r4.corr -->12.53%<!-- /num --> in the spec-corrected exploratory (post-hoc, D4) run —
an exploratory/post-hoc figure that does not replace the registered result — beside
<!-- num:c1.band.precision.r4.run -->100.00%<!-- /num --> in the registered band (frozen, D1) run and
<!-- num:c1.expl.precision.r4.run -->84.71%<!-- /num --> in the frozen exploratory (as-run, D1) run. R4 is the rung whose passage is the gold
passage with one span swapped, so a feature set that scores how well a passage matches a question has
```

§5.2 is scoped. Exact quote (L587–598):

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

All three figures and the §5.2 scope match `mf14-fix.md`'s "Generated draft passages" verbatim; the fix is present in the built artifact.

## (b) VERIFY-RESOLVED.md — CONFIRMED

Programmatic parse of the markdown table (excluding header/separator rows):

- Data rows: **23** (unique IDs: 23). Summary line agrees: "`- Rows: 23 (23 expected).`"
- Verdicts: **resolved 13, partial 10**; summary line agrees: "`- Final verdicts: resolved 13, partial 10 (23 total).`"
- IDs: MF-1, MF-2, MF-8, MF-11, MF-14, MF-15, MF-20, MF-26, MF-27, MF-33, MF-34, MF-35, MF-38, MF-39, MF-40, MF-41, MF-42, MF-43, R3-MF-3, R3-MF-36, R3-MF-37, R3-MF-38, R3-MF-39 — exactly the 23 originally-resolved set (18 round-2 + 5 round-3) stated in VERIFY-RESOLVED.md line 3 and `verify-consolidate.md` §1.
- Cross-check against the letter: the 13 resolved IDs in VERIFY-RESOLVED.md equal the 13 sections still marked `Verdict: resolved` in the response letter; the 10 partial IDs equal the 10 sections carrying a `Downgrade reason (R3-4d verification` sentence. Both set comparisons returned `True`.

## (c) Response letter re-parse and 86→85 correction — CONFIRMED

Parsing every `^Verdict:` line in `06_review/RESPONSE-LETTER-R3.md`:

- `resolved: 13`, `partial: 61`, `deferred: 11`, **total 85** (85 item headers, 85 unique IDs).
- Header line 6 documents the correction, exact quote: "Canonical tally after R3-4d draft verification: **13 resolved, 61 partial, 11 deferred = 85 canonical items** (round-2 MF-1…MF-44 plus round-3 R3-MF-1…R3-MF-41). This supersedes the orchestration brief's '23 resolved, 52 partial, 11 deferred = 86': there are 85 distinct canonical IDs, and the pre-downgrade partial count was 51, not 52 (the brief is off by +1 partial and +1 total). Ten items previously marked resolved were downgraded to partial after draft verification (MF-1, MF-8, MF-11, MF-14, MF-15, MF-20, MF-35, MF-39, MF-40, R3-MF-39), moving the split from 23 resolved / 51 partial to 13 resolved / 61 partial; 11 deferred are unchanged. Later batches may change these numbers again; re-parse the `Verdict:` lines rather than relying on this line."
- Line 5 retains the round-2 split qualifier: "`Status: final R3 verdicts assigned per ... (round-2 split 18 resolved, 21 partial, 5 deferred); ...`" — matches `verify-consolidate.md` §3 NEW header.

Reconciliation: 23 resolved − 10 downgrades = 13; 51 partial + 10 = 61; 11 deferred unchanged; 13 + 61 + 11 = 85. No duplicate/orphan IDs observed in the parse.

## (d) Gate re-runs — ALL PASS

Draft sha256 before every run: `1679b75fe7db7cfc734a44d2ed1b4d7b94214351950377585d00bdd95ebe80d0` (61306 bytes).

`python 05_paper/build_draft.py` (exit 0), exact stdout:

```
wrote 05_paper/draft/paper.md from 7 tables (T7_prior_work, T3_audit, T1_per_rung, T2_hypotheses, T5_arms, T4_frozen_vs_corrected, T6_ablations_corrected); 61306 bytes; sha256 1679b75fe7db
```

`python tools/check_numbers.py --draft 05_paper/draft/paper.md` (exit 0), exact stdout:

```
509 number(s) in 1 file(s): 322 matched, 187 exempt, 0 finding(s)
report -> C:\Users\shubh\research-lab\06_review\audits\numbers-audit.md
PASS — every number is accounted for
```

`python tools/check_all.py` (exit 0), exact stdout:

```
repo root: C:\Users\shubh\research-lab
python:    C:\Users\shubh\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe
running 4 step(s), timeout 600s per step

.. tools-tests: python -m pytest tools/tests -q
   -> PASS in 37.5s
.. harness-tests: python -m pytest 04_experiments/harness/tests -q
   -> PASS in 36.4s
.. paper-tests: python -m pytest 05_paper/template/tests -q
   -> PASS in 5.1s
.. toy-pipeline: python 04_experiments/toy/run_pipeline.py
   -> PASS in 8.9s

step           command                                           exit  duration  result
---------------------------------------------------------------------------------------
tools-tests    python -m pytest tools/tests -q                   0     37.5s     PASS
harness-tests  python -m pytest 04_experiments/harness/tests -q  0     36.4s     PASS
paper-tests    python -m pytest 05_paper/template/tests -q       0     5.1s      PASS
toy-pipeline   python 04_experiments/toy/run_pipeline.py         0     8.9s      PASS
---------------------------------------------------------------------------------------
4/4 steps passed
```

SHA-256 of `05_paper/draft/paper.md` after build, after check_numbers, and after check_all (all identical, byte-deterministic):

```
1679b75fe7db7cfc734a44d2ed1b4d7b94214351950377585d00bdd95ebe80d0 *05_paper/draft/paper.md
```

This equals the post-fix sha recorded in `mf14-fix.md` §"SHA-256 determinism" (`1679b75fe7db7cfc734a44d2ed1b4d7b94214351950377585d00bdd95ebe80d0`, 61306 bytes). No drift.

## Mismatches / observations

- No mismatch found in the four machine-checkable claims (a)–(d): all counts, verdict sets, header correction, gate outputs and sha values reproduce exactly as reported.
- One documented timing nuance (not a defect): the response letter's MF-14 downgrade reason is explicitly recorded against the audited *pre-fix* state — exact quote: "`Downgrade reason (R3-4d verification, audit-A; recorded against the audited pre-fix state): ... A separate writer is fixing the template; this reason records the pre-fix state the audit verified.`" The built draft now contains the fix (section (a)), and VERIFY-RESOLVED.md MF-14 likewise says "`MISSING (audited pre-fix state): ... A separate writer is fixing the template; verdict recorded against the audited pre-fix state.`" The letter's stale description is therefore accounted for in both source reports; MF-14 remains `partial` deliberately.
- Side effects of the required gate commands (not manual edits): `check_numbers.py` rewrote `06_review/audits/numbers-audit.md` (its documented default-report behaviour; draft sha unchanged across the check). `check_all.py`'s `toy-pipeline` step created seven new untracked `04_experiments/runs/20261118T1723*/` directories (timestamps 17:23:05–17:23:11), despite the runner's own "writes nothing" docstring; no tracked file changed as a result. These are pre-existing/generated artifacts, not edits made by this review.
