## ADDED Requirements

### Requirement: Setup Doctor Reports Local Readiness

The system SHALL provide a local diagnostic command that checks whether the repository checkout contains required Architecture Radar files, directories, workflows, scripts, OpenSpec files, Codex skills, community files, and release documentation.

#### Scenario: Local setup is complete

- **WHEN** `python3 scripts/check-radar-setup.py --skip-github` runs in a complete checkout
- **THEN** it reports no failed checks
- **AND** exits with status `0`

#### Scenario: Required local file is missing

- **WHEN** a required local file is absent
- **THEN** the setup doctor reports a failed check
- **AND** exits with status `1`

### Requirement: Setup Doctor Performs Best-Effort GitHub Checks

The setup doctor SHALL use GitHub CLI metadata when available to check repository configuration without requiring network access for local checks.

#### Scenario: GitHub CLI is unavailable

- **WHEN** GitHub checks are enabled but `gh` cannot provide repository metadata
- **THEN** local checks still run
- **AND** GitHub checks are reported as warnings rather than local setup failures

#### Scenario: GitHub metadata is available

- **WHEN** GitHub metadata is available
- **THEN** the setup doctor checks branch protection, required `validate` status, Actions workflows, `OPENAI_API_KEY` secret metadata, community profile, and `v0.1.0` release/tag state

### Requirement: Setup Doctor Supports Machine-Readable Output

The setup doctor SHALL support JSON output for automation and future CI integration.

#### Scenario: JSON output is requested

- **WHEN** `python3 scripts/check-radar-setup.py --json` runs
- **THEN** it emits an object containing `ok`, `summary`, and `checks`
- **AND** every check includes `id`, `severity`, `message`, and `details`

### Requirement: Setup Doctor Is Diagnostic-Only

The setup doctor SHALL NOT mutate repository files, GitHub settings, secrets, branch protection, releases, workflows, or generated artifacts.

#### Scenario: Remote setup is incomplete

- **WHEN** the setup doctor finds missing GitHub settings
- **THEN** it reports the problem and suggested remediation
- **AND** does not modify remote settings
