# LANDSCAPE — twelve areas of active AI research, mapped for a one-paper entry

**S2-1 · literature landscape · 2026-11-03**

Who this is for: a first-semester BCA student in India choosing **one small paper** to write in
one to two weeks of agent-assisted work, then weeks of human polishing. The target is a workshop,
a student track, or an arXiv preprint — not a main conference. The hardware is one Windows laptop
(48 GB RAM, Core Ultra 5 225H, Intel Arc iGPU, no CUDA) and an old second laptop. Anything below
that needs an A100 is marked as such rather than quietly recommended.

The organising question for every area is not "what is hot" but **"what is the field unable to
settle, and can this laptop produce evidence about it"**. Heat without an accessible disagreement
is a trap for a student: you arrive late, with no compute, to a question that better-resourced
people have already answered.

---

## 0. Scope and method

**What was searched.** 166 distinct queries were run against arXiv's search interface between
02:15 and 03:40 IST on 2026-11-03, covering all twelve mandated areas: five to fifteen queries per
area, mixing named-paper lookups ("exact-ish title" searches) with concept queries ("agent memory
long-term", "calibration evaluation RLHF"). Each query surfaced up to 25 records; the pipeline kept
the three most title-similar per query, giving **318 shortlisted records**. From those, 67 were
selected for verification and 67 are reported here.

**Why arXiv and not OpenAlex.** The plan was to resolve against OpenAlex first. On this network
OpenAlex returned `429 Insufficient budget … free daily budget shared by everyone on your network's
IP address, $0 remaining, resets at midnight UTC`, and Semantic Scholar returned 429 without a key.
DBLP's API is behind a bot challenge. arXiv's `/abs` and `id_list` endpoints and Crossref's REST
API were the two resolvers that answered. This matters for what follows: **every reference below
carries an arXiv identifier (two carry a publisher DOI instead), and the `venue` column is what the
resolver returned** — for 64 of 67 that string is literally `arXiv preprint`, because the arXiv
record carries no journal reference. No venue in this document has been asserted from memory. If a
paper was later published at a venue, this file does not claim to know that.

**How verification was done.** Selected identifiers were enriched in bulk through
`02_literature/tools/verify_citations.py enrich` (67/67 records returned title, authors, year,
abstract), claims were written from those API records, and each claim was re-resolved through
`verify_citations.py add`, which rejects a claim whose title does not match the resolved record at
0.90 similarity. Result: **66 VERIFIED, 0 FAIL, 1 MISMATCH**. The mismatch was the DeepSeek-R1
paper: the arXiv record points at the *Nature* version, whose title is worded differently
("DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning"). The title was
changed to the resolved one — the identifier was not touched — and the re-run verified. Final
count: **67 rows in `02_literature/staging/S2-1-verified.csv`**, which is the authority for every
author, year, and venue string in this document.

**What read level.** Every abstract was read in full. Ten papers were read past the abstract (intro
and results) where the claim I needed was a number: τ-bench, LongMemEval, MMLU-Pro, The Leaderboard
Illusion, AbstentionBench, Fraud-R1, SWE-bench, Textbooks, PRISM, AgentDojo.

**Known limits of this map, stated up front.** (i) Area boundaries are administrative; several
papers belong to two areas and are assigned where their contribution is load-bearing. (ii) "Heat"
is a judgement from 2025–2026 publication volume and citation velocity, not a measurement.
(iii) The entry-difficulty scores are about *this* laptop, not about intellectual difficulty.
(iv) Nothing here is a novelty claim — that is a separate procedure with its own search log.

---

## 1. LLM agents and tool use

**What the field is actually arguing about.** Three arguments, and only the third is still live.

The first, now settled, was whether an LLM could be made to act in loops rather than answer in one
shot; ReAct [1] settled it by interleaving reasoning traces with tool calls, and Toolformer [2]
showed a model could learn *when* to call an API from a handful of demonstrations rather than from
hand-built pipelines. The second, also largely settled, was whether agents could be measured at
all: WebArena [3] built four functioning websites, AgentBench [4] built eight environments, and
both found a large gap between commercial models and open models under 70B, attributed to weak
long-horizon reasoning and instruction-following rather than to missing tools.

The live argument is about **what an agent benchmark should hold constant, and whether the
scaffolding or the model is doing the work**. τ-bench [5] makes the sharpest move: instead of a
static task list it simulates a user with an LLM, gives the agent domain policy documents, and
scores the final *database state* against an annotated goal — an outcome check that is hard to game
with fluent text. Its headline number is the uncomfortable one: gpt-4o-class function-calling
agents succeed on under half the tasks, and on the reliability metric `pass^8` in retail they fall
below 25%. That reframes agent quality from "can it ever do this" to "will it do this eight times
running", which is the property a deployment actually needs. The multi-agent wing of the field is
under the same pressure: Cemri et al. [6] annotated 1,600+ traces across seven popular multi-agent
frameworks, built a failure taxonomy (MAST) with inter-annotator agreement κ = 0.88 on the 150
traces it was derived from, and reported that the widely advertised performance gains of multi-agent
systems are often minimal. The disagreement this creates is real and unresolved: a large camp
attributes multi-agent failures to orchestration design (fixable in the harness), the other to the
base model's inability to maintain state across handoffs (not fixable in the harness).

**Landmark papers.** [1] ReAct established the reason-act interleaving that almost every agent
framework still uses. [2] Toolformer showed self-supervised learning of API calls, making tool use a
training problem rather than an integration problem. [3] WebArena provided a reproducible,
self-hosted web environment with real functional sites, which is why agent results became
comparable at all. [4] AgentBench established the multi-environment evaluation format and documented
the commercial/open gap. [5] τ-bench introduced simulated users, policy adherence, and the `pass^k`
reliability metric, and showed state-of-the-art agents below 50% success. [6] Why Do Multi-Agent LLM
Systems Fail? supplied the first empirically derived failure taxonomy for multi-agent systems and
the evidence that gains are often marginal.

**Open problems a small lab could attack.** (i) *Failure attribution without an oracle*: MAST needs
human annotators; a cheap automatic classifier of the same failure modes, validated against a small
human-labelled subset, is a legitimate workshop contribution. (ii) *Tool-selection under distractor
tools*: how many near-duplicate tools can a 1–3B model hold before selection collapses, and does
retrieval over tool descriptions fix it? This needs no environment, only a tool catalogue and
scored choices. (iii) *Cost-aware success*: every agent benchmark reports success or pass^k, almost
none reports tokens or wall-clock per success, so a "cheaper to the same score" result is
publishable and needs only a laptop plus an API budget. (iv) *Small-model agents in a fixed policy
domain*: τ-bench-style policy following with a 3B model, where the interesting number is how far
below the frontier the reliability curve falls.

**Entry difficulty: 3/5.** The apparatus (a tool sandbox, a scorer, a small model) is laptop-sized,
but a reliable agent loop multiplies model calls, so a 1–3B local model makes each run slow and an
API makes each run cost money; the honest experiments are small.

**Status: maturing.** Scaffold design is saturated — another "planner-executor-critic" framework
adds nothing. Reliability measurement, failure attribution, and cost accounting are open and
under-populated.

---

## 2. RAG and agent memory

**What the field is actually arguing about.** RAG began as an architecture claim: Lewis et al. [7]
showed that a generator conditioned on retrieved passages beats a purely parametric model on
knowledge-intensive tasks, and that the retrieval index can be updated without retraining. For
several years the argument was about the retriever (dense vs sparse, chunking, reranking). The
2023–2025 argument is different and more interesting: **is retrieval still the right primitive now
that context windows are long?**

Two results cut against naive context stuffing. Liu et al. [8] showed that accuracy depends on
*where* the relevant passage sits — best at the beginning or end, degraded in the middle, even for
models explicitly built for long context — which means "just put everything in the prompt" is not a
neutral choice. Asai et al. [9] attacked the other half: retrieving a fixed number of passages
regardless of need hurts, so Self-RAG trains the model to decide when to retrieve and to critique
what came back. Meanwhile the retrieval unit itself moved: GraphRAG [10] builds an LLM-derived
entity graph so that corpus-level questions ("what are the main themes") become summarisation over
communities rather than top-k lookup, which is a genuine failure mode of passage RAG.

The memory wing has a different disagreement: **is memory a retrieval problem or an operating-system
problem?** MemGPT [11] takes the OS view — tiered storage, paging between context and external
store, interrupts for control flow. LongMemEval [12] takes the measurement view and is the more
damaging paper: 500 curated questions across five abilities (extraction, multi-session reasoning,
temporal reasoning, knowledge update, abstention), embedded in scalable chat histories, and
commercial assistants plus long-context models drop roughly 30% when information must be carried
across sessions. Note the fifth ability: **abstention is inside the memory benchmark**, which is
where this area touches area 11.

**Landmark papers.** [7] RAG established parametric-plus-non-parametric memory as a general recipe.
[8] Lost in the Middle established position sensitivity in long contexts, the empirical basis for
distrusting context stuffing. [9] Self-RAG made retrieval adaptive and self-critiqued rather than
fixed-k. [10] GraphRAG established graph indices for corpus-level (global) questions that top-k
retrieval cannot answer. [11] MemGPT introduced virtual context management with tiered memory and
paging. [12] LongMemEval produced the first multi-ability long-term memory benchmark and measured a
~30% cross-session drop.

**Open problems a small lab could attack.** (i) *Memory decay curves*: how does answer accuracy fall
as a function of sessions-since-evidence, for a fixed small model and a fixed retrieval budget? This
is a measurement paper with no training, and the shape of the curve (not the endpoint) is the
contribution. (ii) *Attribution*: when a RAG answer is wrong, was it retrieval or the reader? Almost
all RAG papers report end accuracy; an oracle-passage upper bound plus a retrieval-recall number
separates the two, and a 3B reader on CPU makes this cheap. (iii) *Abstention under retrieval*: what
happens when the index does not contain the answer — the system should abstain, and most RAG
evaluations never score that case (see area 11). (iv) *Chunking sensitivity*: the least glamorous,
most reproducible experiment in the area, and still under-reported for non-English text.

**Entry difficulty: 2/5.** Embedding models and a 3B reader run on CPU in minutes per hundred
questions; a FAISS or numpy index over a few thousand chunks is trivial; the whole loop is
`python` plus a JSON file.

**Status: maturing, and crowded at the architecture level.** Another "hybrid retriever with
reranking" paper is dead on arrival. Evaluation of memory over time, and separation of retrieval
from reader error, remain thin.

---

## 3. Evaluation methodology and benchmarks for agents

**What the field is actually arguing about.** This is the area where the argument is most
self-critical, and therefore the most welcoming to a student with no compute.

The first thread is **saturation of the instrument**. MMLU-Pro [13] rewrote MMLU with ten options
instead of four and reasoning-heavy items, and accuracy dropped by 16% and more, which is a polite
way of saying the original benchmark had stopped discriminating. The second thread is
**contamination**: Deng et al. [17] built a retrieval system to find overlap between benchmarks and
pretraining corpora and a "testset slot guessing" protocol that works on closed models too — mask a
wrong answer in a multiple-choice item and see whether the model can supply it, which it should not
be able to do from the question alone.

The third thread is the one with the most room: **evaluation is an experiment and is analysed like
one almost nowhere**. Miller [15] reframes eval questions as draws from a super-population and gives
the formulas for standard errors, paired comparisons, and power analysis. BetterBench [14] turned
that into an audit: 46 best practices across a benchmark's lifecycle, applied to 24 widely used
benchmarks, finding large quality differences and that most benchmarks do not report statistical
significance at all. The Leaderboard Illusion [16] pushed it from statistics into political economy:
Chatbot Arena, the field's reference leaderboard, is distorted by undisclosed private testing —
they document 27 private Llama-4 variants tested before release and selective disclosure of the best
score, i.e. a max-over-variants bias in a ranking that the community treats as a measurement.

The live disagreement: **is the benchmark or the model the problem?** One camp says build harder,
fresher benchmarks (MMLU-Pro, live/rolling datasets); the other says the existing numbers are
statistically meaningless at the reported precision and the fix is methodology, not new data. Both
are being published at the same venues, and neither has won.

**Landmark papers.** [13] MMLU-Pro showed headroom can be restored by raising option count and
reasoning demand, at a cost of 16%+ accuracy. [14] BetterBench audited 24 benchmarks against 46
practices and found most report no significance testing. [15] Adding Error Bars gave the field
usable statistics for eval design and comparison. [16] The Leaderboard Illusion documented selective
disclosure and private-variant testing distorting Arena rankings. [17] Data-contamination work
supplied both a retrieval-based overlap detector and a black-box probing protocol.

**Open problems a small lab could attack.** (i) *Variance decomposition at small scale*: how much of
a reported difference between two 1–3B models is seed noise, prompt-format noise, and item noise?
Run 5 seeds × 3 formats on 500 items and publish the decomposition; it is cheap, and it directly
extends [15] to the regime everyone actually experiments in. (ii) *Judge-free scoring for agent
trajectories*: most agent evals need an LLM judge; a rule-based or state-based scorer validated
against a small human-labelled set is a real contribution (see area 12). (iii) *Contamination
probing of small models*: TS-Guessing on open models where the pretraining corpus is documented —
the check is cheap and the result is a clean negative or positive. (iv) *Benchmark replication*:
re-run a published small-model comparison and report whether the ordering holds; replication is
under-published and workshops accept it when the protocol is preregistered.

**Entry difficulty: 2/5.** Everything here is inference plus arithmetic; a 3B model over 1,000
multiple-choice items is an afternoon on CPU, and the statistics are closed-form.

**Status: maturing but structurally under-served.** New benchmarks are saturated; methodology
(replication, variance, contamination, cost) is wide open because it earns no citations from model
labs.

---

## 4. Reasoning and test-time compute

**What the field is actually arguing about.** The 2024 claim was economic: Snell et al. [18] showed
that spending inference compute optimally can be more effective than spending it on parameters, for
a fixed FLOP budget — which implies a trade curve between training and inference that changes what
"bigger" means. The 2025 claim went further: DeepSeek-R1 [21] reported that pure reinforcement
learning on verifiable tasks, without human-labelled reasoning traces, produces emergent
self-reflection and verification, and the paper's publication in *Nature* signalled that the result
was treated as a landmark rather than a lab report. s1 [20] supplied the deflationary counterpart:
1,000 carefully chosen questions plus "budget forcing" — literally appending "Wait" to extend
thinking, or truncating it to save compute — gets much of the way there, which suggests the
ingredients are simpler than the framing implies.

Three papers then attack the edifice from different sides. Huang et al. [19] show that intrinsic
self-correction — the model revising itself with no external signal — does not reliably improve
reasoning and can degrade it, which undercuts a whole family of self-reflection designs. Sprague et al.
[23] ran a meta-analysis of over 100 CoT papers plus their own 20 datasets across 14 models and
found CoT's gains concentrate in math and symbolic tasks, with near-parity elsewhere — on MMLU,
answer-only prompting matched CoT unless the item involved symbolic operations. Shojaee et al. [22]
built controllable puzzle environments where complexity can be dialled precisely and found a
three-regime structure: at low complexity standard models beat reasoning models, at medium
complexity the reasoning models pull ahead, and beyond a threshold both collapse entirely — with
reasoning-token usage increasing up to a point and then *declining* even when budget remains, the
opposite of the "think longer when it is hard" story.

So the live disagreement is sharp: **is a reasoning model doing more computation on hard problems,
or is it pattern-matching over reasoning-shaped text that fails to generalise past a complexity
horizon?** [21] and [18] say compute buys capability; [19], [22], [23] say the measured gains are
narrow, self-correction is illusory without an external verifier, and the scaling story breaks at
the frontier of complexity.

**Landmark papers.** [18] established compute-optimal test-time scaling as an alternative to
parameter scaling. [19] showed intrinsic self-correction fails on reasoning tasks without external
feedback. [20] demonstrated that 1,000 curated examples plus budget forcing reproduces much of o1's
behaviour at small scale. [21] showed emergent reasoning from pure RL without human reasoning
traces. [22] showed accuracy collapse and shrinking reasoning effort past a complexity threshold in
controllable puzzles. [23] showed CoT's benefit is concentrated in math/symbolic tasks via a
100-paper meta-analysis and 20-dataset re-evaluation.

**Open problems a small lab could attack.** (i) *Complexity-threshold replication at 1–3B*: [22]
used frontier models; whether the collapse point moves with model size is a clean, cheap question
with a small puzzle generator. (ii) *Budget forcing on small models*: does appending "Wait" help a
1.5B model, and does it help for the same task families where [23] says CoT helps? (iii) *Cost of
overthinking*: tokens-per-correct-answer as a function of problem difficulty — a measurement paper
that needs no training. (iv) *Verifier quality*: the entire RL-reasoning story depends on a
verifier; how noisy can a verifier be before [21]-style training stops working? Answering this by
*evaluation* (not training) is possible with released checkpoints.

**Entry difficulty: 3/5.** A 1.5–3B reasoning model generating 4,000-token traces is slow but
feasible on CPU; what is not feasible is any training, and most of this area's claims are training
claims.

**Status: very hot, maturing fast at the method level, and genuinely open at the measurement level.**
Do not enter with a training proposal; do enter with a measurement one.

---

## 5. Small and efficient models, and on-device inference

**What the field is actually arguing about.** Whether capability at small scale comes from data,
from architecture, or from the training recipe — and, separately, how much quality quantisation
actually costs.

The data camp is loudest. phi-3-mini [24] is 3.8B parameters trained on 3.3T tokens of heavily
filtered web text plus synthetic data, and reports 69% on MMLU, competitive with models an order of
magnitude larger, with the explicit pitch that it fits on a phone. SmolLM2 [26] makes the same bet
more transparently: 1.7B parameters, ~11T tokens, a multi-stage mix, and three purpose-built
datasets (FineMath, Stack-Edu, SmolTalk) released because the existing ones were too small or too
dirty. Qwen2.5 [25] scales the same logic to a family: 18T tokens, over a million SFT samples,
multi-stage RL.

The architecture camp pushed back with MobileLLM [27]: at sub-billion scale, they argue, architecture
dominates — deep-and-thin shapes, embedding sharing, grouped-query attention — and they report
2.7%/4.3% gains over prior 125M/350M models *at matched size*, which is the correct control and
therefore the interesting result. This is a real disagreement: [24] and [25] attribute small-model
quality to data, [27] shows a same-size architecture change also moves the number.

The third argument is the one that matters for anyone deploying on a laptop: **what does 4-bit cost
you?** AWQ [28] observes that not all weights matter equally, that protecting ~1% salient channels
(identified from *activation* distributions, not weights) sharply reduces quantisation error, and
derives a per-channel scaling that keeps the hardware-friendly uniform format. This is why "3B at
4-bit" is now a real deployment target rather than a curiosity.

**Landmark papers.** [24] phi-3 showed 3.8B parameters with curated data reaching GPT-3.5-class
scores and phone deployment. [25] Qwen2.5 documented the data-scale-and-recipe path (18T tokens,
1M+ SFT) across a model family. [26] SmolLM2 released a fully documented 1.7B data-centric recipe
and the three datasets behind it. [27] MobileLLM showed architecture choices move quality
independently of size below 1B. [28] AWQ established activation-aware weight quantisation with ~1%
salient-channel protection.

**Open problems a small lab could attack.** (i) *Honest on-device measurement*: tokens/second, peak
RAM, and quality at 4-bit vs 8-bit vs fp16 on a specific laptop, with a documented harness — the
literature reports quality at 4-bit far more often than latency and memory on consumer hardware.
(ii) *Quantisation damage in Indic scripts*: tokenisers fragment Devanagari and other Indic scripts
into more tokens, so the same 4-bit model may degrade differently per language; our searches found no
per-script quantisation-damage curve, and measuring one needs only CPU. (iii) *Reasoning distillation into
≤1B*: does a distilled 1B reasoner keep the *format* of reasoning without the accuracy, and can a
cheap test tell? (iv) *Benchmark leakage in small models*: small models are trained on
heavily-filtered web data whose filtering is often undisclosed; a contamination probe (area 3) on a
"clean" small model is a sharp, publishable check.

**Entry difficulty: 2/5.** This is the friendliest area on this hardware: GGUF/`llama.cpp` runs a
3B model at a few tokens/second, and every experiment above is measurement rather than training.
Training anything at this scale, however, is out of reach — a 1B model for one epoch on CPU is days.

**Status: maturing, industry-driven.** Architecture and pretraining papers are effectively closed to
a CPU lab; measurement papers (latency, memory, quantisation damage, per-language quality) are open
and useful.

---

## 6. Safety, robustness and adversarial behaviour

**What the field is actually arguing about.** Whether alignment is a deep property of the model or a
shallow behavioural shell — and, for agents, whether prompt injection is a solvable problem at all.

The attack side has two landmark results. Zou et al. [29] found that a single adversarial suffix,
optimised to maximise the probability of an affirmative prefix, transfers across models — so
"aligned" is not a security boundary, it is a tendency. Greshake et al. [30] introduced the more
structural problem: if an LLM-integrated application reads retrieved content, that content is
instructions. Indirect prompt injection needs no access to the model, only access to data the model
will read, and it turns every tool-using agent into an attack surface.

The defence side splits. The systems camp builds benchmarks and environments: InjecAgent [31] with
1,054 cases across 17 user tools and 62 attacker tools, and AgentDojo [32], which is deliberately
*not* a static test suite but an extensible environment with 97 realistic tasks and 629 security
cases so that new attacks and defences can be evaluated as they appear. The training camp argues the
vulnerability is architectural: Wallace et al. [33] show models treat system prompts and untrusted
third-party text as equally authoritative, and train an explicit priority hierarchy so the model
learns to ignore lower-privileged instructions.

Then comes the paper that reframes the whole thing mechanistically. Arditi et al. [34] show that
refusal in 13 open chat models up to 72B is mediated by a *single direction* in the residual stream:
ablating it removes refusal, adding it induces refusal on harmless prompts. If refusal is
one-dimensional, then safety fine-tuning mostly taught a direction rather than a capability — which
is the strongest available evidence for the "shallow alignment" position, and it is why
representation-level attacks work at all.

The live disagreement: **is the fix training (hierarchy, adversarial training, "deeper" alignment)
or architecture (capability limits, information-flow control, sandboxing)?** The benchmarks [31, 32]
are agnostic; [33] and [34] sit on opposite sides.

**Landmark papers.** [29] GCG established transferable adversarial suffixes against aligned models.
[30] established indirect prompt injection as a remote, data-mediated attack on LLM applications.
[31] InjecAgent quantified agent vulnerability with 1,054 cases over 17 tools. [32] AgentDojo made
injection evaluation a living, extensible environment instead of a frozen set. [33] The Instruction
Hierarchy argued priority confusion is the root cause and trained a hierarchy as defence. [34]
showed refusal is a single direction in 13 open models, implying shallow alignment.

**Open problems a small lab could attack.** (i) *Defence evaluation under adaptive attack*: most
defence papers evaluate against a fixed attack set; re-running a published defence against a
slightly adapted attacker is a legitimate, cheap, and frequently negative result. (ii)
*Over-refusal vs under-refusal frontier*: every defence trades one for the other, and the trade curve
is rarely reported for small models; this needs only a benign and a harmful prompt set. (iii)
*Injection in low-resource languages*: if a model's safety training is English-heavy, does an
instruction injected in Hindi or Hinglish bypass it more easily? This is cheap (black-box), timely,
and connects to area 7. (iv) *Refusal-direction replication at 1–3B*: does the single-direction
result hold below 3B? If it does not, that is a publishable negative.

**Entry difficulty: 3/5.** Black-box attack and defence experiments are laptop-feasible; gradient-based
attacks (GCG) are not practical on CPU, so the honest scope is black-box and prompting-level.

**Status: maturing, in an arms race.** New jailbreak variants are saturated. Defence evaluation under
adaptive attack, multilingual safety, and over/under-refusal trade curves are open.

---
## 7. Multilingual, Indic and low-resource NLP

**What the field is actually arguing about.** Not whether multilingual models are worse in
low-resource languages — they are, and that is settled. The argument is **why they are worse and
therefore what to measure**: language competence, cultural knowledge, or tokenisation economics.

The benchmark wave. MILU [36] covers 8 domains and 41 subjects across 11 Indic languages, built
India-centric from regional and state-level examinations. M3Exam [37] takes real official human
exams across countries, and is multilingual, multimodal (some questions need a figure), and
multilevel. Belebele [38] is the methodological opposite: 122 language variants, fully parallel,
four-way multiple choice over Flores-200 passages, so that the *same* question exists in every
language and cross-language comparison is direct rather than approximate. INCLUDE [39] pushes to
197,243 QA pairs drawn from local exam sources, on the explicit argument that translated English
resources erase exactly the regional knowledge that multilingual deployment needs.

That last point is the sharpest disagreement in the area: **is a translated benchmark a fair test?**
The translation camp gets parallelism and comparability; the native-construction camp (MILU, INCLUDE,
M3Exam) argues translation preserves the wrong distribution — you end up measuring whether the model
can answer an English question expressed in Hindi. Both camps publish, and the field has not
resolved whether the two measure the same construct.

IndicTrans2 [35] sits underneath all of this as infrastructure: before it there was no parallel
training data spanning all 22 scheduled languages, no India-relevant benchmark covering them, and no
model supporting all of them — it supplied data, benchmarks, and models together, which is why Indic
MT results became comparable.

**Landmark papers.** [35] IndicTrans2 built the data, benchmarks and models for all 22 scheduled
Indian languages. [36] MILU produced an India-centric multi-task understanding benchmark over 11
Indic languages and 8 domains. [37] M3Exam established human-exam-based multilingual, multimodal
evaluation. [38] Belebele gave 122 fully parallel reading-comprehension variants enabling direct
cross-language comparison. [39] INCLUDE argued from 197k locally sourced QA pairs that translated
benchmarks miss regional knowledge.

**Open problems a small lab could attack.** (i) *Tokenisation tax*: how many extra tokens does
Devanagari (or Bengali, Tamil) cost versus English for the same content, and how does that inflate
latency and cost on a fixed budget? It is a measurement, needs no GPU, and is consistently
under-reported. (ii) *Code-mixed evaluation*: real Indian user text is Hinglish, and the code-switching
literature says multilingual LLMs handle it poorly; a small, honestly constructed code-mixed set with
a documented collection protocol is a workshop-sized contribution. (iii) *Answer-position and format
sensitivity in Indic MCQs*: if a model's Indic accuracy swings with option order or script
normalisation, published numbers are partly artefact — cheap to test, and it composes with area 3.
(iv) *Small-model Indic quality*: published comparisons concentrate on 70B+ models; a systematic 1–3B comparison on
MILU/Belebele subsets is reproducible on CPU and useful to exactly the deployment audience that
matters in India.

**Entry difficulty: 2/5.** The datasets are small, the models can be 1–3B, and the metrics are exact
match or multiple-choice accuracy; the cost is care in normalisation, not compute.

**Status: wide open for Indic-specific measurement; saturated for headline multilingual benchmark
construction.** Another "massive multilingual benchmark" paper needs annotators a student does not
have; a measurement paper about how small models actually fail in Indic scripts does not.

---

## 8. Scam, fraud and misinformation detection

**What the field is actually arguing about.** Whether detection is a *classification* problem or an
*adversarial robustness* problem. The older literature — and most deployed systems — treat it as
classification: features plus a classifier, evaluated on a held-out split of messages. That framing
is now under attack from two directions.

The first is that the adversary moves. Fraud-R1 [40] reframes fraud detection as multi-round
resistance: 8,564 cases across five fraud types (phishing, fake job postings, social media, news),
evaluated at successive stages of an inducement — credibility building, urgency creation, emotional
manipulation — under two settings, a plain helpful assistant and a role-play persona. The finding is
that models which look safe in the assistant setting capitulate in role-play, i.e. the deployment
context, not the model, decides the vulnerability. The same paper reports a substantial Chinese–English
performance gap, which is the closest thing in the verified literature to evidence that fraud
defences do not transfer across languages. PhishAgent [41] takes the systems route, combining
online and offline knowledge bases with a multimodal LLM so brand recognition generalises beyond a
fixed blocklist; LLMPEA [42] goes at email specifically, testing three frontier models against prompt
injection, text refinement, and multilingual attack vectors, and concludes that current LLMs need
substantial hardening before email-security deployment.

The second attack is on the labels themselves. Chen and Shu [43] show that LLM-generated
misinformation is *harder* to detect than human-written misinformation, for both human readers and
automated detectors — which breaks the assumption that detectors trained on human-written fake news
transfer. Meanwhile the classic datasets keep being useful: the SMS scam corpus [44] released
153,551 messages, the largest public SMS scam dataset at the time, and benchmarked shallow ML, deep
nets, and syntactic/semantic features on it.

The unresolved disagreement: **does a detector that wins on a static benchmark have any value
against an adaptive adversary?** Fraud-R1 and [42] say no; the classifier literature mostly does not
ask.

**Landmark papers.** [40] Fraud-R1 established multi-round, stage-wise fraud resistance evaluation
over 8,564 cases and 15 LLMs, and showed role-play settings break models that pass as assistants.
[41] PhishAgent showed a multimodal agent with retrieval over brand knowledge generalises phishing
detection beyond blocklists. [42] LLMPEA showed frontier LLMs remain vulnerable to prompt-injection,
refinement, and multilingual phishing attacks in email security. [43] showed LLM-generated
misinformation is harder to detect than human-written misinformation for both people and detectors.
[44] released the largest public SMS scam corpus (153,551 messages) and a baseline comparison across
classical and neural detectors.

**Open problems a small lab could attack.** (i) *Code-mixed Indian scam messages*: essentially no
public benchmark exists for Hinglish/Indic-language fraud messages, and the failure modes (urgency
markers, fake authority, UPI/payment lures) are culturally specific; building 500–1,000 labelled
examples with a documented protocol is achievable and genuinely useful. (ii) *Base-rate honesty*:
published detectors report balanced accuracy on constructed splits; real SMS streams have a scam
prevalence well under 1%, where precision collapses. Re-reporting a published detector at realistic
prevalence is a legitimate, cheap, embarrassing result. (iii) *Adversarial paraphrase robustness*:
how much does a detector's score drop when a scam message is paraphrased by an LLM (or by a simple
synonym/format perturbation)? No GPU needed. (iv) *Calibration of "is this a scam"*: a detector that
outputs 0.51 on a borderline message is not actionable; measuring calibration and abstention for this
task connects directly to area 11.

