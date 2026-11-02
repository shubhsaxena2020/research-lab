# Ethics and AI use: what is actually allowed

**What this page is for:** the rules that decide whether a paper is publishable or a liability — who counts as an author, what plagiarism means in 2026, when you need ethics approval, and where AI tools are allowed. Every venue policy below is quoted word-for-word from the live page on 2026-11-03 with its URL, so you can check it. Text in quotation marks is the organisation's sentence, not mine.

## The short version

- An author is a person who did real intellectual work, wrote or revised the text, approved the final version, and will answer for it [14]. AI tools cannot be authors anywhere.
- **arXiv will not take your paper yet.** "Undergraduate or high school research" sits on its list of content types that are typically not accepted [2]. A workshop or student track first; arXiv after a conventional publication.
- Disclosure rules differ. IEEE and ACL want AI use named in the Acknowledgements [5][11]. ACM (rewritten May 2026) wants it in the *methods* only when AI was part of the research, and no longer asks about AI used to write [3]. NeurIPS requires no declaration for pure writing help [8].
- Fabricated references are measurable now: about one in 277 PubMed-indexed papers in early 2026 cited a paper that does not exist, up from one in 2,828 in 2023 [15].
- The rule that satisfies every venue at once: **if you cannot explain a sentence you wrote, delete it.**

---

## 1. Who is an author, and who is not

### The four criteria everyone borrows

The ICMJE standard, which most fields now copy. All four must hold:

> "Substantial contributions to the conception or design of the work; or the acquisition, analysis, or interpretation of data for the work; AND Drafting the work or reviewing it critically for important intellectual content; AND Final approval of the version to be published; AND Agreement to be accountable for all aspects of the work in ensuring that questions related to the accuracy or integrity of any part of the work are appropriately investigated and resolved." [14]

Note what is missing: paying for compute, being the lab head, introducing you to the field, or owning the idea in a corridor conversation. None of those are criteria.

IEEE says the same more compactly — authors must have:

> "made a significant intellectual contribution to the theoretical development, system or experimental design, prototype development, and/or the analysis and interpretation of data associated with the work contained in the article; contributed to drafting the article or reviewing and/or revising it for intellectual content; approved the final version of the article as accepted for publication, including references." [6]

ACM adds the criterion that settles the AI question: an author must be "an identifiable human being" [3].

### Three kinds of fake authorship

- **Gift or guest authorship**: a name added that did not earn it — a senior professor, a department head, a friend. ACM calls this author misrepresentation, listing "the listing of authors who did not participate in a meaningful way in the preparation of the Work" as one form [4].
- **Ghost authorship**: someone writes and is left off, usually a junior student. AI ghostwriting is the 2026 version.
- **Purchased authorship**: paying to be added; ACM names it explicitly as a violation [3].

All three "may have severe consequences for those found to have participated in such practices" [3].

### Order, and the corresponding author

CS mostly orders authors by contribution, with the student who did the work first; some theory groups go alphabetical; physics-style labs put the senior person last. There is no universal rule, so **agree the order in writing before you start writing**. At ICML it freezes early: "The author list cannot be changed after the abstract deadline." [9]

The corresponding author is the single contact with the editor. IEEE lists the extra duties: including "as co-authors all persons appropriate and none inappropriate", collecting everyone's assent and approval of the final version, and keeping co-authors informed [6]. If you are first author and the only one who understands the code, that is usually you — answering reviewer email at 2 a.m., not your guide.

### If a faculty member asks to be added without contributing

1. **Ask what they will contribute, in writing.** "Could you let me know which sections you'd revise, so I can fill in the CRediT roles accurately?" Someone who intends to contribute answers. Someone who wants a free name says "just put me on".
2. **Offer the acknowledgement instead**, and say why: ACM treats listing a non-contributor as misrepresentation [4].
3. **Keep the email thread** in the repo. It is your evidence.
4. **Escalate only if pressured** — to the Head of Department, or by taking the paper elsewhere. A paper you cannot defend is worse than one you did not publish.

