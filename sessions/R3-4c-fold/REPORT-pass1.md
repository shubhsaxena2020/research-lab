# R3-4c-fold — orchestrator pass 1 report

Date: 2026-11-18 (about 21:30 IST)

## Read

- `RULES.md`
- `sessions/R3/COMMON.md`
- `orchestration/HEAD-REVIEW.md`
- `orchestration/DIRECTIVES.md` (noted as superseded by round-3 instructions)
- `06_review/reviews/round3-c1/AGGREGATE.md`
- `06_review/reviews/round3-c1/methodologist.review.yaml`
- `06_review/reviews/round3-c1/reproducibility_reviewer.review.yaml`
- Existing R3-4b lane card, prompt, protocol, progress, response letter, and round comparison

## Findings and decisions

- The round-3 simulated review has six personas, mean 5.67/10, median 6, and six borderline decisions. The aggregate lists 41 distinct new-round must-fix items.
- 22 of those items persist themes from round 2; 19 are new. Persisted themes include gold-paragraph confounding, D4/preregistration consistency, operating-point comparability, H1/H3 verdict wording, run labels, held-out R2 and exchangeability reporting, SQuAD unanswerables, answerability baseline and companion metrics, uncertainty intervals, small cluster counts, novelty-search documentation, DeclineCraft coverage, the pre-registration hash, and abstract terminology/order.
- New themes include fixed-capacity ablation controls, IDF leakage disclosure, R4 label validation, sampling and article counts, selective-classification context, missing control-arm n/intervals, explicit novelty delta, artifact seeds/traceability/license/hyperparameters/smoke test, R4 replacement and reader model details, scope overgeneralization, and figure-caption ordering.
- Round-3 reviews are valid for the pre-fold draft. Round 3 must not be repeated in this lane. Its scores must remain labelled as pre-fold evidence in the comparison.
- The previous claim that the round-3 prompt packs were stale is incorrect: the simulator's newline-normalized hash `9194a481` and the byte hash `e346271e` refer to the same draft. This correction is recorded in Checkpoint 6.

## Written

- `sessions/R3-4c-fold/TASK.md`: fold all 26 outstanding round-2 items and 41 round-3 must-fix items with existing evidence, rebuild, update comparison and response letter, and meet the three gates. Excludes `05_paper/latex-build/**`.
- `sessions/R3-4c-fold/PROMPT-R3.txt`: protocol plus lane-specific instructions, with no double-quote characters.
- Checkpoint 6 appended to `orchestration/HEAD-REVIEW.md`.

## Launched

- Started the res-s4 runner hidden with a 10,800-second budget and output lane `sessions/R3-4c-fold/`.
- Confirmed a Hermes process for res-s4 exists after launch. res-s1 remained the other active Hermes session; no third session was started.
- Runner file: `ops/hermes_runner.ps1`; prompt: `sessions/R3-4c-fold/PROMPT-R3.txt`.

## Open risks

- The lane must fold a large set of issues without adding unregistered numbers or concealing items that lack support.
- It must preserve the valid pre-fold status of round-3 scores and avoid launching another review round.
- It must keep outside-owned files, especially `05_paper/latex-build/**`, untouched.
- Final gates remain for the lead to verify: changed draft SHA, 0 number findings, and check_all 4/4 PASS.

## Claude Code should watch before resuming Codex

- Read the res-s4 process/runner state and `sessions/R3-4c-fold/PROGRESS.md`; do not infer completion from process existence alone.
- Check that `PROMPT-R3.txt` contains no double quotes and the process command line uses profile res-s4.
- Confirm `05_paper/template/draft_template.md` changed and the generated draft hash changed from baseline.
- Check that comparison scores are explicitly for the pre-fold draft and no additional review files were generated.
- Re-run `python tools/check_numbers.py --draft 05_paper/draft/paper.md` and `python tools/check_all.py`; require 0 findings and 4/4 PASS.
- Verify response-letter coverage for all 44 round-2 and 41 round-3 items, unresolved statuses, and no invented numbers.

## Round-3 must-fix inventory

**Persisted (22):**
1. Rung-separability 0.977 may encode gold-paragraph identity.
2. D4 is outside the preregistration hash chain.
3. Frozen/corrected Table 6 cuts differ and corrected exploratory coverage is omitted.
4. H1/H3 verdict language conflicts with not-exercisable wording and exploratory direction.
5. Abstract mixes frozen R5 and corrected R4 values.
6. Held-out R2 and exchangeability counts are incomplete.
7. SQuAD's own unanswerable questions are not evaluated.
8. A fine-tuned answerability baseline is absent.
9. A field companion metric such as AURC/F1/EM is absent.
10. Coverage/over-refusal uncertainty is missing.
11. AUROC uncertainty is missing across runs and ablations.
12. Reader baseline subset selection and interval are unclear.
13. Cluster bootstrap has only 17 dev and 18 test articles.
14. Exploratory per-rung precision intervals are absent.
15. Novelty search details are not documented in the draft.
16. DeclineCraft's taxonomy relation to the rungs is unclear.
17. Frozen preregistration hash appears as `#`.
18. Abstract says six features separate no rung while R4 is inverted separation.
19. Abstract orders R5 incorrectly relative to R2/R3.
20. Abstract confuses over-refusal and per-rung precision.
21. Table 5 mislabels conditionals as abstain precision.
22. `abstain recall` is undefined.

**New in round 3 (19):**
1. Leave-one-group-out ablations vary feature count and refit thresholds without a fixed-capacity control.
2. IDF scope for R2 construction and possible held-out leakage are unstated.
3. R4 answer-span substitutions lack human validation/agreement evidence.
4. Sampling method and article counts per split are unstated.
5. Related work omits answerability-detection/selective-classification work.
6. Table 5 control arms omit sample sizes and intervals.
7. No single-sentence mechanism/design delta versus Abdumalikov et al.
8. Primary coverage-risk/reject-option literature may be omitted.
9. The claimed audit contribution lacks evidence distinguishing its components from standard leakage checks.
10. Ho et al. arXiv identifier and abstention-survey author list have citation-hygiene defects.
11. Article split and item-sampling seeds are missing.
12. Pinned environment/lockfile and hardware/software details are missing.
13. Headline numbers lack per-table run IDs/output paths and commands.
14. Code license is unstated.
15. Logistic-regression and gate hyperparameters are unspecified.
16. A small smoke-test command and full-run resource needs are undocumented.
17. R4 replacement rule and reader model/version are unnamed.
18. Abstract generalizations exceed the one-corpus/feature-stack/gate scope.
19. Figure 1 mentions spec-corrected bands before their introduction.

## Launch evidence

Runner PowerShell PID: 42664. Hermes res-s4 PID: 27668. The prompt contains no double quotes. Launch used `ops/hermes_runner.ps1` with profile res-s4 and budget 10800.
