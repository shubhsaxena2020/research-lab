# How Hard Are Your Negatives? A Pre-Registered Audit of Negative Ladders for Retrieval-Feature Abstention Gates, with a Negative Result

*Student author: Shubh (PSIT, BCA, first semester). Analysis and code: agent-assisted, human-directed (§7).
Draft generated from `05_paper/template/draft_template.md` by `05_paper/build_draft.py`; every table
below is written by `04_experiments/src/make_paper_assets.py` from a results file, and every numeral is
bound to `04_experiments/RESULTS-INDEX.json`.*

*Pre-registration: the pre-registration file in the experiments directory, whose three recorded hashes
(frozen, then two amendments) cover the declared deviations D1–D3.*

## Abstract

An abstention gate for retrieval-augmented question answering decides whether the retrieved passage
supports an answer. How hard such a gate looks depends on the negatives it is measured against, and we
tested that dependence with a pre-registered four-rung ladder over SQuAD v2.0 dev, fitting the gate and
both of its thresholds on a disjoint half. The result is negative and specific. The registered rule —
maximise abstain recall subject to a dev abstain precision of
<!-- num:c1.const.target_precision -->0.80<!-- /num --> — produced a gate that refuses
<!-- num:c1.band.over_refusal.run -->75.50%<!-- /num --> of answerable questions, so it answers only
<!-- num:c1.pm.band.answer_rate -->24.50%<!-- /num --> of the questions it is asked, and the precision of
the items it refuses is <!-- num:c1.pm.band.pooled_precision -->83.03%<!-- /num --> pooled. At that
operating point the quantity the ladder was built to move stops moving: the per-rung refusal rate is
<!-- num:c1.pm.band.refusal.r1 -->100.00%<!-- /num -->,
<!-- num:c1.pm.band.refusal.r2 -->99.64%<!-- /num -->,
<!-- num:c1.pm.band.refusal.r3 -->100.00%<!-- /num --> and
<!-- num:c1.pm.band.refusal.r4 -->100.00%<!-- /num --> (H1 refuted, R1 minus R3 =
<!-- num:c1.h1.diff -->0.00%<!-- /num -->, 95% CI [<!-- num:c1.h1.lo -->0.00%<!-- /num -->,
<!-- num:c1.h1.hi -->0.00%<!-- /num -->]), a two-sided band is indistinguishable from the one-sided
threshold it was meant to beat (H3 refuted, difference <!-- num:c1.h3.diff -->0.00%<!-- /num -->, 95% CI
[<!-- num:c1.h3.lo -->0.00%<!-- /num -->, <!-- num:c1.h3.hi -->0.00%<!-- /num -->]), and dev-to-held-out
transfer is trivial rather than informative (H2 degenerate, loss
<!-- num:c1.h2.loss -->0.07%<!-- /num -->). The audit that produced that verdict is the useful part. Six
surface features separate no rung from answerable items (AUROC
<!-- num:c1.audit.surface.r1 -->0.506<!-- /num -->, <!-- num:c1.audit.surface.r2 -->0.539<!-- /num -->,
<!-- num:c1.audit.surface.r3 -->0.488<!-- /num -->, <!-- num:c1.audit.surface.r4 -->0.415<!-- /num -->);
adding question–passage overlap to the same six features separates the first three almost perfectly
(<!-- num:c1.audit.surface_lex.r1 -->0.977<!-- /num -->, <!-- num:c1.audit.surface_lex.r2 -->0.889<!-- /num -->,
<!-- num:c1.audit.surface_lex.r3 -->0.923<!-- /num -->). The refusals are mostly answerable questions, which
is what an over-refusal of <!-- num:c1.band.over_refusal.run -->75.50%<!-- /num --> means: the band's
precision is
<!-- num:c1.pm.band.precision.r1 -->56.98%<!-- /num --> on R1 and
<!-- num:c1.pm.band.precision.r2 -->48.02%<!-- /num --> on R2. The ladder, in other words, is a ladder of
lexical overlap, which is exactly what a retrieval-feature gate scores. Two control arms make that
concrete: an overlap-matched rung (R5, exploratory) is still refused at
<!-- num:c1.r5.precision.expl -->89.25%<!-- /num -->, while the rung that changes what the passage *says*
rather than how much of it overlaps (R4, one answer span replaced inside the gold passage) breaks the gate
once the dense features are implemented as specified — refusal on R4 falls to
<!-- num:c1.expl.precision.r4.corr -->12.53%<!-- /num --> and discrimination from
<!-- num:c1.auroc.test.run -->0.982<!-- /num --> to <!-- num:c1.auroc.test.corr -->0.874<!-- /num --> AUROC.
We report this as a negative result for the gate and a positive one for the audit: an abstention precision
is not interpretable without its coverage, and a negative-ladder result is not interpretable without an
overlap control.

## 1 Introduction

A retrieval-augmented system that always answers will sometimes answer from a passage that does not
support the question. An abstention gate is the component that decides, before generation, whether to
answer from the passage it was given. Gates are built from retrieval signals — lexical scores, dense
cosine, reranker scores — and they are evaluated against a set of negatives that is usually described in
one sentence.

That sentence matters. Abdumalikov et al. (arXiv:2403.01461) train on random negative excerpts, then
evaluate on excerpts with high semantic overlap, and report accuracy falling from
<!-- num:c1.lit.acc.random -->98%<!-- /num --> to <!-- num:c1.lit.acc.overlap -->1%<!-- /num -->. A gate
measured only on random negatives would look finished. The honest reading of that result is not that
gates are bad; it is that the negative sampler, not the gate, was doing most of the work in the earlier
numbers.

So we designed a measurement rather than a method. One corpus (SQuAD v2.0 dev, arXiv:1806.03822), one
question set, one feature extractor, one fitting procedure, and four rungs of negatives that differ only
in how they were constructed. Three hypotheses were frozen before the first result-producing run:

- **H1 (hardness monotonicity).** Abstain precision is non-increasing across the rungs and falls by at
  least fifteen points from R1 to R3.
- **H2 (operating-point transfer).** The dev-fitted operating point loses at least ten points of abstain
  precision at equal abstain recall when applied to a disjoint held-out half and to a second corpus.
- **H3 (two-sided beats one-sided).** A two-threshold band beats the best single threshold on the same
  score, by at least five points, at matched abstain recall.

The pre-registered analysis refutes H1 and H3 and leaves H2 degenerate, and we say so in the abstract
rather than in a footnote. That is the first contribution, and it is a negative one: at a precision
target without a coverage constraint, a gate can satisfy the target by refusing almost everything, and
when it does, the quantity the ladder is supposed to measure stops existing.

The second contribution is the instrument that made the negative result legible:

1. **A reproducible four-rung ladder** over a closed public corpus, with item counts, drop rates and
   construction code another lab can re-run (§3.1).
2. **A separability audit as a hard gate**, run before any result is reported: a classifier that sees
   only surface properties of the text must not be able to tell a rung's negatives from answerable
   items, or the rung is measuring formatting (§3.4, Table 3). Its sensitivity variant — the same
   features plus question–passage overlap — is what turns the audit from a formatting check into a
   measurement of what the rungs actually vary.
