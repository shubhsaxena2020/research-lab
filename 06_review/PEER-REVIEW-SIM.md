# Simulated peer review

Status: procedure + tooling, v1.0 (2026-11-03). Applies to every draft in `05_paper/`.
Owner: Shubh. Tool: `tools/simulate_review.py`. Tests: `tools/tests/test_simulate_review.py`.

---

## 1. What this is, and what it is not

This is an **internal pre-submission check**. Six reviewer personas read the draft through
six different lenses and produce structured, scored reviews. The aggregate tells you which
defects are raised by more than one lens and gives you a tracker for the revision.

**The tool does not generate reviews.** `simulate_review.py` is an orchestrator: it renders
one self-contained prompt pack per persona (persona + attack protocol + rubric + the draft,
delimited as data), then validates, aggregates and compares the YAML reviews that a human or
an agent fills in. No model API is called anywhere in the tool, and none is reachable from
this environment. If you see six review files in a round directory, somebody wrote them -
that fact must stay visible in the meta-review.

Three consequences, stated plainly:

1. **It cannot predict acceptance.** Scores from six personas you wrote are not a programme
   committee. Venue decisions depend on fit, novelty judged by people with different priors,
   reviewer assignment, and luck. Never quote a simulated score as evidence that a paper
   "would be accepted", and never describe this process as peer review in the paper, a CV, or
   an email.
2. **It cannot find what none of the six lenses looks for.** The personas cover methods,
   domain validity, statistics, novelty, reproducibility and clarity. They do not cover
   ethics review, legal exposure, compute cost, or "is this interesting to anyone". Those are
   separate checks (`00_foundations/ETHICS-AND-AI-USE.md`, venue checklist).
3. **It can be gamed, including by you.** If you fill all six reviews in one sitting, they
   will agree with each other and with your intentions. The procedure below exists to make
   that harder: separate passes, frozen draft, evidence per point.

What it *is* good for: catching missing baselines, missing intervals, unstated scope,
overclaimed abstracts, undocumented novelty claims, and irreproducible numbers **before** a
real reviewer does. It is a checklist with teeth and a rebuttal discipline.

---

## 2. Can and cannot

| Question | Can it answer? | Why |
|---|---|---|
| Does the draft support its abstract? | Yes, usefully | The clarity persona audits claim-by-claim against results. |
| Is the main comparison under-controlled? | Yes | Methodologist reconstructs the comparison row by row. |
| Is the effect distinguishable from noise? | Yes, as a flag | Statistician checks n, intervals, multiplicity. The flag is only as good as the reported numbers. |
| Can someone rerun the headline table? | Yes, as a checklist | Reproducibility persona traces number to run, seed, command, data. |
| Is the delta against prior work real? | Partly | The persona demands a documented search; it cannot perform a literature search itself. |
| Would reviewer 2 at NeurIPS like this? | No | Personas are caricatures with known blind spots, written by the authors' side. |
| Will it be accepted? | No | Acceptance is a social process with fit, luck and committee composition. |
| Is the topic important? | No | No persona is tasked with significance beyond "would practice change". |

Read the aggregate as **a defect inventory**, not a verdict.

---

## 3. Files

| Path | Role |
|---|---|
| `06_review/personas/<name>.md` | Persona definition: YAML front matter (name, role, focus, red_flags, scoring_weights) + attack protocol. |
| `<round>/*.PROMPT.md` (generated) | Prompt pack for one persona and one round. Not a review. |
| `<round>/<name>.review.yaml` | The filled-in review. One per persona. |
| `<round>/_MANIFEST.json` | Draft path, sha256, round, prompt hashes, generated timestamp. |
| `<round>/INGEST.md`, `<round>/_ingest.json` | Validation report (written by `ingest`). |
| `<round>/AGGREGATE.md` | Scores, decision distribution, ranked must-fix list, tracker seed. |
| `COMPARE.md` | Round 1 vs round 2: resolved / persisted / new. |
| `06_review/templates/META-REVIEW.md` | Meta-review template, filled by the author after aggregating. |

