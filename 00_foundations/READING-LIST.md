# Reading list — 15 places to learn how to read and write papers

> **READ THIS FIRST — 10 lines**
> 1. This page is fifteen free things to read about reading and writing papers, in the order that helps most, each with a reading time and a difficulty.
> 2. The one thing: if you have one hour, read [1] (35 minutes) then [2] (15 minutes) and you have a working method today.
> 3. Read it today, before your first paper, then come back to it when you start drafting.
> 4. Skip on a first pass: items 6-8 (writing-style guides) and 15 (the Transformer explainer); they are for later stages.
> 5. Fifteen items, all free, every URL checked on 2026-11-03, and every one carries a stated reading time.
> 6. The one-hour path: [1] How to Read a Paper at 35 minutes, plus [2] at 15 minutes.
> 7. Two weeks before you submit, read [3], [5] and [10] and edit the draft against them.
> 8. Item [10] is the NeurIPS 2026 reviewer guidelines, 30 minutes, and it is the clearest public statement of what reviewers judge.
> 9. Date-sensitive: item [10] is year-stamped (2026) and its guidelines change each cycle, and links rot, so re-check before relying on one.
> 10. Full read about 11 minutes (2,400 words) to read the list itself; the one-hour path is items [1] and [2].

**What this page is for:** fifteen things worth reading, in the order that helps most, so you are not guessing. Each one is free to read, was checked with a live request on 2026-11-03, and says how long it takes and how hard it is.

**If you only have one hour:** read [1] (35 minutes) and [2] (15 minutes). That pair gives you a working method for reading a paper today.

**If you are two weeks from submitting:** read [3], [5] and [10], then edit your draft against them.

**How the checks were done:** every URL below was requested once with Python `requests` from this machine on 2026-11-03, following redirects, and the status code and content type were recorded. "OK" means the page returned 200 and served the resource it claims to be. Reading times are my estimates for a careful first read, not measured.

---

### 1. How to Read a Paper

**URL:** https://web.stanford.edu/class/ee384m/Handouts/HowtoReadPaper.pdf  
**Author / organisation:** S. Keshav (University of Waterloo)  
**Year:** 2007  
**Reading time:** about 35 minutes  
**Difficulty:** easy  
**Access:** OK

The three-pass method: read the title, abstract and section headings first; then the figures and conclusions; only then the details. It is the single most useful thing on this list, and it is short.

**When to read it:** Read it first, this week. Everything else assumes you can get through a paper without reading every word.

**Note:** Published in ACM SIGCOMM Computer Communication Review 37(5). The Stanford PDF below is the full text. The ACM page (dl.acm.org/doi/10.1145/1273445.1273458) refused automated requests with HTTP 403, so the PDF is the verified copy.

### 2. How to Read a Technical Paper

**URL:** https://www.cs.jhu.edu/~jason/advice/how-to-read-a-paper.html  
**Author / organisation:** Jason Eisner (Johns Hopkins University)  
**Year:** 2009  
**Reading time:** about 15 minutes  
**Difficulty:** easy  
**Access:** OK

A one-page set of habits: give yourself a time budget per page, skim before you study, and write a one-paragraph summary of each paper you finish. The summary habit is what turns reading into a literature review you can actually use.

**When to read it:** Read straight after Keshav, before your first batch of ten papers.

**Note:** A plain HTML page, no paywall.

### 3. Tips for Writing Technical Papers

**URL:** https://cs.stanford.edu/people/widom/paper-writing.html  
**Author / organisation:** Jennifer Widom (Stanford University)  
**Year:** undated; page live 2026-11-03  
**Reading time:** about 40 minutes  
**Difficulty:** medium  
**Access:** OK

Practical rules for structure, including the five-paragraph introduction (problem, why it matters, why it is hard, why it is unsolved, what you did). It also covers where to put related work and how to handle versions of a paper online.

**When to read it:** Read when you have results and are about to write, not before. This is the outline you will copy.

**Note:** Undated page; I could not find a publication year, so it is marked undated rather than guessed.

### 4. How to Write a Great Research Paper

