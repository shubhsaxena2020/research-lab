#!/usr/bin/env python
"""Single-slot heavy-compute lock (``ops/HEAVY.lock``) -- RULES.md #10.

The laptop is shared with another build, so at most one heavy job (training,
big downloads) may run at a time.  This module is that mutual exclusion:

* ``acquire(name, timeout=...)`` returns a context manager.  The lock file is
  created with ``O_CREAT | O_EXCL`` (atomic on Windows and POSIX), so two
  racing processes cannot both win.
* If a lock already exists and is **live**, ``acquire`` raises :class:`LockError`
  immediately (or after waiting ``timeout`` seconds) naming the holder:
  name, pid, host, age.
* A lock is **stale** -- and is reclaimed with a warning -- when
  ``age > stale_after_s`` (default 4 h, env ``HEAVY_LOCK_STALE_S``) or when the
  holder pid is dead *on this host*.  A lock held by another host is never
  judged by pid (it is judged by age only).
* The lock is always released on exception (the context manager uses
  ``finally``), and release only deletes the file if it still carries our
  token, so a reclaimed lock cannot be deleted by its previous owner.
* Reclaiming happens under a short-lived guard file (``HEAVY.lock.guard``,
  also ``O_EXCL``) and re-reads the lock inside the guard, so two processes
  cannot both reclaim and both create a lock.

CLI
---
    python 04_experiments/harness/lock.py status      # exit 0 free, 1 held
    python 04_experiments/harness/lock.py acquire --name train --timeout 0
    python 04_experiments/harness/lock.py release [--force]
    ... add ``--json`` to any of them for machine-readable output.

``acquire`` from the CLI leaves the lock in place after the process exits (that
is the ops/heavy_lock.py semantics); call ``release`` when the job is done.  If
the process dies, the next ``acquire`` sees a dead pid on this host and
reclaims the stale lock automatically.
"""

from __future__ import annotations

import argparse
import json
import os
import socket
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

#: Default staleness threshold: 4 hours.  Override with HEAVY_LOCK_STALE_S.
STALE_AFTER_S = 4 * 60 * 60
#: Upper bound for ``timeout=None`` so a wedged job cannot block forever.
MAX_WAIT_S = 60 * 60
#: Poll interval while waiting for a lock.
POLL_S = 0.25


class LockError(RuntimeError):
    """A live heavy lock is held by someone else (or the lock is unusable)."""