3. **A measurement of the coverage–precision pathology** in gate fitting, with the numbers beside every
   precision figure, and the observation that a two-sided band buys nothing when the admit region is
   degenerate (§4.2, Table 2).
4. **Two control arms that localise the effect**: overlap-matched negatives (R5) and a top-1-presented
   variant in which every item shows the retriever's first choice (§4.4, §4.5, Table 5). Together they
   say what the gate is really measuring.
5. **An implementation correction, disclosed** (§4.6, Table 4): the frozen run's dense block was
   degenerate because the presented passage was used as its own dense query. Re-implementing the
   feature as specified lowers held-out AUROC and changes which rung is hard. We report both runs.

We do not claim novelty, state of the art, or generality beyond one corpus family, one feature stack, one
gate family and English passage-level question answering.

## 2 Related work

**Abstention and selective prediction.** Surveys of abstention in language models (arXiv:2407.18418)
organise the space by what the model is uncertain about — the query's answerability, the model's own
confidence, or the values at stake — and our gate addresses only the first of those. **Negative choice in
answerability.** The collapse from near-perfect to near-zero accuracy when random-negative training is
tested on high-overlap excerpts (arXiv:2403.01461) is the observation this paper is built on; our ladder
is a systematic version of its two conditions. **Benchmarks that join retrieval and generation
abstention.** DeclineCraft (arXiv:2610.28340) measures retrieval-side and parametric abstention jointly;
our ladder varies only the presented passage and never asks the model to rely on memory, so the two
designs are complementary rather than nested. **Retrieval components.** BM25 through the `bm25s`
implementation; dense retrieval with a small BGE English model (arXiv:2309.07597); cross-encoder
reranking in the passage-reranking tradition (arXiv:1901.04085) with the `ms-marco-MiniLM-L-6-v2`
weights; dense passage retrieval as a baseline reference (arXiv:2004.04906). **Model confidence as a
gate.** Eliciting a model's probability that a proposed answer is true (arXiv:2207.05221) is the
strongest cheap reader-side baseline a reviewer expects; we ran a weaker reader signal — mean
generated-token log-probability — and report why it failed here (§4.7). Table 7 sets the closest work
beside this one on data, negatives, metric and reported operating point.

**Table 7.** The closest work, compared on data, negative construction, metric and the operating point it reports.

| Work | Data | Negatives | Metric | Operating point reported |
|---|---|---|---|---|
| Abdumalikov et al., arXiv:2403.01461 | ODQA corpora, SQuAD v2.0 pairs for repair | random text excerpts versus excerpts with high semantic overlap | answerability accuracy | one accuracy figure per sampler; coverage not reported |
| DeclineCraft, arXiv:2610.28340 | retrieval and parametric abstention suite | several unanswerable classes | joint abstention metrics | per category, retrieval and memory reported separately |
| This paper | SQuAD v2.0 dev, article-disjoint split | four constructed rungs, plus overlap-matched and top-1-presented variants | abstain precision, over-refusal, coverage | every precision reported with over-refusal and coverage beside it |

## 3 Method

### 3.1 Items

SQuAD v2.0 dev (arXiv:1806.03822) contains
<!-- num:c1.data.articles -->35<!-- /num --> articles,
<!-- num:c1.data.paragraphs -->1204<!-- /num --> paragraphs and
<!-- num:c1.data.questions -->11873<!-- /num --> questions, of which
<!-- num:c1.data.answerable -->5928<!-- /num --> are answerable. Only the answerable rows are used;
impossible rows are a different kind of negative and are out of scope for this study. Articles are split
whole, never at paragraph level, into a dev half and a held-out half. From each half we sample four
hundred answerable questions and present each question with five passages, one per rung:

| Rung | Label | Presented passage |
|---|---|---|
| R0 | answerable | the question's gold paragraph |
| R1 | negative | a uniformly sampled other paragraph from the same split's pool |
| R2 | negative | a paragraph containing the question's highest-IDF content token |
| R3 | negative | the paragraph immediately before or after the gold paragraph, in the same article |
| R4 | negative | the gold paragraph with its first answer span replaced by a same-surface-type value |

The ladder therefore varies the negative along one axis at a time: unrelated text (R1), topically
anchored text (R2), adjacent text from the same document (R3), and text that is the gold passage except
for one span (R4). This yields <!-- num:c1.items.total -->3752<!-- /num --> items
(<!-- num:c1.items.test -->1879<!-- /num --> held out); R2 is short at
<!-- num:c1.items.rung2.dev -->273<!-- /num --> dev items because most questions have no content word that
occurs in a paragraph other than their own. Following the pre-registration the rung is reported at its
true size rather than topped up, and §4.7 checks that the questions which kept an R2 item are not
different from those which did not.

### 3.2 Features

<!-- num:c1.const.n_gate_features -->12<!-- /num --> retrieval-side features per item: the BM25 score and
log-rank of the presented passage, corpus top-1 and mean-top-5 scores, the top-1/top-2 margin; the same
four for dense cosine; whether BM25 and dense agree on the top document; the cross-encoder score of the
presented passage; and question–passage token overlap. A rung-4 passage is a rewrite rather than a corpus
document, so it inherits its source paragraph's rank and is flagged.

### 3.3 Gate and operating point

A logistic regression on standardised features, fitted on dev only, gives a score that is meant to read
as the probability that the presented passage answers the question. Two operating points are fitted on
dev, both constrained to the observed dev score range: a band that admits only inside two thresholds, and
a single threshold that admits above one. Both maximise dev abstain recall subject to a dev abstain
precision of <!-- num:c1.const.target_precision -->0.80<!-- /num -->. The fitted band is
[<!-- num:c1.thr.lo -->0.9072<!-- /num -->, <!-- num:c1.thr.hi -->0.9478<!-- /num -->], width
<!-- num:c1.band.width -->0.0406<!-- /num -->; the fitted single threshold is
<!-- num:c1.thr.single -->0.9394<!-- /num -->. All three sit inside the observed dev score range, so the
failure this paper reports is not a threshold placed outside the data: it is that the admissible region
is degenerate. Dev admit mass is <!-- num:c1.dev.admit_mass -->6.03%<!-- /num -->, and
<!-- num:c1.dev.refused_below_lo -->92.95%<!-- /num --> of dev items are refused by the lower threshold
alone.

### 3.4 Separability audit

Before any result is reported, a logistic regression on
<!-- num:c1.const.n_surface_features -->6<!-- /num --> surface features (characters, tokens, digit ratio,
upper-case ratio, punctuation ratio, mean word length) is fitted with
<!-- num:c1.const.cv_folds -->5<!-- /num -->-fold cross-validation, separately per rung, to tell that
rung's negatives from answerable items. Any rung above an AUROC of
<!-- num:c1.const.audit_gate -->0.750<!-- /num --> is rebuilt by length-matched resampling, at most twice;
if two or more rungs still fail after a rebuild the run stops and the audit is the finding. A sensitivity
variant adds question–passage overlap and question length to the same features. It is labelled a
sensitivity variant, not a surface check, because overlap is a retrieval signal and calling it surface
would measure whether retrieval works rather than whether a rung leaks its identity through formatting.

