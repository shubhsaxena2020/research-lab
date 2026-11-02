# Meta-review - <paper short title> - round <N>

| | |
|---|---|
| Draft reviewed | `05_paper/draft/<file>.md` |
| Draft sha256 | `<sha12>` (from `_MANIFEST.json`) |
| Round | `<1 or 2>` |
| Review directory | `06_review/reviews/round<N>/` |
| Reviews ingested | `<n>` of 6 personas |
| Aggregate | `06_review/reviews/round<N>/AGGREGATE.md` |
| Comparison | `06_review/reviews/COMPARE.md` (round 2 only) |
| Meta-reviewer | Shubh |
| Date | `<YYYY-MM-DD>` |

> **Honesty statement (required).** This meta-review summarises a *simulated* review. The six
> reviews were produced by reviewer personas written by the authors and filled in by
> `<Shubh | an AI agent | a mix>`. No external reviewer, programme committee or venue was
> involved. The scores are a triage device, not a prediction of acceptance, and this document
> must not be described as peer review.

---

## 1. Summary of the discussion

<Two to four paragraphs. What did the six lenses agree on? Where did they disagree, and how
was the disagreement resolved (by looking at a table, a run, a citation - not by averaging)?
Name the single most damaging finding and the single strongest part of the draft.>

**Consensus defects** (raised by two or more personas):

1. <defect> - raised by <personas>
2. ...

**Contested points:**

| Point | For | Against | Resolution |
|---|---|---|---|
| <point> | <persona + reason> | <persona + reason> | <what was checked and what it showed> |

---

## 2. Per-point resolution

One row per aggregated `MF-n` item plus any individual reviewer point that did not cluster.
Resolution types: `change` (with file/diff/commit), `rebuttal` (with citation or result),
`defer` (with a limitations sentence). No row may be left as "acknowledged".

| ID | Raised by | Point (one sentence) | Type | Response / change | Evidence (file#Lx, commit, run id, citation key) | Status |
|---|---|---|---|---|---|---|
| MF-1 | <personas> | <point> | change | <what changed> | `05_paper/draft/x.md#L10-L24`, commit `<hash>` | done |
| MF-2 | <personas> | <point> | rebuttal | <why the point does not hold> | `04_experiments/runs/<run_id>/results.json`, Table <n> | rejected-with-reason |
| MF-3 | <personas> | <point> | defer | <scope boundary> | Limitations, Section <n> | done |
| ... | | | | | | |

**Coverage check**

- Must-fix items in aggregate: `<N>`
- Resolved by change: `<n>`
- Resolved by rebuttal: `<n>`
- Deferred to limitations: `<n>`
- Open: `<n>` (must be 0 before submission, or explained below)

---

## 3. Remaining weaknesses

Weaknesses that survive this round, stated as the paper would have to state them. For each:
why it remains, and where the paper now admits it.

| Weakness | Why it remains | Where the paper states the limit | Risk to the claim |
|---|---|---|---|
| <weakness> | <out of scope / data unavailable / would need new experiment> | <section> | <none / narrows claim to X / blocks claim Y> |
| ... | | | |

If a remaining weakness blocks a claim in the abstract, the abstract must change. List the
abstract sentence that changed, or write "no abstract change required" and say why.

---

## 4. Scores and decision rationale

Round 1 -> round 2 (from `COMPARE.md`):

| Metric | Round 1 | Round 2 | Delta |
|---|---:|---:|---:|
| Mean overall | <x.xx> | <x.xx> | <+x.xx> |
| Median overall | <x> | <x> | <+x> |
| Reject recommendations | <n> | <n> | <+n> |
| Must-fix items (distinct) | <n> | <n> | <+n> |
| Resolved / persisted / new | - | <n> / <n> / <n> | |

**Do not justify the decision with the mean score.** Justify it with the resolution table:
what was fixed, what was rebutted, what remains.

Decision for this draft (internal triage, not a venue decision):

- [ ] Ready to submit: every must-fix item is `change` or `rebuttal` with evidence; remaining
      weaknesses are stated in limitations and do not contradict the abstract.
- [ ] Needs another revision: list the blocking items and the owner/date below.
- [ ] Scope cut: the claim must shrink to what the evidence supports. State the new claim.

Rationale: <three to five sentences. Say what would have to be true for the answer to change.>

---

## 5. Actions before submission

| Action | Owner | Due | Blocking? | Done |
|---|---|---|---|---|
| <action> | Shubh | <date> | yes/no | [ ] |
| ... | | | | |

---

## 6. What this simulation did not cover

Tick what applies and note the separate check:

- [ ] Ethics review / dual-use / human-subjects approval - see `00_foundations/ETHICS-AND-AI-USE.md`
- [ ] Citation existence and metadata - `tools/verify_citations.py`, `02_literature/verified_citations.csv`
- [ ] Originality / text overlap - `06_review/ORIGINALITY.md`
- [ ] Venue paper checklist (NeurIPS) or ARR checklist - current venue guidelines
- [ ] Compute budget and artifact size
- [ ] Authorship, acknowledgements, funding, AI-assistance disclosure (RULES #4)
- [ ] Current review-form fields and score ranges re-verified against the venue page

---

## 7. Sign-off

- I can explain every section of this draft without notes: <yes/no>
- Every number in the draft traces to a committed run: <yes/no>
- Every citation is verified in `verified_citations.csv`: <yes/no>
- AI assistance is disclosed per the target venue's policy: <yes/no>
- This meta-review is honest about being a simulation: yes

Signed: <name>, <date>