def _repo_root() -> Path:
    env = os.environ.get("RESEARCH_LAB_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    here = Path(__file__).resolve().parent
    for cand in (here, *here.parents):
        if (cand / "RULES.md").is_file() or (cand / "04_experiments").is_dir():
            return cand
    return here.parents[1]


def lock_path() -> Path:
    """``$HEAVY_LOCK_PATH`` if set, else ``<repo>/ops/HEAVY.lock``."""
    env = os.environ.get("HEAVY_LOCK_PATH")
    if env:
        return Path(env).expanduser()
    return _repo_root() / "ops" / "HEAVY.lock"


def stale_after_s() -> float:
    try:
        return float(os.environ.get("HEAVY_LOCK_STALE_S", STALE_AFTER_S))
    except ValueError:
        return float(STALE_AFTER_S)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _atomic_create(path: Path, payload: str) -> bool:
    """Create ``path`` with contents ``payload`` atomically; False if it exists."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    except FileExistsError:
        return False
    try:
        os.write(fd, payload.encode("utf-8"))
        os.fsync(fd)
    finally:
        os.close(fd)
    return True


def _read(path: Path) -> Optional[Dict[str, Any]]:
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    except OSError:
        return {"raw": "<unreadable>", "pid": None, "host": None, "name": "<unreadable>"}
    try:
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValueError
        data.setdefault("name", "<unnamed>")
        return data
    except (ValueError, json.JSONDecodeError):
        # A truncated hand-made lock is still a lock; treat it as very old.
        return {"name": "<unparsable>", "pid": None, "host": None,
                "created_at": None, "created_ts": 0.0, "raw": raw}


def pid_alive(pid: Optional[int]) -> Optional[bool]:
    """True/False for a pid on this host, None when it cannot be determined."""
    if not isinstance(pid, int) or pid <= 0:
        return None
    try:
        import psutil  # type: ignore
    except Exception:
        psutil = None  # type: ignore
    if psutil is not None:
        try:
            return bool(psutil.pid_exists(pid))
        except Exception:
            pass
    if os.name == "posix":
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        except OSError:
            return None
        return True
    # Windows without psutil: OpenProcess + GetExitCodeProcess.
    try:
        import ctypes
        from ctypes import wintypes

        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        STILL_ACTIVE = 259
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if not handle:
            err = ctypes.get_last_error()
            return True if err == 5 else False  # 5 = access denied => alive
        try:
            code = wintypes.DWORD()
            if kernel32.GetExitCodeProcess(handle, ctypes.byref(code)):
                return code.value == STILL_ACTIVE
            return None
        finally:
            kernel32.CloseHandle(handle)
    except Exception:
        return None


def _age_s(info: Dict[str, Any]) -> Optional[float]:
    ts = info.get("created_ts")
    if isinstance(ts, (int, float)):
        return max(0.0, time.time() - float(ts))
    return None


def describe(info: Dict[str, Any]) -> str:
    age = _age_s(info)
    age_txt = f"{age:.0f}s" if age is not None else "unknown age"
    return (f"name={info.get('name')} pid={info.get('pid')} "
            f"host={info.get('host')} since={info.get('created_at')} ({age_txt})")


def staleness(path: Optional[Path] = None) -> Dict[str, Any]:
    """Inspect the lock: exists/held/stale plus the reason."""
    path = Path(path) if path else lock_path()
    info = _read(path)
    if info is None:
        return {"path": str(path), "exists": False, "held": False, "stale": True,
                "reason": "absent", "holder": None}
    age = _age_s(info)
    reason = None
    if age is not None and age > stale_after_s():
        reason = f"age {age:.0f}s > stale threshold {stale_after_s():.0f}s"
    elif info.get("host") == socket.gethostname():
        alive = pid_alive(info.get("pid"))
        if alive is False:
            reason = f"pid {info.get('pid')} is not running"
    return {"path": str(path), "exists": True, "held": True, "stale": reason is not None,
            "reason": reason or "live", "holder": info,
            "age_s": age, "stale_after_s": stale_after_s()}


def status(path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    """Holder info or None when the lock is free."""
    state = staleness(path)
    return state["holder"] if state["exists"] else None


class _Acquired:
    """Context manager returned by :func:`acquire`."""

    def __init__(self, info: Dict[str, Any], path: Path) -> None:
        self.info = info
        self.path = path
        self.released = False

    def __enter__(self) -> "_Acquired":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self.release()
        return False

    def release(self) -> None:
        """Delete the lock if it is still ours (token match)."""
        if self.released:
            return
        self.released = True
        current = _read(self.path)
        if current is None:
            return
        if current.get("token") != self.info.get("token"):
            print(f"warning: heavy lock {self.path} no longer ours "
                  f"(holder: {describe(current)}); leaving it in place", file=sys.stderr)
            return
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass


def _reclaim(path: Path, state: Dict[str, Any], warn: bool = True) -> bool:
    """Remove a stale lock under a guard file.  True if the stale lock is gone."""
    guard = path.with_name(path.name + ".guard")
    deadline = time.monotonic() + 5.0
    acquired_guard = False
    while time.monotonic() < deadline:
        token = uuid.uuid4().hex
        if _atomic_create(guard, json.dumps({"pid": os.getpid(), "token": token})):
            acquired_guard = True
            break
        current = _read(guard)
        if current is not None and current.get("host") == socket.gethostname() \
                and pid_alive(current.get("pid")) is False:
            try:
                guard.unlink()
            except FileNotFoundError:
                pass
            continue
        time.sleep(0.02)
    if not acquired_guard:
        # Someone else is reclaiming right now; let the caller retry.
        print(f"warning: could not take reclaim guard {guard}; retrying", file=sys.stderr)
        return False
    try:
        # Re-check inside the guard: the situation may have changed.
        fresh = _read(path)
        if fresh is None:
            return True
        if fresh.get("token") != (state.get("holder") or {}).get("token"):
            return True  # someone else already replaced it; do not touch
        if warn:
            print(f"warning: reclaiming stale heavy lock {path}: "
                  f"{describe(fresh)} ({state.get('reason')})", file=sys.stderr)
        try:
            path.unlink()
        except FileNotFoundError:
            pass
        return True
    finally:
        try:
            guard.unlink()
        except FileNotFoundError:
            pass


def acquire(name: str, timeout: Optional[float] = 0.0, *, path: Optional[Path] = None,
            stale_after: Optional[float] = None, force: bool = False,
            command: Optional[str] = None, owner_pid: Optional[int] = None) -> _Acquired:
    """Take the heavy lock or raise :class:`LockError` naming the holder.

    ``timeout``: seconds to wait for a live lock (0 = fail fast, None = wait up
    to ``MAX_WAIT_S``).  ``force`` reclaims even a live lock (loud warning).
    ``owner_pid``: pid recorded as the holder; defaults to this process.  The
    CLI passes its parent (the invoking shell) because the CLI process itself
    exits immediately, while the shell lives for the duration of the job.
    """
    target = Path(path) if path else lock_path()
    if stale_after is not None:
        os.environ["HEAVY_LOCK_STALE_S"] = str(float(stale_after))
    wait = float(timeout) if timeout is not None else float(MAX_WAIT_S)
    wait = max(0.0, min(wait, float(MAX_WAIT_S)))
    deadline = time.monotonic() + wait
    token = uuid.uuid4().hex
    info = {
        "name": name,
        "pid": int(owner_pid) if owner_pid else os.getpid(),
        "host": socket.gethostname(),
        "created_at": _now_iso(),
        "created_ts": time.time(),
        "token": token,
        "command": command or " ".join([Path(sys.executable).name, *sys.argv]),
    }
    payload = json.dumps(info, indent=2, sort_keys=True) + "\n"

    while True:
        if _atomic_create(target, payload):
            return _Acquired(info, target)

        state = staleness(target)
        if force:
            print(f"warning: --force reclaiming heavy lock {target}: "
                  f"{describe(state['holder'] or {})}", file=sys.stderr)
            _reclaim(target, state, warn=False)
            continue
        if state["stale"]:
            if _reclaim(target, state):
                continue
        if time.monotonic() >= deadline:
            holder = state.get("holder") or {}
            raise LockError(
                f"heavy lock {target} is held by {describe(holder)} "
                f"[{state.get('reason')}]; refusing to start '{name}'. "
                f"Wait for it to finish (RULES #10: heavy compute runs one at a time), "
                f"or remove the lock only if you are certain the holder is gone.")
        time.sleep(POLL_S)


def release(*, path: Optional[Path] = None, force: bool = False) -> bool:
    """Remove the lock file.  Without ``force`` this ignores ownership."""
    target = Path(path) if path else lock_path()
    info = _read(target)
    if info is None:
        return False
    if not force:
        print(f"release: removing {target} held by {describe(info)}", file=sys.stderr)
    try:
        target.unlink()
    except FileNotFoundError:
        return False
    return True


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(prog="lock.py", description="ops/HEAVY.lock helper")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_status = sub.add_parser("status", help="show the lock state (exit 1 if held)")
    p_status.add_argument("--path", default=None)
    p_status.add_argument("--json", action="store_true")

    p_acq = sub.add_parser("acquire", help="take the lock (exit 1 if held)")
    p_acq.add_argument("--name", required=True)
    p_acq.add_argument("--timeout", type=float, default=0.0)
    p_acq.add_argument("--path", default=None)
    p_acq.add_argument("--force", action="store_true")
    p_acq.add_argument("--pid", type=int, default=None,
                       help="pid to record as holder (default: the invoking shell)")
    p_acq.add_argument("--json", action="store_true")

    p_rel = sub.add_parser("release", help="remove the lock")
    p_rel.add_argument("--path", default=None)
    p_rel.add_argument("--force", action="store_true")
    p_rel.add_argument("--json", action="store_true")

    args = parser.parse_args(argv)
    target = Path(args.path) if args.path else lock_path()

    if args.cmd == "status":
        state = staleness(target)
        if args.json:
            print(json.dumps(state, indent=2, sort_keys=True, default=str))
        elif not state["exists"]:
            print(f"heavy lock free ({target})")
        else:
            print(f"heavy lock HELD ({target}): {describe(state['holder'])} "
                  f"[{state['reason']}]")
        return 0 if not state["exists"] else 1

    if args.cmd == "acquire":
        try:
            handle = acquire(args.name, timeout=args.timeout, path=target,
                             force=args.force,
                             owner_pid=args.pid if args.pid else os.getppid())
        except LockError as exc:
            if args.json:
                print(json.dumps({"acquired": False, "error": str(exc)}, indent=2))
            else:
                print(f"error: {exc}", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps({"acquired": True, "lock": handle.info,
                              "path": str(target)}, indent=2, sort_keys=True))
        else:
            print(f"heavy lock acquired by '{args.name}' ({target}); "
                  f"release with: python 04_experiments/harness/lock.py release")
        return 0

    removed = release(path=target, force=args.force)
    if args.json:
        print(json.dumps({"released": removed, "path": str(target)}, indent=2))
    elif removed:
        print(f"released {target}")
    else:
        print(f"no lock at {target}")
    return 0 if removed else 1


if __name__ == "__main__":
    sys.exit(main())