### 3.5 What the reported numbers are, and a correction to one name

The pre-registration names two quantities and then gives one estimator. It calls the per-rung figure
"abstain precision = P(negative | refused)" and defines it as "the mean of the refusal indicator over that
rung's negatives", which is P(refused | negative) — a recall on that rung. Round-2 review caught the
contradiction, and it matters: at the registered operating point the per-rung refusal rate saturates at
<!-- num:c1.pm.band.refusal.r1 -->100.00%<!-- /num --> while the precision of those same refusals is between
<!-- num:c1.pm.band.precision.r2 -->48.02%<!-- /num --> and
<!-- num:c1.pm.band.precision.r1 -->56.98%<!-- /num -->, because three quarters of the answerable questions
are refused alongside the negatives. We therefore report both, always labelled: **refusal rate** for
P(refused | negative), which is the quantity H1 and H3 are stated over and the one the pre-registration
called abstain precision, and **precision** for P(negative | refused), computed over the rung's items and
the answerable items together. Pooled precision is
<!-- num:c1.pm.band.pooled_precision -->83.03%<!-- /num --> at the registered point and
<!-- num:c1.pm.expl.pooled_precision -->97.29%<!-- /num --> at the exploratory point. No hypothesis is
restated over precision: the registered tests stay exactly as they were frozen, and the precision numbers
are descriptive.

### 3.6 Statistics

Item-level BCa bootstrap, <!-- num:c1.stats.n_boot -->10000<!-- /num --> resamples, seed
<!-- num:c1.stats.seed -->12345<!-- /num -->; paired comparisons resample items jointly; exact sign tests
for paired binary indicators; Holm correction over the two tests that carry p-values (H1 and H3; H2 has
none, because one side of it is the fitting half). Rates are reported to two decimals and AUROC to three,
in line with the precision the intervals support. AUROC itself carries no interval: the bootstrap used
here intervals rates, not ranking statistics, and the change from one run to another is reported as a
difference between two analyses rather than as a tested contrast.

## 4 Results

### 4.1 The audit passes, and says something uncomfortable

**Table 3.** Separability audit on dev: can a classifier that sees only surface properties tell this rung's negatives from answerable items? The overlap column is the sensitivity variant.

| Rung | Six surface features | + question–passage overlap | Gate |
|---:|---:|---:|---|
| R1 | <!-- num:c1.audit.surface.r1 -->0.506<!-- /num --> | <!-- num:c1.audit.surface_lex.r1 -->0.977<!-- /num --> | pass (gate <!-- num:c1.const.audit_gate -->0.750<!-- /num -->) |
| R2 | <!-- num:c1.audit.surface.r2 -->0.539<!-- /num --> | <!-- num:c1.audit.surface_lex.r2 -->0.889<!-- /num --> | pass (gate <!-- num:c1.const.audit_gate -->0.750<!-- /num -->) |
| R3 | <!-- num:c1.audit.surface.r3 -->0.488<!-- /num --> | <!-- num:c1.audit.surface_lex.r3 -->0.923<!-- /num --> | pass (gate <!-- num:c1.const.audit_gate -->0.750<!-- /num -->) |
| R4 | <!-- num:c1.audit.surface.r4 -->0.415<!-- /num --> | <!-- num:c1.audit.surface_lex.r4 -->0.408<!-- /num --> | pass (gate <!-- num:c1.const.audit_gate -->0.750<!-- /num -->) |
| R5 (exploratory) | <!-- num:c1.r5.audit.surface -->0.721<!-- /num --> | <!-- num:c1.r5.audit.lex -->0.794<!-- /num --> | pass (gate <!-- num:c1.const.audit_gate -->0.750<!-- /num -->) |

On the six pre-registered surface features no rung is separable from answerable items, so the ladder is
not a formatting artefact and the run is allowed to proceed. Add question–passage overlap to the same six
features and R1 becomes almost perfectly identifiable:
<!-- num:c1.audit.surface_lex.r1 -->0.977<!-- /num -->. That number is the paper's most transferable
single measurement. It says the rungs differ mainly in how much of the question the passage's words cover,
which is precisely what a lexical retriever scores, and it predicts the main result before the gate is
fitted. R4 is the exception: overlap does not identify it
(<!-- num:c1.audit.surface_lex.r4 -->0.408<!-- /num -->), because R4's passage *is* the gold passage.

### 4.2 At the pre-registered operating point the ladder disappears

**Table 1.** Held-out results per rung: the refusal rate the pre-registered tests are stated over, and the precision of those refusals.

| Rung | n | Band refusal rate | Band precision | Exploratory refusal rate | Exploratory precision |
|---:|---:|---:|---:|---:|---:|
| R1 | <!-- num:c1.pm.n.r1 -->400<!-- /num --> | <!-- num:c1.pm.band.refusal.r1 -->100.00%<!-- /num --> | <!-- num:c1.pm.band.precision.r1 -->56.98%<!-- /num --> | <!-- num:c1.pm.expl.refusal.r1 -->99.75%<!-- /num --> | <!-- num:c1.pm.expl.precision.r1 -->91.30%<!-- /num --> |
| R2 | <!-- num:c1.pm.n.r2 -->280<!-- /num --> | <!-- num:c1.pm.band.refusal.r2 -->99.64%<!-- /num --> | <!-- num:c1.pm.band.precision.r2 -->48.02%<!-- /num --> | <!-- num:c1.pm.expl.refusal.r2 -->91.07%<!-- /num --> | <!-- num:c1.pm.expl.precision.r2 -->87.03%<!-- /num --> |
| R3 | <!-- num:c1.pm.n.r3 -->400<!-- /num --> | <!-- num:c1.pm.band.refusal.r3 -->100.00%<!-- /num --> | <!-- num:c1.pm.band.precision.r3 -->56.98%<!-- /num --> | <!-- num:c1.pm.expl.refusal.r3 -->92.75%<!-- /num --> | <!-- num:c1.pm.expl.precision.r3 -->90.71%<!-- /num --> |
| R4 | <!-- num:c1.pm.n.r4 -->399<!-- /num --> | <!-- num:c1.pm.band.refusal.r4 -->100.00%<!-- /num --> | <!-- num:c1.pm.band.precision.r4 -->56.92%<!-- /num --> | <!-- num:c1.pm.expl.refusal.r4 -->84.71%<!-- /num --> | <!-- num:c1.pm.expl.precision.r4 -->89.89%<!-- /num --> |

