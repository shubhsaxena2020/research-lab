# Aggregate simulated review - round 1

- Generated: 2026-11-03T00:19:51Z
- Source: `06_review/reviews/round1-c1`
- Draft: `05_paper/draft/paper.md` (sha256 `0ab8c4f33e2d`)
- Reviews: 5 of 6 personas (methodologist, statistician, novelty_skeptic, reproducibility_reviewer, clarity_reviewer)

> **This is a simulation, not a real review.** The personas were written by the
> project, the reviews were filled in by the authors or an agent, and no venue or
> external reviewer was involved. Use it to find and track defects; do not read the
> scores as a prediction of acceptance.

## Scores

| Persona | Soundness (1-4) | Presentation (1-4) | Contribution (1-4) | Confidence (1-5) | Overall (1-10) | Decision |
|---|---:|---:|---:|---:|---:|---|
| methodologist | 2 | 3 | 2 | 4 | 4 | borderline |
| statistician | 2 | 3 | 2 | 4 | 4 | borderline |
| novelty_skeptic | 3 | 3 | 1 | 3 | 3 | reject |
| reproducibility_reviewer | 3 | 2 | 2 | 4 | 5 | borderline |
| clarity_reviewer | 3 | 3 | 2 | 3 | 4 | borderline |
| **Mean (n=5)** | 2.60 | 2.80 | 1.80 | 3.60 | 4.00 | - |
| **Median** | 3 | 3 | 2 | 4 | 4 | - |

Overall: mean **4.00**, median **4**, range 3-5, sd 0.71 (n=5).

## Decision distribution

| Decision | Count | Personas |
|---|---:|---|
| reject | 1 | novelty_skeptic |
| borderline | 4 | methodologist, statistician, reproducibility_reviewer, clarity_reviewer |
| accept | 0 | - |

## Must-fix, ranked (12 distinct items from 12 raised)

Ranked by how many distinct personas raised the item, then by how often it was
raised. Near-identical wording is merged; the exact phrasings are kept below the
table so nothing is lost.

| Rank | Reviewers (n) | Claim | Evidence needed |
|---:|---:|---|---|
| 1 | 1 (methodologist) | The gate can identify rung-0 items from construction artefacts, so the separation may not measure answerability. | Held-out AUROC and per-rung precision without rank features, plus a variant where every presented passage is the top-1 retrieved document. |
|  |  | _Where:_ Section 3.2, Section 4.2 |  |
| 2 | 1 (methodologist) | No ablation isolates which retrieval features carry the result. | Per-rung abstain precision for leave-one-out variants: without overlap, without ranks, without the cross-encoder. |
|  |  | _Where:_ Section 4.2 |  |
| 3 | 1 (methodologist) | Rung 2 is reported at 68% of designed size with no exchangeability check. | Comparison of question length and answer type between the 273 kept and 127 dropped rung-2 dev questions. |
|  |  | _Where:_ Section 3.1, Table 1 |  |
| 4 | 1 (statistician) | The exploratory per-rung precisions that carry the ladder claim have no uncertainty. | BCa intervals at the frozen seed for each exploratory per-rung precision and for the rung 1 minus rung 3 difference. |
|  |  | _Where:_ Section 4.3 |  |
| 5 | 1 (statistician) | Intervals ignore clustering of questions within articles. | A cluster bootstrap by article reported alongside the item bootstrap for the primary per-rung precisions. |
|  |  | _Where:_ Section 3.5 |  |
| 6 | 1 (statistician) | 'Matched abstain recall' is asserted but the matched test recalls are not shown. | A row reporting band recall and matched-single recall on the held-out half. |
|  |  | _Where:_ Section 4.2 |  |
| 7 | 1 (novelty_skeptic) | Title and abstract promise a hardness effect the confirmatory result refutes, while the real finding sits in a deviation log. | Either a title and abstract leading with the coverage-precision finding, or a second corpus showing the ladder effect at a non-degenerate operating point. |
|  |  | _Where:_ Title, Abstract, Section 4.3 |  |
| 8 | 1 (novelty_skeptic) | Prior work is named but not compared. | A table comparing this setup with the closest benchmark on data, metric, negative construction and reported operating point. |
|  |  | _Where:_ Section 2 |  |
| 9 | 1 (reproducibility_reviewer) | The draft references generated tables by path instead of including them, so the paper contains no results tables. | Tables inlined (or \input in LaTeX) with the generated content and no hand-edited cells. |
|  |  | _Where:_ Section 4.1, Section 4.2 |  |
| 10 | 1 (reproducibility_reviewer) | The numbers audit does not pass on the draft, which is a hard gate in this project's own rules. | A zero-finding run of tools/check_numbers.py on the draft, or a per-finding justification. |
|  |  | _Where:_ Section 4 |  |
| 11 | 1 (clarity_reviewer) | The abstract's first reported numbers are the degenerate ones, so the finding is invisible to a skimming reader. | An abstract whose first quantitative sentence is the over-refusal figure and its consequence. |
|  |  | _Where:_ Abstract |  |
| 12 | 1 (clarity_reviewer) | Four-decimal reporting overstates precision relative to the reported intervals. | Two decimals for rates and three for AUROC, consistent with Section 6's own rule. |
|  |  | _Where:_ Abstract, Section 4 |  |

