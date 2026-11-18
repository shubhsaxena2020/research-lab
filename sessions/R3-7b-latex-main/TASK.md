# TASK R3-7b — move the LaTeX/PDF build to the main laptop (MAIN laptop, profile res-s1)

Context (head, 2026-11-18): R3-7 built the ACL and article PDFs on laptop 2, which is now offline. Its build lives in
`05_paper/latex-build/` (md2tex.py, svg2pdf.py, build.ps1, tests/, BUILD-REPORT.md, ENGINE.md). `build.ps1` line 12
hardcodes `C:/Users/admin/tools/tectonic/tectonic.exe`, which does not exist here. The current PDFs were built from an
older draft, and BUILD-REPORT.md records one overfull box of about 10.9pt in the ACL build (limit is 10pt).
R3-4b (the other session) owns the draft and is editing it now; never edit anything outside your OWNED paths.

OWNED: `05_paper/latex-build/**`, `tools/tectonic/**` (create it; add `tools/tectonic/` to .gitignore — that one line is
the only edit you may make to .gitignore), `sessions/R3-7b-latex-main/**`. Everything else is read-only.

Deliverables
1. Install Tectonic 0.17.0 (the same version as ENGINE.md) into `C:\Users\shubh\research-lab\tools\tectonic\` from the
   official GitHub release zip. Verify the sha256 against the release page if it is published. Record the URL, hash and
   path in ENGINE.md (keep the laptop-2 record as history). No admin rights, no other installs.
2. Make build.ps1 find the engine without a hardcoded user path: repo-relative `tools/tectonic/tectonic.exe` first, then
   an optional TECTONIC env var. It must still fail loudly on undefined references or citations.
3. Build the CURRENT draft: `out/paper-acl.pdf` and `out/paper-article.pdf`. Run
   `python 05_paper/latex-build/tests/test_md2tex.py` (a plain script, not pytest) and the PDF checks from R3-7
   (page count, no ?? references, all tables present, numbers in the extracted text match paper.md).
4. Fix the 10.9pt overfull box so no box exceeds 10pt, without changing any number or wording in paper.md
   (fix it in the converter or the LaTeX preamble).
5. Update BUILD-REPORT.md for this laptop. The final rebuild after R3-4b finishes is done by the head with
   `build.ps1`, so the build must be one command and re-runnable on any later draft.
Batches of exactly 3 subagents (engine install / build.ps1 + overfull fix / checks), then a reviewer subagent re-runs
the whole build clean.
