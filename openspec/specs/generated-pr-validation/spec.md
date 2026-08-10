# generated-pr-validation Specification

## Purpose
Generated pull requests published by scheduled or manual radar workflows need a reliable way to satisfy the protected `main` branch's required `validate` check. This capability records successful deterministic generator validation on the generated PR head without relying on manual empty commits or on `pull_request` workflows that GitHub suppresses for `GITHUB_TOKEN`-authored PRs.
## Requirements
### Requirement: Generated PRs Receive Validate Check Markers

Generated radar pull requests SHALL receive the required `validate` check without requiring manual empty commits.

#### Scenario: Generator workflow succeeds and opens a PR

- **WHEN** an Architecture Radar, Opportunity Radar, or Weekly Synthesis workflow completes successfully
- **AND** an open pull request exists whose head branch matches the generator workflow and run number
- **THEN** the system creates a completed successful check-run named `validate` on the PR head SHA

#### Scenario: Generator workflow produces no PR

- **WHEN** a generator workflow completes successfully but no matching open generated PR exists
- **THEN** the marker workflow exits successfully without creating a check-run

### Requirement: Failed Generator Runs Are Not Marked Validated

The system SHALL NOT create validate markers for failed or incomplete generator workflows.

#### Scenario: Generator workflow fails

- **WHEN** an Architecture Radar, Opportunity Radar, or Weekly Synthesis workflow completes with a non-success conclusion
- **THEN** no generated PR validate marker is created

### Requirement: Human PR Validation Remains Unchanged

Human-authored pull requests SHALL continue to use the normal pull request validation workflow.

#### Scenario: A normal pull request is opened or updated

- **WHEN** a pull request is not created by a generated radar workflow branch
- **THEN** validation is provided by `radar-validation.yml` through the existing `pull_request` trigger

### Requirement: Generated Pull Requests Carry Governance Metadata

Generated radar pull requests SHALL include the governance metadata required by
the repository pull request validator.

#### Scenario: Generated publisher creates pull request body

- **WHEN** an Architecture Radar or Opportunity Radar publisher writes a pull request body
- **THEN** the body includes `User request:`
- **AND** the body includes `Scope confirmed: yes`
- **AND** the body includes `Autonomous follow-up: no`

#### Scenario: Generated research artifact does not require OpenSpec evidence

- **WHEN** a generated pull request only stages allowed generated research artifacts
- **THEN** the body records that OpenSpec evidence is not required for generated research artifacts
