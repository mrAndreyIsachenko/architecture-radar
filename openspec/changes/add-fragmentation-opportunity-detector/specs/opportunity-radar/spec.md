## ADDED Requirements

### Requirement: Opportunity Radar Detects Fragmentation-Driven Control Layers
Opportunity Radar SHALL explicitly search for markets where recent primitive or provider growth creates fragmentation, manual comparison or reconciliation, a measurable objective, and a plausible aggregation, optimization, routing, execution, or control-layer wedge.

#### Scenario: Structural candidate is selected
- **WHEN** Opportunity Radar selects, selects-for-test, or marks an opportunity sell-before-build
- **THEN** the opportunity includes primitive/provider growth evidence
- **AND** fragmentation evidence
- **AND** a current manual workflow
- **AND** an objective function or explicit measurable decision criterion
- **AND** an execution ladder from observe to recommend to choose to execute
- **AND** timing evidence explaining why the opportunity is more interesting now than in prior years

#### Scenario: Keyword-only signal is found
- **WHEN** a signal only matches terms such as gateway, router, aggregator, unified API, comparison, fallback, or reconciliation
- **THEN** Opportunity Radar treats it only as a discovery signal
- **AND** does not select it without independent evidence for fragmentation, manual workflow, objective function, execution potential, and economic pain

### Requirement: Opportunity State Preserves Structural Opportunity Fields
Opportunity Radar SHALL keep structural opportunity metadata comparable across selected, deferred, and watchlisted entries in `opportunities.json`.

#### Scenario: Opportunities state is updated
- **WHEN** an entry is written under `selected`, `deferred`, or `watchlisted`
- **THEN** it includes `structural_pattern`, `primitive_growth`, `fragmentation_summary`, `manual_workflow`, `objective_function`, `execution_ladder`, `economic_pain`, `timing_reason`, `competitors`, and `structural_scores`
- **AND** `structural_scores` includes `fragmentation`, `manual_pain`, `economic_value`, `objective_measurability`, `execution_potential`, `timing`, `competition_gap`, `prototype_feasibility`, and `total`

### Requirement: Opportunity Reports Expose Structural Ranking
Opportunity Radar reports SHALL expose structural candidate ranking and structural score breakdowns before detailed opportunity reviews.

#### Scenario: Report contains structural candidates
- **WHEN** Opportunity Radar produces a report with selected, deferred, or watchlisted opportunities
- **THEN** the report includes a `Structural Candidate Ranking` table with Rank, Opportunity, Ecosystem, Score, Why now, Manual workflow, and Wedge
- **AND** the report includes a `Structural Score Breakdown` table with Opportunity, Fragmentation, Manual pain, Economic value, Objective measurability, Execution potential, Timing, Competition gap, Prototype feasibility, and Total

### Requirement: Structural Scores Are Weighted And Auditable
Opportunity Radar SHALL compute structural totals from dimension scores using fixed weights.

#### Scenario: Structural score is validated
- **WHEN** `structural_scores` is written for an opportunity entry
- **THEN** every structural dimension score is an integer from 0 to 5
- **AND** `total` equals the weighted 0-10 score derived from fragmentation 15%, manual pain 15%, economic value 20%, objective measurability 10%, execution potential 10%, timing 10%, competition gap 10%, and prototype feasibility 10%

### Requirement: Weak Structural Evidence Blocks Selection
Opportunity Radar SHALL NOT select an opportunity when the structural opportunity mechanism is unclear.

#### Scenario: Manual workflow is unclear
- **WHEN** an opportunity lacks a concrete manual comparison, routing, reconciliation, export/import, spreadsheet, internal-script, fallback, or multi-provider workflow
- **THEN** it stays in `watchlisted`
- **AND** `do_not_build_until` names the public signal required before selection

#### Scenario: Objective function is unclear
- **WHEN** an opportunity cannot name a measurable objective such as cost, latency, quality, reliability, yield, accuracy, risk, availability, or resource usage
- **THEN** it stays in `watchlisted`

#### Scenario: Execution path is unclear
- **WHEN** an opportunity cannot plausibly progress beyond observe/recommend into choosing or executing a workflow action
- **THEN** it stays in `watchlisted`
