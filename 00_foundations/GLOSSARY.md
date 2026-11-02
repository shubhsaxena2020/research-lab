# Glossary — research papers, reviewing, publishing and ML basics

> **READ THIS FIRST — 10 lines**
> 1. This page defines the words you will meet in your first year of reading papers, reviewing and submitting: 125 entries in alphabetical order.
> 2. The one thing: it is a lookup table, not a book, so use Ctrl+F when a word stops you.
> 3. Read it in passes: skim it now, then open it whenever a paper or a review uses a word you cannot define.
> 4. Skip on a first pass: entries whose headword you have never seen in a paper; leave them until you meet them.
> 5. 125 entries, one or two sentences each, with an example or a number where the number helps.
> 6. Citation counts differ by database (Google Scholar, Scopus, Web of Science), so always name the one you used and the date.
> 7. h5-index is the h-index computed over the last five complete years; CORE ranks conferences in four tiers, A* down to C.
> 8. CORE listed 825 ranked venues when checked on 2026-11-03, and only 7.52% of them were A*.
> 9. Date-sensitive: the UGC-CARE entry says that list has not been updated since October 2024, and the CORE and h5 numbers move every year.
> 10. Full read about 27 minutes (6,000 words); used as a lookup, a few seconds per word.

**What this page is for:** the words you will meet in your first year of reading papers, reviewing, and submitting. Each entry is one or two sentences with an example or a number where the number helps. Nothing is grouped by topic; the whole file is alphabetical, so use Ctrl+F to jump to a word.

Read it in passes, not once. Skim it now, then come back each time a word in a paper or a review stops you.

---

**Ablation study** — Removing or replacing one part of a method and re-running the experiment, to show that the part was actually doing the work. If dropping one component costs 4 F1 points, that component has earned its place in the paper.

**Abstract** — The 150–250 word summary at the top of a paper: the problem, the method, the main result with a number, and why it matters. Most readers decide whether to read further from the abstract alone, so it is the most-read and most-rewritten part.

**Acceptance rate** — Accepted papers divided by submitted papers at a venue. It is a rough difficulty signal, not a quality measure: a 20% venue and a 25% venue can differ more in reviewing culture than in rigour.

**Accuracy** — The share of predictions that are correct. It is misleading on imbalanced data: on 100 transactions where 1 is fraud, always predicting "not fraud" gives 99% accuracy and catches nothing.

**Advisor** — The faculty member who supervises a student's research: suggests readings, checks the experimental design, and signs off before submission. A good advisor reads your drafts and tells you what is wrong; that is the main thing you are selecting for.

**Affiliation** — The institution and department listed under an author's name on a paper (for Shubh: PSIT College of Higher Education, Kanpur). It is how citation databases attribute the paper to a college, so it must match the official name exactly.

**AICTE** — All India Council for Technical Education, the statutory body that approves technical institutions and programmes in India (engineering, pharmacy, management, computer applications). UNCERTAIN: aicte-india.org refused connections from this network on 2026-11-03, so this entry has no verified URL.

**Annotation** — Labelling data by hand so a model can learn from it or be scored on it, e.g. marking 2,000 tweets as positive, negative or neutral. Who annotated, how many people, and how much they agreed are all reportable facts.

**APC (article processing charge)** — The fee a journal charges the author to make an article open access, always quoted in USD (or the currency the publisher uses) and paid on acceptance, not on submission. It is the single biggest cost of publishing open access, so check the journal's own page before you submit.

**Appendix** — Material placed after the references: full proofs, extra tables, long derivations. It does not count against many page limits, and reviewers are not obliged to read it.

**Area chair (AC)** — The senior researcher who handles a group of submissions at a conference: assigns reviewers, chases late reviews, writes the meta-review, and argues the paper's case at the programme committee meeting.

**arXiv identifier** — The ID of a preprint on arXiv, written as YYMM.NNNNN, e.g. 2405.12345 means a paper first submitted in May 2024 with sequence number 12345 [1]. The same paper can have v1, v2, v3 appended as it is revised.

