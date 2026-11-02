# What a Paper Does For You (And What It Doesn't)

**What this page is for.** An honest accounting of what one undergraduate research paper changes for a BCA student in India — in MCA and MS admissions, in PhD applications abroad, in scholarships and internships — and what it does not change. Every eligibility rule below was checked against the programme's own page on 2026-11-03. Where a rule could not be confirmed, it says `UNCERTAIN` instead of guessing.

Written for you specifically: 17 now, 18 in December 2026, first-semester BCA at PSIT College of Higher Education (college code KN162, affiliated to Chhatrapati Shahu Ji Maharaj University, Kanpur) [1]. Your BCA runs 2026–2029, so "Year 1" means 2026-27, "Year 2" means 2027-28, "Year 3" means 2028-29. I use those labels throughout, because almost every rule below is a rule about which year you are in.

---

## 1. The honest version, first

A single paper, written by one undergraduate at a college without a research lab, published at a workshop or mid-tier venue, changes less than the internet implies.

What it actually does: it proves to a stranger that you can finish a long, boring, self-directed task. It gives a professor something concrete to write in a letter ("she ran the experiments, found the bug in the baseline, rewrote the evaluation"). It teaches you the loop — read, implement, measure, write, respond to criticism — which is the actual skill. And it gives you twenty minutes of interview material that is not coursework.

What it does not do: it does not get you into an MCA programme, because MCA admission is decided by an entrance rank, and no NIT admissions office reads your publication list before your NIMCET rank [2][3]. It does not raise your GATE score by a mark. It does not pay for anything. It does not make you employable on its own — a company hiring a junior developer wants to know whether you can build and ship software, and a PDF on a workshop site is weaker evidence than a repository someone can clone and run.

**The counter-intuitive part.** For a student in your position, a good public GitHub repository or a real internship can matter more than one workshop paper, and it is not close.

A repository is checkable in ninety seconds: a reviewer or a professor deciding whether to take you for a summer can click, read your code, and see whether anyone found it useful. A workshop paper is checkable only if the reader trusts the venue, and many readers have never heard of it. A two-month internship produces the thing admissions committees actually weigh: a letter from someone who watched you work. Neither requires a publication, and both are harder to fake.

**The actively harmful case.** A bad publication is worse than no publication. "Predatory" journals accept almost anything for a fee, review nothing, and are indexed nowhere that matters. Publishing in one signals that you cannot tell a real venue from a fake one — which is a bad signal for someone who claims to want a research career. In an interview the question "why did you publish there?" has no good answer. There is also a harder risk: a paper built on fabricated results or copied text can be retracted, and a retraction follows your name permanently. RULES.md exists in this repo because the failure mode is common, not hypothetical.

So the correct mental model is: **the paper is a by-product of doing research, not a trophy you acquire by paying a fee.** If the research is real, the artifact (code, data, write-up) is worth more than the certificate.

---

## 2. Indian admissions: where a paper counts, and where it is noise

Four routes are relevant to you. They have almost nothing in common.

### 2.1 MCA — the route you will most likely take

MCA admission in India runs on entrance exams. Three sub-routes:

