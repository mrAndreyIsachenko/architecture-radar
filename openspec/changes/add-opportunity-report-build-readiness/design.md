## Context

Opportunity Radar PRs are reviewed from the generated report first. `opportunities.json` is good for structured comparison, and `opportunities/*.md` is good for durable records, but neither should be required to answer the first review question:

> Is this opportunity buildable now, test-only, or watchlist-only?

## Decision

Add a required report section:

```markdown
## Build Readiness

| Opportunity | Paid wedge | Distribution channel | Private data barrier | OSS commoditization risk | Product shape | Pricing hypothesis | Do not build until | Build decision |
|---|---|---|---|---|---|---|---|---|
| ... | ... | ... | `public-only` | `medium` | `cli` | `team` | ... | `selected-for-test` |
```

The allowed enum values match the existing structured state validator:

- private data barrier: `none`, `public-only`, `private-code-required`, `private-data-required`, `unclear`;
- OSS commoditization risk: `low`, `medium`, `high`, `unclear`;
- product shape: `cli`, `github-action`, `browser-extension`, `hosted-api`, `report`, `other`, `unclear`;
- pricing hypothesis: `free`, `team`, `pro`, `unclear`.

The report-level validator should not try to prove the paid wedge is real. It should enforce that a selected or selected-for-build row cannot carry an unclear paid wedge or a private-data-blocking boundary.

## Non-Goals

- Do not rewrite historical reports.
- Do not require a report to select an opportunity.
- Do not infer consistency between every table row and every `opportunities.json` entry yet; this can be added later if drift becomes a real issue.
