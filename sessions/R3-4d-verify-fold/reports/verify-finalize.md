# Verify-finalize — post-fold reconciliation (R3-4d-verify-fold)

## Files touched

- **Modified:** `sessions/R3-4d-verify-fold/VERIFY-RESOLVED.md` — appended a clearly labelled
  `## Post-fold status (final, after batches 2 and 3)` section (lines 41–86). The 23 original audit
  rows and the `## Summary` lines (lines 1–38) were left verbatim; the new section explicitly states
  it supersedes their verdicts.
- **Created:** this report.
- Not touched: response letter, template, generator, draft, `05_paper/latex-build/**`.

## What was done

1. Re-parsed `06_review/RESPONSE-LETTER-R3.md` (451 lines): matched each of the 23 item IDs to its
   section (`## MF-n` / `### R3-MF-n`) and read the first `Verdict:` line. The letter's own header
   reports 28 resolved / 46 partial / 11 deferred = 85 canonical items; this lane re-parsed the
   23-item subset directly rather than trusting the header.
2. Reopened `05_paper/draft/paper.md` (707 lines, sha256 `d81cc90ffe60…` per `folds-batch3.md`) and
   verified a short evidence quotation (with current line number) or `MISSING` for each of the 23
   items. Also checked the generator (`04_experiments/src/make_paper_assets.py` L588–594) and template
   placeholders for the MF-35 prefix-alignment evidence.
3. Cross-checked the change provenance against `reports/mf14-fix.md`, `reports/letter-upgrades-batch3.md`
   and `reports/folds-batch3.md`.
4. Appended the reconciliation table (`item ID | audit verdict | current letter verdict | current draft
   evidence | note`), plus a tally/notes block. Verified the section has exactly 23 rows, the IDs match
   the original 23 with no omissions or extras, and the verdict columns parse cleanly.

## Findings

- **Audit verdicts (preserved):** 13 resolved / 10 partial.
- **Current letter verdicts for the same 23:** **17 resolved / 6 partial / 0 deferred.**
- **Four upgrades** (audit partial → current resolved), all with current letter and draft evidence:
  - **MF-14** — FIXED by batch 2: registered band R4 100.00% now beside corrected exploratory R4
    12.53%, D4 marked exploratory/post-hoc, §5.2 scoped (draft L48–50, L592).
  - **MF-35** — batch-3 fold 4 aligned generator prefixes and template placeholders to caption
    appearance order (T1_prior_work … T7_ablations_corrected; draft captions Tables 1–7).
  - **MF-40** — batch-3 letter wording correction "all eight tables" → "all seven tables" plus the
    prefix alignment; seven numbered captions present. Note: the L246 caption still defers n to
    Table 3 — recorded as a retained audit observation, not part of the corrected letter wording.
  - **R3-MF-39** — batch-3 fold 1 removed all five "abstain recall" occurrences (0 remain in draft);
    refusal-rate/precision definitions preserved at L221–223.
- **Six items remain partial**, each with a concrete reason recorded in the table:
  - MF-1 — exact fractions 400/400, 279/280, 1478/1780 never printed (only 83.03%).
  - MF-8 — cell counts 279/280 and 279/(279+302) never printed (only 99.64% / 48.02%).
  - MF-11 — no per-rung length/overlap distributions; R5 matched on overlap only (10.29% residue)
    and called the longest negatives (L401).
  - MF-15 — 400/400, 279/280, 1760/1873, 1478/1780 absent; percentages only.
  - MF-20 — cap-on-dev distinction and 11.00% breach present; corrected dev over-refusal value absent.
  - MF-39 — refusal counts behind cells (279, 302, 400/400) absent from `paper.md`; this is the
    round-2 item, distinct from the upgraded R3-MF-39.
- **No originally resolved item is now deferred** — every one of the 23 is `resolved` or `partial`
  in the current letter. No item was downgraded further.
- Batch-3 folds also upgraded **MF-13** (§3.4 two-sided rule, L205–208) and **MF-29** (§4.7
  construction-degeneracy wording, L542–544). Both were `partial` at the audit and were **never in the
  23-item originally-resolved set**; they are noted in the section for context and excluded from the
  17/6 tally. The task wording grouped them with the R3-MF-39 fold; the table therefore keeps the
  23-item contract intact and records MF-13/MF-29 separately in the notes block.

## Verification performed

- Programmatic row count: 23 post-fold rows; ID set equals the original 23 exactly (no missing/extra).
- Column parse: audit 13 resolved / 10 partial; current 17 resolved (13 plain + 4 bold) / 6 partial;
  zero deferred rows.
- 42 quote/line pairs from the new table were checked against the current draft; one stale citation
  (MF-38 "one question in four" spans L582–583) was corrected to L582–583, and a missing parenthesis
  in the MF-13 note was fixed. All citations now match the current draft.

## Issues encountered

- The round-3 items use `###` headers in the letter, so the initial `##`-only parser returned no
  verdicts for five IDs; the parser was corrected to accept both heading levels and re-parsed all 23.
- The batch-3 letter upgrades were written while the parallel writer's folds were still pending
  (flags in `letter-upgrades-batch3.md`); the current draft now contains the folded evidence for
  MF-13/MF-29/MF-35/R3-MF-39, so no verdict needs reverting on that basis.