**Attention** — The mechanism that lets a model weigh different parts of its input when producing each output, instead of squeezing everything into one fixed vector. It is the core operation inside transformers [2].

**Baseline** — The existing method your work is compared against, ideally the strongest published one and not a strawman. A paper that beats only a weak baseline has shown nothing; reviewers ask for the strong baseline by name.

**Batch** — The group of training examples processed before one weight update. Batch size 32 means the model sees 32 examples, averages their errors, and takes one step; it changes speed and stability, not what the model can learn in principle.

**Benchmark** — A fixed dataset plus a fixed metric plus a fixed protocol that many groups report on, so numbers are comparable. MMLU, GLUE and ImageNet are benchmarks; a benchmark is only useful while people trust that nobody trained on its test split.

**Benchmark contamination** — When a model's training data contains the benchmark's test questions, so its score measures memorisation rather than ability. It is hard to detect from outside and is a standard reason to distrust a suspiciously high score.

**BLEU** — A machine-translation score that counts overlapping word sequences between the system output and one or more human references, scaled 0–100 [3]. It rewards literal overlap, so a correct paraphrase can score badly; report it with an example or two.

**Camera-ready** — The final version of an accepted paper, formatted to the publisher's template and delivered by a fixed date. Changes after this point need the publisher's permission, so proofs must be read carefully.

**Citation count** — How many times other papers have cited a work, as counted by one database. The number differs between Google Scholar, Scopus and Web of Science, so always say which one you used and on what date.

**Classification** — Predicting which category something belongs to, from a fixed list (spam / not spam; which of 10 digits is in the image). The output is a label, sometimes with a probability.

**Co-author** — Anyone listed as an author besides the first author, each of whom should have contributed substantially to the work. Guest authorship, where a name is added for status, is misconduct under ICMJE criteria [21].

**Cohen's kappa** — Agreement between two annotators after correcting for agreement that would happen by chance: 0 means chance-level, 1 means perfect. A common rule of thumb is that below about 0.6 the labels are too noisy to build on, but the number to report is the one you measured.

**Confidence interval** — A range around an estimate that shows how much it would move if the experiment were repeated, usually a 95% interval. "F1 = 0.81 [0.79, 0.83]" says the true value is plausibly in that band; a single number without one hides how noisy the result is.

**Conflict of interest (COI)** — Any relationship that could bias a judgement: same institution, recent co-authorship, a shared grant, a financial stake. Reviewers and ACs declare these and are reassigned, and authors declare funding on the paper.

**Confound** — A hidden variable that changes along with the thing you are testing, so you cannot tell which caused the effect. If every model you compare was also trained on different data sizes, data size is a confound.

**Control condition** — The comparison setup that isolates the variable you changed: same data, same code, same seed, one thing different. Without a control, an improvement could come from anywhere.

**Copyright transfer** — The agreement by which authors hand the publisher the right to distribute the paper, usually signed at acceptance. It is why you often cannot post the publisher's PDF on your own site, but can post the accepted manuscript.

**CORE rank** — A ranking of computing conferences by CORE (Computing Research and Education), in four tiers A*, A, B, C; its portal listed 825 ranked venues when checked on 2026-11-03 [12]. Not the same thing as CORE, the open-access aggregator at core.ac.uk.

**Corresponding author** — The author who handles all communication with the journal or conference, and whose email is printed on the paper. Usually the senior author or the student who will answer reviewer questions.

**Data leakage** — When information the model would not have at prediction time sneaks into training, inflating results. Fitting a scaler on the full dataset before splitting, or letting the test set influence model choice, are the two classic forms.

**Dataset** — The collection of examples an experiment runs on, with a documented source, size and licence. "We used 12,480 product reviews from the public X corpus, split 80/10/10" is a dataset description; "we used some reviews" is not.