## Rebuttal tracker seed

Copy this into the response tracker. Every item must end as a change (with the
file or diff) or a rebuttal (with a citation or result) - never as silence.

- [ ] **MF-1** (1 reviewer(s): methodologist) The gate can identify rung-0 items from construction artefacts, so the separation may not measure answerability.  
      evidence to supply: Held-out AUROC and per-rung precision without rank features, plus a variant where every presented passage is the top-1 retrieved document.
- [ ] **MF-2** (1 reviewer(s): methodologist) No ablation isolates which retrieval features carry the result.  
      evidence to supply: Per-rung abstain precision for leave-one-out variants: without overlap, without ranks, without the cross-encoder.
- [ ] **MF-3** (1 reviewer(s): methodologist) Rung 2 is reported at 68% of designed size with no exchangeability check.  
      evidence to supply: Comparison of question length and answer type between the 273 kept and 127 dropped rung-2 dev questions.
- [ ] **MF-4** (1 reviewer(s): statistician) The exploratory per-rung precisions that carry the ladder claim have no uncertainty.  
      evidence to supply: BCa intervals at the frozen seed for each exploratory per-rung precision and for the rung 1 minus rung 3 difference.
- [ ] **MF-5** (1 reviewer(s): statistician) Intervals ignore clustering of questions within articles.  
      evidence to supply: A cluster bootstrap by article reported alongside the item bootstrap for the primary per-rung precisions.
- [ ] **MF-6** (1 reviewer(s): statistician) 'Matched abstain recall' is asserted but the matched test recalls are not shown.  
      evidence to supply: A row reporting band recall and matched-single recall on the held-out half.
- [ ] **MF-7** (1 reviewer(s): novelty_skeptic) Title and abstract promise a hardness effect the confirmatory result refutes, while the real finding sits in a deviation log.  
      evidence to supply: Either a title and abstract leading with the coverage-precision finding, or a second corpus showing the ladder effect at a non-degenerate operating point.
- [ ] **MF-8** (1 reviewer(s): novelty_skeptic) Prior work is named but not compared.  
      evidence to supply: A table comparing this setup with the closest benchmark on data, metric, negative construction and reported operating point.
- [ ] **MF-9** (1 reviewer(s): reproducibility_reviewer) The draft references generated tables by path instead of including them, so the paper contains no results tables.  
      evidence to supply: Tables inlined (or \input in LaTeX) with the generated content and no hand-edited cells.
- [ ] **MF-10** (1 reviewer(s): reproducibility_reviewer) The numbers audit does not pass on the draft, which is a hard gate in this project's own rules.  
      evidence to supply: A zero-finding run of tools/check_numbers.py on the draft, or a per-finding justification.
- [ ] **MF-11** (1 reviewer(s): clarity_reviewer) The abstract's first reported numbers are the degenerate ones, so the finding is invisible to a skimming reader.  
      evidence to supply: An abstract whose first quantitative sentence is the over-refusal figure and its consequence.
- [ ] **MF-12** (1 reviewer(s): clarity_reviewer) Four-decimal reporting overstates precision relative to the reported intervals.  
      evidence to supply: Two decimals for rates and three for AUROC, consistent with Section 6's own rule.

---

_Generated by `tools/simulate_review.py aggregate`. Scores are diagnostics for
revision, not a venue decision._
