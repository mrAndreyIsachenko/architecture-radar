## Why

Opportunity Radar currently finds well-evidenced pain, but it can still rank
developer-visible technical problems above opportunities with clearer buyer,
spend, and channel evidence. The next iteration should make the run answer
"what can be sold or manually validated this week?" before it answers "what is
interesting to build?".

## What Changes

- Add money-first scoring fields for pain, spend, reachability, timing, and
  buildability.
- Add explicit technology-shift and buyer/workflow/spend fields so technology
  acts as an economic catalyst, not the center of selection.
- Add a `sell-before-build` stage for opportunities that should be validated
  by a paid/manual offer before implementation.
- Require selected opportunities to have evidence from multiple source classes,
  not only GitHub issues.
- Tighten `selected-for-build` gates so build work is blocked when spend,
  reachability, source diversity, or paid-experiment evidence is weak.
- Update Opportunity Radar operating rules, prompt text, state validator, tests,
  and docs.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `opportunity-radar`: money-first selection, source-class diversity,
  technology-shift evidence, `sell-before-build`, and stricter build gates.

## Impact

- Updates `docs/opportunity-agent-rules.md` and
  `docs/opportunity-research-scope.md`.
- Updates `scripts/run-codex-opportunity-radar.sh`.
- Updates `scripts/validate-opportunity-radar-state.py` and its tests.
- Updates `opportunities.json` entries to the expanded comparable schema.
- Adds OpenSpec change evidence under
  `openspec/changes/add-money-first-opportunity-selection/`.