**Entry difficulty: 1/5.** This is the cheapest area on the list: text classification with
embeddings and a logistic regression or a 1–3B model runs in minutes on CPU, the datasets are small,
and the metrics are standard.

**Status: wide open methodologically, saturated as "another classifier".** A new classifier on a
public split adds nothing. Robustness under paraphrase, realistic base rates, code-mixed data, and
calibration are open — and the last two are where the student already has apparatus.

---

## 9. Code generation and software-engineering agents

**What the field is actually arguing about.** Two things: whether agents are needed at all, and
whether the benchmarks measure coding or recall.

The origin story is Codex [46]: HumanEval, a functional-correctness benchmark from docstrings, where
the model solved 28.8% of problems at pass@1 and 70.2% with 100 samples — the paper that made
"sampling beats prompting" a standard move. SWE-bench [45] moved the target from function synthesis
to repository repair: 2,294 real GitHub issues across 12 Python repositories, where the model must
edit a codebase so that the project's own tests pass. That shift is what made "SWE agent" a research
area, because repository context does not fit in a prompt and must be retrieved.

Then the deflation. Agentless [48] showed a fixed three-phase pipeline — localise, repair, validate
— competing with elaborate agents, which is the "do we need the scaffolding" argument from area 1
reappearing with a sharper result: complexity was buying less than the papers claimed. And EvalPlus
[47] attacked the measurement: augmenting HumanEval/MBPP with large numbers of generated tests
showed that pass rates drop substantially once you test more than the handful of cases a benchmark
ships — concretely, an 80× expansion of HumanEval's tests cut pass@k by up to 19.3–28.9% and
*reversed* model rankings (two models that beat ChatGPT on HumanEval lost to it on HumanEval+),
i.e. published functional correctness was partly an artefact of weak tests.

