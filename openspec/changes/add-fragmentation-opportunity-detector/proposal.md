## Why

Opportunity Radar currently ranks demand signals by buyer, spend, reachability, timing, and buildability, but it can still over-index on isolated pain. The next useful evolution is to detect structural markets where rapid primitive/provider growth creates fragmentation, manual comparison or reconciliation, and an opening for an aggregation, optimization, routing, or control layer.

## What Changes

- Extend Opportunity Radar rules to search explicitly for fragmentation-driven opportunities, not generic startup ideas.
- Add structural opportunity fields to comparable opportunity state and selected opportunity files.
- Add a weighted structural scoring model covering fragmentation, manual pain, economic value, objective measurability, execution potential, timing, competitive gap, and prototype feasibility.
- Require selected opportunities to explain the execution ladder from `observe` to `recommend` to `choose` to `execute`.
- Add report sections for ranked structural candidates and structural score breakdowns.
- Add validation so selected opportunities cannot pass without manual workflow evidence, objective function evidence, execution potential, timing delta, and structural score metadata.
- Keep existing money-first readiness rules; structural scoring narrows candidate quality but does not replace paid wedge and source-diversity gates.

## Capabilities

### New Capabilities

### Modified Capabilities
- `opportunity-radar`: add fragmentation/control-layer detection, structural fields, scoring, report sections, and validation gates.

## Impact

- Updates `docs/opportunity-agent-rules.md` and `docs/opportunity-research-scope.md`.
- Updates `scripts/run-codex-opportunity-radar.sh` prompt constraints.
- Updates `scripts/validate-opportunity-radar-state.py` and tests.
- Updates report and opportunity record expectations without changing artifact directories.
- Updates documentation for the Opportunity Radar operating model.
- Does not create a third radar workflow.
- Does not run public discovery or generate a new opportunity report as part of implementation.
