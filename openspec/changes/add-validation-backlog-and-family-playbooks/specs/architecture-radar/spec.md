## ADDED Requirements

### Requirement: Architecture Radar Uses Family Playbooks
Architecture Radar SHALL use file-backed family playbooks to steer discovery, selection, rejection, and validation expectations for topic families that require domain-specific evidence standards.

#### Scenario: Research run starts with family playbooks
- **WHEN** an Architecture Radar research run starts
- **THEN** it reads applicable playbooks under `docs/family-playbooks/`
- **AND** it treats those playbooks as operating guidance subordinate to `interests.md` and `docs/research-scope.md`

#### Scenario: Under-covered family is reported
- **WHEN** a topic family has weak candidate supply or no selected repository
- **THEN** the generated report records the family-specific gap using the applicable playbook's mechanisms and evidence expectations

### Requirement: Satellites And Space Systems Are A Topic Family
Architecture Radar SHALL include `satellites-space-systems` as a first-class topic family for candidate accounting and source-backed mechanism discovery.

#### Scenario: Satellite candidate is triaged
- **WHEN** a candidate concerns satellite operations, ground stations, space-domain awareness, RF/geospatial processing, delayed connectivity, command/telemetry loops, or constellation coordination
- **THEN** the candidate ledger may classify it as `satellites-space-systems`
- **AND** selection still requires an inspectable source-backed mechanism tied to `interests.md`

#### Scenario: Satellite family has no strong candidate
- **WHEN** a run searches the satellites/space systems family but no candidate clears the threshold
- **THEN** the report records the family gap instead of selecting a weak repository

### Requirement: Runtime Evidence Gaps Create Validation Backlog Items
Architecture Radar SHALL preserve a persistent validation backlog for selected mechanisms that require runtime, failure-injection, replay, restart, reconnect, SITL, fleet, or operational validation before adoption.

#### Scenario: Selected repository has runtime validation gap
- **WHEN** a generated report selects a repository and records an unresolved evidence gap requiring runtime or failure validation
- **THEN** the report includes a `Validation Backlog Updates` section
- **AND** the report references an item in `experiments/failure-injection-backlog.yml`
- **AND** that backlog item names the source report, source repository, topic family, mechanism, evidence gap, validation type, proposed validation, success condition, priority, status, creation date, and last-updated date

#### Scenario: No runtime validation gap exists
- **WHEN** a generated report has no selected mechanism requiring runtime, failure-injection, replay, restart, reconnect, SITL, fleet, or operational validation
- **THEN** the `Validation Backlog Updates` section explicitly states that no backlog update was required

#### Scenario: Backlog reference is invalid
- **WHEN** a changed Architecture Radar report references a validation backlog item
- **THEN** validation fails unless the referenced item exists in `experiments/failure-injection-backlog.yml` and matches the report's repository and topic family
