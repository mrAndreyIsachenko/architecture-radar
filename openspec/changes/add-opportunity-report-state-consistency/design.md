## Context

The report is optimized for human review. `opportunities.json` is optimized for machine comparison. Both carry the same build-readiness fields, so they must not silently disagree.

The previous build-readiness change intentionally did not enforce this because the first step was report visibility. Now that visibility exists, the next smallest guardrail is deterministic report/state consistency.

## Decision

The validator will parse `## Build Readiness` into structured rows.

Each row's `Opportunity` cell must match either `title` or `id` from one entry in `opportunities.json`, after normalizing punctuation, whitespace, case, markdown links, and backticks.

For the matched state entry:

- `Build decision` must equal the entry `stage`;
- if an entry has no explicit `stage`, the array name supplies the default decision;
- enum and text build-readiness fields must match state values after whitespace normalization;
- a row that cannot be matched fails validation.

The state validator will also enforce array/stage consistency:

- entries in `selected` use `selected`, `selected-for-test`, or `selected-for-build`;
- entries in `deferred` use `deferred`;
- entries in `watchlisted` use `watchlist` or `watchlisted`.

## Non-Goals

- Do not rewrite historical reports.
- Do not require every accumulated state entry to appear in a report.
- Do not add IDs to the report table yet.
- Do not attempt semantic similarity between differently worded paid wedges; use normalized text equality.
