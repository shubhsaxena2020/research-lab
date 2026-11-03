"""Assemble 05_paper/draft/paper.md from the template and the generated tables.

Why a build step: the review asked for tables inlined rather than referenced by path, and the numbers
audit requires every table cell to carry a traceability marker. Both are satisfied only if the table
text comes from the generator (make_paper_assets.py) and is never retyped. The template contains
`{{TABLE:<name>}}` placeholders; this script substitutes the contents of
05_paper/tables/generated/<name>.md verbatim and refuses to build if a placeholder has no file or a
generated table would be included twice.

Run: python 05_paper/build_draft.py
Writes: 05_paper/draft/paper.md, and prints a sha256 of the result.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "05_paper" / "template" / "draft_template.md"
TABLES = ROOT / "05_paper" / "tables" / "generated"
OUT = ROOT / "05_paper" / "draft" / "paper.md"

PLACEHOLDER = re.compile(r"\{\{TABLE:([A-Za-z0-9_]+)\}\}")


def main() -> int:
    text = TEMPLATE.read_text(encoding="utf-8")
    used: list[str] = []

    def sub(match: re.Match) -> str:
        name = match.group(1)
        path = TABLES / f"{name}.md"
        if not path.exists():
            raise SystemExit(f"no generated table {path} — run make_paper_assets.py first")
        if name in used:
            raise SystemExit(f"table {name} included twice; reference it instead of duplicating it")
        used.append(name)
        return path.read_text(encoding="utf-8").rstrip("\n")

    out = PLACEHOLDER.sub(sub, text)
    if PLACEHOLDER.search(out):
        raise SystemExit("a table placeholder was left unexpanded")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(out + "\n", encoding="utf-8")
    blob = OUT.read_bytes()
    print(f"wrote {OUT.relative_to(ROOT).as_posix()} from {len(used)} tables "
          f"({', '.join(used)}); {len(blob)} bytes; sha256 {hashlib.sha256(blob).hexdigest()[:12]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
