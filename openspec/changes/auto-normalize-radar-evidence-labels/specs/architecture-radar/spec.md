## MODIFIED Requirements

### Requirement: Repository Reviews Are Evidence-Labeled

Generated reports and repository reviews SHALL distinguish source-verified facts, test-verified behavior, maintainer claims, interpretation, and hypotheses, and SHALL normalize deterministic E1 over-labeling before strict validation.

#### Scenario: Source evidence path is documentation

- **WHEN** a generated artifact labels a README, documentation, changelog, NEWS, release, issue, ADR, or spec path as `E1 source verified`
- **AND** the evidence line does not mix implementation evidence with weaker evidence paths
- **THEN** the workflow normalizes the label to `E3 maintainer stated` before validation

#### Scenario: Source evidence path is a test

- **WHEN** a generated artifact labels a test path as `E1 source verified`
- **AND** the evidence line does not mix implementation evidence with weaker evidence paths
- **THEN** the workflow normalizes the label to `E2 test verified` before validation

#### Scenario: Evidence line is ambiguous

- **WHEN** a generated artifact mixes implementation evidence with test, documentation, release, ADR, or spec evidence on the same `E1 source verified` line
- **THEN** the normalizer leaves the line unchanged
- **AND** strict validation fails with the expected evidence label
