## Why

Weekly Synthesis PR #61 generated Markdown links pointing at the GitHub Actions
workspace path `/home/runner/work/...`. Those links are not stable repository
references and become broken noise in committed weekly reports.

## What Changes

- Require Weekly Synthesis reports to use repository-relative paths for local
  artifacts.
- Instruct the weekly synthesis prompt not to emit absolute workspace, runner,
  or local filesystem paths.
- Extend weekly synthesis validation to reject absolute runner/workspace paths
  in generated reports.
- Fix the already generated `weekly-reports/2026-W34.md` links.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `weekly-synthesis`: Weekly reports must not contain absolute runner or local
  filesystem paths for repository artifacts.

## Impact

- `weekly-reports/2026-W34.md`
- `scripts/run-codex-weekly-synthesis.sh`
- `scripts/validate-weekly-synthesis-state.py`
- `tests/test_validate_weekly_synthesis_state.py`
