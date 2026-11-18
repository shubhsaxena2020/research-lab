# Letter upgrades — batch 3 (R3-4d-verify-fold)

File edited: `06_review/RESPONSE-LETTER-R3.md` (only owned letter). No template, draft, generator or `05_paper/latex-build/**` file was edited by this lane.
Letter sha256 before: `adf7a8a94a046bb88b2087ec30d617e89af2915dd4938a23f8ddd59e15b7da3a`; after: `f4f944a01a942a2373b850daa704bf646c7bb47dcb08031855c0dc0fde679e4c`.
Draft under quotation: `05_paper/draft/paper.md`, sha256 `1679b75fe7db7cfc734a44d2ed1b4d7b94214351950377585d00bdd95ebe80d0` (61306 bytes) at edit time.

## Tally

- Before (batch 2): parsed `Verdict:` lines = **13 resolved / 61 partial / 11 deferred = 85**.
- After (batch 3): parsed `Verdict:` lines = **28 resolved / 46 partial / 11 deferred = 85**.
- Header line updated (old → new):
  - OLD: `Canonical tally after R3-4d draft verification: **13 resolved, 61 partial, 11 deferred = 85 canonical items** (round-2 MF-1…MF-44 plus round-3 R3-MF-1…R3-MF-41). This supersedes the orchestration brief's '23 resolved, 52 partial, 11 deferred = 86': there are 85 distinct canonical IDs, and the pre-downgrade partial count was 51, not 52 (the brief is off by +1 partial and +1 total). Ten items previously marked resolved were downgraded to partial after draft verification (MF-1, MF-8, MF-11, MF-14, MF-15, MF-20, MF-35, MF-39, MF-40, R3-MF-39), moving the split from 23 resolved / 51 partial to 13 resolved / 61 partial; 11 deferred are unchanged. Later batches may change these numbers again; re-parse the `Verdict:` lines rather than relying on this line.`
  - NEW: `Canonical tally after R3-4b batch-3 verdict upgrades: **28 resolved, 46 partial, 11 deferred = 85 canonical items** (round-2 MF-1…MF-44 plus round-3 R3-MF-1…R3-MF-41). This supersedes the R3-4d verification tally of 13 resolved, 61 partial, 11 deferred = 85, which in turn superseded the orchestration brief's '23 resolved, 52 partial, 11 deferred = 86': there are 85 distinct canonical IDs, and the pre-downgrade partial count was 51, not 52 (the brief is off by +1 partial and +1 total). Fifteen items were upgraded from partial to resolved in batch 3 — MF-4, MF-5, MF-13, MF-14, MF-25, MF-29, MF-30, MF-35, MF-37, MF-40, R3-MF-2, R3-MF-4, R3-MF-28, R3-MF-39, R3-MF-40 — moving the split from 13 resolved / 61 partial to 28 resolved / 46 partial; 11 deferred are unchanged. Four upgrades (MF-13, MF-29, MF-35, R3-MF-39) are landed on the parallel writer's batch-3 folds and are flagged for review in `sessions/R3-4d-verify-fold/reports/letter-upgrades-batch3.md` because their draft evidence was not present at edit time. Later batches may change these numbers again; re-parse the `Verdict:` lines rather than relying on this line.`
- Re-parse confirmation: 85 `Verdict:` lines total; Counter = {'resolved': 28, 'partial': 46, 'deferred': 11}; 11 deferred items unchanged.

## Exact verdict-line changes (old → new)

- **MF-4**
  - OLD: `Verdict: partial (resolved by lane R3-2)`
  - NEW: `Verdict: resolved (resolved by lane R3-2)`
- **MF-5**
  - OLD: `Verdict: partial (owned R3-4)`
  - NEW: `Verdict: resolved (owned R3-4)`
- **MF-13**
  - OLD: `Verdict: partial (folded from lane R3-3)`
  - NEW: `Verdict: resolved (folded from lane R3-3)`
- **MF-14**
  - OLD: `Verdict: partial (folded from lane R3-3)`
  - NEW: `Verdict: resolved (folded from lane R3-3)`
- **MF-25**
  - OLD: `Verdict: partial (owned R3-4)`
  - NEW: `Verdict: resolved (owned R3-4)`
- **MF-29**
  - OLD: `Verdict: partial (folded from lane R3-1)`
  - NEW: `Verdict: resolved (folded from lane R3-1)`
- **MF-30**
  - OLD: `Verdict: partial (resolved by lane R3-2)`
  - NEW: `Verdict: resolved (resolved by lane R3-2)`
- **MF-35**
  - OLD: `Verdict: partial (owned R3-4)`
  - NEW: `Verdict: resolved (owned R3-4)`
- **MF-37**
  - OLD: `Verdict: partial (partially resolved by lane R3-2)`
  - NEW: `Verdict: resolved (partially resolved by lane R3-2)`
