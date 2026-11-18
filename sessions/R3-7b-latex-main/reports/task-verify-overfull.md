# Task verify-overfull — verification report

Date: 2026-11-18 (main laptop, profile res-s1)
Scope: overfull-box fix + wording preservation for R3-7b LaTeX build.

## Check 1 — preamble settings (paper-acl.tex, paper-article.tex)

PASS. Both files contain:
- `\setlength{\emergencystretch}{5em}`
- `\tolerance=5000`

Evidence:
- `paper-acl.tex:11` / `paper-acl.tex:12`
- `paper-article.tex:11` / `paper-article.tex:12`
- git diff vs HEAD confirms only `3em`→`5em` and `2000`→`5000` changed (no other preamble edits).

## Check 2 — build logs contain no "Overfull"

PASS. Case-insensitive grep count = 0 in both logs:
- `05_paper/latex-build/paper-acl.log`: 0
- `05_paper/latex-build/paper-article.log`: 0

## Check 3 — git diff shows no changes to 05_paper/draft/paper.md

FAIL (as of current working tree). `git diff --stat -- 05_paper/draft/paper.md` reports:
- `05_paper/draft/paper.md | 13 +++++++------` (7 insertions, 6 deletions)

Diff content (unrelated to overfull fix; appears to be R3-4b content updates):
- pre-registration hash count: 3 → 6; deviations D1–D3 → D1–D6
- environment pinning note replaced ("no lockfile" paragraph → `requirements-lock.txt` / `ENVIRONMENT.md`)

The overfull fix itself touched only `paper-acl.tex` and `paper-article.tex` (4 lines total); it did not edit `paper.md`. Wording preservation for the overfull fix therefore holds at the fix level, but the working tree's `paper.md` is not byte-identical to HEAD.

## Supporting checks
- `python 05_paper/latex-build/tests/test_md2tex.py`: PASS — 317 numbers preserved.
- BUILD-REPORT.md states "No text in paper.md was changed" for the overfull fix; consistent with Check 1/2 but contradicted by the current working-tree diff in Check 3 (see note above).

## Verdict
- Overfull-box fix (tex preambles): VERIFIED.
- Build logs (no Overfull): VERIFIED.
- Wording preservation of paper.md vs HEAD: NOT VERIFIED in current tree (paper.md modified by other work).
