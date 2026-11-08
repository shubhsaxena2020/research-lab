# Cross-file consistency check: WALKTHROUGH.md vs SLIDES-OUTLINE.md

Scope: `WALKTHROUGH.md` vs `SLIDES-OUTLINE.md` only. Both cite `05_paper/draft/paper.md` (draft as of 2026-11-08). Line refs below are `W:Ln` (Walkthrough) and `S:Ln` (Slides).

## Overall verdict

The two files agree on every headline number checked (75.50% over-refusal, 24.50% answered, AUROC audit values, gate AUROC 0.982→0.874, R4 12.53%, R5 89.25%, top-1 78.25%/0.945). They disagree on **structure and completeness**: Slides reorders §4.6 before §4.4/§4.5, folds §2 and §5 into two slides, drops the glossary entirely, and trims 2 of 8 threats. No numeric contradiction found.

## 1. Section order

### Agree
- Title → problem/motivation → setup/method → ladder/audit → registered result → hypotheses → exploratory point → controls → limitations → AI disclosure. W treats paper in numeric order (W:L11-L245: Title, Abstract, §1-§9, Glossary, Summary). S treats the same arc in slides 1-12 (S:L7-S:L182). Abdumalikov 98%→1% is the framing observation in both: W:L33, S:L25.
- Separability audit comes before the result in both: W §4.1 before §4.2 (W:L105-L119); S Slide 5 before Slide 6 (S:L65-L89).
- AI disclosure comes last in both: W §7 (W:L217-L224), S Slide 12 (S:L167-L182).

### Disagree
1. **§4.6 vs controls order inverted.** Walkthrough follows paper order §4.4 → §4.5 → §4.6 → §4.7 → §4.8 (W:L129-L167). Slides promote the dense-defect finding to Slide 9 (S:L123-L134) and demote R5/top-1/second-corpus to Slide 10 (S:L138-L147), i.e., §4.6 before §4.4/§4.5/§4.8. Both report the same numbers, but a reader following Slides sees the fix before the controls it sits between in Walkthrough.
2. **§2 Related work nearly missing in Slides.** W has a full §2 (W:L41-L48: abstention surveys, BM25/dense/reranking, arXiv:2207.05221 reader baseline, Table 7). S compresses it to one Abdumalikov bullet on Slide 2 (S:L19-L30); dense/reranking/Table 7 never appear in Slides.
3. **§5 Discussion folded away.** W has §5.1-§5.4 (W:L173-L204). S folds the only Discussion claims into Slide 12 "what I learned" bullets (S:L169-L173); §5.4 future-work items (gold-paragraph presentation, hand-built R4, declared coverage, 40 ungrammatical items) have no slide.
4. **No slide for Abstract, §8 Reproduction, §9 References.** W covers all three (W:L21-L28, W:L227-L244). S has no equivalents; S Slide 1 subtitle is the only front-matter carried over.
5. Walkthrough's one-minute summary (W:L285-L287) quotes AUROC 0.977/0.874/12.53% — consistent with S Slides 5/9. Call this agreement, not disagreement.

## 2. Glossary terms

### Agree
- Slides' point-of-use definitions match Walkthrough's glossary entries: "abstention gate … yes/no filter" (S:L28) ≡ W:L249; "overlap" usage (S:L71, S:L141) ≡ W:L272.

### Disagree
- **Slides has no glossary at all.** Walkthrough defines 34 terms with analogies (W:L247-L282: Abstention gate, Answerable, AUROC, Band, BCa bootstrap, BM25, Bootstrap interval, Coverage, Cross-validation, Cross-encoder, Dense/cosine, Dev/held-out halves, Deviations D1-D4, Exploratory vs confirmatory, Gate AUROC, Gold paragraph, Holm, H1/H2/H3, IDF/content token, Item, Logistic regression, Negative, Operating point, Overlap, Over-refusal, Pooled precision, Precision P(negative|refused), Pre-registration, Recall/refusal rate, Rung/ladder, Separability audit, Single threshold, Top-1 presented). Slides offers only one inline plain-English gloss (S:L28) plus occasional numbers. A presenter using Slides alone has no definition for AUROC, band, BCa, Holm, D1-D4, or refusal rate — terms Slides itself uses on S:L68, S:L82-S:L85, S:L111.
- Walkthrough glossary gives H1/H2/H3 criteria inline (W:L266: ≥15/≥10/≥5 points); Slides repeats them on Slide 7 (S:L96-S:L98) — agree on values, but Slides never labels them "glossary".

