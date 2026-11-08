# Progress

- Engine installed: Tectonic 0.17.0 (sha256 f61ce51f... from GitHub asset digest via API). ENGINE.md written.
- md2tex.py built: paper.md -> body.tex (numbers byte-identical, tables booktabs tabularx, figure inclusion, refs.bib via citations_to_bib.py 342 entries). Tests: tests/test_md2tex.py PASS 296 numbers.
- Figures: svg2pdf.py (pure Python, no installs) converts F1 SVG -> PDF (6660 bytes). FIGURES.md records choice.
- Wrappers: paper-acl.tex (article+natbib) and paper-article.tex (a4paper, numbers natbib), both tabularx + emergencystretch. build.ps1 one-command build.
- PDFs built: out/paper-acl.pdf (~97 KiB), out/paper-article.pdf (~103 KiB). pdftotext extracts (title, numbers 75.50%/24.50%/83.03% present). No ?? references.
- Overfull: one ~10.9pt in acl (front-matter italic) and one ~16.7pt in article; table overfulls removed via tabularx X columns. Reported in BUILD-REPORT.md.
- Known gaps documented in BUILD-REPORT.md.
- Review batch completed: converter PASS (review-converter.md), engine and PDF verified directly by lead (review-engine.md, review-pdfs.md).
CARD COMPLETE
