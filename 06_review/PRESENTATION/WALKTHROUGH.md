# Presentation walkthrough — how to present the paper section by section

For Shubh. Plain English. Short sentences.
All numbers below are copied from `05_paper/draft/paper.md` (draft as of 2026-11-08; may change in round 3).
Each point is grounded in the paper section shown in brackets, e.g. [paper §4.2].

How to use this file: read the title and abstract first. Then go section by section. For every section you get: what it says in 3-5 lines, the one thing a reviewer will attack, and how you answer. The glossary at the end explains every technical term with a daily-life analogy.

---

## Title and front matter

**What it says.** The title is "How Hard Are Your Negatives? A Pre-Registered Audit of Negative Ladders for Retrieval-Feature Abstention Gates, with a Negative Result." You are the author. Analysis and code were agent-assisted, human-directed [paper front matter, §7]. The paper was generated from a template, and every table and number comes from a results file [paper front matter].

**The one thing a reviewer will attack.** "Is this just a failed method that you dressed up as a result?"

**How to answer.** "No. The result *is* that the gate fails in a specific way. We pre-registered the test. The gate refuses 75.50% of answerable questions. Precision without coverage is not a result. The audit that shows this is the contribution." [paper §1, §5.1]

---

## Abstract

**What it says.** The paper audits an abstention gate on SQuAD, not a new gate. The pre-registered rule is: maximise abstain recall subject to dev abstain precision 0.80 [paper Abstract]. That rule makes the gate refuse 75.50% of answerable questions, so it answers only 24.50% of questions. The ladder stops moving: refusal rate R1 100.00%, R2 99.64%, R3 100.00%, R4 100.00% [paper Abstract].

**The one thing a reviewer will attack.** "Why lead with a negative result? Where is the working gate?"

**How to answer.** "The negative result is specific. H1 is refuted: R1 minus R3 is 0.00% with 95% CI [0.00%, 0.00%]. H3 is refuted: difference 0.00%. H2 is degenerate: loss 0.07% [paper Abstract]. What works is the audit: surface features give AUROC 0.506, 0.539, 0.488, 0.415 for R1-R4. Add overlap and R1 jumps to 0.977 [paper Abstract]. A precision number means nothing without its coverage. That is the point." [paper Abstract, §5.1]

---

## 1 Introduction

**What it says.** A system that always answers will answer from passages that do not support the question. An abstention gate decides whether to answer. Gates are built from retrieval signals. Abdumalikov et al. (arXiv:2403.01461) show accuracy falling from 98% to 1% when negatives change [paper §1]. So the paper designs a measurement, not a method.

**The one thing a reviewer will attack.** "Your H1, H2, H3 are straw men. Of course refusing everything gives 100% refusal."

**How to answer.** "That is exactly the finding. The registered rule has no coverage constraint, so the gate satisfies the target by refusing almost everything. At that point the ladder quantity stops existing [paper §1]. The contribution is a reproducible four-rung ladder, a separability audit as a hard gate, and two control arms. We claim neither priority nor generality beyond one corpus family, one feature stack, one gate family, and English passage-level QA." [paper §1]

---

## 2 Related work

**What it says.** The paper covers abstention surveys, negative choice in answerability, and benchmarks that join retrieval and generation. It also lists retrieval parts: BM25, dense retrieval, and reranking. The reader-confidence baseline is the cheap reader signal from arXiv:2207.05221. Table 7 compares the closest work.

**The one thing a reviewer will attack.** "This is just Abdumalikov plus DeclineCraft. What is new?"

**How to answer.** "The 98% to 1% collapse is known. Our ladder is a systematic version of its two conditions [paper §2]. DeclineCraft varies retrieval and parametric abstention jointly. Our ladder varies only the presented passage. The two designs are complementary, not nested. What we report is abstain precision with over-refusal and coverage beside it, which Table 7 shows the closer work does not." [paper §2]

---

## 3 Method

### 3.1 Items (§3.1)