**URL:** https://simon.peytonjones.org/great-research-paper/  
**Author / organisation:** Simon Peyton Jones (Microsoft Research)  
**Year:** 2016 slides; talk recorded earlier  
**Reading time:** 60 minutes for the talk, 20 for the slides  
**Difficulty:** easy  
**Access:** OK

Seven concrete suggestions delivered as a talk, including the one that matters most for a beginner: write the paper before you do the work, and use the paper to decide what the work is. The slide deck is free to reuse with acknowledgement.

**When to read it:** Watch it once end to end. Then keep the slides open while you draft.

**Note:** The page links the slides (PDF and PPT) and a 34-minute Cambridge recording.

### 5. How to Write a Technical Paper or a Research Paper

**URL:** https://homes.cs.washington.edu/~mernst/advice/write-technical-paper.html  
**Author / organisation:** Michael Ernst (University of Washington)  
**Year:** undated; page live 2026-11-03  
**Reading time:** about 45 minutes  
**Difficulty:** medium  
**Access:** OK

A dense checklist: what goes in each section, how to write an abstract that states the result, how to make figures readable, and a long list of specific mistakes with examples. It is the closest thing to a marking scheme.

**When to read it:** Use it as a checklist on your own draft, section by section, the day before you send it to anyone.

**Note:** Undated page; the advice is stable but some LaTeX and tooling examples are older.

### 6. Writing Systems and Networking Articles

**URL:** https://www.cs.columbia.edu/~hgs/etc/writing-style.html  
**Author / organisation:** Henning Schulzrinne (Columbia University)  
**Year:** undated; page live 2026-11-03  
**Reading time:** about 20 minutes  
**Difficulty:** easy  
**Access:** OK

Short, blunt advice on the mechanics: tense, voice, paragraph length, when to use a list, and how to write figure captions that stand alone. It is written for systems papers but the sentence-level rules apply to any field.

**When to read it:** Read before your first full draft, then again during editing.

**Note:** Undated page; plain HTML.

### 7. Whitesides' Group: Writing a Paper

**URL:** https://mason.gmu.edu/~hjing2/advice%20for%20phd%20students/Writing%20a%20paper-George%20Whiteside.pdf  
**Author / organisation:** George M. Whitesides (Harvard University)  
**Year:** 2004  
**Reading time:** about 30 minutes  
**Difficulty:** medium  
**Access:** OK (university mirror of a paywalled article)

The argument that a paper is a plan for the research, not a report written afterwards, plus the outline-first method: agree on the data and the outline before writing a sentence of prose. It is the most quoted piece of writing advice in science.

**When to read it:** Read when you are designing the experiment, not after. It will change what you record.

**Note:** Originally in Advanced Materials 16(15):1377 (Wiley, paywalled; the Wiley page returned 403 here). This verified PDF is a university mirror of the same article.

### 8. Ten Simple Rules for Structuring Papers

**URL:** https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005619  
**Author / organisation:** Brett Mensh and Konrad Kording (PLOS Computational Biology)  
**Year:** 2017  
**Reading time:** about 25 minutes  
**Difficulty:** easy  
**Access:** OK

Ten rules that reduce to one idea: every paragraph should make one point, and the paper's structure should make the argument in the same order a reader needs it. Rule 4 (the context-content-conclusion paragraph) is worth the whole article.

**When to read it:** Read alongside Widom [3], before you write your first draft.

**Note:** Open access under CC BY.

### 9. Troubling Trends in Machine Learning Scholarship

**URL:** https://arxiv.org/abs/1807.03341  
**Author / organisation:** Zachary Lipton and Jacob Steinhardt  
**Year:** 2018  
**Reading time:** about 45 minutes  
**Difficulty:** medium  
**Access:** OK

A critique of how ML papers mislead without lying: suggesting a method works for reasons it was not tested for, maths that decorates rather than explains, and claims that outrun the experiments. Reading it makes you a harder reviewer of your own results.

**When to read it:** Read after you have read five or six ML papers and started to notice the pattern.

**Note:** arXiv preprint 1807.03341; also published at ICML 2018 as a position paper.