**Desk reject** — Rejection by the editor or programme chair before any reviewer sees the paper, usually for scope, length, formatting, or a missing ethics statement. It costs days, not months.

**Discussion** — The section that interprets the results: what they mean, why they might be happening, how they compare with prior work, and what follows. It is where you are allowed to speculate, provided you label it as speculation.

**Distribution shift** — When the data at use time differs from the data at training time, e.g. a model trained on 2021 reviews deployed on 2026 slang. Performance usually drops, and the size of the drop is itself a result worth reporting.

**DOI** — Digital Object Identifier, a permanent ID for a published object, written as 10.prefix/suffix (e.g. 10.1145/3290605.3300233) and resolvable at doi.org [10]. Use the DOI, not a URL, when citing: URLs rot, DOIs are redirected forever.

**DORA (San Francisco Declaration on Research Assessment)** — A declaration, now signed by thousands of organisations, arguing that researchers and papers should be judged on their content rather than on journal-level metrics such as the impact factor [23].

**Double-blind, single-blind and triple-blind review** — Double-blind hides author names from reviewers (and reviewer names from authors); single-blind hides only the reviewer; triple-blind also hides names from the area chair. CS conferences mostly use double-blind, which is why you write "our prior work [7]" instead of "our prior work".

**Effect size** — How big the difference is, in interpretable units, rather than whether it is statistically detectable. "+6.2 F1 points over the baseline" or "Cohen's d = 0.4" are effect sizes; "p < 0.001" is not.

**Embargo** — A period after publication during which the article cannot be freely read, set by the publisher's policy and often running to many months. It usually applies to the publisher's final PDF, not to a preprint you posted before submission.

**Embedding** — A list of numbers (a vector) that represents a word, sentence or image, positioned so that similar things are close together. A 768-number embedding is a common size for a transformer's internal representation.

**Epoch** — One complete pass over the training data. "Trained for 30 epochs" means the model saw every training example 30 times; too few underfits, too many overfits.

**Erratum** — A short publisher notice correcting an error in a published paper, linked to the original. It keeps the record honest; a retraction is the stronger step taken when the findings themselves cannot be trusted.

**Error analysis** — Reading the individual cases your system got wrong and sorting them into categories, then reporting the counts. Twenty misclassified examples grouped into five causes usually teaches more than the aggregate score.

**Evaluation metric** — The number you use to compare systems, chosen before the experiments and defined precisely in the paper. Different metrics can reverse the ranking of two systems, so the choice is an argument, not a detail.

**F1 score** — The harmonic mean of precision and recall, so a system cannot win by maximising one and ignoring the other. It is the usual headline metric when classes are imbalanced.

**Fairness and bias** — Systematic differences in a model's behaviour across groups of people or inputs, e.g. higher error rates for one dialect. It is measured by reporting metrics per subgroup, and it is a property of the data and the deployment, not only of the model.

**Few-shot and zero-shot** — Zero-shot means the model handles a task with no examples in the prompt; few-shot means you put a handful (typically 2–10) of worked examples in the prompt. Neither involves changing the model's weights.

**Fine-tuning** — Further training of a pretrained model on your own smaller dataset so it adapts to your task. It is cheaper than training from scratch and risks destroying general ability if overdone.

**First author** — The person listed first, conventionally the one who did most of the work and wrote the draft. In most Indian and international evaluation, first authorship is the credit that counts most for a student.

**Generalisation** — Performance on data the model has never seen. A model that scores 99% on its training set and 61% on new data has memorised rather than learned, and only the second number is a result.

**Gold and green open access** — Gold means the publisher makes the final article free immediately, usually paid by an APC; green means the author deposits a version in a repository, often after an embargo. Gold is paid for, green is free but usually not the typeset PDF.

**Gradient descent** — The optimisation loop that adjusts a model's weights a small step at a time in the direction that reduces the loss. Every deep-learning model you will meet is trained by some variant of it.

**h5-index** — The h-index of a venue, computed only over the papers it published in the last five complete years [5]. It is the fairest single number for comparing venues of different ages.

