# Review: md2tex.py number preservation

**Date:** 2026-11-08
**Scope:** `05_paper/latex-build/md2tex.py`, `05_paper/latex-build/tests/test_md2tex.py`, `05_paper/draft/paper.md` → `05_paper/latex-build/body.tex`
**Owned file:** this report only (`sessions/R3-7-latex/reports/review-converter.md`)

## Verdict: PASS — 296/296 numbers preserved, 0 mismatches

```
Command (from repo root C:\Users\admin\research-lab):
  python 05_paper/latex-build/tests/test_md2tex.py

Output:
  wrote C:\Users\admin\research-lab\05_paper\latex-build\body.tex
  PASS: 296 numbers preserved in body.tex
  exit code 0
```

Note: the test emits a Python `SyntaxWarning` at line 26 (`"\%"` is an invalid escape sequence — should be `"\\%"` or a raw string). It is harmless (the escaped check still works because `"\%"` evaluates to `"%"`... see caveat below), but it should be fixed. See §4.

## §1. How number preservation works (code inspection)

`md2tex.py` preserves numbers by design, in two steps:

1. **`strip_num_markers()` (lines 11–13)** — regex `<!--\s*num:[^>]*-->(.*?)<!--\s*/num\s*-->` with capture group 1 replaced verbatim. The inner value is spliced byte-identical; no parsing, no rounding, no reformatting. Verified: `body.tex` contains 0 leftover `num:` / `/num` markers; `paper.md` contains 296.

2. **`convert_inline_safe()` (lines 74–99) → `esc()` (lines 16–48)** — digits `0–9` fall through to the `else` branch and pass unchanged. The only numeric-relevant transformations in `esc()`:
   - `%` → `\%` (180 of the 296 numbers end in `%`; all 180 appear escaped; 0 raw `%` left in `body.tex` — 191 `\%` total in tex vs 191 `%` in md).
   - Unicode minus U+2212 → ASCII `-`, em-dash → `---`, en-dash → `--`. The one U+2212 in `paper.md` (line 277, "R1 − R3") is prose, not inside a `num:` marker; the 4 negative numbers (`-2.23%`, `-3.11%`, `-1.35%`) use ASCII `-` and survive byte-identical.
   - No `round()`, `float()`, or `.format()` anywhere in `md2tex.py` (grep-verified). Numbers are never parsed as floats, so 2-decimal vs 3-decimal precision cannot be altered.

Idempotence: re-running `md2tex.py` produces a byte-identical `body.tex` (sha256 `99f98b22…ad01be4d7ac874dfe5aa4d22efad`, 45974 bytes, 1091 lines).

## §2. Independent diff (not relying on the test)

Re-extracted all 296 `num:` values from `paper.md` independently and checked each against `body.tex`:

- **296 total, 142 unique** values. 68 values repeat (e.g. `0.00%` ×20, `100.00%` ×18).
- **0 missing** under the test's own criterion (byte-identical, or `%`→`\%` form).
- All 180 `%-ending` numbers appear in escaped `\%` form; none found only as a substring of a longer number.
- All 3 negative numbers (`-2.23%`, `-3.11%`, `-1.35%`) present byte-identical (escaped form).
- Table numbers: extracted all numeric tokens from the 65 pipe-table lines in `paper.md` — 0 missing in `body.tex`. 8 `\begin{table}` environments in tex.
- Table caption numbers: captions contain only `Table 1` / `Table 4` references; both present.

Sample (first 30 unique numbers, contexts from `body.tex`):

| Number | Status | Context |
|---|---|---|
| `0.80` | byte-identical | "dev abstain precision of 0.80 --- produced a gate…" |
| `75.50%` | escaped `75.50\%` | "refuses 75.50\% of answerable questions…" |
| `24.50%` | escaped | "answers only 24.50\% of the questions…" |
| `83.03%` | escaped | "items it refuses is 83.03\% pooled" |
| `100.00%`, `99.64%`, `0.00%` | escaped | "per-rung refusal rate is 100.00\%, 99.64\%, …" |
| `0.506`, `0.539`, `0.488`, `0.415` | byte-identical | "(AUROC 0.506, 0.539, 0.488, 0.415)" |
| `0.977`, `0.889`, `0.923` | byte-identical | "(0.977, 0.889, 0.923)" |
| `56.98%`, `48.02%` | escaped | "precision is 56.98\% on R1 and 48.02\% on R2" |
| `0.982`, `0.874` | byte-identical | "from 0.982 to 0.874 AUROC" |
| `35`, `1204`, `11873`, `5928` | byte-identical | "contains 35 articles, 1204 paragraphs and 11873 questions, of which 5928…" |
| `3752`, `1879`, `273` | byte-identical | "yields 3752 items (1879 held out); R2 is short at 273 dev items…" |

## §3. Substring false-positive check (test strictness)

The test's `n in tex` check is a substring test, so short numbers could pass spuriously (e.g. `98%` inside `56.98\%`, `1%` inside `91.07\%`). Independently verified every substring-prone value also has a **standalone** occurrence:

- `98%` → standalone `98\%` exists ("accuracy falling from 98\% to 1\%"); 6 total occurrences.
- `1%` → standalone `1\%` exists; 7 total occurrences.
- `35` → 1 standalone + 1 inside `-3.11\%` context (164/1204/11873 counts match).
- `273`/`400`/`280`/`553` exact occurrence counts match marker counts (3/3/2/2). `3752`/`5928` ×1 each.

So the PASS is genuine, not a substring artifact.

## §4. Issues found (non-blocking)

1. **SyntaxWarning, cosmetic (test only):** `tests/test_md2tex.py:26` uses `"\%"` (invalid escape). Harmless today but will break under `-W error` or future Python versions. Fix: `n.replace("%", "\\%")` or raw string. Fix owned by `05_paper/latex-build/tests/` — not edited here (outside this task's owned file), recorded as a request for the lane lead.
2. **Test criterion is weaker than ideal (suggestion):** substring `in` allows false passes for short numbers. The independent standalone-occurrence check above passes for the current draft, but a stricter test would use word-boundary regex per number. Non-blocking for this draft.
3. **`inline()` (lines 56–71) is dead code** — superseded by `convert_inline_safe()`; contains its own incomplete escaping. Not on the number path, no impact, but it is a maintenance trap.

None of these affect number preservation on the current `paper.md` → `body.tex` pair.

## §5. Files

- Modified (by the test run itself, expected): `05_paper/latex-build/body.tex` (regenerated, byte-identical, sha256 `99f98b22…`).
- Created by this review: `sessions/R3-7-latex/reports/review-converter.md` (this file).
- No other files created or edited. No installs or downloads.

CARD COMPLETE
