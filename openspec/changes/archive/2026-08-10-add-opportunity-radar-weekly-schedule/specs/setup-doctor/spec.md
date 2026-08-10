## ADDED Requirements

### Requirement: Setup Doctor Checks Opportunity Radar Weekly Schedule

Setup Doctor SHALL verify that Opportunity Radar supports both manual dispatch
and the configured weekly schedule.

#### Scenario: Opportunity workflow is configured

- **WHEN** local setup checks inspect `.github/workflows/opportunity-radar.yml`
- **THEN** the workflow contains `workflow_dispatch:`
- **AND** the workflow contains `schedule:`
- **AND** the workflow contains the Tuesday `05:30 UTC` cron expression