Refusal rate is P(refused | a negative of that rung) — a recall on the rung, and the quantity the pre-registration labelled abstain precision. Precision is P(negative of that rung | refused), over that rung's items and the answerable items together. Pooled precision is <!-- num:c1.pm.band.pooled_precision -->83.03%<!-- /num --> at the registered point and <!-- num:c1.pm.expl.pooled_precision -->97.29%<!-- /num --> at the exploratory point; the band gate answers <!-- num:c1.pm.band.answer_rate -->24.50%<!-- /num --> of answerable questions, while its item-level coverage is much lower because every question contributes four negatives to the item count.

**Table 2.** The three pre-registered hypotheses, their criteria and their verdicts.

| Hypothesis | Pre-registered criterion | Observed | Verdict |
|---|---|---|---|
| H1 hardness monotonicity | R1 − R3 at least <!-- num:c1.crit.h1 -->15<!-- /num --> points, non-increasing | difference <!-- num:c1.h1.diff -->0.00%<!-- /num -->, 95% CI [<!-- num:c1.h1.lo -->0.00%<!-- /num -->, <!-- num:c1.h1.hi -->0.00%<!-- /num -->]; sequence is not non-increasing | REFUTED |
| H2 transfer | loss at least <!-- num:c1.crit.h2 -->10<!-- /num --> points; refuted if within <!-- num:c1.crit.h2.slack -->5<!-- /num --> points | dev-to-test loss <!-- num:c1.h2.loss -->0.07%<!-- /num --> | REFUTED (it transfers, degenerately) |
| H3 two-sided vs one-sided | band at least <!-- num:c1.crit.h3 -->5<!-- /num --> points ahead at matched recall | difference <!-- num:c1.h3.diff -->0.00%<!-- /num -->, 95% CI [<!-- num:c1.h3.lo -->0.00%<!-- /num -->, <!-- num:c1.h3.hi -->0.00%<!-- /num -->] | REFUTED |

Table 1 reports the refusal rate and the precision of those refusals per rung, for both operating points.
The band refuses <!-- num:c1.band.precision.r1.run -->100.00%<!-- /num -->,
<!-- num:c1.band.precision.r2.run -->99.64%<!-- /num -->,
<!-- num:c1.band.precision.r3.run -->100.00%<!-- /num --> and
<!-- num:c1.band.precision.r4.run -->100.00%<!-- /num --> of the four rungs' negatives, refuses
<!-- num:c1.band.over_refusal.run -->75.50%<!-- /num --> of answerable questions, and therefore answers
<!-- num:c1.pm.band.answer_rate -->24.50%<!-- /num --> of the questions it is asked. Three verdicts follow,
and none of them is the one the design was hoping for.

Figure 1 plots the same quantities across the four rungs for both runs
(`05_paper/figures/generated/F1_abstain_precision_by_rung.svg`); the flat as-run curves and the collapsed
corrected R4 are visible in it directly.

**H1 is refuted.** R1 minus R3 is <!-- num:c1.h1.diff -->0.00%<!-- /num --> with a 95% CI of
[<!-- num:c1.h1.lo -->0.00%<!-- /num -->, <!-- num:c1.h1.hi -->0.00%<!-- /num -->]; the sequence is not
non-increasing and the fifteen-point criterion is not met.

**H3 is refuted.** At the band's dev recall the recall-matched single threshold gives an identical
held-out refusal rate: the difference is <!-- num:c1.h3.diff -->0.00%<!-- /num --> with a 95% CI of
[<!-- num:c1.h3.lo -->0.00%<!-- /num -->, <!-- num:c1.h3.hi -->0.00%<!-- /num -->]. The band and the
matched single threshold refuse the same negatives to within
<!-- num:c1.st.match.maxdiff -->0.00<!-- /num --> points in every rung, and the band's only measurable
effect is worse over-refusal: <!-- num:c1.st.match.over.band -->75.50%<!-- /num --> against
<!-- num:c1.st.match.over.matched -->72.50%<!-- /num -->. Two-sidedness buys nothing when almost everything
is refused on the low side.

**H2 is degenerate rather than supported.** Dev pooled precision is essentially identical to held-out
pooled precision, a loss of <!-- num:c1.h2.loss -->0.07%<!-- /num -->, which the pre-registered rule counts
as refuted-in-the-direction-that-means-it-transfers. A gate that refuses
<!-- num:c1.dev.refused_below_lo -->92.95%<!-- /num --> of dev items on its lower threshold alone cannot
fail to transfer. This is robustness of the trivial kind and we do not present it as stability.

The precision figures show what those refusals contain:
<!-- num:c1.pm.band.precision.r1 -->56.98%<!-- /num --> of the band's refusals on R1 and
<!-- num:c1.pm.band.precision.r2 -->48.02%<!-- /num --> on R2 are that rung's negatives, so most of what the
gate refuses with such a high pre-registered "precision" is an answerable question. Dev precision at the
fitted band is <!-- num:c1.band.dev_precision -->83.69%<!-- /num -->, so the rule did exactly what it was
asked; what it was asked was not enough.

The two single-score baselines show what the gate is doing. A threshold on BM25 top-1 pooled abstain
precision of <!-- num:c1.b1.pooled -->1.69%<!-- /num -->: it can only buy precision by refusing nothing
useful. A dense-cosine score reaches <!-- num:c1.b2.pooled.run -->74.58%<!-- /num --> pooled — but in this
run that score is constant, so the figure is an artefact of a degenerate column rather than a baseline,
which is the defect §4.6 corrects.

### 4.3 Exploratory: constrain coverage and the ladder returns, partly

The registered rule is not the rule a practitioner would use, so before its numbers existed we declared a
second operating point (deviation D1): maximise dev recall subject to precision
<!-- num:c1.const.target_precision -->0.80<!-- /num --> and dev over-refusal at most
<!-- num:c1.const.over_cap -->0.10<!-- /num -->. It keeps over-refusal at
<!-- num:c1.expl.over_refusal.run -->9.50%<!-- /num --> with coverage
<!-- num:c1.expl.coverage.run -->25.44%<!-- /num -->, and the per-rung refusal rate now falls across the
ladder:
<!-- num:c1.expl.precision.r1.run -->99.75%<!-- /num -->,
<!-- num:c1.expl.precision.r2.run -->91.07%<!-- /num -->,
<!-- num:c1.expl.precision.r3.run -->92.75%<!-- /num -->,
<!-- num:c1.expl.precision.r4.run -->84.71%<!-- /num -->, while the precision of those refusals stays
between <!-- num:c1.pm.expl.precision.r2 -->87.03%<!-- /num --> and
<!-- num:c1.pm.expl.precision.r1 -->91.30%<!-- /num --> in every rung. The R1 to R3 drop is
<!-- num:c1.st.expl.diff -->7.00%<!-- /num --> with a paired-by-question 95% CI of
[<!-- num:c1.st.expl.lo -->4.50%<!-- /num -->, <!-- num:c1.st.expl.hi -->9.75%<!-- /num -->] — real, but
half the pre-registered fifteen-point criterion, and not monotone (R2 sits below R3). R1 to R4 is
<!-- num:c1.st.expl.r14 -->15.04%<!-- /num -->, CI [<!-- num:c1.st.expl.r14.lo -->11.53%<!-- /num -->,
<!-- num:c1.st.expl.r14.hi -->18.80%<!-- /num -->]. So the ladder is not invisible; it is bought out by
coverage at the registered point, and at a coverage-constrained point it appears at about half the
predicted size. This is exploratory, it rescues no hypothesis, and the confirmatory verdict stands.