A guide who did nothing is your liability too. Every author certifies they are "responsible and accountable for any issues relating to the correctness or integrity of the Work" [3]. If that guide later turns out to have copied a paragraph, your name is on the retraction notice beside theirs.

### AI is not an author, anywhere

> "AI tools cannot meet the requirements for authorship as they cannot take responsibility for the submitted work. As non-legal entities, they cannot assert the presence or absence of conflicts of interest nor manage copyright and license agreements." — COPE [13]

> "Chatbots (such as ChatGPT) should not be listed as authors because they cannot be responsible for the accuracy, integrity, and originality of the work, and these responsibilities are required for authorship." — ICMJE [14]

> "generative AI language tools should not be listed as an author; instead authors should refer to (1)." — arXiv [1]

ICMJE's next sentence is the one to remember: "humans are responsible for any submitted material that included the use of AI-assisted technologies" [14]. No tool configuration changes that.

### The 17-year-old problem

- **arXiv does not want undergraduate work.** "Undergraduate or high school research" sits among "Content types that are typically NOT accepted", next to course projects and "Proposals for future research" [2]. Post after a workshop or conference has accepted the work.
- **You are legally a child until December 2026.** The DPDP Act defines a "child" as "an individual who has not completed the age of eighteen years" [24], and Section 9(1) requires "verifiable consent of the parent" before processing a child's personal data. Run a survey yourself and your own responses are children's data — so are your classmates'.

---

## 2. The venue policies, quoted

| Venue | AI as author | Where to disclose | Writing help needs disclosure? |
|---|---|---|---|
| arXiv | No [1] | In the paper, as a method/tool [1] | Yes, if "significant" [1] |
| ACM | No — must be human [3] | Methods, only if AI was part of the research [3] | No longer required [3] |
| IEEE | No, by the authorship criteria [6] | Acknowledgements [5] | Recommended, not required [5] |
| NeurIPS | No [7] | Experimental setup if it is a core component [7]; checklist 16 [8] | Not required [8] |
| ICML | No [9] | "Explain any notable ways" — encouraged [9] | Encouraged |
| ACL | No [11] | Acknowledgements [11] | Yes, "fully disclosed" [11] |
| COPE (journals) | No [13] | Materials and Methods [13] | Yes |

### arXiv

arXiv is a preprint server, but its moderation decides whether your work exists publicly at all:

> "continue to require authors to report in their work any significant use of sophisticated tools, such as instruments and software; we now include in particular text-to-text generative AI among those that should be reported consistent with subject standards for methodology." [1]

> "by signing their name as an author of a paper, they each individually take full responsibility for all its contents, irrespective of how the contents were generated. If generative AI language tools generate inappropriate language, plagiarized content, biased content, errors, mistakes, incorrect references, or misleading content, and that output is included in scientific works, it is the responsibility of the author(s)." [1]

**For you:** draft a paragraph with an LLM, leave a wrong number in it, and arXiv's position is that *you* wrote it. Its moderation standard is about content, not credentials: a submission "may be declined if the moderators determine it lacks originality, novelty, significance, and/or contains falsified, plagiarized content or serious misrepresentations of data, affiliation, or content" [1].

### ACM

ACM rewrote its policy on 14 May 2026 and moved opposite to most venues:

> "When using Artificial Intelligence to conduct research, including the design and methodology of the research project, creation and selection of data sources, designing experiments, generation and collection of data, coding, implementing models, running simulations, data analysis, testing, validating results, deploying software, archiving data and code for reproducibility, or any other aspects of the research lifecycle that are directly relevant to the conclusions of the research underlying the Work, the specific use(s) of AI tools must be described in detail in the methods section of the Work." [3]

> "When using Artificial Intelligence to assist with writing an ACM submission, ACM no longer requires the disclosure of information regarding the use of AI (as distinct from AI used in the conduct of the research itself, addressed in item 1 above)." [3]

