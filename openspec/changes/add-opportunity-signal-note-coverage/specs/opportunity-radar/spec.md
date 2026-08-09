## MODIFIED Requirements

### Requirement: Opportunity Reports Preserve Signal Ledgers

Opportunity Radar reports SHALL include a ledger of reviewed public signals and opportunity candidates, including rejected and deferred items, SHALL expose build-readiness metadata for opportunity decisions, SHALL keep report build-readiness rows consistent with `opportunities.json`, and SHALL keep report ledger URLs covered by durable signal notes.

#### Scenario: A run reviews public signals

- **WHEN** the run completes
- **THEN** the report lists reviewed signals with source, URL, topic family, evidence label, decision, and rejection or deferral reason
- **AND** the report includes a `Build Readiness` table with paid wedge, distribution channel, private data barrier, OSS commoditization risk, product shape, pricing hypothesis, do-not-build-until condition, and build decision
- **AND** the report ledger URLs appear in date-prefixed signal notes under `signals/`

#### Scenario: Report marks an opportunity buildable

- **WHEN** a report row marks an opportunity as selected or selected-for-build
- **THEN** the paid wedge is not unclear
- **AND** the private data barrier is `none` or `public-only`

#### Scenario: Report build-readiness row is validated

- **WHEN** a changed Opportunity Radar report contains a `Build Readiness` row
- **THEN** the row matches an `opportunities.json` entry by title or id
- **AND** the row's build decision matches the entry stage
- **AND** the row's build-readiness fields match the corresponding state fields

### Requirement: Opportunity Radar Uses Separate Artifacts

Opportunity Radar SHALL store its configuration, reports, records, signals, state, and validation separately from Architecture Radar repository-review artifacts, and SHALL keep signal notes reviewable enough to support future evidence revision.

#### Scenario: Opportunity report is generated

- **WHEN** Opportunity Radar produces a report
- **THEN** the report is written under `opportunity-reports/`
- **AND** selected opportunity records are written under `opportunities/`
- **AND** raw or normalized signal records are written under `signals/`
- **AND** Architecture Radar files under `reports/`, `repositories/`, `patterns/`, and `radar.json` are not used for opportunity output

#### Scenario: Signal note is written

- **WHEN** a signal note is created or updated under `signals/`
- **THEN** it includes source URL, date or date range, topic family, signal type, market evidence label, and concise notes
