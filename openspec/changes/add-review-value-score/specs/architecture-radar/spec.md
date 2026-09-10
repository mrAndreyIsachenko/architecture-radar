## ADDED Requirements

### Requirement: Architecture Reports Expose Review Value

Generated Architecture Radar reports SHALL include a deterministic review value verdict that downstream review tooling can parse before recommending merge, targeted fix, or closure.

#### Scenario: Architecture report declares useful value

- **WHEN** an Architecture Radar report adds verified architectural knowledge, changes confidence in an existing pattern, identifies a material repository change, or explicitly concludes no candidate cleared the threshold
- **THEN** the report includes a `Review Value` section
- **AND** the section includes one row with verdict, score, reason, and recommended action
- **AND** the score is an integer from 0 to 5
- **AND** the recommended action is `merge`, `request-fix`, `close`, or `watchlist`

#### Scenario: Architecture report uses an accidental ten-point review value score

- **WHEN** an Architecture Radar report contains a single-row `Review Value` table whose score is an integer from 6 to 10
- **THEN** the deterministic report repair step maps the score onto the 0 to 5 scale before strict validation
- **AND** the repaired score is used by downstream report and pull request summarizers

#### Scenario: Architecture report has low value

- **WHEN** an Architecture Radar report is stale, duplicate-heavy, has no material change, or needs targeted evidence repair
- **THEN** the `Review Value` section does not recommend `merge`
- **AND** the reason names the specific value problem
