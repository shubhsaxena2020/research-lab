# What Is a Research Paper?

> **READ THIS FIRST — 10 lines**
> 1. This page explains what a research paper actually is: its parts, its types, and what "contribution" and "novelty" mean.
> 2. The one thing to keep: a paper is one main claim plus enough evidence that a stranger can check it without emailing you.
> 3. Read it in your first week, before you read your first paper closely and before you write anything.
> 4. Skip on a first pass: §4 Types of paper and §8 A worked mini-example; both make more sense after one experiment.
> 5. A paper is usually 8 to 12 pages, and the venue sets the limit, not you (NeurIPS 2024 allowed 9 content pages).
> 6. The abstract is 150-250 words and must contain a number; "we explore X" is not an abstract.
> 7. Section budgets: method 1.5-2.5 pages, results 1.5-2.5 pages, references 30-60 entries.
> 8. Reproducibility decides value: Raff tried to reimplement 255 papers from 1984-2017 without the authors' code.
> 9. Date-sensitive: the per-venue page limits and cycle numbers (NeurIPS 2024, ACL and workshop limits); re-check the live call for papers.
> 10. Full read about 19 minutes (4,200 words); the skim path in item 4 about 15 minutes.

**What this page is for.** A research paper is the basic unit of scientific communication in computer science, and nobody explains what one actually is in first semester. This page covers the object, its parts, its types, what counts as a contribution, what "novelty" means, and why reproducibility decides whether your work is worth anything.

---

## 1. The object itself

A research paper is a short PDF, usually 8 to 12 pages, that makes **one main claim** about how something works and gives enough evidence that a stranger can check the claim without asking you anything.

Everything else — formatting, citations, section order — exists to make that check possible for someone who was not there.

Length is not yours to choose; venues set it. NeurIPS 2024 allowed **nine content pages**, with references and appendices outside the limit [1]. The ACL Rolling Review, which feeds the ACL family of NLP conferences, allows **eight pages of content for a long paper and four for a short paper** [2].

### Paper vs. report vs. blog vs. college project

| | Research paper | Lab report | Blog post | College project |
|---|---|---|---|---|
| **Who checks it** | 2-4 anonymous experts, before publication | one teacher, after | nobody | one examiner, after |
| **The claim** | one testable claim nobody knew before | reproduce a known result | any opinion, no evidence needed | demonstrate a skill |
| **Evidence** | experiments a stranger can rerun | the steps the teacher prescribed | links, screenshots | screenshots, a demo |
| **"Good" means** | the claim survives checking | the procedure was followed | people read it | the rubric was met |

A college project asks "can you build it?". A paper asks "is it true, and how would we know?". A project write-up usually fails as a paper for exactly that reason: it describes what was built, never what was learned.

---

## 2. What a paper is for

**It moves an idea from your head into a stranger's head.** A paper is not a record of what you did; it is a machine for making someone else understand something they did not. If a competent reader finishes and cannot state your claim in one sentence, the paper failed even if the experiments were perfect.

**It lets others build on it.** Science accumulates because papers are specific enough to reuse: this dataset, this baseline, this number. Vague papers get cited politely and forgotten.

**It fixes priority and credit.** Publication date is how a field decides who found a thing first, which is why double submission is treated as misconduct.

**It is the currency of admissions and hiring** — a social fact rather than a scientific one, covered in a separate page.

One hard constraint shapes everything: **most reviewers read your paper once, quickly**. Keshav, in the standard short guide to reading papers, notes that when you write a paper you should expect most reviewers to make only one pass over it, which is why the abstract and introduction must carry the whole argument [3]. Write for the tired reader at 1 a.m. with eleven other papers to review.

---

## 3. Anatomy, section by section

