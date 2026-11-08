# Report: latex build batch 1 (lead direct)

Engine: Tectonic 0.17.0 installed at C:/Users/admin/tools/tectonic/tectonic.exe
sha256 f61ce51f0b0ade1015b7de7ef368541c5424e9756ecbd0d7af97d6d48030845f
(from GitHub release asset digest; downloaded via api.github.com asset URL).
ENGINE.md at 05_paper/latex-build/ENGINE.md.

Converter: md2tex.py maps paper.md -> body.tex; tests/test_md2tex.py PASS 296 numbers.

Figures: svg2pdf.py pure Python; F1 PDF 6660 bytes.

Build: tectonic paper-acl.tex and paper-article.tex -> out/*.pdf (97-103 KiB).

Verification: pdftotext shows title + 75.50%/24.50%/83.03%; tests pass.