**Hallucination** — When a language model states something false in confident, fluent prose, e.g. an invented citation with a plausible title and author list. It is the main reason AI-generated references must be checked one by one against a real database.

**h-index** — The largest number h such that h of your papers have at least h citations each: 10 papers with 10 or more citations gives h = 10 [4]. It rewards both volume and impact, and it never goes down, which is why it favours long careers.

**Hyperparameter** — A setting chosen before training rather than learned during it: learning rate, batch size, number of layers, dropout. Your choices must be listed in the paper, or nobody can reproduce the result.

**Hyperparameter search** — The systematic search over those settings (grid, random, or Bayesian), run on the validation set and never on the test set. Searching on the test set is a form of data leakage and quietly inflates the final number.

**Hypothesis** — A specific, falsifiable statement you test, e.g. "adding a retrieval step improves answer accuracy by at least 3 points on our dev set". If no possible result could show it false, it is not a hypothesis.

**i10-index** — The number of your papers that have at least 10 citations, a figure Google Scholar displays next to the h-index [5]. It is common in Indian academic CVs because it is simple to read.

**Impact factor** — A journal-level average citation measure published by Clarivate in the Journal Citation Reports, computed from citations to that journal's recent articles [25]. It says nothing about any single paper: a mediocre paper in a high-impact journal borrows a reputation it has not earned.

**Introduction** — The first section: what the problem is, why it matters, why it is hard, what others have done, and what you did. A good introduction ends with a bulleted list of contributions, which doubles as the outline of the paper.

**IQAC (Internal Quality Assurance Cell)** — The office inside an Indian college that maintains the documents and data used at accreditation time, and submits the college's Annual Quality Assurance Report. NAAC publishes the guideline for creating one [15]. For publication numbers, this is the office to ask.

**ISBN and ISSN** — An ISBN identifies a specific book; an ISSN identifies a serial publication such as a journal, in the form 1234-5678, and stays the same for every issue [20]. A journal has an ISSN; the conference proceedings volume has an ISBN.

**Journal** — A periodically published venue that reviews submissions and prints accepted articles in volumes and issues. Review cycles are typically 3–12 months, and journals usually allow resubmission after revision, unlike conferences.

**Lab** — A research group's physical and organisational home: a room, a set of machines, a weekly meeting and a shared budget. "Joining a lab" as a student usually means attending its reading group and helping with an existing project.

**Learning rate** — The size of each step in gradient descent, often around 1e-4 to 1e-3 for fine-tuning and smaller for large models. Too high and the loss jumps around; too low and training takes forever.

**Licence (CC BY)** — Creative Commons Attribution: anyone may copy, reuse and even sell the work as long as they credit the authors [6]. Most open-access papers use CC BY, and reusing a figure from one still requires the citation.

**Limitations** — A short, honest section saying where the method fails, on what data, and why. Reviewers look for it: a paper that claims no limitations is read as either naive or hiding something.

**LLM (large language model)** — A neural network trained on very large text corpora to predict and generate text, such as the GPT, Claude, Gemini and Llama families. It produces plausible text; it does not check facts unless you build the checking.

**Loss function** — The number the training loop minimises, which defines what "good" means: cross-entropy for classification, mean squared error for regression. Choosing the loss is choosing what the model optimises, which is not always what you care about.

**Meta-review** — The area chair's summary of the reviews and the decision reasoning, sent to authors with the reviews. It matters as much as the individual scores, because it is the argument the AC will make to the committee.

**Method** — The section that describes what you did in enough detail that a competent reader could redo it: data, model, training setup, hyperparameters, and the exact procedure. Vague methods are the most common cause of a reproducibility failure.

**NAAC** — National Assessment and Accreditation Council, set up in 1994 as an autonomous institution of the UGC and based in Bengaluru, which accredits Indian higher-education institutions and grades them [14]. Its grade is one reason a college cares about publication counts.

