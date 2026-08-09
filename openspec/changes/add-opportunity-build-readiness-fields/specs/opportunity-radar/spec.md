## MODIFIED Requirements

### Requirement: Selected Opportunities End In Testable Offers

Every selected opportunity SHALL include a concrete next test that can be executed manually without building a large product first, plus build-readiness fields that determine whether more implementation is justified.

#### Scenario: Opportunity clears selection threshold

- **WHEN** an opportunity is selected
- **THEN** it includes the observed signal, repeated pain, likely user or buyer, current workaround or money signal, proposed offer, success threshold, falsification threshold, and evidence gaps
- **AND** it records paid wedge, distribution channel, private data barrier, OSS commoditization risk, product shape, pricing hypothesis, and do-not-build-until condition

### Requirement: Opportunity State Preserves Build Readiness

Opportunity Radar SHALL keep build-readiness metadata comparable across selected, deferred, and watchlisted opportunities.

#### Scenario: Opportunities state is updated

- **WHEN** an entry is written under `selected`, `deferred`, or `watchlisted`
- **THEN** the entry includes `paid_wedge`, `distribution_channel`, `private_data_barrier`, `oss_commoditization_risk`, `product_shape`, `pricing_hypothesis`, and `do_not_build_until`

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
