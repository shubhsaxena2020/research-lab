# Venues and publishing: where a paper can go, and what each place actually is

> **READ THIS FIRST — 10 lines**
> 1. This page is the other half of the job: the four places a paper can go, what each one is, what it costs, and how to spot a fake venue.
> 2. The one thing: arXiv is a distribution channel, not a credential, and a non-archival workshop is the realistic first target.
> 3. Read it the week you pick a venue, and again before you pay anyone a fee.
> 4. Skip on a first pass: §4 tiers and rankings, and §7's travel and visa subsections.
> 5. There are four places: arXiv preprint (no review, only moderation), workshop (2-3 light reviews, sometimes none), conference and journal.
> 6. NeurIPS 2026 workshop rhythm: proposals in June, papers about 29 August, decision 29 September, event 11-13 December.
> 7. Real student costs: CODS 2026 is ₹5,000 plus 18% GST as an ACM member, ACL 2026 is $750, NeurIPS Paris is €380; virtual rates are 30-40% of in-person.
> 8. ICORE2026 lists 825 ranked venues and only 7.52% are A*; since 21 January 2026 arXiv no longer accepts an institutional email as the only endorsement.
> 9. Date-sensitive: every deadline, fee and rank here is for the 2026 cycle, verified 2026-11-03.
> 10. Full read about 32 minutes (7,100 words); the skim path in item 4 about 27 minutes.

**What this page is for.** Writing the paper is half the job; the other half is putting it where someone will read it, check it, and record it. This page covers the four kinds of place work appears, what arXiv really is, how review and rebuttal work, what it costs, and how to spot a fake venue. Every policy claim has a URL I opened on 2026-11-03. Where a page was behind a login or would not load, I say so and mark it UNCERTAIN instead of guessing.

---

## 1. The four places work appears

A "venue" is the place a paper is published or presented. There are four.

| | What it is | Peer review | Timeline (verified anchors) | Prestige | Archival? | Who it suits |
|---|---|---|---|---|---|---|
| **arXiv preprint** | Public PDF server, moderated | **None** — moderation checks topicality and standards only [1][2] | Submitted before 14:00 US Eastern → public ~20:00 same day [3] | Low as a credential | Effectively permanent once announced [4] | Everyone, as a *supplement*. Never the only place |
| **Workshop** | One-day event attached to a bigger conference | Light: 2–3 reviews, sometimes none | NeurIPS 2026: contributions ~29 Aug, decision 29 Sep, event 11–13 Dec [5][6] | Modest — "work in progress" | Either; see §3 | A first paper. Your realistic target |
| **Conference (main track)** | Main programme; proceedings via ACM/IEEE/Springer/ACL | Heavy: 3–4 reviews, area chair, rebuttal, meeting | NeurIPS 2026: submit 6 May, reviews 22 Jul, decision 24 Sep [7]. AAAI-27: submit 28 Jul, decision 30 Nov [8] | High — NeurIPS, ACL, AAAI are ICORE A* [9] | Yes | Work with a clear result and a real comparison |
| **Journal** | Periodic publication; no event, no travel | Heaviest per paper, but slow | TMLR and JOSS review continuously, no deadline [10][11] | High but slow to accrue | Yes | Extended work, or when you cannot travel |

Two things this hides. **Conference ≠ journal in CS:** in most fields the journal is the prize, but here the top conferences *are* the primary publication — which is why CS ranks conferences at all [9]. And **a preprint is not a publication** in the sense a scholarship committee means: citable, identified (arXiv:2410.01234), but unreviewed.

---

## 2. arXiv in detail

### 2.1 What it is

arXiv started in 1991, was founded by Paul Ginsparg, spent decades at Cornell, and became an independent nonprofit in 2026. It hosts over three million articles across eight subject areas, and submission is free [1]. The most important sentence on the site:

> "Material is not peer-reviewed by arXiv - the contents of arXiv submissions are wholly the responsibility of the submitter and are presented 'as is' without any warranty or guarantee." [1]

And from the moderation page:

> "Please note that the arXiv moderation process is not a peer-review process. arXiv staff and moderators cannot give feedback on the submission." [2]

A human with a PhD asks only "is this a real research paper in this area?" A wrong number stays wrong, permanently, with your name on it.

### 2.2 Endorsement — and the January 2026 change

This is the part that will bite you personally.

To submit your first paper to arXiv, or your first in a new category, you must be **endorsed**: a working scientist vouches you are a real researcher in that area.

**Who can endorse.** Endorsers must have authored a certain number of papers within the *endorsement domain* — the number varies by area, and only papers from three months to five years old count. They must hold an active positive endorsement themselves [12].

Before January 2026, an institutional email was usually enough. No longer:

> "As of January 21, 2026, arXiv will no longer accept institutional email addresses ... as the sole qualifier of endorsement for new authors." [13]

The first path now needs **both** an institutional email **and** prior authorship on a paper already in the endorsement domain you want [13].

The second path is personal endorsement. You start a submission, pick the category, and arXiv emails you an **endorsement request email** with a link for a prospective endorser. That person receives a **six-character alphanumeric endorsement code** from you, enters it on arXiv's form, and records yes or no. A no is a recorded negative vote; identity and comments stay private [12].

**For you:** with no arXiv paper, path one is closed. Path two needs a scientist who knows you or has read your draft — realistically a **faculty co-author** already publishing in cs.LG or cs.CL. Do not bulk-email strangers; arXiv calls that inappropriate [12], and staff cannot help: "arXiv staff cannot waive endorsement requirements or provide a personal endorsement for authors." [13]

