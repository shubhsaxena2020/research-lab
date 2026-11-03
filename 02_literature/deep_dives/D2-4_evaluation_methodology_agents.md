# Evaluation methodology and benchmarks for agents and LLM systems — deep dive (S2-5)

## 0. Scope and method

This deep dive treats measurement as the object of study rather than as plumbing. The question
driving it is not "which agent is best" but "what would have to be true for a published agent number
to mean anything, and how much of that is checkable on one laptop".

I searched the citation tool (`verify_citations.py search`) against arXiv and OpenAlex with queries
covering the named benchmark families (AgentBench, WebArena, SWE-bench, τ-bench, GAIA, OSWorld,
MLE-bench), the judge literature ("LLM-as-a-judge", "position bias", "verbosity bias",
"self-preference", "judge reliability"), statistical practice ("error bars evals", "variance in
evaluation benchmarks", "reproducibility machine learning", "statistical significance"), and
contamination ("data contamination benchmarks", "benchmark leakage", "memorization"). Forty-six
records were resolved by identifier and their abstracts read in bulk; seven were read at HTML
full-text level (AI Agents That Matter, the ABC checklist paper, the HAL harness paper, JudgeBench, the
position-bias study, Quantifying Variance, Adding Error Bars), plus the results sections of three
benchmarks to extract human-versus-agent gaps. Thirty-two papers were resolved into
`02_literature/staging/S2-5-verified.csv` and are the only works cited here.

Two exclusions matter. "SWE-bench Verified" and the Chatbot Arena leaderboard are products with
announcements rather than papers, so I cite the peer-reviewed criticisms of them instead of the
artifacts themselves. And I cite nothing whose abstract I had not read, which is why the bibliography
is narrower than the reading list in this area usually is.

## 1. Taxonomy

### 1.1 Executable-environment benchmarks: the object of measurement moved from answers to end states

The first cluster replaces "produce a string" with "leave the world in a specified state". AgentBench
[1] assembled eight interactive environments (operating system, database, knowledge graph, card game,
lateral-thinking puzzles, household simulation, web shopping, web browsing) and ran 25 models through
them, finding a large gap between top commercial models and open models at or below 70B and
attributing failures to long-horizon reasoning, decision-making and instruction following rather than
to knowledge. WebArena [2] built self-hosted clones of four real website categories plus tools and
manuals, released 812 long-horizon tasks with programmatic success checks, and reported that the best
GPT-4-based agent at release completed 10.59% of them. SWE-bench [3] took 2,294 GitHub issues from 12
Python repositories with their merged pull requests as ground truth, and found that contemporary
models resolved only the simplest. OSWorld [4] made the environment a real desktop: 369 tasks across
Ubuntu, Windows and macOS, humans at 72.36% and the best model at 12.24%, with multi-application
workflows at 6.57%. GAIA [5] went the other way and made the tasks easy for people: 466 questions
whose answers require browsing, tool use and multi-modality, humans at 92% and GPT-4 with plugins at
15%, with answers to 300 questions withheld for a leaderboard. τ-bench [6] added a simulated user and
a domain policy, scored by comparing final database state to an annotated goal state, and introduced
pass^k to measure whether an agent succeeds repeatedly rather than once: GPT-4o stayed below 50% and
its pass^8 in the retail domain fell below 25%. MLE-bench [7] turned 75 Kaggle competitions into
tasks and found the strongest scaffold reaching at least bronze-medal level in 16.9% of them.

The common move is real progress: these benchmarks cannot be passed by a lookup table of strings,
and the human-agent gaps they report (60 points on OSWorld, 77 on GAIA) are too large to be artifacts
of scoring. That is precisely why they are poor targets for a small lab — the gap is so large that
any interesting question lives inside a narrow band that these benchmarks were not designed to
resolve.

### 1.2 Reward design and validity as a research object

The second cluster audits the benchmarks rather than the agents, and it produces the most useful
numbers in this whole area. ABC [9] surveyed 17 agentic benchmarks and assessed ten in depth against
two validity conditions: *task validity* (a task is solvable if and only if the agent has the target
capability) and *outcome validity* (a positive check really implies task success). Seven of the ten
had outcome-validity flaws, seven had task-validity flaws, and all ten had reporting limitations.
Their examples are concrete: an agent that returns empty responses is scored successful on 38% of
τ-bench airline tasks and beats a GPT-4o-based agent there; an agent can reach 100% on SWE-Lancer
without resolving any task; KernelBench overestimates by 31 points because fuzzing is incomplete;
WebArena's string matching overestimates by 5.2 points. They also cite that 24% of the top-50
positions on one SWE-bench leaderboard are incorrect, and that applying their checklist to CVE-Bench
cut measured overestimation by 33 points.

AI Agents That Matter [8] makes the complementary argument from the evaluation-practice side. Of 17
agent benchmarks they classify by intended generality, only five had a holdout set at the appropriate
level, and seven had no holdout and no stated plan for one. They then reproduced three published
agents on HumanEval and found that a trivially cheap "warming" baseline (retry with rising
temperature) was not significantly different in accuracy from the best agent architecture, while
costs differed by nearly two orders of magnitude — LATS cost more than fifty times the warming
baseline, Reflexion and LDB more than 50% more. In a separate case study they found retrieval and
long-context answering roughly equal in accuracy on NovelQA with retrieval more than twenty times
cheaper, a reversal that the benchmark's own leaderboard hides because it never reports cost.

### 1.3 The judge literature: a measurement instrument with a known error model

MT-Bench [15] established the practice and its limits in the same paper: GPT-4 as judge agreed with
human preferences above 80%, comparable to agreement between humans, while the paper itself
documented position, verbosity and self-enhancement biases. "Large Language Models are not Fair
Evaluators" [16] showed how far the position effect reaches: by swapping the order of two answers,
Vicuna-13B could be made to beat ChatGPT on 66 of 80 queries with ChatGPT judging, and their
calibration recipe (multiple evidence, balanced positions, human fallback) recovered most of the
loss. Self-preference has a mechanism, not just a correlation: evaluators recognise their own
generations at above-chance rates, and fine-tuning experiments show self-recognition and
self-preference rise together [17]. Length bias is separable and correctable: fitting a regression
that predicts the judge's preference from length difference and then predicting at zero length
difference produced a length-controlled variant of a popular pairwise benchmark [18].

The systematic study of position bias [19] is the best single source on the size of the problem: 15
judges, 22 tasks, roughly 40 answer-generating models, over 150,000 judgement instances, with three
metrics (repetition stability, position consistency, preference fairness). The most positionally
consistent judge reached 0.828 consistency on their second suite; nine judges agreed in more than 80%
of instances about two-thirds of the time, and disagreed on about a quarter — concentrated on pairs
whose quality difference was small. That last finding is the important one for anyone claiming a
small improvement: judge noise is not spread evenly, it pools exactly where the effect being claimed
is small.

JudgeBench [20] attacks the other axis, correctness rather than preference, by converting hard
knowledge, reasoning, math and coding items into response pairs with objectively correct labels. On
it, a vanilla GPT-4o judge scores 50.86% overall, a stronger Arena-Hard-style prompt 56.57%, the best
fine-tuned judge 57.43%, and the open 7B evaluator 34.86% — below chance. Prometheus 2 [21] is the
serious attempt to make an open evaluator usable: 7B and 8x7B models that handle both direct
assessment and pairwise ranking under user-supplied rubrics, trained to mirror human and GPT-4
judgements. Trust or Escalate [22] is the most useful idea in this cluster for a small lab: treat the
judge as a classifier with an abstention option, calibrate its confidence on a small human-labelled
set, and only accept its verdicts when a conformal-style guarantee holds, escalating the rest to a
stronger (or human) judge. The guarantee is the product; the judge is a component.

### 1.4 Statistical practice: the part the field knows and does not do

The oldest paper in this set is still the sharpest warning. Deep RL that Matters [11] showed that
seed variance, environment nondeterminism and hyperparameter sensitivity were large enough that
reported improvements over baselines were frequently not identifiable, and that reporting conventions
made this invisible. Dacrema et al. [12] turned the same suspicion on recommender systems: of 18
recent neural methods, only 7 could be reproduced with reasonable effort, and 6 of those 7 were
outperformed by simple nearest-neighbour or graph heuristics, with the seventh not consistently
beating a well-tuned linear ranker. Their follow-on lesson is the one that transfers to agents: a
comparison against a weakly tuned baseline is not a comparison, because the amount of search a method
received can decide the ranking on its own.

The two modern papers translate this into eval practice. Adding Error Bars to Evals [13] treats
evaluation questions as draws from a super-population and gives the whole apparatus: standard errors
for independent items, clustered standard errors when questions come in groups, resampling and
next-token-probability variance reduction, paired analysis on question-level differences, and a
sample-size formula. Their worked example is the number to memorise: to detect a 3-point absolute
difference at 80% power with a paired design and a plausible per-question variance, an eval needs
about 969 independent questions, and they recommend new evals contain at least 1,000. Quantifying
Variance in Evaluation Benchmarks [14] measures what happens when nobody does this: across 13
benchmarks and 280 models, they note that papers "rarely report more than a single number per
benchmark" and that significance values are "scarcely reported" on release papers and leaderboards.
Their measured variance is largest exactly where test sets are small (COPA, HumanEval), and their
negative result is worth as much as the positive one: item-response-theory style reweighting did not
meaningfully reduce variance, while simply reframing multiple-choice items as completion items did
for 7B-scale models.

### 1.5 Contamination: the failure mode that looks like capability

Min-K% Prob [24] detects pretraining membership from black-box token probabilities, on the hypothesis
that unseen text contains a few unusually low-probability tokens, and validates the detector on a
benchmark built from pre- and post-cutoff data. The rephrasing paper [25] demonstrates why string
matching is not enough: paraphrase and translation bypass n-gram decontamination, a 13B model can
then be overfit to a benchmark until it rivals GPT-4, and their LLM-based decontamination still finds
8–18% HumanEval overlap inside large pretraining corpora. GSM1k [26] is the cleanest natural
experiment: 1,205 new grade-school math items built to match GSM8k on human solve rate, step count and
answer magnitude, on which leading models drop by up to 8 points with systematic overfitting across
model sizes. At the agent end, SWE-bench+ [27] hand-screened successful patches and found 32.67%
relied on solutions leaked into the issue text and 31.08% passed only because tests were weak; after
removing those instances the headline agent's resolution rate fell from 12.47% to 3.97%, and over 94%
of issues predate model knowledge cutoffs.

### 1.6 Claims that evaporate when the baseline is fair

Agentless [29] is the cleanest documented case in agents: a fixed three-phase pipeline (localise,
repair, validate) with no autonomous control flow reached 32.00% on SWE-bench Lite at $0.70 per
issue, above every open-source agent at the time, and manual inspection found items whose ground-truth
patches were wrong or whose issue text was misleading. MAST [30] annotated more than 1,600 traces
across seven multi-agent frameworks, built a 14-mode failure taxonomy from 150 traces at κ = 0.88, and
opens with the observation that multi-agent gains on popular benchmarks are often minimal; one of
their three failure categories is task verification. The self-correction survey [31] closes the loop:
no prior work demonstrates successful self-correction from prompted-LLM feedback except in tasks
unusually suited to it, self-correction works when reliable external feedback exists, and large-scale
fine-tuning enables it. In other words, the parts of "reviewer gates" that work are the parts that
add information the generator did not have.

### 1.7 Metrics as a design choice: pass@k and its siblings

The last cluster is small and consequential: the metric itself can manufacture a result. Codex [28]
introduced pass@k with an unbiased estimator from n samples per problem and reported 28.8% pass@1
against 70.2% when allowed 100 samples — a 41-point improvement from one model, obtained purely by
changing k. That number is not a scandal; it is the correct measurement of a different question
("can the model ever produce a solution"), and it becomes a scandal when a paper reports "pass@k" for
some k, does not say which, and is compared against a system measured at k = 1. τ-bench [6] supplies
the mirror image for deployed agents, pass^k, the probability that an agent succeeds on the same task
k times in a row. The two metrics diverge violently: at a per-attempt success rate of 0.3, pass@8 is
94% while pass^8 is 0.01%. A leaderboard that mixes the two is measuring nothing but its own
convention.

## 2. What is saturated

Adding another agent benchmark is saturated. The pattern — pick a domain, wrap it in Docker, report
that GPT-class agents score 10–20% and humans 70–90% — has been executed dozens of times, and the
marginal benchmark now contributes a leaderboard entry rather than knowledge, because the interesting
variance is inside the scoring code, not in the domain.

Also saturated: another debiasing trick for judges evaluated on the authors' own agreement set; another
"our multi-agent framework beats a single agent on reasoning benchmarks" claim without a cost column;
another SOTA-on-SWE-bench claim; and another survey of LLM-as-a-judge that lists the same five biases.
The evidence that these are saturated is partly the critique literature above and partly the shape of
the results: when independent groups re-measure, the effect sizes shrink toward the noise floor
[8, 27, 29].

What is *not* saturated is the audit layer. Ten benchmarks were assessed by ABC [9], 17 were
classified for holdout adequacy by AI Agents That Matter [8], and 13 were measured for seed and
checkpoint variance by [14]. Nobody has done the equivalent for the 2025–2026 generation, and nobody
has counted how many of those papers report a seed variance at all.

## 3. What is genuinely open

The open problems here are measurement problems, and they are open because the field's incentives
point away from solving them.

**Reporting.** Almost no agent result carries an interval. HAL [10], a standardised harness run at
scale — 21,730 rollouts, 9 models, 9 benchmarks, about $40,000 and 2.5 billion tokens of logs — states
plainly that for most evaluations it "was forced to rely on single runs without statistical
validation", because benchmarks cost between $13 and more than $450 per model per evaluation. That is
the honest version of the field's position, published by a group with every incentive to do otherwise.

**Construct.** "Agentic" is used as a capability label but measured as task success in a specific
environment with a specific scaffold. Scaffold and model are confounded in almost every comparison;
HAL finds generalist scaffolds cheaper in 20 of 24 model comparisons but with a substantial accuracy
penalty, which means the leaderboard ordering is a property of the pair, not the model.

**Cost and latency.** Cost is reported in a minority of papers and almost never as part of the
headline claim, even though the same accuracy can be bought at 50x the price [8] or at a 100x
difference between benchmarks [10].

**Selective prediction.** No agent benchmark reports risk-coverage curves; agents either answer or
fail. This is the gap closest to the lab's existing work, where an abstention gate over-refused on
answerable items (a contaminated private evaluation; no figure is quoted) — a failure that a
coverage-aware metric would have caught immediately and a bare accuracy number cannot express.

### 3.1 Six adversarial questions, answered with names

**How many published agent-benchmark results report variance over seeds or a confidence interval?**
Very few, and the papers that say so are explicit. [14] states that papers rarely report more than one
number per benchmark and that significance values are scarcely reported on release papers or
leaderboards. [8] states that agent evaluations are "rarely accompanied by error bars", and documents
the consequence: in their five-run reproductions, several reported scores sat above the maximum of
their five runs, and some reported baselines sat below the minimum. [10] reports single runs for most
of its own 21,730 rollouts. The most thorough reproduction attempt is [8], with five runs per agent on
HumanEval; the one with the most compute, [10], still could not afford replicates. So the defensible
answer is: single digits in percentage terms, and none of the large agent benchmarks reports item-level
uncertainty as a matter of course.

**What is the measured human-judge agreement for the most-used judges, and at what effect size does
judge noise exceed the claimed improvement?** The headline number is above 80% for GPT-4-class judges
on preference-style comparisons, matching human-human agreement [15]. On correctness-style judgements
of hard pairs it collapses: 50.86% for a vanilla GPT-4o judge, 56.57% with a stronger prompt, 57.43%
for the best fine-tuned judge, against a 50% chance baseline [20]. Position consistency for the best
judge was 0.828 [19], and disagreement concentrated on near-ties. The arithmetic that follows is
simple and rarely done: if a judge agrees with humans 80% of the time, its labels behave like a
measure with reliability ≈ 0.8, which attenuates an observed effect to 0.8 of its true size and
inflates the standard error by about 12%. With 200 judged items at p ≈ 0.5, the standard error of a
single-system accuracy estimate is about 3.5 points and of a paired difference somewhat less; a
claimed 2–3 point improvement is therefore inside the judge's own noise unless the judge is
calibrated against human labels on the same items and the analysis is paired. Below roughly 5 points,
an uncalibrated LLM judge cannot distinguish a real improvement from its own bias. Above roughly 10
points, the biases matter much less than the effect — which is why the judge literature's famous
results are all large effects.

**Which agent benchmarks are known to be gameable or saturated, and what replaced them?** SWE-bench
is the clearest case: 32.67% of successful patches involved leaked solutions, 31.08% passed on weak
tests, and the resolution rate fell by two-thirds after screening [27]. τ-bench is gameable by
returning nothing on impossible tasks, which scores 38% and beats a real agent [9]. WebArena
overestimates by 5.2 points through string matching [9], and its Reddit clone rate-limits actions so
that task order changes results [8]. Chatbot Arena's problems are structural rather than adversarial:
27 private variants from one provider tested before release, 19.2% and 20.4% of all battle data going
to two providers while 83 open-weight models shared 29.7%, and up to 112% relative gains available
from extra arena data alone
[23]. The replacements in 2025–2026 followed three patterns rather than one successor benchmark:
time-gated live sets that cannot be in a training corpus, exemplified by LiveCodeBench's 400 problems
drawn from contests in a fixed window [32]; private holdouts plus a standardised harness, exemplified by
HAL; and checklist-audited reward design, exemplified by ABC.

**Is there a documented case where a "significant" multi-agent or RAG improvement disappeared under
proper pairing or CIs?** Three partial cases, and one honest negative. Partial: a simple retry-with-
rising-temperature baseline was statistically indistinguishable from the best published agent
architecture while costing up to fifty times less, and reported scores fell outside the range of five
reproduction runs [8]; a fixed non-agentic pipeline beat every open-source agent on SWE-bench Lite at
$0.70 per issue [29]; and removing leaked and weakly-tested instances cut a headline resolution rate
from 12.47% to 3.97% [27]. For multi-agent specifically, the failure taxonomy paper reports that gains
are "often minimal" across seven frameworks and locates a whole failure category in verification [30].
Honest negative: I did not find a verified paper that takes one multi-agent system, re-runs it with
paired CIs and reports that the significant gain vanishes. That specific null is unpublished, which is
itself an opportunity (§6).

**Reviewer gates and verifier ensembles: does independent review improve correctness or mostly add
cost?** The measured answer depends on whether the reviewer sees new evidence. When the reviewer is
another LLM reading the same context, the critical survey finds no demonstrated success except in
tasks unusually suited to it, and finds that success appears when reliable external feedback exists
[31]. HAL's log analysis finds self-correction and verification *correlated* with task success across
1,634 transcripts from 36 model-scaffold pairs — but that is observational, and the plausible reading
is that stronger agents both verify more and succeed more, not that verification caused the success
[10]. Where verification injects external signal (executing tests, retrieving a document, checking a
database), the gains are well documented and the cost is real: ABC's audit exists because test-based
verification is itself unreliable [9]. So the honest summary is: review adds correctness in proportion
to the independence of its evidence, and adds cost always.

**Contamination: which cheap probes exist, and who validated them?** Three families, all CPU-feasible
at small scale. N-gram overlap is the cheapest and is validated as *insufficient*: paraphrase and
translation evade it, and 8–18% HumanEval overlap survived string-matching decontamination in large
pretraining corpora [25]. Membership-inference-style probes based on token probabilities (Min-K%) need
only black-box log probabilities and were validated against a benchmark constructed from pre- and
post-cutoff data [24]. Paraphrase sensitivity — measuring how much a score moves when items are
mechanically paraphrased — was demonstrated as a leakage signature by the same rephrasing work [25]
and is the probe with the best cost-to-evidence ratio for a student. What none of them gives you is a
calibrated false-positive rate on your own data, which is the open measurement problem in §6.

## 4. Benchmarks and datasets that a CPU laptop can actually use

The honest headline: of the seven large agent benchmarks, none is a laptop benchmark. They need
Docker fleets, VM images, hosted website clones or GPUs, and their per-evaluation costs are dollars to
hundreds of dollars before you count your own time. What a laptop can do is (a) run small
contamination and judge-calibration experiments on text-only subsets, and (b) re-analyse published
item-level predictions, which requires no environment at all and is where the cheapest publishable
results live.

| Benchmark | What it measures | Size | License | Judge required | CPU cost | Validity threat |
|---|---|---|---|---|---|---|
| AgentBench [1] | Multi-environment interactive task completion | 8 environments, 25 models benchmarked | Apache-2.0 (repo) | No — rule-based per environment | High: Docker plus several service backends; hours of setup | Static task set with no held-out environments, so agent-side overfitting is possible [8]; environment bugs dominate small score differences |
| WebArena [2] | Long-horizon web task completion, functionally checked | 812 tasks, 6 site clones | Apache-2.0 (repo) | No — programmatic checks | High: docker-compose, tens of GB of images | String-matching overestimates ~5.2 pts [9]; rate limits break task-order invariance [8]; hardcoded policies inflate scores [8] |
| SWE-bench [3] | Repository-level issue resolution | 2,294 issues, 12 repos (Lite/Verified are curated subsets) | MIT (repo) | No — unit tests | Very high: per-instance containers, minutes to hours each | Solution leakage 32.67%; weak tests 31.08%; >94% pre-cutoff [27] |
| τ-bench [6] | Policy-following tool use with a simulated user | 2 domains (retail, airline) | MIT (repo) | Yes — an LLM plays the user; any capable API model works | Medium: API calls only, no environment | Empty responses count as success on impossible tasks (38%) [9]; user simulator is itself an unvalidated judge |
| GAIA [5] | General assistant questions needing browsing and tools | 466 questions, 300 answers withheld | Gated on Hugging Face; no license stated on the dataset card | No — exact match, but answers are hidden | Medium: browsing plus inference; gated access is the real barrier | Held-out answers make local scoring impossible for the public split; contamination of the public split is unmeasurable |
| OSWorld [4] | Real desktop tasks across three OSes | 369 tasks | Apache-2.0 (repo) | No — execution-based | Very high: VM images, GUI automation | Heavy environment drift; multi-app tasks at 6.57% leave no headroom to measure small gains |
| MLE-bench [7] | End-to-end ML engineering on Kaggle competitions | 75 competitions | MIT (repo) | No — leaderboard grading | Not feasible: GPU plus hundreds of GB of competition data | The authors themselves test pre-training contamination; resource scaling confounds capability with spend |
| GSM1k [26] | Grade-school arithmetic, matched to GSM8k | 1,205 items, ~0.5 MB | None declared on the dataset card | No — exact match | Minutes to hours on CPU with a ≤3B model | Designed as a contamination contrast, not a capability benchmark; single-domain |
| BFCL (Gorilla repo) | Function-calling accuracy: AST and executable checks | Several hundred single- and multi-turn items | Apache-2.0 (repo) | No — AST/executable validation | Low: one model call per item, no environment | Single-turn emphasis; measures call syntax more than agentic behaviour |
| LiveCodeBench [32] | Contest coding with a time window | 400 problems (May 2023–May 2024) | MIT (repo) | No — test execution | Medium: sandboxed execution needed | Window closes; later models may still have seen the window |

Everything else in the table is either from the verified paper or from the repository's own metadata,
fetched from the GitHub API.

The judge column is the one that decides feasibility. Almost none of these benchmarks needs an LLM
judge — they need execution. The judge enters when you evaluate *open-ended* outputs (RAG answers,
summaries, trajectories), and there the evidence says a small local judge is not a primary metric:
the 7B open evaluator scored 34.86% on correctness-style pairs, below chance [20]. A 3B judge on a
laptop is useful for triage and for format compliance, and it is not usable to adjudicate a 3-point
difference.

## 5. Baselines and the cheapest statistically defensible harness on this hardware

### 5.1 What runs

Three CPU-served models cover the range: Qwen2.5-3B-Instruct at 4-bit GGUF (~2 GB, roughly 8–15
tokens/s on six threads for a Core Ultra-class chip), Llama-3.2-3B-Instruct at 4-bit (similar), and
Phi-3.5-mini at 4-bit if a slightly stronger small model is wanted. Embeddings come from a
MiniLM-class sentence encoder (~90 MB) which is fast enough to embed a few thousand passages in
minutes. The strong baseline is an API model, used at development time only, with its price and
version pinned in the log. Every number in this paragraph is an estimate to be replaced by a measured
tokens-per-second figure in the first hour of work; the harness should log it.

### 5.2 The harness

The design that survives review at n ≈ 500 items has six components, and none of them is expensive.

*Item-level logging.* Every run writes one JSONL row per item per seed with the system name, seed,
item id, task family, binary or scalar outcome, token counts, wall-clock time and dollar cost. Nothing
is aggregated until analysis. This single decision is what makes every later statistic possible, and
it is the thing most published agent papers cannot do because they logged only aggregate scores.

*Pairing.* Systems are compared on the same items, and the analysis runs on item-level differences.
Pairing is not a cosmetic choice: with a discordance structure typical of two similar systems (both
correct on 40% of items, each correct on 50%), the standard deviation of the paired difference is
about 0.45 against 0.71 unpaired, which buys roughly a 1.6x reduction in required sample size.

*Resampling.* Ten thousand bootstrap resamples over items, stratified by task family, recomputing the
paired difference each time; report the 2.5th and 97.5th percentiles. For binary outcomes, McNemar's
exact test on the discordant pairs is the cheap cross-check. With more than two systems, Holm-correct
the family: five systems means ten pairwise tests and a 22.6% chance of at least one false positive at
α = 0.05 if nothing is corrected.

*Seeds.* Three seeds per system per item is the minimum that lets you see tool-call nondeterminism;
report the per-seed spread alongside the pooled estimate. If the between-seed standard deviation is
larger than half the effect you want to claim, the claim is not available at this scale, and saying so
is a result.

*Power, decided in advance.* The detectable effect follows directly from the variance. At n = 500
items with a paired standard deviation of 0.45, the minimum detectable difference at 80% power and
α = 0.05 is about 5.6 points; at n = 200 it is about 8.9 points; at n = 1,000, about 4.0. Inverting
the same formula: detecting 5 points needs about 628 items, detecting 3 points needs about 1,744. The
published worked example in [13] reaches a similar place from a different variance assumption — about
969 questions for a 3-point difference — and recommends 1,000 items as a floor for new evals. The
practical translation for a student is blunt: **at 500 items you can defend a 5-point claim and
nothing smaller**, and a 2-point win reported to one decimal place is a description of your sampling
error.

*Judge calibration, if a judge is used at all.* Label 50–100 items by hand, measure agreement between
the judge and those labels on your own data, and report it. If agreement is below about 0.75, the judge
is a triage tool and the headline number must come from the human labels. If it is 0.8, remember the
attenuation: a judged experiment needs roughly 1/0.8² ≈ 1.56 times as many items as a human-labelled
one to reach the same precision, and the observed effect will read about 20% smaller than the truth.

*Reporting.* Accuracy with interval, cost per item in dollars and in seconds, the number of seeds, the
exact command, and the released item-level predictions. Confidence intervals at n = 500 are wide —
about ±4.4 points at p = 0.5, ±3.5 at p = 0.8 — and printing them next to the point estimate is the
single cheapest credibility signal available.

## 6. Five candidate gaps

**1. A variance-reporting audit of the 2025–2026 agent literature.** Nobody has counted, for a defined
corpus, how many agent papers report a seed variance, a confidence interval, or a per-item breakdown.
The cheapest experiment is a two-annotator extraction over 60–80 papers with a fixed codebook and a
reported κ, which is a week of work and needs no compute. The confound is that a paper may report
variance in an appendix table that the codebook does not reach, so the codebook must search
appendices; a second confound is that papers reporting CIs may be a biased sample of careful authors,
which limits causal claims about why.

**2. Judge-noise decision thresholds.** Given a claimed improvement, at what judge-human agreement
does the claim become unfalsifiable? This is arithmetic plus a resampling study on public judge
outputs, and it needs no model calls. The cheapest version: take a public pairwise-judge dataset,
simulate judges at agreement levels from 0.6 to 0.95 with position bias of varying strength, and
report the minimum detectable true effect as a function of agreement and n. The confound is that
simulated judge errors are usually independent of item difficulty, whereas real judge errors cluster
on near-ties [19] — so the simulation will be optimistic unless errors are made difficulty-dependent.

**3. Calibrated contamination probes.** Existing probes report detections, not false-positive rates.
A student can inject a known-contaminated subset (verbatim, paraphrased, translated) into a small
model's fine-tuning data and measure the ROC of n-gram overlap, Min-K% and paraphrase sensitivity at
detecting it. This is CPU-feasible with a 3B model and a few thousand items. The confound is realism:
injected verbatim contamination is easier to detect than the contamination that actually occurs, so
the measured sensitivity will be an upper bound, and the paper must say so.

**4. pass@k versus pass^k, recomputed from published logs.** The same system can look 94% capable at
pass@8 and 0.01% reliable at pass^8 when its per-attempt success rate is 0.3 — a swing of more than
90 points produced by metric choice alone. HAL released its agent logs, so a student can recompute
both metrics from real traces and measure how often leaderboard orderings flip. The confound is that
published logs come from scaffolds that were tuned for pass@1, so the recomputed pass^k may understate
what a reliability-tuned system could achieve.

**5. Selective prediction metrics for abstention gates.** No agent benchmark reports risk-coverage
curves, yet abstention is where deployed systems fail: the lab's own gate over-refused on answerable
items (contaminated private evaluation, no figure quoted), a failure invisible to accuracy-only
reporting. The cheapest experiment
is to take a public QA set, sweep an abstention threshold on a 3B model's confidence, and report AURC
and accuracy at fixed coverage against two baselines. The confound is that confidence is not
calibrated out of the box, so the curve may measure calibration failure rather than gate design; a
temperature-scaling step on a held-out slice is the control that must be included.

## 7. References

1. AgentBench: Evaluating LLMs as Agents (2023) arXiv:2308.03688.
2. WebArena: A Realistic Web Environment for Building Autonomous Agents (2023) arXiv:2307.13854.
3. SWE-bench: Can Language Models Resolve Real-World GitHub Issues? (2023) arXiv:2310.06770.
4. OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments (2024) arXiv:2404.07972.
5. GAIA: a benchmark for General AI Assistants (2023) arXiv:2311.12983.
6. τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains (2024) arXiv:2406.12045.
7. MLE-bench: Evaluating Machine Learning Agents on Machine Learning Engineering (2024) arXiv:2410.07095.
8. AI Agents That Matter (2024) arXiv:2407.01502.
9. Establishing Best Practices for Building Rigorous Agentic Benchmarks (2025) arXiv:2507.02825.
10. Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation (2025) arXiv:2510.11977.
11. Deep Reinforcement Learning that Matters (2017) arXiv:1709.06560.
12. Are We Really Making Much Progress? A Worrying Analysis of Recent Neural Recommendation Approaches (2019) Proc. 13th ACM Conference on Recommender Systems; arXiv:1907.06902.
13. Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations (2024) arXiv:2411.00640.
14. Quantifying Variance in Evaluation Benchmarks (2024) arXiv:2406.10229.
15. Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (2023) arXiv:2306.05685.
16. Large Language Models are not Fair Evaluators (2023) arXiv:2305.17926.
17. LLM Evaluators Recognize and Favor Their Own Generations (2024) arXiv:2404.13076.
18. Length-Controlled AlpacaEval: A Simple Way to Debias Automatic Evaluators (2024) arXiv:2404.04475.
19. Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge (2024) arXiv:2406.07791.
20. JudgeBench: A Benchmark for Evaluating LLM-based Judges (2024) arXiv:2410.12784.
21. Prometheus 2: An Open Source Language Model Specialized in Evaluating Other Language Models (2024) arXiv:2405.01535.
22. Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement (2024) arXiv:2407.18370.
23. The Leaderboard Illusion (2025) arXiv:2504.20879.
24. Detecting Pretraining Data from Large Language Models (2023) arXiv:2310.16789.
25. Rethinking Benchmark and Contamination for Language Models with Rephrased Samples (2023) arXiv:2311.04850.
26. A Careful Examination of Large Language Model Performance on Grade School Arithmetic (2024) arXiv:2405.00332.
27. SWE-Bench+: Enhanced Coding Benchmark for LLMs (2024) arXiv:2410.06992.
28. Evaluating Large Language Models Trained on Code (2021) arXiv:2107.03374.
29. Agentless: Demystifying LLM-based Software Engineering Agents (2024) arXiv:2407.01489.
30. Why Do Multi-Agent LLM Systems Fail? (2025) arXiv:2503.13657.
31. When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs (2024) arXiv:2406.01297.
32. LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code (2024) arXiv:2403.07974.
