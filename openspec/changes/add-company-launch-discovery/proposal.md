## Why

The radars can miss early but relevant signals when they appear first as company
launches instead of GitHub repositories. Degla and RightNow/RunInfra exposed
that the current discovery rules are too repository-first for drones, robotics,
AI infrastructure, and other fast-moving company-led areas.

## What Changes

- Add company-launch discovery as an explicit Opportunity Radar seed source.
- Add company-to-repository expansion as an Architecture Radar discovery path.
- Extend watchlist semantics to support company, product, launch, and runtime
  artifacts that may or may not have an inspectable GitHub repository.
- Require generated reports to distinguish launch/company signals from demand
  proof and source-level architecture evidence.
- Add watchlist entries for Degla and RightNow/RunInfra so the next eligible
  runs account for the misses directly.
- Do not change schedules, publish permissions, model choice, or selection
  thresholds.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `architecture-radar`: Add company-to-repository expansion and watchlist
  artifact handling for company/product/launch/runtime seeds.
- `opportunity-radar`: Add company-launch discovery sources and require company
  launch signals to remain seed/watchlist evidence unless buyer, paid wedge, and
  repeatable demand are separately evidenced.

## Impact

- `docs/agent-rules.md`
- `docs/opportunity-research-scope.md`
- `docs/opportunity-agent-rules.md`
- `watchlist.yml`
- `opportunity-watchlist.yml`
- `openspec/specs/architecture-radar/spec.md`
- `openspec/specs/opportunity-radar/spec.md`
- Validation scripts/tests only if existing validators reject the new artifact
  types.