| Section | Rough length | Its one job | Classic beginner mistake |
|---|---|---|---|
| Title | 8-14 words | let the right reader decide to read | "A Study of Deep Learning Methods" |
| Authors + affiliations | 2-8 names | credit, and take responsibility | adding a teacher who did nothing |
| Abstract | 150-250 words | the whole paper in miniature | "we study X" with no result |
| Keywords | 3-6 terms | findability | synonyms nobody searches |
| Introduction | 1-1.5 pages | why this question, what you found | three pages of history |
| Related work | 0.5-1 page | what exists, how you differ | a list of citations, no comparison |
| Method | 1.5-2.5 pages | enough detail to reimplement | hiding the one trick that matters |
| Experiments / results | 1.5-2.5 pages | numbers, baselines, variance | one run, no baseline |
| Discussion | 0.5-1 page | what the numbers mean | repeating the numbers in prose |
| Limitations | 0.25-0.5 page | where it breaks | "our method has some limitations" |
| Conclusion | 0.2-0.5 page | what changed | claims not in the results |
| References | 30-60 entries | the conversation you joined | padding to look well-read |
| Appendix | no limit | proofs, extra tables | hiding a weak result there |

These lengths are convention, read off a few hundred CS papers. The only numbers a venue enforces are the page limits [1][2].

**Title.** Say what the paper does, specifically. A reader should guess your contribution from the title alone. "Attention Is All You Need" is memorable but unusual; most good titles name the task and the method.

**Authors and affiliations.** Order usually means amount of work, senior author last. Every author is responsible for the whole paper, which is why gift authorship is misconduct. Write your college's full official name and city — "PSIT College of Higher Education, Kanpur, India" — so the paper is indexed correctly.

**Abstract.** Four sentences: the problem, what you did, the main quantitative result, why it matters. It must contain a number. "We reach 84.2% accuracy, 3.1 points above the logistic-regression baseline" is an abstract. "We explore small-data classification" is a table of contents.

**Keywords.** Three to six terms a searcher would type, in the field's standard vocabulary. If your topic is "small-data classification", do not list only your own coinage, "data-scarce regimes".

**Introduction.** The hardest page and the one that decides your fate. Answer in order: what is the problem, why it matters, what others did, what is missing, what you contribute. End with three bullets, each a claim you can defend in the results. The beginner mistake is retelling the history of the field.

**Related work.** Not a bibliography. For each cluster of prior work, say what it did and how you differ, so the reader finishes knowing which gap you stand in. "Smith et al. did X. Jones et al. did Y." with no comparison is a list, not an argument.

**Method.** Enough detail to rebuild your system without emailing you: architecture, loss, hyperparameters, preprocessing, and why you chose them. Equations are fine if each is explained in words. The beginner mistake is omitting the one detail that makes it work, because by then it feels obvious.

**Experiments and results.** This is where a paper becomes checkable: datasets, baselines (the methods you compare against), metric, number of runs, variance, compute. One table readable without the text beats three paragraphs. The beginner mistake is a single run against no baseline, which proves nothing because you cannot separate signal from noise.

**Discussion.** Interpretation, not repetition. Why does the 2-layer model win only below 200 examples? What does that suggest about the bias-variance tradeoff? Speculation is allowed if labelled as speculation.

**Limitations.** Required at ACL venues — submissions missing it are desk rejected [2] — and encouraged at NeurIPS [4]. Say what your evaluation does not cover: one dataset, one language, one hardware setup. Naming a limitation costs nothing; a reviewer finding it for you costs the paper.

**Conclusion.** Half a page: what you showed, what it means, what comes next. No new results. A claim that appears only here reads as one you could not defend earlier.

**References.** Thirty to sixty entries for a workshop paper, more for a survey. Every entry must be real and actually read. Fabricated references are the fastest way to end a research career, and they are trivially detected.

**Appendix and supplementary material.** Proofs, extra tables, dataset documentation, code — unlimited pages at NeurIPS and explicitly outside the limit [1]. Two rules: the main claims must be checkable from the main text, and the appendix is not a dump for results you are embarrassed by.

---

## 4. Types of paper