### 2.3 What moderation rejects

arXiv declines submissions "in its sole discretion" [2], on these grounds:

- **Scholarly standards** — poorly prepared sections or figures, unprofessional or non-neutral language [2].
- **No scholarly interest** — no originality or significance; falsified or plagiarised content; misrepresented affiliation [2].
- **Not substantive research.** The policy names "course projects, research proposals, news" [2]. Your mini-project is not an arXiv paper unless it becomes a real study.
- **"In need of significant review and revision"** [2].
- **Rights** — your original work only; no referee comments pasted in [2].
- **Rate limit** — two new submissions per month, three active; one replacement per week after version 5 [2].

A journal publication does **not** guarantee arXiv accepts you [2].

### 2.4 AI content and authorship

Quoted because most venues now copy it:

> "1. continue to require authors to report in their work any significant use of sophisticated tools ... we now include in particular text-to-text generative AI among those that should be reported ... 2. ... by signing their name as an author of a paper, they each individually take full responsibility for all its contents, irrespective of how the contents were generated ... 3. generative AI language tools should not be listed as an author." [2]

Disclose significant AI use; own everything regardless of who typed it; never list a model as an author. If a tool invents a citation, that is your misconduct.

### 2.5 Versions, replacement, withdrawal

- Each submission gets a **date stamp** when you click submit [4].
- Once public, "each version of a work is considered a permanent part of the scientific record and may not be removed" [4].
- **Replacement** (v2, v3…) is for corrections and added references. State the reason in Comments, and merge the old comments or they are lost [14].
- **Withdrawal is not deletion.** It creates a *new version* marked withdrawn with your reason public; the PDF disappears from that version, but **all previous versions stay downloadable** [15].
- It is "not appropriate to withdraw a paper because it is published or submitted to a journal" (use a journal-ref) nor "because it is being updated" (use a replacement) [15].

Your v1 is forever. Post when the abstract and main table are numbers you trust.

### 2.6 Bottom line

arXiv is a **distribution channel**, not a credential. It gets work in front of people in 24 hours, free. It does not review you, and it is not a publication in institutional counting exercises [16][17]. Use it after you have a venue, not instead of one.

---

## 3. Workshops, conferences, journals — and "archival"

**A conference** has a deadline, a review round, a decision, a proceedings volume and a meeting. **A workshop** is smaller, usually one day, attached to a big conference, for work in progress: workshops "provide an informal, dynamic venue for discussion of work in progress" [5]. NeurIPS 2026 got 477 proposals and accepted 102 [18]. **A journal** has no event: you submit, wait, revise, and a PDF appears. TMLR uses "a rolling submission process", reviewed on OpenReview [10].

### Archival vs non-archival

**Archival** means the paper enters a permanent proceedings with an ISBN/DOI and counts as a publication. **Non-archival** means it is presented but not published; you keep the copyright and can submit an extended version elsewhere.

ACL's Student Research Workshop offers both: "Submissions (in both categories) may be archival or non-archival, based on the wish of the authors. All archival papers will be published in the ACL 2026 SRW Proceedings. Non-archival papers may be submitted to any venue in the future except for another SRW." [19]

CODS 2026 says the same from the other side: accepted papers "are eligible to be published in the conference proceedings. Authors may choose to withhold their paper from publication in case they wish to submit a completed version to a conference in future." [20]

An **archival** workshop paper spends the work — you cannot publish those results at a main conference later. **Non-archival** gets you the talk, the feedback and the CV line, and keeps the paper for a bigger venue. For a first paper, non-archival is almost always right.

### Why a workshop is the realistic first target

1. **The bar is "interesting", not "complete"** — workshops ask for work in progress [5].
2. **The format is shorter** — CODS asks for 4 pages [20], AAAI student abstracts 2 pages including references [21].
3. **Mentorship is built in** — ACL SRW runs pre-submission mentoring before review [19]: free reviewing.
4. **It is where you meet the people who will later review you properly.**

### Satellite deadlines: the pattern to memorise

For NeurIPS 2026: workshop **proposals** due 6 June, organisers notified 11 July, *suggested* workshop-paper deadline 29 August, **mandatory** accept/reject notification 29 September, workshops 11–12 December (Sydney) and 12–13 December (Paris, Atlanta) [5]. ICLR follows the same rhythm with a late-September paper deadline and December decisions [22].

So: **proposals in early summer → papers late August → decision late September → event in December.** To submit to a NeurIPS workshop you write in July and August. Dates shift by days, not months.

---

## 4. Tiers and rankings

### CORE / ICORE

CORE (now ICORE, "an international collaboration") ranks computing conferences [9]. The ICORE2026 round lists **825 ranked venues**: A* 7.52%, A 13.09%, B 30.18%, C 46.18% [9]. Official definitions [23]:

- **A\*** — flagship. "A* is not necessarily stronger in terms of (e.g.) citations but is recognised as a flagship conference, i.e. 'A* = A + flagship'".
- **A** — "Excellent". **B** — "good to very good". **C** — the floor for being ranked at all; venues below "the standard expected for rank C" are not accepted, and a venue needs at least 10 full research papers a year to qualify.
- A **National/Regional** tag means held in one country with a local chair; such venues "should be considered equivalent to B or C ranked venues", and the tag "means that the conference is weaker than A, but does not indicate whether it is B or C" [23].

Verified 2026-11-03: ACL A\*, NeurIPS A\*, AAAI A\*, EACL A, NAACL A [9].