- **NIMCET** — one national test for MCA at 11 NITs and 2 IIITs (Agartala, Allahabad, Bhopal, Delhi, Jamshedpur, Kurukshetra, Meghalaya, Patna, Raipur, Tiruchirappalli, Warangal, plus IIIT Bhopal and IIIT Vadodara) [3]. Eligibility in the 2026 brochure: at least 60% aggregate or 6.5 CGPA on a 10-point scale (55%/6.0 for SC/ST/PwD) in **any undergraduate programme of at least three years' duration with Mathematics or Statistics as one of the subjects**, or a B.E./B.Tech [2]. A BCA qualifies **only if your BCA transcript actually contains Mathematics or Statistics**. This is the single most consequential administrative detail on this page: check your syllabus, and if maths is not there, ask your department now, in first year, not in 2029. `UNCERTAIN: whether the CSJM University BCA syllabus that PSIT CHE follows includes a Mathematics or Statistics paper — the syllabus page on psitche.ac.in was not reachable on 2026-11-03, and this must be confirmed from your own scheme of examination.`
- **CUET-PG** — the National Testing Agency's postgraduate test, used by central and many state universities. MCA is one of the programmes admitted this way; the Central University of Karnataka, for example, published a CUET(PG)-2026 merit list for its MCA programme [4][5]. Registration typically opens around December and the exam runs in March.
- **University's own entrance or merit** — CSJM University and most state universities run their own MCA admission. `UNCERTAIN: CSJM's mode for 2027 onwards; check csjmu.ac.in, not aggregator sites.`

**Effect of a publication on any of these: essentially zero.** Rank decides. A publication appears nowhere in the NIMCET or CUET-PG scoring rules [2][5]. It can matter in a marginal way at an interview-based selection (some universities interview for MCA seats), and it matters if you later apply for a research position from your MCA.

### 2.2 M.Sc. / MS by research

A taught M.Sc. in Computer Science or Data Science usually wants a B.Sc. with mathematics; whether a BCA is accepted varies by department and is often decided case by case. A **research** MS (IISc's M.Tech (Research), IIT research programmes) is a different animal: it is a supervised research degree, and the selection is an interview in front of people who will ask what you have read and what you have built. That is the one Indian route where a paper helps meaningfully, because it is evidence for exactly the thing being assessed.

`UNCERTAIN: whether IISc and the IITs accept a BCA (rather than B.E./B.Tech/B.Sc./MCA) for their research programmes. The IISc research-programme admissions page lists eligible degrees per department and the answer differs by department [6]. Treat any claim that "BCA students can do an MS at IISc" as unverified until you have read the specific department's eligibility table.`

### 2.3 IIT/NIT M.Tech through GATE

GATE eligibility is broader than most people assume: candidates "currently studying in the 3rd or higher years of any undergraduate degree program" or holding a government-approved degree in Engineering/Technology/Architecture/Science/Commerce/Arts/Humanities may appear [7]. Read literally, that covers a BCA in its third year. But eligibility to *sit* GATE and eligibility to *be admitted* to a particular M.Tech are two different rules, and the second one is set by each institute. Most CSE M.Tech programmes expect a B.E./B.Tech in CSE/IT or an equivalent; several allow MCA or M.Sc. for specific specialisations.

`UNCERTAIN: which IIT/NIT M.Tech programmes in CSE would admit a BCA graduate with a good GATE CS score. This must be checked institute by institute, department by department, from the institute's own M.Tech admission page. Do not rely on coaching-centre blogs.`

A GATE score stays valid for three years [8], so a February 2029 score can still be used in 2031, after an MCA.

### 2.4 Summary table

