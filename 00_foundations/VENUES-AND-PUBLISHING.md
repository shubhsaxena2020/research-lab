# Venues and publishing: where a paper can go, and what each place actually is

**What this page is for.** A paper is only half the job; the other half is putting it somewhere that will read it, check it, and record it. This page explains the four kinds of place work appears, what arXiv really is (and is not), how review and rebuttal work, what it costs, and how to spot a fake venue. Every policy claim below has a URL I opened on 2026-11-03. Where a page was behind a login or would not load, I say so and mark it UNCERTAIN instead of guessing.

Read this before you pick a target. Choosing a venue badly wastes three months; choosing it well is the difference between a line on your CV and a lesson.

---

## 1. The four places work appears

A "venue" is just the place a paper is published or presented. There are four, and they are not ranked in a single ladder — they do different jobs.

| | What it is | Peer review | Typical timeline (verified anchors) | Prestige | Archival? | Who it suits |
|---|---|---|---|---|---|---|
| **arXiv preprint** | A public server for PDFs, run as a nonprofit, moderated not reviewed | **None.** Moderation only checks topicality and scholarly standards [1][2] | Submitted before 14:00 US Eastern, usually public 20:00 same day [5] | Low as a credential; high as a way to be read and cited early | Yes, effectively permanent once announced [8] | Everyone, as a *supplement* to a real venue. Never as the only place |
| **Workshop** | A one-day event attached to a bigger conference, or standalone | Light. Often 2–3 reviews, sometimes none; acceptance rates are high | NeurIPS 2026 satellite: contributions ~29 Aug, decision by 29 Sep, event 11–13 Dec [13][14] | Modest. Signals "work in progress" | **Depends**: archival (has proceedings) or non-archival [24] | A first paper. This is your realistic target |
| **Conference (main track)** | The main programme of a conference; proceedings usually published by ACM/IEEE/Springer/ACL | Heavy. 3–4 reviews, area chair, rebuttal, decision meeting [13][26] | NeurIPS 2026: submit 6 May, reviews 22 Jul, discussion to 3 Aug, decision 24 Sep [13]. AAAI-27: submit 28 Jul, decision 30 Nov [26] | High. NeurIPS, ACL and AAAI are all ICORE A* [9] | Yes | Work with a clear result and a real comparison |
| **Journal** | Periodic publication; no event, no travel | Heaviest per paper, but slow and often single-blind | TMLR and JOSS review on a rolling basis, no deadline [36][37] | High, but slow to accrue | Yes | Extended work, or when you cannot travel |

Two things this table hides.

First, **conference ≠ journal in computer science.** In most other fields the journal is the prize and conferences are for talking. In CS the opposite is true: the top conferences are the primary publication, and a NeurIPS paper counts more than most journal papers. That is why the CS ranking systems rank conferences at all [9].

Second, **a preprint is not a publication** in the sense your college or a scholarship committee means. It has a DOI-like identifier (arXiv:2410.01234) and it is citable, but it has passed no review. Anyone can check that in ten seconds by opening the abstract page, which says so.

---

## 2. arXiv in detail

### 2.1 What it is

arXiv (pronounced "archive") started in 1991, was founded by Paul Ginsparg, and spent decades hosted at Cornell University. In 2026 it became an independent nonprofit organisation [1]. It hosts over three million articles across physics, mathematics, computer science, quantitative biology, quantitative finance, statistics, electrical engineering and economics [1]. Submission is free [1][5].

The single most important sentence on the site:

> "Material is not peer-reviewed by arXiv - the contents of arXiv submissions are wholly the responsibility of the submitter and are presented 'as is' without any warranty or guarantee." [1]

And from the moderation page:

> "Please note that the arXiv moderation process is not a peer-review process. arXiv staff and moderators cannot give feedback on the submission." [2]

So: a human with a PhD in the field looks at your submission and asks "is this a real research paper in this subject area?" They do not check your maths, your experiments, or your claims. If you put a wrong number on arXiv, it stays wrong, permanently, with your name on it.

### 2.2 The endorsement system — and the January 2026 change

This is the part that will bite you personally, so read it twice.

To submit your **first** paper to arXiv, or your first paper in a new category, you must be **endorsed**. Endorsement is a working scientist vouching that you are a real researcher in that area.

**Who can endorse.** Endorsers must have authored a certain number of papers within the *endorsement domain* of the subject area — the number varies by area, and only papers submitted between three months and five years ago count. They must also hold an active positive endorsement themselves [3].

**Before January 2026**, having an institutional email address was usually enough to be auto-endorsed. That is no longer true.

> "As of January 21, 2026, arXiv will no longer accept institutional email addresses ... as the sole qualifier of endorsement for new authors." [4]

The new first path requires **both**: (1) an institutional email from an academic or research institution, **and** (2) prior authorship on a paper already accepted into the arXiv endorsement domain you want [4].

The second path is personal endorsement. You start a new submission, choose the category, and arXiv emails you an **endorsement request email** containing a link you can send to a prospective endorser [3]. The endorser receives a **six-character alphanumeric endorsement code** from you, enters it on arXiv's endorsement form, and records a yes or a no. A no is a recorded negative vote. The endorser's identity and comments are private to arXiv staff [3].

**What this means for you, concretely.** As a first-semester BCA student with no arXiv paper, path one is closed. Path two requires a scientist in the field who knows you or has seen your draft. Your realistic route is a **faculty co-author** — a PSIT teacher or an IIT/IISc mentor — who is already an arXiv author in cs.LG or cs.CL. That is one more reason to get a mentor before you write, not after.

Do not email a list of strangers asking for endorsement. arXiv explicitly calls that inappropriate [3], and it is how you get remembered badly.

Also: arXiv staff cannot endorse you. "arXiv staff cannot waive endorsement requirements or provide a personal endorsement for authors." [4]

### 2.3 What moderation rejects

arXiv declines submissions "in its sole discretion" [2]. The stated grounds:

- **Scholarly standards** — poorly prepared sections, figures, tables, references; unprofessional language; non-neutral tone [2].
- **Lacks scholarly interest** — no originality, novelty or significance; falsified or plagiarised content; misrepresented affiliation [2].
- **Not original or substantive research.** The policy names, in plain words, "course projects, research proposals, news" [2]. Your third-semester mini-project is not an arXiv paper unless it becomes a real study.
- **"Submissions in need of significant review and revision may also be declined."** [2]
- **Duplicated content** — multiple similar submissions get consolidated or versioned [2].
- **Rights** — must be your original work, no referee comments pasted in, no third-party copyright violations [2].
- **Rate limit** — two new submissions per calendar month, three active submissions; replacements limited to one per week after version 5 [2].