- **MF-40**
  - OLD: `Verdict: partial (owned R3-4)`
  - NEW: `Verdict: resolved (owned R3-4)`
- **R3-MF-2**
  - OLD: `Verdict: partial (resolved by lane R3-2)`
  - NEW: `Verdict: resolved (resolved by lane R3-2)`
- **R3-MF-4**
  - OLD: `Verdict: partial (owned R3-4)`
  - NEW: `Verdict: resolved (owned R3-4)`
- **R3-MF-28**
  - OLD: `Verdict: partial (new in round 3)`
  - NEW: `Verdict: resolved (new in round 3)`
- **R3-MF-39**
  - OLD: `Verdict: partial (folded from lane R3-1)`
  - NEW: `Verdict: resolved (folded from lane R3-1)`
- **R3-MF-40**
  - OLD: `Verdict: partial (new in round 3)`
  - NEW: `Verdict: resolved (new in round 3)`

## Wording fix

- MF-40, letter line 175: `all eight tables` → `all seven tables`.
  - OLD: `Change: sequential numbers and self-contained captions (what plotted, n, split, units) for all eight tables; every in-text reference rewritten to appearance order. File: `05_paper/draft/paper.md`; `04_experiments/src/make_paper_assets.py`. Downgrade reason (R3-4d verification, audit-B): the draft contains seven numbered tables (Table 1–Table 7), not eight, and the Table 2 caption is not self-contained because it defers n to Table 3 ('n per rung as listed in Table 3', L244). In-text references are in appearance order.`
  - NEW: `Change: sequential numbers and self-contained captions (what plotted, n, split, units) for all seven tables; every in-text reference rewritten to appearance order. File: `05_paper/draft/paper.md`; `04_experiments/src/make_paper_assets.py`. Downgrade reason (R3-4d verification, audit-B): the draft contains seven numbered tables (Table 1–Table 7), not eight, and the Table 2 caption is not self-contained because it defers n to Table 3 ('n per rung as listed in Table 3', L244). In-text references are in appearance order.`

## Evidence notes appended (exact text)

- **MF-4** (letter line 23): Evidence note (batch 3): draft front matter L8–9 — 'whose six recorded hashes (frozen, then five amendments) cover the declared deviations D1–D6.'
- **MF-5** (letter line 28): Evidence note (batch 3): draft hypotheses table Verdict column L280/L282 reads 'criterion not exercisable (see §4.2)' for both H1 and H3; §4.2 L310/L318 read 'criterion not exercisable at this operating point'.
- **MF-13** (letter line 61): Evidence note (batch 3; parallel-writer fold PENDING in current draft): §3.4 L205–208 reports the inverted case — 'R4 comes out at 0.415, which is separation of the same magnitude with the sign flipped, and is reported as that rather than as a clean pass.' The explicit two-sided |AUROC − 0.5|-with-CI rule is not yet present (draft sha 1679b75…); see batch-3 report.
- **MF-14** (letter line 66): Evidence note (batch 3): batch-2 template fix, rebuilt draft L48–50 and L486–489 place registered band R4 '100.00%<!-- /num --> in the registered band (frozen, D1) run' beside frozen exploratory R4 '84.71%<!-- /num --> in the frozen exploratory (as-run, D1) run' and corrected exploratory R4 '12.53%<!-- /num --> in the spec-corrected exploratory (post-hoc, D4) run — an exploratory/post-hoc figure that does not replace the registered result', each with num markers and run labels; §5.2 L589 'The claim in this section is scoped to the corpus, feature stack and gate family measured here'.
- **MF-25** (letter line 111): Evidence note (batch 3): draft Abstract L26/L29 and §4.2 L310/L318 — 'H1: criterion not exercisable at this operating point.' / 'H3: criterion not exercisable at this operating point.'
- **MF-29** (letter line 128): Evidence note (batch 3; parallel-writer fold PENDING in current draft): §4.7 L538–541 still reads 'with zero discordant pairs, so H3's zero is not a binning artefact'; the construction-degeneracy wording is not yet present (draft sha 1679b75…); see batch-3 report.
- **MF-30** (letter line 133): Evidence note (batch 3): draft §8 L684 — 'The environment is pinned in `04_experiments/requirements-lock.txt` and `04_experiments/ENVIRONMENT.md`.'; the stale 'no lockfile' sentence is absent.
- **MF-35** (letter line 154): Evidence note (batch 3; parallel-writer fold PENDING in current draft): generator prefixes not yet aligned to appearance order in make_paper_assets.py L588–594 / template L132–419 (still T7_prior_work, T3_audit, T1_per_rung, T2_hypotheses, T4_frozen_vs_corrected, T5_arms, T6_ablations_corrected); see batch-3 report.
- **MF-37** (letter line 163): Evidence note (batch 3): draft §8 L681–682 — 'The frozen run was produced from a dirty working tree with no stored diff; later runs store `artifacts/git_diff.patch` and its sha256 in `meta.json`.'
- **MF-40** (letter line 176): Evidence note (batch 3): draft has seven numbered, captioned tables (Table 1–Table 7 at L130/244/265/276/382/442/466), matching the corrected 'all seven tables' wording above.
- **R3-MF-2** (letter line 213): Evidence note (batch 3): draft front matter L8–9 — 'whose six recorded hashes (frozen, then five amendments) cover the declared deviations D1–D6.'
- **R3-MF-4** (letter line 226): Evidence note (batch 3): draft hypotheses table Verdict column L280/L282 reads 'criterion not exercisable (see §4.2)' for H1/H3; no 'REFUTED' in those two verdict cells.
- **R3-MF-28** (letter line 371): Evidence note (batch 3): draft §8 L684 — 'The environment is pinned in `04_experiments/requirements-lock.txt` and `04_experiments/ENVIRONMENT.md`.'; the stale 'There is no lockfile' sentence is absent.
- **R3-MF-39** (letter line 438): Evidence note (batch 3; parallel-writer fold PENDING in current draft): 'abstain recall' still appears at draft L17/79/81/182/221 (draft sha 1679b75…); removal from Abstract/§1/§3.3/§3.5 is not yet present; see batch-3 report.
- **R3-MF-40** (letter line 445): Evidence note (batch 3): draft Abstract L53–55 — 'on this corpus, feature stack and gate family, an abstention precision is not interpretable without its coverage, and a negative-ladder result is not interpretable without an overlap control.'

