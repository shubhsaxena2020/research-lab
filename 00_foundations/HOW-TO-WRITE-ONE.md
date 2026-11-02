# How to Write Your First Paper, End to End

> **READ THIS FIRST — 10 lines**
> 1. This page is the working process for a first paper: the order of the stages, the hours each takes, and where beginners lose weeks.
> 2. The most useful rule in it: write the tables and figures first and the introduction last, because the claim only becomes true after the experiment.
> 3. Read it before you start the experiment; §3 and §4 change what you write down while you work.
> 4. Skip on a first pass: §8 LaTeX and Overleaf (the skeleton and five errors) and §10(b) the three-month plan; return when you reach that stage.
> 5. Budget 70-120 hours for the whole paper, and expect the hours to be lumpy.
> 6. Read 15-25 papers properly and skim 40-60; the Related Work section itself is only half a page.
> 7. Run 3-5 seeds per configuration and report mean and standard deviation; a 0.6-point gain against a 1.4-point spread is noise.
> 8. The two-week workshop plan is about 56 hours and works only if the data already exists and is clean.
> 9. Date-sensitive: the free-tool facts (Colab publishes no GPU limits and sessions die without warning) and each venue's current page limits.
> 10. Full read about 22 minutes (4,800 words); the skim path in item 4 about 17 minutes.

**What this page is for.** The actual working process behind a first research paper: what happens in what order, how long each stage takes, and where beginners lose weeks. It assumes you know the parts of a paper (title, abstract, method, results, references). It does not assume you have run an experiment, searched a database, or opened LaTeX.

Written for one person: a first-semester BCA student with a laptop, exam weeks, and about 4 hours a day at best.

## 1. The honest overview

A paper is not written. It is assembled, then repaired several times. The real sequence for a small empirical paper in AI or NLP:

| # | Stage | What you actually do | Time (small paper) |
|---|---|---|---|
| 1 | Idea | Notice one narrow thing that seems wrong or untested | 3–10 h, over days |
| 2 | Reading | Find the 10 papers that define the area and what they did not test | 15–25 h |
| 3 | Question | Shrink the idea until it fits 40 hours of work | 2–4 h |
| 4 | Tiny experiment | One dataset, two baselines, one change | 10–20 h, mostly debugging |
| 5 | Draft | Tables and figures first, then prose | 25–35 h |
| 6 | Internal review | Someone else reads it and finds the holes | 3–5 h, plus fixes |
| 7 | Submission | Format, page limit, checklist, upload | 4–8 h |
| 8 | Rebuttal | Answer reviewers in 1–2 pages under a deadline | 6–12 h |
| 9 | Camera-ready | Fix the paper using reviewer comments | 5–10 h |

That is roughly 70–120 hours, and the hours are lumpy: one day you do six, the next three vanish into a bug.

**The loop-backs are the normal case.** The table looks linear; it is not.

- **Experiment fails → back to reading.** Your idea scores worse than the dumb baseline and you cannot tell whether the idea or your code is wrong. This happens at least once, usually twice.
- **Reading → new question.** Paper 12 shows everyone evaluates on one dataset. Your question changes. That is progress.
- **Drafting → new experiment.** Writing the method in plain words exposes a step you never defined.
- **Review → new framing.** A reviewer says your contribution is a special case of something from 2019. You answer it or reframe it. Both are work.

One habit saves people: **write down the claim you believe, with a date, every week.** When it changes you can see why, instead of quietly rewriting history.

## 2. The literature review is a process, not a chapter

The "Related Work" section is half a page. The reading behind it is 40–80 papers, most skimmed. Do not confuse the two.

### Where to search

| Tool | Best for | Note |
|---|---|---|
| Google Scholar [25] | Keyword search, "cited by" links | Use the page by hand. Do not scrape it; that breaks its terms. |
| Semantic Scholar [23] | Citation contexts, "papers citing this", free API | Scriptable |
| arXiv [22] | Newest CS preprints, full text free | Not peer reviewed; check if it was later published |
| DBLP [24] | Clean venue and author records in CS | Good for "what appeared at ACL 2023", not for ideas |

