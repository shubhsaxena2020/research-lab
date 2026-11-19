# PROGRESS — R3-4f-bind-3b

Lane: R3-4f-bind-3b (integrator, res-s4). Card: sessions/R3-4f-bind-3b/TASK.md.
Gate note: TASK.md HEAD NOTE (2026-11-19 01:40 IST) releases this lane — R3-4e was stopped by the head
at 01:32 with no files written and the draft unchanged (sha d81cc90ffe60), so there is no 4e evidence to
wait for. Lane launched after that handoff.

## Batch 0 — lead ground truth (before any subagent)

Read: RULES.md, orchestration/HEAD-REVIEW.md (Checkpoint 11 latest), sessions/R3/COMMON.md,
sessions/R3/TRIAGE.md, this lane TASK.md, ops/lead_protocol_r3.txt, R3-3b ANSWERS.md and its three JSONs.

Baseline state, measured (not assumed):
- draft sha256 `d81cc90ffe60a9e58c86aff04cb6fcea0958cc25de5ea512574a05c04a679500` (05_paper/draft/paper.md)
- template sha256 `fc3178a1f9aef12116760b5d1fc587b947517754dc6cfaaa860ca80ab011c0af`
- `python tools/check_numbers.py --draft 05_paper/draft/paper.md` -> 509 numbers, 322 matched, 187 exempt,
  0 findings, PASS
- `python tools/check_all.py` -> 4/4 steps passed
- response letter: 85 canonical IDs, verdicts parsed as 28 resolved / 46 partial / 11 deferred
- files are CRLF; edits must preserve CRLF (scripts written under sessions/R3-4f-bind-3b/repro/)

Known block, resolved before delegating: R3-3b `results{}` keys are literal dotted strings
(`c1.r3_3b.mf17.frozen_heldout_auroc.point`), but `tools/check_numbers.py` resolves an index `key` as a
dotted path, so it cannot address a key that itself contains dots. The same evidence files carry the same
values in nested blocks (`aurocs.<scope>.point`, `paired_diffs.<scope>.ci_item.*`, `mf10.agreement.*`,
`details.d3_pooled.*`). Index entries therefore point at the nested path, with the flattened `results` key
named in the entry description, and a lane script asserts nested value == flattened value for every entry.
No new numbers, no new analyses, no file written under 04_experiments/results/.

## Binding block identified and resolved on paper (not yet applied)

`tools/check_numbers.py:lookup_value` resolves an index `key` as a dotted path (`key.split(".")`), so it
cannot address R3-3b's literal dotted `results` keys (e.g. `c1.r3_3b.mf17.frozen_heldout_auroc.point`).
The same evidence files carry identical values in nested blocks (`aurocs.<scope>.point`, `.ci_item.lo/hi`,
`paired_diffs.<scope>.ci_item.*`, `mf10.agreement.*`, `mf10.resolved.*`,
`details.gold_indicator_control.*`, `details.d3_pooled.all.*`). Decision: index entries point at the nested
path, name the flattened `results` key in the entry description, and a lane script must assert nested value
== flattened value for all 26 entries. No new numbers, no new analyses, nothing written under
04_experiments/results/.

Verified nested values (read directly from the three JSONs):
- mf17: frozen point 0.9823630831643002, ci_item [0.9776211411662427, 0.9866543835742593];
  corrected 0.8738488843813388, [0.8586833140203312, 0.8893003500532195]; paired ci_item diff
  0.10851419878296142 [0.09458017350090517, 0.12252082237972457], contains_zero false; paired ci_cluster
  [0.10110016227207592, 0.1142774512332159]; denominators.held_out_common.n_items 1879,
  n_article_clusters 18; seed 20261118; n_boot 10000
- mf10: kappa 0.2801966292134831, po 0.59, n_items 100, n_agreed 59, n_disagreed 41,
  resolved.overall_answerable_n 56, share 0.56; earlier-run block prior_kappa 0.1975,
  prior_resolved_answerable_n 5 — deliberately NOT quoted in the draft (not in `results`)