### 10. 2026 Reviewer Guidelines

**URL:** https://neurips.cc/Conferences/2026/ReviewerGuidelines  
**Author / organisation:** NeurIPS  
**Year:** 2026  
**Reading time:** about 30 minutes  
**Difficulty:** medium  
**Access:** OK

What reviewers are told to judge: quality, clarity, originality and significance, with different bars for different contribution types including negative results. It is the clearest public statement of what a reviewer is looking for, which makes it a checklist for authors.

**When to read it:** Read before you write, and again before you submit, pretending you are the reviewer.

**Note:** The venue's own page for the current cycle. Guidelines change year to year, so read the one for the year you submit to.

### 11. ARR Reviewer Guidelines

**URL:** https://aclrollingreview.org/reviewerguidelines  
**Author / organisation:** ACL Rolling Review (Association for Computational Linguistics)  
**Year:** undated; current version live 2026-11-03  
**Reading time:** about 30 minutes  
**Difficulty:** medium  
**Access:** OK

A second set of reviewer guidelines, written for NLP, with concrete language about soundness, reproducibility and what counts as a real claim. Reading two venues' guidelines shows you which expectations are universal and which are local custom.

**When to read it:** Read after [10], especially if you are targeting an NLP venue.

**Note:** Live guidelines page, updated by ARR; undated, so the year is not stated.

### 12. Submission Overview

**URL:** https://info.arxiv.org/help/submit/index.html  
**Author / organisation:** arXiv  
**Year:** undated; current version live 2026-11-03  
**Reading time:** about 20 minutes  
**Difficulty:** easy  
**Access:** OK

The actual rules for posting a preprint: what counts as an acceptable submission, licensing choices, versioning, and endorsement for new authors in some categories. Read it before you need it, because the endorsement step can take days.

**When to read it:** Read the week you decide to post a preprint, and check whether your category needs endorsement.

**Note:** Official help pages; the endorsement page is separate (info.arxiv.org/help/endorsement.html).

### 13. Learn LaTeX in 30 minutes

**URL:** https://www.overleaf.com/learn/latex/Learn_LaTeX_in_30_minutes  
**Author / organisation:** Overleaf  
**Year:** undated; current version live 2026-11-03  
**Reading time:** about 30 minutes, plus practice  
**Difficulty:** easy  
**Access:** OK

A hands-on introduction to the commands you need for a paper: sections, equations, figures, tables, citations and references. Doing it inside Overleaf means you compile as you go instead of fighting an install.

**When to read it:** Do it the same week you start writing, in a throwaway project, not in your real paper.

**Note:** Free tutorial; no account needed to read it.

### 14. Academic Phrasebank

**URL:** https://www.phrasebank.manchester.ac.uk/  
**Author / organisation:** University of Manchester  
**Year:** undated; current version live 2026-11-03  
**Reading time:** reference; 10 minutes per section  
**Difficulty:** easy  
**Access:** OK

Collections of standard academic phrases grouped by function: describing methods, reporting results cautiously, comparing with prior work, stating limitations. Use it to get unstuck, not to fill a paper with stock sentences.

**When to read it:** Keep it open while editing. Use one phrase, then rewrite it in your own words.

**Note:** Free; navigation is by function rather than alphabetical.

### 15. The Illustrated Transformer

**URL:** https://jalammar.github.io/illustrated-transformer/  
**Author / organisation:** Jay Alammar  
**Year:** 2018  
**Reading time:** about 45 minutes  
**Difficulty:** medium  
**Access:** OK

A visual walkthrough of attention and the transformer, with diagrams of queries, keys and values. If you plan to work on anything LLM-related, this is the explanation that makes the architecture page of a paper readable.

**When to read it:** Read before your first NLP or LLM paper, then again after.

**Note:** Personal blog, free, diagrams included.


---

## Sources

All URLs requested on 2026-11-03. Status codes as returned to a plain HTTP GET.

