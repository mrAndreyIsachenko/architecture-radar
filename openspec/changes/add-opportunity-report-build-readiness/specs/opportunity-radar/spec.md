## MODIFIED Requirements

### Requirement: Opportunity Reports Preserve Signal Ledgers

Opportunity Radar reports SHALL include a ledger of reviewed public signals and opportunity candidates, including rejected and deferred items, and SHALL expose build-readiness metadata for opportunity decisions.

#### Scenario: A run reviews public signals

- **WHEN** the run completes
- **THEN** the report lists reviewed signals with source, URL, topic family, evidence label, decision, and rejection or deferral reason
- **AND** the report includes a `Build Readiness` table with paid wedge, distribution channel, private data barrier, OSS commoditization risk, product shape, pricing hypothesis, do-not-build-until condition, and build decision

#### Scenario: Report marks an opportunity buildable

- **WHEN** a report row marks an opportunity as selected or selected-for-build
- **THEN** the paid wedge is not unclear
- **AND** the private data barrier is `none` or `public-only`