**What it says.** SQuAD v2.0 dev has 35 articles, 1204 paragraphs, 11873 questions, of which 5928 are answerable. Only answerable rows are used. Articles are split whole into dev and held-out halves. Each half gives 400 questions, each with 5 passages, one per rung. Total is 3752 items, 1879 held out, R2 short at 273 dev items [paper §3.1].

**The one thing a reviewer will attack.** "R2 has only 273 items. The ladder is broken."

**How to answer.** "R2 is short because most questions have no content word in another paragraph. The pre-registration says report the rung at its true size, do not top it up. §4.7 checks that questions which kept an R2 item are not different from those which did not. No variable differs at 5%, smallest p is 0.052 [paper §3.1, §4.7]."

### 3.2 Features (§3.2)

**What it says.** The gate uses 12 retrieval-side features per item. They are BM25 scores, dense cosine scores, agreement, cross-encoder score, and overlap. A rung-4 passage is a rewrite, not a corpus document. It inherits its source rank and is flagged [paper §3.2].

**The one thing a reviewer will attack.** "Twelve features is arbitrary. Why not a real reader?"

**How to answer.** "The claim is about the gate family, not one set of features. If all of them measure overlap, the separation is distributed. Table 6 shows removing any one group costs less than a third of the AUROC margin [paper §4.6]. The dense block defect is disclosed separately. A reader baseline is in §4.7 and fails for an inspectable reason."

### 3.3 Gate and operating point (§3.3)

**What it says.** A logistic regression on dev gives a score that reads as the probability the passage answers the question. Two operating points are fitted on dev: a band with two thresholds, and a single threshold. Both maximise dev abstain recall subject to precision 0.80. The band is [0.9072, 0.9478], width 0.0406. The single threshold is 0.9394 [paper §3.3].

**The one thing a reviewer will attack.** "Your thresholds are outside the data or hand-tuned."

**How to answer.** "All three sit inside the observed dev score range. The failure is not outside-data placement. Dev admit mass is 6.03%, and 92.95% of dev items are refused by the lower threshold alone [paper §3.3]. The admit region is degenerate."

### 3.4 Separability audit (§3.4)

**What it says.** Before any result, a logistic regression on 6 surface features must not separate a rung's negatives from answerable items. Gate is AUROC 0.750. Any rung above is rebuilt by length matching, at most twice. If two or more rungs still fail, the run stops. The overlap variant is a sensitivity check, not a surface check [paper §3.4].

**The one thing a reviewer will attack.** "Your audit passes, so the rungs are clean. The overlap result does not matter."

**How to answer.** "The audit is one-sided by design. It flags formatting leakage, not real signal [paper §3.4]. The overlap variant is what turns the audit into a measurement of what the rungs vary. R4 is 0.415, separation with the sign flipped. We report it as that, not as a clean pass."

### 3.5 What the reported numbers are (§3.5)

**What it says.** The pre-registration names "abstain precision" but defines it as P(refused | negative), which is a recall. Round-2 review caught the contradiction. The paper now reports both: refusal rate for P(refused | negative), and precision for P(negative | refused). Tests stay as frozen. Precision is descriptive only [paper §3.5].

**The one thing a reviewer will attack.** "You changed the metric after seeing results."

**How to answer.** "No hypothesis is restated over precision [paper §3.5]. The registered tests stay exactly as frozen. We report both, always labelled. At the registered point refusal saturates at 100.00% while precision is 48.02% to 56.98%. That gap is the over-refusal."

### 3.6 Statistics (§3.6)

**What it says.** Item-level BCa bootstrap, 10000 resamples, seed 12345. Paired comparisons resample jointly. Exact sign tests for paired binary indicators. Holm correction over two tests carrying p-values, H1 and H3. Two intervals are zero-width because every item is refused [paper §3.6].

**The one thing a reviewer will attack.** "Zero-width intervals are impossible. You made an error."

**How to answer.** "A zero-width interval at a boundary is reported as a boundary, not as certainty [paper §3.6]. If every item in the comparison is refused, every paired difference is zero. AUROC carries no interval because the bootstrap here intervals rates, not ranking statistics."

