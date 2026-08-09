## Why

Opportunity Radar currently records score, confidence, money signal, reachability, evidence count, and next test. That is enough to compare public signals, but not enough to decide whether an opportunity is safe to build.

The first Opportunity Radar run exposed the gap: some opportunities had repeated pain but no direct spend or procurement evidence, and some tests would require private logs, private code, or private configuration before they could be useful. Without explicit build-readiness fields, the agent can over-promote a watchlist hypothesis into a build recommendation.

## What Changes

Require Opportunity Radar opportunity records and structured state to include:

- `paid_wedge`
- `distribution_channel`
- `private_data_barrier`
- `oss_commoditization_risk`
- `product_shape`
- `pricing_hypothesis`
- `do_not_build_until`

Add a deterministic rule: if the paid wedge is unclear, or if the opportunity requires access to private code or private data, the opportunity cannot remain in `selected` or be marked `selected-for-build`; it must stay in `watchlisted`.

## Capabilities

### Modified Capabilities

- `opportunity-radar`: adds build-readiness metadata and validation rules for selected opportunity state.

## Impact

- Updates Opportunity Radar operating rules and research scope.
- Updates `opportunities.json` schema expectations and current state.
- Updates selected opportunity records with explicit build-readiness sections.
- Updates deterministic validation and unit tests.
- Updates the reusable opportunity-demand example.