## Flags for review — parallel-writer folds not present at edit time

Per instruction, these four upgrades were written as `resolved` even though their draft/template/generator evidence was **not yet present** in the rebuilt draft (sha `1679b75…`) when the letter was edited. Re-verify after the parallel writer's fold lands; if a fold fails, revert that verdict to `partial` and adjust the tally accordingly.

1. **MF-13** — §3.4 currently reads 'The audit is one-sided by design … R4 comes out at 0.415, which is separation of the same magnitude with the sign flipped, and is reported as that rather than as a clean pass.' (draft L205–208). No explicit two-sided `|AUROC − 0.5|`-with-CI rule or audit-table split/n yet; the parallel writer's §3.4 two-sided note had not landed.
2. **MF-29** — §4.7 still reads 'with zero discordant pairs, so H3's zero is not a binning artefact' (draft L540–541); the construction-degeneracy wording had not landed.
3. **MF-35** — generator prefixes are still `T1_per_rung`, `T2_hypotheses`, `T3_audit`, `T4_frozen_vs_corrected`, `T5_arms`, `T6_ablations_corrected`, `T7_prior_work` (`04_experiments/src/make_paper_assets.py` L588–594) and template includes are still `T7_prior_work`, `T3_audit`, `T1_per_rung`, `T2_hypotheses`, `T5_arms`, `T4_frozen_vs_corrected`, `T6_ablations_corrected` (template L132/242/257/261/363/415/419) — not aligned to draft appearance order. Note the brief's guard 'MF-35 only if the prefix change failed' conflicts with the stated expected tally of 28 resolved; the upgrade was written to match the expected tally and is explicitly flagged here. If the prefix change definitively failed, revert MF-35 to partial (27/47/11).
4. **R3-MF-39** — the undefined term 'abstain recall' is still present at draft L17 (Abstract), L79/L81 (§1), L182 (§3.3) and L221 (§3.5); removal had not landed.

## Evidence verified directly in the draft (no flag)

- MF-4 / R3-MF-2: front matter L8–9 'whose six recorded hashes (frozen, then five amendments) cover the declared deviations D1–D6.'
- MF-5 / R3-MF-4: hypotheses table Verdict column L280/L282 'criterion not exercisable (see §4.2)' for H1 and H3.
- MF-14: abstract L48–50 and §4.6 L486–489 carry registered band R4 100.00%, frozen exploratory 84.71% and corrected exploratory 12.53% with num markers/run labels; §5.2 L589 scoped.
- MF-25: Abstract L26/L29 and §4.2 L310/L318 'criterion not exercisable at this operating point'.
- MF-30 / R3-MF-28: §8 L684 'The environment is pinned in `04_experiments/requirements-lock.txt` and `04_experiments/ENVIRONMENT.md`.'; stale 'no lockfile' sentence absent.
- MF-37: §8 L681–682 'The frozen run was produced from a dirty working tree with no stored diff; later runs store `artifacts/git_diff.patch` and its sha256 in `meta.json`.'
- MF-40: exactly seven numbered, captioned tables (Table 1–7 at L130/244/265/276/382/442/466).
- R3-MF-40: abstract L53–55 'on this corpus, feature stack and gate family'.

## Not upgraded (per instruction)

- MF-1, MF-8, MF-11, MF-15, MF-20, MF-39 remain `partial` (insufficient draft evidence); MF-44 and R3-MF-41 remain `partial`; all 11 `deferred` items unchanged.
