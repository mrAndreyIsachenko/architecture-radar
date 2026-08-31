## ADDED Requirements

### Requirement: Architecture Reports Expose Review Value

Generated Architecture Radar reports SHALL include a deterministic review value verdict that downstream review tooling can parse before recommending merge, targeted fix, or closure.

#### Scenario: Architecture report declares useful value

- **WHEN** an Architecture Radar report adds verified architectural knowledge, changes confidence in an existing pattern, identifies a material repository change, or explicitly concludes no candidate cleared the threshold
- **THEN** the report includes a `Review Value` section
- **AND** the section includes one row with verdict, score, reason, and recommended action
- **AND** the recommended action is `merge`, `request-fix`, `close`, or `watchlist`

#### Scenario: Architecture report has low value

- **WHEN** an Architecture Radar report is stale, duplicate-heavy, has no material change, or needs targeted evidence repair
- **THEN** the `Review Value` section does not recommend `merge`
- **AND** the reason names the specific value problem