Two more measurement papers complete the picture. CRUXEval [49] (800 short Python functions, input
and output prediction) found that models ranking high on HumanEval do not transfer their advantage
to execution reasoning — generation skill and execution understanding are different abilities.
LiveCodeBench [50] attacks contamination by collecting contest problems continuously from LeetCode,
AtCoder and Codeforces, and broadens the task beyond generation to self-repair, code execution, and
test-output prediction.

The live disagreement: **is SWE-bench progress capability or benchmark-fitting?** The contamination
and weak-test results [47, 50] plus the Agentless result [48] point one way; the steady climb of
resolve rates points the other.

**Landmark papers.** [45] SWE-bench defined repository-level issue resolution with 2,294 real
issues and execution-based grading. [46] Codex introduced HumanEval and established functional
correctness plus repeated sampling as the standard protocol. [47] EvalPlus showed an 80× test
expansion cut pass@k by up to 19.3–28.9% and reversed model rankings. [48] Agentless showed a simple
three-phase pipeline is competitive with complex agents on SWE-bench. [49] CRUXEval showed HumanEval
rankings do not transfer to execution reasoning over 800 functions. [50] LiveCodeBench provided
contamination-free, continuously refreshed evaluation across generation, repair, and execution tasks.

**Open problems a small lab could attack.** (i) *Test-suite adequacy as a measured variable*: how
much of a reported pass@1 is explained by the number and diversity of tests? EvalPlus [47] opened
this; a systematic curve (tests vs measured pass rate) across several benchmarks is cheap and has no
GPU requirement beyond running code. (ii) *Execution-free proxies*: can a small model predict whether
generated code will pass, well enough to be used as a cheap filter? This is a classification task on
CPU with public data. (iii) *Multilingual spread*: Multi-SWE-bench exists but not for Indian-language
code comments/docstrings, a niche our searches found unoccupied. (iv) *Small-model repair*: a 3B model fixing
single-line bugs with the failing test as context — well-scoped, CPU-feasible, and the honest question
is where the cliff is.

