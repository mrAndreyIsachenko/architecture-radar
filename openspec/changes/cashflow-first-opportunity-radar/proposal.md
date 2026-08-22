## Why

Opportunity Radar still over-promotes interesting technical pain into plausible
diagnostic, audit, CLI, or report ideas. It needs to rank opportunities by the
shortest credible path to a first transaction, starting from existing money
flow and paid manual work rather than adjacent technical budgets.

## What Changes

- Shift the primary objective to: "Where can one developer permissionlessly
  find a buyer, manually solve an already-paid problem, and plausibly get the
  first transaction within 7 days?"
- Add explicit money evidence classes distinguishing direct workflow spend from
  budget adjacency and no money evidence.
- Add time-to-transaction scoring and gates for sell-before-build decisions.
- Add cashflow-first discovery sources such as freelance marketplaces, agency
  pages, SaaS pricing, procurement/RFPs, job posts for recurring manual work,
  app marketplaces, product reviews, and public manual workflow examples.
- Add required opportunity fields for buyer, existing paid workflow, money
  evidence, one-sentence offer, concrete pricing hypothesis, acquisition path,
  manual-first delivery, time-to-transaction, productization path, and
  falsification.
- Add `Best Paths To First Transaction` and `Interesting But Not Yet
  Commercial` report sections.
- Re-evaluate existing LangGraph, Tailscale, and ArduPilot opportunities under
  the new model instead of carrying previous stages forward automatically.
- **BREAKING**: bump `opportunities.json` to `schema_version: 2` and require the
  new cashflow-first fields in comparable state entries.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `opportunity-radar`: Change selection, state, report, evidence, and validation
  requirements from technical-pain-first to cashflow-first opportunity ranking.

## Impact

- `docs/opportunity-agent-rules.md`
- `docs/opportunity-research-scope.md`
- `scripts/run-codex-opportunity-radar.sh`
- `scripts/validate-opportunity-radar-state.py`
- `tests/test_validate_opportunity_radar_state.py`
- `opportunities.json`
- Existing opportunity records under `opportunities/`
- A dry-run re-evaluation report under `opportunity-reports/`
