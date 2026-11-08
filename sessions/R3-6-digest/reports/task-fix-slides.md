# Report — Fix slides (Slide 1 AI disclosure + Slide 11 threats)

## Task
Fix Slides: (1) expand Slide 1 AI disclosure to state agents wrote analysis code, ran experiments, drafted sections and performed simulated review (not analysis/code only). (2) Add two missing threats as Slide 11 bullets: gate fitted on 1873 dev items; second-corpus arm is a direction test with different construct. Keep 12 slides, add speaker-note sentences if needed. Run slide/word counts and include in report. Write patch + report only.

Owned: `06_review/PRESENTATION/SLIDES-OUTLINE.md` only. Report: `sessions/R3-6-digest/reports/task-fix-slides.md`. Ground in `05_paper/draft/paper.md` §7 and §6.

## Changes made

### Slide 1 (`06_review/PRESENTATION/SLIDES-OUTLINE.md`, line 11)
- Old subtitle: `Analysis and code: agent-assisted, human-directed (§7).`
- New subtitle: `AI disclosure: agents wrote analysis code, ran experiments, drafted sections and performed simulated review; human-directed (§7).`
- Grounded in `05_paper/draft/paper.md` §7, lines 624-625: "Language-model agents wrote analysis code, ran the experiments, drafted sections and performed the simulated review". Now states all four activities, not only analysis/code.

### Slide 11 — Limitations (bullets + speaker notes)
- New bullet 6: `Gate fitted on 1873 dev items; uncertainty reflects item/article resampling, not corpus-level uncertainty.` — from §6 threat 7 (paper.md lines 609-610: "The gate is fitted on a dev half of 1873 items; intervals reflect item-level and article-level resampling, not corpus-level uncertainty.")
- New bullet 7: `Second-corpus arm is a direction test with a different construct (no article grouping, shorter passages, multi-hop questions); its confirmatory point is degenerate.` — from §6 threat 5 (paper.md lines 606-607) and §4.8 (lines 546-547: "no article grouping, shorter passages, multi-hop and comparison questions"). Previously this was only a speaker-note sentence, not a bullet.
- Speaker notes: added `The gate is fitted on 1873 dev items, so intervals do not capture corpus-level uncertainty.` Wording of existing direction-test note kept (now "not a generality claim" suffix).

No other slides touched. Slide 12 AI-use disclosure already had full wording; left unchanged.

## Counts (re-run after patch)

Verified with Python regex on the file:
- Slide count: 12 (`## Slide 1` … `## Slide 12` all present — unchanged)
- Word count: 2092 (was 2007 before patch; +85 words from the two new bullets + speaker note + expanded Slide 1 subtitle)
- Character count: 13,125
- Lines: 186 (was 182)
- Slide 11 bullets: 8 (was 6)
- Slide 1 subtitle contains all four activities: `agents wrote analysis code, ran experiments, drafted sections and performed simulated review`
- `1873 dev items` present in bullets and speaker notes
- `direction test with a different construct` present in bullets and speaker notes

## Files
- Modified: `06_review/PRESENTATION/SLIDES-OUTLINE.md`
- Created: `sessions/R3-6-digest/reports/task-fix-slides.md` (this report)

## Issues
- None. Grounding confirmed in §7 (AI disclosure) and §6 threats 5 and 7 (1873 dev items / second-corpus direction test).