**What ranks do NOT mean.** Not acceptance rates, not citations, not how much you will learn — the A\* definition says outright it is not about citations [23]. A B venue that three people in your subfield read beats an A\* where you are poster #4,102.

CORE stopped ranking journals: **the journal database was discontinued from March 2022** [24]. A site claiming "CORE A journal" makes an uncheckable claim.

### h5-index and Google Scholar Metrics

Google Scholar Metrics reports an **h5-index** per venue: the largest *h* such that *h* articles published there in the last five complete years have at least *h* citations each, plus a median h5. The page is https://scholar.google.com/citations?view_op=top_venues [25].

I extracted no numbers from it: project rules forbid scraping Scholar and it blocks automation. **UNCERTAIN: no specific h5 value here** — do not quote one from this document. h5 gives a rough five-year view of usage; it is useless for new venues, niche venues and workshops.

### "Scopus-indexed" and "Web of Science-indexed"

These are **indexing facts, not quality ranks.** Scopus calls itself "a comprehensive abstract and citation database" with 100M+ records and 30.2k active serial titles [26]; Web of Science is a family of indexes — SCIE, SSCI, ESCI, Conference Proceedings Citation Index [27]. Being in either means a database tracks the venue. It says nothing about acceptance rate or review quality. A journal can be in Scopus and still be a mill.

### Why rank is a weak proxy for fit

