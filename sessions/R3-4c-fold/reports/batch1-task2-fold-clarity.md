# R3-4c fold clarity report

## Changed lines (05_paper/template/draft_template.md)
- 05_paper/template/draft_template.md:17
- 05_paper/template/draft_template.md:33-36
- 05_paper/template/draft_template.md:39-40
- 05_paper/template/draft_template.md:43
- 05_paper/template/draft_template.md:50
- 05_paper/template/draft_template.md:175
- 05_paper/template/draft_template.md:214
- 05_paper/template/draft_template.md:275
- 05_paper/template/draft_template.md:358

## Commands and outputs
Command: `python 05_paper/build_draft.py`
Output:
```
wrote 05_paper/draft/paper.md from 7 tables (T7_prior_work, T3_audit, T1_per_rung, T2_hypotheses, T5_arms, T4_frozen_vs_corrected, T6_ablations_corrected); 60295 bytes; sha256 89e92e7990a4
```

Command: `python tools/check_numbers.py --draft 05_paper/draft/paper.md`
Output:
```
505 number(s) in 1 file(s): 318 matched, 187 exempt, 0 finding(s)
report -> C:\Users\shubh\research-lab\06_review\audits\numbers-audit.md
PASS — every number is accounted for
```