**For you:** ACM has decided AI-written prose is not by itself an integrity problem; an AI-written *result* is. Many university handouts still describe the 2023–2024 rule ("disclose in acknowledgements") — that is out of date. ACM can still retract: if issues "are identified after publication or posting in the ACM Digital Library, ACM reserves the right to retract the published Work in its entirety" [3].

### IEEE

> "The use of content generated by artificial intelligence (AI) in an article (including but not limited to text, figures, images, and code) shall be disclosed in the acknowledgments section of any article submitted to an IEEE publication. The AI system used shall be identified, and specific sections of the article that use AI-generated content shall be identified and accompanied by a brief explanation regarding the level at which the AI system was used to generate the content." [5]

> "The use of AI systems for editing and grammar enhancement is common practice and, as such, is generally outside the intent of the above policy. In this case, disclosure as noted above is recommended." [5]

**For you:** IEEE wants the tool named ("ChatGPT (GPT-5.2), accessed 12 October 2026"), the sections named, and the level described. "I used AI to improve the writing" fails all three.

### NeurIPS

> "We expect authors to document their methodology clearly for upholding scientific rigorousness and transparency standards. The use of agents and/or LLMs in implementing the method should be described in the experimental setup section (or equivalent) if it is an important, original, or non-standard component of the approach e.g. if the paper is about using an LLM as a search heuristic. The use of spell checkers and grammar suggestions, aid for editing purposes, and basic code assistance does not need to be documented." [7]

> "There have been many cases of hallucinated citations in literature review, which violates the NeurIPS Code of Conduct. It is the author's responsibility to verify the tools are used in a scientifically responsible manner. Relatedly, as you are the one taking responsibility for the work, agents and LLMs cannot be authors." [7]

The mandatory checklist, item 16:

> "Does the paper describe the usage of LLMs if it is an important, original, or non-standard component of the core methods in this research? Note that if the LLM is used only for writing, editing, or formatting purposes and does not impact the core methodology, scientific rigorousness, or originality of the research, declaration is not required." [8]

**For you:** the most permissive of the big three on writing, the most explicit that hallucinated citations are a conduct violation. If an LLM sits inside your pipeline, name the model and version in the experimental setup. Omit the checklist and the paper is desk-rejected [8].

### ICML

> "Authors are allowed to use generative AI tools such as Large Language Models (LLMs) to assist in writing or research. However, authors must take full responsibility for all content in their paper, including any content generated by AI tools that might be construed as plagiarism or scientific misconduct. We encourage authors to explain any notable ways in which these tools were used in their research methodology. LLMs are not eligible for authorship." [9]

**For you:** note "encourage", not "must". ICML also runs an ethics review: reviewers may flag submissions, and "in extreme cases papers may be rejected by the program chairs on ethical grounds, regardless of scientific quality or contribution" [9].

### ACL

> "Generative AI tools and technologies may not be listed as authors of a submission, and any use of generative AI tools and technologies to create content, whether to support research or in review rebuttals, should be appropriate and should be fully disclosed in the Acknowledgements section - for instance, "Section 3 was written with inputs from ChatGPT."" [11]

ACL then lists permitted uses and closes with "Any use not listed below is considered inappropriate use." [11] Permitted: language polishing and predictive typing (no disclosure), literature search, low-novelty text about existing ideas (disclose, show citations were checked), and model output as a source of ideas you develop yourself (disclose). "New ideas + new text" is where it stops — a generative model is not "an entity that can fulfill the requirements of co-authorship" [11]. Every ARR submission must also answer checklist question E1 on AI use, and vague answers can lead to desk rejection [12].

### COPE (journals with no policy of their own)

> "Authors who use AI tools in the writing of a manuscript, production of images or graphical elements of the paper, or in the collection and analysis of data, must be transparent in disclosing in the Materials and Methods (or similar section) of the paper how the AI tool was used and which tool was used. Authors are fully responsible for the content of their manuscript, even those parts produced by an AI tool, and are thus liable for any breach of publication ethics." [13]

---

