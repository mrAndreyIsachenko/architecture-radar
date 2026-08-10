## ADDED Requirements

### Requirement: Opportunity Radar Runs Weekly And Manually

Opportunity Radar SHALL support a weekly scheduled run while preserving manual
dispatch for event-driven demand checks.

#### Scenario: Weekly workflow trigger is configured

- **WHEN** the Opportunity Radar workflow is configured
- **THEN** it includes a scheduled trigger for Tuesday at `05:30 UTC`
- **AND** it includes `workflow_dispatch`

#### Scenario: Manual run remains available

- **WHEN** a user wants to validate a specific demand hypothesis outside the weekly cadence
- **THEN** the workflow can be started manually with `workflow_dispatch`

## REMOVED Requirements

### Requirement: Opportunity Radar Starts Manual-Only

Opportunity Radar SHALL start as a manual workflow before any recurring schedule is enabled.

#### Scenario: Workflow is added

- **WHEN** the first Opportunity Radar workflow is implemented
- **THEN** it supports `workflow_dispatch`
- **AND** it does not include a scheduled trigger