Note the asymmetry: prior publication in a journal does **not** guarantee arXiv accepts you. Journals and arXiv are independent gates [2].

### 2.4 AI-generated content and authorship

arXiv's policy is short and worth quoting in full, because it is the model most venues now copy:

> "1. continue to require authors to report in their work any significant use of sophisticated tools, such as instruments and software; we now include in particular text-to-text generative AI among those that should be reported... 2. remind all colleagues that by signing their name as an author of a paper, they each individually take full responsibility for all its contents, irrespective of how the contents were generated... 3. generative AI language tools should not be listed as an author; instead authors should refer to (1)." [2]

Three rules, then: **disclose** significant AI use, **own** everything in the paper regardless of who typed it, and **never** list a model as an author. If an AI tool invents a citation and you submit it, that is your misconduct, not the tool's.

### 2.5 Versions, replacement, and withdrawal

- Every submission gets a **date stamp** when you click submit [8].
- Once public, "each version of a work is considered a permanent part of the scientific record and may not be removed" [8].
- **Replacement** (v2, v3...) is for corrections, added references, revised arguments. You must state the reason in the Comments field, and you should merge old comments with new ones or they are lost [7].
- **Withdrawal** is not deletion. It creates a *new version* marked withdrawn, showing your reason publicly; the PDF download disappears from that version, but **all previous versions stay fully downloadable** [6].
- arXiv explicitly says it is "not appropriate to withdraw a paper because it is published or submitted to a journal" — use a journal-ref instead — and not appropriate "because it is being updated" — use a replacement [6].

Practical consequence: your v1 is forever. Do not post a draft you would be embarrassed by in six months. Post when the abstract and the main table are numbers you trust.

### 2.6 The bottom line on arXiv

arXiv is a **distribution channel**, not a credential. It gets your work in front of people in 24 hours, for free, with a permanent identifier. It does not review you, does not improve you, and does not count as a publication at most Indian institutions' counting exercises [45][47]. Use it after you have a venue, not instead of one.

---

## 3. Workshops, conferences, journals — and "archival"

**A conference** is an event with a deadline, a review round, an accept/reject decision, a proceedings volume, and a physical or virtual meeting where you present.

**A workshop** is a smaller event, usually one day, usually attached to a big conference. Its job is discussion of work in progress, not archiving finished results. NeurIPS states the purpose plainly: workshops "provide an informal, dynamic venue for discussion of work in progress and future directions" [14]. NeurIPS 2026 received 477 workshop proposals, accepted 102 [57].

**A journal** has no event. You submit, wait, revise, and eventually a PDF appears. TMLR, for example, uses "a rolling submission process, shortened review period, flexible timelines, and variable manuscript length", with review hosted openly on OpenReview [36].

### Archival vs non-archival — the distinction that trips up beginners

**Archival** means the paper goes into a permanent published proceedings with an ISBN/DOI and counts as a publication. **Non-archival** means it is presented but not published as proceedings; you keep the copyright and can submit an extended version elsewhere.

ACL's Student Research Workshop states both options explicitly: "Submissions (in both categories) may be archival or non-archival, based on the wish of the authors. All archival papers will be published in the ACL 2026 SRW Proceedings. Non-archival papers may be submitted to any venue in the future except for another SRW." [24]

CODS 2026's Young Researchers' Symposium says the same from the other direction: accepted papers "are eligible to be published in the conference proceedings. Authors may choose to withhold their paper from publication in case they wish to submit a completed version to a conference in future." [32]

Why you care: if you submit an **archival** workshop paper, that work is spent — you cannot publish the same results at a main conference later. If you submit **non-archival**, you get the talk, the feedback and the CV line, and you keep the paper for a bigger venue. For a first paper, non-archival is almost always the right choice.

### Why a workshop is the realistic first target

Four reasons, all mechanical rather than motivational.

1. **Review is lighter and the bar is "interesting", not "complete".** Workshops ask for work in progress [14].
2. **The format is shorter.** CODS YRS asks for a 4-page extended abstract [32]; AAAI student abstracts are 2 pages including references [28].
3. **There is mentorship built in.** ACL SRW runs a pre-submission mentorship programme where you get feedback *before* review [24]. That is free reviewing.
4. **It is where you meet the people who will later review you properly.** A workshop is a low-stakes introduction to the community you are trying to join.

### Satellite workshops and their deadline pattern

Big conferences host workshops in the days around the main event. The pattern is stable and worth memorising, because it tells you when to start writing.

For NeurIPS 2026: workshop **proposals** were due 6 June 2026, organisers were notified 11 July, the *suggested* deadline for workshop paper submissions was 29 August 2026, and the **mandatory** accept/reject notification was 29 September 2026. Workshops ran 11–12 December (Sydney) and 12–13 December (Paris, Atlanta) [14].

So the shape is: **proposals in early summer → paper deadline late August → decision late September → event in December.** ICML and ICLR follow the same rhythm with their own months. If you want to submit to a NeurIPS workshop, you are writing in July and August. Mark that in your calendar a year ahead; the dates shift by days, not months, and the cycle page for the current year is the only authority.

---

## 4. Tiers and rankings

### CORE / ICORE

CORE (now called ICORE, "an international collaboration") publishes a ranked list of computing conferences, assessed by committees of academics [9]. As of the ICORE2026 round there are **825 ranked venues**, distributed as: A* 7.52%, A 13.09%, B 30.18%, C 46.18%, plus Australasian and "other" categories [9].

The official definitions, quoted from ICORE's 2026 update page [10]:

- **A\*** — flagship. Critically: "A* is not necessarily stronger in terms of (e.g.) citations but is recognised as a flagship conference, i.e. 'A* = A + flagship'" [10].
- **A** — "Excellent" [10].
- **B** — "good to very good" [10].
- **C** — the floor for a venue to be ranked at all; ICORE notes that proposals below "the standard expected for rank C" are not accepted, and a venue needs at least 10 full research papers a year to qualify [10].
- A **National/Regional** tag means a conference is held in a single country or small group of countries with a local chair; ICORE says such venues "should be considered equivalent to B or C ranked venues" and that the tag "means that the conference is weaker than A, but does not indicate whether it is B or C" [10].

Verified examples from the portal, retrieved 2026-11-03: ACL A\*, NeurIPS A\*, AAAI A\*, EACL A, NAACL A [9].

**What these ranks do NOT mean.** They are not acceptance rates, not citation counts, not teaching quality, and not a measure of how much you will learn. The A\* definition says outright that it is not about citations — it is about being the place where the field's flagship conversation happens [10]. A B-ranked venue that three people in your exact subfield read can be worth more to you than an A\* where you are poster #4,102.