Try 3–4 keyword phrasings; read titles only; keep 25–40 candidates in a spreadsheet.

### Snowballing: how one good paper becomes forty

Take the best paper you have found (usually a survey, or the one everyone cites). Move in two directions [2]:

- **Backward:** open its reference list and check each entry against your question. This finds the foundations — older, smaller, often clearer.
- **Forward:** find every paper citing it ("Cited by" in Scholar, citations in Semantic Scholar) and skim the titles. This finds what happened next, including the paper that already did your idea.

Wohlin's guidelines run this in iterations: start from a start set, snowball, screen, then snowball again from the newly included papers until an iteration adds nothing new [2]. Two iterations usually cover a small field, and every paper you open is already connected to your question.

### Notes you can actually use

Do not write paragraph summaries; they are unreadable three weeks later. One table, one row per paper:

| Paper | Claim (your words) | Evidence (data, metric, number) | Limitation |
|---|---|---|---|
| A | Synthetic typos improve robustness to noisy text | 3 classifiers, 2 datasets, +4.1 F1 on noisy test | English only; hand-written noise model |
| B | Sentence embeddings beat TF-IDF on short queries | 1 dataset, 5 folds, +6 nDCG | Single domain; no length ablation |

A claim with no evidence in the third column tells you the paper is an opinion piece. The limitation column is where your question comes from: when five papers share the same limitation, that is not a gap in your reading, it is your gap.

### When to stop

There is no universal number. The test is not "have I found every paper" but "would one more paper change what I do next" [3]. You are close when three searches in a row return papers you have already seen, and when you can predict a new paper's method and limitation from its title.

For a first small paper: **15–25 papers read properly** (method and results understood, notes filled) and **40–60 skimmed**. That is judgment from practice, not a rule from a textbook; a narrow question may need 12. Set a date: "reading stops on day 8 whether or not I feel ready."

Learn one technique now: Keshav's three passes [1]. First pass, 5–10 minutes — title, abstract, intro, headings, conclusions; decide whether it is relevant at all. Second pass, up to an hour — figures, tables, method; you should be able to summarise it aloud. Third pass, four or five hours (Keshav's figure "for beginners"; he says about an hour for an experienced reader) — reserve it for the small number of papers you must reimplement or beat. Beginners read everything at pass three and run out of time by paper six.

## 3. From reading to a research question

A topic is not a question. "Sentiment analysis for Hindi" cannot be answered, so it cannot be finished, so it cannot become a paper.

Two frameworks help, both from clinical research:

- **PICO** — Population, Intervention, Comparison, Outcome [4]. In CS: which data, what you change, what you compare against, which metric decides.
- **FINER** — Feasible, Interesting, Novel, Ethical, Relevant [4]. The one that saves undergraduates is **Feasible**: can you do this with your data, skills and hours?

### The one-sentence form

> On **[dataset]**, does **[your change]** improve **[metric]** compared with **[baseline]**, and by how much?

Example: "On the SST-2 and IMDB test sets, does a character-level tokenizer improve macro-F1 for a 6-layer transformer trained on 10k examples, compared with a word-level baseline?"

Every part is bounded: two public datasets, one model size, one metric, one comparison. If a slot is vague ("better performance", "real-world text"), you will not know when you are done.

### The feasibility test that works

Estimate hours first. For that sentence: clean data 3 h, baseline 4 h, five baseline runs 3 h, implement the change 8 h, debug 6 h (always), five runs 2 h, tables 3 h — about 29 hours plus compute. A question needing 200 hours is not a first paper.

### Question versus task

| | Example | Finish line |
|---|---|---|
| Task | "Build a Hindi sentiment classifier" | Never — accuracy can always improve |
| Question | "Does X improve Y over Z on dataset D, by how much?" | When the experiment is run and the number reported |

A task gives you a demo. A question gives you a result you can defend, including a negative one.

## 4. Hypotheses and pre-registration

A hypothesis is a prediction you can be wrong about, written before you look at the results.

