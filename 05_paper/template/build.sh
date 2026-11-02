#!/usr/bin/env bash
# =============================================================================
#  build.sh -- compile the paper, or explain exactly what to install.
#
#  This script NEVER installs anything. It looks for latexmk / pdflatex and,
#  when they are missing, prints the install commands and exits 0, so that a
#  fresh clone on a machine without TeX does not look like a broken build.
#
#  Usage
#    ./build.sh                     compile main.tex
#    ./build.sh --venue ieee        compile ieee/main.tex (needs IEEEtran.cls)
#    ./build.sh --venue acl         compile acl/main.tex
#    ./build.sh --venue all         all three, reporting each separately
#    ./build.sh --engine pdflatex   force pdflatex+bibtex instead of latexmk
#    ./build.sh --regenerate        rebuild figures/tables from 04_experiments/
#    ./build.sh --doctor            report tool/package status, change nothing
#    ./build.sh --clean             remove aux files for the selected venue
#
#  Exit codes: 0 success or "nothing to do, here is how to install";
#              1 compile failure; 2 usage error.
#
#  What to install is documented in BUILD.md. Short version (Debian/Ubuntu):
#    sudo apt install texlive-latex-base texlive-latex-recommended \
#                     texlive-latex-extra texlive-fonts-recommended \
#                     latexmk biber texlive-publishers
#  (texlive-publishers is what provides IEEEtran.cls.)
# =============================================================================
set -u

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd) || exit 1
cd "$HERE" || exit 1
REPO=$(cd "$HERE/../.." && pwd)

VENUE=main
ENGINE=auto
DOCTOR=0
REGEN=0
CLEAN=0
FIGURE=main-accuracy
SUMMARY="$REPO/04_experiments/results/summary_main.json"

usage() {
  sed -n '4,30p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

while [ $# -gt 0 ]; do
  case "$1" in
    --doctor)     DOCTOR=1 ;;
    --regenerate) REGEN=1 ;;
    --clean)      CLEAN=1 ;;
    --venue)      VENUE="${2:-}"; shift ;;
    --engine)     ENGINE="${2:-}"; shift ;;
    --figure)     FIGURE="${2:-}"; shift ;;
    --summary)    SUMMARY="${2:-}"; shift ;;
    -h|--help)    usage; exit 0 ;;
    *) echo "build.sh: unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

case "$VENUE" in
  main|ieee|acl|all) ;;
  *) echo "build.sh: --venue must be main, ieee, acl or all (got '$VENUE')" >&2; exit 2 ;;
esac
case "$ENGINE" in
  auto|latexmk|pdflatex) ;;
  *) echo "build.sh: --engine must be auto, latexmk or pdflatex (got '$ENGINE')" >&2; exit 2 ;;
esac

have() { command -v "$1" >/dev/null 2>&1; }

# Git-bash/MSYS paths like /c/Users/... mean nothing to native python.exe;
# hand it a Windows path when we can.
winpath() {
  if have cygpath; then cygpath -w "$1"; else printf '%s' "$1"; fi
}

engine_available() {
  case "${1:-$ENGINE}" in
    latexmk)  have latexmk ;;
    pdflatex) have pdflatex ;;
    *)        have latexmk || have pdflatex ;;
  esac
}

pick_engine() {
  if [ "$ENGINE" != auto ]; then
    echo "$ENGINE"
  elif have latexmk; then
    echo latexmk
  elif have pdflatex; then
    echo pdflatex
  else
    echo none
  fi
}