**NIRF** — National Institutional Ranking Framework, the Ministry of Education's annual ranking of Indian institutions by teaching, research, graduation outcomes and outreach [13]. Research output is one of its inputs, so colleges track it.

**Notification date** — The date on which authors are told the decision (accept, reject, revise). It is fixed in the call for papers and is the date to plan your next semester around.

**Null hypothesis** — The assumption of no effect or no difference, used as the baseline for a statistical test. A small p-value means the data would be unlikely under this assumption, which is not the same as proving your own hypothesis.

**Open access** — Free to read without a subscription. It is a property of the specific article and licence, not of the journal's reputation, and it usually costs money somewhere in the chain (an APC, an institutional agreement, or a repository deposit).

**OpenAlex ID** — OpenAlex's identifier for a work, author, venue or institution, written with a leading letter (W for works) and resolvable at openalex.org [9]. It is free and open, which makes it the basis of many literature tools.

**ORCID** — A free, persistent identifier for a researcher, 16 digits in four groups, e.g. 0000-0002-1825-0097, that distinguishes you from everyone with a similar name [7]. Register before your first submission; it takes two minutes and follows you between institutions.

**Overfitting** — When a model learns the training examples and their noise instead of the pattern, so training accuracy rises while validation accuracy falls. The usual signs are a widening gap between the two curves and results that vanish on new data.

**Perplexity** — How surprised a language model is by a piece of text, reported as a number where lower is better: perplexity 20 means the model is about as uncertain as a fair choice among 20 equally likely next tokens. It is only comparable between models that use the same tokenizer, which is why it is a weak way to compare papers.

**PI (principal investigator)** — The senior researcher who holds the grant and leads the project, usually the advisor on a student's work. "The PI's lab" is shorthand for the group and its funding.

**Plagiarism** — Presenting someone else's words, ideas, figures or code as your own, whether or not you meant to. It includes copying a paragraph and changing a few words, and it is checked by similarity tools such as Turnitin and iThenticate [19].

**Precision and recall** — Precision is the fraction of your positive predictions that were right; recall is the fraction of real positives you found. Reporting both is mandatory when positives are rare, because the two trade off against each other.

**Predatory journal** — A journal that charges a fee, promises publication in days, and runs no real peer review, existing mainly to sell authors a publication. Warning signs: a wide scope, an editorial board you cannot verify, an email invitation, and a fee quoted before review.

**Preprint** — A paper posted publicly before peer review, on a server such as arXiv. It establishes priority and gets you read, but it is not peer reviewed and should never be cited as if it were.

**Preprint server** — A website that hosts preprints with a permanent ID and versions, e.g. arXiv for physics, maths and computer science. Posting usually needs an endorsement from an existing author in some categories [24].

**Proceedings** — The published collection of the papers accepted at a conference, with its own ISBN or DOI, published after the event. "In the proceedings of X" is the citation form.

**Proceedings chair** — The organiser responsible for producing the proceedings volume: collecting camera-ready files, checking formatting, and working with the publisher. A thankless role, and a way for a young researcher to see the inside of a conference.

**Prompt** — The instruction or text you give a language model. Small changes in wording can move accuracy by tens of points, which is why prompt text belongs in the paper's appendix if it is part of the method.

**PubPeer** — A site where anyone can post comments on a published paper after publication, usually flagging image duplication or statistical problems [17]. A paper with unanswered comments there is a citation risk.

**p-value** — The probability of getting data at least as extreme as yours if the null hypothesis were true. It is NOT the probability that your hypothesis is true, and p > 0.05 does not mean "no effect" — it means the data are compatible with no effect [16].

**Random seed** — The number that fixes all the randomness in an experiment (initialisation, shuffling, dropout), so a run can be repeated exactly. Report it, and report at least three seeds with mean and spread, because a single run's 0.4-point gain is often noise.

**Rebuttal (author response)** — The authors' short reply to the reviews, correcting misunderstandings and answering specific questions within a word limit. It rarely reverses a strong reject but often moves a borderline paper, so answer the factual points first and politely.