### 4.4 Control arm: matching the overlap does not defeat the gate

If the rungs differ from answerable items chiefly in question–passage overlap, then a negative built to
match the gold paragraph's overlap should be the hardest possible negative for an overlap-driven gate. We
built it (deviation D2): for each sampled question, the candidate paragraph whose overlap with the
question is closest to the gold paragraph's overlap. Matching is as good as the pool allows rather than
exact — the mean absolute overlap difference is
<!-- num:c1.r5.match.mean_absdiff -->10.29%<!-- /num --> on the held-out half, against
<!-- num:c1.r5.match.contrast -->42.08%<!-- /num --> for a random negative, so R5 is closer to the gold
paragraph's overlap than any other rung.

**Table 5.** The control arms. All four numbers are refusal rates on the arm's own negatives, not precisions; precision is reported for the main ladder only (Table 1).

| Arm (all exploratory) | Abstain precision | 95% CI | Over-refusal | Discrimination |
|---|---:|---|---:|---:|
| Rung R5, confirmatory band | <!-- num:c1.r5.precision.conf -->100.00%<!-- /num --> | [<!-- num:c1.r5.ci.lo -->100.00%<!-- /num -->, <!-- num:c1.r5.ci.hi -->100.00%<!-- /num -->] | degenerate, see §4.4 | <!-- num:c1.r5.auroc -->0.974<!-- /num --> |
| Rung R5, exploratory band | <!-- num:c1.r5.precision.expl -->89.25%<!-- /num --> | [<!-- num:c1.r5.expl.ci.lo -->85.75%<!-- /num -->, <!-- num:c1.r5.expl.ci.hi -->91.75%<!-- /num -->] | matching residue <!-- num:c1.r5.match.mean_absdiff -->10.29%<!-- /num --> | <!-- num:c1.r5.auroc -->0.974<!-- /num --> |
| Second-corpus arm, confirmatory band | <!-- num:c1.tr.precision.conf -->98.50%<!-- /num --> | not informative | <!-- num:c1.tr.over_refusal.conf -->89.50%<!-- /num --> | <!-- num:c1.tr.auroc -->0.640<!-- /num --> |
| Second-corpus arm, exploratory band | <!-- num:c1.tr.precision.expl -->85.50%<!-- /num --> | [<!-- num:c1.tr.ci.lo -->79.50%<!-- /num -->, <!-- num:c1.tr.ci.hi -->89.50%<!-- /num -->] | <!-- num:c1.tr.over_refusal.expl -->57.50%<!-- /num --> | <!-- num:c1.tr.auroc -->0.640<!-- /num --> |
| Top-1 presented (hit rate <!-- num:c1.t1.hit.test -->78.25%<!-- /num -->) | <!-- num:c1.t1.precision.miss -->87.30%<!-- /num --> P(miss refused) | not informative | <!-- num:c1.t1.refuse.hit -->2.56%<!-- /num --> of hits refused | <!-- num:c1.t1.auroc -->0.945<!-- /num --> |

Every arm here is exploratory. R5 and the top-1 variant are declared deviations (D2, D3). The second-corpus arm is H2's pre-declared second corpus, but its construct differs (no article grouping, shorter passages, multi-hop questions), so it supports a direction claim only.

The gate is not defeated: R5's negatives are refused at
<!-- num:c1.r5.precision.expl -->89.25%<!-- /num --> (95% CI
[<!-- num:c1.r5.expl.ci.lo -->85.75%<!-- /num -->, <!-- num:c1.r5.expl.ci.hi -->91.75%<!-- /num -->]) at the
exploratory point, which places it between R2 (<!-- num:c1.expl.precision.r2.run -->91.07%<!-- /num -->) and
R4 (<!-- num:c1.expl.precision.r4.run -->84.71%<!-- /num -->) in the ordering. Overlap is therefore not the whole story: R5
items also differ in length (they are the longest negatives in the ladder), and the surface audit is
closest to its gate on this rung (<!-- num:c1.r5.audit.surface -->0.721<!-- /num --> on dev) without
crossing it. The honest reading is that a paragraph drawn from elsewhere in the corpus can be caught by
several correlated signals, and matching one of them is not enough to hide it.

### 4.5 Control arm: what the gate does when the passage is always the retrieved one

The first review round's top objection was that answerable items always present the gold paragraph while
negatives never do, so the gate may be reading "is this the document retrieval found" rather than
answerability. The pre-registered design cannot answer that, so we built the variant (deviation D3): every
item presents the BM25 rank-1 paragraph for its question, labelled answerable if that paragraph is the
gold paragraph. The retriever's first choice is correct for
<!-- num:c1.t1.hit.test -->78.25%<!-- /num --> of held-out questions, so this variant has a real mixture
of hits and misses rather than a constant label.

The same feature stack detects retrieval correctness at
<!-- num:c1.t1.auroc -->0.945<!-- /num --> AUROC on the held-out half, refuses
<!-- num:c1.t1.refuse.miss -->63.22%<!-- /num --> of retrieval misses and
<!-- num:c1.t1.refuse.hit -->2.56%<!-- /num --> of retrieval hits, and when it refuses, the passage is
usually a miss (P(miss refused) = <!-- num:c1.t1.precision.miss -->87.30%<!-- /num -->). That is a good
retrieval-correctness detector. It is also the reason the ladder result should be read carefully: in this
variant the label *is* retrieval correctness, so "detects misses" and "detects unanswerable passages"
coincide item for item, and the comparison cannot separate the two readings. It confirms the mechanism
the audit implies and it does not exculpate the gate.

### 4.6 The dense block was degenerate: a disclosed implementation correction

Two readers of the code, working separately, found the same defect, and it changes the numbers. In the
frozen implementation the dense query was the presented passage itself rather than the question, so
`dense_presented` and `dense_top1` were identical to each other, the dense cosine was exactly one on
<!-- num:c1.obs.dense.eq1 -->78.70%<!-- /num --> of as-run rows (every row of R0–R3, none of R4), and
`dense_rank_log` was constant;
the two dense columns also received the same fitted coefficient. The gate therefore had ten informative
columns, not twelve, and the dense-cosine baseline in §4.2 was a constant score.

We did not refit the registered analysis: the frozen run is reported exactly as it was produced. Instead
we implemented the feature as §3.2 specifies — a question-to-passage cosine — and re-ran the whole
analysis through the same code path as a declared sensitivity analysis (deviation D4). Table 4 puts the
two side by side, and Table 6 reports leave-one-group-out ablations on the corrected features.

**Table 4.** The pre-registered run and the spec-corrected re-implementation (D4), side by side. The two runs fit their thresholds on different dev score distributions, so the precision and coverage rows compare two operating points; the AUROC rows are threshold-free.