> **Prediction:** character-level tokenization improves macro-F1 by at least 2 points on noisy text, and by less than 1 point on clean text.
> **Metric:** macro-F1 on the held-out test split, mean of 5 seeds.
> **Decision rule:** the effect counts as real only if the 5-seed mean difference exceeds the between-seed spread.

**Why write it first.** Because you are extremely good at fooling yourself, and the fooling is not conscious. Run four variants, look at the numbers, then pick the metric where your method wins, and you have fitted a story to noise. The fix has a name — separating confirmatory from exploratory analyses: planned tests are reported as planned, unplanned ones are labelled exploratory and treated as tentative [5].

Pre-registration in ML is light. The minimum version costs 30 minutes:

1. A dated file with hypothesis, metric, datasets, seeds, baseline, and the exact command.
2. One sentence on what result would make you abandon the idea.

Psychology uses OSF for this [5]; in ML the nearest institutional habit is the reproducibility checklist venues now require [6][7]. NeurIPS states that papers without its checklist are desk rejected [7]. Filling that in early is pre-registration with a deadline attached.

**What a null result means.** If your change does not help, you learned that a plausible intervention fails under a specified setup. That is information, and it is publishable — but only where someone wants it. Workshops exist for this: the ACM workshop on Negative Results in Network Measurements invites work whose methods "did not yield the expected results" [27]. Main conferences reject nulls unless they are surprising and well tested; "it did not work on one dataset" is a blog post. A null becomes publishable when it contradicts a believed claim, or when a reported effect vanishes under a fair baseline. Report it as a null; do not spin "no significant difference" into "competitive performance".

## 5. Experiments a beginner can run

**Two baselines, always.** A **dumb baseline** that needs no ML — majority class, random, TF-IDF plus logistic regression. It catches the dataset that is 90% one class, where 90% accuracy means nothing. And a **strong baseline** — the best simple published method, ideally with public code. If you cannot beat it, your contribution is not established, and you need to know that on day five, not day twenty.

**One variable at a time.** Tokenizer or learning rate or augmentation, not all three. Change three things and a reviewer cannot tell which one worked. Ablations apply the same principle afterwards.

**Seeds and spread.** Set every seed explicitly (`random`, `numpy`, `torch`). Run **3–5 seeds** per configuration and report mean and standard deviation, never the best run. A 0.6-point gain when seed-to-seed spread is 1.4 points is noise with a decimal point. Five seeds × two settings × 20 minutes is roughly 3.5 hours — affordable. Cherry-picking the best of five costs the same and yields a number you cannot defend.

**Save everything.** Raw predictions and per-seed metrics to `runs/char_tok_s3/metrics.json`; the exact command and git hash in `run_log.md`; stdout and stderr to files, because the traceback you need is the one that scrolled past. A number that cannot be traced to a file gets deleted.

**Compute you actually need.** Order of magnitude:

| Setup | What fits | Rough time |
|---|---|---|
| Laptop CPU | TF-IDF + linear model, ≤20k short texts | Minutes per run |
| Laptop CPU | Small transformer (~60M params), 10k texts, 3 epochs | 3–8 h per run |
| Free Colab GPU | Same small transformer | 15–40 min per run |
| Free Colab GPU | Full BERT-base fine-tune, 10k texts | 30–90 min per run |

These are planning estimates, not measurements. Time one run before planning five.

Colab gives GPUs free but publishes no limits, because idle timeouts, maximum VM lifetime and available GPU types vary [21]. So assume a session dies without warning, checkpoint every epoch to Drive, and never plan a run longer than about 8 hours. Keep the project under 1 GB: a 10k-row text CSV is a few MB, a small transformer checkpoint 250–500 MB. A plan needing a 50 GB corpus is not a first paper on a shared laptop.

## 6. Writing order (the most useful tip here)

1. **Tables and results.** Decide what the reader must see, built from real files. This exposes missing experiments.
2. **Method.** Exactly what you did, past tense, in the order you did it, with every hyperparameter needed to reproduce it.
3. **Introduction.** Now you know the result, so the contribution can be stated accurately.
4. **Related work.** Now you know which papers you actually differ from.
5. **Abstract.** A summary, so it comes near the end.
6. **Title.** Last, and rewritten three times.

