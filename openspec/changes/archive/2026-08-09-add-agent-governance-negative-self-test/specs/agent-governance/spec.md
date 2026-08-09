## ADDED Requirements

### Requirement: Governance Enforcement Has Negative Self-Tests

The required `validate` check SHALL include deterministic negative self-tests
that prove invalid governance scenarios are rejected.

#### Scenario: Negative fixture is rejected

- **WHEN** the self-test evaluates a fixture with invalid PR metadata or a governed behavior change without OpenSpec evidence
- **THEN** the validator returns at least one error
- **AND** the error output contains the fixture's expected error substring

#### Scenario: Negative fixture unexpectedly passes

- **WHEN** a negative fixture produces no validation errors
- **THEN** the self-test fails
