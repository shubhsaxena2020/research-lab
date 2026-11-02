# `05_paper/template/` — venue-agnostic paper skeleton

Everything here is a **skeleton**, not a submission. It compiles (with a TeX
install), it is wired so that numbers and citations cannot be typed by hand, and
it says TODO wherever a human has to think. Nothing in this directory is a
result: figures and tables are generated from `04_experiments/` files only.

## What is here

| Path | What it is |
|---|---|
| `main.tex` | `article`-class paper: title, AI-disclosure footnote, abstract, all required sections, booktabs table + figure wired to generated files, `\label`/`\ref` cross-references, bibliography. |
| `ieee/main.tex` | Minimal IEEE-style stub (`IEEEtran`, two columns), same section skeleton. |
| `acl/main.tex` | Minimal ACL / NeurIPS-workshop stub (`article` + natbib), same skeleton, with the exact two-line switch to the official style package. |
| `refs.bib` | **Zero active entries.** Header states the only legal source (verified citations); three commented example entries. |
| `tools/citations_to_bib.py` | `verified_citations.csv` → BibTeX, keeping only `VERIFIED` rows, with a provenance comment per entry. |
| `md/DRAFT.md` | Markdown twin of `main.tex` with `<!-- num:id -->` markers, a numbers inventory, and a pre-submission checklist. |
| `figures/make_figures.py` | Results/index → CSV + hand-written SVG + `.tex` fragment (PDF/PNG only if matplotlib exists). |
| `tables/make_tables.py` | `summary_*.json` → booktabs `.tex` + Markdown twin. |
| `build.sh` | Compiles if LaTeX is installed; otherwise prints install instructions and exits 0. `--doctor` reports what is missing. |
| `BUILD.md` | Packages, commands, and the verified status of this directory. |
| `tests/test_template.py` | pytest: brace/environment balance, `refs.bib` parses to zero entries, generators run end-to-end on fixtures, refusals exit 2. |

## Quick start

```bash
cd 05_paper/template
./build.sh --doctor                 # what is installed, what is missing
python tools/citations_to_bib.py --csv ../../02_literature/verified_citations.csv \
       --out refs.generated.bib
python tables/make_tables.py  --summary ../../04_experiments/results/summary_main.json \
       --out-dir tables/generated --name main-results --format both
python figures/make_figures.py --index ../../04_experiments/RESULTS-INDEX.json \
       --figure main-accuracy --out-dir figures/generated
./build.sh                          # or: ./build.sh --venue ieee
```

Write the text in `main.tex` (and keep `md/DRAFT.md` in step), then run the
repo tools: `tools/check_numbers.py`, `tools/verify_citations.py`,
`06_review/ORIGINALITY.md`.

---

## Venue styles: official sources, licences, and the one rule

**The rule, for every venue: download the official files yourself, copy the
licence file that ships with them into the venue directory, read it, and do not
redistribute the official files from this repo.**
The stubs in `ieee/` and `acl/` are written from scratch for this repo: they
reproduce the *shape* of the layout and the minimum preamble, and contain no
copied file.

| Venue | Official source (verify before submission) | Licence / copyright | What to do |
|---|---|---|---|
| **ACL / *CL venues** | `https://github.com/acl-org/acl-style-files` — style files + `acl_natbib.bst` | Ships with its own licence file; **read it in the download and record its name here**. Not verified: this build machine has no network, so no licence in this table was checked against the source. | Download, copy `acl.sty` + `acl_natbib.bst` into `acl/`, keep the licence file beside them, and swap the two preamble lines marked `SWITCH TO THE OFFICIAL STYLE`. |
| **NeurIPS / NeurIPS workshops** | `https://neurips.cc` → *Paper Information* → *Style Files* (the page moves each year; find the current year's kit) | Distributed inside the author kit with its own notice; **read it in the download and record it here**. Not verified. | Download the kit, copy `neurips_20XX.sty` into `acl/`, use `\usepackage[preprint]{neurips_20XX}`, keep the notice. |
| **IEEE conferences** | `https://www.ieee.org/conferences/publishing/templates.html` | © IEEE. The templates page grants their use for preparing IEEE submissions; it does not grant redistribution. **Read the notice that comes with the download; do not re-host the files.** Not verified. | Download the conference template (the one matching your conference), read its notice, then move your text from `ieee/main.tex` into the official source. Layout, page limits and the copyright block belong to the venue, not to this stub. |

Why the stubs are not copies: an official template carries a licence you must
read and accept, and a page-limit/layout contract you must not silently edit. A
stub that compiles today is useful for drafting; it is not a submission format.
`README` is deliberately explicit about this because "I found a template on
GitHub" is how authors end up redistributing someone else's file with the
copyright notice stripped.

Every URL above must be re-checked before submission: venue pages move, and a
dead link at submission time is a deadline problem.

---

## How numbers and citations are kept honest

* **Numbers.** Nothing is typed by hand. `figures/make_figures.py` and
  `tables/make_tables.py` read `results.json` / `summary_*.json` /
  `RESULTS-INDEX.json` and refuse (exit 2) to plot or tabulate a metric that is
  missing. In the text, a number carries `% num:<id>` (LaTeX) or
  `<!-- num:<id> -->…<!-- /num -->` (Markdown) so `tools/check_numbers.py` can
  trace it back to a file.
* **Citations.** `refs.bib` has zero active entries. The only sanctioned way in
  is `tools/citations_to_bib.py`, which drops every row whose status is not
  `VERIFIED` and refuses a CSV with no `status` column.
* **Toy data.** A results file with `"toy": true` is refused by both generators
  (CONTRACTS section 5). `--allow-toy` exists only for smoke tests; output from
  it must never be cited.
* **AI assistance.** The disclosure lives in the author block footnote of each
  `main.tex`, with a matching Ethics Statement section. It is venue-specific on
  purpose: see `00_foundations/ETHICS-AND-AI-USE.md` for which venue wants it
  where.

## Known gaps (honest list)

* **Not compiled here.** No TeX installation exists on the machine this was
  built on, so no PDF was produced and no layout claim is made. `build.sh`
  documents the install; `BUILD.md` records the actual command output.
* **No PDF figures yet.** matplotlib is not installed, so `make_figures.py`
  emits CSV + SVG + a `.tex` fragment that renders a placeholder. Install
  matplotlib and re-run to get PDF/PNG; nothing else changes.
* **Page limits are not encoded.** A stub cannot know the current limit for
  your track; check the call for papers.
* **`\ref` targets in the stubs** point at labels defined in the same file
  (`sec:*`, `tab:main-results`, `fig:main-accuracy`), so they resolve without
  the generated files. The generated *snippets* contain no labels, which is why
  captions and labels live in `main.tex` and cannot collide.
* **Bibliography is empty.** `\bibliography{refs}` on an empty `.bib` emits
  "no \citation" warnings. That is the correct state of a skeleton.
