# BACKLOG S3-experiments

Tick only what has been verified by running it (RULES #14). Evidence under each item.

## Phase 1 — topic-independent tooling

- [x] **S3-1** `tools/verify_citations.py` — DOI (Crossref → DataCite) / arXiv / OpenAlex /
      Semantic Scholar resolution, fuzzy title+author+year check, VERIFIED / MISMATCH /
      NOT_FOUND / ERROR, cache, polite limits, CSV+BibTeX input, one canonical output schema.
      *Evidence:* 79 tests; live run 5/5 real papers VERIFIED, fabricated row NOT_FOUND.
- [x] **S3-2** `tools/check_numbers.py` — every draft number traced through `num:` markers to
      `RESULTS-INDEX.json`; UNTRACEABLE / MISMATCH / DANGLING_MARKER; narrow visible exemptions.
      *Evidence:* 88 tests; clean toy draft 0 findings, tampered digit → MISMATCH exit 1.
- [x] **S3-3** `05_paper/template/` — article + IEEE + ACL stubs, refs.bib with zero active
      entries, `citations_to_bib.py`, Markdown skeleton, figure/table generators, build docs.
      *Evidence:* 30 tests; generators run end-to-end; toy summary refused (exit 2);
      **270 verified rows → 270 BibTeX entries** from the real register.
- [x] **S3-4** `04_experiments/harness/` — runner with provenance, heavy lock, aggregator,
      bootstrap/BCa, exact Wilcoxon, sign test, effect sizes, Holm/BH, ablation tables, toy
      experiment, `--check-repro`.
      *Evidence:* 72 tests; exact Wilcoxon n=6 = 0.03125 cross-checked against scipy.
- [x] **S3-5** `06_review/PEER-REVIEW-SIM.md` + six personas + `tools/simulate_review.py` +
      meta-review template. Orchestrator only — it never pretends to be an LLM.
      *Evidence:* 9 tests; round1 → aggregate ranks the shared must-fix #1 → round2 → `compare`
      shows it resolved.
- [x] **S3-6** `06_review/ORIGINALITY.md` + `tools/originality_check.py` +
      `06_review/templates/AI-DISCLOSURE.md` (reconciled with S1's verified policy quotes).
      *Evidence:* 27 tests; planted 21-word copy caught, quoted copy passes.
- [x] **S3-7** `06_review/CLAIMS-AUDIT-TEMPLATE.md` + `tools/claims_audit.py`.
      *Evidence:* 16 tests; five failure modes each fail with a named row.
- [x] **S3-8** `tools/make_digest.py` + `06_review/STUDENT-DIGEST/README.md`.
      *Evidence:* 11 tests; gaps emitted as `[TO FILL]`, never invented.

## Cross-cutting (added this session)

- [x] **One canonical citation schema** `tools/lib/citation_schema.py`; S2 owns the register,
      S3 writes the same columns. *Evidence:* 270/270 rows load and convert.
- [x] **One-command proof** `tools/check_all.py` + `ops/check.sh`. *Evidence:* 4/4 steps, 44 s.
- [x] **Toy pipeline** `04_experiments/toy/run_pipeline.py`. *Evidence:* 12/12 steps.
- [x] **Protocol checklist** `04_experiments/PROTOCOL-CHECKLIST.md` (topic-agnostic, ready for
      S3-9 the moment Phase 2 unlocks).
- [x] **Docs-drift tests** `tools/tests/test_docs_and_cli.py` — every `--help`, exit code 2 on
      bad usage, documented paths exist, toy rules stated, and the Phase-2 gate asserted by
      exact line match.
- [x] **Adversarial suites** `test_check_numbers_adversarial.py`, `test_verify_citations_adversarial.py`
      — 8 real bugs found, all fixed, all guarded without xfail.

## Phase 2 — LOCKED

- [ ] **S3-9** `04_experiments/PROTOCOL.md` pre-registration, frozen with a hash.
      Blocked: no standalone `TOPIC APPROVED` line in `orchestration/HEAD-REVIEW.md` (line 10
      only *describes* the line the head will write), and `03_topics/` is empty. Not started.

## Not done / open

- No LaTeX installed → no template compiled; layout unverified.
- `02_literature/sources/` empty → originality gate not run on a real draft.
- `05_paper/draft/` empty → no real section through the gates yet.
- `simulate_review.py` has no `--json` (documented; the README claim is scoped accordingly).
- `aggregate.py` writes `summary_<experiment>.json` but does not copy per-run `results.json`
  into `04_experiments/results/`, although CONTRACTS §3 reads as if it does. Left as a
  documented discrepancy rather than changed silently.
- Nothing committed: S1/S2 write in the same tree; a commit would capture their in-flight work.
