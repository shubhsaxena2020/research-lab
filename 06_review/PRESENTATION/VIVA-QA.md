# VIVA-QA — the 25 hardest questions a teacher or reviewer could ask

For Shubh. Short, honest answers. Every number is copied from
`05_paper/draft/paper.md` (draft as of 2026-11-08; may change in round 3).
Where a number comes from a round-2 review item rather than the draft, it is
labelled "(MF-n)". Pointers are to sections of the draft.

---

## Q1. Did you write this yourself?

**Answer:** No, not alone, and I say so in the paper. Language-model agents wrote
analysis code, ran the experiments, drafted sections, and performed the *simulated*
review; I directed the work, hold the author position, and am expected to explain
every section. The simulated review is labelled as a simulation, not a venue
decision (§7; RULES #4). Code, seeds and raw outputs are committed beside the
scripts. I am the responsible author; the agent is a tool.

## Q2. Your headline says "abstain precision 100.00%" but also "75.50% over-refusal" — how can both be precision?

**Answer:** They are not both precision, and that is the defect the round-2 review
caught (MF-1, MF-8, MF-15, MF-39). The 100.00% cells are refusal *rates*,
P(refused | negative) = 400/400, 279/280, 400/400, 399/399. "Precision",
P(negative | refused), is 56.98% on R1 and 48.02% on R2; pooled 83.03%. The
pre-registration called the refusal rate "abstain precision" and defined it as a
recall. I now report both, always labelled: refusal rate (the quantity H1/H3 are
stated over) and precision (§3.5, Table 1).

## Q3. Why does your gate answer only 24.50% of the questions it is asked?

**Answer:** Because the registered rule — maximise dev abstain recall subject to
dev precision 0.80 — has no coverage cap, and the lower threshold alone refuses
92.95% of dev items; dev admit mass is 6.03%. The gate satisfies the rule by
refusing almost everything (over-refusal 75.50%). That is the pathology finding,
not a feature: a precision target without a coverage constraint is not a
specification (§5.1, §3.3).

## Q4. H1 is refuted — doesn't that mean negative hardness does not matter?

**Answer:** No. At the registered point three rungs sit at 100.00% and R2 at
99.64%, so the quantity is undefined there and the CI [0.00, 0.00] is a
boundary bootstrap (MF-5, MF-25). The exploratory operating point (coverage cap
10%) shows a 7.00-point R1–R3 drop, 95% CI [4.50, 9.75] — real, but half the
pre-registered 15-point criterion, and not monotone (R2 below R3). So hardness
matters; the registered point cannot measure it (§4.2, §4.3, Table 2).

## Q5. H3 says a two-sided band beats a single threshold — you found zero difference. Isn't that because you built the comparison to be degenerate?

**Answer:** The matched single threshold equals the band's lower threshold to five
decimals (0.9072), so the upper threshold never binds and there are zero
discordant pairs (MF-29). H3 is refuted by construction at that point. Worse, on
corrected features the band is *below* the matched single by 2.23 points
(95% CI [−3.11, −1.35]); the matched single's dev precision also falls below
0.80, so that comparison is descriptive, not the registered test (§4.6, MF-19).

## Q6. H2 "transfers" with a 0.07% loss — isn't that a strength you are downplaying?

**Answer:** No. A gate that refuses 92.95% of dev items on its lower threshold
cannot fail to transfer; that is robustness of the trivial kind and I do not
present it as stability (§4.2). The second-corpus leg is inconclusive under the
registered rule: a 7.25-point drop lands in the undefined 5–10 point gap, with
over-refusal 57.50% there against 9.50% on the main corpus and AUROC falling
from 0.982 to 0.640 (§4.8, MF-6).

## Q7. Your dense features were degenerate. How can any number be trusted?

**Answer:** In the frozen run the dense query was the presented passage itself, so
`dense_presented` == `dense_top1`, dense cosine was exactly 1 on 78.70% of rows
(every R0–R3 row, none of R4), and `dense_rank_log` was constant — ten informative
columns, not twelve. I report the frozen run exactly as produced and the
spec-corrected re-implementation (question-to-passage cosine) as a declared
sensitivity analysis: AUROC 0.982 → 0.874, exploratory R4 refusal 84.71% → 12.53% (band R4 refusal 100.00% → 90.73%). Both
runs are in the paper; neither substitutes for a fresh pre-registered replication
(§4.6, Table 4).

## Q8. You call D4 a "declared deviation" but the hash chain stops at D3. Why?

**Answer:** Honestly: it is not declared. `PREREGISTRATION.sha256` holds three
hashes (frozen, D1, D2+D3) and the deviation log stops at D3 (MF-4, MF-32).
D4 is a post-hoc sensitivity analysis. §5.3 recommends the corrected numbers for
carrying forward, but that is a recommendation, not a claim that D4 was
pre-registered. I should label it post hoc wherever cited.

## Q9. Your audit's 0.977 confounds rung hardness with "is this the gold paragraph."

**Answer:** Correct limitation (MF-7). The audit runs on items where answerables
always present the gold paragraph, so 0.977/0.889/0.923 measure overlap
identifiability, not pure hardness. The fix is to re-run the six-surface-plus-
overlap audit inside the D3 top-1-presented items, where rung 0 is not always
gold. The overlap-augmented audit is also not in the frozen pre-registration and
has no deviation entry (MF-24); it should be labelled post hoc.

## Q10. The audit is one-sided, so R4's 0.415 "passes."

**Answer:** Yes. The audit flags only separation in the expected direction;
R4's 0.415 is the same magnitude with the sign flipped and is reported as that,
not as a clean pass (§3.4). It should be a two-sided rule on |AUROC − 0.5| with
intervals, with split and n stated (MF-13). R5 is closest to the gate on surface
features (0.721) without crossing 0.750.

## Q11. No negative in your study has an adjudicated answerability label.

**Answer:** True (MF-10). "Negative" means "not the gold paragraph," not
"does not answer the question." R2/R3 passages may still support the question.
Needed: two-annotator adjudication of ≥100 R2/R3 passages with kappa, plus
SQuAD 2.0's impossible rows as a human-labelled anchor rung. I do not claim
adjudicated labels.

## Q12. "One axis at a time" is contradicted by your own length observation.

**Answer:** Acknowledged (MF-11, §3.1). Rungs also differ in length and
provenance; R5 is the longest negatives in the ladder. Hardness is not
identified with any single axis. Needed: per-rung length and overlap
distributions and one rung matched on both overlap and length (§4.4).

## Q13. Your reader baseline is a fluency proxy, not P(True).

**Answer:** Yes (MF-12). Mean generated-token log-probability on 553 dev items
gives AUROC 0.419 — worse than chance — because the reader emits a fixed refusal
string at near-certainty, so a correct refusal scores as high confidence. It
measures fluency, not evidential support. Reported as exploratory; not used to
rank gates. It is not evidence that reader-side gating fails on this task.

## Q14. Your coverage denominator understates coverage by about a factor of five.

**Answer:** Coverage is computed over items (four negatives per question). Question-
level coverage is 98/400 = 24.50%, which is what "answers one in four" means;
the item-level figure is much lower (MF-9, MF-38). The abstract's two headline
numbers sit on different denominators and must be restated over one population.
AURCC/abstention F1 should accompany (MF-9).

## Q15. The R4 "swapped answer breaks the gate" claim rests on one post-hoc exploratory cell.

**Answer:** The registered (band) R4 refusal is 100.00% and the frozen exploratory R4 refusal is 84.71%; the 12.53% figure is the
corrected *exploratory* run (MF-14). The "swapped answer breaks the gate" claim
is bounded to the corrected run. Either promote D4 to primary (title/abstract)
or report the frozen 84.71% beside the corrected 12.53% and restrict §5.2 to what the registered run
supports. I report both and keep the claim scoped (§4.6).

## Q16. Your zero-width CIs are boundary artefacts.

**Answer:** H1 and H3 CIs are [0.00, 0.00] because every item in those
comparisons is refused, so every paired difference is zero (MF-16). The primary
evidence should be discordant counts: 0 of 400 pairs (H1), 0 of 1479 (H3), with
the interval called degenerate. There is also a BCa-vs-percentile method mismatch
to reconcile (§3.6).

## Q17. No AUROC in the paper carries an interval.

**Answer:** True (MF-17). The bootstrap intervals rates, not ranking statistics.
Needed: a paired bootstrap 95% CI on the AUROC difference for 0.982 vs 0.874
over the 1879 held-out items, plus intervals for 0.945, 0.640 and 0.977, with
the number of held-out articles stated. I do not claim significance for the
0.982 → 0.874 drop.

## Q18. Your cluster bootstrap rests on few articles and a misquoted ratio.

**Answer:** Clustering resamples whole articles; the draft does not state how many
held-out articles there are (MF-18 flags this). Four of five comparable cluster
intervals are narrower than item intervals (narrowest 0.45 ratio, not 0.851 as
the draft says), one is wider (1.17); two cells are zero-width at both levels.
Rung-1 and rung-3 cluster intervals should be shown, not described (§4.7).

## Q19. The corrected H3 comparison is not at matched recall and violates the 0.80 constraint.

**Answer:** The corrected band operates at recall 0.9898 against the matched
single's 0.9925, and the matched single's dev precision is 0.7886, below the
0.80 constraint (MF-19, from review evidence, not the draft). So −2.23% is a
descriptive difference, not the registered test. It must be re-matched and
re-reported before any verdict.

## Q20. The corrected exploratory arm reports 11.00% over-refusal against a 0.10 cap.

**Answer:** The cap binds on dev, not the held-out half; the corrected dev
over-refusal should be stated (MF-20). The 11.00% held-out figure is a breach
and is reported rather than hidden; the constraint is on dev precision/recall,
not held-out over-refusal (§4.6).

## Q21. "No single feature group carries the result" is supported only by point estimates.

**Answer:** Table 6's eight subsets are point estimates without intervals
(MF-21). Needed: paired bootstrap 95% CIs for all_12 vs no_dense (0.874 vs
0.862) and vs dense_only (0.874 vs 0.870) over the same 1879 items. I do not
claim equivalence from point estimates.

## Q22. The rung-2 shortfall is never stated and exchangeability is only checked on dev.

**Answer:** Held-out kept 280 of 400 sampled questions; dev kept 273 of 400 with
127 dropped (MF-22). The exchangeability check (question length, answer surface
type, gold paragraph length, article size) reports only dev figures; the smallest
dev p-value is 0.052 on question length. Held-out per-variable p-values are
needed (§3.1, §4.7).

## Q23. Table 7 omits five near neighbours from your own search.

**Answer:** True (MF-23). Table 7 lists only Abdumalikov et al. and DeclineCraft;
the project's search (84 OpenAlex + 91 arXiv queries, 2026-11-03) marks five
closer works: N1 (arXiv:2502.07255), N2 (arXiv:2609.22056), N3
(doi:10.32604/cmc.2026.088937), N4 (arXiv:2609.32269) and N10. Rows and a
differentiating paragraph for each are needed, including what §4.1's audit adds
beyond N4's surface-only adversary (AUROC 0.979).

## Q24. Can anyone actually reproduce your numbers?

**Answer:** Not yet cleanly (MF-30, MF-31, MF-33, MF-37). There is no
requirements/lockfile or model revisions; the frozen run records
`preregistration_sha256` as `#` (parser defect, not freeze defect); §8 omits
`build_transfer_items.py` and `reader_logprob.py`; the frozen run came from a
dirty tree with no stored diff. Fix: pinned environment, correct hash, full
command list, run from a clean recorded commit. I state these as open items, not
as done.

## Q25. R5 is mis-ordered and "ladder of lexical overlap" overstates.

**Answer:** R5's exploratory refusal is 89.25% (95% CI [85.75, 91.75]), placing
it between R2 (91.07%) and R4 (84.71%), not between R2 and R3 (MF-27).
Overlap-matching does not defeat the gate; R5 is also the longest negatives and
its surface audit (0.721) is closest to the gate. "Ladder of lexical overlap"
should be rewritten: overlap separates each rung from answerable items, with the
R2 91.07 vs R3 92.75 inversion and R5 89.25 stated beside it (MF-26). Overlap
is not the whole story (§4.4).