---

## 4 Results

### 4.1 The audit passes (§4.1)

**What it says.** On 6 surface features no rung is separable, so the run proceeds. Add overlap and R1 becomes 0.977, R2 0.889, R3 0.923. R4 stays at 0.408 because its passage is the gold passage. Table 3 shows all five rungs including R5 at 0.721 [paper §4.1].

**The one thing a reviewer will attack.** "0.977 means your ladder is just overlap position. The experiment is circular."

**How to answer.** "That is the paper's most transferable measurement [paper §4.1]. It says the rungs differ mainly in question-word coverage. That predicts the main result before the gate is fitted. The gate scores overlap. So the circularity is the finding, and §4.4, §4.5, §4.6 test it."

### 4.2 The ladder disappears at the registered point (§4.2)

**What it says.** Table 1: band refusal is 100.00%, 99.64%, 100.00%, 100.00% for R1-R4. Precision of those refusals is 56.98%, 48.02%, 56.98%, 56.92%. H1, H2, H3 are refuted or degenerate. The band refuses 75.50% of answerable questions and answers only 24.50% [paper §4.2].

**The one thing a reviewer will attack.** "You report 100% refusal and 56% precision as if both are true. Which is the real number?"

**How to answer.** "Both are true. They measure opposite directions [paper §3.5, §4.2]. Refusal rate is P(refused | negative). Precision is P(negative | refused). With 75.50% over-refusal, most of what the gate refuses is answerable. Dev precision at the fitted band is 83.69%, so the rule did what it was asked. What it was asked was not enough."

### 4.3 Exploratory: constrain coverage (§4.3)

**What it says.** Practitioners would cap over-refusal at 0.10. That keeps over-refusal at 9.50% with coverage 25.44%. Refusal now falls: 99.75%, 91.07%, 92.75%, 84.71%. R1 minus R3 is 7.00%, CI [4.50%, 9.75%], half the 15-point criterion. Not monotone [paper §4.3].

**The one thing a reviewer will attack.** "You found the effect once you moved the operating point. The refutation is an artefact."

**How to answer.** "We do not read the refutation as evidence that hardness does not matter [paper §4.2]. §4.3 finds the effect at about half the predicted size. This is exploratory, it rescues no hypothesis, and the confirmatory verdict stands [paper §4.3]."

### 4.4 Control arm: overlap-matched negatives (§4.4)

**What it says.** R5 is the paragraph whose overlap is closest to the gold paragraph. Mean absolute difference is 10.29%, against 42.08% for a random negative. R5 still refused at 89.25% at the exploratory point. It sits between R2 and R4. Overlap is not the whole story [paper §4.4].

**The one thing a reviewer will attack.** "R5 still differing in length means the control is mismatched."

**How to answer.** "R5 items are the longest negatives, and surface audit is closest to its gate at 0.721 without crossing it [paper §4.4]. The honest reading is that a paragraph from elsewhere can be caught by several correlated signals. Matching one signal is not enough to hide it."

### 4.5 Top-1 presented variant (§4.5)

**What it says.** Every item shows the BM25 rank-1 paragraph. The retriever's first choice is correct for 78.25% of held-out questions. The gate detects misses at AUROC 0.945, refuses 63.22% of misses and 2.56% of hits. P(miss | refused) is 87.30% [paper §4.5].

**The one thing a reviewer will attack.** "You are just measuring retrieval correctness, not answerability."

**How to answer.** "In this variant the label *is* retrieval correctness, so 'detects misses' and 'detects unanswerable passages' coincide [paper §4.5]. It confirms the mechanism the audit implies and it does not exculpate the gate. That limit is in the threat list."

### 4.6 Dense block was degenerate (§4.6)

**What it says.** The frozen code used the presented passage as its own dense query. Dense cosine was exactly 1 on 78.70% of rows. The gate had ten informative columns, not twelve. Re-implementing as specified drops held-out AUROC from 0.982 to 0.874. R4 collapses to 12.53% at the EXPLORATORY (coverage-capped) operating point (Table 4, deviation D4). H1 and H3 stay refuted; H3 is now -2.23% [paper §4.6]. This is a declared sensitivity analysis, not a fresh pre-registered replication.