Rank answers "how central is this venue to its field?" It does not answer: will reviewers understand my method, will anyone cite me, can I afford it, does the deadline collide with exams, will a human reply to my email. **CODS** (ACM India's data-science conference) returns no ranked row in ICORE 2026, searched 2026-11-03 [9] — yet it is the best-fit venue here for you: Indian, cheap, open to bachelor's students, with travel grants [20][28]. Rank says skip it. Fit says submit.

---

## 5. How acceptance works, end to end

### The submission site

| System | Who runs it | What it feels like |
|---|---|---|
| **OpenReview** | Nonprofit; "configurable platform for peer review", free submissions [29] | Reviews often public after decision. Incomplete profile → desk rejection [30] |
| **HotCRP** | Used by "thousands of sites", strong USENIX presence [31] | Utilitarian, fast, text-heavy |
| **CMT** | Microsoft Research [32] | Common for vision and some IEEE events |
| **EasyChair** | 4.9M users, 125,944 conferences [33] | Common for workshops |

Two habits: create your profile **weeks** early (OpenReview profiles without an institutional email can take two weeks to moderate [30]), and enter co-author emails exactly as on their profiles.

### The pipeline

1. **Abstract deadline**, 2–7 days before the paper deadline; it exists to recruit reviewers, and missing it can lock you out (NeurIPS 2026: abstracts 4 May, papers 6 May) [7].
2. **Desk rejection** — no review, for formatting, anonymity, page limits, dual submission or incomplete profiles. CVPR: "Papers that are not properly anonymized, or do not use the template, or have more than eight pages (excluding references) will be rejected without review." [34] ICML 2026 added **cascading** desk rejections: abuse by one paper can take down all papers by any of its authors [35].
3. **Reviewer assignment** — area chairs match papers by expertise and conflicts; an incomplete OpenReview profile "risks desk rejection" [30][34].
4. **Scores** — typically 3–4 reviews on quality, clarity, significance, originality [36].
5. **Rebuttal** — §6.
6. **Area chair and decision meeting** — the AC writes a meta-review and argues your case; scores are advice, the AC decides.
7. **Notification** — NeurIPS 2026: 24 September [7]; AAAI-27: 30 November [8]; ACL 2026: 4 April [37].
8. **Camera-ready** — revised PDF on the publisher template. AAAI-27: 14 December 2026 [8]; ACL 2026: 19 April 2026 [37]. NeurIPS lets you buy one extra content page [30].
9. **Copyright form** — ACM/IEEE/ACL; read the open-access option first.
10. **arXiv posting** — check the venue's preprint policy. ACL has had **no anonymity period** since 15 February 2024, so a non-anonymous preprint is fine while under review [38]. Others differ.
11. **Registration and presentation** — ACL 2026: "All papers must be registered for presentation by May 11"; "Papers not properly registered will not be included in the program or proceedings" [39].

### Double-blind review, precisely

The reviewer does not know who wrote the paper; the author does not know who reviewed it [38]:

> "Papers must not include authors' names and affiliations. Furthermore, self-references that reveal the authors' identities, e.g., 'We previously showed (Smith, 1991)…' must be avoided. Instead, use citations such as 'Smith previously showed (Smith, 1991)…'"

> "Supplementary materials, including any links to repositories, should also be anonymized. Links to file hosting services that can track downloads, such as Dropbox, are not allowed."

> "Submissions that violate these requirements will be desk rejected."

CVPR adds: "Authors are not allowed to include external links (e.g., to webpages, images, or videos) in submissions, supplementary material, and rebuttal, when the links expand content and subvert the reviewing process." [34]

**Five mistakes that break anonymity.**

1. **"Our previous work [12] showed…"** → "Rao et al. [12] showed…". The citation stays; the "our" goes.
2. **A GitHub link.** `github.com/shubhsaxena/paper-code` is your name. Use an anonymised repository or a zip in supplementary material [38].
3. **Acknowledgements.** "We thank Prof. X at PSIT" identifies institution and person. Delete for submission, restore in camera-ready.
4. **Self-identifying metadata** — the PDF author field, the filename `shubh_camera_ready.pdf`, an Overleaf link carrying your username.
5. **Talking about the submission.** CVPR prohibits saying a paper is "under submission to CVPR"; even a webpage saying so can count as a violation [40].

Two things it does not protect you from: reviewers guessing ("a small Indian college writing about Hindi OCR"), and venues that are single-blind by design (most journals). Write as if your name were visible, because it may be.

---

## 6. Rebuttal

The rebuttal ("author response", "author feedback") is written after the reviews, before the decision — the only place to correct a reviewer who misread you.

**Length.** Assume one page. CVPR 2026: "the rebuttal is limited to a one-page PDF file using the rebuttal template ... Responses longer than one page will simply not be reviewed. This includes responses where the margins and formatting are deemed to have been significantly altered." [34] Shrinking the font discards the whole response, not trims it.

Some venues use a discussion period instead. NeurIPS 2026 ran an "Author + Reviewer + AC Discussion Period" from 27 July to 3 August [7]; AAAI-27 has an author feedback window in late October [8]; ARR uses a character-limited box on OpenReview.

**Structure.**
- **Opening, 3–4 lines:** thank reviewers, restate the contribution in one sentence, name the two or three changes you will make. Do not re-argue the paper.
- **One block per substantive concern**, in the reviewers' order: quote the concern in italics, answer in 2–4 sentences, state exactly what changed ("we added the ablation in Table 4, +0.8 F1").
- **A table of small fixes** — typos, missing citations, clarifications, one line each.
- **Closing, 2 lines:** what the paper will say after revision.

**Fight** factual errors ("the reviewer says we did not compare to X; we do, Table 2 row 4"), misreads of your method, and a claim that you lack an experiment you ran.

**Do not fight** taste: "the reviewer thinks the problem is unimportant" is not winnable in 500 words and arguing it makes you look defensive. Acknowledge, explain the choice in one sentence, move on. Never fight scores or imply a reviewer is incompetent.

**Tone.** Write to a tired person who read nine papers today. Short sentences, no adjectives about your own work. If a reviewer is right, say "the reviewer is right, we will fix this" — that buys more credibility than a page of defence.

One hard rule: **no new results in a rebuttal** unless the venue allows it; CVPR discourages new contributions and unrequested experiments [40].

---

## 7. Money and travel

This is where a good paper dies for an Indian student.

### Registration, in real numbers (verified 2026-11-03)

| Venue | Category | Early | Late |
|---|---|---|---|
| ACL 2026, San Diego | Student, full conference, presenting | **$750** | $900 |
| ACL 2026 | Student, 2-day workshop only | $450 | $600 |
| ACL 2026 | Student, 1-day workshop only | $350 | $500 |
| ACL 2026 (virtual) | Student, full conference | $300 | $450 |
| ACL 2026 | ACL student membership (required, extra) | $50 | — |
| NeurIPS 2026, Paris | Student, conference + tutorials + workshops | **€380** | €480 |
| NeurIPS 2026, Paris | Student, workshops only | €130 | €180 |
| CODS 2026, Gandhinagar | Student author, ACM member | **₹5,000** + 18% GST | — |
| CODS 2026 | Student author, non-member | ₹6,000 + 18% GST | — |

Sources: [39] ACL; [41] NeurIPS Paris; [28] CODS. ACL notes food and beverage alone "can exceed $800 per full conference attendee" and that it "intentionally subsidize[s] student and academic registrations" [39]. NeurIPS 2026 in-person places **sold out**; each paper got one author place [42].

### Travel

**UNCERTAIN — estimate, not a verified price.** I found no official airfare source. Planning arithmetic only: return economy Delhi→US East Coast ≈ ₹70,000–₹1,20,000; Delhi→Paris ≈ ₹45,000–₹80,000. Hotel $120–$200/night for 5–7 nights, food $30–$50/day. A US trip lands at ₹1.5–2.5 lakh all-in. Check a booking site before quoting a number.

### The visa reality

**United States.** Attending a conference is an explicitly permitted B-1 activity: the State Department lists "Attend a scientific, educational, professional, or business convention or conference" under Business (B-1) [43][44]. The application fee is **$185**, on form DS-160. An interview is "generally required for visa applicants with certain limited exceptions", so plan on attending one [43].

**An acceptance letter is evidence, not permission.** The consular officer decides whether you qualify and may interview any applicant [43]; NeurIPS warns that even with a visa, "it is possible that immigration officers at U.S. points of entry may require you to undergo additional screening" [45]. A first-time Indian student applicant with an invitation and no travel history faces real refusal risk. Apply 3–4 months early with invitation letter, registration receipt, proof of enrolment, bank statements and a return ticket.

**Europe (Schengen).** India is visa-required; the short-stay visa covers "up to 90 days in any 180-day period" across all 29 Schengen countries [46]. **UNCERTAIN: the EU visa-fees page would not load on 2026-11-03, so no fee is quoted here.** Check the consulate of the country hosting the conference.

Get invitation letters early. NeurIPS generates them only for registered attendees and stops after the conference closes [45].

### The four funded paths

**1. Student volunteers — usually free registration.** AAAI: "A limited number of complimentary technical program registrations will be available for students who volunteer during the conference." Eligibility: full-time undergraduate or graduate students, AAAI members, who "submitted paper(s) to the conference program AND letter(s) of recommendation from their faculty advisor." Applications for AAAI-27 run 30 November – 4 December 2026, and the page warns not to register before hearing back, "otherwise you will forfeit their complementary registration" [47].

**2. Travel grants.** ACL 2026 SRW grant applications closed 8 May 2026, notification 20 May [19]; CODS offers "partial travel Grants ... for all students whose papers are accepted" [20]; NeurIPS Financial Assistance covers registration, virtual registration and "prepaid accommodation" [18].

**3. Present remotely.** ICML 2026 made attendance **optional**: authors may present or "just wish to include their paper in the proceedings (without presentation)", with "at least one of the authors must obtain virtual registration" [48]. NeurIPS 2026 allows only "a maximum of 1-hour remote presentation ... in case of unforeseen emergencies" per workshop [5] — a fallback, not a right.

**4. Virtual rates** run 30–40% of in-person student rates: ACL $300 vs $750; NeurIPS Paris workshops-only €130 vs €380 [39][41].

If your visa is refused, check the refund rule first. NeurIPS refunds in full before 4 November 2026, then converts you to virtual and refunds the difference **if** you applied by 20 October [49].

Cheapest realistic path: an Indian venue (₹5,000–6,000), then a virtual registration abroad, then in person only when a grant covers it.

---

## 8. Student tracks and student-focused venues

**ACL Student Research Workshop.** The most student-centred venue in NLP, aimed at students "at multiple stages of their education, including highschool, undergraduate, MSc/MA, junior and senior PhD students" [19]. Two categories: thesis proposals, and research papers where "the first author MUST BE a current student"; archival or non-archival by choice. For ACL 2026: submission 18 March, notification 24 April, camera-ready 8 May, mentorship 4 February [19]. The mentorship is the prize — free feedback before review.

**AAAI Student Abstract and Poster Program.** "Open to all students at the Undergraduate, Masters, and Doctoral levels." Advisors may be co-authors, but students "should honor the spirit of the program by submitting only work for which they are primary investigators." Format: "no longer than 2 pages including references" in AAAI two-column style, plus a supplementary file up to 20 MB. For AAAI-26: abstract 15 September 2025, notification 30 October, camera-ready 13 November [21]. AAAI is A\* [9] — a 2-page door at a top venue.

**ACM Student Research Competition.** Runs *inside* ACM SIG conferences; in the year described, 21 SIG conferences took part with "more than 342 student participants". You submit an abstract, present a poster, and if you place, present again, judged on "knowledge of their research area, contribution of the research, and the quality of the oral and visual presentation" [50].

**CODS Young Researchers' Symposium (India).** For students "currently pursuing PhD/ Masters/ Bachelors" [20]. 4-page extended abstract, first author must be a current student, work-in-progress welcome, partial travel grants for all accepted students, best-paper award, mentorship events. For CODS 2026: submission 20 August, decision TBD (originally 6 October 2026, now listed as "October 6, 2026 TBD"), camera-ready 18 November [20]. If you submit to one thing this year, make it this.

**MIT Undergraduate Research Technology Conference.** "An internationally-renowned research conference for undergraduates and by undergraduates" [51]. Technical paper deadline 9 August 2026, notification 28 August; poster and lightning-talk deadline 4 September. It is in Cambridge, Massachusetts, so cost is the barrier, but the bar is set for undergraduates.

One caution: some programmes have conditions a 17-year-old first-year may not meet. AAAI's volunteer programme needs AAAI membership and a submitted paper [47]; NeurIPS requires in-person attendees to be "14 years of age or older" and to attend with an adult [52]. Read the eligibility sentence first.

---

## 9. Predatory venues: a 10-point check

A predatory venue takes your money and gives you a fake publication. It is not a bad venue; it is a business selling the *appearance* of one. Indian students get targeted because our emails are public on college sites and our institutions reward publication counts. Score one point per red flag; **three or more: walk away.**

1. **Guaranteed acceptance, or a decision in days.** Real review takes months — NeurIPS took 6 May → 24 September [7].
2. **Money asked before review.** Legitimate venues charge after acceptance; an invoice at submission is the business model.
3. **Fees hidden or vague.** TCS asks: "Does the journal site explain what these fees are for and when they will be charged? ... Do they mention the currency and amount of any fees?" [53]
4. **No findable editorial board.** TCS: "Is the publisher offering a review by an expert editorial board or by researchers in your subject area?" [53] If names do not exist in a search, stop.
5. **Fake metrics.** "Universal Impact Factor 4.9", "ICV 98.7", "Global Impact Factor" are invented indices. UGC says journals displaying "misleading and/or false metrics ... will not be eligible" for its list [16]. A claimed "CORE A journal" rank cannot be real — CORE stopped ranking journals in March 2022 [24].
6. **A templated name.** Long, generic, unGoogleable, easily confused with a real journal. TCS: "the name is unique; it is not the same or easily confused with another journal" [53].
7. **Spelling and grammar errors on the homepage.** A venue that cannot proofread its call for papers will not proofread yours; arXiv lists "appropriate standards of scholarly communication" for exactly this reason [2].
8. **No peer-review description.** TCS: "Does the website mention whether the process involves independent/external reviewers, how many reviewers per paper?" [53] "Fast double-blind review by eminent reviewers", with no names, is not a description.
9. **Spam invitations.** Unsolicited "Dear Researcher" emails offering a keynote you never applied for are marketing. Real conferences do not recruit speakers by bulk mail.
10. **No verifiable indexing.** Check DOAJ [54] and Scopus's own source list or Clarivate's Master Journal List — not the journal's homepage [26][27].

### The authorities

**Think. Check. Submit.** (https://thinkchecksubmit.org/) is the cross-industry campaign run by publishers, librarians and research bodies. Its checklist asks: do you know the journal; can you identify and contact the publisher; is the review type clear; are articles indexed and archived; are fees clear; are guidelines provided; is the publisher in a recognised initiative such as COPE [53]. Its best line for a beginner: a trustworthy journal "doesn't guarantee acceptance or a very short peer review time" [53].

**Beall's List** (https://beallslist.net/) is an archived list of potential predatory publishers, originally by librarian Jeffrey Beall. The site is explicit: "This is an archived version of the Beall's list ... We will only update links and add notes to this list." Method: find the publisher in the site footer or "About" section and search that name, with the warning that "All journals published by a predatory publisher are potentially predatory unless stated otherwise" [55].

Use it as a **pointer, not a verdict**. Absence proves nothing; presence means look harder.

**Beall-style red flags:** you are invited to be an editor by unsolicited email; the "impact factor" is calculated by the publisher; the board lists people who have never heard of the journal; the APC is waived "for a limited time"; submissions go to an email address.

**On conferences:** a predatory conference spams, charges $600 for "registration" with no proceedings, puts "IEEE" in the title without IEEE technical co-sponsorship, and gives every attendee an award. Check last year's proceedings in a real digital library. If they do not exist, this year's will not either.

---

## 10. The Indian context

### UGC-CARE — most advice you will get is out of date

UGC-CARE was the UGC's list of approved journals, created to fight predatory publishing. **It has been discontinued.** The site now carries this banner:

> "The UGC-CARE List has not been updated since October 2024 and will not be updated further, as per the UGC Public Notice dated February 11, 2025. The website is available for information purposes only." [16]

The follow-up notice of 16 July 2025 made the status precise. UGC approved "Suggestive Parameters for choosing Peer-Reviewed Journals" and the uploading of "a list of 1474 UGC CARE listed journals as on 10 February, 2025, for referencing purposes", then stated:

> "This list of UGC-CARE Journals (now discontinued) is intended to serve as a reference resource only; the inclusion or exclusion of a journal in this list does not imply validation or endorsement by the Commission." [17]

So **UGC-CARE is a reference list, not a mandate.** If a senior says "it must be a UGC-CARE journal", that instruction is out of date. What replaced it is Annexure-1 of that notice — suggestive parameters on title, ISSN, periodicity, review transparency, domain, editorial board, APC transparency, timeline, acceptance rate and citation record [17]. That annexure is a ready-made checklist.

**To check a journal now:** the ISSN portal, DOAJ [54], Scopus's source list or Clarivate's Master Journal List [26][27], then the ten-point check above.

### Scopus and Web of Science

Both are indexes [26][27]. Three practical facts: most good CS conferences are indexed through their publisher's proceedings, not individually; "Scopus-indexed" is claimed loosely and must be verified on Elsevier's own list; and an ESCI listing is weaker than SCIE, both weaker than "the people in my field read this".

### NIRF and what it measures

NIRF is the Ministry of Education's institutional ranking. For Engineering 2025 the weights are: Teaching, Learning & Resources 0.30; **Research and Professional Practice 0.30**; Graduation Outcomes 0.20; Outreach and Inclusivity 0.10; Perception 0.10 [56].

Inside that research block of 100 marks: **Publications 35, Quality of Publications 40, IPR and Patents 15, Footprint of Projects 10** [56].

Publications are therefore **75 of the 100 research marks** — a structural reason for your college to want faculty publishing. But NIRF scores the **institution's** output; a student's workshop paper contributes nothing measurable.

### AICTE

AICTE funds research through schemes like the Research Promotion Scheme, "aimed to create research ambience in the institutes by promoting research in engineering sciences". Eligibility: an "AICTE approved Technical Institution/University Department with relevant PG programme" and "**Full time regular faculty** with research experience and publications" [57]. Students cannot apply. The honest answer to "can AICTE fund my project" is no — but a faculty member with an RPS grant can fund you as project staff or co-author.

### What this means for you

Almost nothing, and that is good news. UGC-CARE, Scopus, WoS, NIRF and AICTE govern **institutional accounting**: promotions, rankings, funding eligibility. None reviews your paper, so none changes where you should submit.

Your objective function differs from your college's: reviewers who understand the work, a deadline that fits around exams, a cost near zero, and a CV line a supervisor can verify by clicking a link. A 4-page abstract at CODS [20] serves that better than a paid "publication" in a journal NIRF would not count anyway. Some Indian PhD committees still ask "is it Scopus indexed?" You will have a better answer — a peer-reviewed venue with public proceedings.

---

## 11. Ten realistic target venue types

Deadlines are the ones I verified for the cycle named. The years shift; the *pattern* is what you plan around.

| # | Type | Real example | Deadline pattern (verified cycle) | Cost | Rigour | Why it fits |
|---|---|---|---|---|---|---|
| 1 | **arXiv preprint** (step 1, not a venue) | arXiv cs.LG — https://arxiv.org | Anytime; before 14:00 ET → public ~20:00 same day [3] | Free [1] | None [2] | A citable link and fast feedback. Needs an endorser [12][13] |
| 2 | **Student research workshop at a top NLP conference** | ACL 2026 SRW — https://2026.aclweb.org/calls/student_research_workshop/ | Mentorship early Feb; submission mid-March; decision late April [19] | Virtual student $300 [39] | Medium: 2–3 reviews + mentor | Open to undergraduates, with pre-submission mentoring [19] |
| 3 | **Student abstract at a top AI conference** | AAAI-26 Student Abstract — https://aaai.org/conference/aaai/aaai-26/student-abstract-and-poster-program-call/ | Abstract mid-September; decision late October; camera-ready mid-November [21] | Student registration | Medium | 2 pages including references; undergraduate-eligible; A* venue [21][9] |
| 4 | **Young Researchers' Symposium, Indian ACM conference** | CODS 2026 YRS — https://ikdd.acm.org/cods-2026/call-for-young-researchers-symposium-papers.php | Submission late August; decision TBD (listed "October 6, 2026 TBD"); camera-ready mid-November [20] | ₹5,000–6,000 + GST [28] | Medium; travel grants [20] | Bachelor's students eligible; in India; cheapest real option |
| 5 | **ACM Student Research Competition** | https://src.acm.org/ | Follows the host conference; 21 SIG conferences participate [50] | Host registration | Medium; judged poster + talk | Built for undergraduates; expert feedback [50] |
| 6 | **Undergraduate research conference** | MIT URTC — https://urtc.mit.edu/ | Paper early August; poster/lightning talk early September; event October [51] | Registration + US travel | Medium | By and for undergraduates; poster track is a low bar [51] |
| 7 | **Non-archival workshop at a major ML conference** | NeurIPS 2026 workshops — https://neurips.cc/Conferences/2026/CallForWorkshops | Proposals June; contributions late August; decision late September [5] | NeurIPS student; Paris €380 [41] | Light–medium | Work-in-progress welcome; non-archival keeps the paper free [5][19] |
| 8 | **Rolling journal (no deadline)** | TMLR — https://jmlr.org/tmlr/ ; JOSS — https://joss.theoj.org/about | Any day; decisions rolling [10] | Free to submit [11] | High (TMLR); medium (JOSS) | No deadline to miss during exams; TMLR values correctness over significance [10] |
| 9 | **Short paper at a main conference** | ACL 2026 short papers (4 pages) — https://2026.aclweb.org/calls/main_conference_papers/ | Submit early January; decision early April [37] | Virtual student $300 [39] | High | A focused negative result or small study fits 4 pages [38] |
| 10 | **Datasets / evaluations / reproducibility track** | NeurIPS 2026 Evaluations & Datasets — https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets | Same as main: abstract 4 May, full 6 May, decision 24 Sep [7] | Main conference | High | A careful reproduction or a small clean dataset is a real contribution |

Rows 2, 3, 4 and 5 are what to attempt this year; rows 8 and 9 are what you do with the same work twelve months later; row 1 is a step, not a target.

Caveat on row 3: the AAAI-27 URL still serves AAAI-21 content, so eligibility and format were verified from the AAAI-26 call [21]. **UNCERTAIN whether AAAI-27 changes the 2-page limit.**

---

## Sources

All retrieved 2026-11-03 unless stated. Every URL below was opened and read while writing this page.

1. arXiv, "About arXiv" — https://info.arxiv.org/about/index.html
2. arXiv, "arXiv moderation" — https://info.arxiv.org/help/moderation/index.html
3. arXiv, "Submission guidelines" — https://info.arxiv.org/help/submit/index.html
4. arXiv, "Submission Version Availability" — https://info.arxiv.org/help/versions.html
5. NeurIPS 2026, "Guidance for NeurIPS Workshop Proposals" — https://neurips.cc/Conferences/2026/WorkshopsGuidance
6. NeurIPS 2026, "Call for Workshops" — https://neurips.cc/Conferences/2026/CallForWorkshops
7. NeurIPS 2026, "Dates and Deadlines" — https://neurips.cc/Conferences/2026/Dates
8. AAAI-27, "Main Technical Track Call" — https://aaai.org/conference/aaai/aaai-27/main-technical-track-call/
9. ICORE Conference Portal (ICORE2026 database) — https://portal.core.edu.au/conf-ranks/
10. Transactions on Machine Learning Research — https://jmlr.org/tmlr/
11. Journal of Open Source Software, "About" — https://joss.theoj.org/about
12. arXiv, "The arXiv endorsement system" — https://info.arxiv.org/help/endorsement.html
13. arXiv blog, "Attention Authors: updated endorsement policy" (21 Jan 2026) — https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/
14. arXiv, "Submit a new version of a work" — https://info.arxiv.org/help/replace.html
15. arXiv, "Withdrawing an article" — https://info.arxiv.org/help/withdraw.html
16. UGC-CARE site notice on discontinuation — https://ugccare.unipune.ac.in/site/website/index.aspx
17. UGC Public Notice, 16 July 2025, "Suggestive Parameters for choosing Peer-Reviewed Journals" (PDF) — https://www.ugc.gov.in/pdfnews/6124898_Public-Notice-CARE-Journals.pdf
18. NeurIPS blog, "Announcing the NeurIPS 2026 Workshops" (477 proposals, 102 accepted; Financial Assistance) — https://blog.neurips.cc/2026/08/10/announcing-the-neurips-2026-workshops/
19. ACL 2026, "Student Research Workshop" — https://2026.aclweb.org/calls/student_research_workshop/
20. CODS 2026, "Call for Young Researchers' Symposium Papers" — https://ikdd.acm.org/cods-2026/call-for-young-researchers-symposium-papers.php
21. AAAI-26, "Student Abstract and Poster Program: Call for Proposals" — https://aaai.org/conference/aaai/aaai-26/student-abstract-and-poster-program-call/
22. ICLR 2027, conference page and important dates — https://iclr.cc/Conferences/2027
23. CORE, "ICORE 2026 Rankings Updates" (rank definitions) — https://www.core.edu.au/icore-portal/icore-portal-2026-rankings-updates
24. CORE, "CORE Rankings Portal" (journal DB discontinued March 2022) — https://www.core.edu.au/conference-portal
25. Google Scholar Metrics (cited as a pointer; not scraped) — https://scholar.google.com/citations?view_op=top_venues
26. Elsevier, "Scopus" product page — https://www.elsevier.com/products/scopus
27. Clarivate, "Web of Science platform" — https://clarivate.com/academia-government/scientific-and-academic-research/research-discovery-and-referencing/web-of-science/
28. CODS 2026, "Conference Registration" (rates) — https://ikdd.acm.org/cods-2026/registration.php
29. OpenReview, "About OpenReview" — https://openreview.net/about
30. NeurIPS 2026, "Main Track Handbook" (V2026.3) — https://neurips.cc/Conferences/2026/MainTrackHandbook
31. HotCRP.com — https://hotcrp.com/
32. Microsoft CMT — https://cmt3.research.microsoft.com/
33. EasyChair — https://easychair.org/
34. CVPR 2026, "Author Guidelines" — https://cvpr.thecvf.com/Conferences/2026/AuthorGuidelines
35. ICML blog, "What's New in ICML 2026 Peer Review" — https://blog.icml.cc/2026/01/08/whats-new-in-icml-2026-peer-review/
36. NeurIPS 2026, "Reviewing Guidelines" — https://neurips.cc/Conferences/2026/ReviewerGuidelines
37. ACL 2026, "Main Conference call for papers" — https://2026.aclweb.org/calls/main_conference_papers/
38. ACL Rolling Review, "Call for Papers" (two-way anonymised review; preprint policy) — https://aclrollingreview.org/cfp
39. ACL 2026, "Registration" (fees, membership, deadlines) — https://2026.aclweb.org/registration/
40. CVPR 2027, "Author Guidelines" (anonymity FAQ; rebuttal policy) — https://cvpr.thecvf.com/Conferences/2027/AuthorGuidelines
41. NeurIPS 2026 Paris, "Registration fees" — https://neurips-europe.cc/
42. NeurIPS 2026, "Author Registration" (one place per paper; sold out) — https://neurips.cc/Conferences/2026/AuthorRegistration
43. U.S. Department of State, "Visitor Visa" (B-1/B-2; $185 fee; interview) — https://travel.state.gov/content/travel/en/us-visas/tourism-visit/visitor.html
44. U.S. Department of State, "FACT SHEET: U.S. Business Visas (B-1)" — https://travel.state.gov/content/travel/en/us-visas/business/b-1-fact-sheet.html
45. NeurIPS 2026, "Visa Information" — https://neurips.cc/Conferences/2026/Visa
46. European Commission, "EU visa policy" (Schengen 90/180) — https://home-affairs.ec.europa.eu/policies/schengen-borders-and-visa/visa-policy_en
47. AAAI-27, "Student Scholar Volunteer Program" — https://aaai.org/conference/aaai/aaai-27/student-scholar-volunteer-program/
48. ICML 2026, "Call For Papers" (attendance optional; proceedings-only) — https://icml.cc/Conferences/2026/CallForPapers
49. NeurIPS 2026, "Pricing" (cancellation and visa-refund policy) — https://neurips.cc/Conferences/2026/Pricing
50. ACM Student Research Competition — https://src.acm.org/
51. MIT Undergraduate Research Technology Conference — https://urtc.mit.edu/
52. NeurIPS 2026, "Registration" (minors policy) — https://neurips.cc/Register/view-registration
53. Think. Check. Submit., "Journals" checklist — https://thinkchecksubmit.org/journals/
54. Directory of Open Access Journals — https://doaj.org/
55. Beall's List of Potential Predatory Journals and Publishers — https://beallslist.net/
56. NIRF, "India Rankings 2025 — Methodology (Engineering)" (PDF) — https://www.nirfindia.org/nirfpdfcdn/2025/framework/Engineering.pdf
57. AICTE Research Promotion Scheme, eligibility — https://www.indiascienceandtechnology.gov.in/programme-schemes/research-and-development/aicte-research-promotion-scheme-rps?language=en

---

## How confident is this?

- **Solid.** arXiv policy — endorsement, moderation, AI use, versions, withdrawal — is quoted verbatim from arXiv's own pages [1]–[15]. The January 2026 endorsement change [13] is the most consequential fact here for Shubh: a college email alone no longer earns endorsement.
- **Solid.** Fees, dates and rebuttal rules are transcribed from the current cycle pages for ACL 2026, NeurIPS 2026, AAAI-27, CVPR 2026/2027, ICLR 2027 and CODS 2026 [7][8][19][20][21][22][28][34][37][39][41]. ICORE rank definitions and the 825-venue distribution come from CORE's own 2026 update page [9][23].
- **Solid.** UGC-CARE's discontinuation is confirmed twice: the site banner [16] and the July 2025 UGC notice with the "reference resource only ... does not imply validation or endorsement" wording [17]. NIRF weights are from the 2025 Engineering methodology PDF [56].
- **UNCERTAIN — airfare and hotel costs.** No official source; the ₹70,000–₹1,20,000 and $120–$200 figures in §7 are labelled estimates. Re-check against a booking site.
- **UNCERTAIN — Schengen visa fee.** The EU visa-fees page would not load on 2026-11-03, so no amount is quoted.
- **UNCERTAIN — h5-index values.** By design I extracted nothing from Google Scholar Metrics (project rule: no scraping Scholar). Only the definition is given.
- **UNCERTAIN — AAAI student abstract format for AAAI-27.** That URL still serves AAAI-21 content; the 2-page format and undergraduate eligibility were verified from the AAAI-26 call [21].
- **Date-sensitive everywhere.** Every deadline belongs to the cycle named beside it. Nothing here should be used to plan a submission without opening the current-year CFP.

last_updated: 2026-11-03