| Type | The question it answers | Verified example |
|---|---|---|
| **Survey / review** | What is known here, and how does it fit together? | *A Survey of Large Language Models*, arXiv:2303.18223 [5] |
| **Empirical** | Does method A beat method B on task C, and by how much? | *Attention Is All You Need*, arXiv:1706.03762 [6] |
| **Position / opinion** | The field is measuring the wrong thing, or building something harmful. | *On the Dangers of Stochastic Parrots*, FAccT 2021, DOI 10.1145/3442188.3445922 [7] |
| **Resource / dataset** | Here is data others can use. | *ImageNet Large Scale Visual Recognition Challenge*, IJCV 2015, DOI 10.1007/s11263-015-0816-y [8] |
| **Negative result** | The reported effect is an artifact, or the method does not work. | *Are Emergent Abilities of Large Language Models a Mirage?*, arXiv:2304.15004 [9] |
| **Short / workshop** | One focused finding, in four pages. | *Feriji: A French-Zarma Parallel Corpus*, ACL SRW 2024, pp. 1-9 [10] |
| **System / demo** | Here is a working system and what it cost to build. | *PagedAttention* (vLLM), SOSP 2023, DOI 10.1145/3600006.3613165 [11] |
| **Theory** | A proof about what a class of models can do. | *On the Number of Linear Regions of Deep Neural Networks*, arXiv:1402.1869 [12] |

**Surveys** are the easiest to read and hardest to write well. A good one imposes structure on 100-300 papers; a bad one is an annotated bibliography.

**Empirical papers** are what most people mean by "a paper": a new architecture, evaluated on a task, with a table others could try to beat. **Position papers** argue rather than measure; *Stochastic Parrots* became one of the most cited papers in modern NLP without a single new experiment, and is judged on the argument and the evidence it assembles.

**Resource papers** contribute data. ImageNet redirected a decade of computer vision, and venues now run tracks for this: NeurIPS has a Datasets and Benchmarks track [13].

**Negative results** are the most useful and least published type. The Mirage paper reanalyses published results and shows that "emergent" jumps appear when you pick a discontinuous metric and vanish under continuous ones — same models, same outputs, different analysis.

**Short and workshop papers** are where a first paper should probably go. A workshop is, in NeurIPS's words, "an informal, dynamic venue for in-person discussion of work in progress and future directions" [14], and submissions are commonly capped at four pages — the ML for Systems workshop at NeurIPS 2024 states a hard four-page limit excluding references [15]. A short paper is also not a truncated long paper: ACL says it "should have a small, focused contribution", and lists reproduction reports, negative results and opinion pieces as typical kinds [2].

**System papers** describe engineering others can reuse; vLLM's contribution is a memory-management design, evidenced by serving throughput. **Theory papers** prove things: the linear-regions paper counts how many regions a ReLU network can carve the input space into, as a function of depth and width, with no dataset at all.

---

## 5. What counts as a contribution

A contribution answers "what does the field now know, or now have, that it did not before?".

| Kind | You contribute | Evidence you need |
|---|---|---|
| New method | an algorithm, architecture or training procedure | it beats strong baselines in more than one setting |
| New dataset | data others can train or evaluate on | documentation, licence, splits, baseline numbers |
| New evaluation / benchmark | a way to measure something previously unmeasured | the measure is valid and changes conclusions |
| New analysis / insight | an explanation of why existing results happen | the explanation predicts something you then test |
| New application | a method applied where it was not, on a real problem | the domain problem is genuinely new and the result matters there |
| Replication | an independent check of a published result | same protocol, reported honestly, including when it fails |

Replication is on the list. ACL's reviewer guidelines say reproduction and reimplementation studies are in scope and "deserve a fair hearing" [16]. A failed replication, reported carefully, is a contribution, not an embarrassment.

### The "existing model on a new dataset" question

Take your idea: "I fine-tuned BERT on my college's feedback comments and got 91% accuracy." Is that a contribution? Ask three questions.

