# Task verify-install — Tectonic 0.17.0 install record (R3-7b)

Verification (read-only) of the install record, `.gitignore` change, and ENGINE.md sections.

## Checks

1. `tools/tectonic/tectonic.exe --version` → `Tectonic 0.17.0` ✓ (expected `Tectonic 0.17.0`).
2. SHA-256 of `tools/tectonic/tectonic.zip` → `f61ce51f0b0ade1015b7de7ef368541c5424e9756ecbd0d7af97d6d48030845f` ✓ (matches expected).
3. `.gitignore` contains a line `tools/tectonic/` ✓.
4. `ENGINE.md` contains both `## Current install` and `## Historical` sections ✓.

## Result

PASS — all four checks satisfied; no changes made.