## 3. Limitations / threats

### Agree
- "One corpus family, one language, passage-level QA, one feature stack, one gate family" — W:L37, W:L167 vs S:L154. Verbatim.
- Gold-paragraph presentation bias, quantified in §4.5 — W:L209 (item 2 of 8) vs S:L155.
- R2 incomplete 273 dev / 280 held-out, exchangeability p=0.052 — W:L209 (item 3, 280 held-out) vs S:L156 (273/280, p=0.052). Note W places 273 at W:L55 (dev only) and 280 at W:L209; no conflict, just split across sections.
- R4 substitutions automatic, sometimes ungrammatical — W:L209 (item 4) vs S:L157.
- Reader baseline AUROC 0.419 on 553 dev items — W:L155, W:L209 (item 6) vs S:L158.
- Dense block degenerate, both runs reported, no substitute for fresh pre-registered replication — W:L147-L151 vs S:L159.

### Disagree
1. **Two threats missing as Slide bullets.** Walkthrough §6 lists 8 threats (W:L209). Slides Slide 11 lists 6 bullets (S:L153-L159). Dropped: "gate fitted on 1873 dev items" (W:L209 item 7) — no bullet and no speaker note in S:L161-L163; "second-corpus direction test" (W:L209 item 5) appears only in S:L163 speaker notes ("different construct"), not as a bullet.
2. Walkthrough §6 adds "Intervals now cover item and article resampling, not corpus-level uncertainty" (W:L213) — absent from Slides.
3. Walkthrough carries counts as whole corpus/paragraph numbers in §3.1 (W:L55: 35 articles, 1204 paragraphs, 11873 questions, 5928 answerable, 3752 items); Slides Slide 3 carries the same (S:L37-S:L39) — agree. But Walkthrough's total 3752/1879 held-out is repeated in glossary "Item … Total 3752" (W:L268); Slides states it only on Slide 4 (S:L57).

## 4. AI-disclosure wording

### Agree
- Both say the student is the responsible author and agents did the work. W:L13 ("You are the author. Analysis and code were agent-assisted, human-directed"), W:L219 ("AI agents wrote code, ran experiments, drafted sections, and performed simulated review. The student directed the work and holds the author position"), W:L223 ("The student is the responsible author") vs S:L11 ("always: agent-assisted, human-directed (§7)" on title slide), S:L176 ("agents wrote analysis code, ran the experiments, drafted sections and performed a simulated review"), S:L181 ("I am the responsible author; I can explain every section").
- Both label the simulated review a simulation, not a venue decision: W:L223 vs S:L176 ("labelled as a simulation, not a venue decision").
- Both restrict to public data: W:L219 ("Public data only: SQuAD v2.0 dev and a multi-hop corpus dev split. … No private, scraped, or login-walled source") vs S:L178 ("Public data only (SQuAD v2.0 dev, share-alike; multi-hop corpus dev, Apache); no private or scraped data").

### Disagree
1. **Slide 1 narrows the disclosure.** S:L11 says only "Analysis and code: agent-assisted, human-directed" — omits experiments, drafting, and simulated review that W:L219 and S:L176 include. A presenter stopping at Slide 1 understates the agent role relative to both other statements.
2. **Walkthrough-only clauses.** "Disclosure follows the target venue's policy" (W:L223) and the logging record ("Every request logged with URL, status, size, checksum" — W:L219) and the freeze record ("pre-registration hash … code, seeds and raw outputs committed" — W:L223) have no equivalent on Slide 12.
3. **Slides-only clauses.** "expected to explain every section; `06_review/STUDENT-DIGEST-S3.md` and `06_review/CLAIMS-AUDIT.md` exist for that" (S:L177) and per-corpus licenses "share-alike; Apache" (S:L178) have no equivalent in W §7.
4. Wording variant (same meaning): W says "AI agents" (W:L219); S says "Language-model agents" (S:L176).

## 5. The 12.53% finding (dense-defect correction)

