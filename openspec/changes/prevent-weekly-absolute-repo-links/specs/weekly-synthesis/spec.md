## ADDED Requirements

### Requirement: Weekly Synthesis Uses Repository-Relative Artifact Paths

Weekly synthesis SHALL reference repository artifacts with repository-relative
paths rather than absolute runner, workspace, or local filesystem paths.

#### Scenario: Weekly report references repository artifacts

- **WHEN** a weekly synthesis report references local repository artifacts
- **THEN** the references use paths relative to the repository root
- **AND** the report does not contain GitHub Actions workspace paths
- **AND** the report does not contain local machine absolute paths

#### Scenario: Weekly report validation runs

- **WHEN** a weekly synthesis report contains an absolute runner, workspace, or
  local filesystem path
- **THEN** validation fails before the pull request can be merged
