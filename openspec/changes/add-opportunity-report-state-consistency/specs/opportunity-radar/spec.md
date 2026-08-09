## MODIFIED Requirements

### Requirement: Opportunity Reports Preserve Signal Ledgers

Opportunity Radar reports SHALL include a ledger of reviewed public signals and opportunity candidates, including rejected and deferred items, SHALL expose build-readiness metadata for opportunity decisions, and SHALL keep report build-readiness rows consistent with `opportunities.json`.

#### Scenario: A run reviews public signals

- **WHEN** the run completes
- **THEN** the report lists reviewed signals with source, URL, topic family, evidence label, decision, and rejection or deferral reason
- **AND** the report includes a `Build Readiness` table with paid wedge, distribution channel, private data barrier, OSS commoditization risk, product shape, pricing hypothesis, do-not-build-until condition, and build decision

#### Scenario: Report marks an opportunity buildable

- **WHEN** a report row marks an opportunity as selected or selected-for-build
- **THEN** the paid wedge is not unclear
- **AND** the private data barrier is `none` or `public-only`

#### Scenario: Report build-readiness row is validated

- **WHEN** a changed Opportunity Radar report contains a `Build Readiness` row
- **THEN** the row matches an `opportunities.json` entry by title or id
- **AND** the row's build decision matches the entry stage
- **AND** the row's build-readiness fields match the corresponding state fields

### Requirement: Opportunity State Preserves Build Readiness

Opportunity Radar SHALL keep build-readiness metadata comparable across selected, deferred, and watchlisted opportunities, and SHALL keep each entry's stage consistent with the array that contains it.

#### Scenario: Opportunities state is updated

- **WHEN** an entry is written under `selected`, `deferred`, or `watchlisted`
- **THEN** the entry includes `paid_wedge`, `distribution_channel`, `private_data_barrier`, `oss_commoditization_risk`, `product_shape`, `pricing_hypothesis`, and `do_not_build_until`

#### Scenario: State entry declares a stage

- **WHEN** an entry is stored under `selected`, `deferred`, or `watchlisted`
- **THEN** its `stage` value matches the containing array's allowed stage family
