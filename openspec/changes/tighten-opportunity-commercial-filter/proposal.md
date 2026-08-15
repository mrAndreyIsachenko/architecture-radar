## Why

Opportunity Radar now detects fragmentation-driven control layers, but fragmentation alone is still too broad. The next filter should prefer cross-company glue problems where buyers use multiple providers and are more likely to buy a non-core intermediary layer than build proprietary tooling internally.

## What Changes

- Add a stricter commercial filter for opportunities where the missing layer sits between independent vendors, infrastructure providers, protocols, data sources, or organizations.
- Require every comparable opportunity to explain provider proliferation, multi-provider usage, boundary work, money flow, build-vs-buy reasoning, and internal-build likelihood.
- Penalize or block selected opportunities when the natural buyer owns the whole stack, treats the layer as core IP, can solve it internally once, or rarely uses multiple providers.
- Add report sections that make the commercial filter visible before detailed reviews.
- Update deterministic validation so selected opportunities cannot pass without multi-provider usage, money flow, non-core build-vs-buy evidence, and a small non-platform wedge.
- Keep existing money-first and structural-fragmentation gates; this change tightens commercial attractiveness instead of replacing those gates.

## Capabilities

### New Capabilities

### Modified Capabilities

- `opportunity-radar`: add cross-company commercial filtering, internal-build likelihood penalties, multi-provider usage evidence, money-flow evidence, and smallest-wedge validation.

## Impact

- Updates `docs/opportunity-agent-rules.md` and `docs/opportunity-research-scope.md`.
- Updates `scripts/run-codex-opportunity-radar.sh` prompt constraints.
- Updates `scripts/validate-opportunity-radar-state.py` and tests.
- Updates Opportunity Radar report and opportunity record expectations without changing artifact directories or workflow cadence.
- Migrates current `opportunities.json` entries and opportunity files with conservative commercial-filter metadata.
- Does not run a live public discovery pass or generate a new Opportunity Radar report as part of implementation.
