# ORIGINALITY — the procedure we actually run before a draft is called done

RULES.md #3 says: summarize in your own words, quote sparingly with quotation marks and
citation, never paste paper text — and run *this* procedure before any draft is called done.

Everything below is free, local and offline. Nothing is uploaded: the draft is unpublished,
and RULES.md #7 forbids scraping behind logins, so no paid plagiarism service and no
"paste your text here" website is used at any point.

**What this procedure is.** A mechanical search for long verbatim runs shared between the
draft and the source texts we actually read, plus a quotation audit, plus a documented
human read of the worst hits.

**What it is not.** It is not a plagiarism detector. A pass does not prove originality. It
proves one narrow, checkable thing: *no run of 8 or more consecutive words from the
corpus survives in the draft outside quotation marks*. The corpus is only the sources we
consulted and archived — a source read but never archived is invisible to it. It cannot
see the web, it cannot see ideas, and it cannot see a close paraphrase that swaps every
third word (that is what the human read in Step 4 is for).

Time cost: about 10 minutes for a 5,000-word draft plus the manual read.

---

## Step 0 — Build the corpus from the PDFs we actually read

Only sources that exist in `02_literature/sources/` belong in the corpus. If a paper
influenced the draft but its text was never saved, add it first; if it cannot be obtained
legitimately, say so in the session STATUS and treat its influence as a manual-review item.

Layout:

```
02_literature/sources/            # publisher PDFs, kept local, never committed
02_literature/sources/txt/        # plain-text derivatives -- this is the corpus
```

### Converter: which one, and is it installed

Use **`pdftotext` (poppler/Xpdf)** as the primary converter and **`pdfminer.six`** only as
the fallback for PDFs `pdftotext` mangles.

Check what this machine has before assuming:

```bash
command -v pdftotext && pdftotext -v            # primary
python -c "import pdfminer; print(pdfminer.__version__)"   # fallback
```

State on this machine (verified 2026-11-03, no network, no `pip install`):

| tool | status here | note |
|------|-------------|------|
| `pdftotext` | **installed** — `pdftotext version 4.00` (Xpdf), `/mingw64/bin/pdftotext` | use this |
| `pdfminer` | not installed (`ModuleNotFoundError`) | fallback only |
| `pypdf` | not installed | not used |

So the commands below work here today. On another machine, if `command -v pdftotext`
prints nothing, either install poppler locally or use the pdfminer fallback — do not
substitute hand-typed "quotes from memory".

### Convert

```bash
cd /c/Users/shubh/research-lab
mkdir -p 02_literature/sources/txt

for pdf in 02_literature/sources/*.pdf; do
  [ -e "$pdf" ] || continue
  base=$(basename "$pdf" .pdf)
  out="02_literature/sources/txt/$base.txt"
  [ -s "$out" ] && { echo "skip (exists): $base"; continue; }
  if ! pdftotext -layout -nopgbrk -enc UTF-8 "$pdf" "$out"; then
    echo "FAILED: $pdf"; rm -f "$out"; continue
  fi
  n=$(wc -w < "$out" | tr -d ' ')
  echo "$base: $n words"
  if [ "$n" -lt 500 ]; then
    echo "  WARN: $base extracted only $n words -- scanned/image PDF?"
  fi
done
```

Fallback for one stubborn PDF (only if pdfminer is available):

```bash
python -c "from pdfminer.high_level import extract_text; import sys; print(extract_text(sys.argv[1]))" \
  02_literature/sources/foo.pdf > 02_literature/sources/txt/foo.txt
```

Rules for the corpus:

- **De-hyphenate line breaks in the extracted text before checking.** PDF extraction
  turns `docu-\nment` into two tokens, which hides a word and therefore *understates*
  overlap. One pass fixes it (perl ships with Git Bash):
  `perl -0pi -e 's/(\w)-\n(\w)/$1$2/g' 02_literature/sources/txt/*.txt`
  It also joins genuine compounds split at a line end (`state-\nof-the-art` →
  `stateof-the-art`), which is harmless for matching but means the corpus line numbers
  are those of the `.txt`, not of the PDF page. Run it once after extraction, not on every
  check.
- **Do not** put the draft, your notes, or any LLM output into `02_literature/sources/txt/`.
  The corpus is other people's text, nothing else.
- A WARN line (under 500 words) usually means a scanned PDF. OCR is not installed; mark
  the source `UNAVAILABLE` in the session STATUS rather than pretending it was checked.
- Two files of the same paper (preprint + proceedings) are fine — duplicates only make
  the check stricter.
- Publisher PDFs stay local. Do not `git add` them; the `.txt` derivatives are what the
  check needs and what the report cites.
- Rebuild the corpus whenever a new source is read. A stale corpus is a silent hole.

