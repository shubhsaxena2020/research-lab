# BUILD.md — how to compile this paper, and what is verified

`build.sh` never installs anything. It compiles when a LaTeX engine exists and
prints the install commands when it does not, exiting 0 in that case so a fresh
clone is not mistaken for a broken build.

## Requirements

| Needed for | Package | Debian / Ubuntu | macOS | Windows |
|---|---|---|---|---|
| any build | TeX Live or MiKTeX | `texlive-latex-base` | `brew install --cask mactex-no-gui` | `winget install MiKTeX.MiKTeX` |
| `booktabs`, `caption`, `xcolor`, `natbib` | LaTeX extra packages | `texlive-latex-extra` | included in MacTeX | MiKTeX installs on demand |
| `geometry`, `graphicx`, `amsmath`, `hyperref` | LaTeX recommended | `texlive-latex-recommended` | included | MiKTeX on demand |
| build driver | `latexmk` | `latexmk` | included in MacTeX | `tlmgr install latexmk` |
| bibliography | `bibtex` (or `biber`) | `texlive-latex-base` / `biber` | included | included |
| IEEE stub only | `IEEEtran.cls` | `texlive-publishers` | included | MiKTeX on demand |
| figure PDF/PNG (optional) | matplotlib | `pip install matplotlib` | same | same |

One command, Debian/Ubuntu/WSL:

```bash
sudo apt update && sudo apt install -y \
  texlive-latex-base texlive-latex-recommended texlive-latex-extra \
  texlive-fonts-recommended latexmk biber texlive-publishers
```

Smallest useful install (any platform): [TinyTeX](https://yihui.org/tinytex/),
then

```bash
tlmgr install latexmk booktabs natbib caption xcolor geometry hyperref IEEEtran
```

## How to run

```bash
cd 05_paper/template

./build.sh --doctor        # what is installed; changes nothing; always exits 0
./build.sh                 # main.tex  -> main.pdf  (latexmk if present, else pdflatex x3 + bibtex)
./build.sh --venue ieee    # ieee/main.tex (needs IEEEtran.cls; compiled from ieee/)
./build.sh --venue acl     # acl/main.tex  (compiles with plain article today)
./build.sh --venue all     # all three, each reported separately
./build.sh --clean         # remove aux files for the selected venue
./build.sh --regenerate    # run the figure/table generators against 04_experiments/ first
```

Each stub is compiled **from its own directory**, because `\input`/`\bibliography`
paths are relative to the compile directory, not to the file:

```
05_paper/template/main.tex      -> \input{tables/generated/...}      \bibliography{refs}
05_paper/template/ieee/main.tex -> \input{../tables/generated/...}   \bibliography{../refs}
05_paper/template/acl/main.tex  -> \input{../tables/generated/...}   \bibliography{../refs}
```

Exit codes: `0` success or "nothing to build, here is how to install";
`1` compile failure (last log lines are printed); `2` usage error.

## Caveat: the official venue styles are not here, and must not be taken from here

`ieee/` and `acl/` are minimal stubs written for this repo. The official IEEE,
ACL and NeurIPS files carry their own licence and layout contract. Download them
yourself from the sources listed in `README.md`, read the licence that ships with
them, keep it beside the files, and do not redistribute them from this repo.

Layout, page limits and the copyright block are owned by the venue. The stub is
for drafting; the official template is for submission.

## Figures without matplotlib

`figures/make_figures.py` writes a CSV, a hand-written SVG, and a `.tex` fragment.
PDF/PNG output is produced only if matplotlib imports. Without it the `.tex`
fragment renders a visible placeholder box, so the paper still compiles. To get
PDFs:

```bash
pip install matplotlib
python figures/make_figures.py --index 04_experiments/RESULTS-INDEX.json \
       --figure main-accuracy --out-dir figures/generated
```

## Verified status (what was actually run)

Run on 2026-11-03 on the repo's Windows build machine, from
`C:\Users\shubh\research-lab\05_paper\template`. **No LaTeX distribution is
installed there**, so no PDF was produced and this directory makes no claim that
`main.tex` typesets correctly. What *was* run is below, verbatim.

`./build.sh --doctor`:

```
build.sh --doctor  (/c/Users/shubh/research-lab/05_paper/template)
  repo root        : /c/Users/shubh/research-lab
  python           : Python 3.11.15
  matplotlib       : not installed (optional: SVG/CSV output only)
  latexmk          : MISSING
  pdflatex         : MISSING
  bibtex           : MISSING
  biber            : MISSING
  kpsewhich        : MISSING
  generated files  :
    figures/generated/ is empty (run --regenerate)
    tables/generated/ is empty (run --regenerate)

  verdict: cannot build here -- install TeX Live or MiKTeX (see BUILD.md)
```

`./build.sh` (no engine installed) printed the Debian/macOS/Windows/TinyTeX
install block and exited `0`:

```
  No LaTeX engine found (neither latexmk nor pdflatex on PATH).
  Nothing was built. This script does not install packages; run one of these:
  ...
  After installing, re-run ./build.sh and ./build.sh --doctor.
rc=0
```

The generators and the test suite were run for real; see
`sessions/S3-experiments/reports/S3-3.md` for the full transcript, and
`tests/test_template.py` for the assertions. The pytest suite is the closest
thing to a compile check available in this environment: it verifies balanced
braces and `\begin`/`\end` pairs in every `.tex` file, that every `\ref` has a
matching `\label`, and that `refs.bib` parses to zero entries.

**First thing to do on a machine with LaTeX**: run `./build.sh` and fix whatever
it reports. Until then, treat the layout as untested.