**The one thing a reviewer will attack.** "You used buggy code. The whole paper is invalid."

**How to answer.** "We did not refit the registered analysis [paper §4.6]. The frozen run is reported exactly as produced. The corrected run is D4, a declared sensitivity analysis. Both runs are in Table 4. Reporting both is the only honest option. The corrected numbers are the ones to carry forward [paper §5.3]. No fresh pre-registered replication is claimed."

### 4.7 Robustness checks (§4.7)

**What it says.** Four cheap checks. R2 subsample is not biased: smallest p is 0.052. Cluster resampling leaves every verdict unchanged. Band vs matched single has zero discordant pairs. Reader log-probability reaches AUROC 0.419 on 553 dev items, worse than chance [paper §4.7].

**The one thing a reviewer will attack.** "The reader baseline is weak, so you are hiding a better baseline."

**How to answer.** "When the reader refuses it emits a fixed string at near-certainty, so a correct refusal scores as high confidence [paper §4.7]. Mean log-probability measures fluency, not evidential support. We report it as exploratory and do not use it to rank gates."

### 4.8 Second corpus (§4.8)

**What it says.** The second corpus is direction only: no article grouping, shorter passages, multi-hop questions. Operating point transfers but discrimination does not: AUROC falls from 0.982 to 0.640. H2's second arm is inconclusive by the registered rule. Confirmatory over-refusal is 89.50% [paper §4.8].

**The one thing a reviewer will attack.** "Transfer fails. The paper is SQuAD-only."

**How to answer.** "We claim generality only for the direction. A paper reporting only precision would have said the opposite [paper §4.8]. The paper already says: one corpus family, one language, passage-level QA, one feature stack, one gate family. Nothing here is evidence about chapter-level or multi-hop retrieval [paper §6]."

---

## 5 Discussion

### 5.1 Precision without coverage is not a specification (§5.1)

**What it says.** The registered rule produced a gate answering about one question in four, 24.50% of answerable questions, with refusals only 83.03% true negatives. Over-refusal 75.50% makes precision interpretable. It belongs first, not in limitations [paper §5.1].

**The one thing a reviewer will attack.** "Every paper reports precision. Why single out this one?"

**How to answer.** "Any paper reporting abstention without over-refusal and coverage beside it should be read as reporting a choice about how often to refuse [paper §5.1]. Our gate's 75.50% is the number that makes the precision figure interpretable."

### 5.2 What a retrieval-feature gate measures (§5.2)

**What it says.** The features measure how well the passage matches the question and how likely it is to be the retrieved document. On substituted-paragraph negatives, those move with answerability. When they come apart in R4, the gate has nothing to work with [paper §5.2].

**The one thing a reviewer will attack.** "So gates are useless."

**How to answer.** "Not useless. A ladder of substituted paragraphs measures overlap. The rung that changes what the passage says must be in the ladder, or the ladder measures the wrong thing [paper §5.2]."

### 5.3 Why the corrected run matters more (§5.3)

**What it says.** The frozen run is the registered result. The corrected run is the deviation. Readers should carry the corrected numbers forward. Its R4 behaviour was the opposite of the construct. Quietly refitting would have been the move this paper is about [paper §5.3].

**The one thing a reviewer will attack.** "You are asking us to trust the unregistered numbers."

**How to answer.** "Trust them less as confirmatory, more as construct-true. The frozen discrimination was inflated by a construction artefact [paper §5.3]. Both are reported with the defect in the text. The corrected run is still not a substitute for a fresh pre-registered replication with corrected features [paper §6]."

### 5.4 What would make the ladder stronger (§5.4)

**What it says.** Three changes: present the retriever's actual passage for every item, build R4 by hand, evaluate at declared coverage. Hand inspection found 40 items where substitution kept surface type but not grammatical role [paper §5.4].

**The one thing a reviewer will attack.** "Why did you not do these in the first place?"

