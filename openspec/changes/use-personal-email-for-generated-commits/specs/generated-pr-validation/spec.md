## MODIFIED Requirements

### Requirement: Generated Pull Requests Carry Governance Metadata

Generated radar pull requests SHALL include the governance metadata required by
the repository pull request validator. Generated radar artifact commits SHALL use
the configured generated-commit Git identity.

#### Scenario: Generated publisher creates pull request body

- **WHEN** an Architecture Radar or Opportunity Radar publisher writes a pull request body
- **THEN** the body includes `User request:`
- **AND** the body includes `Scope confirmed: yes`
- **AND** the body includes `Autonomous follow-up: no`

#### Scenario: Generated research artifact does not require OpenSpec evidence

- **WHEN** a generated pull request only stages allowed generated research artifacts
- **THEN** the body records that OpenSpec evidence is not required for generated research artifacts

#### Scenario: Generated workflow prepares an artifact branch

- **WHEN** an Architecture Radar, Opportunity Radar, or Weekly Synthesis workflow prepares a generated artifact branch
- **THEN** the local Git `user.name` defaults to `Andrey Isachenko`
- **AND** the local Git `user.email` defaults to `mr.andrey.isachenko@gmail.com`
- **AND** the name and email can be overridden by workflow environment variables before the commit is created