| Quantity | As run (frozen, D1) | Spec-corrected (D4) |
|---|---:|---:|
| Gate AUROC, dev | <!-- num:c1.auroc.dev.run -->0.988<!-- /num --> | <!-- num:c1.auroc.dev.corr -->0.887<!-- /num --> |
| Gate AUROC, held out | <!-- num:c1.auroc.test.run -->0.982<!-- /num --> | <!-- num:c1.auroc.test.corr -->0.874<!-- /num --> |
| Band abstain precision, R1 | <!-- num:c1.band.precision.r1.run -->100.00%<!-- /num --> | <!-- num:c1.band.precision.r1.corr -->100.00%<!-- /num --> |
| Band abstain precision, R2 | <!-- num:c1.band.precision.r2.run -->99.64%<!-- /num --> | <!-- num:c1.band.precision.r2.corr -->99.64%<!-- /num --> |
| Band abstain precision, R3 | <!-- num:c1.band.precision.r3.run -->100.00%<!-- /num --> | <!-- num:c1.band.precision.r3.corr -->100.00%<!-- /num --> |
| Band abstain precision, R4 | <!-- num:c1.band.precision.r4.run -->100.00%<!-- /num --> | <!-- num:c1.band.precision.r4.corr -->90.73%<!-- /num --> |
| Band over-refusal | <!-- num:c1.band.over_refusal.run -->75.50%<!-- /num --> | <!-- num:c1.band.over_refusal.corr -->91.50%<!-- /num --> |
| Band coverage | <!-- num:c1.band.coverage.run -->5.27%<!-- /num --> | <!-- num:c1.band.coverage.corr -->3.83%<!-- /num --> |
| Exploratory precision, R1 | <!-- num:c1.expl.precision.r1.run -->99.75%<!-- /num --> | <!-- num:c1.expl.precision.r1.corr -->99.75%<!-- /num --> |
| Exploratory precision, R2 | <!-- num:c1.expl.precision.r2.run -->91.07%<!-- /num --> | <!-- num:c1.expl.precision.r2.corr -->92.86%<!-- /num --> |
| Exploratory precision, R3 | <!-- num:c1.expl.precision.r3.run -->92.75%<!-- /num --> | <!-- num:c1.expl.precision.r3.corr -->95.50%<!-- /num --> |
| Exploratory precision, R4 | <!-- num:c1.expl.precision.r4.run -->84.71%<!-- /num --> | <!-- num:c1.expl.precision.r4.corr -->12.53%<!-- /num --> |
| Exploratory over-refusal | <!-- num:c1.expl.over_refusal.run -->9.50%<!-- /num --> | <!-- num:c1.expl.over_refusal.corr -->11.00%<!-- /num --> |
| H3 band minus matched single | <!-- num:c1.h3.diff.run -->0.00%<!-- /num --> | <!-- num:c1.h3.diff.corr -->-2.23%<!-- /num --> |
| Dense-cosine (B2) pooled precision | <!-- num:c1.b2.pooled.run -->74.58%<!-- /num --> | <!-- num:c1.b2.pooled.corr -->99.73%<!-- /num --> |
| Dense-cosine (B2) coverage | <!-- num:c1.b2.coverage.run -->27.73%<!-- /num --> | <!-- num:c1.b2.coverage.corr -->0.27%<!-- /num --> |

**Table 6.** Leave-one-group-out ablations on the spec-corrected features, with the same threshold rule refitted for each subset.

| Feature subset | n | Dev AUROC | Held-out AUROC | Band over-refusal | Exploratory R4 |
|---|---:|---:|---:|---:|---:|
| all_12 | <!-- num:c1.abl.all_12.n -->12<!-- /num --> | <!-- num:c1.abl.all_12.dev -->0.887<!-- /num --> | <!-- num:c1.abl.all_12.test -->0.874<!-- /num --> | <!-- num:c1.abl.all_12.over -->91.50%<!-- /num --> | <!-- num:c1.abl.all_12.r4 -->12.53%<!-- /num --> |
| dense_only | <!-- num:c1.abl.dense_only.n -->4<!-- /num --> | <!-- num:c1.abl.dense_only.dev -->0.888<!-- /num --> | <!-- num:c1.abl.dense_only.test -->0.870<!-- /num --> | <!-- num:c1.abl.dense_only.over -->94.75%<!-- /num --> | <!-- num:c1.abl.dense_only.r4 -->23.06%<!-- /num --> |
| lex_overlap_only | <!-- num:c1.abl.lex_overlap_only.n -->1<!-- /num --> | <!-- num:c1.abl.lex_overlap_only.dev -->0.812<!-- /num --> | <!-- num:c1.abl.lex_overlap_only.test -->0.811<!-- /num --> | <!-- num:c1.abl.lex_overlap_only.over -->92.25%<!-- /num --> | <!-- num:c1.abl.lex_overlap_only.r4 -->10.03%<!-- /num --> |
| no_bm25 | <!-- num:c1.abl.no_bm25.n -->7<!-- /num --> | <!-- num:c1.abl.no_bm25.dev -->0.881<!-- /num --> | <!-- num:c1.abl.no_bm25.test -->0.868<!-- /num --> | <!-- num:c1.abl.no_bm25.over -->91.25%<!-- /num --> | <!-- num:c1.abl.no_bm25.r4 -->12.53%<!-- /num --> |
| no_cross_encoder | <!-- num:c1.abl.no_cross_encoder.n -->11<!-- /num --> | <!-- num:c1.abl.no_cross_encoder.dev -->0.886<!-- /num --> | <!-- num:c1.abl.no_cross_encoder.test -->0.872<!-- /num --> | <!-- num:c1.abl.no_cross_encoder.over -->93.75%<!-- /num --> | <!-- num:c1.abl.no_cross_encoder.r4 -->13.78%<!-- /num --> |
| no_dense | <!-- num:c1.abl.no_dense.n -->8<!-- /num --> | <!-- num:c1.abl.no_dense.dev -->0.867<!-- /num --> | <!-- num:c1.abl.no_dense.test -->0.862<!-- /num --> | <!-- num:c1.abl.no_dense.over -->87.75%<!-- /num --> | <!-- num:c1.abl.no_dense.r4 -->9.77%<!-- /num --> |
| no_lex_overlap | <!-- num:c1.abl.no_lex_overlap.n -->11<!-- /num --> | <!-- num:c1.abl.no_lex_overlap.dev -->0.888<!-- /num --> | <!-- num:c1.abl.no_lex_overlap.test -->0.874<!-- /num --> | <!-- num:c1.abl.no_lex_overlap.over -->90.50%<!-- /num --> | <!-- num:c1.abl.no_lex_overlap.r4 -->13.03%<!-- /num --> |
| no_rank | <!-- num:c1.abl.no_rank.n -->10<!-- /num --> | <!-- num:c1.abl.no_rank.dev -->0.884<!-- /num --> | <!-- num:c1.abl.no_rank.test -->0.872<!-- /num --> | <!-- num:c1.abl.no_rank.over -->92.25%<!-- /num --> | <!-- num:c1.abl.no_rank.r4 -->13.28%<!-- /num --> |