**How to answer.** "R0 with the gold paragraph was the pre-registered design. §4.5 approximates the retriever-returned version. Hand-built R4 and declared coverage are future work. The paper says so in order of expected value."

---

## 6 Threats to validity

**What it says.** Eight threats: one corpus family, gold-paragraph presentation, incomplete R2 (280 held-out items), automatic R4 substitutions, second-corpus direction test, reader baseline on 553 items only, gate fitted on 1873 dev items, and the degenerate dense block [paper §6].

**The one thing a reviewer will attack.** "With eight threats, nothing is left standing."

**How to answer.** "Each threat is bounded, not fatal. R2 has an exchangeability check. Gold-paragraph bias is quantified in §4.5. Intervals now cover item and article resampling, not corpus-level uncertainty. That list is in §6 and §7 of the paper, not hidden."

---

## 7 Ethics, data and AI disclosure

**What it says.** Public data only: SQuAD v2.0 dev and a multi-hop corpus dev split. Every request logged with URL, status, size, checksum. No private, scraped, or login-walled source. AI agents wrote code, ran experiments, drafted sections, and performed simulated review. The student directed the work and holds the author position [paper §7].

**The one thing a reviewer will attack.** "So an AI wrote the paper. Who is responsible?"

**How to answer.** "The student is the responsible author [paper §7]. Code, seeds and raw outputs are committed beside the scripts. The pre-registration hash is recorded before the first result-producing run. The simulated review is labelled a simulation, not a venue decision. Disclosure follows the target venue's policy."

---

## 8 Reproduction

**What it says.** Section 8 lists exact commands: `build_items.py`, `features.py`, `run_c1.py`, `features_corrected.py`, `eval_corrected.py`, plus R5, transfer, top-1, ablation, stats, reader, precision and asset scripts. One known defect: the frozen run records its hash as `#` because the reporting line splits on whitespace. The four real hashes are in `PREREGISTRATION.sha256` [paper §8].

**The one thing a reviewer will attack.** "No lockfile. Nobody can reproduce this."

**How to answer.** "Versions are in the session status file and the pre-registration pins model versions. A requirements file with exact pins is the obvious next step and is not in this draft [paper §8]. The hash defect is a reporting-line defect, not a freeze defect."

---

## 9 References

**What it says.** References are generated from `02_literature/verified_citations.csv`, keeping only entries with a real API resolution. The Ho et al. multi-hop reference notes arXiv:2011.01079 resolves to an unrelated physics paper and is not that work [paper §9].

**The one thing a reviewer will attack.** "Some of these venues or years look odd."

**How to answer.** "Entries are from verified resolution only, and identifiers are shown so each can be checked. The unrelated arXiv resolution is called out in the draft itself."

---

## Glossary — every term with a daily-life analogy

