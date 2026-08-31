## ADDED Requirements

### Requirement: Opportunity Reports Expose Review Value

Generated Opportunity Radar reports SHALL include a deterministic review value verdict that downstream review tooling can parse before recommending merge, targeted fix, closure, or watchlisting.

#### Scenario: Opportunity report declares useful value

- **WHEN** an Opportunity Radar report adds a new public demand signal, changes the commercial stage of an opportunity, or records a useful no-build/watchlist conclusion
- **THEN** the report includes a `Review Value` section
- **AND** the section includes one row with verdict, score, reason, and recommended action
- **AND** the recommended action is `merge`, `request-fix`, `close`, or `watchlist`

#### Scenario: Opportunity report has low commercial value

- **WHEN** an Opportunity Radar report has unclear paid wedge, weak money evidence, private-data barriers, stale watchlist repetition, or no material commercial delta
- **THEN** the `Review Value` section does not recommend `merge`
- **AND** the reason names the commercial value problem