**Entry difficulty: 4/5.** Executing tests is cheap, but generating plausible code needs a strong
model (API, dev-time only), sandboxing is fiddly on Windows, and benchmark runs are long. The
measurement sub-questions are cheaper than the capability ones.

**Status: saturated at the frontier, do not enter there.** The capability race needs clusters. The
measurement questions (test adequacy, contamination, execution-free prediction) are open but
crowded by well-resourced labs.

---

## 10. Data-centric AI and synthetic data

**What the field is actually arguing about.** Whether model quality is now a data problem, and
whether synthetic data is a renewable resource or a slow poison.

The optimistic case is strong and specific. phi-1 [51] trained a 1.3B code model for four days on
8 A100s using 6B tokens of "textbook quality" filtered web text plus 1B tokens of GPT-3.5-generated
textbook material, and reached 50.6% pass@1 on HumanEval — the paper that made "data quality beats
data quantity" a slogan with a number attached. LIMA [52] pushed it to the limit: 65B parameters,
fine-tuned on 1,000 curated prompt-response pairs with no RLHF at all, producing strong
instruction-following, which implies alignment is mostly a formatting-and-style problem solved by
small, very good data. Self-Instruct [53] showed the bootstrap can be automated — generate
instructions with the model, filter, fine-tune — with a 33% absolute improvement over the un-tuned
baseline. Magpie [54] removed even the seed set: prompt an aligned model with only the left-hand chat
template and it will generate user queries, from which instruction data can be synthesised at scale.