### Agree (no contradiction on the headline number)
- Both: frozen held-out AUROC 0.982 → spec-corrected 0.874; dense cosine = 1 on 78.70% of rows because the dense query was the passage itself; R4 refusal collapses to 12.53%. W:L147 ("Dense cosine was exactly 1 on 78.70% of rows … drops held-out AUROC from 0.982 to 0.874. R4 collapses to 12.53%") vs S:L127-S:L129 ("dense cosine = 1 on 78.70% of rows … held-out AUROC 0.982 → 0.874; R4 exploratory refusal 84.71% → 12.53%"). Walkthrough's one-minute summary repeats "AUROC 0.874, R4 at 12.53%" (W:L287).
- Both: report both runs; frozen = registered result; corrected = carry forward. W:L151 ("We did not refit the registered analysis … frozen run is the registered result … Both runs are in Table 4 … corrected numbers are the ones to carry forward") vs S:L134 ("Report both runs; the frozen run is the registered result, the corrected run is the one worth carrying forward").
- Both: R1-R3 stay high after correction. S:L129 gives 99.75/92.86/95.50; W:L123 gives exploratory 99.75/91.07/92.75/84.71 for frozen, and W does not tabulate corrected R1-R3, but W:L151 says H1/H3 stay refuted, consistent with S's "R1-R3 stay in the nineties."
- Both: interpretive conclusion identical — features measure passage-question match, so R4 (perfect match, wrong span) breaks the gate. W:L147-L151 + W:L183 vs S:L130 ("Interpretation: … nothing to work with when the passage matches perfectly and one span is wrong — exactly the failure mode an abstention gate should have").

### Disagree (detail/precision, not the 12.53% value)
1. **Which point is 12.53% at?** S:L128-S:L129 explicitly says "exploratory refusal 84.71% → 12.53%" with R1-R3 at the exploratory point. W:L147-L151 says only "R4 collapses to 12.53%" without labelling the operating point in that section; W's §4.6 header context and its §4.3 exploratory numbers (W:L123) imply exploratory, but W never says "exploratory" for the corrected run, risking confusion with the confirmatory 100% refusal (W:L115).
2. **Corrected H3 value.** W:L147 adds "H3 is now -2.23%" for the corrected run; Slides never gives the corrected H3 (S:L128-S:L129 covers AUROC and R4 only).
3. **Provenance labels.** W calls the corrected run "D4, a declared sensitivity analysis … Both runs are in Table 4" (W:L151) and warns "No fresh pre-registered replication is claimed" (W:L151). S:L128-S:L134 does not mention D4, Table 4, or the no-replication caveat in the Slide 9 bullets (it appears only in Slide 11 bullet 6, S:L159).
4. W adds mechanism detail absent from Slides: "ten informative columns, not twelve" (W:L147); S says only "dense block degenerate" (S:L127).

## 6. Other numeric checks (all agree)

- Registered rule "maximise recall subject to dev precision 0.80" and band [0.9072, 0.9478], width 0.0406, single 0.9394, dev admit mass 6.03%, 92.95% refused by lower threshold: W:L71-L75 vs S:L41, S:L85. Agree.
- Band refusal 100.00/99.64/100.00/100.00, over-refusal 75.50%, answered 24.50%, pooled precision 83.03%, R1 precision 56.98%, R2 48.02%: W:L115, W:L175 vs S:L82-S:L84, S:L100. Agree.
- H1 0.00% CI [0.00%,0.00%], H3 0.00%, H2 loss 0.07%: W:L27, W:L115 vs S:L96-S:L98. Agree.
- Audit AUROC R1-R4 0.506/0.539/0.488/0.415; +overlap 0.977/0.889/0.923/0.408; R5 0.721 (surface) / 0.794 (+overlap): W:L27, W:L107, W:L83 vs S:L69-S:L70. Agree.
- Exploratory: over-refusal 9.50%, coverage 25.44%, refusal 99.75/91.07/92.75/84.71, R1-R3 7.00% CI [4.50%,9.75%]: W:L123 vs S:L112-S:L114. Agree.
- R5 refused 89.25%, MAD 10.29% vs 42.08%: W:L131 vs S:L141. Agree. Top-1: hit 78.25%, AUROC 0.945, refuses 63.22%/2.56%, P(miss|refused)=87.30%: W:L139 vs S:L142. Agree. Second corpus AUROC 0.640, over-refusal 89.50%: W:L163 vs S:L143. Agree.

## Bottom line

No factual conflicts on numbers. Disagreements are presentation-level: Slides reorders §4.6 ahead of §4.4/§4.5, deletes the glossary and two threats, narrows the title-slide AI disclosure, and omits the corrected H3 (-2.23%), D4 label, and Table 4 pointer. Highest-risk item is (1) the Slide 1-only disclosure scope and (2) W §4.6's unlabelled 12.53% operating point, since Slides correctly labels it "exploratory."
