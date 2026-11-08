Figure conversion: pure-Python svg2pdf.py (no pip installs).

Choice: hand-written SVG->PDF for the subset used by 05_paper/figures/generated/*.svg
(rect, line, polyline, circle, text with rotate). No Inkscape/rsvg/cairosvg/svglib
was installed; the converter has zero dependencies (stdlib xml + math).

Verified: F1_abstain_precision_by_rung.pdf generated (6660 bytes) and text extracts
with pdftotext.