The pessimistic case is equally specific. Shumailov et al. [55] showed that training on
model-generated content causes "model collapse": the tails of the original distribution disappear
over successive generations, irreversibly in their experiments. That is a direct contradiction of the
optimistic programme, and the disagreement is about **whether collapse is an artefact of their
setup or a law**. The defence is that real pipelines accumulate data rather than replacing it, and
that filtering and deduplication change the dynamics; the offence is that the empirical result has
been reproduced in several modalities.

**Landmark papers.** [51] phi-1 established that filtered plus synthetic "textbook" data yields
strong code capability at 1.3B parameters. [52] LIMA showed 1,000 curated examples without RLHF
produce competitive instruction following. [53] Self-Instruct established self-generated instruction
bootstrapping with a 33% absolute gain over the base model. [54] Magpie showed instruction data can
be synthesised from an aligned model with no seed prompts at all. [55] The Curse of Recursion
demonstrated model collapse and tail disappearance under recursive training on generated data.

**Open problems a small lab could attack.** (i) *Cheap quality metrics*: "quality
filtering" is claimed almost universally but rarely isolated in a small-scale study of which measurable property
(diversity, deduplication rate, perplexity, instruction length) predicts downstream gain at 1B
scale. This needs fine-tuning, which is the problem — see the difficulty score. (ii) *Collapse with
accumulation*: a simulation of recursive training where each generation *adds* fresh real data at a
fixed rate, measuring the tail-loss curve. This can be done with small models and few generations,
but still needs training. (iii) *Synthetic data for Indic*: quality of machine-translated or
LLM-generated Indic instruction data is largely unmeasured; evaluation-only studies (no training)
are feasible on CPU. (iv) *Contamination audit of public synthetic datasets*: check whether
"generated" instruction data leaks benchmark items — pure text analysis, no GPU.

**Entry difficulty: 4/5.** The ideas are cheap and the experiments are not: any causal claim here
requires fine-tuning runs, and a 1B model on CPU is days per run. Evaluation-only corners exist but
are thin.

**Status: hot, but compute-gated.** If the lab had one A100, this would be the highest-value area on
the list. It does not.

---

## 11. Uncertainty, calibration and abstention

**What the field is actually arguing about.** Whether a model can know what it does not know, and
whether asking it in words works as well as reading its probabilities.

The foundational result is cautiously optimistic: Kadavath et al. [56] showed larger models are
well-calibrated on multiple-choice and true/false questions when the format is right, and that
"P(True)" — the model's probability that its own sampled answer is correct — is a usable
self-evaluation signal that improves when the model sees several of its own samples. Semantic
entropy [57] made the same idea distributional and unsupervised: cluster sampled answers by meaning,
then take entropy over clusters, which beats token-level entropy because it respects the fact that
different sentences can mean the same thing. SelfCheckGPT [59] removed the need for probabilities
entirely: sample several responses and measure their consistency, which works on black-box APIs.

