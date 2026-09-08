## Overview

GitHub Actions `schedule` is best-effort. A single weekly cron can be delayed or
missed without producing a failed run. The workflow should therefore separate
cheap wake-up frequency from expensive Codex research frequency.

## Workflow Design

Configure `opportunity-radar.yml` with multiple scheduled wake-ups:

- daily 05:30 UTC;
- daily 08:30 UTC;
- daily 11:30 UTC.

Each wake-up runs checkout plus a shell cadence gate. The expensive Node/Codex,
validation, and publish steps run only when the gate outputs
`should_run=true`.

## Cadence Gate

`scripts/check-opportunity-radar-cadence.sh` computes the weekly Opportunity
Radar due date as Tuesday in `Europe/Moscow`.

For scheduled events:

- run only during the configured catch-up window starting on the due Tuesday;
- use the due Tuesday as `OPPORTUNITY_RADAR_RUN_DATE`, even when catch-up happens
  later in the week;
- skip if `opportunity-reports/<due-date>.md` already exists on `main`;
- skip if a remote branch matching `opportunity-radar/<due-date>-*` already
  exists, which prevents duplicate generated PRs while the first PR is open.

For manual dispatch:

- always run;
- use the supplied `OPPORTUNITY_RADAR_DATE` when present;
- otherwise use the current `Europe/Moscow` date.

## Review Helper

The heartbeat helper should stop treating a missing due scheduled run as
indefinite waiting after a bounded grace window. Once the grace window passes,
it should surface a missed schedule as an actionable status so the user can run
or fix the workflow instead of being told to wait.

## Non-Goals

- Do not change the Opportunity Radar prompt or commercial filter.
- Do not increase expensive weekly research frequency.
- Do not auto-merge generated PRs.
- Do not create a paid API polling service outside GitHub Actions.
