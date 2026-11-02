# Claims evidence sheet — 20 consequential claims in 00_foundations

What this page is for: the head review said that a URL loading is not the same as a URL supporting the sentence we wrote. This sheet takes the 20 claims in `00_foundations/` that would cost Shubh money, eligibility or an integrity finding if they were wrong, and for each one quotes the sentence we published, the sentence the live page actually carries, and a verdict. Every source was re-read on 2026-11-03. Where the page was weaker than our sentence, the document was changed and the new sentence is printed here.

**Summary.** Of 20 claims: **17 SUPPORTED**, **3 PARTLY**, **0 NOT SUPPORTED**, **0 UNVERIFIED**. The three partials were all cases of our prose being stronger than the page — a heading that said "will not" where arXiv says "typically not" (E2), an SRFP affiliation requirement that is not on the SRFP page (E14), and a DAAD semester rule that is not in the DAAD brochure we cite (E17). Three further sentences were corrected inside otherwise-supported claims: a stale CODS decision date, an overstated ACM "rewrite", and a Keshav timing given without his "for beginners" qualifier. No claim was deleted; no citation was swapped for a new URL.

| ID | Claim (short) | File | Verdict |
|---|---|---|---|
| E1 | arXiv endorsement, 21 Jan 2026; 6-character code | VENUES §2.2 | SUPPORTED |
| E2 | arXiv rejects "undergraduate or high school research" | ETHICS §1 | PARTLY — softened |
| E3 | UGC-CARE discontinued, reference only | VENUES §10, GLOSSARY | SUPPORTED |
| E4 | CORE stopped ranking journals, March 2022 | VENUES §4, §9 | SUPPORTED |
| E5 | ACM AI policy, 14 May 2026, methods disclosure | ETHICS §2 | SUPPORTED |
| E6 | NeurIPS 2026 agents/LLMs paragraph | ETHICS §2 | SUPPORTED |
| E7 | ICML 2025 generative-AI paragraph | ETHICS §2 | SUPPORTED |
| E8 | ACL: disclose in Acknowledgements | ETHICS §2 | SUPPORTED |
| E9 | IEEE AI-generated-text policy | ETHICS §2 | SUPPORTED |
| E10 | COPE position on authorship and AI | ETHICS §2 | SUPPORTED |
| E11 | ACL 2026 student fees ($750/$900, $50 membership) | VENUES §7 | SUPPORTED |
| E12 | NeurIPS 2026 Paris student fees (€380/€480) | VENUES §7 | SUPPORTED |
| E13 | CODS 2026 fees; bachelor's-eligible YRS | VENUES §7, §8 | SUPPORTED |
| E14 | SRFP: BCA in years II and III only | WHAT-A-PAPER §4 | PARTLY — qualifier removed |
| E15 | INSPIRE-SHE excludes Computer Applications | WHAT-A-PAPER §4 | SUPPORTED |
| E16 | Mitacs: 18+, two years completed | WHAT-A-PAPER §4 | SUPPORTED |
| E17 | DAAD WISE: 5th/6th semester | WHAT-A-PAPER §4 | PARTLY — downgraded to UNCERTAIN |
| E18 | NIRF research weights 35/40/15/10 of 30% | VENUES §10 | SUPPORTED |
| E19 | US B-1 for conferences; $185 | VENUES §7 | SUPPORTED |
| E20 | Keshav's three-pass method | HOW-TO-WRITE-ONE §2 | SUPPORTED |

---

## E1 — arXiv endorsement after 21 January 2026

**Our sentence** (`VENUES-AND-PUBLISHING.md`, §2.2 "Endorsement — and the January 2026 change", lines 60–62):

> "The first path now needs **both** an institutional email **and** prior authorship on a paper already in the endorsement domain you want [13]. … That person receives a **six-character alphanumeric endorsement code** from you, enters it on arXiv's form, and records yes or no."

