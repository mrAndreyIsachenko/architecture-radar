## Why

Opportunity Radar is currently manual-only. That was useful for early safety,
but the workflow is now stable enough for a low-frequency automatic cadence.

Demand signals move more slowly than repository architecture changes, so weekly
cadence is a better default than every three days. Manual dispatch remains
available for event-driven checks.

## What Changes

Enable a weekly scheduled Opportunity Radar run:

- Tuesday at `05:30 UTC`, which is `08:30 Europe/Moscow`;
- keep `workflow_dispatch`;
- keep generated PR publication and validation behavior;
- update setup doctor checks and docs to reflect weekly scheduling.

## Capabilities

### Updated Capabilities

- `opportunity-radar`: weekly schedule plus manual dispatch.
- `setup-doctor`: validates the Opportunity Radar schedule requirement.

## Impact

- Updates `.github/workflows/opportunity-radar.yml`.
- Updates setup doctor required workflow checks.
- Updates docs that currently describe Opportunity Radar as manual-only.
- Adds OpenSpec evidence and archives it in the same PR.