## 3. Plagiarism, self-plagiarism, and the boring ways people get caught

> "IEEE defines plagiarism as the use of someone else's work (for example, use of text, prior ideas, processes, results, or algorithms) without explicitly acknowledging the original author and/or source. Plagiarism in any form is unacceptable and is considered a serious breach of professional conduct, with potentially severe ethical and legal consequences." [6]

Three things people miss. It covers **ideas**, not just words. It covers **results and algorithms**, so re-implementing a method and presenting it as new is covered. And it is not limited to copy-paste: ACM lists "verbatim copying, near-verbatim copying, or intentionally paraphrasing portions of another's work" [4], plus:

> "using automated tools that rephrase existing work as one's text without proper attribution" [4]

That is: running a paper through a paraphraser and pasting the output is plagiarism under ACM's definition, whether or not a similarity checker notices.

### Self-plagiarism and text recycling

> "Self-plagiarism is defined as the verbatim or near-verbatim reuse of significant portions of one's own published work without citing the original source." [4]

The same policy says it "does not apply… if an explicit and appropriate reference is made to that prior publication" [4]. Reusing your own text is not automatically misconduct; reusing it *silently* is. The research term is text recycling:

> "Text recycling is the reuse of textual material (prose, visuals, or equations) in a new document where (1) the material in the new document is identical to that of the source (or substantively equivalent in both form and content), (2) the material is not presented in the new document as a quotation (via quotation marks or block indentation), and (3) at least one author of the new document is also an author of the prior document." [20]

The student version: reusing your own **method description** across two papers is normal with a citation. Reusing your **results section** to pad a second paper is not. Reusing a **thesis chapter** in a conference paper is common in India and usually acceptable *if* the venue allows prior publication and you cite the thesis — check, because many CS venues treat a published thesis as prior publication.

### Salami slicing and figures

Salami slicing is cutting one study into the smallest publishable units to get three papers from one. The test: does each paper stand alone with its own question, or does a reader need the other two? It is also a dual-submission risk — ICML forbids submissions "identical, or substantially similar, to versions that have been previously published" [9], and IEEE requires you to "disclose whether there are prior publications… that are similar" and state "how the new submission differs" [6].

Figure reuse follows the same logic. Your own earlier figure needs a citation. Someone else's needs permission *and* a citation, because copyright sits with the publisher: CC BY figures can be reused with attribution, CC BY-NC ones cannot go into a commercially published paper without permission. And do not retouch a plot to make it look better — IEEE lists "image manipulation: Excessive or inappropriate adjustment of an image that alters the scientific meaning of the image" beside fabrication and falsification [6].

### The tools

**iThenticate** is the publisher-side checker, "designed for academic researchers, publishers, institutions", comparing a document against 244 million items and content from 1,500 publishers via Crossref, plus ProQuest theses; AI-writing detection is "a paid add-on" [21]. **Turnitin** is the student-side version with the same engine.

Two warnings. A similarity score is not a verdict: 22% can be all references and method boilerplate, and 4% can hide one stolen paragraph. Editors read the report; they do not sort by number. And AI detectors are noisy in both directions — Turnitin's own description admits the indicator flags "content that may have been paraphrased or bypassed using a text spinner or humanizer" [21], which is a statement about uncertainty.

**UNCERTAIN:** whether PSIT subscribes to Turnitin or iThenticate, or what threshold it uses. No public PSIT document states either; ask the library.

---

## 4. Data, consent, and ethics review

### When you need approval

You need an ethics committee review (an IRB in the US, an IEC in India) when research involves **human participants**: surveys, interviews, user studies, A/B tests on people, human annotation, or data that identifies individuals.

> "if the research presented involves direct interactions between the researchers and human participants or between a technical system and human participants, authors are required to follow existing protocols in their institutions (e.g. human subject research accreditation, IRB) and go through the relevant process. In cases when no formal process exists, they can undergo an equivalent informal process (e.g. via their peers or an internal ethics review)." [7]

