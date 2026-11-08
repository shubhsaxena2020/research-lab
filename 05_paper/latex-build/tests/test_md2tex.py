#!/usr/bin/env python
"""test_md2tex.py -- verify every number in paper.md appears unchanged in body.tex."""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PAPER = ROOT / "05_paper" / "draft" / "paper.md"
BODY = ROOT / "05_paper" / "latex-build" / "body.tex"


def main():
    md = PAPER.read_text(encoding="utf-8")
    # extract numbers from <!-- num:... -->VALUE<!-- /num -->
    import re as _re
    nums = _re.findall(r"<!--\s*num:[^>]*-->(.*?)<!--\s*/num\s*-->", md, flags=_re.S)
    nums = [n.strip() for n in nums]
    subprocess.run(
        [sys.executable, str(ROOT / "05_paper" / "latex-build" / "md2tex.py")],
        check=True,
    )
    tex = BODY.read_text(encoding="utf-8")
    missing = []
    for n in nums:
        if n not in tex and n.replace("%", "\%") not in tex:
            missing.append(n)
    if missing:
        print(f"FAIL: {len(missing)} numbers missing from body.tex")
        for m in missing[:20]:
            print("  missing:", repr(m))
        return 1
    print(f"PASS: {len(nums)} numbers preserved in body.tex")
    return 0


if __name__ == "__main__":
    sys.exit(main())
