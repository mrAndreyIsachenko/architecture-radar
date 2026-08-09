## Why

Architecture Radar has become useful as a scheduled, evidence-backed research agent, and the same mechanics are attractive for opportunity and demand research. But market/demand research has different evidence, artifacts, and failure modes than source-level architecture review.

If we put public demand signals directly into the existing repository-oriented `radar.json`, `repositories/`, and source-inspection rules, the system will blur two different domains:

- architecture research: `GitHub repository -> source evidence -> reusable mechanism -> engineering decision`
- opportunity research: `public demand signal -> repeated pain -> money signal -> testable offer`

This change specifies a separate Opportunity/Demand Radar mode before implementation so the new mode can reuse the workflow discipline without corrupting the Architecture Radar schema.

## What Changes

Add a planned `opportunity-radar` capability with its own inputs, outputs, evidence taxonomy, validation rules, and workflow boundary.

This proposal does not implement the workflow yet. It creates the OpenSpec agreement for the future implementation.

## Capabilities

### New Capabilities

- `opportunity-radar`: tracks public demand signals, repeated pain, money evidence, competitor/workaround proof, opportunity hypotheses, and testable offers.

### Modified Capabilities

- `architecture-radar`: no behavioral change; remains repository/source-review focused.

## Impact

- Adds OpenSpec project state under `openspec/`.
- Documents the intended Opportunity/Demand Radar mode before code changes.
- Future implementation is expected to add separate files such as `opportunity-interests.md`, `opportunity-watchlist.yml`, `opportunities.json`, `opportunity-reports/`, `opportunities/`, `signals/`, `docs/opportunity-agent-rules.md`, `docs/opportunity-research-scope.md`, `scripts/validate-opportunity-radar-state.py`, and `.github/workflows/opportunity-radar.yml`.
- Future validation should include `openspec validate --all` in CI once OpenSpec is part of the contribution workflow.
