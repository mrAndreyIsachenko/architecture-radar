## ADDED Requirements

### Requirement: Opportunity Radar Prefers Cross-Company Glue

Opportunity Radar SHALL prefer opportunities where the missing layer sits between independent vendors, infrastructure providers, protocols, data sources, or organizations, and SHALL NOT treat fragmentation alone as sufficient evidence of a commercially attractive opportunity.

#### Scenario: Commercially strong fragmentation is selected

- **WHEN** Opportunity Radar selects, selects-for-test, marks sell-before-build, or marks selected-for-build
- **THEN** the opportunity names the concrete providers, protocols, products, or data sources that fragmented
- **AND** identifies the buyer or user that interacts with more than one provider
- **AND** describes repeated boundary work such as normalization, adapters, routing, reconciliation, failover, orchestration, policy enforcement, auditing, verification, settlement, billing reconciliation, migration, monitoring, or unified reporting
- **AND** explains why the workflow is non-core enough to buy rather than build

#### Scenario: Fragmentation is only internal to one buyer

- **WHEN** the natural buyer owns the whole stack or treats the missing layer as core IP
- **THEN** the opportunity is not ranked as a selected opportunity unless the report proves a separate cross-company buyer or non-core purchase path

### Requirement: Opportunity State Preserves Commercial Filter Fields

Opportunity Radar SHALL keep commercial filter metadata comparable across selected, deferred, and watchlisted entries in `opportunities.json`.

#### Scenario: Opportunities state is updated

- **WHEN** an entry is written under `selected`, `deferred`, or `watchlisted`
- **THEN** it includes `fragmented_providers`, `multi_provider_user`, `boundary_workflow`, `build_vs_buy_reason`, `internal_build_likelihood`, `money_flow`, `recurrence`, `permissionless_validation`, `smallest_wedge`, and `intermediary_maturity`
- **AND** `internal_build_likelihood` is one of `low`, `medium`, or `high`

### Requirement: Opportunity Reports Expose Commercial Filter

Opportunity Radar reports SHALL expose the commercial filter before detailed opportunity reviews.

#### Scenario: Report contains comparable opportunities

- **WHEN** Opportunity Radar produces a report with selected, deferred, or watchlisted opportunities
- **THEN** the report includes a `Commercial Filter` table with Opportunity, Fragmented providers, Multi-provider user, Boundary workflow, Build-vs-buy, Internal build likelihood, Money flow, Permissionless validation, Smallest wedge, and Decision
- **AND** each row matches the corresponding `opportunities.json` entry by title or id

### Requirement: High Internal-Build Likelihood Blocks Selection

Opportunity Radar SHALL NOT select opportunities whose natural buyer is likely to build the missing layer internally.

#### Scenario: Internal-build likelihood is high

- **WHEN** an opportunity has `internal_build_likelihood` of `high`
- **THEN** it stays in `watchlisted`
- **AND** `do_not_build_until` names the evidence required to prove a non-core or cross-company purchase path

#### Scenario: Multi-provider usage is unclear

- **WHEN** an opportunity cannot identify who uses more than one provider, protocol, data source, or vendor
- **THEN** it stays in `watchlisted`

#### Scenario: Money flow is unclear

- **WHEN** an opportunity cannot identify who already pays whom in the underlying ecosystem
- **THEN** it stays in `watchlisted`

### Requirement: Selected Wedges Are Narrow And Non-Platform

Opportunity Radar SHALL require selected opportunities to name a narrow first wedge that can be validated before building a broad platform.

#### Scenario: Wedge is platform-shaped

- **WHEN** the smallest wedge is described only as a platform, marketplace, operating system, end-to-end suite, or generic AI-powered product
- **THEN** the opportunity is not selected

#### Scenario: Wedge requires hardware deployment before validation

- **WHEN** the smallest wedge requires hardware deployment before the next useful validation
- **THEN** the opportunity stays in `watchlisted`
