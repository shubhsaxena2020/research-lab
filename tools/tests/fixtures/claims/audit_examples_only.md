# CLAIMS AUDIT — fixture: example rows only (all EX- rows must be skipped, not judged)

Every row here is a worked example and deliberately broken (missing evidence file, verified=NO).
A correct validator skips them and only reports the draft's uncovered claim.

Draft: `tools/tests/fixtures/claims/draft_min/paper.md`

| claim_id | claim | section | evidence_file | evidence_key | command | result_value | verified | limitation | reviewer |
|---|---|---|---|---|---|---|---|---|---|
| EX-001 | "Example row — our method halves the error rate." | Abstract | tools/tests/fixtures/claims/results/does_not_exist.json | accuracy | echo "not a real command" | 0.5 | NO | example only | — |
| EX-002 | "Example row — see the template for how a real row is written." | Introduction | tools/tests/fixtures/claims/results/main_ours.json | no_such_key | echo "not a real command" | 0.1 | MAYBE | example only | — |
