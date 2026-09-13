## ADDED Requirements

### Requirement: Agent Runtime And Memory Launch Seeds Are Accounted
Architecture Radar SHALL treat high-signal AI agent runtime and agent-memory launches as explicit discovery seeds when they are named in `docs/research-scope.md` or `watchlist.yml`.

#### Scenario: Canonical runtime source is found through a secondary artifact
- **WHEN** discovery finds a DeepSeek Harness handbook, plugin list, desktop wrapper, product page, documentation page, or fork before the canonical runtime repository
- **THEN** the candidate ledger records the secondary artifact and the source-expansion path to `deepseek-ai/deepseek-harness` or records a concrete reason why no stable canonical source snapshot was inspectable

#### Scenario: Agent memory seed is required
- **WHEN** a normal Architecture Radar run processes active watchlist entries
- **THEN** `TencentCloud/TencentDB-Agent-Memory` is either selected, source-inspected, explicitly deferred, or rejected in the candidate ledger with a commit or release reference and a reason tied to source evidence quality

#### Scenario: Watchlist inclusion does not force selection
- **WHEN** a required runtime or memory launch seed is inspected
- **THEN** the run may defer or reject it when source-level evidence is insufficient, but it MUST still account for the seed and its canonical source-expansion decision in the report