- **Abstention gate.** The doorman who decides whether to let the question through to the answerer. Analogy: a shop guard who checks if you have a ticket before you enter.
- **Answerable.** The passage actually contains the answer. Analogy: the book on the table has the page you need.
- **AUROC.** A score for how well the model sorts yes from no, 0.5 is random, 1.0 is perfect. Analogy: how well a chess coach ranks strong vs weak players without seeing the games.
- **Band / two-sided threshold.** Two cut points; only scores in the middle are admitted. Analogy: a toll road open only to cars between length A and length B.
- **BCa bootstrap interval.** A confidence interval built by resampling many times and correcting for skew. Seed 12345, 10000 tries here. Analogy: ask 10,000 similar classes and see where the middle falls.
- **BM25.** Lexical word-counting retriever that ranks by rare-word matches. Analogy: an old library index that finds books by unusual words on the cover.
- **Bootstrap interval.** Same idea as BCa: resample items and watch the number wiggle. Analogy: re-ask a straw poll many times with slightly different people.
- **Coverage.** What fraction the gate still answers. Analogy: how many customers the shop still lets in after adding the guard.
- **Cross-validation / 5-fold.** Split data into 5 parts, test on each part in turn. Analogy: practise on 4 exam papers, mark the 5th.
- **Cross-encoder / reranker.** A model that scores one question-passage pair at a time. Analogy: a judge who reads the question and the passage together, not separately.
- **Dense retrieval / cosine.** Word meaning vectors; cosine is the angle between question vector and passage vector. Analogy: find stories that *mean* the same, even with different words.
- **Dev half / held-out half.** The practice set (fit thresholds here) vs the final exam set (never seen during fitting). Analogy: nets in practice vs the real match.
- **Deviation D1-D4.** A declared change after pre-registration. D1 exploratory point, D2 R5 arm, D3 top-1 arm, D4 corrected features. Analogy: a match rule change announced in writing before it affects scoring.
- **Exploratory vs confirmatory.** Confirmatory = the frozen test. Exploratory = look around after, labelled as such. Analogy: the official exam vs the practice round.
- **Gate AUROC.** The ranking quality of the whole gate before thresholds. Analogy: the player's skill rating before the pass/fail line is drawn.
- **Gold paragraph.** The true paragraph containing the answer span. Analogy: the correct answer key page.
- **Holm correction.** A method to adjust p-values when you run several tests at once. Analogy: sharing your cheating suspicion across several suspects so one shout does not convict.
- **Hypothesis H1 / H2 / H3.** H1: precision falls 15 points R1 to R3. H2: transfer loses 10 points. H3: band beats single by 5 points. Analogy: three bets written before the race.
- **IDF / content token.** Inverse document frequency: rare words count more. Highest-IDF content token is the most distinctive word. Analogy: a rare surname matters more than "first" when searching the class list.
- **Item.** One question + one presented passage + one label. Total 3752. Analogy: one exam card.
- **Logistic regression.** A simple model that turns features into a 0-1 probability-like score. Analogy: a marks calculator that weighs several test scores.
- **Negative.** The presented passage does NOT support the question. The abstention gate should refuse these. Analogy: a fake ticket, the guard should stop it.
- **Operating point.** The exact thresholds you actually use in deployment. Analogy: the exact height bar on the ride.
- **Overlap / lexical overlap.** How many question words appear in the passage. Analogy: how many words you and the shop sign share.
- **Over-refusal.** Refusing things you should have answered (refusing answerable questions). 75.50% here. Analogy: the guard stops 3 out of 4 real customers.
- **Pooled precision.** Precision over all rungs together, 83.03% here. Analogy: one overall hit rate across all fake-ticket types.
- **Precision P(negative | refused).** Of all refusals, what fraction were truly negative. Here 56.98% on R1. Analogy: of everyone the guard stopped, how many really had fake tickets.
- **Pre-registration.** Rules and hashes written and frozen before results exist. Analogy: locking the exam rules in a sealed envelope before the class sits it.
- **Recall / refusal rate P(refused | negative).** Of all negatives, what fraction you refuse. Here 100.00% on R1. Analogy: of all fake tickets, how many the guard catches.
- **Rung / negative ladder.** Levels of negatives from easy to hard: R1 random, R2 topical, R3 neighbour, R4 one span swapped, plus R0 answerable and R5 overlap-matched. Analogy: steps of a ladder getting harder to climb.
- **Separability audit / surface features.** Test whether formatting alone (length, digits, punctuation) can tell negatives apart. 6 features here. Gate AUROC 0.750. Analogy: can you spot the fake ticket just by its paper colour?
- **Single threshold / one-sided.** Only one cut point; admit above it. Analogy: only a minimum height, no maximum.
- **Top-1 presented.** Showing the retriever's first choice for every item. Analogy: always judge the shop by the first shelf the assistant picks.

---

## One-minute summary to say aloud

"We built a four-rung ladder of negative passages over SQuAD. We froze the test before running it. The gate that maximises recall at precision 0.80 refuses 75.50% of good questions. The ladder disappears at that point. The audit shows the rungs differ in word overlap, AUROC 0.977. The honest numbers are the corrected ones: AUROC 0.874, R4 at 12.53%. Precision means nothing without coverage."