Sanity check: `ls 02_literature/sources/txt | wc -l` should equal the number of PDFs you
believe you read.

---

## Step 1 — Run the checker

```bash
cd /c/Users/shubh/research-lab
python tools/originality_check.py \
  --draft 05_paper/main.md \
  --corpus 02_literature/sources/txt \
  --n 8 --min-words 8 \
  --out 06_review/originality-$(date +%Y%m%d).md
```

Add `--json` for machine-readable output (the report shape is stable; use it in scripts).
`--strict-quotes` also fails the run on an uncited quotation or a quote-budget overrun —
use it for the final gate.

What the checker does, so the report is readable:

- Reads `.md`, `.tex`, `.txt`. Normalizes whitespace and case; tokenizes on words
  (hyphens split, apostrophes kept).
- **Strips LaTeX markup but keeps the argument text**: `\emph{per-item notes}` →
  `per-item notes`. Citation commands (`\citep{...}`, `\citet{...}`, `\parencite{...}`)
  are removed entirely — their argument is a bibliography key, not prose — and replaced
  by a non-word sentinel so the quotation audit can still see that a citation was there.
- Drops unescaped `%` comments in `.tex` and `<!-- -->` comments in `.md`: commented-out
  text is not in the paper and can never count as an overlap.
- **Ignores the draft's own References/Bibliography section** (Markdown heading, `\section
  {References}`, `\bibliography{}`, `\begin{thebibliography}`, or a bare `References` line
  in `.txt`). Your bibliography is not your prose; citations are checked by
  `tools/verify_citations.py`, not here.
- Finds **maximal** runs: one hit per shared passage, not one per sliding window. A
  20-word copy is reported once, as 20 words — not thirteen times as 8-word hits.
- Classifies each run `UNQUOTED` or `QUOTED`. `QUOTED` means *every* token of the run is
  inside a quotation (straight `"..."`, curly `“...”`, guillemets `«...»`, or TeX
  double-backtick quotes); a run that starts inside a quote and ends outside it is
  `UNQUOTED`, deliberately.
- Prints, per hit: draft line + sentence, source file + line + sentence, a 12-word
  context window on each side, and the shared text.
- Audits quotations: every quoted span must carry a citation marker in the same sentence
  (`\citep`, `[@key]`, `[3]`, `(Author, 2020)`), and total quoted words must stay under
  the budget (default **2%** of draft words).

Reading the output:

```
verdict: FAIL  hits=3 unquoted=1 quoted=2 longest_unquoted=18
quoted words: 74/4210 = 1.76% (budget 2.00%); uncited quotes: 0
  H001 UNQUOTED  18w draft:412 <- smith2020.txt:2190
```

`FAIL` here means "a decision is outstanding", not "you plagiarised". A single
`UNQUOTED` hit can still be a coincidence; Step 2 is how that gets decided.

---

## Step 2 — Classify every hit

Every `UNQUOTED` hit gets exactly one decision, written into the report:

| Class | What it looks like | Action |
|-------|--------------------|--------|
| **Coincidental technical phrase** | Field-standard wording in a fixed order (`attention over the encoder states`), no distinctive word choice, and the sentence would read the same if you had never seen the source | **FINE** — one-line justification required |
| **Unmarked quotation** | Intact clause or sentence, grammar and word order preserved, distinctive phrasing or numbers | **MUST FIX** — put it in quotation marks with a citation in the same sentence, or delete it and rewrite |
| **Paraphrase too close** | Same sentence skeleton and same sequence of ideas, with a few words swapped; often *below* the 8-word threshold and therefore invisible to the tool | **MUST FIX** — close the source, rewrite from your own notes, then re-run |

Decision rule that keeps this honest: **if you cannot justify a hit as coincidental in one
sentence, it is a MUST FIX.** "It's just standard terminology" is a justification only if
the run contains no verbatim clause; `the model was trained on the training set` is
standard, `we found that the model was trained on the training set and evaluated` is not.

`QUOTED` hits are not automatically fine either: check the citation is in the same
sentence, the quote is not longer than needed, and the quoted claim is one you actually
rely on.

Write the decision next to the hit in the report file:

```
### H001 UNQUOTED 18w  draft:412 <- smith2020.txt:2190
- Decision: FIXED (rewritten)
- Was: "pipeline encodes each document into a dense vector and compares candidate passages"
- Now: "each document becomes a dense vector; candidate passages are ranked by cosine similarity" (line 412)
- Justification: original sentence order preserved the source's clause structure.
```

Then fix the draft and **re-run**: after the fix the hit must either disappear or come
back `QUOTED` with a citation. A hit that "went away" without a diff is a corpus mistake,
not a fix.

---

## Step 3 — Quotation audit

The checker reports both numbers; you confirm them by eye:

```bash
python tools/originality_check.py --draft 05_paper/main.md \
  --corpus 02_literature/sources/txt --strict-quotes
