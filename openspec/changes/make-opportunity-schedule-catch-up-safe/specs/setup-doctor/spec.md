## MODIFIED Requirements

### Requirement: Setup Doctor Checks Opportunity Radar Weekly Schedule

Setup Doctor SHALL verify that Opportunity Radar supports manual dispatch,
scheduled wake-ups, and a deterministic catch-up gate for the weekly research
cadence.

#### Scenario: Opportunity workflow is configured

- **WHEN** local setup checks inspect `.github/workflows/opportunity-radar.yml`
- **THEN** the workflow contains `workflow_dispatch:`
- **AND** the workflow contains `schedule:`
- **AND** the workflow contains at least one daily scheduled wake-up
- **AND** the workflow invokes `scripts/check-opportunity-radar-cadence.sh`
