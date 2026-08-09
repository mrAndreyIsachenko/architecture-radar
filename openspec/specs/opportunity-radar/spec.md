# opportunity-radar Specification

## Purpose

Opportunity Radar maintains a separate, reviewable library of public demand signals and testable opportunity hypotheses. It complements Architecture Radar without mixing market artifacts into repository-review artifacts.

## Requirements
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

### Requirement: Opportunity Evidence Uses Market-Specific Labels

Opportunity Radar SHALL distinguish paid demand, repeated pain, competitor proof, workaround evidence, interpretation, and hypothesis.

#### Scenario: A demand claim is made

- **WHEN** a selected opportunity claims that demand exists
- **THEN** the claim includes at least one evidence label from `M1 paid demand`, `M2 repeated pain`, `M3 competitor proof`, or `M4 workaround evidence`

#### Scenario: A claim is speculative

- **WHEN** evidence is insufficient to prove demand
- **THEN** the claim is labeled `H hypothesis` or explicitly rejected/deferred

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

### Requirement: Selected Opportunities End In Testable Offers

Every selected opportunity SHALL include a concrete next test that can be executed manually without building a large product first, plus build-readiness fields that determine whether more implementation is justified.

#### Scenario: Opportunity clears selection threshold

- **WHEN** an opportunity is selected
- **THEN** it includes the observed signal, repeated pain, likely user or buyer, current workaround or money signal, proposed offer, success threshold, falsification threshold, and evidence gaps
- **AND** it records paid wedge, distribution channel, private data barrier, OSS commoditization risk, product shape, pricing hypothesis, and do-not-build-until condition

### Requirement: Opportunity Radar Starts Manual-Only

Opportunity Radar SHALL start as a manual workflow before any recurring schedule is enabled.

#### Scenario: Workflow is added

- **WHEN** the first Opportunity Radar workflow is implemented
- **THEN** it supports `workflow_dispatch`
- **AND** it does not include a scheduled trigger

### Requirement: Opportunity State Preserves Build Readiness

Opportunity Radar SHALL keep build-readiness metadata comparable across selected, deferred, and watchlisted opportunities, and SHALL keep each entry's stage consistent with the array that contains it.

#### Scenario: Opportunities state is updated

- **WHEN** an entry is written under `selected`, `deferred`, or `watchlisted`
- **THEN** the entry includes `paid_wedge`, `distribution_channel`, `private_data_barrier`, `oss_commoditization_risk`, `product_shape`, `pricing_hypothesis`, and `do_not_build_until`

#### Scenario: State entry declares a stage

- **WHEN** an entry is stored under `selected`, `deferred`, or `watchlisted`
- **THEN** its `stage` value matches the containing array's allowed stage family

### Requirement: Unclear Paid Wedges Stay Watchlisted

Opportunity Radar SHALL NOT mark opportunities as selected for build when the paid wedge is unclear or useful validation requires private code or private data.

#### Scenario: Paid wedge is unclear

- **WHEN** an opportunity does not identify what a buyer concretely pays for
- **THEN** it is kept in `watchlisted`
- **AND** `do_not_build_until` names the evidence required before further build work

#### Scenario: Private data is required

- **WHEN** an opportunity requires access to private code or private data before the next useful validation
- **THEN** it is kept in `watchlisted`
- **AND** it is not marked `selected-for-build`