1. **Is the dataset new, documented and useful to others?** If you collected 12,000 comments, cleaned and labelled them, and will release them with documentation, yes — that is a resource contribution, and the model result is the baseline proving the data is learnable. Feriji has this shape: a first French-Zarma parallel corpus of 61,085 Zarma sentences, plus models fine-tuned on it [10].
2. **Is the question new?** If the data is ordinary but the question is not — "does accuracy survive below 200 training examples?" — the contribution is the analysis. The Mirage paper has this shape: no new data, no new model, a new question about an old result [9].
3. **If neither holds**, you have an application report. Legitimate for a workshop or a company blog; not a main-track contribution, because a reader who knows the field learns nothing they could not have guessed.

### Why reviewers are strict

**Review is a ranking, not a verdict.** A conference with 10,000 submissions and 2,500 slots is not asking "is this good?" but "is this better than the 7,500 we reject?". "Existing model, new dataset" is a category with thousands of interchangeable members a year.

**The bar is in the review form.** NeurIPS reviewers are asked: "Are the tasks or methods new? Is the work a novel combination of well-known techniques? (This can be valuable!) Is it clear how this work differs from previous contributions?" [17]. The parenthetical matters — combining known pieces is allowed, but you must show what the combination buys. Reviewers are also told that slicing contributions too thinly is discouraged and may breach the dual-submission policy [17].

**Checking is now cheap.** A reviewer can search arXiv for your method name in thirty seconds. ACL even concedes the reverse pressure: "papers that are more novel tend to be harder to publish", because reviewers get conservative when they cannot map a paper onto known work [16].

---

## 6. What "novelty" really means

Novelty does not mean "nobody has ever done this". That bar is either trivially met (nobody used your seed) or impossible (somebody, somewhere, tried it).

The workable definition: **a reviewer who knows the field learns something they did not know.** It is a test about the reader, not the artifact.

| Level | What it looks like | How it ends |
|---|---|---|
| **None** | same method, same task, new dataset, no new question | rejected at a main track; fine as a blog post |
| **Incremental** | a known trick applied where it had not been, with an ablation showing which part mattered | workshops and short papers; at a top conference it needs a strong result |
| **Surprising** | the result contradicts expectations and the evidence is clean | what top venues are buying |

Incremental is not an insult. Most published papers are incremental and the field needs them: someone must check whether the trick transfers. The problem is claiming incremental work is surprising. Reviewers punish the gap between claim and evidence far harder than they punish a modest result honestly described.

The bar moves with the venue:

| Venue type | Limit | "Novel enough" means |
|---|---|---|
| Workshop | 4 pages [15] | interesting, correct, early; work in progress welcome [14] |
| ACL short paper | 4 pages of content [2] | one small, sharp, complete claim |
| NeurIPS main track | 9 pages [1] | a claim that changes what practitioners do or believe |

This is why "aim for a workshop first" is good advice, not a consolation prize. At a workshop, "I tested whether a 2-layer classifier beats logistic regression below 200 examples, and it does not" is a complete finding. At NeurIPS the same sentence needs a mechanism, a theory of when it holds, and five datasets.

### Run the novelty check

Novelty is relative to what the field knows, so you cannot assess it from your own head. You search, and you write down the searches: in this repo that is `02_literature/NOVELTY-CHECK.md` with the queries, the databases and the dates. Five queries across arXiv, Semantic Scholar and DBLP take an hour and save three months.

If you find a paper that already did it, you have three honest options: cite it and position your work as an extension, change the question, or stop. Not citing it and hoping is the option reviewers catch.

---

## 7. Reproducibility

ACM's artifact policy opens with a sentence worth memorising: "An experimental result is not fully established unless it can be independently reproduced" [18].

The same page separates three words people blur:

- **Repeatability** — same team, same setup. You rerun your own experiment and get the same number.
- **Reproducibility** — different team, same setup, using your artifacts. A stranger runs your code and gets your result.
- **Replicability** — different team, different setup, built independently.

Most papers aim at the middle one, and it is the one you can guarantee with effort.

