## ADDED Requirements

### Requirement: Validation Backlog Types Are Canonicalized Before Strict Validation

Architecture Radar SHALL repair known descriptive or combined validation type
phrases into a single canonical validation backlog enum before strict
validation.

#### Scenario: Generated backlog type combines known validation dimensions

- **WHEN** a generated Architecture Radar artifact writes a recoverable
  descriptive validation type such as `runtime validation and failure-injection`
- **THEN** the repair step canonicalizes it to one allowed primary
  `validation_type`
- **AND** strict validation validates the canonical value

#### Scenario: Generated backlog type is unknown

- **WHEN** a generated Architecture Radar artifact writes a validation type that
  cannot be mapped to the allowed enum
- **THEN** the repair step leaves it unchanged
- **AND** strict validation rejects it