Generated files are disposable; the persona files and the reviews are the record.

---

## 4. The six personas

Each persona has a different attack surface on purpose. If two reviews read the same, one of
them was written by the same voice and is not doing its job.

| Persona | Attacks | Its blind spot |
|---|---|---|
| `methodologist` | Baselines, ablations, confounds, leakage, metric-claim match, sensitivity. "If the mechanism were removed, would the numbers still look like this?" | Says little about whether the task matters, or whether the prose is readable. |
| `domain_expert` | Construct validity, label provenance, population/scope, field baselines and metrics, framing against the application literature. | Can under-weight statistical and reproducibility detail; may assert field norms without a citation. |
| `statistician` | n, unit of analysis, replication, CIs on the difference, multiplicity, analysis flexibility, small denominators. | Not interested in novelty or writing; will not tell you if the paper is boring. |
| `novelty_skeptic` | Exact delta against the closest prior work, documented search, combination claims, level of contribution, concurrent work. | Cannot run the search; may mistake "I have not seen it" for "it does not exist". |
| `reproducibility_reviewer` | Seeds, commands, environment, data snapshot, number-to-run trace, explicit "what is NOT reproducible", artifact completeness. | Silent on whether the experiment is worth rerunning. |
| `clarity_reviewer` | Abstract overclaim, contribution-to-evidence map, section logic, figure readability, terminology, limitations. | Cosmetic comments can crowd out substance if not filtered. |

Deliberately excluded: an "area chair" persona. The meta-review (section 11) is written by
the author, not simulated, because a simulated AC would launder the authors' own judgement
into an authority it does not have.

---

## 5. Rubric and where it comes from

### 5.1 Scales

**soundness (1-4)** - are the claims supported by the evidence as presented?

| 1 | 2 | 3 | 4 |
|---|---|---|---|
| Major concerns; the central claim is not supported by the design or the numbers. | Significant concerns; a real gap that could change the conclusion. | Mostly sound; minor gaps that do not threaten the main claim. | Sound; claims match evidence, limits stated. |

**presentation (1-4)** - can a competent reader follow and check the paper?

| 1 | 2 | 3 | 4 |
|---|---|---|---|
| Hard to follow; the argument cannot be reconstructed. | Significant clarity problems (structure, figures, undefined terms). | Clear, with local problems. | Clear, well organised, figures readable at print size. |

**contribution (1-4)** - what is added relative to existing work?

| 1 | 2 | 3 | 4 |
|---|---|---|---|
| None, or negative (a claim the evidence contradicts). | Incremental: a dataset swap, a rename, a combination with no new insight. | Solid: a clear delta, compared, useful to the subfield. | Significant: would change how people approach the problem. |

**confidence (1-5)** - the reviewer's confidence in their own assessment.

| 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|
| Educated guess; outside my area. | Some familiarity. | Fairly confident. | Confident; know the area and the baselines. | Certain; know all the relevant work. |

**overall (1-10)** - judgement, not an average of the dimensions.

| 1-3 | 4-5 | 6-7 | 8-9 | 10 |
|---|---|---|---|---|
| Strong reject. | Reject. | Borderline. | Accept. | Strong accept, award-worthy. |

**decision** - `reject` / `borderline` / `accept`, expected to be consistent with overall
(<=4 reject, 5-6 borderline, >=7 accept). `ingest` warns, does not fail, when it is not; a
deliberate deviation must be explained in `summary`.

### 5.2 Provenance: what is modelled on what

Public forms change. This table records what each element is modelled on, and how confident
the wording is. **Verify the current form fields before submission.** No form text is quoted
verbatim in this repo; nothing here is a substitute for reading the venue's current
guidelines.

