# verify-schema — R3-5 related-work validation

Generated: 2026-11-08 (local check)

## Inputs
- `02_literature/related-work-r3/table7.json`
- `02_literature/related-work-r3/NOVELTY-R3.md`
- `sessions/R3-5-related-work/ANSWERS.md`

## Checks

| # | Check | Result | Detail |
|---|-------|--------|--------|
| 1 | JSON parses | PASS | `json.load` succeeded, no error |
| 2 | Has `rows` array | PASS | top-level key `rows` is a list |
| 3 | >=7 rows excluding this paper (total >=8) | PASS | 12 total rows; 11 excluding "This paper (C1 audit)" |
| 4 | Every row has required keys (work,id,data,metric,negatives,operating_point,both_directions,source_quotes) | PASS | all 12 rows complete; no missing keys |
| 5 | Every `source_quotes` has 7 keys | FAIL | row 0 "This paper (C1 audit)" has 6 keys (missing `id`); other 11 rows have 7 |
| 6 | NOVELTY-R3.md has >=15 query rows in its table | PASS | 18 numbered query rows in section 2 table |
| 7 | ANSWERS.md exists | PASS | `sessions/R3-5-related-work/ANSWERS.md` present |
| 8 | ANSWERS.md mentions MF-23 | PASS | found |
| 9 | ANSWERS.md mentions MF-28 | PASS | found |

## Summary
- 8 of 9 checks PASS.
- 1 check FAILS: `table7.json` row 0 (`This paper (C1 audit)`) `source_quotes` has 6 keys instead of 7 (missing `id`).
- Recommended fix: add an `id` entry to that row's `source_quotes` (e.g. pointing to the draft title page), then re-run this validation.

Overall: FAIL (schema not fully satisfied until the missing `id` source_quote is added).