1. How to Read a Paper — https://web.stanford.edu/class/ee384m/Handouts/HowtoReadPaper.pdf — OK — retrieved 2026-11-03 (200, application/pdf)
2. How to Read a Technical Paper — https://www.cs.jhu.edu/~jason/advice/how-to-read-a-paper.html — OK — retrieved 2026-11-03 (200, text/html)
3. Tips for Writing Technical Papers — https://cs.stanford.edu/people/widom/paper-writing.html — OK — retrieved 2026-11-03 (200, text/html)
4. How to Write a Great Research Paper — https://simon.peytonjones.org/great-research-paper/ — OK — retrieved 2026-11-03 (200, text/html)
5. How to Write a Technical Paper or a Research Paper — https://homes.cs.washington.edu/~mernst/advice/write-technical-paper.html — OK — retrieved 2026-11-03 (200, text/html)
6. Writing Systems and Networking Articles — https://www.cs.columbia.edu/~hgs/etc/writing-style.html — OK — retrieved 2026-11-03 (200, text/html)
7. Whitesides' Group: Writing a Paper — https://mason.gmu.edu/~hjing2/advice%20for%20phd%20students/Writing%20a%20paper-George%20Whiteside.pdf — OK (university mirror of a paywalled article) — retrieved 2026-11-03 (200, application/pdf)
8. Ten Simple Rules for Structuring Papers — https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005619 — OK — retrieved 2026-11-03 (200, text/html)
9. Troubling Trends in Machine Learning Scholarship — https://arxiv.org/abs/1807.03341 — OK — retrieved 2026-11-03 (200, text/html)
10. 2026 Reviewer Guidelines — https://neurips.cc/Conferences/2026/ReviewerGuidelines — OK — retrieved 2026-11-03 (200, text/html)
11. ARR Reviewer Guidelines — https://aclrollingreview.org/reviewerguidelines — OK — retrieved 2026-11-03 (200, text/html)
12. Submission Overview — https://info.arxiv.org/help/submit/index.html — OK — retrieved 2026-11-03 (200, text/html)
13. Learn LaTeX in 30 minutes — https://www.overleaf.com/learn/latex/Learn_LaTeX_in_30_minutes — OK — retrieved 2026-11-03 (200, text/html)
14. Academic Phrasebank — https://www.phrasebank.manchester.ac.uk/ — OK — retrieved 2026-11-03 (200, text/html)
15. The Illustrated Transformer — https://jalammar.github.io/illustrated-transformer/ — OK — retrieved 2026-11-03 (200, text/html)

Two URLs I checked and did **not** include, with the reason:

- `https://dl.acm.org/doi/10.1145/1273445.1273458` (the ACM DL version of Keshav) returned **403** to automated requests. The Stanford PDF in entry [1] is the same paper and is the link to use.
- `https://onlinelibrary.wiley.com/doi/10.1002/adma.200400767` (the Wiley version of Whitesides) returned **403** and is paywalled anyway. Entry [7] points at a university mirror that serves the full PDF.

## How confident is this?

- **Solid.** All fifteen URLs returned HTTP 200 on 2026-11-03 and served the resource named: HTML pages for fourteen of them, a PDF for [1] and [7]. Titles and authors were checked against the page itself, not against a search result.
- **Solid.** [1], [7] and [8] were additionally read for content (the three-pass method, the outline-first argument, the structuring rules), so the descriptions are not guesses from titles.
- **UNCERTAIN — years.** Entries [3], [5], [6], [11], [12], [13] and [14] are undated pages. I wrote "undated" rather than guessing a year. Entry [4]'s slides are dated 2016 by their hosting; the talk itself is older.
- **UNCERTAIN — reading times.** All times are estimates for a careful first read; they are not measured.
- **UNCERTAIN — link stability.** University personal pages ([2], [3], [5], [6]) and the GMU mirror [7] are the kind of URLs that move when someone retires. If one breaks, search the exact title plus the author's surname.
- **Not included, because I could not verify them today:** a Semantic Scholar "how to read a paper" post (no stable URL found), the UGC/Scopus indexing guides, and any "structured abstracts" guidance page (no primary source loaded).

last_updated: 2026-11-03