Three things change and one does not. Held-out AUROC falls from
<!-- num:c1.auroc.test.run -->0.982<!-- /num --> to <!-- num:c1.auroc.test.corr -->0.874<!-- /num -->: the
frozen figure was flattered by a column that encoded "this passage is a corpus document" rather than "this
passage answers the question". The exploratory ladder changes shape: R1 to R3 stay in the nineties
(<!-- num:c1.expl.precision.r1.corr -->99.75%<!-- /num -->,
<!-- num:c1.expl.precision.r2.corr -->92.86%<!-- /num -->,
<!-- num:c1.expl.precision.r3.corr -->95.50%<!-- /num -->) and R4 collapses to
<!-- num:c1.expl.precision.r4.corr -->12.53%<!-- /num -->. R4 is the rung whose passage is the gold
passage with one span swapped, so a feature set that scores how well a passage matches a question has
nothing to work with: the passage matches perfectly and the answer is wrong. That is the failure mode the
gate should have, and the frozen run hid it because the degenerate dense column was in effect a
"presented-versus-gold" flag. The confirmatory verdicts do not change: H1 remains refuted
(<!-- num:c1.h1.diff.corr -->0.00%<!-- /num -->), H2 remains degenerate, and H3 remains refuted — now in
the stronger form that the band is worse than the recall-matched single by
<!-- num:c1.h3.diff.corr -->-2.23%<!-- /num --> (95% CI
[<!-- num:c1.h3.diff.lo.corr -->-3.11%<!-- /num -->, <!-- num:c1.h3.diff.hi.corr -->-1.35%<!-- /num -->]).
Two caveats on that last number: the matched single threshold is refitted on corrected dev scores, where
its dev precision falls below the 0.80 constraint, so the comparison is descriptive rather than a
re-run of the registered test; and the corrected exploratory band ends at an over-refusal of
<!-- num:c1.expl.over_refusal.corr -->11.00%<!-- /num -->, above the 0.10 cap it was constrained to on dev
— the constraint is on dev, not on the held-out half, and we report the breach rather than hide it.
The corrected dense baseline is a real score at a degenerate operating point:
<!-- num:c1.b2.pooled.corr -->99.73%<!-- /num --> pooled precision at
<!-- num:c1.b2.coverage.corr -->0.27%<!-- /num --> coverage.

Table 6 names the feature group that carries the corrected result: removing the dense group costs
<!-- num:c1.abl.no_dense.test -->0.862<!-- /num --> held-out AUROC against
<!-- num:c1.abl.all_12.test -->0.874<!-- /num --> for the full set, and overlap alone reaches
<!-- num:c1.abl.lex_overlap_only.test -->0.811<!-- /num -->. No single group carries the result; the
separation is distributed across overlap, BM25 and dense scores, which is what one expects when all of
them measure the same thing.

### 4.7 Robustness of the pieces the ladder rests on

Four checks a reviewer asked for, all of them cheap and all of them reported as they came out.

**Is the short rung a biased subsample?** Of the four hundred sampled questions per split,
<!-- num:c1.st.exch.kept.dev -->273<!-- /num --> kept an R2 item and
<!-- num:c1.st.exch.dropped.dev -->127<!-- /num --> did not. Comparing the two groups on question length,
answer surface type, gold paragraph length and article size, no variable differs at the five-percent level in
either split; the smallest p-value is <!-- num:c1.st.exch.p -->0.052<!-- /num -->, on dev question
length. So the R2 figures describe the sampled question set rather than a selected subset, with the caveat
that several p-values sit between five and ten percent.

**Do the intervals survive clustering?** Resampling whole articles instead of items leaves every verdict
unchanged. Of the five comparable cells, four cluster intervals are narrower than the item intervals (width ratios
from 0.45 to 0.85) and one is slightly wider (1.17), because the refusal rate is almost constant across
the held-out articles and there is almost no article-level variance for clustering to add. Two cells are
zero-width at both levels because every item in them is refused.

**Is the matched-recall comparison fair?** The recall-matched single threshold is chosen on dev, never on
test. On the held-out negatives the band and the matched single refuse the same items to within
<!-- num:c1.st.match.maxdiff -->0.00<!-- /num --> points, with zero discordant pairs, so H3's zero is not a
binning artefact.

**Does the reader-confidence baseline work?** No, and for an inspectable reason. On the
<!-- num:c1.reader.n -->553<!-- /num --> dev items where it was run (a small instruction-tuned reader,
mean generated-token log-probability), the signal reaches AUROC
<!-- num:c1.reader.auroc -->0.419<!-- /num --> — worse than chance. When the reader refuses it emits a
fixed refusal string at near-certainty, so a correct refusal scores as high confidence and a confident
wrong answer scores low. Mean log-probability measures the fluency of the string produced, not evidential
support. We report the baseline as exploratory and do not use it to rank gates.

### 4.8 Second corpus: direction only

