# WRITING-SPEC (binding for every document written in session S1)

Retrieval date for all sources in this session: **2026-11-03** (IST). Write it as `retrieved 2026-11-03`.

## 1. Audience
Shubh: 17 years old (born Dec 2008), first-semester BCA student at PSIT College of Higher Education, Kanpur.
He is smart, in his exam period, and new to research. Write for him.
- Plain English. Short paragraphs (2-5 sentences). Concrete examples with numbers.
- No jargon without a one-line definition in parentheses the first time it is used.
- Never write "as is well known" / "obviously" / "simply". If a step is hard, say it is hard.
- Use headings, bullet lists and small tables. Markdown only (the repo is markdown).

## 2. Integrity rules (from RULES.md, non-negotiable)
- Every factual claim about the outside world (a policy, a fee, a deadline, a statistic, a rule)
  must have a real source with a URL, listed in a `## Sources` section at the bottom of the file,
  numbered [1], [2], ... and cited inline as [1].
- Verify the URL actually loads and actually says what you claim, with web_extract or a browser fetch,
  BEFORE you cite it. If it does not load, drop the claim or mark it UNCERTAIN.
- If you could not verify something, write it as `UNCERTAIN: ...` and say what is missing.
  Never invent a number, a date, a fee, a policy or a paper title.
- Prefer primary sources: the venue's own website, the publisher's policy page, the government body's page.
  A blog post or a Wikipedia page may only be used as a pointer ("see [n] for the official page"), not as the authority.
- Date-sensitive facts (deadlines, fees, ranks) get the marker `(as of 2026-11-03)`.
- Anything you produce must be reproducible: where you make a numeric claim, say how it was obtained.

## 3. File conventions
- Output goes to the exact path given in your task. Do not create other files except temporary
  scratch files under the repo (and delete them) or `logs/`.
- Start each file with a one-line `#` title, then a 2-4 line "What this page is for" block.
- End each file with:
  `## Sources` (numbered, with title + URL + retrieved date)
  `## How confident is this?` (3-6 bullets: what is solid, what is UNCERTAIN and why)
  `last_updated: 2026-11-03`
- Target length is given per file. Going over by 20% is fine; under by 20% means you skipped content.
- Do not write "TODO". Either write it or write "not covered" with a reason.

## 4. Style traps to avoid
- No hype: not "game-changing", "cutting-edge", "revolutionary".
- No emoji. No exclamation marks. No "delve", "leverage", "unlock", "in today's fast-paced world".
- Prefer active voice and concrete nouns: "NeurIPS rejected 76% of submissions in 2024 [3]".
