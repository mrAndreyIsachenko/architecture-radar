## Why

Weekly Synthesis can currently pass validation while turning a watchlisted
Opportunity Radar entry into an active next-week build recommendation. This
breaks the commercial filter: `opportunities.json.selected` is supposed to be
the source of opportunities that are ready for active experiments.

## What Changes

- Require Weekly Synthesis to respect Opportunity Radar state when producing
  `Decisions And Experiments` and `Next Week Focus`.
- Treat `opportunities.json.selected` as the only source of active opportunity
  experiments.
- Allow watchlisted and deferred opportunities to be mentioned only as blocked,
  pending validation, or not-ready work.
- Add deterministic validation so generated weekly reports fail when they
  recommend active opportunity work from `watchlisted` or `deferred`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `weekly-synthesis`: Weekly reports must not promote non-selected Opportunity
  Radar entries into active next-week experiments.

## Impact

- `scripts/run-codex-weekly-synthesis.sh`
- `scripts/validate-weekly-synthesis-state.py`
- `tests/test_validate_weekly_synthesis_state.py`
- `openspec/specs/weekly-synthesis/spec.md`