Also note what CORE does *not* rank any more: **the CORE journal database was discontinued from March 2022** [11]. If a website tells you a journal is "CORE A", that claim is not checkable through CORE, because CORE stopped ranking journals.

### h5-index and Google Scholar Metrics

Google Scholar Metrics publishes, per venue, an **h5-index**: the largest number *h* such that *h* articles published in that venue in the last five complete years have at least *h* citations each. It also gives a median h5. The metrics page is at https://scholar.google.com/citations?view_op=top_venues [54].

I deliberately did not extract numbers from that page. This project's rules forbid scraping Google Scholar, and Scholar blocks automated access; I am citing it as the place to look, not as a source of figures I read. **UNCERTAIN: I did not verify any specific h5 value**, so do not quote one from this document.

What h5 is good for: a rough, five-year, citation-based view of how much a venue's papers get used. What it is bad for: new venues (no history), niche venues (small but devoted readership), and anything where citation counts lag reality by years. A workshop will never have a good h5, and that tells you nothing about whether it is right for you.

### "Scopus-indexed" and "Web of Science-indexed"

These are **indexing facts**, not quality ranks. Scopus describes itself as "a comprehensive abstract and citation database" with 100M+ records, 30.2k active serial titles, 404k+ books and 2.6M+ preprints [52]. Web of Science is a citation database with several sub-indexes — Science Citation Index Expanded, Social Sciences Citation Index, Emerging Sources Citation Index, Conference Proceedings Citation Index, and others [53].

Being in either means a database has decided to track that venue. It says nothing about acceptance rate, review quality, or whether the editor answers email. A journal can be in Scopus and still be a mill. Plenty are.

### Why rank is a weak proxy for fit

Ranking answers "how central is this venue to its field?" It does not answer: will the reviewers understand my method, will anyone cite me, can I afford to attend, will the deadline collide with my exams, and will a human being reply to my email. For a first paper, those five questions matter more than a letter with an asterisk.

