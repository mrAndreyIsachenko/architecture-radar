## Implementation

- [x] Add Opportunity Radar scheduled wake-up/catch-up spec deltas.
- [x] Add `scripts/check-opportunity-radar-cadence.sh`.
- [x] Wire the cadence gate into `opportunity-radar.yml`.
- [x] Update setup doctor and CI syntax checks for the new gate.
- [x] Update PR review status handling for missed scheduled runs after a grace window.
- [x] Update docs to describe catch-up-safe scheduling.

## Validation

- [x] Add unit tests for Opportunity Radar cadence gating.
- [x] Update existing setup doctor and PR review tests.
- [x] Run targeted unit tests.
- [x] Run `openspec validate --all --strict --no-interactive`.
- [x] Run `git diff --check`.