**Source URL** (from that file's Sources, [13] and [12]):
https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/ and https://info.arxiv.org/help/endorsement.html

**What the page says** (HTTP 200, direct fetch, 2026-11-03):

> "As of January 21, 2026, arXiv will no longer accept institutional email addresses (i.e., an email address associated with an academic or research institution) as the sole qualifier of endorsement for new authors."

> "The first path requires both 1) an institutional email address from an academic/research institution and 2) previous authorship on an existing paper which has been accepted to the arXiv "endorsement domain" * they wish to submit to (see paper ownership)."

From the endorsement help page (HTTP 200):

> "If an author asks you for endorsement, they will send you a six-character alphanumeric endorsement code."

**Verdict: SUPPORTED.** Date, both conditions, the six-character code and the recorded negative vote are all on the two pages. No change.

---

## E2 — arXiv and "undergraduate or high school research"

**Our sentence** (`ETHICS-AND-AI-USE.md`, §1 "The short version", line 20, and §"The 17-year-old problem", line 75):

> "**arXiv will not take your paper yet.** "Undergraduate or high school research" sits on its list of content types that are typically not accepted [2]."

**Source URL** ([2]): https://info.arxiv.org/help/policies/content-types.html

**What the page says** (HTTP 200, direct fetch, 2026-11-03):

> "In general, the guidelines below represent what types of content are and are not accepted. Content types that are typically NOT accepted include … Undergraduate or high school research"

and, in the Theses section:

> "Undergraduate or Master's level researchers should consult their advisor before submitting to arXiv."

**Verdict: PARTLY.** The list entry is verbatim. But the page says *typically* not accepted, in a paragraph that calls the list a guideline, and it separately contemplates undergraduates submitting. Our heading "will not take your paper yet" turned a moderation tendency into a prohibition. That matters because a reader could conclude arXiv is closed to him, when the operative advice is "not as an undergraduate research report; yes as a real article, after review elsewhere".

**Corrective action:** softened both occurrences and added the advisor sentence as the page's own escape hatch. New sentence (line 20):

> "**arXiv usually will not take your paper yet.** arXiv's policy page lists "Undergraduate or high school research" among the "Content types that are typically NOT accepted" [2]. It is a moderation guideline, not a rule that names you, but plan for it: a workshop or student track first, arXiv after a conventional publication."

New sentence (line 75):

> "**arXiv does not want undergraduate work as such.** "Undergraduate or high school research" sits among "Content types that are typically NOT accepted", next to course projects and "Proposals for future research" [2]. This is a statement about the *content type*, not about who you are — the accepted list includes ordinary articles, and the Theses section adds that "Undergraduate or Master's level researchers should consult their advisor before submitting to arXiv". Post after a workshop or conference has accepted the work."

---

## E3 — UGC-CARE is discontinued / reference-only

**Our sentence** (`VENUES-AND-PUBLISHING.md`, §10 "UGC-CARE — most advice you will get is out of date", line 338; also `GLOSSARY.md`, "UGC-CARE"):

> "UGC-CARE was the UGC's list of approved journals, created to fight predatory publishing. **It has been discontinued.** The site now carries this banner:"

**Source URLs** ([16], [17]): https://ugccare.unipune.ac.in/site/website/index.aspx and https://www.ugc.gov.in/pdfnews/6124898_Public-Notice-CARE-Journals.pdf

**What the pages say** (both HTTP 200, direct fetch; the PDF read with a text extractor, 2026-11-03):

> "The UGC-CARE List has not been updated since October 2024 and will not be updated further, as per the UGC Public Notice dated February 11, 2025. The website is available for information purposes only."

> "This list of UGC-CARE Journals (now discontinued) is intended to serve as a reference resource only; the inclusion or exclusion of a journal in this list does not imply validation or endorsement by the Commission."

**Verdict: SUPPORTED.** The word "discontinued" is UGC's own, in the 16 July 2025 notice; the banner confirms no further updates. Both quoted blocks in our document match character for character. No change.

---

## E4 — CORE stopped ranking journals in March 2022

**Our sentence** (`VENUES-AND-PUBLISHING.md`, §4 "CORE / ICORE", line 146):

> "CORE stopped ranking journals: **the journal database was discontinued from March 2022** [24]. A site claiming "CORE A journal" makes an uncheckable claim."

**Source URL** ([24]): https://www.core.edu.au/conference-portal

**What the page says** (HTTP 200, direct fetch, 2026-11-03):

> "ACCESS THE CORE JOURNAL DB HERE DISCONTINUED FROM MARCH 2022"

> "The CORE Journal Rankings were discontinued in 2022 due to limited resources."

**Verdict: SUPPORTED.** Month and reason are on CORE's own page; the conference database is still live, which is why the distinction between "ICORE A*" (checkable) and "CORE A journal" (not) is the right one to make. No change.

---

## E5 — ACM authorship policy, updated 14 May 2026

**Our sentence** (`ETHICS-AND-AI-USE.md`, §2 "The venue policies, quoted", ACM subsection):

> "ACM rewrote its policy on 14 May 2026 and moved opposite to most venues:"

**Source URL** ([3]): https://www.acm.org/publications/policies/new-acm-policy-on-authorship

**What the page says** (HTTP 403 to a plain request — bot-blocked; read in full via `web_extract`, 2026-11-03):

> "Updated on May 14, 2026"

> "1. When using Artificial Intelligence to conduct research, including the design and methodology of the research project, creation and selection of data sources, designing experiments, generation and collection of data, coding, implementing models, running simulations, data analysis, testing, validating results, deploying software, archiving data and code for reproducibility, or any other aspects of the research lifecycle that are directly relevant to the conclusions of the research underlying the Work, the specific use(s) of AI tools must be described in detail in the methods section of the Work."

> "2. When using Artificial Intelligence to assist with writing an ACM submission, ACM no longer requires the disclosure of information regarding the use of AI (as distinct from AI used in the conduct of the research itself, addressed in item 1 above)."

**Verdict: SUPPORTED.** The date, the methods-section rule and the dropped writing-disclosure rule are all exact. One word was ours, not ACM's: the page says the policy was "Updated", and "rewrote" overstates a revision whose structure (authorship criteria, accountability, submission criteria) is unchanged.

**Corrective action:** "rewrote" changed to "updated", with the page's own date string quoted beside it:

> "ACM updated its authorship policy on 14 May 2026 ("Updated on May 14, 2026" on the page) and moved opposite to most venues:"

---

## E6 — NeurIPS 2026 on authors' use of agents and LLMs

**Our sentence** (`ETHICS-AND-AI-USE.md`, §2, NeurIPS subsection — presented as a quotation):

> "We expect authors to document their methodology clearly … The use of agents and/or LLMs in implementing the method should be described in the experimental setup section (or equivalent) if it is an important, original, or non-standard component of the approach …"

**Source URL** ([7]): https://neurips.cc/Conferences/2026/MainTrackHandbook

**What the page says** (HTTP 200, direct fetch, 2026-11-03), under the heading "Author Use of Agents and Large Language Models (LLMs)":

> "We expect authors to document their methodology clearly for upholding scientific rigorousness and transparency standards. The use of agents and/or LLMs in implementing the method should be described in the experimental setup section (or equivalent) if it is an important, original, or non-standard component of the approach e.g. if the paper is about using an LLM as a search heuristic. The use of spell checkers and grammar suggestions, aid for editing purposes, and basic code assistance does not need to be documented."

> "There have been many cases of hallucinated citations in literature review, which violates the NeurIPS Code of Conduct. It is the author's responsibility to verify the tools are used in a scientifically responsible manner. Relatedly, as you are the one taking responsibility for the work, agents and LLMs cannot be authors."

**Verdict: SUPPORTED.** Quoted verbatim, including the ellipses we marked. No change.

---

## E7 — ICML 2025 "Use of Generative AI"

**Our sentence** (`ETHICS-AND-AI-USE.md`, §2, ICML subsection — quoted):

> "Authors are allowed to use generative AI tools such as Large Language Models (LLMs) to assist in writing or research. However, authors must take full responsibility for all content in their paper … LLMs are not eligible for authorship."

**Source URL** ([9]): https://icml.cc/Conferences/2025/CallForPapers

**What the page says** (HTTP 200, direct fetch, 2026-11-03), heading "Use of Generative AI":

> "Authors are allowed to use generative AI tools such as Large Language Models (LLMs) to assist in writing or research. However, authors must take full responsibility for all content in their paper, including any content generated by AI tools that might be construed as plagiarism or scientific misconduct. We encourage authors to explain any notable ways in which these tools were used in their research methodology. LLMs are not eligible for authorship."

**Verdict: SUPPORTED.** Exact. Our gloss that this is "encourage", not "must", is also correct on the page's own verb. No change.

---

## E8 — ACL publication ethics on AI disclosure

**Our sentence** (`ETHICS-AND-AI-USE.md`, §2, ACL subsection — quoted; and the table row "ACL | No [11] | Acknowledgements [11]"):

> "Generative AI tools and technologies may not be listed as authors of a submission, and any use of generative AI tools and technologies to create content … should be fully disclosed in the Acknowledgements section …"

**Source URL** ([11]): https://www.aclweb.org/adminwiki/index.php/ACL_Policy_on_Publication_Ethics

**What the page says** (HTTP 200, direct fetch, 2026-11-03), under "Guidelines for Generative Assistance in Authorship":

> "Generative AI tools and technologies may not be listed as authors of a submission, and any use of generative AI tools and technologies to create content, whether to support research or in review rebuttals, should be appropriate and should be fully disclosed in the Acknowledgements section - for instance, "Section 3 was written with inputs from ChatGPT.""

Followed by:

> "Any use not listed below is considered inappropriate use."

**Verdict: SUPPORTED.** Exact, including the venue of disclosure and the "any use not listed" closure that our paraphrase relies on. No change.

---

## E9 — IEEE policy on AI-generated text

**Our sentence** (`ETHICS-AND-AI-USE.md`, §2, IEEE subsection — quoted):

> "The use of content generated by artificial intelligence (AI) in an article (including but not limited to text, figures, images, and code) shall be disclosed in the acknowledgments section …"

**Source URL** ([5]): https://open.ieee.org/author-guidelines-for-artificial-intelligence-ai-generated-text/

**What the page says** (HTTP 200, direct fetch, 2026-11-03; page dated April 16, 2024):

> "The use of content generated by artificial intelligence (AI) in an article (including but not limited to text, figures, images, and code) shall be disclosed in the acknowledgments section of any article submitted to an IEEE publication. The AI system used shall be identified, and specific sections of the article that use AI-generated content shall be identified and accompanied by a brief explanation regarding the level at which the AI system was used to generate the content."

> "The use of AI systems for editing and grammar enhancement is common practice and, as such, is generally outside the intent of the above policy. In this case, disclosure as noted above is recommended."

**Verdict: SUPPORTED.** Exact; our advice that IEEE wants tool name, section and level follows the second and third sentences of the policy. No change.

---

## E10 — COPE position on authorship and AI tools

**Our sentence** (`ETHICS-AND-AI-USE.md`, §2, COPE subsection — quoted; table row "COPE (journals) | No [13] | Materials and Methods [13]"):

> "Authors who use AI tools in the writing of a manuscript, production of images or graphical elements of the paper, or in the collection and analysis of data, must be transparent in disclosing in the Materials and Methods (or similar section) of the paper how the AI tool was used and which tool was used."

**Source URL** ([13]): https://publicationethics.org/guidance/cope-position/authorship-and-ai-tools

**What the page says** (HTTP 403 to a plain request — bot-blocked; read via `web_extract`, 2026-11-03):

> "AI tools cannot meet the requirements for authorship as they cannot take responsibility for the submitted work. As non-legal entities, they cannot assert the presence or absence of conflicts of interest nor manage copyright and license agreements."

> "Authors who use AI tools in the writing of a manuscript, production of images or graphical elements of the paper, or in the collection and analysis of data, must be transparent in disclosing in the Materials and Methods (or similar section) of the paper how the AI tool was used and which tool was used. Authors are fully responsible for the content of their manuscript, even those parts produced by an AI tool, and are thus liable for any breach of publication ethics."

**Verdict: SUPPORTED.** Both blocks exact. Note the fetch was via a reader service because direct requests are blocked; the text is COPE's page text, not a summary. No change.

---

## E11 — ACL 2026 student registration fees

**Our sentence** (`VENUES-AND-PUBLISHING.md`, §7 "Registration, in real numbers (verified 2026-11-03)", table):

> "| ACL 2026, San Diego | Student, full conference, presenting | **$750** | $900 | … | ACL 2026 | ACL student membership (required, extra) | $50 | — |"

**Source URL** ([39]): https://2026.aclweb.org/registration/

**What the page says** (HTTP 200, direct fetch, 2026-11-03):

> "IP - Full Conference - Registering Paper Student $750.00 $900.00"

> "IP - 2 Day Workshop Only - Registering Paper Student $450.00 $600.00"

> "IP - 1 Day Workshop Only - Registering Paper Student $350.00 $500.00"

> "V - Full Conference - Registering Paper Student $300.00 $450.00"

> "All conference attendees must be current ACL members for 2026. So, in addition to the registration fee, each registration will incure the following fees if not already a paid 2026 member: … $50 for Students"

The page also refers to "the San Diego venue".

**Verdict: SUPPORTED.** All five rows match, including the membership charge, which is the number most easily missed. Early/late cut-offs ($750 until 26 May AoE, $900 to 30 June) are consistent with the table's two columns. No change.

---

## E12 — NeurIPS 2026 Paris student fees

**Our sentence** (`VENUES-AND-PUBLISHING.md`, §7 table):

> "| NeurIPS 2026, Paris | Student, conference + tutorials + workshops | **€380** | €480 | … | NeurIPS 2026, Paris | Student, workshops only | €130 | €180 |"

**Source URL** ([41]): https://neurips-europe.cc/

**What the page says** (HTTP 200, direct fetch, 2026-11-03):

> "Conference sessions, tutorials, workshops & competitions — Student 380 € 480 €"

> "Workshops & competitions — Student 130 € 180 €"

> "EARLY … Until October 30, 2026 (CET) … STANDARD … From October 31, 2026 (CET)"

**Verdict: SUPPORTED.** Both pairs exact, both columns correctly labelled early/standard. No change.

---

## E13 — CODS 2026 fees and the bachelor's-eligible track

**Our sentence** (`VENUES-AND-PUBLISHING.md`, §7 table and §8 "CODS Young Researchers' Symposium"):

> "| CODS 2026, Gandhinagar | Student author, ACM member | **₹5,000** + 18% GST | — |" and "For students "currently pursuing PhD/ Masters/ Bachelors" [20]."

**Source URLs** ([28], [20]): https://ikdd.acm.org/cods-2026/registration.php and https://ikdd.acm.org/cods-2026/call-for-young-researchers-symposium-papers.php

**What the pages say** (both HTTP 200, direct fetch, 2026-11-03):

> "Student (ACM Member) 5000 100 3,500 75 … Student (Non-Member) 6000 125 5,000 100 * 18% GST will be added to registration rates"

> "The Young Researchers' Symposium at CODS 2026 invites extended abstract submissions from students who are currently pursuing PhD/ Masters/ Bachelors."

The main site confirms the venue: "Dhirubhai Ambani Institute of Information and Communication Technology, Gandhinagar", conference dates 13–16 December 2026.

**Verdict: SUPPORTED** for the fees, the GST and the bachelor's eligibility. One adjacent number in the same paragraph was stale: the YRS page now reads "October 6, 2026 TBD : Final decision notifications (Accept / Reject)", while our text said decisions land on 6 October.

**Corrective action** (adjacent claim, same paragraph): decision date changed to TBD, with the old value kept visible. New sentences:

> "For CODS 2026: submission 20 August, decision TBD (originally 6 October 2026, now listed as "October 6, 2026 TBD"), camera-ready 18 November [20]."

and in the ranked table: "Submission late August; decision TBD (listed "October 6, 2026 TBD"); camera-ready mid-November [20]".

---

## E14 — IAS-INSA-NASI SRFP: BCA in years II and III only

**Our sentence** (`WHAT-A-PAPER-DOES-FOR-YOU.md`, §4 "Scholarships and fellowships", SRFP row):

> "Students in **BCA II and III year only**; ≥65% average in core subjects from Class X onwards; college must be UGC/AICTE-affiliated or an accredited institution [15]"

**Source URL** ([15]): https://webjapps.ias.ac.in/fellowship2027/application_instructions.jsp

**What the page says** (HTTP 200, direct fetch, 2026-11-03), §B Eligibility Criteria:

> "6a) Applicants should be studying in one of the following: … BE / BTech / BCA (II and III years only) …"

> "The minimum percentage of average marks in core subjects only (i.e. excluding languages ) from X std. up to post-graduation (whichever years completed) should be 65% or above for students."

The page also requires "the contact details of one of their present teachers" and mark sheets from Class X. It does **not** contain the strings "UGC", "AICTE" or "affiliated" anywhere.

**Verdict: PARTLY.** The BCA year rule and the 65% rule are verbatim and are the load-bearing facts. The affiliation condition is not on the cited page — it appears to have been carried over from a general assumption about Indian fellowship programmes. It is the kind of clause that makes a student think he is disqualified, so it had to go.

**Corrective action:** deleted the unsupported clause and replaced it with a requirement the page does state. New sentence:

> "Students in **BCA II and III year only** ("BE / BTech / BCA (II and III years only)"); ≥65% average in core subjects from Class X onwards; one teacher's contact for the recommendation [15]"

The second SRFP row (§5 timing table) was tightened at the same time, because "apply by 30 November of the preceding year" was our inference; the page states one date: "The last date for receipt of applications online is 30 November 2026."

---

## E15 — INSPIRE-SHE excludes Computer Applications by name

**Our sentence** (`WHAT-A-PAPER-DOES-FOR-YOU.md`, §4, INSPIRE-SHE row):

> "enrolled in B.Sc./B.S./Int. M.Sc./M.S. in one of 18 listed natural-science subjects. The FAQ explicitly excludes **Computer Applications** [14]"

**Source URL** ([14]): https://online-inspire.gov.in/Content/SHEFAQs.pdf

**What the page says** (HTTP 200 with TLS verification disabled — the site serves a certificate chain Python rejects; PDF text extracted with pypdf, 2026-11-03):

> "The following subjects under Basic and Natural Sciences are within the scope of INSPIRE Scholarship for pursuing B.Sc./B.S./Int. M.Sc./Int. M.S. courses: (1) Physics (2) Chemistry (3) Mathematics (4) Biology (5) Statistics (6) Geology (7) Astrophysics (8) Astronomy (9) Electronics (10) Botany (11) Zoology (12) Biochemistry (13) Anthropology (14) Microbiology (15) Geophysics (16) Geochemistry (17) Atmospheric Sciences & (18) Oceanic Sciences."

> "Courses other than these subjects such as … Computer Science, Computer Applications, … are NOT supported."

**Verdict: SUPPORTED.** Eighteen subjects, and "Computer Applications" named in the exclusion list. The same document carries the money: "12,000 scholarships (From SHE -2017 batch onwards), each valued at [rupee sign] 80,000/- are announced annually" (the rupee glyph does not survive PDF text extraction). No change.

---

## E16 — Mitacs Globalink: 18+ and two years completed

**Our sentence** (`WHAT-A-PAPER-DOES-FOR-YOU.md`, §4, Mitacs row):

> "**At least 18 years old at the time of application**; enrolled full-time at an eligible institution; at least two years of undergraduate study completed; one to three semesters remaining as of the fall of the application year; India is a participating country [16]"

**Source URL** ([16]): https://www.mitacs.ca/our-programs/globalink-research-internship-students/

**What the page says** (HTTP 200, direct fetch, 2026-11-03), "Eligibility requirements for 2027":

> "Be at least 18 years of age at the time of application"

> "Be enrolled in a full-time undergraduate or combined undergraduate/master's program at an eligible institution"

> "Applicants must have completed at least two years of undergraduate study or be in be enrolled in the second year of their current program (see requirement by country)"

> "Have one to three semesters remaining in their program as of fall 2027"

**Verdict: SUPPORTED.** Every clause is present. Our `UNCERTAIN` note about fitting a 3-year BCA into the "one to three semesters remaining" rule stands and is correctly flagged, because the page sets the rule per country rather than explaining 3-year degrees. No change.

---

## E17 — DAAD WISE: 5th or 6th semester of a 4-year degree

**Our sentence** (`WHAT-A-PAPER-DOES-FOR-YOU.md`, §4, DAAD WISE row):

> "Indian students in the **5th or 6th semester of a 4-year bachelor's**, at **selected Indian universities** [24]"

**Source URL** ([24]): https://www.daad.in/files/2025/05/A-New-Passage-to-India-Brochure_____Pdf_compressed.pdf

**What the page says** (HTTP 200, PDF text extracted with pypdf, 61 pages, 2026-11-03):

> "The Working Internships in Science and Engineering (WISE) scholarship programme for individuals, where undergraduates from selected Indian universities are introduced to Germany as a destination for academic studies and research at an early stage by receiving the opportunity to support German doctoral students and university teachers in their work."

That is the only substantive WISE eligibility sentence in the brochure. The word "semester" appears four times in 61 pages, none of them about WISE eligibility; "5th" and "6th" do not appear in connection with WISE at all.

**Verdict: PARTLY.** The brochure supports "undergraduates from selected Indian universities" and nothing more. The 5th/6th-semester rule is real in circulation — DAAD host-institute pages and study-abroad blogs state it — but it is not in the source we cite, and a blog may not be the authority under our own writing spec. Citing the brochure for it was a mis-attribution even though the conclusion (not a route for a 3-year BCA at a non-partner college) survives on the brochure's own words.

**Corrective action:** the semester rule is now marked `UNCERTAIN` and attributed to nothing, and the brochure is quoted for exactly what it says. New sentence:

> "DAAD's India brochure says WISE places "undergraduates from selected Indian universities" in German labs; it does not state a semester rule [24]. The commonly quoted "5th or 6th semester of a 4-year degree" is `UNCERTAIN`: it appears on DAAD host-institute pages and study-abroad blogs, not in the brochure, and DAAD's scholarship-database entry would not load on 2026-11-03"

The confidence note in the same file was rewritten to match, and now says plainly that "The "5th/6th semester" figure that circulates online is not in the source we cite".

---

## E18 — NIRF research weights

**Our sentence** (`VENUES-AND-PUBLISHING.md`, §10 "NIRF and what it measures", lines 356–360):

> "For Engineering 2025 the weights are: Teaching, Learning & Resources 0.30; **Research and Professional Practice 0.30**; Graduation Outcomes 0.20; Outreach and Inclusivity 0.10; Perception 0.10 [56]." … "Inside that research block of 100 marks: **Publications 35, Quality of Publications 40, IPR and Patents 15, Footprint of Projects 10** [56]."

**Source URL** ([56]): https://www.nirfindia.org/nirfpdfcdn/2025/framework/Engineering.pdf

**What the page says** (HTTP 403 to a plain request — bot-blocked; read via `web_extract`, 2026-11-03):

> "1 Teaching, Learning & Resources 100 0.30 / 2 Research and Professional Practice 100 0.30 / 3 Graduation Outcomes 100 0.20 / 4 Outreach and Inclusivity 100 0.10 / 5 Perception 100 0.10"

> "2. Research and Professional Practice (RP) Ranking weight: 0.30 … A. Combined metric for Publications (PU): 35 marks B. Combined metric for Quality of Publications (QP): 40 marks C. IPR and Patents: Published and Granted (IPR): 15 marks D. Footprint of Projects and Professional Practice (FPPP): 10 marks"

**Verdict: SUPPORTED.** All nine numbers match, in the right pillar. The arithmetic in our next sentence (35 + 40 = 75 of 100 research marks) is ours, done on NIRF's marks, and is correct. No change.

---

## E19 — US B-1 visa for attending a conference, and the fee

**Our sentence** (`VENUES-AND-PUBLISHING.md`, §7 "The visa reality"):

> "Attending a conference is an explicitly permitted B-1 activity: the State Department lists "Attend a scientific, educational, professional, or business convention or conference" [43][44]. The application fee is **$185**, on form DS-160, with an in-person interview [43]."

**Source URL** ([43]): https://travel.state.gov/content/travel/en/us-visas/tourism-visit/visitor.html

**What the page says** (HTTP 403 to a plain request — bot-blocked; read via `web_extract`, 2026-11-03):

> "Business (B-1): Consult with business associates / Attend a scientific, educational, professional, or business convention or conference / Settle an estate / Negotiate a contract"

> "**Fees - Pay the non-refundable visa application fee** … $185"

> "Interviews are generally required for visa applicants with certain limited exceptions. Consular officers may require an interview of any visa applicant."

**Verdict: SUPPORTED** for the category and the fee. "With an in-person interview" was stated as unconditional; the page qualifies it.

**Corrective action:** the sentence now carries the page's own qualifier rather than a flat requirement. New sentence:

> "Attending a conference is an explicitly permitted B-1 activity: the State Department lists "Attend a scientific, educational, professional, or business convention or conference" under Business (B-1) [43][44]. The application fee is **$185**, on form DS-160. An interview is "generally required for visa applicants with certain limited exceptions", so plan on attending one [43]."

---

## E20 — Keshav's three-pass method

**Our sentence** (`HOW-TO-WRITE-ONE.md`, §2, line 87):

> "First pass, 5–10 minutes — title, abstract, intro, headings, conclusions … Second pass, an hour — figures, tables, method … Third pass, 4–5 hours — only for the two or three papers you must reimplement or beat."

**Source URL** ([1]): https://web.stanford.edu/class/ee384m/Handouts/HowtoReadPaper.pdf

**What the page says** (HTTP 200, PDF text extracted with pypdf, 3 pages, 2026-11-03):

> "The key idea is that you should read the paper in up to three passes, instead of starting at the beginning and plowing your way to the end."

> "This pass should take about five to ten minutes and consists of the following steps: 1. Carefully read the title, abstract, and introduction 2. Read the section and sub-section headings, but ignore everything else …"

> "The second pass should take up to an hour. After this pass, you should be able to grasp the content of the paper. You should be able to summarize the main thrust of the paper, with supporting evidence, to someone else."

> "This pass can take about four or five hours for beginners, and about an hour for an experienced reader."

**Verdict: SUPPORTED** for the method and all three timings. Two of our words were not Keshav's: "an hour" for the second pass drops his "up to", and "4–5 hours" for the third pass drops "for beginners".

**Corrective action:** both qualifiers restored. New sentence:

> "First pass, 5–10 minutes — title, abstract, intro, headings, conclusions; decide whether it is relevant at all. Second pass, up to an hour — figures, tables, method; you should be able to summarise it aloud. Third pass, four or five hours (Keshav's figure "for beginners"; he says about an hour for an experienced reader) — reserve it for the small number of papers you must reimplement or beat."

---

## What this sheet does not cover

- It does not re-verify the 60-odd other citations in `00_foundations/`. It covers the 20 claims named by the head plus the sentences immediately adjacent to them.
- Fee pages change without notice. Every number here was read on 2026-11-03 and should be re-read before any application is filed.
- Four sources (ACM, COPE, NIRF, travel.state.gov) refuse plain automated requests. They were read through a text-extraction reader, which returns page text without browser rendering; that is a weaker read than a browser session but stronger than a link check, and no quote here depends on a rendering-only element such as a table image.

## Sources

All read 2026-11-03 (IST). Status recorded per claim above; "200" means an HTTP 200 to a direct request with a descriptive User-Agent.

1. arXiv blog, "Attention Authors: updated endorsement policy", 21 Jan 2026 — https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/ (200)
2. arXiv, "The arXiv endorsement system" — https://info.arxiv.org/help/endorsement.html (200)
3. arXiv, "Policies for specific content types" — https://info.arxiv.org/help/policies/content-types.html (200)
4. UGC-CARE portal notice — https://ugccare.unipune.ac.in/site/website/index.aspx (200)
5. UGC Public Notice, 16 July 2025 — https://www.ugc.gov.in/pdfnews/6124898_Public-Notice-CARE-Journals.pdf (200, PDF)
6. CORE Rankings Portal — https://www.core.edu.au/conference-portal (200)
7. ACM, "ACM Policy on Authorship" (Updated on May 14, 2026) — https://www.acm.org/publications/policies/new-acm-policy-on-authorship (403 direct; read via web_extract)
8. NeurIPS 2026, "Main Track Handbook" — https://neurips.cc/Conferences/2026/MainTrackHandbook (200)
9. ICML 2025, "Call For Papers" — https://icml.cc/Conferences/2025/CallForPapers (200)
10. ACL, "ACL Policy on Publication Ethics" — https://www.aclweb.org/adminwiki/index.php/ACL_Policy_on_Publication_Ethics (200)
11. IEEE, "Author Guidelines for AI-Generated Text", 16 April 2024 — https://open.ieee.org/author-guidelines-for-artificial-intelligence-ai-generated-text/ (200)
12. COPE, "Authorship and AI tools" — https://publicationethics.org/guidance/cope-position/authorship-and-ai-tools (403 direct; read via web_extract)
13. ACL 2026, "Registration" — https://2026.aclweb.org/registration/ (200)
14. NeurIPS 2026 Paris, "Registration fees" — https://neurips-europe.cc/ (200)
15. CODS 2026, "Conference Registration" — https://ikdd.acm.org/cods-2026/registration.php (200)
16. CODS 2026, "Call for Young Researchers' Symposium Papers" — https://ikdd.acm.org/cods-2026/call-for-young-researchers-symposium-papers.php (200)
17. CODS 2026 home (venue and dates) — https://ikdd.acm.org/cods-2026/ (200)
18. Indian Academy of Sciences, SRFP 2027 "Instructions to Applicants" — https://webjapps.ias.ac.in/fellowship2027/application_instructions.jsp (200)
19. DST, INSPIRE-SHE FAQs — https://online-inspire.gov.in/Content/SHEFAQs.pdf (200 with TLS verification disabled; PDF)
20. Mitacs, Globalink Research Internship, students page — https://www.mitacs.ca/our-programs/globalink-research-internship-students/ (200)
21. DAAD, "A New Passage to India" brochure — https://www.daad.in/files/2025/05/A-New-Passage-to-India-Brochure_____Pdf_compressed.pdf (200, PDF)
22. NIRF, "India Rankings 2025 — Methodology (Engineering)" — https://www.nirfindia.org/nirfpdfcdn/2025/framework/Engineering.pdf (403 direct; read via web_extract)
23. U.S. Department of State, "Visitor Visa" — https://travel.state.gov/content/travel/en/us-visas/tourism-visit/visitor.html (403 direct; read via web_extract)
24. S. Keshav, "How to Read a Paper" — https://web.stanford.edu/class/ee384m/Handouts/HowtoReadPaper.pdf (200, PDF)

## How confident is this?

- **Solid.** 17 of 20 claims are supported by a sentence that says the same thing in the same words. The quotes above were copied from the fetched page text on 2026-11-03, not reconstructed from memory.
- **Solid.** The three corrections are conservative: one heading softened, one unsupported clause deleted, one unsourced rule demoted to `UNCERTAIN`. No claim was strengthened to match a source, and no source was replaced with a friendlier one.
- **Solid.** The four bot-blocked sources were read through a text extractor, not a browser. Their key sentences are plain body text in `<p>` elements, so the risk of a rendering artefact is low, but a browser session would be the stronger read.
- **Weaker.** Fees and deadlines are the least stable facts here. ACL, NeurIPS, CODS and the State Department can all change a number without changing the page's structure; re-read before filing anything.
- **UNCERTAIN.** DAAD WISE's semester rule is now unresolved rather than wrong. Someone should open DAAD's scholarship database entry in a browser (it would not load today) or write to DAAD India, and then either cite it or leave it out.
- **Not covered.** Whether PSIT's own BCA scheme includes Mathematics or Statistics — still open, still matters for NIMCET, and no web source can settle it.

last_updated: 2026-11-03
