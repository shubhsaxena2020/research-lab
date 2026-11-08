# TASK R3-6 — student digest, presentation & viva prep (LAPTOP 2, profile res-s6)

You run on laptop 2 in a COPY of the repo at `C:\Users\admin\research-lab` (wherever RULES.md/COMMON.md say
`C:\Users\shubh\research-lab`, read `C:\Users\admin\research-lab`). The head copies your OWNED files back.

Reader: Shubh — BCA first semester (PSIT, CHE), the paper's responsible author, who must understand, present and defend every
section himself. Plain English, short sentences, no jargon without a one-line explanation. Never invent numbers: every number
you quote must be copied from the current `05_paper/draft/paper.md` and marked "(draft as of 2026-11-08; may change in round 3)".

OWNED: `06_review/STUDENT-DIGEST-S3.md`, `06_review/PRESENTATION/**`, `sessions/R3-6-digest/**`. Everything else read-only.

Deliverables
1. `06_review/STUDENT-DIGEST-S3.md` (<= 2 pages): what we built, what we measured, what failed and why that is still a result,
   what the 12.5% swapped-answer finding means, what the paper does NOT claim. Follow the style of STUDENT-DIGEST-S1/S2.
2. `06_review/PRESENTATION/WALKTHROUGH.md`: the paper section by section — for each: what it says in 3-5 lines, the one
   thing a reviewer will attack, how to answer. Include a glossary of every term (abstention gate, BM25, AUROC, negative,
   rung, pre-registration, over-refusal, coverage, bootstrap interval, ...) with an everyday analogy.
3. `06_review/PRESENTATION/SLIDES-OUTLINE.md`: a 10-12 slide talk (title, problem, setup, ladder, result, why negative,
   swapped-answer finding, limitations, what I learned, AI-use disclosure) with speaker notes per slide.
4. `06_review/PRESENTATION/VIVA-QA.md`: the 25 hardest questions a teacher/reviewer could ask (use the 44 round-2 must-fix
   items as a source) with honest short answers, incl. "did you write this yourself?" -> the AI-assistance disclosure truth.
5. `06_review/PRESENTATION/SELF-CHECK.md`: a 15-question quiz with answers so Shubh can test himself.
Batches of >= 3 subagents (e.g. digest / walkthrough / slides+notes / Q&A), then a reviewer subagent checks every number
against paper.md and every explanation for correctness against the methods section.
