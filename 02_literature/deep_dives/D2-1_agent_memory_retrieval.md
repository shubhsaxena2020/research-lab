# Agent memory and retrieval — deep dive (S2-2)

## 0. Scope and method

Four literatures that are usually kept apart and probably should not be: (i) agent memory systems,
meaning anything that decides what an agent stores, forgets, updates and retrieves across sessions;
(ii) the IR stack underneath them — lexical, dense, late-interaction and reranked retrieval, and the
fusion rules that combine them; (iii) the long-context-versus-retrieval argument, which is really an
argument about cost curves; (iv) the evaluation layer, where most of the field's claims live or die.

Search ran through the project's verification tool against OpenAlex and the arXiv API, Crossref as
DOI fallback: forty-six claims submitted, forty-five resolved into
`02_literature/staging/S2-2-verified.csv`, thirty-seven cited here. Queries covered each named
system ("MemGPT", "Mem0", "A-MEM", "Zep", "HippoRAG", "GraphRAG", "LightRAG", "RAPTOR"), each
benchmark ("LongMemEval", "LoCoMo", "MemBench", "MultiHop-RAG"), each retrieval method ("ColBERT",
"BEIR", "MTEB", "reciprocal rank fusion", "passage re-ranking with BERT") and the adversarial terms
("semantic chunking computational cost", "power of noise RAG", "abstention unanswerable questions").
About 120 candidate records were screened by title and abstract; all retained papers were read at
abstract level, and a dozen beyond it (intro, results tables, or the dataset's own repository).

Two classes of number appear below and they are labelled differently. Numbers attributed to a paper
are as the paper reports them. Numbers marked **measured here** come from scripts I ran on the
target laptop this session — Core Ultra 5 225H, 48 GB RAM, no CUDA, 14 logical cores — with scripts
and JSON left in `02_literature/staging/_s2_2_data/`. Where a paper does not report something the
field needs (usually cost, variance, or a random baseline) I say so rather than estimate it. Nothing
was accepted on a fuzzy title match: no claim produced a MISMATCH, and records that failed on rate
limits were re-submitted, never repaired.

## 1. Taxonomy

### 1.1 Tiered context management ("memory as virtual memory")

The founding idea is that the context window is RAM and the store is disk, so a controller pages
blocks in and out and interrupts itself when it needs something [1]. MemGPT is the canonical
instance: main context, external context, function calls between them. MemoryBank adds an
Ebbinghaus-style forgetting curve and a user-model summary [2]; MemOS generalises it into a memory
operating system — short-, mid- and long-term stores with FIFO and paged updates — reporting +49.1%
F1 over baselines on LoCoMo with GPT-4o-mini [3]. The survey literature groups these as hierarchical
memory, alongside parametric and episodic variants [4].

What improved, and over what. MemGPT's headline is 93.4% on Deep Memory Retrieval against 35.3% for
recursive summarisation [1, as reproduced in 7]. That is a 58-point gap — but the baseline is a
summariser that discards information every turn, not a full-context reader. Running the same 500 DMR
conversations with the entire history in the prompt gives 94.4% with the same model, i.e. the memory
system loses to doing nothing [7]. This is the most instructive number in the memory literature and
it sits in a competitor's related-work section.

### 1.2 Extraction-and-consolidation stores

The second cluster abandons paging and rewrites the transcript into atomic facts: an LLM extracts
candidate memories, compares each against its nearest neighbours, then chooses ADD / UPDATE / DELETE
/ NOOP [5]; or builds Zettelkasten notes with generated keywords, tags and contexts, links them to
similar notes, and "evolves" neighbours when a new note arrives [6].

Mem0 reports, on LoCoMo with GPT-4o-mini as the memory engine, LLM-judge scores of 67.1 single-hop,
51.2 multi-hop, 72.9 open-domain, 55.5 temporal, against 63.8 / 42.9 / 62.3 / 21.7 for the OpenAI
memory baseline [5]. The abstract advertises "26% relative improvement over OpenAI"; the conclusion
reports 5%, 11% and 7% relative gains over the best per-category method [5]. Both are true; they are
different aggregations. A-MEM shows the fragility from the other side: with GPT-4o-mini it moves
multi-hop F1 from 9.64 to 10.61 — one point — while moving temporal from 2.01 to 21.39 [6]. When one
category moves twenty points and another moves one, the aggregate is decided by category weighting,
not quality.

### 1.3 Graph and hierarchy structures

GraphRAG builds an entity graph with an LLM, partitions it into Leiden communities, pre-generates
community summaries, and answers global questions by map-reduce over them; the claim is scoped to
query-focused summarisation over corpora "in the 1 million token range", judged on comprehensiveness
and diversity [8]. LightRAG keeps the graph and adds dual-level (low-level entity, high-level theme)
retrieval with an incremental update path, reporting efficiency gains [9]. RAPTOR recursively
embeds, clusters and summarises chunks into a tree so retrieval can hit a summary or a leaf,
reporting +20 absolute accuracy on QuALITY with GPT-4 [10]. HippoRAG runs a knowledge graph plus
Personalized PageRank, imitating hippocampal indexing, and reports up to 20% gains on multi-hop QA
while being 10–20× cheaper and 6–13× faster than iterative retrieval [11]. Zep/Graphiti is the
temporal variant: bi-temporal edges with validity intervals, LLM-driven edge invalidation when a new
fact contradicts an old one, community summaries for global queries [7].

The best-evidenced result here is not an accuracy number but Zep's cost table on LongMemEval-S: 115k
tokens and 31.3 s at 55.4% accuracy, versus 1.6k tokens and 3.2 s at 63.8% with GPT-4o-mini (60.2% →
71.2% with GPT-4o) [7]. A 70× context and 10× latency reduction with a real accuracy gain, in one
table. Nothing else in this set does that.

### 1.4 The retrieval substrate

Underneath sits ordinary IR. Dense dual-encoders beat Lucene-BM25 by 9–19 points of top-20 passage
accuracy on open-domain QA [12], and late interaction made multi-vector matching practical by
pre-computing document representations offline [13]; ColBERTv2 then cut late-interaction storage
6–10× via residual compression while keeping state-of-the-art quality in and out of domain [14].
BEIR then produced the result that generalises: across 18 datasets and more than 50 million
documents, BM25 is a robust zero-shot baseline, learned dense and sparse retrievers often
underperform it out of domain, and the systems that do beat it — cross-encoder reranking and late
interaction — do so "at high computational costs" [15]. MTEB extends the scepticism to embeddings: 8
task types, 58 datasets, 112 languages, 33 models, no single method dominating [16].

Two details are load-bearing later. The cross-encoder reranker [17] costs per candidate, not per
query. And fusion is not free: Bruch et al. show reciprocal rank fusion is sensitive to its k
parameter, and that a tuned convex combination of lexical and semantic scores beats RRF in and out
of domain from a small tuning set [18]. "BM25 + dense + RRF", the default in most agent memory
stacks, is an untested default rather than a result.

### 1.5 Retrieval control

Self-RAG trains the generator to emit reflection tokens and critique its own retrieval [19]; CRAG
puts a lightweight retrieval evaluator in front, triggering web search or discarding retrieved text
on low confidence [20]; In-Context RALM showed that simply prepending retrieved documents, with no
architecture change and no training, gives large LM gains across model sizes [21]. These are filed
under "agentic RAG", but the shared move is narrower and more useful: they put a *decision* in front
of retrieval. That decision point is where the abstention problem in §3.6 lives.

### 1.6 Evaluation

LongMemEval is the reference point: 500 hand-written questions over five abilities (extraction,
multi-session reasoning, temporal reasoning, knowledge update, abstention), embedded in histories of
~115k tokens (S) or 500 sessions / ~1.5M tokens (M), with turn- and session-level gold labels so
recall@k and nDCG@k can be scored separately from answer accuracy [22]. LoCoMo is the older
conversational benchmark: 50 very long dialogues of ~300 turns and 9k tokens over up to 35 sessions
[23], released as a 10-conversation subset. MemBench separates factual from reflective memory and
participation from observation, scoring effectiveness, efficiency and capacity [24];
MemoryAgentBench targets four competencies including selective forgetting [25]; MultiHop-RAG
supplies 2,556 multi-hop queries over 609 news documents [26]. On the metric side, RAGAS introduced
reference-free faithfulness, answer-relevance and context-precision metrics that need no gold
answers and are in practice computed by prompting an LLM judge [27] — now the field's default
scoring apparatus, and its default confound.

## 2. What is saturated

**"Graph + community summaries beats vector RAG."** At least five variants make this claim, each
with its own construction and LLM-judged comparison [7–11]. Another variant adds engineering, not
knowledge. None tests it where the baseline could plausibly fail for IR reasons: GraphRAG's evidence
is ~1M-token corpora scored for answer comprehensiveness, not retrieval metrics over millions of
documents.

**"Extract facts, then ADD/UPDATE/DELETE."** Mem0, A-MEM and MemoryBank share the pipeline and
differ in prompt and linking policy [2, 5, 6]. The interesting variable — when to delete — is
delegated to an LLM call whose reliability nobody measures.

**"Hybrid retrieval with RRF."** Universal, contradicted by the one careful study [18], and in my
own measurement worse than BM25 alone (§5). Adding RRF is not a contribution.

**"Long context makes retrieval unnecessary."** Refuted three ways: positional degradation inside
the window [28], effective context far below claimed context [29], and a 30–60% drop when a model
reads a 115k-token history instead of the evidence sessions [22]. A fourth demonstration adds
nothing; the open question is the crossover curve. LOFT sharpens it: long-context models can rival
retrieval and RAG on in-context retrieval tasks over corpora of up to millions of tokens, but still
fail compositional, SQL-like ones [36], which turns "can it replace retrieval" into "at what price,
on which task".

**"Semantic chunking improves retrieval."** The one systematic test finds the cost unjustified by
consistent gains across document retrieval, evidence retrieval and answer generation [30].

## 3. What is genuinely open

### 3.1 Most memory benchmarks are too small for recall@k to mean anything

This is arithmetic, and it is the strongest criticism available. LoCoMo as released contains ten
conversations, 272 sessions, 5,882 turns and 1,986 questions (**measured here** by parsing
`locomo10.json`). Because retrieval is per conversation, the corpus for any query is one
conversation: about 588 turns, or 27 sessions. Recall@5 at turn granularity is therefore a hit rate
over 0.85% of the corpus; at session granularity, k=5 is 18.5% of the corpus. At that ratio a
retriever returning a fifth of the sessions scores well whenever the question is topically close,
and the number cannot distinguish that from skill.

The same arithmetic travels. DMR conversations are five sessions of up to twelve messages — 60
messages total, which is why full context beats the memory system [7]. LongMemEval-S is ~40–50
sessions, so session-level k=5 covers ~10–12% of the corpus. Compare BEIR, where corpora reach 50
million documents and nDCG@10 over a 5,000-document subset still means something [15]. Single-vector
retrieval also has a provable ceiling — the number of distinct top-k result sets one embedding can
express is bounded by its dimension, and state-of-the-art embedders fail a simple dataset built on
that bound [37] — which is a second reason lexical baselines are not merely cheap fallbacks.

The fix is cheap and rare: report k/N beside recall@k, and report the random-retrieval floor k/N. My
measurement shows why — BM25 reaches recall@5 = 0.459 on LoCoMo, which sounds respectable until the
floor is noted at 0.0085; on a 27-session corpus the same score would face a floor of 0.185.

### 3.2 Retrieval "gains" that are judge artefacts or unmeasured cost

Three mechanisms. First, absolute scores are LLM-generated: Mem0's headline metric is
"LLM-as-a-Judge" [5]; Zep scores DMR and LongMemEval with GPT-4o using LongMemEval's prompts [7];
GraphRAG's core claims are GPT-4 head-to-head win rates on comprehensiveness and diversity, with no
IR metric in the paper [8]. When the judge is the same family that generated the memory —
GPT-4o-mini builds Mem0's memory, GPT-4o judges it — self-preference is uncontrolled.

Second, effect sizes sit inside the noise. Zep's DMR win is 94.8% versus 94.4% for full context: 0.4
points on 500 questions, about two questions, no confidence interval anywhere [7]. Third, comparison
sets are written by competitors: Mem0 benchmarks Zep, LangMem and OpenAI memory; Zep benchmarks
MemGPT, and states it could not get MemGPT to answer LongMemEval questions at all [7]. Not fraud,
but not independent replication.

Retrieval score is also not answer utility: adding random documents to a RAG prompt raised LLM
accuracy by up to 35%, while the retriever's highest-scoring *irrelevant* documents actively hurt
[32]. Retrieval and answer improvements can move in opposite directions, so a paper reporting only
the second has not shown the first.

Reranker cost is the specific unmeasured term. BEIR notes late interaction and reranking win at high
cost [15]; no memory paper I read separates rerank latency from end-to-end latency. **Measured
here**: reranking 50 candidates with a 22.7M-parameter cross-encoder costs 361 ms per query; a
33.4M-parameter model at length 256 costs 13.4 ms per pair. Across 1,982 LoCoMo queries that is 12
minutes of pure reranking for one configuration — and in my run it still lost to plain BM25.

### 3.3 Memory scores that are really answerer scores

The clean demonstration is inside LongMemEval: with oracle retrieval (only evidence sessions in
context) GPT-4o reaches 0.870; with the full 115k-token history, 0.606 [22]. That 26-point gap is a
*reading* failure, not a retrieval failure. Symmetrically, adding Chain-of-Note at fixed retrieval
buys up to 10 absolute points [22]. A paper that improves a memory store and reports +8 accuracy has
not shown that memory improved; it has shown the reader answered better from a different context.

Almost no memory paper reports retrieval quality. LongMemEval is the exception and should be the
template: recall@k and nDCG@k from the system's own retrieval log, separately from QA accuracy [22].
Where only a judge score is reported, the memory contribution is whatever survives after the reader,
prompt and judge are fixed — and they are usually not fixed. The agent-benchmark critique makes the
point at system level: accuracy without cost, holdouts absent, so gains cannot be attributed to the
component a paper names [34].

### 3.4 What memory costs, and who says so

Cost reporting is bimodal. Zep reports tokens (115k → 1.6k), latency (31.3 s → 3.2 s) and latency
IQR [7]; Mem0 reports 91% lower p95 latency and >90% token savings against full context [5]. Neither
reports RAM, index size, or the LLM calls spent *ingesting* a conversation — for a graph system the
dominant cost, since every message triggers entity extraction, edge extraction and deduplication,
and every community refresh triggers summarisation [8, 9]. GraphRAG's indexing pass is the clearest
example of a large cost reported only as a scope statement ("1 million token range").

**Measured here** (full table in §5): indexing 5,882 turns with BM25 takes 0.11 s in 406 MB;
encoding them with a 22.7M-parameter MiniLM takes 20.2 s in 600 MB; 33.4M-parameter embedders take
43–45 s in 635–847 MB. Embeddings are 1,536 bytes per turn — 9 MB for this whole benchmark. Memory
is not the bottleneck at this scale, which is exactly why "our memory fits in X GB" is untestable
here.

### 3.5 Contradiction and staleness: one mechanism, almost no measurement

Only one system here has an explicit supersede mechanism with a temporal model. Graphiti/Zep stores
four timestamps per edge — created/expired in transaction time, valid/invalid in event time —
compares a new edge against semantically related existing edges with an LLM, and on a temporally
overlapping contradiction sets the old edge's invalidation time to the new edge's valid time,
prioritising new information [7]. Mem0 reaches something similar with DELETE/UPDATE chosen by an LLM
against the top-10 similar memories, but keeps no validity interval and no audit trail [5]. A-MEM's
"memory evolution" rewrites neighbours' contexts and attributes but describes no delete operation,
so a superseded fact can persist as a live note [6]. The knowledge-conflict literature names the
general taxonomy — context–memory, inter–context and intra–memory conflict — without supplying a
store-level metric for any of the three [35].

Measurement is much weaker than mechanism. LongMemEval has a knowledge-update category; the only
number I can find for it is 78.2% (full context) versus 83.3% (Zep) with GPT-4o [7] — five points on
a fraction of 500 questions, LLM-judged, with no breakdown of why a system failed. The category is
also confounded by construction: evidence sessions are inserted in timestamp order, so a reader that
prefers the latest session answers many update questions correctly with no update logic at all.

What nobody reports is the operational question: after a fact is superseded, does the system still
*retrieve* it? A stale-hit rate — fraction of top-k results containing a superseded value — is
computable from any store with versioned facts, needs no LLM judge, and separates systems that
update from systems that merely append. I could not find a paper reporting it.

### 3.6 Abstention inside memory versus refusal by the answerer

LongMemEval includes 30 false-premise questions (6% of the benchmark) that ask for information never
mentioned, scored as correct only if the system declines [22]. AbstentionBench shows the general
problem is unsolved at the model level: across 20 datasets and 20 frontier models, reasoning
fine-tuning *degrades* abstention by 24% on average, and a well-crafted system prompt helps without
fixing the underlying inability to reason about uncertainty [31].

Both are answerer-side, and neither distinguishes the two failure modes a memory system actually
has: **memory miss** (nothing relevant retrieved) and **memory wrong** (something retrieved that
contradicts the question). Both justify refusal, and they need opposite repairs — one fixes the
index, the other fixes the reader — yet they are scored identically. In the student's prior system
the gate lived in the answerer prompt and refused 47 of 82 answerable questions at precision 0.30,
because the threshold sat outside the observed range of the score feature: the decision was made
where the evidence was not. RAG experience reports reach the same conclusion — validation is only
feasible during operation, and robustness evolves rather than being designed in [33].

## 4. Benchmarks and datasets that a CPU laptop can actually use

Licences read from each dataset's own repository or card this session, not from memory. "Run"
assumes this laptop.

| Name | What it measures | Size (questions / corpus) | Licence | Download + run cost here | Known gotchas |
|---|---|---|---|---|---|
| LongMemEval-S [22] | five memory abilities incl. knowledge update and abstention; turn- and session-level recall | 500 questions; ~115k tokens (~40–50 sessions) per question | MIT (repo) | HF download, no auth; retrieval scoring CPU-cheap; **answering needs an LLM** | scored by GPT-4o via API (>97% human agreement claimed); no local judge shipped; abstention is only 30 questions |
| LongMemEval-M [22] | the same at scale | 500 questions; ~500 sessions / ~1.5M tokens each | MIT | data large; 1.5M tokens/question is hours of CPU retrieval | effectively an API-LLM benchmark; context fits no small local model |
| LoCoMo [23] | long-term conversational QA: single-hop, multi-hop, temporal, open-domain, adversarial | 10 conversations, 5,882 turns, 1,986 QA (**measured**); paper version 50 conv / 7,512 QA | CC BY-NC 4.0 | 2.8 MB single JSON; retrieval in seconds | non-commercial only; released subset is 10 of 50 conversations, so cross-paper numbers are not comparable; 22% of questions are adversarial, which inflates apparent refusal |
| DMR (inside MemGPT) [1] | single-session fact recall across 5 sessions | 500 conversations × 60 messages | licence not checked here | trivial | corpus fits any 8k context; full-context baseline beats the memory system [7]; questions reference attributes never explicitly stated |
| MemBench [24] | factual vs reflective memory; participation vs observation; effectiveness, efficiency, capacity | four settings; the repo's sample files hold 100 dialogues per setting per length (10k / 100k) | MIT (repo) | data hosted on Baidu Pan + Google Drive, not HF — manual download | no scripted download; noise generator adds ~1k tokens per unit so "100k" is approximate; Chinese-language tooling |
| MemoryAgentBench [25] | accurate retrieval, test-time learning, long-range understanding, selective forgetting | multi-turn conversions of long-context datasets; size follows the source sets | check repo before use | moderate; retrieval-only scoring feasible | inherits contamination from the converted datasets |
| MultiHop-RAG [26] | multi-hop retrieval across 2–4 documents with metadata | 2,556 queries; 609-document news corpus | ODC-BY | small HF dataset; BM25 baseline under a minute | tiny corpus, so recall@k is high-variance; paper's answer scoring uses an LLM |
| BEIR [15] | zero-shot retrieval over 18 heterogeneous datasets | 18 datasets; >50M documents total; per-dataset subsets from ~3.6k docs | per-dataset; code Apache-2.0 | per-dataset subsets are megabytes and run in minutes | full BM25 over 50M docs needs an index server, not a laptop; licences differ per dataset |
| MTEB retrieval subset [16] | embedding quality across 8 task types | 58 datasets, 112 languages | Apache-2.0 (code) | `pip install mteb`; minutes per retrieval task | full MTEB is not a laptop job; leaderboard numbers are not comparable across prompt settings |
| RULER [29] | synthetic long-context tasks beyond needle-in-haystack | 13 tasks, configurable 4k–128k; 17 models benchmarked | Apache-2.0 | generation CPU-cheap; **evaluating needs the model** | designed for long-context LLMs; meaningless for a 3B/8k model unless lengths are scaled down |
| AbstentionBench [31] | abstention across 20 datasets (unknown, underspecified, false premise, outdated) | 20 datasets, 20 frontier models | check repo | small; scoring mostly exact-match | measures the answerer, not the retriever; only the outdated-information subset is memory-relevant |

Two flags. **No benchmark here needs a GPU to score**, but most answer-scoring paths need an LLM,
and three explicitly use a paid API judge (LongMemEval, MultiHop-RAG as run in its paper, anything
GraphRAG-style scoring comprehensiveness). For a zero-budget student the rule is: retrieval-side
metrics (recall@k, nDCG@k, stale-hit rate) are primary; LLM-judge accuracy is a secondary check on a
fixed 200-question sample. Second, the LoCoMo version problem is real: LongMemEval's own comparison
table lists LoCoMo at 7,512 questions, the released file has 1,986, and Mem0 evaluated the
10-conversation release [5, 22, 23]. Cross-paper LoCoMo comparisons are not comparisons.

## 5. Baselines runnable on this hardware

All rows were run on the target laptop this session, CPU only, `sentence-transformers` on PyTorch
CPU wheels plus `bm25s`; scripts and JSON in `02_literature/staging/_s2_2_data/`. Recall is
turn-level against LoCoMo's gold dialogue ids over 1,982 answerable questions, retrieval restricted
to the query's own conversation.

| Method | Params | Build (5,882 turns) | Query | RSS | recall@5 | recall@10 |
|---|---|---|---|---|---|---|
| BM25 (`bm25s`) | 0 | 0.11 s | 0.04 ms | 406 MB | **0.459** | **0.544** |
| Dense, all-MiniLM-L6-v2 (384d) | 22.7 M | 20.2 s (292 turns/s) | 10.0 ms (p95 19.1) | 600 MB | 0.259 | 0.346 |
| Dense, bge-small-en-v1.5 (384d) | 33.4 M | 43.1 s (136 turns/s) | 31.6 ms (p95 92.0) | 847 MB | 0.389 | 0.492 |
| Dense, e5-small-v2 (384d) | 33.4 M | ≈42 s, extrapolated (142 turns/s) | ≈30 ms | 635 MB | not run | not run |
| Dense, gte-small (384d) | 33.4 M | ≈45 s, extrapolated (131 turns/s) | ≈30 ms | 773 MB | not run | not run |
| RRF fusion (BM25 + MiniLM) | 0 | — | ≈11 ms | — | 0.382 | 0.485 |
| + cross-encoder rerank of top-50 | 22.7 M | — | **361 ms** | — | 0.335 (200 q) | — |

Three things follow, and they are the most useful empirical content here for our own work.

BM25 is not a straw man on conversational memory. It beats both dense models by 7 to 20 points of
recall@5 at under 1% of the query cost, because LoCoMo questions reuse the vocabulary of the
dialogue that answers them. A paper claiming dense beats BM25 on this benchmark must explain this;
the likely explanations are a tuned retriever, session rather than turn granularity, or a different
LoCoMo release.

Hybrid fusion is not a free win. RRF lands between BM25 and dense — it rescues dense and drags BM25
down — exactly the behaviour Bruch et al. predict: equal-weight rank fusion is optimal only when the
rankers are comparably good [18]. With one ranker much stronger, fusion needs weights tuned on
held-out queries.

The reranker buys quality only relative to the stage it fixes: cross-encoding the dense top-50
lifted MiniLM's recall@5 from 0.259 to 0.335 while staying 12 points below untouched BM25, at 361 ms
per query. A memory paper that adds a reranker and reports a gain has usually reported a gain over
its own weak first stage, and paid in latency it does not report.

For anything we build: `bm25s` (pure Python + NumPy, no JVM) is the lexical baseline; if a neural
component is needed, MiniLM-L6-v2 or bge-small-en-v1.5 are the only sensible sizes — 384 dimensions,
under 850 MB resident, a few thousand memories indexed in under a minute. A 278M-parameter reranker
is about 8× the compute measured above and puts query latency in the seconds; a 7B reranker is not a
baseline on this hardware. For judging, prefer model-free metrics (recall@k, stale-hit rate, refusal
precision/recall against labelled answerability); if an LLM judge is unavoidable, use the dev-time
API on a fixed 200-question sample with prompt and model version pinned.

## 6. Five candidate gaps

**G1. Stale-hit rate as a first-class memory metric.** Build 300 supersede pairs from LoCoMo — a
fact stated in session *i*, contradicted in session *j* — and measure two numbers per store: the
fraction of top-k results containing the superseded value, and the fraction of answers using it when
the question carries no date. Cheapest experiment: implement append-only, delete-on-write and
bi-temporal validity in one local store (SQLite plus a timestamp column), run all three on the same
pairs, report both numbers. Likely confound: the reader may prefer the later session by position
alone, so the stale-hit metric must be computed on the retrieved set before the reader sees it.

**G2. Retrieval-side abstention instead of prompt-side.** Replace a "say I don't know" instruction
with a gate on a retrieval feature — top-1 BM25 score, or the margin between rank 1 and rank k —
calibrated on a held-out split, and report a risk–coverage curve rather than one threshold. Cheapest
experiment: LoCoMo's 446 adversarial questions plus an equal number of answerable ones, sweeping the
threshold and plotting answered fraction against precision. Confound: LoCoMo's adversarial questions
were generated to be unanswerable given the conversation, so a lexical gate may detect them by
vocabulary mismatch rather than by absence of evidence; test on held-out answerable questions with
paraphrased wording or the gate will look better than it is.

**G3. Cost-normalised comparison at fixed RAM.** Report accuracy per 1k prompt tokens and per 100 ms
of query latency on one machine, with the store's resident set size measured. Cheapest experiment:
three configurations (full context, BM25 top-5, summary + BM25) on LongMemEval-S's 500 questions
with one fixed reader, measuring tokens, wall-clock and RSS. Confound: API latency includes the
provider's queueing, so local reader latency must be measured separately or the comparison becomes a
measurement of the network.

**G4. Are the reported gains inside the noise?** Bootstrap per-question results of two systems on
LoCoMo or LongMemEval (1,000 paired resamples) and report 95% intervals on the difference. My
prediction, from the effect sizes in §3.2, is that most single-digit-point gains on 500–2,000
questions will have intervals crossing zero. Cheapest experiment: re-run BM25 versus BM25+rerank and
report the interval width. Confound: paired bootstrap assumes exchangeable questions, which the
seven LongMemEval categories are not — stratify by category or the interval will be too narrow.

**G5. Fix the reader, vary the memory.** Hold the answerer constant (one small local model, one
prompt), vary only the memory store, and report retrieval metrics alongside accuracy. This is the
only design that identifies the memory contribution, and it is cheap: a 1.5–3B model at 8k context
on this laptop can answer 500 short questions in hours. Confound: a weak reader compresses every
system toward the same low accuracy (floor effect), making memory look irrelevant for the wrong
reason — so run the design twice, once locally and once through the dev-time API.

## 7. References

1. MemGPT: Towards LLMs as Operating Systems (2023). arXiv preprint — arXiv:2310.08560.
2. MemoryBank: Enhancing Large Language Models with Long-Term Memory (2023). arXiv preprint — arXiv:2305.10250.
3. Memory OS of AI Agent (2025). arXiv preprint — arXiv:2506.06326.
4. A Survey on the Memory Mechanism of Large Language Model based Agents (2024). arXiv preprint — arXiv:2404.13501.
5. Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory (2025). arXiv preprint — arXiv:2504.19413.
6. A-MEM: Agentic Memory for LLM Agents (2025). arXiv preprint; NeurIPS 2025 per the paper's comments — arXiv:2502.12110.
7. Zep: A Temporal Knowledge Graph Architecture for Agent Memory (2025). arXiv preprint — arXiv:2501.13956.
8. From Local to Global: A Graph RAG Approach to Query-Focused Summarization (2024). arXiv preprint — arXiv:2404.16130.
9. LightRAG: Simple and Fast Retrieval-Augmented Generation (2024). arXiv preprint — arXiv:2410.05779.
10. RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval (2024). arXiv preprint — arXiv:2401.18059.
11. HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models (2024). arXiv preprint — arXiv:2405.14831.
12. Dense Passage Retrieval for Open-Domain Question Answering (2020). arXiv preprint — arXiv:2004.04906.
13. ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT (2020). arXiv preprint — arXiv:2004.12832.
14. ColBERTv2: Effective and Efficient Retrieval via Lightweight Late Interaction (2021). arXiv preprint — arXiv:2112.01488.
15. BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models (2021). arXiv preprint — arXiv:2104.08663.
16. MTEB: Massive Text Embedding Benchmark (2022). arXiv preprint — arXiv:2210.07316.
17. Passage Re-ranking with BERT (2019). arXiv preprint — arXiv:1901.04085.
18. An Analysis of Fusion Functions for Hybrid Retrieval (2022). arXiv preprint — arXiv:2210.11934.
19. Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection (2023). arXiv preprint — arXiv:2310.11511.
20. Corrective Retrieval Augmented Generation (2024). arXiv preprint — arXiv:2401.15884.
21. In-Context Retrieval-Augmented Language Models (2023). arXiv preprint — arXiv:2302.00083.
22. LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory (2024). arXiv preprint — arXiv:2410.10813.
23. Evaluating Very Long-Term Conversational Memory of LLM Agents (2024). arXiv preprint — arXiv:2402.17753.
24. MemBench: Towards More Comprehensive Evaluation on the Memory of LLM-based Agents (2025). arXiv preprint — arXiv:2506.21605.
25. Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions (2025). arXiv preprint — arXiv:2507.05257.
26. MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries (2024). arXiv preprint — arXiv:2401.15391.
27. Ragas: Automated Evaluation of Retrieval Augmented Generation (2023). arXiv preprint — arXiv:2309.15217.
28. Lost in the Middle: How Language Models Use Long Contexts (2023). arXiv preprint — arXiv:2307.03172.
29. RULER: What's the Real Context Size of Your Long-Context Language Models? (2024). arXiv preprint — arXiv:2404.06654.
30. Is Semantic Chunking Worth the Computational Cost? (2024). arXiv preprint — arXiv:2410.13070.
31. AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions (2025). arXiv preprint — arXiv:2506.09038.
32. The Power of Noise: Redefining Retrieval for RAG Systems (2024). arXiv preprint — arXiv:2401.14887.
33. Seven Failure Points When Engineering a Retrieval Augmented Generation System (2024). arXiv preprint — arXiv:2401.05856.
34. AI Agents That Matter (2024). arXiv preprint — arXiv:2407.01502.
35. Knowledge Conflicts for LLMs: A Survey (2024). arXiv preprint — arXiv:2403.08319.
36. Can Long-Context Language Models Subsume Retrieval, RAG, SQL, and More? (2024). arXiv preprint — arXiv:2406.13121.
37. On the Theoretical Limitations of Embedding-Based Retrieval (2025). arXiv preprint — arXiv:2508.21038.
