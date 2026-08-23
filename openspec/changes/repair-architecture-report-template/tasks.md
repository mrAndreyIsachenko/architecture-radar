## Implementation

- [x] Add a deterministic report-structure repair script for Architecture Radar reports.
- [x] Wire the repair step into `scripts/run-codex-radar.sh` before validation.
- [x] Strengthen the CI prompt with exact report headings and Candidate Ledger columns.
- [x] Add unit tests for heading alias repair, missing section placeholders, and diagnostic Candidate Ledger creation.

## Validation

- [x] Run targeted report repair tests.
- [x] Run radar validator tests.
- [x] Run full unit test suite.
- [x] Run `openspec validate --all --strict --no-interactive`.
- [x] Run `git diff --check`.