ICML accepts that standards differ by country but still wants evidence of "the authors' home institution's procedures for obtaining IRB approval or… an exemption" [10].

**For you:** if PSIT has no committee for student projects (likely — I could not verify either way), the substitute is a written protocol reviewed by your guide, a documented consent script, and a sentence in the paper saying no formal board exists and what you did instead. NeurIPS explicitly allows that [7]. Do not skip the consent script because the board is missing.

### Informed consent

Consent must be informed, specific and revocable: what you are studying, what the participant does, how long it takes, what you store, who sees it, that they can stop, and how to withdraw afterwards.

> "Any paper that chooses to create a dataset with real data of real people should ask for the explicit consent of participants, or explain why they were unable to do so." [7]

Under 18, add parental consent: DPDP Section 9(1) requires "verifiable consent of the parent" before processing a child's data [24].

### Public data is not automatically "no ethics needed"

The distinction is **identifiability**, not whether the data was on the internet.

- **Public and non-personal**: abstracts, arXiv metadata, Wikipedia dumps, published benchmarks, government statistics. No consent; cite the source and licence.
- **Public but personal**: Reddit posts with usernames, tweets, public profiles, app reviews with names. Public *and* personal. Usually needs review, and always needs anonymisation.
- **Private**: chats, emails, medical records, marks. Consent and review required. Not a first-paper dataset.

ACL's checklist asks directly whether you "discussed the steps taken to check whether the data… contains any information that names or uniquely identifies individual people" [12]. One true paragraph is enough.

### Dataset licences

| Licence | Allowed | The trap |
|---|---|---|
| **CC BY 4.0** | Use, modify, redistribute, commercially, with attribution | Credit the creator and say if you changed it — in the caption, not only the reference list |
| **CC BY-NC 4.0** | Same, but "You may not use the material for commercial purposes" [22] | A commercially published paper may need separate permission for the figure |
| **"Research only"** | Only what the text says | Derivatives usually inherit the restriction; check before releasing a model trained on it |
| **No licence** | Technically all rights reserved | Email the authors or pick another dataset. "It was on GitHub" is not a licence |

NeurIPS is explicit that this is your problem: "authors must respect the terms of datasets that have defined licenses (e.g. CC 4.0, MIT, etc)" [7].

### GDPR, briefly

The GDPR covers "any information relating to an identified or identifiable natural person", where identifiable includes "an identifier such as a name, an identification number, location data, an online identifier" [23]. It reaches you if you process data of people in the EU or work with an EU institution. Practically: a lawful basis (usually consent), a stated purpose, data minimisation, and nothing published that lets a reader re-identify a participant. "The data was public" is not an exemption.

### DPDP Act 2023, briefly

Two sections decide most student cases. Section 3(c)(ii) excludes personal data "made or caused to be made publicly available" by the person themselves — which is why scraping public posts is grey rather than automatically illegal. Section 9(1) requires verifiable parental consent for a child's data, and "child" means under 18 [24]. Collect data from your batchmates and you need parental consent, not just theirs. **UNCERTAIN:** the commencement status of individual provisions on 2026-11-03; I did not verify which are in force, and the rules were still being phased in during 2026.

---

## 5. Why fabricated citations and fake results end careers

This is measurable, not hypothetical. An audit published as a letter to *The Lancet* in May 2026 screened 97.1 million references from 2.5 million biomedical papers and found 4,046 fabricated references across 2,810 papers. The rate rose from about one paper in 2,828 in 2023, to one in 458 in 2025, to **one in 277 in the first seven weeks of 2026**; over 98% of the affected papers had seen "no publisher action" [15]. That last number is the trap — it makes the practice feel safe right until it is not.

**Case 1 — six hallucinated citations (2026).** A paper in *Disability Studies Quarterly* appeared in March 2026. Two weeks later a reader emailed to report being cited in it for a paper they had never written. The editor audited all 117 footnotes and found "a total of six citations that appeared to be AI hallucinations"; all six had been added *after* the first peer review. The journal retracted the article and the editor personally emailed each of the six scholars falsely cited [16]. The author had not used AI to write — only to search for "additional scholarship", and the names "made sense together" [16]. That is exactly how it happens: not laziness, but not opening the DOI.

