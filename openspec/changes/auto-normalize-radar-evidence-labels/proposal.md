## Why

The 2026-08-11 scheduled Architecture Radar run failed because the model labeled
`spec/OpenLineage.json` as `E1 source verified`. The validator correctly
classified `spec/` as `E3 maintainer stated`, but the whole run failed before a
reviewable PR could be published.

This class of mistake is deterministic and fixable without trusting the model:
path-based E1 downgrades for test/docs/spec evidence should be normalized before
strict validation runs.

## What Changes

- Add a deterministic normalizer for generated Architecture Radar Markdown
  artifacts.
- Downgrade unambiguous `E1 source verified` lines to `E2 test verified` or
  `E3 maintainer stated` when their backtick evidence paths point to tests,
  README/docs/NEWS/CHANGELOG/release/ADR/spec paths.
- Leave ambiguous mixed-source lines unchanged so strict validation still fails
  and forces manual review.
- Run the normalizer between the Codex research step and
  `scripts/validate-radar-state.py`.
- Update setup doctor and tests so the workflow must keep this normalization
  step.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `architecture-radar`: generated evidence labels are normalized before strict
  validation.
- `setup-doctor`: repository readiness includes the normalizer script and
  workflow hook.

## Impact

- Adds `scripts/normalize-radar-evidence-labels.py`.
- Updates `.github/workflows/architecture-radar.yml`.
- Updates setup checks, docs, and tests.
- Adds OpenSpec evidence under
  `openspec/changes/auto-normalize-radar-evidence-labels/`.