| Our element | Modelled on | Wording status |
|---|---|---|
| `summary` | NeurIPS reviewer form "Summary"; ACL Rolling Review "Paper summary" | Paraphrase of the field's purpose. Field name remembered, not quoted. |
| `strengths` | NeurIPS "Strengths"; ARR "Strengths" | Field name remembered, not quoted. |
| `weaknesses` | NeurIPS "Weaknesses"; ARR "Weaknesses" | Field name remembered, not quoted. |
| `questions` | NeurIPS "Questions" | Field name remembered, not quoted. |
| `soundness` 1-4 | NeurIPS "Soundness", 1-4 | Range remembered. Anchor descriptions are ours. |
| `presentation` 1-4 | NeurIPS "Presentation", 1-4 | Range remembered. Anchors ours. |
| `contribution` 1-4 | NeurIPS "Contribution", 1-4 | Range remembered. Anchors ours. |
| `confidence` 1-5 | NeurIPS and ARR confidence scales, 1-5 | Range remembered. Anchors ours. |
| `overall` 1-10 | NeurIPS "Overall rating", 1-10 | Range remembered. Band labels ours. |
| `decision` (3-way) | Not a NeurIPS reviewer field. Loosely maps onto ARR's overall-assessment recommendation bands. | **Local design** for triage. Do not paste into a venue form. |
| `must_fix[].claim` / `evidence_needed` | Our addition, inspired by the practice of writing weaknesses that name the missing evidence (ARR's weaknesses + comments sections) | **Local design.** No venue has an `evidence_needed` field. |
| Limitations, ethics flags, code-of-conduct acknowledgement, paper checklist | NeurIPS form fields | **Deliberately not modelled.** Tracked separately in `00_foundations/ETHICS-AND-AI-USE.md`. |

Notes on the difference between the two forms, as remembered (not quoted):

- NeurIPS has used a 1-4 scale for soundness, presentation and contribution, a 1-10 overall
  rating and a 1-5 confidence score; the reviewer form also asks for summary, strengths,
  weaknesses, questions and limitations, and the submission carries a paper checklist. The
  decision (poster/spotlight/oral/reject) is made by the area chair, not entered by the
  reviewer.
- ACL Rolling Review has used 1-5 scales (soundness, excitement, reproducibility, overall
  assessment) plus a confidence score and free-text summary/strengths/weaknesses/comments.
  Exact labels and ranges have changed between cycles.
- We borrow the NeurIPS 1-4/1-10 shape for the three quality dimensions and the overall, and
  add a 3-way decision because a triage label is more useful to us than a 1-10 number alone.

Sources to check (root pages; navigate to the current reviewer guidelines - deep links move
between years and cycles):

- NeurIPS: <https://neurips.cc/> - Conferences > current year > Paper Information >
  Reviewer Guidelines.
- ACL Rolling Review: <https://aclrollingreview.org/> - reviewer guidelines / review form
  pages for the current cycle.

**Verify the current form fields before submission.** If the venue's form differs, edit the
rubric in `rubric_block()` in `tools/simulate_review.py` and the persona weights, then
regenerate the prompts. Do not silently keep scoring on a scale the venue does not use.

### 5.3 Weights

`scoring_weights` in each persona's front matter says where that reviewer spends attention
(methodologist: soundness 0.50 / presentation 0.10 / contribution 0.40; statistician: 0.60 /
0.10 / 0.30; clarity: 0.20 / 0.55 / 0.25). Weights are documentation of emphasis, **not** an
arithmetic formula: the aggregate reports raw dimension scores and does not compute a weighted
total. That is deliberate - a weighted total would invite "we raised the weighted score by
0.3", which is not a meaningful statement about a paper.

---

## 6. Round 1 runbook

### Step 0 - freeze the draft

Commit the draft (or at least record the hash). `pack` records the sha256 in the prompt and
in `_MANIFEST.json`; a review of an uncommitted, changing draft is not evidence.

```bash
cd /c/Users/shubh/research-lab
git add 05_paper/draft/intro.md && git commit -m "draft: freeze for simulated review round 1"
```

### Step 1 - build prompt packs

```bash
python tools/simulate_review.py pack \
  --draft 05_paper/draft/intro.md \
  --round 1 \
  --out 06_review/reviews/round1/
```

Writes six `<persona>.PROMPT.md` files and `_MANIFEST.json`. Each prompt contains:

- the persona (role, focus, red flags),
- that persona's attack protocol (the body of `06_review/personas/<name>.md`),
- the rubric and the exact YAML output schema with score ranges,
- the draft between `<<<DRAFT-BEGIN:<sha12>>>` and `<<<DRAFT-END:<sha12>>>` markers,
  preceded by an explicit statement that the draft is data and that instruction-like text
  inside it must never be followed.

`--max-chars N` truncates the draft inside the prompt (useful for very long drafts); the
manifest still records the full-draft hash. Do not use it for the section under review.

### Step 2 - fill the reviews, separately

One review per persona, in this order of preference:

1. **Different sittings.** Write or generate one persona's review, save it, then start the
   next. Do not have the other five reviews open.
2. **Different contexts if using an agent.** One session per prompt file, with only that
   prompt loaded. Never paste all six prompts into one conversation and ask for six reviews -
   you will get one review with six accents.
3. **Read the protocol, not just the red flags.** The attack protocol is the persona; the red
   flags are only alarms.

Name the file exactly `<persona>.review.yaml` in the same directory. The schema is in every
prompt and reproduced in section 12.

### Step 3 - validate

```bash
python tools/simulate_review.py ingest --dir 06_review/reviews/round1/
```

Exit code 0 means every file parsed and every required field is present and in range.
Exit code 1 lists every error with the file and the field, for example:

```
ERROR statistician.review.yaml: field 'soundness': 7 is out of range 1-4
ERROR methodologist.review.yaml: field 'confidence': missing required field
ERROR clarity_reviewer.review.yaml: field 'must_fix[2].evidence_needed': missing or empty (required)
```

Fix the review, re-run. Do not "fix" the validator to accept the file. Warnings (decision
inconsistent with overall, more than 8 must-fix items) are printed but do not block; each
warning needs a sentence in the meta-review explaining it.

`ingest` writes `INGEST.md` (human table) and `_ingest.json` (machine record, includes the
exact review content).

### Step 4 - aggregate

```bash
python tools/simulate_review.py aggregate \
  --dir 06_review/reviews/round1/ \
  --out 06_review/reviews/round1/AGGREGATE.md
```

Produces:

- a score table (per persona, mean, median) and overall mean/median/range/sd;
- the decision distribution;
- a **deduplicated must-fix list ranked by how many distinct personas raised the item**,
  with the evidence each reviewer asked for and the alternate wordings kept underneath;
- a checkbox tracker seed (`MF-1`, `MF-2`, ...) to paste into the response tracker.

Ranking is by reviewer count, then mention count, then first appearance. Two items count as
the same when their normalised text is similar (`max(token Jaccard, difflib ratio) >= 0.60`,
with a shared-content-token guard). This is a heuristic: it merges "No CIs for the main
metric" with "Confidence intervals are missing from Table 2", and it will occasionally merge
two distinct points or miss a paraphrase. Read the alternate wordings before acting.

### Step 5 - triage, do not average

Do not compute a single "review score" and try to raise it. Work the ranked list:

| Triage | Meaning | Required output |
|---|---|---|
| Fix | The defect is real and in scope. | A concrete change, with file/diff and, where relevant, a new run id. |
| Rebut | The reviewer is wrong, or the draft already answers it and the answer was not findable. | A citation or a result, plus (if it was a findability problem) a text change. |
| Defer | Real, but out of scope for this paper/venue. | A sentence in limitations explaining the boundary, and a note in the meta-review. |

Never "acknowledge" an item without one of the three. A must-fix item with no resolution is
a defect you have decided to ship.

### Step 6 - meta-review

Copy `06_review/templates/META-REVIEW.md` to `06_review/reviews/round1/META-REVIEW.md` and
fill it. It records the per-point resolution, the remaining weaknesses and the decision
rationale. Without it, the aggregate is a list of complaints with no owner.

---

## 7. Reading the aggregate honestly

- **Six reject votes from six personas you wrote is not six independent judgements.** It is
  one draft failing six checklists. That is still useful, but the count is not evidence about
  the venue.
- **A high score is not a green light.** Personas do not know the field's gossip, the
  concurrent work, or the chair's taste. A 7/10 here means "no checklist defect found", not
  "accept".
- **Clustered items are the signal.** An item raised by three lenses (say, missing intervals
  by the statistician, the methodologist and the reproducibility reviewer) is almost always a
  real defect, because the three lenses reached it by different routes.
- **Singleton items still matter** if they are checkable (a missing citation, a figure that
  cannot be read). The ranking is a triage order, not a truth order.
- **The score spread is information.** If five personas say 3 and one says 8, read the 8:
  either that persona saw something the others missed, or it was written too generously.
  Resolve the disagreement in the meta-review rather than averaging it away.

---

## 8. Writing the rebuttal

The rule, and it is absolute:

> **Every substantive point is either addressed by a concrete change (with the file or the
> diff) or rebutted with a citation or a result. Nothing is ignored.**

"Substantive" means any must_fix item, any question that challenges a claim, and any weakness
that names a missing experiment, baseline, citation or number. Typos and style preferences may
be fixed silently or listed in a short "minor changes" paragraph.

### 8.1 The tracker

One row per aggregated must-fix item (the `MF-n` IDs from `AGGREGATE.md`), plus one row per
individual reviewer point that did not cluster. Columns:

| Column | Content |
|---|---|
| `id` | `MF-1` (aggregated) or `R2-3` (individual reviewer point). |
| `raised_by` | Persona names. For a real venue, reviewer numbers. |
| `point` | One sentence, in your words, not a paste of the review. |
| `type` | `change` / `rebuttal` / `defer`. |
| `response` | What you did or why the point does not hold. |
| `evidence` | `path#Lx-Ly`, commit hash, run id, table/figure, citation key. Not "see revised paper". |
| `status` | `done` / `open` / `rejected-with-reason`. |

### 8.2 What a good response looks like

- **Change:** "Added a paired bootstrap 95% CI over five seeds to Table 2
  (`04_experiments/runs/20261103T.../results.json`, commit `a1b2c3d`); the 6.2 point gap has
  CI [2.1, 9.8], so the claim is now stated as a range."
- **Rebuttal with a result:** "The reviewer notes the baseline is untuned. It was tuned over
  the same grid as our method; the sweep is in Appendix B, Table 5, and the best baseline
  configuration is the one reported."
- **Rebuttal with a citation:** "The claim that ROUGE-L cannot measure faithfulness is
  correct for abstractive summarisation; we now cite [key] and report a human faithfulness
  check on 200 samples instead of claiming ROUGE measures faithfulness."
- **Findability fix:** "The split protocol was in Appendix C.3; it is now in Section 4.1 with
  a pointer, because two reviewers could not find it."

### 8.3 What not to write

- "We thank the reviewer for this insightful comment" followed by no change and no argument.
- "We respectfully disagree" with no evidence.
- A new experiment reported for the first time in the response, with no run id, seed or
  committed result file. RULES #2 applies to rebuttals too: a number without a result file is
  not a result.
- A promise ("we will add this in the camera-ready") for a defect that undermines the current
  claims. Either it is in the revision or the claim goes.
- Arguing about taste. Concede factual errors in one clause and move on.

### 8.4 Shape of the response letter

1. One-paragraph summary of the main changes (3-5 bullets, each with a section pointer).
2. Point-by-point, in the reviewers' order, quoting a short phrase of each point (in quotes)
   and answering it under the tracker columns.
3. A "changes not made, and why" subsection for deferred items.
4. A list of new results with run ids and the exact commands.
5. No score requests, no flattery, no speculation about the decision.

Keep a word budget per point (roughly 80-150 words) and a total budget the venue allows. If a
point needs more than 150 words, it probably needed a change instead.

---

## 9. Round 2: proving the points were addressed

Round 2 exists to produce evidence that the revision changed something, not to produce a
higher number.

```bash
python tools/simulate_review.py pack \
  --draft 05_paper/draft/intro.md --round 2 --out 06_review/reviews/round2/

# fill six fresh reviews, then:
python tools/simulate_review.py ingest --dir 06_review/reviews/round2/
python tools/simulate_review.py compare \
  --round1 06_review/reviews/round1/ \
  --round2 06_review/reviews/round2/ \
  --out 06_review/reviews/COMPARE.md
```

`compare` matches must-fix items across rounds by text similarity and reports:

- **resolved** - raised in round 1, not raised in round 2;
- **persisted** - raised in both, with the round-1 and round-2 reviewer sets;
- **new** - raised only in round 2 (revision-induced problems);
- score deltas per persona, mean/median overall, and the reject count.

**Rules for round 2**

1. **Fresh reviews.** Do not copy round-1 reviews and edit the scores. Regenerate from the
   revised draft. The comparison is meaningless if the round-2 text is derived from round 1.
2. **Resolved is not proof.** An item can disappear because the text moved, because a
   reviewer forgot it, or because the revision buried it. For every resolved item, the
   response letter must name the change: file, diff, commit or run id. If there is no change,
   it was not resolved - it was dropped.
3. **Persisted is the priority list.** Any item raised in both rounds is either unaddressed or
   addressed without convincing the reviewer. Both need action: fix it, or rebut it with
   evidence and say so.
4. **New items are revision damage.** A new claim introduced to answer a reviewer often
   introduces a new overclaim. Triage new items before celebrating the resolved count.
5. **Do not compare absolute scores across different drafts as if they were measurements.**
   The primary metric of round 2 is resolved/persisted, not the mean. Score movement is
   context, and the personas are not calibrated instruments.
6. **Stop after two rounds by default.** A third round on the same six personas mostly
   produces noise and consumes time. If items persist after round 2, the honest conclusion is
   that they are out of scope, and they go in limitations - not that a third round will fix
   them.

---

## 10. Meta-review

`06_review/templates/META-REVIEW.md`. It contains: the summary of the discussion, a
per-point resolution table with evidence, the remaining weaknesses (with why they remain),
the decision rationale, and the honesty statement that this was a simulation. Fill it after
`aggregate`, before starting the revision, and update it after `compare`.

The meta-review is where disagreements between personas are resolved. "The statistician says
no interval, the methodologist says the comparison is fine" is not a tie to be averaged; it
is a question to answer by looking at Table 2.

---

## 11. Anti-patterns

| Anti-pattern | What it looks like | Fix |
|---|---|---|
| Single-voice reviews | Six reviews with the same sentence rhythm and the same three complaints. | Separate sittings/contexts; one persona per pass. |
| Sycophancy | All six score 8-9 on a draft with no interval and no baseline. | Re-read the attack protocol; a review with no must-fix item is a failed review. |
| Invented defects | A reviewer demands an experiment the paper already reports. | Every weakness must quote a location; "not reported" requires a search of the draft. |
| Score chasing | Revision targets the mean score instead of the must-fix list. | Track resolved/persisted counts; scores are diagnostics. |
| Silent drops | A must-fix item disappears between rounds with no change. | `compare` flags it as resolved; the response letter must attach a diff. |
| Simulation laundering | "Six reviewers evaluated this paper." | Say "six simulated reviewer personas written by the authors". Always. |
| Rubric drift | Scores stay on a 1-10 scale the venue no longer uses. | Re-check the form; update `rubric_block()` and note the change. |
| Reviewer-as-editor | Clarity review turns into a copy-edit with 40 typos and no claim audit. | Typos go in a separate minor list; must_fix is for claims, structure, figures. |

---

## 12. Review schema (what `ingest` accepts)

```yaml
persona: statistician          # must match the filename and one of the six personas
summary: |                     # non-empty string
  Two to five sentences.
strengths:                     # list of non-empty strings (may be empty, but should not be)
  - "..."
weaknesses:                    # list, at least one
  - "..."
questions:                     # list (may be empty)
  - "..."
soundness: 2                   # integer 1-4
presentation: 3                # integer 1-4
contribution: 2                # integer 1-4
confidence: 4                  # integer 1-5
overall: 4                     # integer 1-10
decision: reject               # reject | borderline | accept
must_fix:                      # 1-8 items
  - claim: "One sentence naming the defect."
    where: "Table 2"           # optional, but required in practice
    evidence_needed: "What would settle it: run, interval, citation, diff."
```

Validation rules enforced by `ingest`:

- every field above present (`questions` and `strengths` may be empty lists, the rest may not);
- scores are integers in range (floats with an integral value are accepted and cast);
- `decision` is one of the three labels (case-insensitive);
- `must_fix` is a non-empty list of mappings with non-empty `claim` and `evidence_needed`, and
  no keys other than `claim`, `where`, `evidence_needed`;
- `persona` matches the filename stem and is one of the six;
- one review per persona per directory (duplicates are an error).

Errors name the file and the field, and the command exits non-zero. Nothing is written into
`AGGREGATE.md` if any review is invalid.

---

## 13. AI assistance and integrity

RULES #4 applies. The paper must disclose AI assistance (tools and purpose) following the
target venue's policy, and Shubh must be able to defend every section.

- Writing six reviews with an LLM is AI assistance to the *authors*, used for internal QA.
  It is not a review, not independent evaluation, and must not be presented as either.
- If an LLM drafted or rewrote manuscript text in response to a simulated review, that is
  assistance to disclose, exactly like any other drafting help.
- The prompt packs contain the draft. If the draft is confidential or under submission
  elsewhere, check the venue's policy before pasting it into any external tool. The
  orchestrator itself makes no network calls, but whatever fills in the review might.
- Do not let a simulated review supply citations. A persona can say "cite the nearest prior
  work"; it cannot know the DOI. Every citation still goes through
  `tools/verify_citations.py` and `02_literature/verified_citations.csv`.
- The meta-review's honesty statement is mandatory, not decorative.

---

## 14. Known limits, and what would change them

1. **No model in the loop.** `simulate_review.py` builds prompt packs and validates output.
   Any impression that it "runs reviewers" is wrong; the README-style header in every prompt
   says so.
2. **The similarity threshold is a heuristic** (0.60 on `max(Jaccard, difflib)`). Tune it only
   with evidence: false merges are worse than missed merges, because a false merge hides a
   distinct defect inside a ranked item. The alternate-wordings block exists so a human can
   audit the merge.
3. **Persona blind spots are structural.** Six lenses, six blind spots. Do not delete a
   persona because it is annoying; add a seventh only if it attacks something none of the six
   does.
4. **Form fields drift.** The rubric is a snapshot; section 5.2 says which parts are
   remembered and which are ours. Re-verify against the current NeurIPS/ARR guidelines before
   submission, and record the date checked.
5. **Scale of the check.** This procedure reviews a section or a short paper draft, not a
   50-page appendix. For a full paper, run `pack` per section with the same personas and
   aggregate the section reviews into one tracker by hand.

---

## 15. Test coverage

```bash
python -m pytest tools/tests/test_simulate_review.py -q
```

Nine tests, run against the real CLI in a subprocess: pack creates exactly six prompts each
containing its persona name and the draft text (and refuses a draft containing the delimiter);
ingest accepts a valid review and rejects an out-of-range score, a missing field, a bad
decision and a must-fix without `evidence_needed`, naming the file and field; aggregate ranks
a must-fix raised by three personas as rank 1, dedupes three phrasings into one row, and
reports scores and decision distribution; compare reports an item present in round 1 and
absent in round 2 as resolved and keeps the persisting item, and refuses an invalid round.
