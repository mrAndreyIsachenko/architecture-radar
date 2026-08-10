## MODIFIED Requirements

### Requirement: Opportunity Reports Preserve Signal Ledgers

Opportunity Radar reports SHALL include a ledger of reviewed public signals and opportunity candidates, including rejected and deferred items, SHALL expose build-readiness and money-readiness metadata for opportunity decisions, SHALL keep report readiness rows consistent with `opportunities.json`, and SHALL keep report ledger URLs covered by durable signal notes.

#### Scenario: A run reviews public signals

- **WHEN** the run completes
- **THEN** the report lists reviewed signals with source, URL, topic family, evidence label, decision, and rejection or deferral reason
- **AND** the report includes a `Build Readiness` table with paid wedge, distribution channel, private data barrier, OSS commoditization risk, product shape, pricing hypothesis, do-not-build-until condition, and build decision
- **AND** the report includes a `Money Readiness` table with pain, spend, reachability, timing, buildability, buyer, existing spend, paid experiment, source classes, and stage
- **AND** the report ledger URLs appear in date-prefixed signal notes under `signals/`

#### Scenario: Report marks an opportunity buildable

- **WHEN** a report row marks an opportunity as selected-for-build
- **THEN** the paid wedge is not unclear
- **AND** the private data barrier is `none` or `public-only`
- **AND** spend score is at least 3
- **AND** reachability score is at least 3
- **AND** timing score is at least 2
- **AND** buildability score is at least 3
- **AND** the paid experiment is not unclear
- **AND** the source classes include at least three distinct classes

#### Scenario: Report build-readiness row is validated

- **WHEN** a changed Opportunity Radar report contains a `Build Readiness` row
- **THEN** the row matches an `opportunities.json` entry by title or id
- **AND** the row's build decision matches the entry stage
- **AND** the row's build-readiness fields match the corresponding state fields

#### Scenario: Report money-readiness row is validated

- **WHEN** a changed Opportunity Radar report contains a `Money Readiness` row
- **THEN** the row matches an `opportunities.json` entry by title or id
- **AND** the row's stage matches the entry stage
- **AND** the row's money-first fields match the corresponding state fields

### Requirement: Selected Opportunities End In Testable Offers

Every selected opportunity SHALL include a concrete next test that can be executed manually without building a large product first, build-readiness fields that determine whether more implementation is justified, and money-readiness fields that determine whether the next step is selling, testing, or building.

#### Scenario: Opportunity clears selection threshold

- **WHEN** an opportunity is selected
- **THEN** it includes the observed signal, repeated pain, likely user or buyer, current workaround or money signal, proposed offer, success threshold, falsification threshold, and evidence gaps
- **AND** it records paid wedge, distribution channel, private data barrier, OSS commoditization risk, product shape, pricing hypothesis, and do-not-build-until condition
- **AND** it records pain score, spend score, reachability score, timing score, buildability score, technology shift, buyer, expensive workflow, existing spend, paid experiment, and source classes
- **AND** it is supported by at least two distinct source classes

### Requirement: Opportunity State Preserves Build Readiness

Opportunity Radar SHALL keep build-readiness and money-readiness metadata comparable across selected, deferred, and watchlisted opportunities, and SHALL keep each entry's stage consistent with the array that contains it.

#### Scenario: Opportunities state is updated

- **WHEN** an entry is written under `selected`, `deferred`, or `watchlisted`
- **THEN** the entry includes `paid_wedge`, `distribution_channel`, `private_data_barrier`, `oss_commoditization_risk`, `product_shape`, `pricing_hypothesis`, and `do_not_build_until`
- **AND** the entry includes `pain_score`, `spend_score`, `reachability_score`, `timing_score`, `buildability_score`, `technology_shift`, `buyer`, `expensive_workflow`, `existing_spend`, `paid_experiment`, and `source_classes`

#### Scenario: State entry declares a stage

- **WHEN** an entry is stored under `selected`, `deferred`, or `watchlisted`
- **THEN** its `stage` value matches the containing array's allowed stage family

### Requirement: Unclear Paid Wedges Stay Watchlisted

Opportunity Radar SHALL NOT mark opportunities as selected for test, sell-before-build, or selected for build when the paid wedge, spend evidence, reachability, source diversity, or private data boundary is insufficient.

#### Scenario: Paid wedge or spend evidence is weak

- **WHEN** an opportunity does not identify what a buyer concretely pays for
- **OR** spend score is below 2
- **THEN** it is kept in `watchlisted`
- **AND** `do_not_build_until` names the evidence required before further build work

#### Scenario: Private data is required

- **WHEN** an opportunity requires access to private code or private data before the next useful validation
- **THEN** it is kept in `watchlisted`
- **AND** it is not marked `selected-for-test`, `sell-before-build`, or `selected-for-build`

## ADDED Requirements

### Requirement: Opportunity Radar Uses Money-First Selection

Opportunity Radar SHALL rank opportunities by buyer, spend, reachability, timing, and buildability before recommending implementation.

#### Scenario: Opportunity is selected for manual testing

- **WHEN** an opportunity is placed in `selected`
- **THEN** spend score is at least 2
- **AND** reachability score is at least 2
- **AND** source classes include at least two distinct classes
- **AND** the stage is one of `selected`, `selected-for-test`, `sell-before-build`, or `selected-for-build`

#### Scenario: Opportunity is selected for build

- **WHEN** an opportunity is marked `selected-for-build`
- **THEN** spend score is at least 3
- **AND** reachability score is at least 3
- **AND** timing score is at least 2
- **AND** buildability score is at least 3
- **AND** paid experiment is not unclear
- **AND** source classes include at least three distinct classes

#### Scenario: Evidence is GitHub-only

- **WHEN** an opportunity's source classes only include `github`
- **THEN** it is kept in `watchlisted`
- **AND** it is not marked `selected`, `selected-for-test`, `sell-before-build`, or `selected-for-build`

### Requirement: Opportunity Radar Records Technology Shifts

Opportunity Radar SHALL capture the technology or market shift that makes an opportunity timely.

#### Scenario: Opportunity state is updated

- **WHEN** an opportunity entry is written
- **THEN** `technology_shift` records what changed, when, old constraint, new capability, cost delta, quality delta, latency delta, accessibility delta, and affected workflows
- **AND** unclear fields are explicit instead of omitted

### Requirement: Opportunity Radar Supports Sell Before Build

Opportunity Radar SHALL represent opportunities whose next step is a manual paid validation rather than implementation.

#### Scenario: A paid experiment should happen before implementation

- **WHEN** the next useful action is to offer a paid report, sample transformation, audit, review, or other manual service before building software
- **THEN** the opportunity can use the `sell-before-build` stage inside the `selected` array
- **AND** the recommended next test describes the buyer, offer, price or pricing hypothesis, channel, success threshold, and falsification threshold
