# Review — batch-3 writer outputs (folds + letter upgrades), R3-4d-verify-fold

Independent re-review of the batch-3 writer outputs. Workdir `C:\Users\shubh\research-lab`.
No source/template/generator/draft/letter file was edited by this review; only this report was created.

Files read: `sessions/R3-4d-verify-fold/reports/folds-batch3.md`,
`letter-upgrades-batch3.md`, `review-batch2.md`; live artifacts `05_paper/template/draft_template.md`,
`04_experiments/src/make_paper_assets.py`, `05_paper/draft/paper.md`,
`05_paper/tables/generated/`, `06_review/RESPONSE-LETTER-R3.md`, `06_review/audits/numbers-audit.md`.

Current draft: sha256 `d81cc90ffe60a9e58c86aff04cb6fcea0958cc25de5ea512574a05c04a679500`, 61620 bytes —
the post-fold sha recorded in `folds-batch3.md`; the pre-fold sha `1679b75f…` quoted in
`letter-upgrades-batch3.md` is no longer current.

## Verdict

All four machine-checkable claims (a)–(c) reproduce exactly: the four folds landed, the MF-14 fix is
intact, and the response-letter tally/15 upgrades are correct. One documentation mismatch remains
(d): the "flags for review / parallel-writer fold PENDING" note in `letter-upgrades-batch3.md` is now
stale because those folds have since landed. No functional defect found; no verdict needs reverting.

## (a) Four batch-3 folds landed — CONFIRMED

1. **R3-MF-39 ("abstain recall").** `grep -in "abstain recall"` returns **no matches** in either
   `draft_template.md` or `paper.md`. The letter still contains the term only inside historical
   section titles / downgrade reasons (e.g. letter L433–438), which is expected. Refusal-rate and
   precision definitions remain (draft §3.5, L212–224).
2. **MF-29 (§4.7 construction-degeneracy).** Draft L540–544 reads verbatim:
   "...refuse the same items to within `<!-- num:c1.st.match.maxdiff -->0.00<!-- /num --> points: the
   recall-matched single threshold is the band's own lower threshold (to five decimal places), so the
   upper threshold never binds and the zero difference is **degenerate by construction**." The old
   "zero discordant pairs … not a binning artefact" phrasing is gone from draft and template; the
   `c1.st.match.maxdiff` marker is retained (no new number/key).
3. **MF-13 (§3.4 two-sided note).** Draft L205–209: "A two-sided reading of **|AUROC − chance|** would
   flag both directions, inverted separation included, ... and we keep the pre-registered one-sided
   rule. R4 comes out at `<!-- num:c1.audit.surface.r4 -->0.415<!-- /num -->`...". The word "chance"
   is used — no bare `0.5` numeral was introduced (grep for `AUROC … 0.5` finds none). Marker unchanged.
4. **MF-35 (table prefixes).** Generator write paths `make_paper_assets.py` L588–594 are
   `T3_per_rung`, `T4_hypotheses`, `T2_audit`, `T6_frozen_vs_corrected`, `T5_arms`,
   `T7_ablations_corrected`, `T1_prior_work`; template `{{TABLE:…}}` placeholders (L132/244/259/263/365/
   417/421) read T1_prior_work, T2_audit, T3_per_rung, T4_hypotheses, T5_arms,
   T6_frozen_vs_corrected, T7_ablations_corrected. Draft table captions appear in that same order
   (Table 1–7 at L130/246/267/278/384/444/468), and all seven newly named generated files exist with
   matching headers. No stale prefix is referenced by the template, draft, or `build_draft.py`
   (grep for the six old names in those files: none). Six stale old generated files plus `.tex`
   files remain untracked on disk — benign, as reported in `folds-batch3.md`.

## (b) MF-14 fix still intact — CONFIRMED

Draft Abstract L48–50 and §4.6 L488–491 carry all three R4 figures with distinct num markers and
explicit run labels: `c1.band.precision.r4.run` 100.00% "registered band (frozen, D1) run",
`c1.expl.precision.r4.run` 84.71% "frozen exploratory (as-run, D1) run", and
`c1.expl.precision.r4.corr` 12.53% "spec-corrected exploratory (post-hoc, D4) run". §5.2 opens with
the scope restriction at L592 ("scoped to the corpus, feature stack and gate family measured here").
All present in the template too (L48–50, L430–433, L534). Matches `review-batch2.md` (a) and
`mf14-fix.md`.

## (c) Response-letter tally and 15 upgrades — CONFIRMED

Programmatic parse of `06_review/RESPONSE-LETTER-R3.md`:

- 85 `Verdict:` lines; Counter = `{'resolved': 28, 'partial': 46, 'deferred': 11}`; sum **85**.
- Header line 6 states "**28 resolved, 46 partial, 11 deferred = 85 canonical items**" — consistent.
- All **15** upgrade items carry `Verdict: resolved` at their section headers: MF-4 (L20), MF-5
  (L25), MF-13 (L58), MF-14 (L63), MF-25 (L108), MF-29 (L125), MF-30 (L130), MF-35 (L151),
  MF-37 (L160), MF-40 (L173), R3-MF-2 (L208), R3-MF-4 (L221), R3-MF-28 (L366), R3-MF-39 (L433),
  R3-MF-40 (L440). 15/15 verified; no missing or non-resolved verdict.
- Numbers audit on the current draft reports **PASS**, 0 findings, 509 scanned / 322 matched /
  187 exempt — identical to the baseline and to `folds-batch3.md` (no new numeric claims).

## (d) Remaining mismatch — STALE DOCUMENTATION (no action needed on artifacts)

`letter-upgrades-batch3.md` still documents four folds as not-yet-landed:
- L13 header: "...are landed on the parallel writer's batch-3 folds and are flagged for review ...
  because their draft evidence was not present at edit time."
- L74/77/79/85: evidence notes labelled "parallel-writer fold **PENDING** in current draft"
  (MF-13, MF-29, MF-35, R3-MF-39), quoting draft sha `1679b75…`.
- L88 "## Flags for review — parallel-writer folds not present at edit time" and L90 instruction
  "Re-verify after the parallel writer's fold lands; if a fold fails, revert that verdict to
  `partial` and adjust the tally accordingly."

This is now stale: the folds **have** landed (section (a) above; draft sha advanced to
`d81cc90…`), so the documented "PENDING / revert if failed" contingency no longer applies. The
four upgrades remain `resolved`, and the 28/46/11 tally stands — no revert is warranted. Report as
a **documentation mismatch only**; the note is a historical record of the letter-edit moment, not a
defect in the artifacts.

Related (same root cause, not a separate defect): the response letter's own four "parallel-writer
fold PENDING in current draft" evidence notes (letter L74, L77, L79, L85-adjacent sections MF-13,
MF-29, MF-35, R3-MF-39) and the downgrade reasons quoting the old line numbers are likewise
historical and no longer describe the live draft.

## Other observations

- `check_numbers.py`'s audit file (`06_review/audits/numbers-audit.md`) is regenerated with a fresh
  timestamp; this is the documented gate side effect, not a writer edit.
- No new mismatch found in (a)–(c); the only remaining discrepancy is the stale flag note in (d).
- No files were modified by this review.
