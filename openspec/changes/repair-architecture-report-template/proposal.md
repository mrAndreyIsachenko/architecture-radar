## Why

The 2026-08-23 Architecture Radar run generated `reports/2026-08-23.md`, but validation failed because the report omitted several exact H2 section names required by `scripts/validate-radar-state.py`. The failure lost the generated artifact instead of producing a reviewable PR with explicit evidence gaps.

## What Changes

- Add a deterministic Architecture Radar report repair step before validation.
- Require the research workflow to preserve the canonical report section contract even when the model uses alternate headings or omits sections.
- Keep repaired omissions visible as evidence gaps rather than silently fabricating research quality.

## Capabilities

### New Capabilities

### Modified Capabilities

- `architecture-radar`: Scheduled Architecture Radar runs must normalize generated daily report structure before artifact validation.

## Impact

- Affects `scripts/run-codex-radar.sh`, the Architecture Radar workflow, radar validation tests, and a new report-structure repair script.
- Does not change repository review, pattern extraction, or `radar.json` semantics.