- mf7: dev r1 auroc_surface_lex 0.9762, auroc_plus_is_gold 1.0, auroc_is_gold_alone_answerable_oriented 1.0;
  details.d3_pooled.all n_hit 655, n_miss 145, surface_lex_auroc 0.7327;
  per_rung_R1_R3_estimand_available false (boolean — prose only, never bound)

Number-format pre-check: `tools/check_numbers.py` was run against a scratch copy of the draft with the
candidate sentences appended (scratch file deleted afterwards). The 3-decimal prints 0.978/0.987/0.859/
0.889/0.109/0.095/0.123/0.101/0.114 plus 0.976/0.733/0.2802/0.59 round inside half-ULP of their stored
values; unmarked digits are reported as findings as expected; `rung-1–4` leaves the `4` untraceable, so that
phrase must be avoided (write "the R1–R4 negatives").

## Batch 1 — planned in full, NOT executed

Three parallel, non-overlapping tasks were specified but the run-time budget expired before the blocking
`delegate_task` call could be made:
- T1 index writer -> `04_experiments/RESULTS-INDEX.json`: 26 `c1.r3_3b.*` entries (nested key + flattened
  key named in the description + tolerance 0 for counts / 0.0005 for rates), plus
  `sessions/R3-4f-bind-3b/repro/verify_r3_3b_index.py` proving nested == flattened for every entry.
- T2 template writer -> `05_paper/template/draft_template.md`: §1 and §4.6 H1 verdicts to the Table 4
  wording ("not exercisable at the registered operating point", no H1 "refuted" left anywhere), §3.6 "the
  registered analysis reports no AUROC interval" + pointer to §4.6, §4.6 post-hoc interval paragraph, §4.1
  gold-indicator (MF-7) paragraph, §4.7 fifth check (MF-10) and "Four"->"Five", every new number bound,
  CRLF preserved through a script under sessions/R3-4f-bind-3b/repro/.
- T3 letter writer -> `06_review/RESPONSE-LETTER-R3.md`: MF-7 partial, MF-10 resolved (LLM-not-human-gold
  limit stated), MF-17 resolved, R3-MF-16 partial (main pair integrated, ablation intervals still missing),
  MF-25 evidence note, re-parsed tally line (expected 30 resolved / 48 partial / 7 deferred = 85).

## State of the tree at this stop

- 05_paper/template/draft_template.md: UNCHANGED (sha fc3178a1...)
- 05_paper/draft/paper.md: UNCHANGED (sha d81cc90ffe60...), not rebuilt
- 04_experiments/RESULTS-INDEX.json: UNCHANGED (207 entries, no `c1.r3_3b.*` entry)
- 06_review/RESPONSE-LETTER-R3.md: UNCHANGED (28 resolved / 46 partial / 11 deferred)
- Frozen results, runs, PREREGISTRATION and hash history untouched; 05_paper/latex-build untouched; no
  state-changing git command; no new analyses, model calls or result files.
- Side effect of the mandatory gate run, disclosed: `python tools/check_all.py` step 4 executes
  `04_experiments/toy/run_pipeline.py`, which rewrote the TOY-labelled artifacts
  `04_experiments/results/summary_toy.json`, `04_experiments/toy/toy_runs.json` and created untracked
  `04_experiments/runs/*toy*` directories, and it changed only the `run_id`/`updated_at` fields of the two
  toy entries in `04_experiments/RESULTS-INDEX.json`. The index was restored byte-for-byte from
  `git show HEAD:04_experiments/RESULTS-INDEX.json` (57002 bytes, 207 entries, updated_at 2026-11-18T17:45:59Z,
  sha256 5a30a5b3fd15039b...); no real result, frozen run or preregistration file was affected. The toy
  outputs are labelled [TOY - NOT A RESULT] and were left in place rather than deleted.
- None of the card's deliverables was integrated, and no gate was run against an edited draft.

CARD BLOCKED: run-time budget exhausted before batch 1 — no R3-3b value is bound into the template, the
generated draft, RESULTS-INDEX or the response letter; the H1 contradiction at template L437-438 and L83 is
still present; no gate was run on an edited tree. Resume by dispatching the three batch-1 tasks exactly as
specified above.
