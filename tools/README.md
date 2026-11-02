# tools/ — the integrity toolchain

Every number and every citation in the paper passes through one of these tools. They are
deliberately boring: standard library only, offline by default, exit code 0 = pass / 1 =
findings / 2 = usage error. `--json` is available on the six paper tools
(`verify_citations`, `check_numbers`, `claims_audit`, `originality_check`, `make_digest`,
`check_all`); `simulate_review.py` is a subcommand dispatcher and reports in Markdown/YAML
instead, so check `--help` rather than assuming a flag.

Run the whole thing in one command to see it work:

    python 04_experiments/toy/run_pipeline.py

| Tool | Answers the question | Run |
|---|---|---|
| `verify_citations.py` | Does this citation actually exist, and is it the paper I say it is? | `--csv 02_literature/citations.csv --online` |
| `check_numbers.py` | Can every number in the draft be traced to a results file? | `--draft 05_paper/draft/` |
| `claims_audit.py` | Is every abstract/intro claim bound to evidence that exists? | `--audit 06_review/CLAIMS-AUDIT.md --draft 05_paper/draft/ ...` |
| `originality_check.py` | Did any 8-word run get copied from a source without quotes? | `--draft ... --corpus 02_literature/sources_text/` |
| `simulate_review.py` | What will six hostile reviewers attack, and was it fixed in round 2? | `pack` → fill → `ingest` → `aggregate` → `compare` |
| `make_digest.py` | Can Shubh explain this section out loud, and where is the evidence? | `--section 05_paper/draft/method.md` |

Supporting modules (import them, do not run them):

- `lib/netcache.py` — polite HTTP: 1 request/second/host, descriptive User-Agent, Retry-After
  honoured, exponential backoff, disk cache in `01_psit_data/raw/cache/`, and a hard stop on a
  host that tells us to go away for hours (OpenAlex does this when an IP's credit is spent).
- `lib/matchlib.py` — fuzzy title/author/year comparison. Title = min(difflib, token-F1) so
  word-order shuffles cannot pass; authors = max(recall, Jaccard) so citing only the first
  author is not punished.
- `lib/bibtex_min.py` — BibTeX reader, no `bibtexparser` needed.

## The rule these tools implement

RULES.md #1 and #2 are not style preferences:

- A citation that is not `VERIFIED` in `02_literature/verified_citations.csv` may not appear
  in a draft. `MISMATCH`, `NOT_FOUND` and `ERROR` all mean "drop it". `ERROR` (a network
  failure) is **not** a pass — that is the failure mode that produces hallucinated
  bibliographies, so the tool refuses to treat it as absence *or* as success.
- A number that is not traceable through `04_experiments/RESULTS-INDEX.json` may not appear
  in a draft, and may not be exempted to make the audit pass. Exemptions live in
  `04_experiments/config/exempt_numbers.json` and are printed in every report, so an
  exemption is a visible decision, not a hidden hole.

## Adding a number to a draft

1. Produce it in a run: `python 04_experiments/harness/aggregate.py --experiment <name>`.
2. Find its id in `04_experiments/RESULTS-INDEX.json`.
3. Write it with a marker: Markdown `<!-- num:id -->0.812<!-- /num -->`, LaTeX a
   `% num:id` comment on the line above.
4. Run `python tools/check_numbers.py --draft <file>`.

Protocol constants (learning rate, epochs, sample size) get an index entry pointing at the
**config file** that produced them — e.g. `{"id": "toy.protocol.lr",
"file": "04_experiments/harness/configs/toy_ours.json", "key": "lr"}` — so they are traceable
to committed evidence instead of being exempted. `aggregate.py` preserves such manually added
entries when it refreshes the index (verified in the toy pipeline).

## Known limits, stated so nobody over-trusts them

- `verify_citations.py` judges *metadata*, not scientific quality. A paper can be real and
  worthless; that is what `simulate_review.py` and the novelty check are for.
- Title search is a heuristic: at `min_title=0.90` a genuinely different paper with the same
  title still passes. Always read the resolved title in the report.
- `check_numbers.py` proves provenance, not correctness. A number can be faithfully copied
  from the wrong run — that is why the index entry carries a `run_id`.
- `originality_check.py` only knows the corpus you give it. Zero findings means "nothing
  copied from the sources I had", not "original".
