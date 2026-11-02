#!/bin/sh
# ops/check.sh - one command that proves the whole S3 toolchain still works.
#
#   sh ops/check.sh              # 3 test suites + toy pipeline
#   sh ops/check.sh --fast       # test suites only (skips the slow toy pipeline)
#   sh ops/check.sh --list       # show the steps, run nothing
#   sh ops/check.sh --only toy-pipeline
#
# This is a thin wrapper: it cds to the repo root (so relative paths inside the runner and
# in any message you paste are the same ones everyone else sees) and hands every argument
# straight to tools/check_all.py. It adds no logic, so the Python runner stays the single
# source of truth and is testable on its own.
#
# Exit code is the runner's: 0 = every step passed, 1 = a step failed, 2 = usage error.
#
# WINDOWS / MSYS CAVEAT ---------------------------------------------------------------
# This host's shell is git-bash/MSYS. MSYS rewrites path-like arguments for *MSYS*
# programs, but it does NOT translate them for native Windows programs such as python.exe.
# So if you ever pass a path to python by hand, use a native path:
#
#     python tools/check_all.py --only toy-pipeline     # fine, no path argument
#     python C:/Users/shubh/research-lab/tools/check_all.py   # fine: native C:/... path
#     python /c/Users/shubh/research-lab/tools/check_all.py   # BROKEN: python sees a
#                                                              # literal "/c/..." path
#
# (This wrapper sidesteps the issue entirely: it uses a relative path after cd, and the
# runner resolves its own repo root with Path(__file__).resolve().parents[1].)
set -eu

# Resolve the repo root from this script's own location, so `sh ops/check.sh` works from
# anywhere and through a symlink or a relative path.
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/.." && pwd)
cd "$repo_root"

exec python tools/check_all.py "$@"