A concrete example: **CODS** (ACM India's data-science conference) does not appear as a ranked row in the ICORE 2026 database when searched on 2026-11-03 [9]. It is nonetheless the single best-fit venue in this document for a BCA student — Indian, cheap, with a track explicitly open to bachelor's students and travel grants for accepted ones [32][33]. Rank would have told you to skip it. Fit tells you to submit.

---

## 5. How acceptance works, end to end

### The submission site

Almost every CS venue uses one of four systems. You will meet all of them.

| System | Who runs it | What it feels like |
|---|---|---|
| **OpenReview** | Nonprofit; "configurable platform for peer review", open discussion, free submissions [38] | Reviews often become public after decision. Your profile must be complete or you get desk-rejected [20] |
| **HotCRP** | Software used by "thousands of sites", strong USENIX presence [39] | Utilitarian, fast, text-heavy |
| **CMT** | Microsoft Research [41] | Common for vision and some IEEE conferences |
| **EasyChair** | 4.9M users, 125,944 conferences [40] | Common for workshops and smaller conferences |

Whichever it is, two habits save you: create your profile **weeks** before the deadline (OpenReview profiles without an institutional email can take up to two weeks to be moderated [20]), and put every co-author's email in exactly as it appears on their profile.

### The pipeline

1. **Abstract deadline**, usually 2–7 days before the paper deadline. It exists to recruit reviewers. Missing it can lock you out; NeurIPS 2026 had abstracts due 4 May and full papers 6 May [13].
2. **Desk rejection.** An editor or program chair rejects without review for formatting, anonymity, page-limit, dual-submission or profile violations. CVPR states it flatly: "Papers that are not properly anonymized, or do not use the template, or have more than eight pages (excluding references) will be rejected without review." [29] ICML 2026 added **cascading** desk rejections: abuse by one paper can take down all papers by any of its authors [55].
3. **Reviewer assignment.** Area chairs match papers to reviewers using declared expertise and conflicts of interest. Both NeurIPS and CVPR require you to declare domain and personal conflicts in OpenReview; an incomplete profile "risks desk rejection" [20][29].
4. **Scores.** Typically 3–4 reviews on scales like 1–10 for quality, clarity, significance, originality. NeurIPS 2026 publishes exactly those four criteria to reviewers [19 — see the Reviewing Guidelines linked from the handbook]. (*Note: the criteria are on the Reviewer Guidelines page at https://neurips.cc/Conferences/2026/ReviewerGuidelines; I read them there.*)
5. **Rebuttal / author response.** Your one chance to correct misunderstandings. Section 6.
6. **Area chair + decision meeting.** The AC writes a meta-review and argues your case (or doesn't) in a meeting with senior ACs. Reviewers' scores are advice; the AC decides.
7. **Notification.** NeurIPS 2026: 24 September [13]. AAAI-27: 30 November [26]. ACL 2026: 4 April [22].
8. **Camera-ready.** A revised PDF on a publisher template, usually 1–3 weeks after notification. AAAI-27: 14 December 2026 [26]. ACL 2026: 19 April 2026 [22]. NeurIPS lets you buy one extra content page for the camera-ready [20].
9. **Copyright form.** ACM, IEEE or ACL's form, signed by the corresponding author. This transfers or licenses rights; read the open-access option before you sign.
10. **arXiv posting.** Allowed at most venues, but check the venue's preprint policy and the timing. ACL has had **no anonymity period** since 15 February 2024, meaning you may post a non-anonymous preprint while under review [25]. Other venues differ; read the CFP.
11. **Registration and presentation.** At least one author must register and present. ACL 2026: "All papers must be registered for presentation by May 11" and "Papers not properly registered will not be included in the program or proceedings" [23]. One registration covers up to 2 papers [23].

### Double-blind review, precisely

In **double-blind** (also called two-way anonymised) review, the reviewer does not know who wrote the paper, and the author does not know who reviewed it.

The rules that matter, quoted from ACL Rolling Review [25]:

> "Papers must not include authors' names and affiliations. Furthermore, self-references that reveal the authors' identities, e.g., 'We previously showed (Smith, 1991)…' must be avoided. Instead, use citations such as 'Smith previously showed (Smith, 1991)…'"

> "Supplementary materials, including any links to repositories, should also be anonymized. Links to file hosting services that can track downloads, such as Dropbox, are not allowed."

> "Submissions that violate these requirements will be desk rejected."

And from CVPR: "Authors are not allowed to include external links (e.g., to webpages, images, or videos) in submissions, supplementary material, and rebuttal, when the links expand content and subvert the reviewing process." [29]

**The five mistakes that break anonymity.** I have seen each of these kill a submission before review.

1. **"Our previous work [12] showed..."** — third person fixes it: "Rao et al. [12] showed...". The citation stays; the "our" goes.
2. **A GitHub link.** `github.com/shubhsaxena/paper-code` is your name. Use an anonymised repository (Anonymous GitHub, or a zip in the supplementary material) [25].
3. **Acknowledgements.** "We thank Prof. X at PSIT for..." identifies the institution and usually the person. Delete the section in the submitted version and add it back in the camera-ready.
4. **Self-identifying metadata.** The PDF's author field, the file name `shubh_camera_ready.pdf`, an Overleaf link with your username in it. Strip all of it.
5. **Talking about the submission.** CVPR's policy prohibits saying a paper is "under submission to CVPR"; even a webpage saying so can be treated as a violation [30].

Two things double-blind does **not** protect you from. Reviewers can often guess ("a small Indian college writing about Hindi OCR"), and some venues are single-blind by design — most journals, and some conferences. The rule is unchanged in both cases: write as if your name were visible, because it may be.

---

## 6. Rebuttal

The rebuttal (also "author response" or "author feedback") is a document you write after reading the reviews, before the decision. It is the only place you can correct a reviewer who misread you.

### Length

Assume one page unless told otherwise, and check the CFP.

CVPR 2026: "the rebuttal is limited to a one-page PDF file using the rebuttal template included in the CVPR 2026 Submission Template. Responses longer than one page will simply not be reviewed. This includes responses where the margins and formatting are deemed to have been significantly altered." [29]

That last clause matters: shrinking the font to fit more text means the whole response is discarded, not trimmed.

Some venues use a discussion period instead of a document. NeurIPS 2026 ran "Author + Reviewer + AC Discussion Period" from 27 July to 3 August 2026 — you post short comments in the forum over a week, not one PDF [13]. AAAI-27 has an "Author feedback window" in late October 2026, after Phase 2 reviews and before the meta-review [26]. ARR uses a character-limited response box on OpenReview.

### Structure that works

- **Opening, 3–4 lines.** Thank the reviewers, restate what the paper does in one sentence, and state the two or three things you will change. Do not re-argue the paper.
- **One block per substantive concern, in the reviewers' order.** Quote the concern in italics, answer in 2–4 sentences, say exactly what changed in the revision ("we added the ablation in Table 4, +0.8 F1").
- **A table of small fixes.** Typos, missing citations, clarifications — one line each, grouped. Reviewers like seeing their minor points acknowledged.
- **Closing, 2 lines.** What the paper will say after revision, and that you will address the rest in the camera-ready.

### What to fight and what not to

**Fight** factual errors: "the reviewer says we did not compare to X; we do, in Table 2, row 4, and we now say so in the text." Fight a misread of your method. Fight a claim that you lack an experiment you actually ran.

**Do not fight** taste. "The reviewer thinks the problem is unimportant" or "the reviewer wanted a different architecture" is not winnable in 500 words, and arguing it makes you look defensive. Acknowledge, explain your choice in one sentence, move on. Also do not fight scores, do not complain about the process, and never imply a reviewer is incompetent.

### Tone

Write to a tired person who read nine papers today. Short sentences. No adjectives about your own work. Never "we respectfully disagree" followed by three paragraphs of the same claim. If a reviewer is right, say "the reviewer is right, we will fix this" — that single sentence buys you more credibility than a page of defence.

One hard rule: **no new results in a rebuttal** unless the venue allows it. CVPR discourages new contributions and unrequested experiments in rebuttals [30]. Adding a fresh experiment to a one-page response is how you get accused of changing the paper after review.

---

## 7. Money and travel

This is where a good paper dies for an Indian student. I will give you real numbers, then the exits.

### Registration, in real numbers (all verified 2026-11-03)

| Venue | Category | Early | Late/Standard |
|---|---|---|---|
| ACL 2026, San Diego (in person) | Student, full conference, presenting | **$750** | $900 |
| ACL 2026 (in person) | Student, 2-day workshop only | $450 | $600 |
| ACL 2026 (in person) | Student, 1-day workshop only | $350 | $500 |
| ACL 2026 (virtual) | Student, full conference | $300 | $450 |
| ACL 2026 | ACL student membership (required, extra) | $50 | — |
| NeurIPS 2026, Paris satellite | Student, conference + tutorials + workshops | **€380** | €480 |
| NeurIPS 2026, Paris | Student, workshops only | €130 | €180 |
| CODS 2026, Gandhinagar | Student author, ACM member | **₹5,000** (+18% GST) | — |
| CODS 2026 | Student author, non-member | ₹6,000 (+18% GST) | — |

Sources: [23] for ACL 2026; [17] for NeurIPS Paris; [33] for CODS 2026.

Two facts sit inside those numbers. ACL's page says food and beverage alone "can exceed $800 per full conference attendee", which is why the fees are what they are, and notes ACL "intentionally subsidize[s] student and academic registrations" [23]. NeurIPS 2026 in-person registration at Atlanta and Sydney **sold out** to the general public; each accepted paper got exactly one author place [19].

### Travel

**UNCERTAIN — estimate, not a verified price.** I could not find an official source for airfare, so treat the following as planning arithmetic, not fact: a return economy ticket Kanpur/Delhi → US East Coast typically runs ₹70,000–₹1,20,000, and Delhi → Paris/Frankfurt ₹45,000–₹80,000, booked 2–3 months out. Add 5–7 nights of hotel at $120–$200/night in a conference city, plus $30–$50/day food. A US conference trip realistically lands at ₹1.5–2.5 lakh all-in. Verify against a booking site for your dates before you tell anyone a number.

### The visa reality

**United States.** Attending a conference is an explicitly permitted B-1 activity: the State Department lists "Attend a scientific, educational, professional, or business convention or conference" among permitted B-1 uses [49][50]. The application fee is **$185** [49]. You apply on form DS-160, pay, and attend an in-person interview [49].

The part nobody tells you: **an acceptance letter is evidence, not permission.** The consular officer decides whether you qualify, and the officer may require an interview of any applicant [49]. NeurIPS's own visa page warns that even with a visa, "it is possible that immigration officers at U.S. points of entry may require you to undergo additional screening" [18]. In practice, Indian student applicants for a first-time B1/B2 with a conference invitation and no travel history face real refusal risk. Apply 3–4 months early, bring the invitation letter, the registration receipt, proof of enrolment, bank statements and a return ticket.

**Europe (Schengen).** India is a visa-required country; the Schengen short-stay visa covers visits "of up to 90 days in any 180-day period" across all 29 Schengen countries [51]. **UNCERTAIN: I could not load the EU's visa-fees page today, so I am not quoting the current Schengen fee.** Check your intended consulate's site (the country where the conference is held) for the fee and the appointment lead time.

For both: get the invitation letter **early**. NeurIPS generates them only for registered attendees and stops after the conference closes [18].

### The four funded paths

**1. Student volunteer programmes — usually free registration.**
AAAI's Student Scholar Volunteer Program states: "A limited number of complimentary technical program registrations will be available for students who volunteer during the conference." Eligibility: full-time undergraduate or graduate students, AAAI members, who "submitted paper(s) to the conference program AND letter(s) of recommendation from their faculty advisor" [27]. Applications for AAAI-27 run 30 November – 4 December 2026, and the page warns: do not register before you hear back, "otherwise you will forfeit their complementary registration" [27].

**2. Travel grants.** Often tied to a specific track. ACL 2026's Student Research Workshop had a grant application deadline of 8 May 2026 with notification 20 May [24]. CODS offers "partial travel Grants ... for all students whose papers are accepted" [32]. NeurIPS runs a Financial Assistance programme covering "complimentary in-person conference registration", "complimentary virtual registration" and "prepaid accommodation" [57 — see the NeurIPS blog's Financial Assistance section].

**3. Present remotely or hybrid.** Increasingly normal. ICML 2026 made attendance **optional** for authors of accepted papers: authors choose between presenting in person or "just wish to include their paper in the proceedings (without presentation)", and proceedings-only papers need "at least one of the authors must obtain virtual registration" [56]. ACL sells a virtual student rate at $300 early [23]. NeurIPS 2026 reserves "a maximum of 1-hour remote presentation ... in case of unforeseen emergencies" per workshop [14] — so remote is a fallback, not a right, at that venue.

**4. Virtual registration rates.** Typically 30–40% of the in-person student rate. ACL student virtual full conference: $300 early vs $750 in person; NeurIPS Paris student workshops-only €130 vs €380 for the full week [23][17].

Cheapest realistic path for you: an Indian venue (CODS at ₹5,000–6,000), then a virtual registration at an international one, then in-person only when a grant covers it.

---

## 8. Student tracks and student-focused venues

**ACL Student Research Workshop (SRW).** The most student-centred venue in NLP. Its stated goal is to help students "at multiple stages of their education, including highschool, undergraduate, MSc/MA, junior and senior PhD students" [24]. Two categories: thesis proposals (Masters/PhD) and research papers, where "the first author MUST BE a current student" [24]. Submissions may be archival or non-archival [24]. For ACL 2026 the direct submission deadline was 18 March 2026, notification 24 April, camera-ready 8 May, with a pre-submission mentorship deadline of 4 February 2026 [24]. The mentorship is the real prize: free feedback from a senior student or researcher before review.

**AAAI Student Abstract and Poster Program.** "The program is open to all students at the Undergraduate, Masters, and Doctoral levels." Advisors may be co-authors, but "students are requested to honor the spirit of the program by submitting only work for which they are primary investigators" [28]. Format: "no longer than 2 pages including references" in AAAI two-column style, plus a supplementary file up to 20 MB [28]. For AAAI-26 the abstract deadline was 15 September 2025, notification 30 October, camera-ready 13 November [28]. Note the *A\** rank of AAAI [9] — this is a genuinely prestigious venue offering a 2-page door for undergraduates.

**ACM Student Research Competition (SRC).** Runs *inside* ACM SIG conferences. In the year described on the SRC site, competitions took place at 21 participating SIG conferences with "more than 342 student participants" [35]. You submit an abstract, present a poster, and if you place, present again. Judged on "knowledge of their research area, contribution of the research, and the quality of the oral and visual presentation" [35].

**CODS Young Researchers' Symposium (India).** Explicitly for students "currently pursuing PhD/ Masters/ Bachelors" [32]. 4-page extended abstract, first author must be a current student, work-in-progress welcome, partial travel grants for all accepted students, best-paper award, and mentorship events for accepted authors [32]. For CODS 2026: submission 20 August 2026, decision 6 October, camera-ready 18 November [32]. If you submit to exactly one thing this year, make it this.

**MIT Undergraduate Research Technology Conference (URTC).** "An internationally-renowned research conference for undergraduates and by undergraduates" [34]. Technical paper deadline 9 August 2026, notification 28 August; poster and lightning-talk deadline 4 September [34]. It is in Cambridge, Massachusetts, so the cost is the barrier, but the acceptance bar is set for undergraduates.

**Workshops with a student focus.** Many NeurIPS/ICML/ACL workshops exist specifically for early-career researchers and run mentoring sessions alongside the talks. Read the workshop's call for papers for the phrase "work in progress" and for a mentorship programme; those are the two signals that it is aimed at you.

One caution on eligibility. Several programmes have age or enrolment conditions that a 17-year-old first-year may not meet on paper. AAAI's volunteer programme requires AAAI membership and a submitted paper [27]; NeurIPS requires in-person attendees to be "14 years of age or older" and to attend with an adult [21]. Read the eligibility sentence before you spend a weekend on the application.

---

## 9. Predatory venues: a 10-point check

A predatory venue takes your money and gives you a fake publication. It is not a bad venue; it is a business that sells the *appearance* of one. Indian students get targeted heavily because our email addresses are public on college sites and our institutions reward publication counts.

### The 10-point check

Score one point for each red flag. **Three or more means walk away.**

1. **Guaranteed acceptance, or a decision in days.** Real review takes months; NeurIPS took 6 May → 24 September [13]. "Acceptance within 7 days" is a sale, not a review.
2. **Money asked before review.** Legitimate venues charge *after* acceptance (registration) or charge an APC on acceptance. An invoice at submission is the business model.
3. **Fees are hidden or vague.** Think.Check.Submit asks directly: "Does the journal site explain what these fees are for and when they will be charged? ... Do they mention the currency and amount of any fees?" [42]
4. **No findable editorial board.** TCS: "Is the publisher offering a review by an expert editorial board or by researchers in your subject area?" [42] If the board page is empty, or the names do not exist in a search, stop.
5. **Fake or unverifiable metrics.** "Universal Impact Factor 4.9", "ICV 98.7", "Global Impact Factor" — these are invented indices. UGC's own guidance says that if "misleading and/or false metrics are displayed anywhere on the journal's website or its pages the journal will not be eligible" for its list [45]. Also: a claimed "CORE A" journal rank cannot be real, because CORE stopped ranking journals in March 2022 [11].
6. **The name is a template.** "International Journal of Advanced Research in Computer Science and Engineering Technology" — long, generic, unGoogleable, and easily confused with a real journal. TCS: "the name is unique; it is not the same or easily confused with another journal" [42].
7. **Spelling and grammar errors on the homepage.** A venue that cannot proofread its own call for papers will not proofread yours. arXiv lists "appropriate standards of scholarly communication" as a moderation ground for exactly this reason [2].
8. **No peer-review description.** TCS: "Does the website mention whether the process involves independent/external reviewers, how many reviewers per paper?" [42] "Fast double-blind review by eminent reviewers" with no names is not a description.
9. **Spam invitations.** If the email arrived unsolicited, addressed "Dear Researcher", offering a keynote slot you never applied for, it is marketing. Real conferences do not recruit speakers by bulk mail.
10. **No indexing you can verify.** Check the journal in DOAJ (the Directory of Open Access Journals, which vets open-access journals) [44], and check the claimed Scopus/WoS coverage on Scopus's own source list or Clarivate's Master Journal List — not on the journal's homepage.

### The authorities

**Think. Check. Submit.** (https://thinkchecksubmit.org/) is the cross-industry campaign run by publishers, librarians and research bodies. Its journal checklist asks, in order: do you know the journal; can you identify and contact the publisher; is the peer review type clear; are articles indexed and archived; are fees clear; are author guidelines provided; is the publisher a member of a recognised initiative such as COPE [42]. It also states the single most useful line for a beginner: a trustworthy journal "doesn't guarantee acceptance or a very short peer review time" [42].

**Beall's List** (https://beallslist.net/) is an archived list of potential predatory publishers, originally compiled by librarian Jeffrey Beall. The site is explicit about its status: "This is an archived version of the Beall's list... We will only update links and add notes to this list." Its method is to find the publisher (usually in the footer or "About" section) and search that name, with the warning that "All journals published by a predatory publisher are potentially predatory unless stated otherwise" [43].

Use it as a **pointer**, not a verdict: absence from the list proves nothing, presence is a strong signal to look harder.

**Beall-style red flags** in one line each: the journal asks you to be an editor via unsolicited email; the "impact factor" is calculated by the publisher itself; the editorial board lists people who have never heard of the journal; the APC is waived "for a limited time"; the submission system is an email address; the journal published 400 papers in its first year.

**On conferences specifically.** A predatory conference spams, charges $600 for "registration" with no proceedings, puts "IEEE" in the title without IEEE technical co-sponsorship, and hands every attendee an "award". Check the IEEE/ACM/Springer proceedings listing for the previous edition. If last year's "proceedings" do not exist in a real digital library, this year's will not either.

---

## 10. The Indian context

### UGC-CARE — read this carefully, because most advice you will get is out of date

UGC-CARE was the University Grants Commission's list of approved journals, created to fight predatory publishing. **It has been discontinued.**

The UGC-CARE site itself now carries this banner:

> "The UGC-CARE List has not been updated since October 2024 and will not be updated further, as per the UGC Public Notice dated February 11, 2025. The website is available for information purposes only." [45]

The follow-up public notice, dated 16 July 2025, makes the status precise. UGC approved (a) "Suggestive Parameters for choosing Peer-Reviewed Journals" and (b) uploading "a list of 1474 UGC CARE listed journals as on 10 February, 2025, for referencing purposes". And then:

> "This list of UGC-CARE Journals (now discontinued) is intended to serve as a reference resource only; the inclusion or exclusion of a journal in this list does not imply validation or endorsement by the Commission." [46]

So: **UGC-CARE is a reference list, not a mandate.** If a senior tells you "it must be a UGC-CARE journal", that instruction is two years out of date. What replaced it is Annexure-1 of that notice — a set of suggestive parameters covering journal title, ISSN, periodicity, transparent review policy, certified domain, editorial board composition, APC transparency, publishing timeline, acceptance rate, citation record [46]. That annexure is, usefully, a ready-made quality checklist you can apply yourself.

**How to check a journal now:** look for the ISSN in the ISSN portal; check DOAJ for open-access vetting [44]; check Scopus's source list or Clarivate's Master Journal List for indexing claims [52][53]; and apply the ten-point check in section 9.

### Scopus and Web of Science

Both are indexes. Scopus covers 100M+ records across journals, books, conference proceedings and preprints [52]. Web of Science is a family of citation indexes including SCIE, SSCI, ESCI, the Conference Proceedings Citation Index and others [53].

For an Indian student the practical facts are: (a) most good CS conferences are indexed through their publisher's proceedings, not individually; (b) "Scopus-indexed" is claimed very loosely and should be verified on Elsevier's own source list; (c) an ESCI listing is a weaker signal than SCIE, and both are weaker signals than "the people in my field read this".

### NIRF and what it actually measures

The National Institutional Ranking Framework is the Ministry of Education's ranking of Indian institutions. For Engineering in 2025, the weights are: Teaching, Learning & Resources 0.30; **Research and Professional Practice 0.30**; Graduation Outcomes 0.20; Outreach and Inclusivity 0.10; Perception 0.10 [47].

Inside that research block of 100 marks: **Publications 35, Quality of Publications 40, IPR and Patents 15, Footprint of Projects and Professional Practice 10** [47].

Two things follow. First, **publications are 75 of the 100 research marks**, so your college has a structural reason to want faculty publishing. Second, **what counts is the institution's output, not yours** — NIRF scores the institution, and a BCA student's workshop paper contributes nothing measurable to it.

### AICTE

AICTE funds research through schemes like the Research Promotion Scheme (RPS), which "is aimed to create research ambience in the institutes by promoting research in engineering sciences". Eligibility is specific: "AICTE approved Technical Institutions/University Department with relevant PG programme" and "**Full time regular faculty** with research experience and publications" [48]. Students are not eligible applicants. That is the honest answer to "can AICTE fund my project" — not directly, but a faculty member with an RPS grant can fund you as project staff or a co-author.

### What all of this means for you

Almost nothing, and that is the good news. UGC-CARE, Scopus, WoS, NIRF and AICTE all govern **institutional accounting**: faculty promotions, college rankings, funding eligibility. None of them changes where you should submit, because none of them reviews your paper.

Your objective function is different from your college's. You want: reviewers who understand the work, a deadline you can meet around exams, a cost near zero, and a line on your CV that a future supervisor can verify by clicking a link. A 4-page extended abstract at CODS [32] serves that better than a paid "publication" in a journal that NIRF would not count anyway.

The one place institutional rules touch you: if you later apply for a faculty post or a PhD in India, some committees still ask "is it UGC-CARE / Scopus indexed?" You will be able to answer with something better — a peer-reviewed venue with a public proceedings page.

---

## 11. Ten realistic target venue types for an undergraduate first-author paper

Each row: what it is, a real example with its URL, the deadline pattern, cost, review rigour, and why it fits you. Deadlines are the ones I verified for the cycle named; the years shift, so the *pattern* is what you plan around.

| # | Type | Real example | Deadline pattern (verified cycle) | Cost | Rigour | Why it fits a BCA first-year |
|---|---|---|---|---|---|---|
| 1 | **arXiv preprint** (not a venue, but step 1) | arXiv cs.LG — https://arxiv.org | Anytime; submitted before 14:00 ET, public ~20:00 same day [5] | Free [1] | None — moderation only [2] | Gets you a citable link and feedback fast. Needs an endorser [3][4] |
| 2 | **Student research workshop at a top NLP conference** | ACL 2026 SRW — https://2026.aclweb.org/calls/student_research_workshop/ | Mentorship early Feb; submission mid-March; decision late April [24] | Virtual ACL student rate $300 [23] | Medium; 2–3 reviews + mentor | Explicitly open to undergraduates, with pre-submission mentoring [24] |
| 3 | **Student abstract at a top AI conference** | AAAI-26 Student Abstract — https://aaai.org/conference/aaai/aaai-26/student-abstract-and-poster-program-call/ | Abstract mid-September; decision late October; camera-ready mid-November [28] | Conference registration (student rate; see AAAI site) | Medium | 2 pages including references, undergraduate-eligible, A* venue [28][9] |
| 4 | **Young Researchers' Symposium at an Indian ACM conference** | CODS 2026 YRS — https://ikdd.acm.org/cods-2026/call-for-young-researchers-symposium-papers.php | Submission mid/late August; decision early October; camera-ready mid-November [32] | ₹5,000–6,000 + GST, student author [33] | Medium; travel grants for accepted students [32] | Bachelor's students eligible; in India; cheapest real option |
| 5 | **ACM Student Research Competition inside a SIG conference** | ACM SRC — https://src.acm.org/ | Follows the host conference's dates; 21 SIG conferences participate [35] | Host conference registration | Medium; judged poster + talk | Built for undergraduates; feedback from judges [35] |
| 6 | **Undergraduate research conference** | MIT URTC — https://urtc.mit.edu/ | Technical paper early August; poster/lightning talk early September; event October [34] | Registration + US travel (the real cost) | Medium | By and for undergraduates; poster track is a low bar [34] |
| 7 | **Non-archival workshop at a major ML conference** | NeurIPS 2026 workshops — https://neurips.cc/Conferences/2026/CallForWorkshops | Proposals June; contributions ~late August; decision late September; event December [14] | NeurIPS student rate; Paris student €380 [17] | Light-medium | Work-in-progress welcome; non-archival keeps the paper free for later [14][24] |
| 8 | **Rolling journal (no deadline)** | TMLR — https://jmlr.org/tmlr/ ; JOSS — https://joss.theoj.org/about | Submit any day; TMLR reviews on OpenReview with rolling decisions [36] | Free to submit; JOSS is free [37] | High (TMLR), medium (JOSS, software-focused) | No deadline to miss during exams; TMLR values correctness over significance [36] |
| 9 | **Short paper at a main conference** | ACL 2026 short papers (4 pages) — https://2026.aclweb.org/calls/main_conference_papers/ | Same cycle as long papers: submit early January, decision early April [22] | Same as long papers; virtual $300 [23] | High | A focused negative result or small study fits the 4-page format [25] |
| 10 | **Datasets / evaluations / reproducibility track** | NeurIPS 2026 Evaluations & Datasets — https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets | Same dates as the main track: abstract 4 May, full 6 May, decision 24 September [13] | Same as main conference | High | A careful reproduction or a small clean dataset is a legitimate contribution, not a lesser one |

Two notes on reading this table. **Rows 2, 3, 4 and 5 are the ones to actually attempt this year.** Rows 8 and 9 are what you do with the same work twelve months later. Row 1 is not a target at all — it is a step.

And the honest caveat on row 3: the AAAI student abstract page for AAAI-27 that I fetched still displays AAAI-21 content, so I verified eligibility and format from the AAAI-26 call [28]. The programme has run continuously since at least 2021 with the same 2-page format; **UNCERTAIN whether AAAI-27 changes the page limit**, so read the AAAI-27 call when it appears.

---

## Sources

All retrieved 2026-11-03 unless stated. Every URL below was opened and read during the writing of this page.

1. arXiv, "About arXiv" — https://info.arxiv.org/about/index.html
2. arXiv, "arXiv moderation" — https://info.arxiv.org/help/moderation/index.html
3. arXiv, "The arXiv endorsement system" — https://info.arxiv.org/help/endorsement.html
4. arXiv blog, "Attention Authors: updated endorsement policy" (21 January 2026) — https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/
5. arXiv, "Submission guidelines / submit" — https://info.arxiv.org/help/submit.html
6. arXiv, "Withdrawing an article" — https://info.arxiv.org/help/withdraw.html
7. arXiv, "Submit a new version of a work" — https://info.arxiv.org/help/replace.html
8. arXiv, "Submission Version Availability" — https://info.arxiv.org/help/versions.html
9. ICORE Conference Portal (CORE rankings database, ICORE2026) — https://portal.core.edu.au/conf-ranks/
10. CORE, "ICORE 2026 Rankings Updates" (rank definitions) — https://www.core.edu.au/icore-portal/icore-portal-2026-rankings-updates
11. CORE, "CORE Rankings Portal" (journal DB discontinued March 2022) — https://www.core.edu.au/conference-portal
12. NeurIPS 2026, "Call For Papers" — https://neurips.cc/Conferences/2026/CallForPapers
13. NeurIPS 2026, "Dates and Deadlines" — https://neurips.cc/Conferences/2026/Dates
14. NeurIPS 2026, "Workshops Guidance" — https://neurips.cc/Conferences/2026/WorkshopsGuidance
15. NeurIPS 2026, "Call for Workshops" — https://neurips.cc/Conferences/2026/CallForWorkshops
16. NeurIPS 2026, "Pricing" (cancellation and visa-refund policy) — https://neurips.cc/Conferences/2026/Pricing
17. NeurIPS 2026 Paris satellite, "Registration fees" — https://neurips-europe.cc/
18. NeurIPS 2026, "Visa Information" — https://neurips.cc/Conferences/2026/Visa
19. NeurIPS 2026, "Author Registration" (one place per paper; sold out) — https://neurips.cc/Conferences/2026/AuthorRegistration
20. NeurIPS 2026, "Main Track Handbook" (V2026.3) — https://neurips.cc/Conferences/2026/MainTrackHandbook
21. NeurIPS 2026, "Registration" (minors policy, student ID) — https://neurips.cc/Register/view-registration
22. ACL 2026, "Main Conference call for papers" — https://2026.aclweb.org/calls/main_conference_papers/
23. ACL 2026, "Registration" (fees, membership, deadlines) — https://2026.aclweb.org/registration/
24. ACL 2026, "Student Research Workshop" — https://2026.aclweb.org/calls/student_research_workshop/
25. ACL Rolling Review, "Call for Papers" (two-way anonymised review, multiple submission, preprint policy) — https://aclrollingreview.org/cfp
26. AAAI-27, "Main Technical Track Call" — https://aaai.org/conference/aaai/aaai-27/main-technical-track-call/
27. AAAI-27, "Student Scholar Volunteer Program" — https://aaai.org/conference/aaai/aaai-27/student-scholar-volunteer-program/
28. AAAI-26, "Student Abstract and Poster Program: Call for Proposals" — https://aaai.org/conference/aaai/aaai-26/student-abstract-and-poster-program-call/
29. CVPR 2026, "Author Guidelines" — https://cvpr.thecvf.com/Conferences/2026/AuthorGuidelines
30. CVPR 2027, "Author Guidelines" (anonymity policy FAQ, rebuttal policy) — https://cvpr.thecvf.com/Conferences/2027/AuthorGuidelines
31. ICLR 2027, conference page and important dates — https://iclr.cc/Conferences/2027
32. CODS 2026, "Call for Young Researchers' Symposium Papers" — https://ikdd.acm.org/cods-2026/call-for-young-researchers-symposium-papers.php
33. CODS 2026, "Conference Registration" (rates) — https://ikdd.acm.org/cods-2026/registration.php
34. MIT Undergraduate Research Technology Conference — https://urtc.mit.edu/
35. ACM Student Research Competition — https://src.acm.org/
36. Transactions on Machine Learning Research — https://jmlr.org/tmlr/
37. Journal of Open Source Software, "About" — https://joss.theoj.org/about
38. OpenReview, "About OpenReview" — https://openreview.net/about
39. HotCRP.com — https://hotcrp.com/
40. EasyChair — https://easychair.org/
41. Microsoft CMT — https://cmt3.research.microsoft.com/
42. Think. Check. Submit., "Journals" checklist — https://thinkchecksubmit.org/journals/
43. Beall's List of Potential Predatory Journals and Publishers — https://beallslist.net/
44. Directory of Open Access Journals — https://doaj.org/
45. UGC-CARE (site notice on discontinuation) — https://ugccare.unipune.ac.in/site/website/index.aspx
46. UGC, Public Notice, 16 July 2025, "Suggestive Parameters for choosing Peer-Reviewed Journals" (PDF) — https://www.ugc.gov.in/pdfnews/6124898_Public-Notice-CARE-Journals.pdf
47. NIRF, "India Rankings 2025 — Methodology for Ranking of Academic Institutions (Engineering)" (PDF) — https://www.nirfindia.org/nirfpdfcdn/2025/framework/Engineering.pdf
48. AICTE Research Promotion Scheme (RPS), scheme page with eligibility — https://www.indiascienceandtechnology.gov.in/programme-schemes/research-and-development/aicte-research-promotion-scheme-rps?language=en
49. U.S. Department of State, "Visitor Visa" (B-1/B-2, $185 fee, interview) — https://travel.state.gov/content/travel/en/us-visas/tourism-visit/visitor.html
50. U.S. Department of State, "FACT SHEET: U.S. Business Visas (B-1) and Allowable Uses" — https://travel.state.gov/content/travel/en/us-visas/business/b-1-fact-sheet.html
51. European Commission, "EU visa policy" (Schengen 90/180 rule) — https://home-affairs.ec.europa.eu/policies/schengen-borders-and-visa/visa-policy_en
52. Elsevier, "Scopus" product page (coverage figures) — https://www.elsevier.com/products/scopus
53. Clarivate, "Web of Science platform" (index family) — https://clarivate.com/academia-government/scientific-and-academic-research/research-discovery-and-referencing/web-of-science/
54. Google Scholar Metrics (h5-index definition and venue tables; cited as a pointer, not scraped) — https://scholar.google.com/citations?view_op=top_venues
55. ICML blog, "What's New in ICML 2026 Peer Review" — https://blog.icml.cc/2026/01/08/whats-new-in-icml-2026-peer-review/
56. ICML 2026, "Call For Papers" (attendance optional, proceedings-only) — https://icml.cc/Conferences/2026/CallForPapers
57. NeurIPS blog, "Announcing the NeurIPS 2026 Workshops" (477 proposals, 102 accepted) and Financial Assistance — https://blog.neurips.cc/2026/08/10/announcing-the-neurips-2026-workshops/

---

## How confident is this?

- **Solid.** arXiv policy (endorsement, moderation, AI, versions, withdrawal) is quoted verbatim from arXiv's own pages [1]–[8]. The January 2026 endorsement change is from arXiv's own blog [4] and it directly affects Shubh — he cannot self-endorse via a college email any more.
- **Solid.** Registration fees, conference dates and rebuttal rules are transcribed from the current cycle pages for ACL 2026, NeurIPS 2026, AAAI-27, CVPR 2026/2027 and CODS 2026 [13][17][22][23][26][29][32][33]. ICORE rank definitions and the 825-venue distribution come from CORE's own 2026 update page [9][10].
- **Solid.** UGC-CARE's discontinuation is confirmed twice: the site banner [45] and the July 2025 UGC notice with the exact "reference resource only ... does not imply validation or endorsement" wording [46]. NIRF weights are from the 2025 Engineering methodology PDF [47].
- **UNCERTAIN — airfare and hotel costs.** No official source; the ₹70,000–₹1,20,000 / $120–$200 figures in section 7 are labelled estimates and should be re-checked against a booking site.
- **UNCERTAIN — Schengen visa fee.** The EU visa-fees page would not load on 2026-11-03, so no amount is quoted.
- **UNCERTAIN — h5-index values.** By design I did not extract numbers from Google Scholar Metrics (project rule: no scraping Scholar). Only the definition is given.
- **UNCERTAIN — AAAI student abstract format for AAAI-27.** The AAAI-27 URL for that programme still serves AAAI-21 content; I verified 2-page format and undergraduate eligibility from the AAAI-26 call [28]. Re-read the AAAI-27 version when it is posted.
- **Date-sensitive everywhere.** Every deadline in this file belongs to the cycle named in brackets. Nothing here should be used to plan a submission without opening the current-year CFP.

last_updated: 2026-11-03
