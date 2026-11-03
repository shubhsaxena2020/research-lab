# PROTOCOL — pointer

The binding pre-registration for C1 is `04_experiments/PREREGISTRATION.md`, frozen with a sha256 in
`04_experiments/PREREGISTRATION.sha256`. This file exists only because two names were used for the same
document (PROMPT.md says `PROTOCOL.md`, HEAD-REVIEW.md condition 3 says `PREREGISTRATION.md`); there is
one document, and `tools/tests/test_prereg_frozen.py` checks the hash still matches its contents.