ACM defines three independent badge families [18]: **Artifacts Evaluated** (Functional or Reusable — your artifacts passed an audit, and "Reusable" means documented well enough to be used); **Artifacts Available** (permanently retrievable, even if that is only the data behind your figures); and **Results Reproduced / Replicated** (someone else obtained your main results, with your artifacts or without them). "Available" is a deliberately low bar: you need the data behind Figure 2 and the script that draws it, not a polished library.

Venues now ask directly. The NeurIPS paper checklist asks whether you included code, data and instructions to reproduce the main results; whether you specified splits and hyperparameters; whether you report error bars and what they capture; and what compute each experiment needed [4]. A missing checklist is desk-rejected; answering "no" with a justification is not [4].

The minimum for a student project is smaller than it looks:

1. One seed written in the paper, plus two more for the main table.
2. `requirements.txt` with pinned versions.
3. One command that regenerates every table and figure.
4. A README naming the data, where to download it, and its checksum.
5. One sentence: "All experiments ran on one RTX 3050 (4 GB), about 40 minutes per run."

The empirical case is bleak. Raff attempted to reimplement 255 papers published between 1984 and 2017, deliberately *without* reading the authors' code, to find what predicts reproducibility [19]. NeurIPS responded with a program in three parts: a code submission policy, a reproducibility challenge, and the ML Reproducibility Checklist still in use today [20].

For your own work the logic is simpler. If nobody can rerun your experiment, you have not produced a result — you have produced a claim with a PDF attached. The person most likely to fail to reproduce it is you, in four months, when someone asks how you got 84.2%.

---

## 8. A worked mini-example

Question: **does a 2-layer neural classifier beat logistic regression on a small tabular dataset (n = 180 training rows), and where does the extra capacity stop helping?**

1. **Title:** "Two-Layer Classifiers Need More Data Than They Get: A Small-Sample Study on Tabular Data".
2. **Abstract:** problem (small tabular data is everywhere in Indian college settings), what you did (5 datasets, n from 60 to 500, 10 seeds), result (the MLP wins above about 250 rows, loses below 120), meaning (capacity is not free).
3. **Introduction:** why small-data classification matters, the standard advice that deep learning needs data, the gap — nobody quantifies the crossover for tabular data at this scale. Contribution: a crossover estimate, a released harness, an explanation.
4. **Related work:** the small-data literature, the tabular deep-learning debate, two paragraphs, fifteen references.
5. **Method:** logistic regression with L2 against a 2-layer MLP with 64 hidden units, same preprocessing, same splits, 10 seeds, accuracy and macro-F1.
6. **Experiments:** one table, rows for n in {60, 120, 180, 250, 400}, columns for the two models, mean ± standard deviation over 10 seeds; one figure of accuracy against n with error bands.
7. **Discussion and limitations:** the crossover sits near 250 rows, below 120 the MLP's variance dominates; five datasets, all tabular, all binary — do not generalise to images.
8. **Conclusion:** capacity helps only past a data threshold you can now estimate cheaply.
9. **Appendix:** hyperparameters, exact splits, code link, per-seed numbers.

That is a workshop paper, and a real contribution: small, checkable, and answering a question someone would actually ask. It is also finishable in a month on a laptop, which is the point of starting here.

---

## Sources