**Case 2 — AI figures in a biology paper (2024).** A paper in *Frontiers in Cell and Developmental Biology* appeared on 13 February 2024 with figures readers spotted as AI-generated within hours. The retraction notice reads:

> "Following publication, concerns were raised regarding the nature of its AI-generated figures. The article does not meet the standards of editorial and scientific rigor for Frontiers in Cell and Developmental Biology; therefore, the article has been retracted." [17]

Frontiers added the detail that matters: "one of the reviewers raised valid concerns about the figures and requested author revisions. The authors failed to respond to these requests." [18] The reviewers did their job; the authors ignored them.

**Case 3 — refusing to share data (2026).** In September 2026 the APA journal *Technology, Mind, and Behavior* retracted a paper on generative AI and user confidence after the sole author refused to share data. It had been covered by *TIME*; PubPeer concerns included "inconsistencies in graphs and results, study design, 'erroneous' references and a lack of ethics approval" [19]. Attention is not protection — it is what brings the checkers.

### The mechanism

1. A reviewer tries to open your citation, and the DOI 404s. One 404 is enough.
2. Post-publication review: PubPeer lets anyone comment permanently, usually within days; ACL, NeurIPS and ICML papers are discussed on OpenReview within hours.
3. Retraction Watch writes it up — that is the version that appears when someone searches your name for the next ten years.
4. The institution is notified. ACM may contact "the violator's employer" [4]; NeurIPS lists "informing the colluding parties home institutions" among its penalties [7]. For a student that means your college, your guide, and eventually an admissions committee.
5. The notice stays attached to the DOI and your ORCID. It does not get deleted; it gets cited.

A fabricated citation saves twenty minutes. Getting caught costs the paper, your guide's trust, and a permanent search result. No student has ever needed that trade.

---

## 6. How to use AI without wrecking the paper

| Task | Status | Why |
|---|---|---|
| Brainstorming topics and angles | **Allowed** | Not content; no disclosure anywhere |
| Explaining a concept you do not understand | **Allowed** | Same as asking a senior; verify against a textbook |
| Summarising a paper you have already read | **Allowed, with care** | ACL permits literature search [11]; you cite the paper, not the chatbot, and check the summary against it |
| Writing code for experiments | **Allowed** | NeurIPS: "basic code assistance does not need to be documented" [7]. You must still be able to debug it |
| A first draft of prose | **Grey** | Fine at ACM (no disclosure) [3]; explain at ICML [9]; must be disclosed at IEEE [5] and ACL [11]. Never the final draft |
| Rewriting your own sentences for clarity | **Allowed** | Language polishing; ACL and IEEE both exempt it [11][5] |
| Generating citations | **Not allowed** | NeurIPS calls hallucinated citations a Code of Conduct violation [7]. Generate search terms, never the bibliography |
| Generating results or "expected" numbers | **Not allowed** | That is fabrication [6][4] |
| Rewriting to evade a plagiarism detector | **Not allowed** | ACM names "automated tools that rephrase existing work as one's text without proper attribution" as plagiarism [4] |
| Drafting the reviewer response | **Grey** | ACL includes "review rebuttals" in its disclosure requirement [11]. Draft, then rewrite yourself |

**Keep an AI-use log** from day one. Reconstructing it at submission is impossible and the reconstruction will be wrong.

**Resolve every citation before it enters a draft.** Search the exact title in Crossref, DBLP, Semantic Scholar or arXiv; open the DOI and confirm title, first author, year and venue; save the DOI, URL and retrieval date to `02_literature/verified_citations.csv` (RULES.md already requires this). If it does not resolve in two minutes, delete the sentence that needed it.

**Disclose where the venue asks.** IEEE and ACL: acknowledgements. ACM: methods, research use only. NeurIPS: experimental setup or checklist 16. COPE journals: materials and methods. When unsure, be more specific than required.