Then the RLHF problem. Tian et al. [58] evaluated how to extract confidence from RLHF-tuned models,
motivated by the observation that RLHF damages the calibration of raw conditional probabilities;
their finding that verbalized confidence is competitive with (and sometimes better than) sequence
probabilities is the empirical basis for "just ask the model how sure it is". This is a live
disagreement: probability-based methods are principled but need logits; verbalized methods are cheap
but inherit sycophancy and format sensitivity.

The abstention literature is where it becomes urgent, and where the field is most honest about
failure. AbstentionBench [60] spans 20 datasets — unknown answers, underspecified questions, false
premises, subjective interpretations, outdated information — and 20 frontier LLMs, and reports that
abstention is broadly poor, with reasoning-tuned models *worse* at abstaining than their base
counterparts, i.e. the training that improves answers degrades the decision to decline. The survey
[61] organises the space by query, model, and human values, and flags as open whether abstention can
be a meta-capability that transfers across domains rather than a per-task threshold.

That last point is the deepest open question, and it is the one a student's own failed gate speaks to
directly: a gate that refuses questions the corpus can answer has not learned a capability, it has a
badly placed threshold on a feature whose range was never checked. (Anecdote, not evidence — the
student's private evaluation is not quoted here.)

**Landmark papers.** [56] established P(True) self-evaluation and format-dependent calibration.
[57] introduced semantic entropy, an unsupervised single-model uncertainty measure over meaning
clusters. [58] showed RLHF degrades probability calibration and that verbalized confidence is
competitive. [59] SelfCheckGPT established zero-resource hallucination detection by sampling
consistency. [60] AbstentionBench evaluated abstention across 20 datasets and 20 LLMs and found
reasoning models worse at it. [61] surveyed abstention by query, model and human values and named
meta-abstention as open.

**Open problems a small lab could attack.** (i) *Threshold transfer*: does an abstention threshold
calibrated on one model/dataset transfer to another model, or another domain? If it does not — and
the student's own apparatus suggests it does not — that is a clean, useful negative result with a
prescription ("recalibrate per model, and here is the cheapest way"). (ii) *Feature-range diagnostics*:
a gate is only meaningful if the triggering feature's observed range overlaps the threshold; a paper
that formalises this check and applies it to published gates would be small and sharp. (iii)
*Abstention vs refusal*: "I don't know" and "I won't answer" are different behaviours and most
benchmarks conflate them; separating them changes measured precision. (iv) *Abstention for RAG*: when
the retrieved context lacks the answer, does a 3B reader abstain, over-answer, or hallucinate — and
does a two-stage gate (retrieval confidence, then answer confidence) beat a single threshold? All
CPU-feasible in minutes.

**Entry difficulty: 1/5.** Sampling 20–50 completions from a 1–3B model and computing AUROC,
ECE, and selective-prediction curves is pure CPU arithmetic; there is no training and no sandbox.

**Status: maturing, but measurement-open — the best fit for this lab's assets.** The conceptual
claims are established; the transfer, threshold, and cross-lingual questions are not.

---

## 12. Human-AI interaction and LLM-as-judge

**What the field is actually arguing about.** Whether a model can stand in for a human rater — and,
if it can on average, whether that is good enough.

The founding result is the tempting one: Zheng et al. [62] showed strong LLM judges agree with human
preferences at roughly the level humans agree with each other (about 80% on their controlled and
crowdsourced comparisons), and simultaneously named the failure modes — position bias, verbosity
bias, self-enhancement bias, limited reasoning. Chatbot Arena [63] turned pairwise human preference
into a continuously running, statistically managed leaderboard with hundreds of thousands of votes,
which is why the community has a shared ranking at all. G-Eval [65] showed that a judge with
chain-of-thought and a form-filling template correlates better with human judgement than earlier
neural metrics, and Prometheus 2 [64] made the judge itself open and steerable by custom criteria, so
that evaluation does not require renting a proprietary model.

The counter-evidence is blunt. Wang et al. [66] showed that swapping the order of two candidate
responses flips verdicts enough that Vicuna-13B beat ChatGPT on 66 of 80 queries under ChatGPT as
judge, and proposed calibration strategies to reduce it. The Leaderboard Illusion [16, area 3] showed
the human-preference platform itself is distorted by private testing. And PRISM [67] attacks the
"human" in human preference: 1,500 participants from 75 countries, 8,011 conversations with 21
models, census-representative samples for the UK and US, with individualised ratings — showing that
preferences are systematically heterogeneous by demographics and culture, so a single aggregate
preference score is an average over people who disagree.

The unresolved argument: **is judge bias a fixable calibration problem or a reason not to trust
judge-based evaluation at all?** [62, 65, 64] say fixable; [66, 67] say the construct is unstable.

**Landmark papers.** [62] MT-Bench established LLM-as-judge agreement near human-human level and
catalogued its biases. [63] Chatbot Arena operationalised crowdsourced pairwise preference at scale
with statistical ranking. [64] Prometheus 2 produced an open, criteria-steerable evaluator supporting
both direct assessment and pairwise ranking. [65] G-Eval showed CoT plus form-filling improves
correlation with human judgement. [66] showed position bias is large enough to invert model rankings
and proposed calibration. [67] PRISM showed preferences vary systematically by demography and
culture across 1,500 participants in 75 countries.

**Open problems a small lab could attack.** (i) *Small judge reliability*: how much does a 3B judge
degrade versus a frontier judge on the same 300 items, and is the degradation bias or noise? Cheap,
and decision-relevant for anyone who cannot pay for GPT-4 judging. (ii) *Bias correction without a
strong judge*: order-swap averaging is the standard fix; does it work when the judge is small and
weak, or does averaging two biased verdicts yield a confidently wrong one? (iii) *Cultural
disagreement in judging*: PRISM is a Western-census dataset; a small Indian-respondent study of
preference disagreement on the same outputs would be genuinely novel and is survey-sized, not
cluster-sized. (iv) *Judge-free scoring*: rule-based or state-based scorers validated against a
small human sample — the practical route for agent evaluation (area 3).

**Entry difficulty: 2/5.** A 3B judge over a few hundred pairs is an hour on CPU; the constraint is
human annotation time if you collect your own preferences, not compute.

**Status: saturated on "judges agree with humans"; open on bias correction at small scale and on
whose preferences are being measured.**

---

## 13. Synthesis

### 13.1 The twelve areas at a glance

Heat = publication and citation pressure in 2025–2026 (5 = everyone is publishing here).
CPU-feasibility = can a real experiment be run on this laptop (5 = yes, today, in minutes; 1 = needs
a cluster). Student-edge = does this lab already have apparatus, data access, or a measured result
that gives an unfair advantage (5 = yes, directly).

| # | Area | Heat | CPU-feasibility | Student-edge |
|---|------|:----:|:---------------:|:------------:|
| 1 | LLM agents and tool use | 5 | 3 | 2 |
| 2 | RAG and agent memory | 4 | 4 | 4 |
| 3 | Evaluation methodology / agent benchmarks | 3 | 5 | 3 |
| 4 | Reasoning and test-time compute | 5 | 2 | 1 |
| 5 | Small / efficient models, on-device | 4 | 5 | 3 |
| 6 | Safety, robustness, adversarial behaviour | 4 | 3 | 1 |
| 7 | Multilingual / Indic / low-resource | 3 | 4 | 3 |
| 8 | Scam, fraud and misinformation detection | 3 | 5 | 5 |
| 9 | Code generation and SWE agents | 5 | 2 | 2 |
| 10 | Data-centric AI and synthetic data | 4 | 1 | 1 |
| 11 | Uncertainty, calibration, abstention | 4 | 5 | 5 |
| 12 | Human-AI interaction / LLM-as-judge | 4 | 4 | 2 |

The pattern is the point of the table: **heat and feasibility are almost inversely correlated.**
The two hottest areas (4 and 9) are the two least runnable here; the two most runnable (8 and 11)
are mid-heat. A student who picks by heat will produce a literature review and no result.

### 13.2 Ranked shortlist — the four areas where a defensible contribution is actually reachable

**1. Uncertainty, calibration and abstention (area 11).** Ranked first because the student already
owns an instrument and a failure mode: an abstention gate, built on this class of hardware, that
over-refused because a single threshold sat outside the range of scores the system actually produced.
That is an anecdote from a private evaluation — no number from it is quotable and none is used — but the
defect is of exactly the kind AbstentionBench [60] reports at frontier scale, and the apparatus to study
it is sampling plus
arithmetic. The paper writes itself in the honest form: "we reproduce a known abstention failure at
1–3B scale, show that the threshold does not transfer across models or domains, and evaluate a
two-stage gate". Every experiment is CPU-minutes; every metric (AUROC, ECE, selective risk/coverage)
is standard; the negative result is publishable and the student can defend every number because he
produced it.

**2. Scam and fraud detection under realistic conditions (area 8).** Ranked second because the
student has a working detector that reached a national student final, domain intuition about Indian
scam messages, and the cheapest possible experimental substrate (text classification). The
contribution is not another classifier: it is one of the three measurement gaps — realistic base
rates (precision at sub-1% prevalence), paraphrase/adversarial robustness, or a code-mixed Indic
scam set. Fraud-R1 [40] establishes that multi-round, role-play conditions break models; the
searches behind this map returned no verified Indian code-mixed fraud benchmark of comparable kind,
which is a gap rather than a proof of absence. Risk: the "just a classifier" trap, and label
collection is manual work.

**3. Evaluation methodology for small models (area 3).** Ranked third on feasibility — it is pure
inference and closed-form statistics — and on the field's own admitted gap: BetterBench [14] found
most benchmarks report no significance testing, and [15] supplies the formulas almost nobody applies
at small scale. A variance decomposition (seed × prompt-format × item) for two or three 1–3B models
is a real, citable, cheap paper. Ranked below 1 and 2 only because it requires no domain edge, so the
student competes on care rather than on access — and because "your numbers are noisy" invites the
reviewer question "so what should we do instead?", which needs a concrete prescription to survive.

**4. RAG and memory measurement (area 2).** Ranked fourth because the apparatus is trivial
(embeddings, a 3B reader, a numpy index) and the questions are clean: memory decay across sessions,
retrieval-versus-reader attribution via an oracle-passage upper bound, abstention when the index
lacks the answer. LongMemEval [12] gives a template and a ~30% cross-session drop to replicate or
contradict at small scale. Ranked last of the four because the area is crowded — the risk is not
failure, it is being ignored.

### 13.3 What I would veto, and why

- **Code generation and SWE agents (area 9) — veto.** Saturated at the frontier and compute-bound
  here. Running SWE-bench needs a strong code model (API, dev-time budget) and long sandboxed runs;
  the open questions are being worked by labs with clusters. A student entering now produces a
  weaker version of a 2024 result.
- **Data-centric AI and synthetic data (area 10) — veto.** Any causal claim needs fine-tuning. A 1B
  model for one epoch on CPU is days, which rules out the multi-run, multi-seed design that would
  make the result credible. Evaluation-only corners exist but are thin and already crowded.
- **Reasoning and test-time compute (area 4) — veto as a training topic.** The area's claims are RL
  claims; a CPU lab can only measure, and measurement here is slow (long traces) and needs released
  checkpoints whose provenance you do not control. Keep it as a *secondary* lens for area 11, not as
  the paper.
- **LLM agents / multi-agent orchestration (area 1) — veto as a systems contribution.** Building
  another orchestration framework is the definition of saturated, and evaluating one honestly needs
  many API calls across many seeds, which the budget does not support.
- **Safety red-teaming with gradient attacks (area 6) — veto the gradient half.** GCG-style attacks
  need gradients and GPU-hours; only the black-box half is feasible, and that half is crowded.
- **Multilingual benchmark construction (area 7, the benchmark-building half) — veto.** Building a
  new Indic benchmark at credible scale needs annotators and money; the measurement half of area 7
  survives and is folded into the shortlist as a possible extension of area 2 or 11.

### 13.4 The one-line summary for a decision

If the goal is a paper that exists in eight weeks and can be defended line by line, take
**abstention/calibration on a small local model with RAG**, and treat the student's over-refusing gate as
the motivating case study rather than as a failure to conceal (anecdote, no figures). Second choice:
**scam detection under
realistic base rates and paraphrase attack**. Both are CPU-only, both have verified literature to
stand on, and neither requires beating a frontier lab at its own game.

---

## 14. References

All entries verified through `02_literature/tools/verify_citations.py`; metadata (authors, year,
venue, identifier) is copied from `02_literature/staging/S2-1-verified.csv`. Venue strings are
reported as the resolver returned them — `arXiv preprint` where the arXiv record carries no journal
reference. Retrieval date for all rows: 2026-11-03.

1. Shunyu Yao et al. *ReAct: Synergizing Reasoning and Acting in Language Models*. 2022. arXiv preprint. `arXiv:2210.03629`.
2. Timo Schick et al. *Toolformer: Language Models Can Teach Themselves to Use Tools*. 2023. arXiv preprint. `arXiv:2302.04761`.
3. Shuyan Zhou et al. *WebArena: A Realistic Web Environment for Building Autonomous Agents*. 2023. arXiv preprint. `arXiv:2307.13854`.
4. Xiao Liu et al. *AgentBench: Evaluating LLMs as Agents*. 2023. arXiv preprint. `arXiv:2308.03688`.
5. Shunyu Yao et al. *$τ$-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains*. 2024. arXiv preprint. `arXiv:2406.12045`.
6. Mert Cemri et al. *Why Do Multi-Agent LLM Systems Fail?*. 2025. arXiv preprint. `arXiv:2503.13657`.
7. Patrick Lewis et al. *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. 2020. arXiv preprint. `arXiv:2005.11401`.
8. Nelson F. Liu et al. *Lost in the Middle: How Language Models Use Long Contexts*. 2023. arXiv preprint. `arXiv:2307.03172`.
9. Akari Asai et al. *Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection*. 2023. arXiv preprint. `arXiv:2310.11511`.
10. Darren Edge et al. *From Local to Global: A Graph RAG Approach to Query-Focused Summarization*. 2024. arXiv preprint. `arXiv:2404.16130`.
11. Charles Packer et al. *MemGPT: Towards LLMs as Operating Systems*. 2023. arXiv preprint. `arXiv:2310.08560`.
12. Di Wu et al. *LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory*. 2024. arXiv preprint. `arXiv:2410.10813`.
13. Yubo Wang et al. *MMLU-Pro: A More Robust and Challenging Multi-Task Language Understanding Benchmark*. 2024. arXiv preprint. `arXiv:2406.01574`.
14. Anka Reuel et al. *BetterBench: Assessing AI Benchmarks, Uncovering Issues, and Establishing Best Practices*. 2024. arXiv preprint. `arXiv:2411.12990`.
15. Evan Miller et al. *Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations*. 2024. arXiv preprint. `arXiv:2411.00640`.
16. Shivalika Singh et al. *The Leaderboard Illusion*. 2025. arXiv preprint. `arXiv:2504.20879`.
17. Chunyuan Deng et al. *Investigating Data Contamination in Modern Benchmarks for Large Language Models*. 2023. arXiv preprint. `arXiv:2311.09783`.
18. Charlie Snell et al. *Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters*. 2024. arXiv preprint. `arXiv:2408.03314`.
19. Jie Huang et al. *Large Language Models Cannot Self-Correct Reasoning Yet*. 2023. arXiv preprint. `arXiv:2310.01798`.
20. Niklas Muennighoff et al. *s1: Simple test-time scaling*. 2025. arXiv preprint. `arXiv:2501.19393`.
21. Daya Guo et al. *DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning*. 2025. Nature. `10.1038/s41586-025-09422-z`.
22. Parshin Shojaee et al. *The Illusion of Thinking: Understanding the Strengths and Limitations of Reasoning Models via the Lens of Problem Complexity*. 2025. arXiv preprint. `arXiv:2506.06941`.
23. Zayne Sprague et al. *To CoT or not to CoT? Chain-of-thought helps mainly on math and symbolic reasoning*. 2024. arXiv preprint. `arXiv:2409.12183`.
24. Marah Abdin et al. *Phi-3 Technical Report: A Highly Capable Language Model Locally on Your Phone*. 2024. arXiv preprint. `arXiv:2404.14219`.
25. Qwen et al. *Qwen2.5 Technical Report*. 2024. arXiv preprint. `arXiv:2412.15115`.
26. Loubna Ben Allal et al. *SmolLM2: When Smol Goes Big -- Data-Centric Training of a Small Language Model*. 2025. arXiv preprint. `arXiv:2502.02737`.
27. Zechun Liu et al. *MobileLLM: Optimizing Sub-billion Parameter Language Models for On-Device Use Cases*. 2024. arXiv preprint. `arXiv:2402.14905`.
28. Ji Lin et al. *AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration*. 2023. arXiv preprint. `arXiv:2306.00978`.
29. Andy Zou et al. *Universal and Transferable Adversarial Attacks on Aligned Language Models*. 2023. arXiv preprint. `arXiv:2307.15043`.
30. Kai Greshake et al. *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*. 2023. arXiv preprint. `arXiv:2302.12173`.
31. Qiusi Zhan et al. *InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents*. 2024. arXiv preprint. `arXiv:2403.02691`.
32. Edoardo Debenedetti et al. *AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents*. 2024. arXiv preprint. `arXiv:2406.13352`.
33. Eric Wallace et al. *The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions*. 2024. arXiv preprint. `arXiv:2404.13208`.
34. Andy Arditi et al. *Refusal in Language Models Is Mediated by a Single Direction*. 2024. arXiv preprint. `arXiv:2406.11717`.
35. Jay Gala et al. *IndicTrans2: Towards High-Quality and Accessible Machine Translation Models for all 22 Scheduled Indian Languages*. 2023. arXiv preprint. `arXiv:2305.16307`.
36. Sshubam Verma et al. *MILU: A Multi-task Indic Language Understanding Benchmark*. 2024. arXiv preprint. `arXiv:2411.02538`.
37. Wenxuan Zhang et al. *M3Exam: A Multilingual, Multimodal, Multilevel Benchmark for Examining Large Language Models*. 2023. arXiv preprint. `arXiv:2306.05179`.
38. Lucas Bandarkar et al. *The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122 Language Variants*. 2024. Proceedings of the conference - Association for Computational Linguistics. Meeting. `10.18653/v1/2024.acl-long.44`.
39. Angelika Romanou et al. *INCLUDE: Evaluating Multilingual Language Understanding with Regional Knowledge*. 2024. arXiv preprint. `arXiv:2411.19799`.
40. Shu Yang et al. *Fraud-R1 : A Multi-Round Benchmark for Assessing the Robustness of LLM Against Augmented Fraud and Phishing Inducements*. 2025. arXiv preprint. `arXiv:2502.12904`.
41. Tri Cao et al. *PhishAgent: A Robust Multimodal Agent for Phishing Webpage Detection*. 2024. arXiv preprint. `arXiv:2408.10738`.
42. Najmul Hasan et al. *Phishing Email Detection Using Large Language Models*. 2025. arXiv preprint. `arXiv:2512.10104`.
43. Canyu Chen et al. *Can LLM-Generated Misinformation Be Detected?*. 2023. arXiv preprint. `arXiv:2309.13788`.
44. Muhammad Salman et al. *An Empirical Analysis of SMS Scam Detection Systems*. 2022. arXiv preprint. `arXiv:2210.10451`.
45. Carlos E. Jimenez et al. *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?*. 2023. arXiv preprint. `arXiv:2310.06770`.
46. Mark Chen et al. *Evaluating Large Language Models Trained on Code*. 2021. arXiv preprint. `arXiv:2107.03374`.
47. Jiawei Liu et al. *Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation*. 2023. arXiv preprint. `arXiv:2305.01210`.
48. Chunqiu Steven Xia et al. *Agentless: Demystifying LLM-based Software Engineering Agents*. 2024. arXiv preprint. `arXiv:2407.01489`.
49. Alex Gu et al. *CRUXEval: A Benchmark for Code Reasoning, Understanding and Execution*. 2024. arXiv preprint. `arXiv:2401.03065`.
50. Naman Jain et al. *LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code*. 2024. arXiv preprint. `arXiv:2403.07974`.
51. Suriya Gunasekar et al. *Textbooks Are All You Need*. 2023. arXiv preprint. `arXiv:2306.11644`.
52. Chunting Zhou et al. *LIMA: Less Is More for Alignment*. 2023. arXiv preprint. `arXiv:2305.11206`.
53. Yizhong Wang et al. *Self-Instruct: Aligning Language Models with Self-Generated Instructions*. 2022. arXiv preprint. `arXiv:2212.10560`.
54. Zhangchen Xu et al. *Magpie: Alignment Data Synthesis from Scratch by Prompting Aligned LLMs with Nothing*. 2024. arXiv preprint. `arXiv:2406.08464`.
55. Ilia Shumailov et al. *The Curse of Recursion: Training on Generated Data Makes Models Forget*. 2023. arXiv preprint. `arXiv:2305.17493`.
56. Saurav Kadavath et al. *Language Models (Mostly) Know What They Know*. 2022. arXiv preprint. `arXiv:2207.05221`.
57. Lorenz Kuhn et al. *Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation*. 2023. arXiv preprint. `arXiv:2302.09664`.
58. Katherine Tian et al. *Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback*. 2023. arXiv preprint. `arXiv:2305.14975`.
59. Potsawee Manakul et al. *SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models*. 2023. arXiv preprint. `arXiv:2303.08896`.
60. Polina Kirichenko et al. *AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions*. 2025. arXiv preprint. `arXiv:2506.09038`.
61. Bingbing Wen et al. *Know Your Limits: A Survey of Abstention in Large Language Models*. 2024. arXiv preprint. `arXiv:2407.18418`.
62. Lianmin Zheng et al. *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*. 2023. arXiv preprint. `arXiv:2306.05685`.
63. Wei-Lin Chiang et al. *Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference*. 2024. arXiv preprint. `arXiv:2403.04132`.
64. Seungone Kim et al. *Prometheus 2: An Open Source Language Model Specialized in Evaluating Other Language Models*. 2024. arXiv preprint. `arXiv:2405.01535`.
65. Yang Liu et al. *G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment*. 2023. arXiv preprint. `arXiv:2303.16634`.
66. Peiyi Wang et al. *Large Language Models are not Fair Evaluators*. 2023. arXiv preprint. `arXiv:2305.17926`.
67. Hannah Rose Kirk et al. *The PRISM Alignment Dataset: What Participatory, Representative and Individualised Human Feedback Reveals About the Subjective and Multicultural Alignment of Large Language Models*. 2024. The Thirty-eight Conference on Neural Information Processing Systems Datasets and Benchmarks Track (2024). `arXiv:2404.16019`.
