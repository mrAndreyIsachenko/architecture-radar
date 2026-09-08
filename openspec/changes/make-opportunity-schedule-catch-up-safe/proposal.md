## Why

The 2026-09-08 Tuesday Opportunity Radar report did not appear because GitHub
Actions never created a scheduled `Opportunity Radar` run for that date. The
workflow was active and the cron expression was valid, but a single weekly
scheduled trigger has no retry path when GitHub silently delays or drops a
scheduled event.

## What Changes

- Replace the single expensive weekly trigger with catch-up-safe scheduled
  wake-ups.
- Add a deterministic Opportunity Radar cadence gate that runs Codex only when
  the weekly due-date report is missing and no generated branch for that due
  date already exists.
- Keep manual dispatch deliberate and immediate.
- Update local setup checks, validation wiring, docs, and tests so the catch-up
  contract is visible and enforced.

## Capabilities

### New Capabilities

### Modified Capabilities

- `opportunity-radar`: Scheduled runs are catch-up safe and duplicate guarded.
- `setup-doctor`: Local checks verify the Opportunity Radar catch-up gate and
  scheduled wake-up configuration.

## Impact

- Affects `.github/workflows/opportunity-radar.yml`.
- Adds `scripts/check-opportunity-radar-cadence.sh`.
- Updates setup doctor checks, CI script syntax validation, docs, and unit
  tests.
- Does not change Opportunity Radar research criteria, output schema, or
  generated artifact semantics.
