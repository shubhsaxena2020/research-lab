# Round-3 review schema (from prompt packs + round2 examples)

Sources inspected:
- `06_review/reviews/round3-c1/*.PROMPT.md` (6 personas), required-output section identical across all six.
- `06_review/reviews/round2-c1/methodologist.review.yaml` (full example).
- `06_review/personas/*.md` (persona frontmatter: role, focus, red flags, scoring weights).

## Required top-level keys (12)
Order in prompt shape; YAML mapping order is not semantically required.

1. `persona` — string, persona id (must match file/persona).
2. `summary` — block scalar (`|`), 2–5 sentences: claim, what is actually shown, main reason for score.
3. `strengths` — list of strings (each a specific strength with section/table/figure).
4. `weaknesses` — list of strings (each a specific weakness with location + why it matters).
5. `questions` — list of strings (rebuttal-answerable questions).
6. `soundness` — integer 1–4.
7. `presentation` — integer 1–4.
8. `contribution` — integer 1–4.
9. `confidence` — integer 1–5.
10. `overall` — integer 1–10.
11. `decision` — enum `reject | borderline | accept`.
12. `must_fix` — list of 1–8 objects.

## must_fix item format
Each item is an object with:
- `claim` (required): one sentence naming the defect, not the topic.
- `where` (optional but strongly preferred): location, e.g. `"Section 5, Table 2"`.
- `evidence_needed` (required): checkable specification — interval, run id, seed set, baseline, citation, section, or exact change.

## Scoring
- Dimensions scored independently; overall is a judgement, not an average.
- `soundness` 1–4: 1 major concerns/claim not supported; 2 significant concerns; 3 mostly sound, minor gaps; 4 sound, claims match evidence.
- `presentation` 1–4: 1 hard to follow; 2 significant clarity problems; 3 clear with local issues; 4 clear, well organised, figures readable.
- `contribution` 1–4: 1 none/negative; 2 incremental; 3 solid; 4 significant.
- `confidence` 1–5: 1 educated guess; 3 fairly confident; 5 certain/familiar with relevant work.
- `overall` 1–10: 1–3 strong reject, 4–5 reject, 6–7 borderline, 8–9 accept, 10 strong accept.
- `decision` must be consistent with overall: reject if overall <= 4, borderline if 5–6, accept if >= 7. If deliberately broken, explain in `summary`.
- Persona declared weights (attention, not arithmetic): clarity 0.20/0.55/0.25; domain_expert 0.40/0.15/0.45; methodologist 0.50/0.10/0.40; novelty_skeptic 0.20/0.15/0.65; reproducibility_reviewer 0.35/0.15/0.50; statistician 0.60/0.10/0.30 (soundness/presentation/contribution).

## Constraints / hard rules
- Output exactly one YAML document, nothing else: no preamble, no markdown fence around the whole file, no commentary after it.
- `must_fix` has between 1 and 8 items; each is a blocking defect, not a nice-to-have. Typos/style do not belong here.
- `claim` is one sentence naming the defect.
- `evidence_needed` must be checkable by authors.
- Quote at most one short phrase per point; do not paste paragraphs.
- If the draft does not report something, write "not reported" and treat as finding; do not invent numbers/citations/results.
- Do not soften real defects or invent defects; if sound, score high.
- One reviewer/one lens: leave out-of-lens defects to others unless they block this assessment.
- `summary` is 2–5 sentences.
- `where` optional but strongly preferred.
- Persona-specific red flags and attack protocols (in `06_review/personas/*.md` and prompt Section 2) define what to attack and how to score; strengths must be actual positive findings, not mere absence of red flags.

## Persona set (round3-c1)
clarity_reviewer, domain_expert, methodologist, novelty_skeptic, reproducibility_reviewer, statistician. Prompt packs are stale against current draft (sha 9194a481 vs e346271e) per task context; schema unaffected.