**Regression** — Predicting a number rather than a category, e.g. next month's sales or a house price. The output is continuous, and the usual metrics are error-based (MAE, RMSE).

**Related work** — The section that places your paper among existing work, grouped by approach rather than listed one paper at a time. Its job is to show you know the field and to make your contribution visible by contrast.

**Replication** — Re-running someone else's experiment, ideally with new data or a fresh implementation, to see whether the finding holds. It is a legitimate contribution and much rarer than it should be.

**Reproducibility** — Getting the same numbers from the same code and data; reproducibility is code plus data plus environment plus seeds. It is weaker than replicability, which is a new study reaching the same conclusion.

**Research group** — A set of researchers who work on related problems under one or two senior people, meeting weekly and sharing code. For a student, the group's reading group is the cheapest way in.

**Results table** — The table of numbers comparing your method with baselines on each dataset and metric, usually with means over runs and some measure of spread. It is the part reviewers read second, after the abstract, so it must be readable without the text.

**Retraction** — A publisher's withdrawal of a published paper because its findings are unreliable, usually after an investigation. Retractions are indexed and follow the authors, which is why fabrication is career-ending rather than merely embarrassing.

**Reviewer** — A researcher, usually unpaid, who reads a submission and writes an assessment of its quality, clarity, originality and significance [22]. Reviewers are typically volunteers with several papers to do in a few weeks, which is why clarity pays.

**Reviewer score** — The numeric rating a reviewer gives, e.g. 1–10 or 1–5, often alongside confidence and a recommendation. Scores are inputs to discussion, not the decision: an AC can accept a paper with a 4 if the argument is strong.

**ROR ID** — A free identifier for a research organisation, e.g. ror.org/02mhbdp94 for Universidad de Los Andes, used so that institution names can be matched despite spelling variants [8]. Useful when asking how many papers a college really published.

**Scopus** — Elsevier's abstract and citation database, one of the two indexes Indian institutions usually mean by "indexed" [18]. Being in Scopus is a binary fact you can check on the journal's page; citation counts from Scopus differ from Google Scholar's.

**Self-citation** — Citing your own earlier papers. Some is normal and necessary; a pattern of inflating counts this way is visible in the data and is treated as a red flag, especially when the cited work is irrelevant.

**Self-plagiarism** — Reusing your own previously published text, figures or results without saying so, so that readers think it is new. Reusing your own method description is usually fine if you cite and quote it; republishing the same result twice is not.

**Self-supervised learning** — Training on unlabelled data by hiding part of the input and asking the model to predict it, so the data labels itself. It is how most large language models are pretrained, before any task-specific fine-tuning.

**SOTA (state of the art)** — The best published result on a benchmark at a given time. Claiming SOTA requires a dated comparison against every relevant published number on the same split and metric; the claim goes stale within months and is the easiest thing for a reviewer to disprove.

**Special issue** — An issue of a journal devoted to one topic, with its own call for papers, guest editors and deadline. They are often easier to enter for a first paper, but check that the guest editors are real people with real records.

**Statistical significance and practical significance** — Statistical significance says the difference is unlikely to be chance; practical significance says the difference is large enough to matter. With enough data, a 0.1-point gain can be statistically significant and still useless, so report the effect size and the interval.

**Student volunteer** — A student who helps run a conference (registration desk, session timing) in exchange for free registration and access to the talks. It is the cheapest way for an undergraduate to attend an international conference.

**Supervised learning** — Training on labelled examples, where each input comes with the correct answer. It is the default setting for classification and regression, and it is limited by how much labelled data you can afford.

**Supplementary material** — Extra files submitted with the paper but not printed in it: code, data, long appendices, videos. Reviewers may or may not read it, so nothing essential should live only there.

**Token** — The unit a language model reads and writes: roughly a word or part of a word, about 0.75 words in English. A 1,000-token budget is roughly 750 words, which is why prompts and context windows are measured in tokens.

