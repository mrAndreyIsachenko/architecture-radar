# Validation Evidence

Date: 2026-09-27. Scope: local implementation of `track-radar-review-delivery`.

## Local Gates

- `python3 -m unittest discover -s tests`: 209 passed.
- `python3 -m py_compile scripts/radar-review-delivery.py scripts/radar-pr-review.py scripts/radar-pr-review-status.py scripts/summarize-radar-pr.py scripts/summarize-opportunity-pr.py`: passed.
- `openspec validate --all --strict --no-interactive`: 28 passed, 0 failed.
- `python3 scripts/validate-agent-governance.py`: passed for the local diff;
  there is no new PR body to validate.
- `python3 scripts/validate-radar-state.py`: passed.
- `python3 scripts/validate-opportunity-radar-state.py`: passed.
- `python3 scripts/validate-weekly-synthesis-state.py`: passed.
- `git diff --check`: passed.

Initial regression runs exposed missing SHA fields in old fixtures, changed
no-PR waiting output, and a concurrent initialization race. Fixtures and status
compatibility were corrected. A POSIX lock now serializes first creation and
acknowledgement, with SQLite enforcing the transaction and unique identity.
The final suite includes both concurrent threads and six concurrent CLI processes.
Expected negative-fixture validator messages in unittest output are not failures.

## Delivery Fixture

`tests/test_review_delivery.py` exercises both real summary parsers with mocked
GitHub responses: two pending PRs, markdown rendering without state creation,
another invocation repeating both reviews, explicit fixture-only acknowledgements
of a simulated visible prior reply, suppression, and reappearance after a new SHA.
Separate subprocess tests verify persistent receipts across process restarts and
idempotent acknowledgement. Tests also cover destination/repository isolation,
old SHA acknowledgements, incomplete CLI fields, missing scope, moving heads,
corrupt records/schema/files, failed writes, one failed summary with the other
family still included, CI blockers, failed runs, and schedule waiting.

These are caller-attestation tests, not a live chat transport test. No actual
conversation delivery receipt was fabricated.

## Read-Only GitHub Check

Executed the helper for both families with `--format markdown --include-failed-log`,
the current conversation scope, and an isolated nonexistent `/tmp` state path.
It returned `no_pr`; the state directory still did not exist afterward.
An independent `gh pr list --state all` confirmed that PRs #91 and #92 are now
merged, so no open two-family queue was available for live replay acceptance.

Latest workflow URLs returned by the helper:

- Architecture: https://github.com/mrAndreyIsachenko/architecture-radar/actions/runs/36233641822
- Opportunity: https://github.com/mrAndreyIsachenko/architecture-radar/actions/runs/36250515986

Direct read-only summary calls successfully exercised immutable report fetches
and before/after metadata checks for the merged PRs:

- #91: `0e9a7bcae9f65d16e2bdae234e1812e7b3ce3f54`.
- #92: `2e6da2038f8052a65e5a9d30647c5c812c45d180`.

## Acceptance Boundary

Implementation and deterministic delivery-state acceptance are complete. Code
alone cannot confirm that a substantive reply is visible in the intended chat.
The heartbeat caller must adopt the documented protocol, inspect a real prior
reply, and acknowledge only its exact reviewed revision and message reference.
If acknowledgement cannot follow a final reply in the same invocation, it happens
on the next invocation after that reply is visible. No extra user confirmation
is needed per review.

Active automation settings, research schedules, synthetic CI verdict logic,
GitHub PR state, and research artifacts were not changed. No commit, push, new
branch, PR, or OpenSpec archive was performed. Publishing and authorized caller
adoption, followed by a live visible-reply/receipt check, remain outside this
local implementation acceptance; this is not an end-to-end delivery guarantee.
