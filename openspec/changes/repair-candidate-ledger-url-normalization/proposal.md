## Why

The 2026-08-17 Architecture Radar run failed after spending the research step because the generated `Candidate Ledger` used a URL-like column name that did not exactly match the validator contract. This is a deterministic format drift that should be repaired before validation when the underlying data is present.

## What Changes

- Normalize safe `Candidate Ledger` column aliases before validation.
- Keep validation strict when the report truly lacks a URL column or URL data.
- Add tests for the observed failure mode.
- Do not change research selection, evidence scoring, cadence, or publication permissions.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `architecture-radar`: pre-validation normalization may repair safe candidate-ledger URL column aliases before strict validation runs.

## Impact

- `scripts/normalize-radar-evidence-labels.py`
- `tests/test_normalize_radar_evidence_labels.py`
- `openspec/changes/repair-candidate-ledger-url-normalization/`
