## MODIFIED Requirements

### Requirement: Opportunity Radar Runs Weekly And Manually

Opportunity Radar SHALL support a weekly scheduled research cadence with
catch-up-safe scheduled wake-ups while preserving manual dispatch for
event-driven demand checks.

#### Scenario: Weekly workflow trigger is configured

- **WHEN** the Opportunity Radar workflow is configured
- **THEN** it includes scheduled wake-ups that can retry the weekly due date
- **AND** it includes a deterministic cadence gate before expensive Codex steps
- **AND** the cadence gate keeps scheduled research to at most one generated run
  per due-date report while that report or a generated branch exists
- **AND** it includes `workflow_dispatch`

#### Scenario: Missed Tuesday wake-up can catch up

- **WHEN** the Tuesday scheduled wake-up does not produce a workflow run
- **AND** no `opportunity-reports/<due-date>.md` exists
- **AND** no `opportunity-radar/<due-date>-*` generated branch exists
- **THEN** a later scheduled wake-up inside the catch-up window runs the
  Opportunity Radar for the Tuesday due date

#### Scenario: Manual run remains available

- **WHEN** a user wants to validate a specific demand hypothesis outside the weekly cadence
- **THEN** the workflow can be started manually with `workflow_dispatch`
