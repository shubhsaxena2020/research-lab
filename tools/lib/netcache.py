"""Polite, cached, offline-by-default HTTP for research-lab tools.

Design constraints (see RULES.md 8, 11 and tools/CONTRACTS.md 6):
  * one request per second per host, never more;
  * descriptive User-Agent with a contact address;
  * exponential backoff on 429/5xx/timeouts: 30 s, 60 s, 120 s, then give up;
  * every successful response cached on disk under 01_psit_data/raw/cache/ so a
    second run of a tool costs zero requests;
  * importable, dependency-light: `requests` if present, else urllib;
  * a caller can inject its own fetcher, which is how the unit tests stay offline.

The cache key is a hash of the full URL, so it is stable across runs. Cached bodies are
stored as `<sha256>.json` holding {"url", "fetched_at", "status", "content_type", "body"}.
Bodies are stored as text (these APIs all return JSON or JSON-ish text).
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Callable, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
CACHE_DIR = REPO_ROOT / "01_psit_data" / "raw" / "cache"
CONTACT = "shubh.saxena2020@gmail.com"
USER_AGENT = f"research-lab-citation-checker/1.0 (mailto:{CONTACT})"

DEFAULT_MIN_INTERVAL = 1.0
DEFAULT_BACKOFF = (30, 60, 120)


class FetchError(RuntimeError):
    """Network or HTTP failure that survived the retry ladder."""


def _sha(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:32]


def cache_path(url: str) -> Path:
    return CACHE_DIR / (_sha(url) + ".json")


def read_cache(url: str) -> Optional[dict]:
    p = cache_path(url)
    if not p.exists():
        return None
    try:
        with p.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError):
        return None


def write_cache(url: str, body: str, status: int = 200, content_type: str = "application/json") -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "url": url,
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": status,
        "content_type": content_type,
        "body": body,
    }
    tmp = cache_path(url).with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False)
    os.replace(tmp, cache_path(url))


def _retry_after_seconds(err: "urllib.error.HTTPError") -> Optional[float]:
    """Read Retry-After (seconds or HTTP-date). None when absent/unparsable."""
    try:
        raw = err.headers.get("Retry-After") if err.headers else None
    except Exception:
        return None
    if not raw:
        return None
    raw = raw.strip()
    if raw.isdigit():
        return float(raw)
    try:
        from email.utils import parsedate_to_datetime
        import datetime as _dt

        when = parsedate_to_datetime(raw)
        if when.tzinfo is None:
            when = when.replace(tzinfo=_dt.timezone.utc)
        delta = (when - _dt.datetime.now(_dt.timezone.utc)).total_seconds()
        return max(0.0, delta)
    except Exception:
        return None


class PoliteFetcher:
    """Fetches a URL as text, with per-host rate limiting, retries and disk cache.

    Parameters
    ----------
    min_interval : seconds between requests to the same host (default 1.0).
    backoff      : sleep ladder for 429/5xx/timeouts (default 30/60/120 s).
    max_bytes    : hard cap on a response body, so one bad URL cannot eat RAM.
    sleeper      : injected in tests so the ladder does not actually sleep.
    """

    def __init__(
        self,
        min_interval: float = DEFAULT_MIN_INTERVAL,
        backoff=DEFAULT_BACKOFF,
        max_bytes: int = 8 * 1024 * 1024,
        sleeper: Callable[[float], None] = time.sleep,
        use_cache: bool = True,
        cache_dir: Optional[Path] = None,
        max_retry_after: float = 120.0,
    ):
        self.min_interval = min_interval
        self.backoff = tuple(backoff)
        self.max_bytes = max_bytes
        self.sleeper = sleeper
        self.use_cache = use_cache
        self.cache_dir = Path(cache_dir) if cache_dir else CACHE_DIR
        self.max_retry_after = max_retry_after
        self._last: dict[str, float] = {}
        self.blocked_hosts: dict[str, str] = {}
        self.n_requests = 0
        self.n_cache_hits = 0

    # -- cache ------------------------------------------------------------
    def _cache_path(self, url: str) -> Path:
        return self.cache_dir / (_sha(url) + ".json")

    def _read_cache(self, url: str):
        if not self.use_cache:
            return None
        p = self._cache_path(url)
        if not p.exists():
            return None
        try:
            with p.open("r", encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError):
            return None

    def _write_cache(self, url: str, body: str, status: int) -> None:
        if not self.use_cache:
            return
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "url": url,
            "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "status": status,
            "content_type": "application/json",
            "body": body,
        }
        tmp = self._cache_path(url).with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False)
        os.replace(tmp, self._cache_path(url))

    # -- rate limit -------------------------------------------------------
    def _throttle(self, url: str) -> None:
        host = urllib.parse.urlsplit(url).netloc
        now = time.monotonic()
        last = self._last.get(host)
        if last is not None:
            wait = self.min_interval - (now - last)
            if wait > 0:
                self.sleeper(wait)
        self._last[host] = time.monotonic()

    # -- fetch ------------------------------------------------------------
    def _http_get(self, url: str) -> str:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/json, application/atom+xml, text/plain, */*",
                "Accept-Encoding": "identity",
            },
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read(self.max_bytes + 1)
            if len(raw) > self.max_bytes:
                raise FetchError(f"response larger than {self.max_bytes} bytes: {url}")
            charset = resp.headers.get_content_charset() or "utf-8"
            return raw.decode(charset, errors="replace")

    def get(self, url: str) -> str:
        cached = self._read_cache(url)
        if cached is not None:
            self.n_cache_hits += 1
            return cached["body"]

        host = urllib.parse.urlsplit(url).netloc
        if host in self.blocked_hosts:
            raise FetchError(f"{host} exhausted for this run: {self.blocked_hosts[host]}")

        last_err: Optional[Exception] = None
        attempts = len(self.backoff) + 1
        for attempt in range(attempts):
            self._throttle(url)
            self.n_requests += 1
            try:
                body = self._http_get(url)
                self._write_cache(url, body, 200)
                return body
            except urllib.error.HTTPError as err:
                last_err = err
                # 404/400 are answers, not transient failures: treat as empty body.
                if err.code in (400, 404):
                    return ""
                if err.code == 429 or 500 <= err.code < 600:
                    retry_after = _retry_after_seconds(err)
                    if retry_after is not None and retry_after > self.max_retry_after:
                        # The service has told us not to come back for a long time (OpenAlex
                        # sends Retry-After ~15859s when the IP's credit is gone). Waiting is
                        # not polite, it is pointless: stop using this host for the whole run.
                        self.blocked_hosts[host] = (
                            f"HTTP {err.code}, Retry-After {int(retry_after)}s — skipped for this run"
                        )
                        raise FetchError(self.blocked_hosts[host]) from err
                    if attempt < attempts - 1:
                        self.sleeper(retry_after if retry_after is not None else self.backoff[attempt])
                    continue
                raise FetchError(f"HTTP {err.code} for {url}") from err
            except (urllib.error.URLError, TimeoutError, OSError) as err:
                last_err = err
                if attempt < attempts - 1:
                    self.sleeper(self.backoff[attempt])
                continue
        raise FetchError(f"gave up after {attempts} attempts: {url} ({last_err})")


def make_fetcher(online: bool, **kw) -> Tuple[Callable[[str], str], "PoliteFetcher"]:
    """Return (fetch, fetcher) so the caller can inspect request counters and blocked hosts."""
    pf = PoliteFetcher(**kw)

    if online:
        return pf.get, pf

    def cached_only(url: str) -> str:
        hit = pf._read_cache(url)
        if hit is None:
            raise FetchError(f"offline mode: no cached response for {url}")
        pf.n_cache_hits += 1
        return hit["body"]

    return cached_only, pf


def default_fetcher(online: bool, **kw) -> Callable[[str], str]:
    """Return a `url -> body` callable.

    When `online` is False the fetcher serves *only* from cache and raises FetchError on a
    miss. That is what makes `--offline` runs deterministic and testable.
    """
    return make_fetcher(online, **kw)[0]


def fetch_json(fetch: Callable[[str], str], url: str):
    """Fetch and parse JSON. Empty body -> None. Raises FetchError on unparsable body."""
    body = fetch(url)
    if not body or not body.strip():
        return None
    try:
        return json.loads(body)
    except json.JSONDecodeError as err:
        raise FetchError(f"non-JSON response from {url}: {body[:200]!r}") from err


def normalize_arxiv_id(raw: str) -> Optional[str]:
    """'arXiv:1706.03762v2' -> '1706.03762'. Handles old-style 'cs/0112017' too."""
    if not raw:
        return None
    s = raw.strip()
    s = re.sub(r"^https?://(www\.)?arxiv\.org/(abs|pdf)/", "", s)
    s = re.sub(r"^arxiv:\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\.pdf$", "", s)
    s = re.sub(r"v\d+$", "", s)
    return s or None


def normalize_doi(raw: str) -> Optional[str]:
    """Strip URL/doi: prefixes, lowercase, keep the '10.' prefix."""
    if not raw:
        return None
    s = raw.strip()
    s = re.sub(r"^https?://(dx\.)?doi\.org/", "", s, flags=re.IGNORECASE)
    s = re.sub(r"^doi:\s*", "", s, flags=re.IGNORECASE)
    s = s.strip().lower()
    if not s.startswith("10."):
        return None
    return s