**Train/validation/test split** — Three parts of the data: train to fit, validation to choose settings, test to report once. Touching the test set more than once turns it into a validation set and your final number becomes optimistic.

**Transformer** — The neural architecture built from attention layers that underlies nearly all modern language models [2]. Its key property is that it processes a whole sequence in parallel instead of one step at a time.

**Travel grant** — Money from a conference, a society or your institution to cover part of the cost of attending. Applications usually open months before the event and are far more likely to succeed for authors of accepted papers.

**Turnitin and iThenticate** — Commercial text-similarity services; Turnitin is used by institutions for student work, iThenticate by publishers and researchers before submission [19]. They report overlap with existing text, which a human then has to interpret: a high score can come from a correctly quoted passage.

**UGC-CARE** — The Consortium for Academic and Research Ethics list of vetted journals, used by Indian universities to judge publication quality. The portal states that the list has not been updated since October 2024 and will not be updated further, per a UGC public notice dated 11 February 2025 [11].

**Unsupervised learning** — Finding structure in data with no labels: clustering, dimensionality reduction, anomaly detection. It is used when labels are expensive or unknown, and its results are harder to evaluate objectively than a labelled task.

**Version (v1, v2)** — Preprints and some journal articles are versioned: v1 is the first posting, v2 the first revision, each with its own date on the abstract page. Cite the version you actually read, because the numbers can change between versions.

**Web of Science** — Clarivate's citation index, the other database Indian institutions usually mean by "indexed", with its own journal list and citation counts [25]. Its coverage is narrower than Scopus and Google Scholar, especially for Indian and regional journals.

**Workshop** — A smaller event attached to a conference, with shorter papers and a narrower topic, usually 4 pages instead of 8. Workshops are the standard first target for an undergraduate: less competitive, faster review, same audience.

---

## Sources

Verified with a live HTTP request on 2026-11-03. "200" means the page loaded; anything else is stated.

