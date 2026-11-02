# STUDENT-DIGEST

One-page study aids for the paper, one per section, generated from the draft by
`tools/make_digest.py`. Their only job is to let Shubh explain and defend every section at a
talk, in his own words.

**These files are study aids, not sources.** The draft is the paper. If a digest and the
draft disagree, the draft wins and the digest is regenerated.

## The three rules of this folder

1. **Every `[TO FILL]` must be filled by the student, in his own words.** A placeholder is a
   question the tool could not answer honestly. Copying a definition or an interpretation
   from a model, a website, or this repository defeats the purpose: at the talk, the student
   is the author who must answer.
2. **The digest may never contain a fact that is absent from the draft and its evidence
   files.** Numbers come only from `04_experiments/RESULTS-INDEX.json` plus the result file
   it points to. Citations come only from `02_literature/verified_citations.csv`. Nothing
   else may be added by hand - not a percentage, not a venue, not a "probably about".
3. **When evidence is missing, the gap stays visible.** If a `<!-- num:id -->` marker has no
   index entry, or a `\cite{key}` has no verified row, the digest says `[TO FILL: ...]`
   instead of guessing. The fix is to repair the index or the citation record (or remove the
   claim), never to type a plausible value into the digest.

## What each block is for

| Block | What it contains | How to use it |
|---|---|---|
| `## What this section says` | One bullet per paragraph, extracted from the paragraph's topic sentence, first person, max 25 words. | Say each bullet out loud until it is fluent. It is deliberately compressed, not paraphrased into new claims. |
| `## Why it is there` | The job the section must do, derived from its role (intro / method / results / limitations / ...), plus a reader checklist. | Answer every checklist item before the talk. An unanswered box is a question you will be asked. |
| `## What could be asked at a talk` | 3-6 prompts from a fixed question bank for that role, each tied to a paragraph or a number in the section. | Rehearse the answers with the draft open. Do not memorise wording; know the evidence. |
| `## Five likely questions with honest answers` | Exactly five first-person answer skeletons. Resolved numbers and citations are quoted from the evidence files; everything else is a `[TO FILL]`. | Fill each slot with a sentence you can defend. If you cannot, the claim may be weaker than the draft says. |
| `## Glossary` | Technical terms outside a small BCA-level vocabulary, each with a placeholder definition and where it first appears. | Write each definition yourself, then check it against a textbook. No definition is supplied here on purpose. |

## Generate and audit

```bash
# one section
python tools/make_digest.py --section 05_paper/draft/method.md

# every .md in a directory (non-recursive, skips README.md and _*.md)
python tools/make_digest.py --section 05_paper/draft --all

# optional explicit evidence files (defaults shown)
python tools/make_digest.py --section 05_paper/draft/method.md \
    --index 04_experiments/RESULTS-INDEX.json \
    --citations 02_literature/verified_citations.csv

# audit a digest: all blocks, exactly 5 questions, 3-6 talk prompts, no definition-like glossary
python tools/make_digest.py --check 06_review/STUDENT-DIGEST/METHOD.md

# final gate: also fail if any [TO FILL] remains
python tools/make_digest.py --check 06_review/STUDENT-DIGEST/METHOD.md --strict
```

Exit codes: `0` pass, `1` findings, `2` usage error. `--json` prints machine-readable
output. The tool is offline and stdlib-only.

A digest is ready for a talk only when `--strict` passes **and** the student can explain every
sentence without reading it. `--strict` proves the placeholders are gone, not that the answers
are good.

## Regeneration

Digests are derived artefacts. After a draft edit that changes a paragraph, a number, or a
citation, regenerate the section and re-fill the affected `[TO FILL]` slots. Do not hand-edit
a generated number to "make it match": if the draft prints one value and the result file
stores another, the digest flags the mismatch with `[TO FILL]` on purpose, and the draft or
the index must be fixed first.

## If a section is unclassified

A filename that does not map to a known role produces `role: generic` plus a `[TO FILL]`
asking for the role. Pass `--role intro|method|results|limitations|related|discussion|conclusion|abstract`
to choose the right question bank. Do not leave the generic checklist in place for a talk.

## AI assistance

The digest generator is a tool; the answers are the student's. Per `RULES.md` #4, any AI
assistance used to prepare the paper is disclosed following the venue's policy. Filling a
`[TO FILL]` slot with generated text the student cannot explain would violate both the
letter and the point of that rule.
