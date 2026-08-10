## ADDED Requirements

### Requirement: Weekly Synthesis Pull Requests Carry Governance Metadata

Weekly Synthesis generated pull requests SHALL include the governance metadata
required by the repository pull request validator.

#### Scenario: Weekly synthesis publisher creates pull request body

- **WHEN** the Weekly Synthesis publisher writes a pull request body
- **THEN** the body includes `User request:`
- **AND** the body includes `Scope confirmed: yes`
- **AND** the body includes `Autonomous follow-up: no`