install_instructions() {
  cat <<'EOF'

  No LaTeX engine found (neither latexmk nor pdflatex on PATH).
  Nothing was built. This script does not install packages; run one of these:

    Debian / Ubuntu / WSL
      sudo apt update
      sudo apt install texlive-latex-base texlive-latex-recommended \
                       texlive-latex-extra texlive-fonts-recommended \
                       latexmk biber texlive-publishers
      # texlive-publishers provides IEEEtran.cls (needed only for --venue ieee)

    macOS
      brew install --cask mactex-no-gui     # full TeX Live (~4 GB)
      # or: brew install --cask basictex && sudo tlmgr install latexmk booktabs \
      #        natbib caption xcolor geometry hyperref IEEEtran

    Windows
      winget install MiKTeX.MiKTeX          # then let MiKTeX fetch packages on first run
      # or install TeX Live: https://tug.org/texlive/windows.html

    Any platform, smallest useful install
      https://yihui.org/tinytex/  (TinyTeX) then:
      tlmgr install latexmk booktabs natbib caption xcolor geometry hyperref IEEEtran

  Packages this template uses: geometry, amsmath, amssymb, graphicx, booktabs,
  caption, natbib, xcolor, url, hyperref; IEEEtran for the IEEE stub; latexmk
  and bibtex or biber for the build. Optional: matplotlib (Python) for PDF
  figures -- the figure script works without it and emits SVG.

  After installing, re-run ./build.sh and ./build.sh --doctor.
EOF
}

doctor() {
  echo "build.sh --doctor  ($HERE)"
  echo "  repo root        : $REPO"
  printf '  python           : '; if have python; then python -V 2>&1; else echo "MISSING"; fi
  printf '  matplotlib       : '; if have python && python -c 'import matplotlib' >/dev/null 2>&1; then python -c 'import matplotlib; print(matplotlib.__version__)'; else echo "not installed (optional: SVG/CSV output only)"; fi
  for tool in latexmk pdflatex bibtex biber kpsewhich; do
    printf '  %-16s : ' "$tool"
    if have "$tool"; then
      case "$tool" in
        kpsewhich) echo "present" ;;
        *) "$tool" --version 2>/dev/null | head -1 ;;
      esac
    else
      echo "MISSING"
    fi
  done
  if have kpsewhich; then
    for sty in booktabs.sty natbib.sty caption.sty geometry.sty hyperref.sty IEEEtran.cls acl.sty; do
      printf '  %-16s : ' "$sty"
      if kpsewhich "$sty" >/dev/null 2>&1; then
        echo "found ($(kpsewhich "$sty"))"
      else
        echo "NOT FOUND"
      fi
    done
  fi
  echo "  generated files  :"
  if [ -d figures/generated ] && [ -n "$(ls -A figures/generated 2>/dev/null)" ]; then
    ls -1 figures/generated | sed 's/^/    figures\/generated\//'
  else
    echo "    figures/generated/ is empty (run --regenerate)"
  fi
  if [ -d tables/generated ] && [ -n "$(ls -A tables/generated 2>/dev/null)" ]; then
    ls -1 tables/generated | sed 's/^/    tables\/generated\//'
  else
    echo "    tables/generated/ is empty (run --regenerate)"
  fi
  echo
  if engine_available; then
    echo "  verdict: ready to build with $(pick_engine). Run ./build.sh"
  else
    echo "  verdict: cannot build here -- install TeX Live or MiKTeX (see BUILD.md)"
  fi
}

regenerate() {
  echo "-- regenerate: figures and tables from 04_experiments/"
  local idx="$REPO/04_experiments/RESULTS-INDEX.json"
  if [ -f "$idx" ]; then
    if have python; then
      echo "   figures: $FIGURE from $idx"
      python figures/make_figures.py --index "$(winpath "$idx")" --figure "$FIGURE" \
             --out-dir figures/generated || echo "   figures: generator refused (see message above)"
    else
      echo "   figures: skipped (python not on PATH)"
    fi
  else
    echo "   figures: skipped (no $idx yet -- no results to plot)"
  fi
  if [ -f "$SUMMARY" ]; then
    if have python; then
      echo "   tables : $SUMMARY"
      python tables/make_tables.py --summary "$(winpath "$SUMMARY")" --out-dir tables/generated \
             --name main-results --format both \
             || echo "   tables: generator refused (see message above)"
    else
      echo "   tables: skipped (python not on PATH)"
    fi
  else
    echo "   tables: skipped (no $SUMMARY yet)"
  fi
}

