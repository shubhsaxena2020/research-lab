# Verification consolidation — R3-4d

Inputs: `sessions/R3-4d-verify-fold/reports/audit-A.md`, `audit-B.md`, `audit-C.md`; generated draft `05_paper/draft/paper.md`; response letter `06_review/RESPONSE-LETTER-R3.md`. The template and generated draft were not edited; `05_paper/latex-build/**` untouched.

## 1. Created: `sessions/R3-4d-verify-fold/VERIFY-RESOLVED.md`

One row per item marked `resolved` before this pass (23 rows). Columns: item ID | claim | exact draft quotation with line numbers (or MISSING) | final verdict. Audit quotations were reopened against `paper.md`; because the draft had shifted, verified current line numbers are listed first and the audit's stale numbers in parentheses. Final verdicts: 13 resolved, 10 partial (Audit-C 'Implemented'→resolved, 'Not implemented'→partial).

- Resolved (13): MF-2, MF-26, MF-27, MF-33, MF-34, MF-38, MF-41, MF-42, MF-43, R3-MF-3, R3-MF-36, R3-MF-37, R3-MF-38.
- Partial (10): MF-1, MF-8, MF-11, MF-14, MF-15, MF-20, MF-35, MF-39, MF-40, R3-MF-39.

## 2. Modified: `06_review/RESPONSE-LETTER-R3.md` — 10 verdict downgrades

Each `Verdict: resolved (...)` line was changed to `Verdict: partial (...)`, and a `Downgrade reason (R3-4d verification, audit-X): ...` sentence was appended to that item's Change/Resolved description.

| Item | Exact OLD verdict line | Exact NEW verdict line | Reason (concrete, audit-based) |
|---|---|---|---|
| MF-1 | `Verdict: resolved (folded from lane R3-1)` | `Verdict: partial (folded from lane R3-1)` | Definitions and percentages present; exact fractions 400/400, 279/280, 1478/1780 absent; draft prints 83.03%, not 83.0% with denominator 1780 (audit-A). |
| MF-8 | `Verdict: resolved (folded from lane R3-1)` | `Verdict: partial (folded from lane R3-1)` | Definitional split and 99.64%/48.02% present; cell counts 279/280 and 279/(279+302) never printed (audit-A). |
| MF-11 | `Verdict: resolved (owned R3-4)` | `Verdict: partial (owned R3-4)` | 'One respect at a time' clause present; no per-rung length/overlap distributions; R5 matched on overlap only (10.29% residue) and L399 calls R5 the longest negatives (audit-A). |
| MF-14 | `Verdict: resolved (folded from lane R3-3)` | `Verdict: partial (folded from lane R3-3)` | Pre-fix state: corrected exploratory R4 12.53% sits beside frozen exploratory 84.71%, not registered band 100.00%; D4 not primary; §5.2 not scoped. Separate writer fixing template; reason recorded against audited pre-fix state (audit-A). |
| MF-15 | `Verdict: resolved (folded from lane R3-1)` | `Verdict: partial (folded from lane R3-1)` | Only percentages appear; no 400/400, 279/280, 1760/1873 or 1478/1780 anywhere in the draft (audit-A). |
| MF-20 | `Verdict: resolved (folded from lane R3-1)` | `Verdict: partial (folded from lane R3-1)` | Cap-on-dev distinction and 11.00% breach present; corrected dev over-refusal value absent (audit-A). |
| MF-35 | `Verdict: resolved (owned R3-4)` | `Verdict: partial (owned R3-4)` | Table numbering/captions/cross-refs aligned, but generator prefixes not: T7_prior_work→Table 1, T3_audit→Table 2, T1_per_rung→Table 3, T2_hypotheses→Table 4 (audit-B). |
| MF-39 | `Verdict: resolved (folded from lane R3-1)` | `Verdict: partial (folded from lane R3-1)` | Definition and R2 48.02% present; refusal counts behind cells (279, 302, 400/400 denominators) not printed in paper.md (audit-B). |
| MF-40 | `Verdict: resolved (owned R3-4)` | `Verdict: partial (owned R3-4)` | Draft has seven tables, not eight; Table 2 caption defers n to Table 3 ('n per rung as listed in Table 3', draft L244) (audit-B). |
| R3-MF-39 | `Verdict: resolved (folded from lane R3-1)` | `Verdict: partial (folded from lane R3-1)` | §3.5 definitions present, but 'abstain recall' still appears in Abstract (L17), §3.3 (L182) and §3.5 (L221); removal claim false (audit-C). |

## 3. Modified: response-letter header tally

OLD header line (line 5):

```
Status: final R3 verdicts assigned per `06_review/reviews/COMPARE-round2-round3.md` (18 resolved, 21 partial, 5 deferred); lane ownership and concrete changes recorded below. No fabricated numbers: every value is a registered result key or a file-cited fact.
```

NEW header lines (line 5 amended; new line 6 added):

```
Status: final R3 verdicts assigned per `06_review/reviews/COMPARE-round2-round3.md` (round-2 split 18 resolved, 21 partial, 5 deferred); lane ownership and concrete changes recorded below. No fabricated numbers: every value is a registered result key or a file-cited fact.
Canonical tally after R3-4d draft verification: **13 resolved, 61 partial, 11 deferred = 85 canonical items** (round-2 MF-1…MF-44 plus round-3 R3-MF-1…R3-MF-41). This supersedes the orchestration brief's '23 resolved, 52 partial, 11 deferred = 86': there are 85 distinct canonical IDs, and the pre-downgrade partial count was 51, not 52 (the brief is off by +1 partial and +1 total). Ten items previously marked resolved were downgraded to partial after draft verification (MF-1, MF-8, MF-11, MF-14, MF-15, MF-20, MF-35, MF-39, MF-40, R3-MF-39), moving the split from 23 resolved / 51 partial to 13 resolved / 61 partial; 11 deferred are unchanged. Later batches may change these numbers again; re-parse the `Verdict:` lines rather than relying on this line.
```

Counting error explained: the brief's 23/52/11 = 86 overstates both partial and total by one. The letter parses to 85 distinct canonical IDs with 51 partial before this pass (audit-B §Inventory and count reconciliation: MF-1…MF-44 = 44 plus R3-MF-1…R3-MF-41 = 41; no duplicates or orphans), and 23 resolved / 11 deferred. Downgrading 10 resolved to partial gives 13 / 61 / 11 = 85.

## 4. Parsed tally after edits (from the final letter file)

Parsing all `^Verdict:` lines in `06_review/RESPONSE-LETTER-R3.md`:

- resolved: 13
- partial: 61
- deferred: 11
- total: 85

By round: round 2 — 9 resolved, 30 partial, 5 deferred (44); round 3 — 4 resolved, 31 partial, 6 deferred (41). Resolved IDs remaining: MF-2, MF-26, MF-27, MF-33, MF-34, MF-38, MF-41, MF-42, MF-43, R3-MF-3, R3-MF-36, R3-MF-37, R3-MF-38.

Verified: each of the 10 downgraded sections contains exactly one `Downgrade reason` sentence on its Change/Resolved description line; the 13 remaining resolved IDs match the 13 resolved rows in VERIFY-RESOLVED.md. Later batches may change these numbers again.
