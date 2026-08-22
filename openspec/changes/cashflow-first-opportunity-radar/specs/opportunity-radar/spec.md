## ADDED Requirements

### Requirement: Opportunity Radar Ranks First-Transaction Paths

Opportunity Radar SHALL rank commercial opportunities by the shortest credible
path to a first paid transaction by one developer within seven days.

#### Scenario: Report presents first-transaction paths

- **WHEN** Opportunity Radar produces a normal, mixed, or dry-run report
- **THEN** the report includes a `Best Paths To First Transaction` section
- **AND** that section lists at most five opportunities
- **AND** every row includes buyer, existing paid workflow, current workaround,
  one-sentence offer, price hypothesis, where to find first buyers,
  time-to-transaction score, why now, and biggest uncertainty

#### Scenario: Technical pain lacks direct money evidence

- **WHEN** a candidate has technical pain but only budget adjacency or no money
  evidence
- **THEN** it is placed in `Interesting But Not Yet Commercial`, `watchlisted`,
  `research`, or `deferred`
- **AND** it is not marked `sell-before-build`

### Requirement: Opportunity Radar Classifies Money Evidence

Opportunity Radar SHALL classify money evidence separately from generic market
or ecosystem budget signals.

#### Scenario: State entry records money evidence

- **WHEN** an opportunity is written to `opportunities.json`
- **THEN** it records `money_evidence_type` as one of
  `direct_workflow_spend`, `manual_labor_spend`, `competitor_revenue_signal`,
  `procurement_or_job_signal`, `budget_adjacency`, or `no_money_evidence`
- **AND** it records `money_evidence` with concrete source-backed reasoning

#### Scenario: Budget adjacency is present

- **WHEN** money exists in the adjacent ecosystem but evidence does not show
  willingness to pay for the proposed wedge or equivalent workflow
- **THEN** the opportunity uses `budget_adjacency`
- **AND** `budget_adjacency` is insufficient for `sell-before-build`

### Requirement: Sell-Before-Build Requires Transaction Readiness

Opportunity Radar SHALL only mark an opportunity `sell-before-build` when the
first paid transaction can plausibly be tested without product build-out.

#### Scenario: Opportunity clears sell-before-build

- **WHEN** an opportunity is marked `sell-before-build`
- **THEN** it has direct or near-direct money evidence
- **AND** it has a concrete reachable buyer
- **AND** it has a one-sentence sellable offer
- **AND** it has a permissionless buyer acquisition path
- **AND** first delivery can be performed manually
- **AND** `time_to_transaction_score` is at least 3

#### Scenario: Time-to-transaction score is low

- **WHEN** an opportunity has `time_to_transaction_score` less than or equal to
  2
- **THEN** it is not marked `sell-before-build` unless direct workflow spend is
  exceptionally strong and the exception is explained

### Requirement: Opportunity State Uses Cashflow Schema

Opportunity Radar SHALL store cashflow-first opportunity fields in
`opportunities.json` schema version 2.

#### Scenario: State entry is comparable

- **WHEN** an entry is stored under `selected`, `deferred`, or `watchlisted`
- **THEN** it includes buyer, existing paid workflow, money evidence type,
  money evidence, current workaround, current cost, why buyer would buy from us,
  smallest sellable outcome, manual first delivery, one-sentence offer, concrete
  price hypothesis, buyer acquisition path, time-to-transaction score,
  time-to-transaction reason, productization path, and falsification test

#### Scenario: Schema version is current

- **WHEN** `opportunities.json` is validated
- **THEN** `schema_version` is `2`

### Requirement: Existing Opportunities Are Re-evaluated

Opportunity Radar SHALL not preserve previous selected stages automatically
after the cashflow-first model is introduced.

#### Scenario: Existing opportunity has weak money evidence

- **WHEN** a previously selected opportunity only has technical pain, GitHub
  issues, adjacent platform pricing, or adjacent hiring evidence
- **THEN** the re-evaluation records it as watchlisted, deferred, or interesting
  but not yet commercial
- **AND** the report explains why its previous stage changed