```

- **Every** quoted string must have a citation in the same sentence. Not the next
  sentence, not the paragraph's topic sentence — the same sentence.
- **Total quoted words ≤ 2% of draft words.** The tool prints `quoted words: X/Y = Z%`.
  Direct quotation is for definitions, a contested claim you are arguing against, or a
  phrase you cannot improve — not for related work.
- Short quoted terms of art (`"chain-of-thought"`) still need the citation.
- If the venue requires page numbers for quotations, add them now; the checker cannot.

A quote budget overrun is not a style opinion: at 5% quoted you are assembling the paper
from other people's sentences, and reviewers read it that way.

---

## Step 4 — Manual read of the top 10 hits

The tool cannot judge paraphrase. The human read is the part that catches it.

1. Take the **top 10** hits — the report lists unquoted hits first, longest first, so the
   worst cases are at the top; include `QUOTED` hits in the read.
2. For each: open the source at the reported line and the draft at the reported line.
   Read both sentences aloud.
3. Ask three questions: *Could I have written this sentence without having read that
   one? Does it follow the source's order of ideas? Would a reviewer put these side by
   side?* Any "no / yes / yes" → rewrite.
4. Record one line per hit in the report ("read, source p. 4, independent" is enough).
5. Also skim the draft for the two things n-grams miss: (a) a paragraph whose structure
   mirrors one source paragraph section by section; (b) a sentence that is a translation
   or a synonym-swap of a source sentence you remember. Fix by rewriting from notes.

The top-10 read is not optional and cannot be delegated to the tool. If the report has
fewer than 10 hits, read them all.

---

## Pass criteria

A draft may be called original **only** when all four hold, recorded in the report file
committed with the draft:

1. **Zero unmarked quotes** — every quoted span has a citation in the same sentence
   (`n_uncited_quotes == 0` in `--json`).
2. **Zero `UNQUOTED` passages of 8 or more consecutive shared words** — the checker exits
   0 with `--n 8` over the complete corpus.
3. **Quoted words under budget** — ratio printed by the tool, ≤ 2% (or the stricter
   venue limit), stated in the report.
4. **Documented manual read of the top-10 hits** — each with a decision and a one-line
   justification, dated and signed by the author (`Shubh`), in the same report file.

If any of the four fails, the draft is not done — regardless of how good the prose is.
Re-run the whole procedure after any prose edit; a "small wording change" is exactly how
an unmarked quote gets reintroduced.

Suggested record in the session STATUS: `originality: PASS 2026-11-05, report
06_review/originality-20261105.md, corpus 14 files, 0 unquoted, 1.7% quoted`.

---

## What this cannot catch (state this in the report, do not paper over it)

- **Synonym-level paraphrase** and translated text: no shared 8-gram exists.
- **Ideas, structure, experimental design**: not text, not detectable here.
- **Sources not in the corpus** — including anything read from a web page, a blog, a
  lecture slide, or a paper we never archived. The report's corpus list is the honest
  scope statement.
- **Figures and tables** copied or adapted from a source: check licences separately, and
  caption/credit every reused figure.
- **Self-plagiarism** from your own earlier paper or report: add that text to the corpus
  by hand if it exists, or check it manually.
- **Fabricated citations** — that is `tools/verify_citations.py` (RULES.md #1), a separate
  gate.
- **Anything behind a login or on the open web.** Deliberate: we do not upload the draft.

So the report always carries the same sentence, and so does the answer to "is this
original?": *no long verbatim passages from the consulted corpus remain outside quotation
marks; originality itself is the author's claim, supported by this evidence and the manual
read.*

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `exit 2`, `draft not found` | wrong path | run from repo root; quote paths |
| `exit 2`, `unsupported draft type` | `.rst`, `.docx` | export to `.md`/`.txt` first |
| `exit 2`, `no .txt/.md files under corpus path` | corpus not built | Step 0 |
| hits inside your bibliography | reference heading not recognised | add the exact heading to `MD_REF_RE`/`TEX_REF_RE` in the tool, or rename the section |
| every hit is in one source and looks like boilerplate | PDF header/footer noise | re-extract with `-layout`, or delete the repeated running head from the `.txt` |
| zero hits on a draft you suspect | corpus incomplete | count PDFs vs `.txt` files; check the WARN lines from Step 0 |
| huge draft, slow run | O(n·m) matching | run per section (`--draft 05_paper/sec3.md`) and merge the reports |

Tool contract: `tools/originality_check.py --help`; tests:
`python -m pytest tools/tests/test_originality_check.py -q` (27 tests, offline).
