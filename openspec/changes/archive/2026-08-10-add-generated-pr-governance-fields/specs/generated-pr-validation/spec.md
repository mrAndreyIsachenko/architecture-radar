## ADDED Requirements

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