clean_one() {
  local dir="$1"
  ( cd "$dir" || exit 1
    if have latexmk && [ -f main.tex ]; then
      latexmk -C main.tex >/dev/null 2>&1 || true
    fi
    rm -f main.aux main.log main.out main.bbl main.blg main.fls main.fdb_latexmk \
          main.toc main.spl 2>/dev/null || true )
  echo "   cleaned $dir"
}

compile_one() {
  local dir="$1" engine="$2"
  local target="main.tex"
  if [ ! -f "$dir/$target" ]; then
    echo "   ERROR: $dir/$target does not exist" >&2
    return 1
  fi
  if [ "$engine" = latexmk ]; then
    ( cd "$dir" && latexmk -pdf -interaction=nonstopmode -halt-on-error \
                            -file-line-error main.tex )
    return $?
  fi
  ( cd "$dir" \
    && pdflatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex \
    && { if have bibtex; then bibtex main || true; fi; } \
    && pdflatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex \
    && pdflatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex )
  return $?
}

if [ "$DOCTOR" -eq 1 ]; then
  doctor
  exit 0
fi

if [ "$REGEN" -eq 1 ]; then
  regenerate
fi

if [ "$CLEAN" -eq 1 ]; then
  case "$VENUE" in
    main) clean_one "$HERE" ;;
    ieee) clean_one "$HERE/ieee" ;;
    acl)  clean_one "$HERE/acl" ;;
    all)  clean_one "$HERE"; clean_one "$HERE/ieee"; clean_one "$HERE/acl" ;;
  esac
  [ "$REGEN" -eq 1 ] || exit 0
fi

if ! engine_available; then
  install_instructions
  exit 0
fi

CHOSEN=$(pick_engine)
echo "-- build.sh: venue=$VENUE engine=$CHOSEN"

# A stub that needs an extra package must fail with an explanation, not with a
# screen of TeX errors.
if { [ "$VENUE" = ieee ] || [ "$VENUE" = all ]; } && have kpsewhich; then
  if ! kpsewhich IEEEtran.cls >/dev/null 2>&1; then
    cat <<'EOF'

  The IEEE stub needs IEEEtran.cls, which is not installed.
  Debian/Ubuntu:  sudo apt install texlive-publishers
  TeX Live:       tlmgr install IEEEtran
  (Or download the official IEEE template; see README.md.)
EOF
    [ "$VENUE" = all ] || exit 0
    VENUE=main
  fi
fi

status=0
build_venue() {
  local name="$1" dir="$2"
  echo "-- $name: compiling in $dir"
  if compile_one "$dir" "$CHOSEN"; then
    if [ -f "$dir/main.pdf" ]; then
      echo "   OK: $dir/main.pdf"
    else
      echo "   WARNING: command succeeded but no main.pdf appeared" >&2
    fi
  else
    echo "   FAILED: see $dir/main.log (last lines below)" >&2
    if [ -f "$dir/main.log" ]; then
      grep -E '^(!|.*\.tex:[0-9]+:)' "$dir/main.log" | head -10 >&2 || true
      tail -15 "$dir/main.log" >&2 || true
    fi
    status=1
  fi
}

case "$VENUE" in
  main) build_venue main "$HERE" ;;
  ieee) build_venue ieee "$HERE/ieee" ;;
  acl)  build_venue acl  "$HERE/acl" ;;
  all)
    build_venue main "$HERE"
    if have kpsewhich && kpsewhich IEEEtran.cls >/dev/null 2>&1; then
      build_venue ieee "$HERE/ieee"
    else
      echo "-- ieee: skipped (IEEEtran.cls not installed)"
    fi
    build_venue acl "$HERE/acl"
    ;;
esac

exit "$status"
