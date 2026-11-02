# STATUS S3-experiments

last_update: 2026-11-03T02:55+05:30
state: **PHASE 1 COMPLETE AND VERIFIED.** PHASE 2 LOCKED.

## Re-verified from disk after the gateway disconnect (2026-11-03T02:55+05:30)

Nothing was lost, and nothing is taken on trust from my own earlier report — the commands
below were re-run just now, in this session, against the files on disk:

    python -m pytest tools/tests 04_experiments/harness/tests 05_paper/template/tests -q
    -> 250 passed in 79.60s      (exit 0)

    python 04_experiments/toy/run_pipeline.py
    -> 12/12 steps behaved as expected   (exit 0)

### Phase 2 gate — read carefully, this is a trap for a careless `grep`

`grep "TOPIC APPROVED" orchestration/HEAD-REVIEW.md` returns **one hit, and it is not an
approval**. It is line 10, the standing-decisions sentence describing what the head *will*
write: "the head reads them, then writes `TOPIC APPROVED` (or a veto) here". The file's own
header still says "Phase 2 (experiments) stays LOCKED. This file does not yet contain the
approval line." `03_topics/` is empty — no `SELECTED.md`, no `NOVELTY-CHECK.md`.
**Verdict: LOCKED. No topic-specific work was done, and none was invented to fill time.**

## Inventory on disk (checked by listing, not by memory)

```
tools/            verify_citations.py  check_numbers.py  claims_audit.py
                  originality_check.py  simulate_review.py  make_digest.py
                  lib/{netcache,matchlib,bibtex_min}.py  tests/  CONTRACTS.md  README.md
04_experiments/harness/  runner.py  lock.py  aggregate.py  stats.py  tables.py
                  configs/  tests/  README.md
05_paper/template/       main.tex  refs.bib  build.sh  BUILD.md  README.md
                  ieee/  acl/  md/  figures/  tables/  tools/  tests/
```

## Delivered (S3-1 .. S3-8), each with the test that proves it

| Item | Path | Proof (re-run 02:55) |
|---|---|---|
| S3-1 citation verifier | `tools/verify_citations.py`, `tools/lib/*` | 39 tests; live run: 5 real papers VERIFIED, 1 fabricated NOT_FOUND |
| S3-2 number tracer | `tools/check_numbers.py` | 46 tests; clean draft 0 findings, tampered digit -> MISMATCH exit 1 |
| S3-3 paper template | `05_paper/template/` | 30 tests; figures+tables generated from results files only |
| S3-4 experiment harness | `04_experiments/harness/` | 72 tests; exact Wilcoxon/BCa cross-checked against scipy; `--check-repro` |
| S3-5 peer-review sim | `06_review/PEER-REVIEW-SIM.md`, `tools/simulate_review.py`, `personas/` | 9 tests; round1->round2 `compare` marks a fixed item resolved |
| S3-6 originality + AI disclosure | `06_review/ORIGINALITY.md`, `tools/originality_check.py`, `templates/AI-DISCLOSURE.md` | 27 tests; planted 21-word copy caught |
| S3-7 claims audit | `06_review/CLAIMS-AUDIT-TEMPLATE.md`, `tools/claims_audit.py` | 16 tests; 5 failure modes each named |
| S3-8 student digest | `tools/make_digest.py`, `06_review/STUDENT-DIGEST/` | 11 tests; gaps emitted as `[TO FILL]`, never invented |
| extra | `04_experiments/PROTOCOL-CHECKLIST.md` | topic-agnostic pre-registration checklist, ready for S3-9 |

## Response to Codex DIRECTIVES

1. *"finish Phase 1 interfaces and run bounded unit checks only; record commands and outcomes
   in S3 status"* — done; commands and results are above and in `BACKLOG.md`.
