## Why

Opportunity Radar now has a broader stated interest set, but the watchlist and reporting loop can still repeatedly converge on already-known zones such as LangGraph. This makes a successful run look productive while failing to show whether blockchain, privacy networking, drones, or document AI had fresh demand evidence.

## What Changes

- Require each normal Opportunity Radar report to account for the priority topic families listed in `opportunity-interests.md`.
- Require the watchlist to contain at least one seed for every priority topic family.
- Add a `Topic Coverage` report section so reviewers can see which families were searched, skipped, selected, deferred, or watchlisted.
- Add a `Commercial Delta` report section so an already-selected opportunity cannot be presented as fresh focus without new commercial evidence.
- Extend validation and tests for the new report sections and watchlist coverage.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `opportunity-radar`: add topic-family coverage accounting and repeated-selected commercial-delta guardrails.

## Impact

- `scripts/run-codex-opportunity-radar.sh`
- `docs/opportunity-agent-rules.md`
- `docs/opportunity-research-scope.md`
- `opportunity-watchlist.yml`
- `scripts/validate-opportunity-radar-state.py`
- `tests/test_validate_opportunity_radar_state.py`