| Route | What it is | Eligibility (verified) | Do you qualify now? | When you qualify |
|---|---|---|---|---|
| MCA at NITs/IIITs (NIMCET) | National entrance test for MCA at 11 NITs + 2 IIITs [3] | UG degree ≥3 years with Maths/Statistics as a subject; 60% or 6.5 CGPA [2] | No — you are in Year 1 | Final year: NIMCET 2029 (the 2026 cycle's brochure appeared in late February 2026) |
| MCA at central universities (CUET-PG) | NTA postgraduate entrance; MCA is a participating programme [4][5] | Bachelor's degree; university-specific minimum marks | No | Final year: apply ~Dec 2028, exam ~Mar 2029 |
| MCA at CSJM University / state universities | University's own entrance or merit | University-specific | No | Final year, 2029 — `UNCERTAIN` on mode |
| M.Sc. (CS/DS) | Taught master's | Usually B.Sc. with maths; BCA acceptance varies | No | After BCA, 2029 — check each department |
| MS by research / PhD (IISc, IITs) | Supervised research degree | Degree requirements per department [6] | No | Likely after MCA/M.Sc. — `UNCERTAIN` for BCA |
| M.Tech (GATE) | Taught master's with scholarship | GATE: 3rd year of any UG degree or a completed approved degree [7] | Eligible to sit GATE in Year 3; admission rules differ per institute | GATE Feb 2029 |
| CAT / MBA | Management entrance | Bachelor's degree; marks cut-off set by each institute | No | Not a research route — see §6 |

---

## 3. Foreign MS and PhD: what publications actually do there

### 3.1 What committees weigh

US CS PhD admissions are not a publication contest. Johns Hopkins' CS department says it plainly on its admissions FAQ: *"Do I need published research papers? No. While many of our applicants have publications demonstrating their research experience, we care more about what you did with the opportunities you were given... Each year we accept many students without prior publications and reject students with multiple publications"* [9].

What dominates instead: **research fit** (does your interest match a faculty member with funding and a slot this year — which is why applicants read recent papers and email professors), **letters** from people who supervised your research and can describe what you did when it went wrong, **transcripts and coursework** (can you survive the qualifying exams), and the **statement** (can you describe a problem precisely and say what you did about it).

A paper helps as *evidence inside the letters category*. It does not substitute for the letter, and a workshop paper from an unknown venue adds much less than a letter saying "she worked in my lab for ten weeks and here is what she found".

### 3.2 Timeline

Applications are due in **December of your final year**. Stanford's CS PhD deadline for autumn 2027 entry was 8 December 2026, with the portal opening in mid-September [10]. For you, that pattern means: if you apply straight out of BCA, you apply in December 2028 for an August 2029 start. If you do an MCA first (2029–2032), you apply in December 2031.

Straight-from-BCA PhD applications abroad are possible but rare, and for a 3-year non-engineering degree they are harder than the timelines suggest. The realistic sequence for most Indian students in your position is: BCA → MCA or M.Sc. (with research) → PhD, or BCA → MS abroad → PhD.

### 3.3 The 3-year bachelor's problem — read this twice

Stanford's stated requirement is that applicants from outside the US "must hold the equivalent of a United States Bachelor's degree" [11]. Whether a 3-year Indian BCA counts as equivalent is decided programme by programme, and in Germany it is assessed through the anabin database, which classifies foreign qualifications for the German system [12]. In practice: some US and European programmes accept a 3-year Indian bachelor's for a master's, some require four years, and a few require a master's before a PhD.

`UNCERTAIN: the general rule does not exist. There is no national policy — not in the US, not in Germany, not in the EU — that says "3-year Indian bachelor's: accepted" or "not accepted". Every programme decides, and the answer changes between departments of the same university.`

What to do about it, concretely:

- Search each programme's admissions page for "three-year", "3-year", "four-year bachelor" and "India". If it is silent, email the graduate coordinator one sentence: "I will hold a three-year BCA from an Indian university affiliated to CSJM University, Kanpur; is that acceptable for this programme?" Keep the reply.
- For Germany, check your degree in anabin before spending money on an application [12].
- A BCA is not an engineering degree. Many MS CS programmes publish prerequisite lists (data structures, algorithms, discrete mathematics, operating systems). Compare your syllabus against them in Year 1, while you can still choose electives.

### 3.4 Funding reality

In US CS PhD programmes, admitted students are normally funded, not self-funded: Cornell's CS PhD page states full support for the duration of the degree, through teaching assistantships, research assistantships, or fellowships [13]. That is the norm at research universities — you are paid a stipend and your tuition is waived, in exchange for teaching or research work.

Taught master's degrees (MS) are the opposite. They are usually full-fee, and funding is scarce and competitive. This asymmetry is the single biggest financial fact in this document: **a funded PhD costs you nothing and pays a stipend; a self-funded MS can cost tens of thousands of dollars.** If money is a constraint, aim at funded PhD programmes and Indian master's degrees, and treat unfunded US MS offers with suspicion.

### 3.5 How Indian undergraduates actually get there

Not by publishing alone. The common paths, roughly in order of frequency: a summer research internship (an academy or IIT programme, or a directly emailed professor) that produces a letter and sometimes a paper; an MCA/M.Sc. with a real thesis, then a PhD application with a writing sample; a research-fellow role at an Indian lab or in industry (Microsoft Research India runs a structured version — see §5); or a funded MS abroad, then a PhD. A publication helps every one of these. It is the cause of none of them.

---

## 4. Scholarships and fellowships: what actually exists for you

The uncomfortable headline: **none of the schemes below pays you for publishing a paper.** Scholarships pay for studying, or for doing an internship, or for travel. Plan accordingly.

| Programme | What it is | Eligibility (verified 2026-11-03) | Do you qualify? |
|---|---|---|---|
| **INSPIRE-SHE** (DST) | ₹80,000/year for up to 5 years; 12,000 scholarships a year [14] | Top 1% in Class XII, or top-10,000 JEE/NEET rank, or KVPY/NTSE/JBNSTS/Olympiad, **and** enrolled in B.Sc./B.S./Int. M.Sc./M.S. in one of 18 listed natural-science subjects. The FAQ explicitly excludes **Computer Applications** [14] | **No.** BCA is excluded by name, whatever your marks |
| **IAS-INSA-NASI Summer Research Fellowship (SRFP)** | Two-month paid research placement with a scientist at an Indian institution; fellowship amount plus travel allowance [15] | Students in **BCA II and III year only**; ≥65% average in core subjects from Class X onwards; college must be UGC/AICTE-affiliated or an accredited institution [15] | **Not yet.** Eligible from Year 2 |
| **Mitacs Globalink Research Internship** (Canada) | 12-week funded research internship at a Canadian university, May–October [16] | **At least 18 years old at the time of application**; enrolled full-time at an eligible institution; at least two years of undergraduate study completed; one to three semesters remaining as of the fall of the application year; India is a participating country [16] | **Not yet** — you are 17 until December 2026, and you have not completed two years |
| **France Excellence Charpak Summer Training Scholarship** | €700/month for up to 2 months for a research internship in a French laboratory, plus visa fee waiver [17] | Indian national resident in India; **not more than 30 years old**; enrolled at Bachelor's or Master's level at an Indian institution; **must already hold an invitation letter from a French lab**; internship 1–2 months between May and August [17] | **Yes, in principle, from 2027.** No year-of-study rule. The hard part is the invitation letter |
| **NTSE** (NCERT) | School-level talent scholarship, awarded at Class X [18] | Class X students in India | **No** — school-level, and already past for you unless you were an NTSE scholar |
| **KVPY** | Was a DST fellowship from Class XI to pre-PhD | **Discontinued.** DST subsumed KVPY into INSPIRE; the aptitude test has not been conducted since 2022 [19] | **No** — it does not exist for new applicants. Any site still selling KVPY coaching is selling nothing |
| **Microsoft Research India Research Fellows** | 1–2 year paid research role in Bangalore, aimed at pre-PhD students [20] | Completed BS/BE/BTech or MS/ME/MTech in CS or related areas; must have graduated at the time of joining; non-CS backgrounds welcome [20] | **Not yet.** This is a post-degree role, not an internship — see §5 |

Two things to notice. The age rule that binds you is Mitacs' 18+ requirement, and it expires in December 2026; the year-of-study rules bind for longer. And **IAS SRFP is the one to plan around**: the only formal programme here that names BCA explicitly, needing no invitation letter, no minimum age and no foreign travel. Charpak is the long shot — it has no year rule at all.

A note on student travel grants: ACM and IEEE run them through individual conferences and SIGs, and acm.org blocked automated access on 2026-11-03. `UNCERTAIN: current ACM/IEEE student travel grant terms. Check the specific conference's "travel grants" page when you have an accepted paper — that conference's budget is where the money comes from.`

---

## 5. Research internships: the real gate is your year of study

This is the section that should make you feel better about being 17 and in first semester, because almost every programme is closed to you right now for a reason that expires.

| Programme | What it is | Eligibility (verified) | Now? | When |
|---|---|---|---|---|
| **IAS-INSA-NASI SRFP** | 2 months with a scientist, any time in the calendar year, preferably summer [15] | **BCA II and III year only**; ≥65% in core subjects from Class X; apply by 30 November of the preceding year [15] | No | Apply **Nov 2027** (Year 2) for a 2028 placement; again Nov 2028 (Year 3) |
| **IIT Kanpur SURGE** | 8-week summer research internship at IIT Kanpur [21] | Non-IITK Indian students: B.Tech/B.E./B.Arch/BS in 3rd year, or B.Sc./B.A. in 2nd year; minimum CPI 6.0 [21] | No | **BCA is not in the eligible course list** — `UNCERTAIN` whether an exception is possible; ask surge@iitk.ac.in rather than assume |
| **IIT Madras Summer Fellowship** | Guided research internship with IITM faculty | B.Tech students who have completed the 6th semester [22] | No | Not a route for a 3-year BCA |
| **IISc summer programmes** | Department-run summer fellowships (the Chemistry department's, for example, is for B.Sc. 2nd year / Int. M.Sc. 2nd–4th year / 4-year BS 2nd–3rd year / M.Sc. 1st year) [23] | Department-specific | No | `UNCERTAIN` whether any IISc department runs a CS summer programme open to BCA. Email the department; do not assume a general IISc undergraduate summer school exists |
| **DAAD WISE** (Germany) | 2–3 month research internship at a German publicly funded institute | Indian students in the **5th or 6th semester of a 4-year bachelor's**, at **selected Indian universities** [24] | No | Not a route for a 3-year BCA at a non-partner college. `UNCERTAIN` on the exact current wording: DAAD's scholarship database entry would not load on 2026-11-03, so the semester rule is taken from DAAD's India brochure and host-institute restatements |
| **Mitacs Globalink** (Canada) | 12-week funded internship, May–Oct [16] | 18+ at application; ≥2 years completed; 1–3 semesters remaining in the fall of the application year [16] | No | `UNCERTAIN` timing for a 3-year degree: the "1–3 semesters remaining in the fall" rule is built around 4-year programmes. Write to Mitacs India and ask whether a 3-year BCA can fit a May–Oct placement at all |
| **Charpak Summer Training** (France) | 1–2 month research internship, €700/month [17] | Bachelor's level, ≤30 years, invitation letter from a French lab required [17] | Eligible from 2027 | Summer 2027 or 2028 — you must find the lab yourself |
| **Microsoft Research India — Research Fellows** | 1–2 year paid research role, Bangalore [20] | Completed BS/BE/BTech or MS/ME/MTech; must be graduated when joining; applications open January, close mid-February [20] | No | After graduation. `UNCERTAIN` whether a BCA alone is accepted — the listed degrees do not include it; an MCA would put you in a stronger position |
| **Google (India)** | Research internships in India are advertised at PhD level (for example "Research Scientist PhD Intern") [25] | Enrolled in a PhD programme | No | Not an undergraduate route. Google's undergraduate internships are software engineering, not research |

The pattern is unmistakable: **formal research internships are for students in their second or third year.** That is not bad news for you. It means the deadline that matters is November 2027, and you have twelve months to become the kind of applicant who gets selected — which is exactly what the paper in this repo is for.

There is also an informal route no table captures: email a professor whose paper you have read, with a specific question and a specific thing you could do for them. Many will not reply; some will. That route has no eligibility rule at all, and it is how a large share of Indian undergraduates get their first research experience. It works far better in Year 2, because you need something to show.

---

## 6. GATE and CAT: the exams, and the cost of getting this wrong

**GATE** is the entrance exam for M.Tech and for direct PhD programmes at IITs/IISc, and public sector companies also recruit on it [8]. The CS paper is genuinely hard: it assumes a four-year CSE curriculum. A publication does not affect your GATE score. It can affect what happens after — an interview at a research programme is a conversation, and a paper gives you something to say — but the score is a number produced by an exam, and nothing else moves it.

**CAT** is the entrance exam for MBA programmes. It is not a research route and has no place in this plan. It appears here only because it is usually mentioned in the same breath as GATE: its logic (quantitative aptitude, verbal ability, data interpretation) is unrelated to research training. If you want an MBA later, CAT will still be there. It should not compete for your hours in 2027.

**The blunt paragraph on opportunity cost.** You have roughly 100 usable hours a month outside class if you work seriously. Every hour chasing a paper is an hour not spent on the exam that decides your next admission. In semester 5, when GATE and NIMCET preparation both matter, the trade is brutal: 100 hours of paper work is about three weeks of exam preparation, and the exam is scored, ranked and used by every institute, while the paper is read by a handful of people. Do paper work in semesters 1–4 and in the summers. In the final year the exams win, and you should decide that in advance rather than in a panic in December.

The reverse also holds: do not let Year 1 exam panic kill the paper. Nothing you sit for in first semester follows you for three years, which makes this the cheapest time you will ever have to learn research.

---

## 7. A realistic three-year plan

Hours are per week, outside class, and assume some weeks will be zero.

### Year 1 (now – May 2027): skills and this paper

- **8–10 hours/week** on research and the skills it needs: Python, git, two papers a week from the A6 reading list, and the work in this repo.
- **Target:** one finished artifact by May 2027 — draft, code, and a public repository with a README a stranger can follow.
- **Target:** one PSIT faculty member who knows your name and has seen your work. Worth more than the paper.
- **Administrative:** confirm that your BCA syllabus includes Mathematics or Statistics. If not, find out your options now, because NIMCET requires it [2].
- **Summer 2027 (after Year 1):** no formal programme will take you — SRFP needs Year 2, Mitacs needs 18+ and two years, DAAD WISE needs the 5th semester. Use the summer to build the repository into something with users, or to work on a PSIT faculty member's problem. Charpak is the only funded option, and only with a French invitation letter.

### Year 2 (2027-28): internship and a second artifact

- **10–12 hours/week** during term; more in the breaks.
- **By 30 November 2027:** submit the SRFP application. It needs a 150–250 word write-up on a specific area, marksheets from Class X onwards, and a teacher's contact for a recommendation [15]. The write-up is the part that decides selection; write it about a specific experiment you want to run, not about "AI in healthcare".
- **Summer 2028:** the internship, if selected. If not, the fallback is the same as Year 1's: a local lab, an open-source contribution, or a remote collaboration.
- **Second artifact:** either a second paper on a different problem, or — often better — one serious repository that other people use. One of each is a strong Year 2.
- **Keep the marks up.** SRFP requires a 65% average in core subjects from Class X onwards [15], and NIMCET requires 60%/6.5 CGPA [2]. A brilliant paper with a 58% average closes doors that no paper opens.

### Year 3 (2028-29): applications, exams, thesis

- **6–8 hours/week** on research, deliberately reduced.
- **December 2028:** if you are applying abroad, this is the deadline month [10]. You will need three letters, a statement, and transcripts — start in September.
- **February 2029:** GATE, if you are taking it. **February–May 2029:** NIMCET. **March 2029:** CUET-PG. These are not compatible with a paper sprint in the same months.
- **Thesis or final project:** use it. A final-year project is the cheapest supervised research you will ever get, and it can become the writing sample for a PhD application.

### What to drop, explicitly

- **Three weeks before any university exam:** research hours go to zero. Not "reduced". Zero. A paper does not care whether you take three weeks off; a backlog in a 6-credit course does.
- **During the exam period itself:** no new experiments, no new reading. If a deadline collides with exams, ask the chairs for an extension — they can grant one, and a rushed submission is worse than a late one.
- **Anything that requires you to pay to publish.** Drop it permanently, not just during exams.
- **The second paper,** if Year 2 goes badly. One good artifact and strong marks beats two mediocre papers and a 60% average.

---

## 8. What a paper does not guarantee

- **It does not get you a job.** Employers hiring developers test whether you can build software. A paper is a weak proxy; a repository is a strong one.
- **It does not get you an admission.** NIMCET and CUET-PG are rank-based [2][5]; foreign PhD committees say outright that they admit students without publications [9].
- **It does not get you a scholarship.** None of the schemes in §4 award money for publishing [14][15][16][17].
- **A workshop paper is not a top-conference paper.** Workshops exist to discuss early work; review is lighter, and the acceptance bar is lower. That is fine — a workshop paper is an honest first step — but do not describe it to anyone as a "conference paper at NeurIPS" if it was a NeurIPS workshop. People check, and being caught inflating a venue is worse than having a modest venue.
- **A paper in a predatory journal is a liability,** not an asset. It costs money, it signals poor judgement, and it can be retracted.
- **Authorship disputes are real and common.** Agree in writing, before you start, on who is an author and in what order. A faculty member who contributes the idea, the supervision and the writing is an author — that is normal, not an injustice. If you did the work and someone adds their name without contributing, raise it early, politely, once.
- **It can burn a semester.** The realistic failure mode is not rejection. It is spending five months on a project that produces nothing, while your CGPA drops and you miss the internship deadline. The defence is a hard stop: if by the end of a fixed period you have no working experiment and no clear negative result, write up what you learned, publish the code, and stop.

The honest summary: **a paper is worth roughly what the research behind it is worth, and nothing more.** Do the research properly, keep the code public, get a professor to supervise you, and treat the paper as the receipt.

---

## Sources

1. PSIT College of Higher Education — About us (affiliation to Chhatrapati Shahu Ji Maharaj University; UGC Section 2(f); college code KN162). https://www.psitche.ac.in/about_us.php — retrieved 2026-11-03.
2. NIMCET-2026 Information Brochure (PDF), eligibility: UG programme of ≥3 years with Mathematics/Statistics as a subject, or B.E./B.Tech; 60% / 6.5 CGPA. https://cdnbbsr.s3waas.gov.in/s33e6260b81898beacda3d16db379ed329/uploads/2026/02/202602271304076377.pdf — retrieved 2026-11-03.
3. NIMCET — About NIMCET (11 NITs and 2 IIITs; admission to MCA based on NIMCET rank). https://nimcet.admissions.nic.in/nit/ — retrieved 2026-11-03.
4. Central University of Karnataka — PG Admission 2026-27 through CUET (PG) 2026-2027, provisional merit list including MCA. https://www.cuk.ac.in/Admission2026/CUK_ADM_NOTIF/CUK_ADM_NOTIF/index5.html — retrieved 2026-11-03.
5. National Testing Agency — CUET (PG) examination page. https://exams.nta.nic.in/cuet-pg/ — retrieved 2026-11-03.
6. Indian Institute of Science — M.Tech (Research) and Ph.D. programmes, eligibility and selection. https://www.iisc.ac.in/admissions/research-programmes/ — retrieved 2026-11-03.
7. GATE 2026 (IIT Guwahati) — Eligibility Criteria ("currently studying in the 3rd or higher years of any undergraduate degree program..."). https://gate2026.iitg.ac.in/eligibility-criteria.html — retrieved 2026-11-03.
8. GATE 2026 — official home page (30 test papers; score valid three years; used for Master's, direct doctoral and doctoral admissions, and by PSUs). https://gate2026.iitg.ac.in/ — retrieved 2026-11-03.
9. Johns Hopkins University, Department of Computer Science — PhD Admissions FAQ ("Do I need published research papers? No..."). https://www.cs.jhu.edu/academic-programs/graduate-studies/phd-program/phd-admissions-faqs/ — retrieved 2026-11-03.
10. Stanford Computer Science — Graduate Application Deadlines (PhD, Autumn entry: application opens 15 September 2026, deadline 8 December 2026). https://www.cs.stanford.edu/admissions-graduate-application-deadlines — retrieved 2026-11-03.
11. Stanford Computer Science — PhD Admissions, eligibility ("Applicants from institutions outside of the United States must hold the equivalent of a United States Bachelor's degree"). https://www.cs.stanford.edu/admissions/phd-admissions — retrieved 2026-11-03.
12. anabin (Kultusministerkonferenz) — information portal for the assessment of foreign educational qualifications. https://anabin.kmk.org/anabin.html — retrieved 2026-11-03.
13. Cornell Computer Science — Apply: Ph.D. in Computer Science, financial support (full support via teaching assistantships, research assistantships, or fellowships). https://www.cs.cornell.edu/phd-computer-science/apply — retrieved 2026-11-03.
14. Department of Science and Technology — INSPIRE Scholarship for Higher Education (SHE) FAQs (₹80,000 per year, 12,000 scholarships; eligible subjects; Computer Applications excluded). https://online-inspire.gov.in/Content/SHEFAQs.pdf — retrieved 2026-11-03.
15. Indian Academy of Sciences — Science Academies' Summer Research Fellowship Programme 2027, Instructions to Applicants (BCA II and III years only; 65% average in core subjects from Class X; last date 30 November 2026). https://webjapps.ias.ac.in/fellowship2027/application_instructions.jsp — retrieved 2026-11-03.
16. Mitacs — Globalink Research Internship, students page (18+ at application; two years of study completed; one to three semesters remaining; India listed as a participating country). https://www.mitacs.ca/our-programs/globalink-research-internship-students/ — retrieved 2026-11-03.
17. Campus France India — France Excellence Charpak Summer Training Scholarship (€700/month for up to 2 months; ≤30 years; Bachelor's or Master's level; invitation letter required). https://www.inde.campusfrance.org/france-excellence-charpak-summer-training-scholarship — retrieved 2026-11-03.
18. NCERT — National Talent Search Examination (Class X level). https://www.ncert.nic.in/national-talent-examination.php — retrieved 2026-11-03.
19. The Indian Express — "KVPY discontinued from current year, subsumed under INSPIRE programme" (DST decision; aptitude test not conducted from 2022; existing fellows continue). https://indianexpress.com/article/education/no-kypy-this-year-onwards-subsumed-under-inspire-programme-8038444/ — retrieved 2026-11-03.
20. Microsoft Research India — Research Fellows Program (eligibility: completed BS/BE/BTech or MS/ME/MTech; must be graduated at joining; application dates January–February). https://www.microsoft.com/en-us/research/academic-program/research-fellows-program-at-microsoft-research-india/ — retrieved 2026-11-03.
21. IIT Kanpur SURGE — Eligibility (non-IITK Indian students: B.Tech/B.E./B.Arch/BS 3rd year, B.Sc./B.A. 2nd year; minimum CPI 6.0). https://surge.iitk.ac.in/eligibility — retrieved 2026-11-03.
22. IIT Madras, Department of Engineering Design — Summer Fellowship Program (B.Tech students who have completed the 6th semester). https://ed.iitm.ac.in/summerfellowship.html — retrieved 2026-11-03.
23. Indian Institute of Science, Department of Inorganic and Physical Chemistry — Summer Research Fellowship eligibility (B.Sc. 2nd year; Int. M.Sc. 2nd–4th year; 4-year BS 2nd–3rd year; M.Sc. 1st year). https://ipc.iisc.ac.in/summer_fellowships.php — retrieved 2026-11-03.
24. DAAD — "A New Passage to India" brochure (WISE: undergraduates from selected Indian universities). https://www.daad.in/files/2025/05/A-New-Passage-to-India-Brochure_____Pdf_compressed.pdf — retrieved 2026-11-03.
25. Google Research — Careers, India (research internships and roles). https://research.google/careers/ — retrieved 2026-11-03.

## How confident is this?

- **Solid:** the Indian exam routes (NIMCET, CUET-PG, GATE) and their eligibility rules, taken from the examining bodies' own pages today. The IAS SRFP rule that BCA students are eligible in years II and III only, and the 65% requirement — this is stated verbatim on the 2027 instructions page, and it is the single most useful fact in this document for you.
- **Solid:** the claim that foreign PhD committees admit students without publications, and that a December deadline in the final year is the norm. Both come from department pages, not from advice blogs.
- **Solid:** INSPIRE-SHE excludes Computer Applications by name, and KVPY no longer exists for new applicants. Both are stated in primary or near-primary sources.
- **UNCERTAIN — the 3-year bachelor's question.** No authority sets a general rule. Programme-by-programme checking is the only honest answer, and it will take you a few hours per application cycle.
- **UNCERTAIN — Mitacs timing for a 3-year degree.** The "one to three semesters remaining" rule is written for four-year programmes; whether a BCA can fit a May–October placement is not answerable from the page. Ask Mitacs directly.
- **UNCERTAIN — DAAD WISE's exact semester rule.** DAAD's own database entry would not load on 2026-11-03; the "5th/6th semester, selected universities" wording comes from DAAD's India brochure and host-institute pages. The conclusion (not a route for a 3-year BCA) is safe; the precise wording is not.
- **UNCERTAIN — whether PSIT CHE's BCA syllabus includes Mathematics or Statistics,** which determines NIMCET eligibility. This is checkable in ten minutes from your own scheme of examination, and you should check it this week.

last_updated: 2026-11-03