**Why the intro first is a trap.** The introduction contains your claim, and before the experiment the claim is a hope. Beginners who start there spend two days on elegant motivation for a result that turns out to be 0.4 points with overlapping error bars — then either rewrite everything or, worse, keep the overclaim and bend the results toward it. Whitesides says the same from chemistry: an outline should be "a carefully organized and presented set of data", and the abstract should not be written until the paper is complete, because you do not yet know what you found [11].

Keep a one-page claims file: every sentence you intend to claim gets a pointer to the table that supports it. No pointer means it is either motivation (label it) or unsupported (cut it).

## 7. Figures and tables

One message per figure. If you cannot say what it shows in one sentence, it shows two things. Rule 2 of "Ten Simple Rules for Better Figures" is exactly this: identify the message, then design [8].

- **Readable at 100% zoom.** If you must zoom to read an axis label, the font is too small. Set the figure to the final printed width (about 3.3 in for one column), use 8–10 pt text, and do not scale the image afterwards.
- **No 3D charts, no pie charts for comparing quantities** — both distort perceived quantities [8, rule 7].
- **The caption stands alone.** A reader who jumps to the figure should get the message, setup and units. Captions are not optional [8, rule 4].
- **Do not trust defaults** — they are "good enough for any plot but best for none" [8, rule 5]. Default `jet` hides structure; use sequential maps for ordered values, qualitative for categories [8, rule 6].
- **Colour-blind safe.** Red-green colour blindness affects up to 8% of men of Northern European ancestry; with three male reviewers the chance at least one is colour blind is about 22% [9]. Use a palette designed for it (ColorBrewer's "colorblind safe" filter [10]) and never encode meaning in colour alone — vary line style or marker too.
- **Resolution.** Vector PDF/SVG where possible, else 300 dpi at final size; `plt.savefig("fig1.pdf", bbox_inches="tight")` [26].

Tables are figures with words: no vertical rules, units in the header, best number bolded, mean ± std, run count in the caption, same row order across tables. A table with no spread says you ran it once.

Tools: matplotlib for anything with data (script it, never hand-edit the output), draw.io or Excalidraw for pipeline diagrams (export SVG or 2× PNG). Keep the script per figure, so a reviewer's request costs ten minutes rather than an evening.

## 8. LaTeX and Overleaf, concretely

LaTeX is a typesetting system, not a word processor: you write plain text with commands and a program produces the PDF [12]. CS uses it because venues ship style files that enforce page limits, because maths and cross-references work, and because the source is text that version control handles.

### Minimal skeleton

```latex
\documentclass[11pt]{article}
\usepackage{graphicx, booktabs}
\title{Does a Character-Level Tokenizer Help on Noisy Short Text?}
\author{Shubh Saxena\\PSIT College of Higher Education, Kanpur}
\begin{document}
\maketitle
\begin{abstract} ... (write last) \end{abstract}

\section{Introduction} ...
\section{Method} ...

\section{Results}
Table~\ref{tab:main} reports macro-F1 over five seeds.
\begin{table}[t]\centering
\begin{tabular}{lcc}\toprule
Model & Clean & Noisy \\ \midrule
TF-IDF + LR & 81.2 \(\pm\) 0.4 & 74.9 \(\pm\) 0.7 \\
Word-level  & 88.6 \(\pm\) 0.3 & 80.1 \(\pm\) 1.1 \\ \bottomrule
\end{tabular}
\caption{Macro-F1, mean \(\pm\) std over 5 seeds.}
\label{tab:main}
\end{table}

\bibliographystyle{plain}
\bibliography{refs}
\end{document}
```

### Get the venue's own template

Never submit in `article` class.

- **IEEE conferences:** the templates page provides the LaTeX zip and bibliography files, and warns that leftover template guidance text can stop a paper being published [18].
- **ACL / EMNLP / NAACL family:** official style files are in `acl-org/acl-style-files`, also an Overleaf template, and authors may not modify them or borrow another conference's [19]. Concrete limits: review versions get 8 pages of content plus unlimited references for long papers, 4 pages for short [20].
- **NeurIPS:** the style file ships with the formatting instructions linked from the checklist page, and the checklist is mandatory [7].

If a venue page is unclear, email the chairs; guessing is a desk rejection.

### Five errors beginners hit

1. **`Missing $ inserted`** — maths outside maths mode, e.g. `accuracy > 90%` or an underscore in `model_name`. Use `$>$`, `90\%`, `\_` [13].
2. **`There were undefined references`** — the target does not exist yet, or you compiled once. Cross-references need two passes; Overleaf does it automatically, local `pdflatex` does not [13].
3. **`File 'xyz.sty' not found`** — the package is not installed. Check for a typo first, then install it through your TeX distribution.
4. **`Overfull \hbox`** — a warning: a line sticks into the margin, usually a long URL or a wide table. Fix with `microtype`, a `p{...}` column, or `\url{}`; unfixed, the paper looks sloppy in print.
5. **Citations render as `[?]` or the bibliography is empty** — BibTeX was not run, or the `.bib` key does not match. Order: latex → bibtex → latex → latex [14].

### If Overleaf is unavailable

Install TeX Live (all platforms, large) [16] or MiKTeX (Windows, installs packages on demand, ~142 MB basic installer) [17]. Then `pdflatex main.tex`, `bibtex main`, `pdflatex main.tex` twice. learnlatex.org has 16 short browser-run lessons covering exactly these commands [15]. Budget 3–4 hours; a first paper needs no more.

## 9. Twenty mistakes, one line each

1. Claiming state of the art after beating one baseline on one dataset.
2. No baseline at all, only "our method" numbers.
3. A table of numbers with no standard deviation and no seed count.
4. Testing on the data you tuned on.
5. Reporting the best of five runs.
6. Changing three things at once and crediting one.
7. A question that cannot be answered, only discussed.
8. Reading 60 papers and starting no experiment.
9. Running the experiment with no written hypothesis.
10. A figure with two messages and a caption that explains neither.
11. Copying a sentence without quotes — plagiarism, even with a citation.
12. Citing a paper you never opened, based on someone else's description.
13. "Novel" in the abstract with no novelty check.
14. Related work that lists papers instead of saying how you differ.
15. Ignoring the page limit until the night before.
16. Using the wrong venue template.
17. Submitting without the required checklist [7].
18. Hiding a negative result instead of reporting it as negative.
19. No run log, so no number traces back to a command.
20. Submitting with the template's example text still in the file [18].

## 10. Two realistic timelines

### (a) Two weeks at ~4 h/day, workshop-style paper

About 56 hours. This works only if the experiment is small and **the data already exists and is clean**. If you must collect or label data, add two weeks.

| Day | Work | h |
|---|---|---|
| 1 | Pick one narrow question; write the one-sentence form; list 5 papers | 4 |
| 2 | Read 6 papers (passes 1–2); start the notes table | 4 |
| 3 | Snowball both directions; notes to ~15 rows | 4 |
| 4 | Freeze question and metric; write the pre-registration file | 3 |
| 5 | Data loader; dumb baseline; metrics saved to a file | 4 |
| 6 | Strong baseline, 5 seeds, mean and std in a CSV | 5 |
| 7 | Implement your change; first run; expect it broken | 4 |
| 8 | Debug, rerun. If the effect is zero, decide: null or change one thing | 5 |
| 9 | Full sweep, 5 seeds. Results frozen; no new experiments after today | 4 |
| 10 | Table 1, Figure 1, Method section | 5 |
| 11 | Introduction and related work; every claim points at a table | 4 |
| 12 | Abstract, title, internal read by a friend or mentor | 4 |
| 13 | Fix what the reader found; format to the template; page limit | 5 |
| 14 | Checklist, references verified one by one, upload early | 4 |

Day 8 is where this plan usually dies. If there is no effect by day 9, write the null result.

### (b) Three months at ~10 h/week, conference submission

About 120 hours across 13 weeks.

| Week | Work | h |
|---|---|---|
| 1 | 20 papers skimmed; three candidate questions | 10 |
| 2 | Snowballing; notes to 30 rows; pick one question | 10 |
| 3 | Feasibility spike: does the baseline run at all here? | 10 |
| 4 | Pre-registration dated; data pipeline rerunnable | 10 |
| 5 | Baselines (dumb + strong), 5 seeds, results in files | 10 |
| 6 | Method implemented; first results | 10 |
| 7 | Debug and rerun, one variable at a time | 10 |
| 8 | Ablations, one component removed at a time, 3 seeds | 10 |
| 9 | Results frozen; tables and figures built from files | 10 |
| 10 | Method and results written | 10 |
| 11 | Intro and related work; mentor review; fixes | 10 |
| 12 | Abstract, title, formatting, page limit, references verified | 10 |
| 13 | Checklist, submission, buffer for the upload breaking at 23:00 | 10 |

Weeks 7 and 8 are the ones that expand. If week 10 arrives with no working experiment, skip this cycle; that is a normal decision.

## 11. Checklists

### Before you start

- [ ] I can state my question in one sentence: data, change, metric, baseline.
- [ ] I found at least one paper that tried something close, and can say how mine differs.
- [ ] The data is public, labelled, and fits on my disk.
- [ ] I have run a dumb baseline end to end, once.
- [ ] I know where results are saved and what one run costs in minutes.
- [ ] I have 40+ non-exam hours in the next month.
- [ ] One person will read a draft and say it is bad.
- [ ] I know the venue, the deadline, and the page limit.

### Before you submit

- [ ] Hypothesis and metric are in a dated file, and the paper reports that metric.
- [ ] Every number traces to a file produced by a logged command.
- [ ] Mean and spread over 3–5 seeds, run count stated in the caption.
- [ ] Dumb baseline and strong baseline both present.
- [ ] Ablation shows what each component contributes.
- [ ] Every citation was opened and verified; none inherited second-hand.
- [ ] No copied sentence without quotes.
- [ ] Every abstract claim is supported by a table or figure.
- [ ] "Novel" and "state of the art" removed or backed by a documented search.
- [ ] Negative or mixed results reported as such.
- [ ] Figures readable at 100% zoom, colour-blind safe, captions standalone.
- [ ] Venue template used, guidance text deleted, page limit met.
- [ ] Required checklist completed and not deleted [7].
- [ ] AI assistance disclosed per venue policy.
- [ ] PDF opens on another machine with fonts embedded.
- [ ] Submitted 24 hours before the deadline.

## Sources

1. S. Keshav, *How to Read a Paper*, University of Waterloo handout. https://web.stanford.edu/class/ee384m/Handouts/HowtoReadPaper.pdf (retrieved 2026-11-03)
2. C. Wohlin, *Guidelines for Snowballing in Systematic Literature Studies and a Replication in Software Engineering* (EASE '16). https://www.wohlin.eu/ease16.pdf (retrieved 2026-11-03)
3. M. B. Garcia, *When to Stop Your Literature Search* (practitioner guide). http://manuelgarcia.info/guides/research/guide/when-to-stop-your-literature-search (retrieved 2026-11-03)
4. *Back to the basics: guidance for formulating good research questions* (PICO and FINER), PMC11129835. https://pmc.ncbi.nlm.nih.gov/articles/PMC11129835/ (retrieved 2026-11-03)
5. Center for Open Science, *Preregistration* FAQ. https://www.cos.io/initiatives/prereg (retrieved 2026-11-03)
6. J. Pineau et al., *Improving Reproducibility in Machine Learning Research (NeurIPS 2019 Reproducibility Program)*, arXiv:2003.12206. https://arxiv.org/abs/2003.12206 (retrieved 2026-11-03)
7. NeurIPS, *Paper Checklist Guidelines*. https://neurips.cc/public/guides/PaperChecklist (retrieved 2026-11-03)
8. N. P. Rougier, M. Droettboom, P. E. Bourne, *Ten Simple Rules for Better Figures*, PLOS Comput Biol 10(9): e1003833, 2014. https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003833 (retrieved 2026-11-03)
9. B. Wong, *Points of view: Color blindness*, Nature Methods 8, 441, 2011. https://www.nature.com/articles/nmeth.1618 (retrieved 2026-11-03)
10. C. Brewer, *ColorBrewer 2.0*. https://colorbrewer2.org/ (retrieved 2026-11-03)
11. G. M. Whitesides, *Whitesides' Group: Writing a Paper*, Advanced Materials 16(15), 2004. https://lab.vanderbilt.edu/wp-content/uploads/sites/81/files/images/2004-%20Whitesides%20-%20Writing%20A%20Paper.PDF (retrieved 2026-11-03)
12. Overleaf, *Learn LaTeX in 30 minutes*. https://www.overleaf.com/learn/latex/Learn_LaTeX_in_30_minutes (retrieved 2026-11-03)
13. Overleaf, *Errors*. https://www.overleaf.com/learn/latex/Errors (retrieved 2026-11-03)
14. Overleaf, *Bibliography management with bibtex*. https://www.overleaf.com/learn/latex/Bibliography_management_with_bibtex (retrieved 2026-11-03)
15. *Learn LaTeX* (16-lesson beginner course). https://www.learnlatex.org/en/ (retrieved 2026-11-03)
16. TeX Users Group, *TeX Live*. https://www.tug.org/texlive/ (retrieved 2026-11-03)
17. MiKTeX, *Getting MiKTeX*. https://miktex.org/download (retrieved 2026-11-03)
18. IEEE, *Manuscript Templates for Conference Proceedings*. https://www.ieee.org/conferences/publishing/templates.html (retrieved 2026-11-03)
19. ACL Organization, *acl-style-files*. https://github.com/acl-org/acl-style-files (retrieved 2026-11-03)
20. ACLPUB, *Paper formatting guidelines*. https://acl-org.github.io/ACLPUB/formatting.html (retrieved 2026-11-03)
21. Google, *Colaboratory FAQ*. https://research.google.com/colaboratory/faq.html (retrieved 2026-11-03)
22. arXiv, *API Access*. https://info.arxiv.org/help/api/index.html (retrieved 2026-11-03)
23. Semantic Scholar, *Academic Graph API documentation*. https://api.semanticscholar.org/api-docs/ (retrieved 2026-11-03)
24. *dblp computer science bibliography*. https://dblp.org/ (retrieved 2026-11-03)
25. *Google Scholar*. https://scholar.google.com/ (retrieved 2026-11-03)
26. matplotlib, *matplotlib.pyplot.savefig*. https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html (retrieved 2026-11-03)
27. ACM SIGCOMM 2026, *Workshop on Negative Results in Network Measurements (NetNeg)*. https://conferences.sigcomm.org/sigcomm/2026/netneg/ (retrieved 2026-11-03)

## How confident is this?

- **Solid:** venue mechanics and formatting numbers (IEEE templates, ACL page limits, NeurIPS mandatory checklist, Colab's unpublished limits) come from the primary pages, verified 2026-11-03.
- **Solid:** figure rules and the colour-blindness statistics are quoted from published sources, not invented.
- **Solid:** Keshav's pass timings and Wohlin's snowballing procedure are described from the papers themselves.
- **Soft:** every compute time in section 5 is a planning estimate, not a measurement on this laptop; it can be off by a factor of two. Time one run first.
- **Soft:** "15–25 papers read, 40–60 skimmed" is practitioner judgment. No study claims that number.
- **Soft:** both timelines are reconstructions of how such projects usually go, not data. The 2-week plan assumes clean existing data.
- **UNCERTAIN:** whether a specific venue you target accepts null results; attitudes differ and change yearly, so check the current call for papers rather than relying on section 4.
- **UNCERTAIN:** Colab's exact free GPU model and session length at any moment, because Google does not publish them [21].
- **UNCERTAIN:** the LaTeX skeleton in section 8 was written without a local compile (no TeX distribution on this machine). It uses only standard packages (`article`, `graphicx`, `booktabs`), but run it once in Overleaf before trusting it.

last_updated: 2026-11-03