The lower rows of Table 5 are the second-corpus arm. The pre-declared second corpus (the multi-hop corpus described in §3.1 of the pre-registration;
<!-- num:c1.data.transfer.items -->400<!-- /num --> items built, half answerable and half drawn from the
same question's non-supporting article pool) is evaluated with the frozen operating point. At the
confirmatory point the arm reports <!-- num:c1.tr.precision.conf -->98.50%<!-- /num --> precision at an
over-refusal of <!-- num:c1.tr.over_refusal.conf -->89.50%<!-- /num -->, which is the same degeneracy as the
main corpus and therefore uninformative; at the exploratory point it reports
<!-- num:c1.tr.precision.expl -->85.50%<!-- /num --> (95% CI [<!-- num:c1.tr.ci.lo -->79.50%<!-- /num -->,
<!-- num:c1.tr.ci.hi -->89.50%<!-- /num -->]), a drop of
<!-- num:c1.tr.drop.expl -->7.25<!-- /num --> points against the main corpus's R3. Discrimination, however,
falls from <!-- num:c1.auroc.test.run -->0.982<!-- /num --> on the main corpus to
<!-- num:c1.tr.auroc -->0.640<!-- /num --> on this one. The construct differs — no article grouping,
shorter passages, multi-hop and comparison questions — so we read this as a direction claim only: transfer
of the *operating point* survives, transfer of the *discrimination* does not, and a paper that reported
only the precision number would have said the opposite.

## 5 Discussion

### 5.1 A precision target without a coverage constraint is not a specification

The registered rule — maximise recall subject to precision of
<!-- num:c1.const.target_precision -->0.80<!-- /num --> — is the rule a practitioner writes down, and it
produced a gate that answers about one question in four
(<!-- num:c1.pm.band.answer_rate -->24.50%<!-- /num --> of answerable questions) and whose refusals are
only <!-- num:c1.pm.band.pooled_precision -->83.03%<!-- /num --> true negatives. Any paper reporting
abstention performance without over-refusal and coverage beside it should be read as reporting a choice
about how often to refuse. Our
own <!-- num:c1.band.over_refusal.run -->75.50%<!-- /num --> over-refusal is the number that makes the
precision figure interpretable, and it belongs first, not in a limitations paragraph.

### 5.2 What a retrieval-feature gate measures

The audit, the overlap-matched rung and the top-1 variant agree on one description: these features
measure how well the presented passage matches the question and how likely it is to be the document
retrieval wanted. On negatives constructed by substituting paragraphs, those quantities and answerability
move together, which is why the ladder looks like a hardness ladder. When they come apart — R4, where the
passage matches perfectly and one span is wrong — the gate has nothing to work with, and the corrected run
shows it. The practical implication is not that abstention gates are useless. It is that a ladder of
substituted paragraphs measures overlap, and that the rung which changes what the passage says must be in
the ladder or the ladder is measuring the wrong thing.

### 5.3 Why the corrected run matters more than the frozen one

We report the frozen analysis as the registered result and the corrected analysis as a deviation, but a
reader should treat the corrected numbers as the ones worth carrying forward. The frozen gate's
discrimination was inflated by a column that encoded a construction artefact, and its R4 behaviour was
the opposite of what the construct implies. Reporting both, with the defect in the text, is the only
honest option available after the fact; the alternative — quietly refitting and calling it the result —
would have been exactly the move this paper is about.

### 5.4 What would make the ladder a stronger instrument

Three changes, in order of expected value. Present, for every item, the passage the retriever actually
returns rather than the gold passage for answerables: that is what §4.5 approximates, and it should
replace the current R0 instead of being an add-on. Build R4 by hand rather than by type-matched
substitution: forty inspected rung-4 items included substitutions that preserved the surface type but not
the grammatical role, which weakens the premise-violation reading to answer-absent. And evaluate at a
declared coverage, not a declared precision, so that the operating point cannot be satisfied by refusing
everything.

## 6 Threats to validity

1. One corpus family, one language, passage-level question answering, one feature stack, one gate family.
   Nothing here is evidence about chapter-level or multi-hop retrieval.
2. The item construction presents the gold paragraph for answerable items, so part of the gate's
   discrimination measures whether retrieval found the gold paragraph. §4.5 quantifies that component
   rather than arguing about it.
3. R2 is incomplete (<!-- num:c1.items.rung2.dev -->273<!-- /num --> dev items and
   <!-- num:c1.pm.n.r2 -->280<!-- /num --> held-out items against four hundred sampled questions), which
   weakens any conclusion that depends on R2 specifically; §4.7 reports the exchangeability check.
4. R4 substitutions are automatic and sometimes ungrammatical.
5. The second-corpus arm is a direction test with a different construct, and its confirmatory operating
   point is degenerate by construction.
6. The reader baseline covers <!-- num:c1.reader.n -->553<!-- /num --> dev items only.
7. The gate is fitted on a dev half of <!-- num:c1.items.dev -->1873<!-- /num --> items; intervals reflect
   item-level and article-level resampling, not corpus-level uncertainty.
8. The frozen run's dense block was degenerate and the corrected re-implementation changes two of the
   reported quantities (§4.6). Both runs are reported; neither is a substitute for a fresh pre-registered
   replication with the corrected features.

## 7 Ethics, data and AI disclosure

Public data only: SQuAD v2.0 dev (share-alike licence) and the multi-hop corpus dev split (Apache licence, as declared by
the authors' repository), with every request logged with URL, status, size and checksum in
`04_experiments/data/TRANSFER-DATA.md` and the per-request log files beside it. No private data, no scraped data, no login-walled source. The student is the
responsible author; code, seeds and raw outputs are committed beside the scripts that produced them (for example
`04_experiments/src/gate.py`), and the pre-registration hash is recorded before the first
result-producing run.

AI assistance is disclosed per the target venue's policy. Language-model agents wrote analysis code,
ran the experiments, drafted sections and performed the simulated review; the simulated review is
labelled as a simulation and is not a venue decision. The student directed the work, holds the author
position, and is expected to be able to explain every section — `06_review/STUDENT-DIGEST-S3.md` exists to
make that possible, and `06_review/CLAIMS-AUDIT.md` maps each claim to the file that supports it.

## 8 Reproduction

```
python 04_experiments/src/build_items.py            # items, seeds fixed
python 04_experiments/src/features.py               # as-run features (dense block degenerate)
python 04_experiments/src/run_c1.py                 # the pre-registered analysis
python 04_experiments/src/features_corrected.py     # spec-corrected features (D4)
python 04_experiments/src/eval_corrected.py         # the corrected analysis
python 04_experiments/src/build_items_rung5.py && python 04_experiments/src/features_rung5.py \
  && python 04_experiments/src/eval_rung5.py        # R5 control arm
python 04_experiments/src/features_transfer.py && python 04_experiments/src/eval_transfer.py
python 04_experiments/src/build_items_top1.py && python 04_experiments/src/features_top1.py \
  && python 04_experiments/src/eval_top1.py         # top-1 control arm
python 04_experiments/src/ablation_corrected.py     # Table 6
python 04_experiments/src/stats_addendum.py         # §4.7 numbers
python 04_experiments/src/make_paper_assets.py      # tables + index entries
python 05_paper/build_draft.py                      # this file, from the template
python tools/check_numbers.py --draft 05_paper/draft/paper.md
```

There is no lockfile. The interpreter and library versions used for every number above are recorded in the
session status file beside the results, and the model versions are pinned in the pre-registration; a
requirements file with exact pins is the obvious next step and is not in this draft.

## 9 References

Reference entries are generated from `02_literature/verified_citations.csv` by
`05_paper/template/tools/citations_to_bib.py`; only entries whose verification column records a real API
resolution appear there. Works cited in this draft, with the identifier used for verification:

- Abdumalikov, Minervini, Kementchedjhieva. Answerability in Retrieval-Augmented Open-Domain Question
  Answering. arXiv:2403.01461, 2024.
- Rajpurkar, Jia, Liang. Know What You Don't Know: Unanswerable Questions for SQuAD. arXiv:1806.03822, 2018.
- Ho, Nguyen, Sugawara, Aizawa. Constructing a Multi-hop QA Dataset for Comprehensive Evaluation of
  Reasoning Steps. COLING 2020, DOI 10.18653/v1/2020.coling-main.580; arXiv:2011.01079 resolves to an
  unrelated physics paper and is not this work.
- Survey of abstention in language models. arXiv:2407.18418, 2024.
- DeclineCraft: retrieval and parametric abstention benchmark. arXiv:2610.28340, 2026.
- Xiao et al. C-Pack: Packed Resources for General Chinese Embeddings. arXiv:2309.07597, 2023.
- Nogueira, Cho. Passage Re-ranking with BERT. arXiv:1901.04085, 2019.
- Karpukhin et al. Dense Passage Retrieval for Open-Domain Question Answering. arXiv:2004.04906, 2020.
- Kadavath et al. Language Models (Mostly) Know What They Know. arXiv:2207.05221, 2022.