**Apply the deletion rule.** If you cannot explain a sentence — why it is there, what it claims, what supports it — delete it. That applies to AI sentences and to ones you wrote at 3 a.m. It is also the test a reviewer applies in the rebuttal.

Do not write to beat a detector. They are noisy, they flag human writing, and the arms race is not winnable. Write so that a human asking "explain this paragraph" gets a good answer from you.

---

## 7. Templates

### Disclosure paragraph (adapt per venue)

> **Use of AI tools.** I used [tool and version, e.g. ChatGPT (GPT-5.2), accessed 2026-10-14] for [specific purpose, e.g. language editing of Sections 2 and 4 / an outline that I rewrote]. All technical claims, citations, results and interpretations are my own, and I verified every reference against the published record. No AI tool generated data, results, figures or references. [Where required: The AI tool is not listed as an author because it cannot take responsibility for the work.]

One-liner for venues that want less:

> "Language editing was assisted by [tool, version, date]; all content and citations were written and verified by the author."

### AI-use log

```
date | tool + version | what I gave it | what I used | where it landed
2026-10-14 | ChatGPT GPT-5.2 | my methods paragraph | grammar only | Sec 3.2, edited by hand
2026-10-15 | Claude Sonnet 4.5 | "difference between precision and recall" | explanation, no text | none (learning)
2026-10-18 | Copilot, VS Code | autocomplete in train.py | boilerplate loop | code/train.py 40-55
```

Two columns people forget: **what you gave it** — never paste a co-author's unpublished draft into a public tool; IEEE treats reviewers doing that as misconduct [5] — and **where it landed**, so you can answer "which sections used AI?" without guessing.

---

## Sources