1. arXiv, *arXiv Identifier* — https://info.arxiv.org/help/arxiv_identifier.html — retrieved 2026-11-03 (200)
2. Vaswani et al., *Attention Is All You Need* (2017) — https://arxiv.org/abs/1706.03762 — retrieved 2026-11-03 (200)
3. Papineni et al., *BLEU: a Method for Automatic Evaluation of Machine Translation* (ACL 2002) — https://aclanthology.org/P02-1040/ — retrieved 2026-11-03 (200)
4. J. E. Hirsch, *An index to quantify an individual's scientific research output*, PNAS 102(46):16569–16572, 2005 — https://doi.org/10.1073/pnas.0507655102 — metadata checked through the Crossref API on 2026-11-03; the publisher page itself blocks automated requests
5. Google, *Google Scholar Metrics* — https://scholar.google.com/citations?view_op=top_venues&hl=en — retrieved 2026-11-03 (200)
6. Creative Commons, *Attribution 4.0 International (CC BY 4.0)* — https://creativecommons.org/licenses/by/4.0/ — retrieved 2026-11-03 (200)
7. ORCID — https://orcid.org/ — retrieved 2026-11-03 (200)
8. Research Organization Registry — https://ror.org/ and example record https://ror.org/02mhbdp94 — retrieved 2026-11-03 (200)
9. OpenAlex — https://openalex.org/ — retrieved 2026-11-03 (200)
10. Crossref — https://www.crossref.org/ — retrieved 2026-11-03 (200)
11. UGC-CARE (Consortium for Academic and Research Ethics) — https://ugccare.unipune.ac.in/ — retrieved 2026-11-03 (200; the notice about the list no longer being updated was read on the rendered page)
12. CORE conference ranking portal — https://portal.core.edu.au/conf-ranks/ — retrieved 2026-11-03 (200; page reported 825 ranked venues and the A*/A/B/C shares)
13. NIRF, Ministry of Education — https://www.nirfindia.org/ — retrieved 2026-11-03 (200)
14. NAAC — https://www.naac.gov.in/ — retrieved 2026-11-03 (200; the "established 1994, autonomous institution of the UGC, Bengaluru" text was read on the rendered page)
15. NAAC, *Guidelines for the Creation of the IQAC and submission of AQAR for Affiliated Colleges* (PDF) — https://naac.gov.in/images/docs/AQAR_ONLINE/IQACAQAR_Guideline_Affiliatedcollege-12-03-2020.pdf — retrieved 2026-11-03 (200, PDF; text not machine-readable here, see honesty note below)
16. V. Amrhein, S. Greenland, B. McShane, *Scientists rise up against statistical significance*, Nature, 2019 — https://www.nature.com/articles/d41586-019-00857-9 — retrieved 2026-11-03 (200)
17. PubPeer — https://pubpeer.com/ — retrieved 2026-11-03 (200)
18. Scopus (Elsevier) — https://www.scopus.com/ — retrieved 2026-11-03 (200)
19. Turnitin — https://www.turnitin.com/ and iThenticate — https://www.ithenticate.com/ — retrieved 2026-11-03 (both 200)
20. ISSN International Centre — https://www.issn.org/ and International ISBN Agency — https://www.isbn-international.org/ — retrieved 2026-11-03 (both 200)
21. ICMJE, *Recommendations for the Conduct, Reporting, Editing, and Publication of Scholarly Work in Medical Journals* — https://www.icmje.org/recommendations/ — retrieved 2026-11-03 (200)
22. NeurIPS, *2026 Reviewer Guidelines* — https://neurips.cc/Conferences/2026/ReviewerGuidelines — retrieved 2026-11-03 (200; the guideline text names quality, clarity, originality and significance as the review criteria)
23. DORA, *San Francisco Declaration on Research Assessment* — https://sfdora.org/ — retrieved 2026-11-03 (200)
24. arXiv, *Endorsement* — https://info.arxiv.org/help/endorsement.html — retrieved 2026-11-03 (200)
25. Clarivate, *Web of Science platform* — https://clarivate.com/products/scientific-and-academic-research/research-discovery-and-workflow-solutions/webofscience-platform/ — retrieved 2026-11-03 (403 to this client; see honesty note)

## How confident is this?

- **Solid.** Definitions of paper sections, review roles, statistical terms and ML terms are standard usage, and the AI-adjacent ones are checks against the primary sources above (the transformer paper, the BLEU paper, the CC BY deed, the arXiv identifier help page).
- **Solid and dated.** Three facts were read off official pages today and could change: CORE's 825 ranked venues and its A*/A/B/C tiers [12]; UGC-CARE's statement that the list has not been updated since October 2024 and will not be updated further, per a UGC notice of 11 February 2025 [11]; NAAC's founding in 1994 as a UGC body [14].
- **UNCERTAIN — AICTE.** aicte-india.org closed the connection from this network on 2026-11-03 (both https and http, repeated), so the AICTE entry has no verified URL. The description of what AICTE is comes from general knowledge, not from a page I loaded. Re-check it before you rely on it.
- **UNCERTAIN — impact factor and Web of Science.** Clarivate's pages return 403 to automated requests, so [25] was not read. The impact-factor definition given is the conventional one and the JCR is named as its source, but no number or policy in that entry was verified today.
- **UNCERTAIN — IQAC guideline detail.** The NAAC guideline PDF [15] downloaded (200) but its text could not be parsed with the tools on this machine, so the entry describes what the guideline's title and file name state, plus common practice.
- **Mostly number-free on purpose.** I removed fee ranges, typical embargo lengths and current acceptance-rate figures, because those move every year and a stale number is worse than none. Numbers that stayed are either illustrative mechanisms (a 20% venue versus a 25% venue) or facts read off a page today. For money and deadlines, check the venue's own page.
- **Not legal or statistical advice.** Kappa bands and learning-rate ranges are rules of thumb, labelled as such.

last_updated: 2026-11-03
