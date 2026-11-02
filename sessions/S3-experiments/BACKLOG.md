# BACKLOG S3-experiments

Tick only what has been verified by running it (RULES #14). Evidence line under each item.

## Phase 1 — topic-independent tooling

- [x] **S3-1** `tools/verify_citations.py` — DOI (Crossref→DataCite) / arXiv / OpenAlex /
      Semantic Scholar resolution, fuzzy title+author+year check, VERIFIED / MISMATCH /
      NOT_FOUND / ERROR, cache, polite limits, CSV+BibTeX input, 3 report formats.
      *Evidence:* `pytest tools/tests -q` → 37 passed; live run on `tools/tests/live_sample.csv`
      → 5/5 real papers VERIFIED, the fabricated row NOT_FOUND (best match 0.50 < 0.55).

- [x] **S3-2** `tools/check_numbers.py` — every number in a draft traced to
      `04_experiments/RESULTS-INDEX.json` via `num:` markers, narrow exemptions, percentage
      and rounding tolerance, UNTRACEABLE / MISMATCH / DANGLING_MARKER.
      *Evidence:* 46 passed; clean toy draft 0 findings, tampered digit → MISMATCH exit 1.

- [x] **S3-3** `05_paper/template/` — article skeleton, IEEE + ACL stubs, refs.bib with zero
      active entries, `citations_to_bib.py`, Markdown skeleton, figure/table generators that
      read only from results files, `build.sh` + `BUILD.md`.
      *Evidence:* 30 passed; both generators run end to end; toy summary is refused (exit 2).

- [x] **S3-4** `04_experiments/harness/` — runner with provenance (git hash, dirty flag,
      config sha256, timing, peak RSS), heavy lock, aggregator, stats (bootstrap/BCa,
      exact Wilcoxon, sign test, Cohen's d, Cliff's delta, Holm, BH), ablation tables, toy
      experiment, `--check-repro`.
      *Evidence:* 72 passed; exact Wilcoxon n=6 → 0.03125 cross-checked against scipy;
      `--check-repro` passes on deterministic fn and fails on noisy fn.

- [x] **S3-5** `06_review/PEER-REVIEW-SIM.md` + `tools/simulate_review.py` + six personas +
      meta-review template. Honest about not calling an LLM.
      *Evidence:* 9 passed; round 1 → 3 reviews → aggregate ranked the shared must-fix at
      rank 1 (3 reviewers) → round 2 → `compare` shows it resolved, 2 persisted.

- [x] **S3-6** `06_review/ORIGINALITY.md` + `tools/originality_check.py` +
      `06_review/templates/AI-DISCLOSURE.md`.
      *Evidence:* 27 passed; a planted 21-word verbatim run caught as UNQUOTED, exit 1;
      quoted variant exits 0. Disclosure table reconciled with
      `00_foundations/ETHICS-AND-AI-USE.md` (S1) — our NeurIPS row was wrong and is fixed.

- [x] **S3-7** `06_review/CLAIMS-AUDIT-TEMPLATE.md` + `tools/claims_audit.py`.
      *Evidence:* 16 passed; toy audit PASSes; missing file / wrong value / verified=NO /
      uncovered claim / unjustified "state of the art" each fail with a named row.
      *Bug found and fixed by the lead:* `"gain"` matched inside `"against"`, making every
      comparison sentence an UNCOVERED claim; now word-prefix matched, with regression tests.

- [x] **S3-8** `tools/make_digest.py` + `06_review/STUDENT-DIGEST/README.md`.
      *Evidence:* 11 passed; digests resolve numbers and citation keys from evidence files and
      emit `[TO FILL]` instead of inventing; `--check` passes on a generated digest.

- [x] **Toy pipeline dry run** `04_experiments/toy/run_pipeline.py`.
      *Evidence:* `12/12 steps behaved as expected` — run → aggregate → repro → table refusal
      → figure → numbers pass → numbers tamper caught → claims → digest → digest check →
      review pack → originality.

## Phase 2 — LOCKED

- [ ] **S3-9** `04_experiments/PROTOCOL.md` pre-registration, frozen with a hash.
      Blocked: `orchestration/HEAD-REVIEW.md` contains no `TOPIC APPROVED` line and
      `03_topics/SELECTED.md` does not exist. Not started, by design.

## Not done / open

- No LaTeX installed here, so no template was compiled to PDF. Stubs are brace/environment
  checked only; layout is unverified. Recorded in `05_paper/template/BUILD.md`.
- `02_literature/sources/` has no PDFs yet, so the originality gate cannot pass on a real
  draft until sources are deposited (the tool itself is proven).
- Nothing committed to git: S1/S2 are writing in the same working tree right now, and a commit
  would capture their in-flight work. `meta.json` records `git_dirty: true` honestly.
- `02_literature/verified_citations.csv` holds 5 real, API-verified entries (Vaswani 2017,
  He 2016, Devlin 2019, Kingma 2015, LeCun 2015) with URLs and retrieval timestamps. They are
  usable in a draft; anything else must be verified before it is added.
