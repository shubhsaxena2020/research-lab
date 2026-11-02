"""Make ``04_experiments/harness`` importable from the tests.

``04_experiments`` is not a valid Python package name (it starts with a digit),
so the harness modules are imported as top-level ``stats`` / ``tables`` after
putting the harness directory on sys.path.
"""

import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parents[1]
if str(HARNESS) not in sys.path:
    sys.path.insert(0, str(HARNESS))
