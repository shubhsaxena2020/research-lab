# AI-DISCLOSURE — per-venue statement template

RULES.md #4: the paper must disclose AI assistance (which tools, for what) following the
target venue's policy, and the student stays the responsible author.

This file is the **template**, not the disclosure. Copy it to
`06_review/ai-disclosure-<venue>-<date>.md`, fill every `<ANGLE BRACKET>`, delete what does
not apply, and paste the finished statement into the draft where the venue asks for it
(usually Acknowledgements, or a separate "Use of AI tools" section right before References).

Two rules before anything else:

1. **Policies differ, and they change.** The venue's own page wins over this table, over a
   supervisor's memory, and over a blog post. Open the policy page the day you submit and
   follow it, even if it contradicts this file. This file only tells you where to look.
2. **Disclose the tool, not just the category.** "AI was used for editing" is not a
   disclosure. Name the tool, the version (or the access date if there is no version), the
   sections, and what you did with the output.

---

## 1. What was done with AI

Tick what applies; delete rows that do not. "What I did with it" is the column reviewers
actually read — never leave it blank.

| # | Task | Tool + version / access date | Scope (sections, files) | What I did with the output |
|---|------|------------------------------|--------------------------|----------------------------|
| A1 | Literature search support (query suggestions, screening help) | `<tool, version>` | `<e.g. candidate pool for related work>` | Ran every query myself in OpenAlex/Semantic Scholar; opened and read each kept paper; every citation resolved via `tools/verify_citations.py` |
| A2 | Code drafting (scripts, plotting, tests) | `<tool, version>` | `<e.g. 04_experiments/plots.py, test harness>` | Read every line, ran it, fixed it, own the result; committed command and seed in `meta.json` |
| A3 | Language editing (grammar, clarity, concision) | `<tool, version>` | `<e.g. Sections 3 and 5, one pass>` | Accepted/rejected each suggestion by hand; final wording is mine |
| A4 | Formatting / BibTeX cleanup | `<tool, version>` | `<e.g. refs.bib keys>` | Checked each entry against the verified citation record |
| A5 | `<other — be specific>` | | | |

## 2. What was NOT done with AI

This section is the point of the disclosure. Do not soften it; if any item is false for
you, delete that item and say what actually happened.

- **The research question and framing** — chosen by the author, not generated.
- **The experiments, their design, and the interpretation of their results** — the author
  decided what to run, what the numbers mean, and which negative results to report.
- **The final text** — every sentence was written or rewritten by the author. AI output was
  never pasted into the draft as prose.
- **All verification** — every citation resolved against a bibliographic API and recorded
  in `02_literature/verified_citations.csv`; every number traced to a run under
  `04_experiments/runs/`; every claim checked against its source by the author.
- **No AI tool is an author**, and none is cited as one. No AI-generated image, table, or
  dataset is presented as the author's own work.

## 3. First-person statement (fill in the blanks)

> I, **`<FULL NAME>`**, am the author of **`<PAPER TITLE>`**, submitted to `<VENUE>`
> (`<TRACK>` track) on `<DATE>`. I used **`<TOOL(S) + VERSION>`** for
> `<literature search support / drafting <SPECIFIC CODE OR SCRIPTS> / language editing of
> <SECTIONS>>`. I did not use AI to formulate the research question, to design or interpret
> the experiments, to write the final text, or to verify any citation, number, or claim:
> those are my own work, and the evidence for them is in `02_literature/` and
> `04_experiments/`. I have read every section of this paper, I can explain and defend
> every claim and number in it, and I take full responsibility for its content. Any
> remaining errors are mine.

Short variant for venues with a 2–3 sentence limit:

> I used `<TOOL(S)>` for `<PURPOSES>`. The research question, the experiments and their
> interpretation, the final text, and all verification of citations, numbers and claims
> are my own work. I take full responsibility for the paper's content.

## 4. Venue policies — where to look, and what to check

**Authoritative source in this repo: `00_foundations/ETHICS-AND-AI-USE.md`** (session S1).
That file quotes each venue's policy word-for-word, with the URL and the retrieval date, and
it was checked against the live pages. Read it before this table; where the two disagree,
**S1's file wins** and this table should be corrected. The summary below exists so you do not
have to open a 36,000-character document to know where the disclosure goes.

Policies change between cycles — every row still needs a check on the day you submit.
"Verify current policy" is not boilerplate; it is the step that keeps the disclosure honest.