2. *"align citation and number-check contracts with S2's canonical register"* — done:
   `verify_citations.py` reads S2's staging schema directly
   (`id,title,authors,year,venue,url,doi_or_arxiv,retrieved_on,...`), classifying the single
   mixed `doi_or_arxiv` column by shape, UTF-8 BOM tolerated, 2 regression tests.
   **Live check on 3 real rows of `02_literature/staging/S2-2-verified.csv`: 3/3 VERIFIED**
   (MemGPT, Mem0, A-MEM) — the head's random-20 re-resolution is one command. Canonical output
   schema remains `tools/CONTRACTS.md §1`; `tools/README.md` names the source of truth.
3. *"prepare a topic-agnostic protocol checklist and paper/review handoff"* — done:
   `04_experiments/PROTOCOL-CHECKLIST.md` plus the handoff in `06_review/PEER-REVIEW-SIM.md`
   and `templates/META-REVIEW.md`.
4. *"label numbers-audit.md as a fixture audit"* — done: default output is
   `06_review/audits/numbers-audit.md`, and every report opens with an explicit scope line
   ("NOT a paper draft ... a PASS here says the tool works, NOT that any draft passed").
   Every `RESULTS-INDEX.json` entry is toy-marked.
5. *"replace the template's AI/data provenance assurance with a TODO"* — done in
   `05_paper/template/main.tex`; the three reassurance sentences are a
   `TODO(verify at drafting time)`.

## Environment facts (carry forward)

- `pandas`, `matplotlib`, `scikit-learn`, `scipy`, `bibtexparser` are **not** installed;
  everything degrades gracefully (`NEEDS_DEPS.md`).
- OpenAlex and Semantic Scholar answer `429` from this network (`Retry-After: 15859`);
  Crossref, arXiv, DataCite are healthy. Title search order is Crossref -> OpenAlex -> S2, and
  an exhausted host is skipped for the whole run instead of sleeping 30/60/120 s.
- `git_dirty: true` in every `meta.json` is honest: S1 and S2 write in the same working tree,
  so **nothing was committed** — a commit would capture their in-flight work.

## Bugs found by verification (why the tests are not decorative)

- `claims_audit.py`: the comparative-stem check matched `"gain"` inside `"against"`, making
  every comparison sentence an UNCOVERED claim. Fixed to word-prefix matching + regression tests.
- `verify_citations.py`: arXiv DOIs (`10.48550/arXiv.*`) were sent to Crossref, which 404s them
  (arXiv registers with DataCite). Now routed to arXiv/DataCite, test asserts Crossref is not called.
- `matchlib.py`: Jaccard-only author matching failed a correct first-author-only citation.
  Now max(recall, Jaccard) plus a given-name-initial check on the first author.
- `06_review/templates/AI-DISCLOSURE.md`: our NeurIPS row over-stated the requirement; S1's
  verified `00_foundations/ETHICS-AND-AI-USE.md` corrected it.

## Honest gaps

- No LaTeX installed: no template has ever been compiled. Brace/environment checks only.
- `02_literature/sources/` is empty, so the originality gate has not run on a real draft.
- `05_paper/draft/` is empty; no real section has been through the numbers/claims/digest/review
  tools yet. The toy draft is the only end-to-end evidence.
- `02_literature/verified_citations.csv` holds 5 real API-verified entries, usable but not yet
  a bibliography for any paper.

## Next session, in order

1. Re-read `orchestration/HEAD-REVIEW.md`; only a *standalone* `TOPIC APPROVED` line unlocks
   Phase 2 (ignore the mention inside the standing-decisions paragraph). Then turn
   `PROTOCOL-CHECKLIST.md` into `04_experiments/PROTOCOL.md` and freeze its hash.
2. Deposit source PDFs into `02_literature/sources/`, convert with `pdftotext -layout`
   (installed) so `originality_check.py` has a corpus.
3. When real numbers exist, point `run_pipeline.py`'s guards at the real draft — the same
   twelve checks then apply to the paper.