1. NeurIPS 2024, Call for Papers. https://neurips.cc/Conferences/2024/CallForPapers (retrieved 2026-11-03).
2. ACL Rolling Review, Call for Papers. https://aclrollingreview.org/cfp (retrieved 2026-11-03).
3. S. Keshav, "How to read a paper", ACM SIGCOMM CCR 37(3):83-84, 2007; DOI 10.1145/1273445.1273458. Text: https://web.stanford.edu/class/ee384m/Handouts/HowtoReadPaper.pdf (retrieved 2026-11-03).
4. NeurIPS, Paper Checklist Guidelines (serves the 2026 cycle). https://neurips.cc/public/guides/PaperChecklist (retrieved 2026-11-03).
5. "A Survey of Large Language Models", arXiv:2303.18223. https://arxiv.org/abs/2303.18223 (retrieved 2026-11-03).
6. "Attention Is All You Need", arXiv:1706.03762. https://arxiv.org/abs/1706.03762 (retrieved 2026-11-03).
7. E. Bender et al., "On the Dangers of Stochastic Parrots", FAccT '21, pp. 610-623. DOI 10.1145/3442188.3445922; https://doi.org/10.1145/3442188.3445922 (retrieved 2026-11-03).
8. O. Russakovsky et al., "ImageNet Large Scale Visual Recognition Challenge", IJCV 115:211-252, 2015. DOI 10.1007/s11263-015-0816-y; https://doi.org/10.1007/s11263-015-0816-y (retrieved 2026-11-03).
9. "Are Emergent Abilities of Large Language Models a Mirage?", arXiv:2304.15004. https://arxiv.org/abs/2304.15004 (retrieved 2026-11-03).
10. M. Keita et al., "Feriji: A French-Zarma Parallel Corpus, Glossary & Translator", ACL 2024 Student Research Workshop, pp. 1-9. DOI 10.18653/v1/2024.acl-srw.1; https://doi.org/10.18653/v1/2024.acl-srw.1 (retrieved 2026-11-03).
11. W. Kwon et al., "Efficient Memory Management for LLM Serving with PagedAttention", SOSP '23, pp. 611-626. DOI 10.1145/3600006.3613165; https://doi.org/10.1145/3600006.3613165 (retrieved 2026-11-03).
12. "On the Number of Linear Regions of Deep Neural Networks", arXiv:1402.1869. https://arxiv.org/abs/1402.1869 (retrieved 2026-11-03).
13. NeurIPS 2024, Call for Datasets and Benchmarks Track. https://neurips.cc/Conferences/2024/CallForDatasetsBenchmarks (retrieved 2026-11-03).
14. NeurIPS 2024, Call for Workshops. https://neurips.cc/Conferences/2024/CallForWorkshops (retrieved 2026-11-03).
15. ML for Systems workshop, NeurIPS 2024, Call for Papers. http://mlforsystems.org/neurips2024/call_for_papers.html (retrieved 2026-11-03).
16. ACL Rolling Review, Reviewer Guidelines (October 2026 revision). https://aclrollingreview.org/reviewertutorial (retrieved 2026-11-03).
17. NeurIPS 2024, Reviewer Guidelines. https://neurips.cc/Conferences/2024/ReviewerGuidelines (retrieved 2026-11-03).
18. ACM, Artifact Review and Badging - Current, v1.1, 24 August 2020. https://www.acm.org/publications/policies/artifact-review-and-badging-current (retrieved 2026-11-03).
19. "A Step Toward Quantifying Independently Reproducible Machine Learning Research", arXiv:1909.06674. https://arxiv.org/abs/1909.06674 (retrieved 2026-11-03).
20. "Improving Reproducibility in Machine Learning Research (NeurIPS 2019 Reproducibility Program)", arXiv:2003.12206. https://arxiv.org/abs/2003.12206 (retrieved 2026-11-03).

## How confident is this?

- **Solid.** Every page limit, badge definition and checklist item was read on the venue or publisher page on 2026-11-03. The 9-page NeurIPS limit, the 8/4-page ACL limits, the mandatory limitations section, the 4-page workshop cap and the three ACM badge families are quoted, not remembered.
- **Solid.** Every example paper resolves to the exact title claimed: DOIs through the Crossref API, arXiv identifiers through the arXiv API, both on 2026-11-03.
- **UNCERTAIN.** The per-section lengths in the anatomy table (abstract 150-250 words, related work 0.5-1 page, and so on) are conventions read off published CS papers. No venue publishes them, and a theory paper will not match that table at all.
- **UNCERTAIN.** "Thirty to sixty references" is a typical range for a workshop paper, not a rule; surveys often carry 200 or more.
- **UNCERTAIN.** The claim that most published papers are incremental is my judgement from reading the literature, not a measured statistic.
- **Changeable.** Rules move between cycles: the pages cited are NeurIPS 2024 and the ACL Rolling Review October 2026 revision. Check the current call for papers before submitting.

last_updated: 2026-11-03