1. arXiv, "arXiv moderation", https://info.arxiv.org/help/moderation/index.html — retrieved 2026-11-03.
2. arXiv, "Policies for specific content types", https://info.arxiv.org/help/policies/content-types.html — retrieved 2026-11-03.
3. ACM, "ACM Policy on Authorship" (page states "Updated on May 14, 2026"), https://www.acm.org/publications/policies/new-acm-policy-on-authorship — retrieved 2026-11-03.
4. ACM, "ACM Policy on Plagiarism, Misrepresentation, and Falsification" (updated 23 February 2023), https://www.acm.org/publications/policies/plagiarism-overview — retrieved 2026-11-03.
5. IEEE, "Author Guidelines for Artificial Intelligence (AI)-Generated Text", https://open.ieee.org/author-guidelines-for-artificial-intelligence-ai-generated-text/ — retrieved 2026-11-03.
6. IEEE Author Center, "Ethical Requirements", https://journals.ieeeauthorcenter.ieee.org/become-an-ieee-journal-author/publishing-ethics/ethical-requirements/ — retrieved 2026-11-03. (Quotes IEEE PSPB Operations Manual §§8.2.1.A.1 and 8.2.1.B.7.)
7. NeurIPS, "Main Track Handbook", V2026.3, https://neurips.cc/Conferences/2026/MainTrackHandbook — retrieved 2026-11-03.
8. NeurIPS, "NeurIPS Paper Checklist Guidelines", https://neurips.cc/public/guides/PaperChecklist — retrieved 2026-11-03.
9. ICML 2025, "Call For Papers", https://icml.cc/Conferences/2025/CallForPapers — retrieved 2026-11-03.
10. ICML 2025, "Publication Ethics 2025", https://icml.cc/Conferences/2025/PublicationEthics — retrieved 2026-11-03.
11. ACL, "ACL Policy on Publication Ethics" (approved 2024-06-15, revised through 2025-09-26), https://www.aclweb.org/adminwiki/index.php/ACL_Policy_on_Publication_Ethics — retrieved 2026-11-03.
12. ACL Rolling Review, "Responsible NLP Research" checklist, https://aclrollingreview.org/responsibleNLPresearch — retrieved 2026-11-03.
13. COPE, "Authorship and AI tools", https://publicationethics.org/guidance/cope-position/authorship-and-ai-tools — retrieved 2026-11-03.
14. ICMJE, "Defining the Role of Authors and Contributors", https://www.icmje.org/recommendations/browse/roles-and-responsibilities/defining-the-role-of-authors-and-contributors.html — retrieved 2026-11-03.
15. Retraction Watch, "One in 277 PubMed-indexed papers in 2026 shows fabricated references, says analysis", 7 May 2026, https://retractionwatch.com/2026/05/07/one-in-277-pubmed-indexed-papers-in-2026-shows-fabricated-references-says-analysis/ — retrieved 2026-11-03. (Reports Topaz M. et al., "Fabricated citations: an audit across 2.5 million biomedical papers", *The Lancet*, May 2026; I did not open the Lancet letter itself.)
16. Retraction Watch, "Above and beyond: An editor wanted authors to know they'd been falsely cited", 25 September 2026, https://retractionwatch.com/2026/09/25/above-and-beyond-an-editor-wanted-authors-to-know-theyd-been-falsely-cited/ — retrieved 2026-11-03.
17. Frontiers Editorial Office, "Retraction: Cellular functions of spermatogonial stem cells in relation to JAK/STAT signaling pathway", *Front. Cell Dev. Biol.* 12:1386861, 16 February 2024, https://doi.org/10.3389/fcell.2024.1386861 — retrieved 2026-11-03.
18. Frontiers, "Frontiers statement concerning the article 'Cellular functions of spermatogonial stem cells…'", 16 February 2024, https://www.frontiersin.org/news/2024/02/16/frontiers-statement-concerning-the-article-cellular-functions-of-spermatogonial-stem-cells — retrieved 2026-11-03.
19. Retraction Watch, "CEO of AI company loses paper on cognitive impact of generative AI", 14 September 2026, https://retractionwatch.com/2026/09/14/american-psychological-association-technology-mind-behavior-sarah-baldeo-id-quotient/ — retrieved 2026-11-03.
20. Text Recycling Research Project, "What is Text Recycling?" (working definition updated January 2020), https://textrecycling.org/what-is-text-recycling/ — retrieved 2026-11-03.
21. Turnitin, "iThenticate", https://www.turnitin.com/products/ithenticate/ — retrieved 2026-11-03.
22. Creative Commons, "Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)", https://creativecommons.org/licenses/by-nc/4.0/ — retrieved 2026-11-03.
23. GDPR, Article 4 definitions, https://gdpr-info.eu/art-4-gdpr/ — retrieved 2026-11-03. (Mirror of Regulation (EU) 2016/679; official text at EUR-Lex.)
24. Ministry of Law and Justice (India), "The Digital Personal Data Protection Act, 2023" (No. 22 of 2023, 11 August 2023), https://www.meity.gov.in/static/uploads/2025/02/07b7d737f483714eacde37d1a259a6c8.pdf — retrieved 2026-11-03.

## How confident is this?

- **Solid:** every quoted sentence was read on the live page on 2026-11-03 and copied character-for-character. The ICMJE criteria, the ACM 2026 rewrite, the ICML paragraph, the ACL acknowledgement rule and the arXiv generative-AI points come from primary sources.
- **Solid:** the three cases have a primary retraction notice or a dated report linked above.
- **UNCERTAIN:** PSIT's own ethics committee, plagiarism-detector subscription and threshold. No public document states any of them; I have not claimed one exists.
- **UNCERTAIN:** the commencement status of individual DPDP Act provisions on 2026-11-03; the quoted sections come from the Gazette text, but which are in force is a legal question I did not verify.
- **UNCERTAIN:** arXiv's policies index labels itself "a work in progress", so the moderation page — the current location of the generative-AI policy — may be reorganised.
- **Not covered:** publisher-specific rules (Elsevier, Springer Nature, Wiley) and Indian funder rules (ICMR, DST). If a target journal has its own AI policy, it wins over COPE.

last_updated: 2026-11-03