| Venue | Policy page | What it actually asks for | Status |
|-------|-------------|---------------------------|--------|
| **ACL / ACL Rolling Review** | https://www.aclweb.org/adminwiki/index.php/ACL_Policy_on_Publication_Ethics · https://aclrollingreview.org/authors | AI use must be **fully disclosed**, named in the Acknowledgements; language polishing is exempt; AI cannot be an author; fabricated citations are misconduct | **verify current policy** |
| **NeurIPS** | https://neurips.cc/Conferences/2026/MainTrackHandbook · https://neurips.cc/public/guides/PaperChecklist | Use as an *important, original or non-standard component of the method* is described in the experimental setup; **spell-checking, grammar, editing and basic code assistance need no documentation**; checklist item 16 asks about it; hallucinated citations are a Code of Conduct violation | **verify current policy** |
| **ICML** | https://icml.cc/Conferences/2025/CallForPapers · https://icml.cc/Conferences/2025/PublicationEthics | "Explain any notable ways" AI was used — encouraged rather than mandated | **verify current policy** |
| **ACM** | https://www.acm.org/publications/policies/frequently-asked-questions | Policy rewritten 14 May 2026: AI use belongs in the **methods**, and only when AI was part of the research; AI used to write the paper is no longer asked about; no AI author | **verify current policy** |
| **IEEE** | https://journals.ieeeauthorcenter.ieee.org/become-an-ieee-journal-author/publishing-ethics/guidelines-and-policies/ | AI-generated text is not accepted as authorial content; limited AI-assisted editing must be disclosed in the **Acknowledgements**; AI cannot be an author; check the specific transaction's page | **verify current policy** |
| **Elsevier** | https://www.elsevier.com/about/policies-and-standards/publishing-ethics (generative-AI section) | A statement before the references describing AI-assisted use, its scope and oversight; AI cannot be an author | **verify current policy** |

**Consequence for this project, stated plainly:** under NeurIPS rules the editing this
pipeline does would not need a declaration, but under ACL and IEEE it does. Disclose anyway,
everywhere, in the venue's own placement — an unnecessary disclosure costs nothing, a missing
required one is misconduct. What you may *not* do is claim in Section 2 something that the
tools in Section 1 contradict.

If the venue is not in this table: search its author guidelines for "generative AI",
"LLM", "AI-assisted", and "authorship", and read the *submission* policy, not a summary of
it. Record the URL and date you read it in section 6.

## 5. Placement and wording by venue

Paste only the block the venue asks for; do not invent a policy quote.

**ACL / ARR** — acknowledgement-style paragraph, adapted from section 3, plus the ethics
statement if the venue requires one:

> **Use of AI tools.** `<TOOL(S)>` was used for `<PURPOSES>`. The author designed the
> study, ran and interpreted the experiments, wrote the manuscript, and verified every
> citation and number. The author takes full responsibility for the content.

**NeurIPS** — answer the checklist item and keep the paper text short:

> **LLM usage.** `<TOOL(S)>` was used for `<PURPOSES>`. No LLM-generated text appears in
> the paper as authorial prose; all cited work was read by the author.

**IEEE** — in Acknowledgements:

> The author used `<TOOL(S)>` for `<PURPOSES>`. The author reviewed and edited all output
> and is solely responsible for the content of this paper.

**Elsevier** — declaration block immediately before the reference list:

> **Declaration of generative AI and AI-assisted technologies in the writing process.**
> During the preparation of this work the author used `<TOOL(S)>` in order to
> `<PURPOSES>`. After using this tool, the author reviewed and edited the content as
> needed and takes full responsibility for the content of the publication.

## 6. Submission-time record

Keep this with the draft; it is what you show if a reviewer or the R&D cell asks.

| Item | Value |
|------|-------|
| Venue / track | `<VENUE>` |
| Policy URL actually opened | `<URL>` |
| Date checked | `<YYYY-MM-DD>` |
| What the policy required | `<quote or paraphrase the requirement>` |
| Where the disclosure was placed | `<Acknowledgements / checklist / declaration>` |
| Tool versions / access dates | `<tool: version or date>` |
| Prompt/output log kept at | `<path or "not retained">` |

## 7. Before you submit — checklist

- [ ] Policy page opened today; requirement matches what this file says.
- [ ] Every tool named, with version or access date.
- [ ] Every scope claim true (no "only for editing" if it also drafted code).
- [ ] Section 2 statements are literally true, not aspirational.
- [ ] AI is not listed as an author, and no AI-generated figure/table is uncredited.
- [ ] Citations all `VERIFIED` in `02_literature/verified_citations.csv`; numbers all
      traceable through `04_experiments/RESULTS-INDEX.json`; `06_review/ORIGINALITY.md`
      procedure passed.
- [ ] The student can explain every section without the tool open. If not, the paper is
      not ready — the disclosure does not fix that.

**Plain statement for the record:** AI assistance was used for support tasks only; the
research question, the experiments and their interpretation, the final text, and all
verification are the author's own. Different venues require this to be said in different
places and different words — the venue's current page decides where and how.
