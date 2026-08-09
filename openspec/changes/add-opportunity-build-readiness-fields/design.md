## Context

Opportunity Radar should distinguish three different states:

- evidence is interesting enough to keep watching;
- evidence is strong enough for a small demand test;
- evidence is strong enough to justify building a product-shaped artifact.

The current schema mostly covers the second state. It requires a `next_test`, but it does not force the agent to name the paid wedge, distribution path, privacy boundary, upstream commoditization risk, product shape, pricing hypothesis, or stop condition before another build step.

## Decisions

### Add Comparable Build-Readiness Fields

Every entry in `opportunities.json` under `selected`, `deferred`, and `watchlisted` should include:

```json
{
  "paid_wedge": "What buyers concretely pay for.",
  "distribution_channel": "How the artifact is installed, bought, or adopted.",
  "private_data_barrier": "none|public-only|private-code-required|private-data-required|unclear",
  "oss_commoditization_risk": "low|medium|high|unclear",
  "product_shape": "cli|github-action|browser-extension|hosted-api|report|other|unclear",
  "pricing_hypothesis": "free|team|pro|unclear",
  "do_not_build_until": "The evidence signal required before more build work."
}
```

The same concepts should appear as sections in opportunity record Markdown files so the PR remains reviewable without reading JSON.

### Selected Means Build-Eligible Enough For The Next Test

The `selected` array should not contain entries whose paid wedge is unclear or whose next useful validation requires private code or private data. Those entries should be kept under `watchlisted` with a concrete `do_not_build_until` condition.

This is deliberately stricter than only blocking `selected-for-build`; it prevents the state file from treating "interesting but inaccessible" signals as selected opportunities.

### Keep Product Shape Narrow

Allowed `product_shape` values are intentionally limited:

- `cli`
- `github-action`
- `browser-extension`
- `hosted-api`
- `report`
- `other`
- `unclear`

If an opportunity needs more than one shape, choose the smallest next-test shape and describe expansions in prose.

### Keep Pricing Hypothesis Coarse

Allowed `pricing_hypothesis` values:

- `free`
- `team`
- `pro`
- `unclear`

These are hypotheses, not prices. The goal is to stop the agent from implying commercial readiness without naming whether the wedge is free distribution, team adoption, or a pro/enterprise sale.

## Risks / Trade-offs

- The validator cannot know whether a paid wedge is truly real; it can only reject missing or explicitly unclear fields.
- Some opportunities may be demoted to watchlist despite being worth a manual interview. That is acceptable because Opportunity Radar should prefer false negatives over build recommendations without a wedge.
- Historical reports may still mention older selections. The structured state and opportunity files should reflect the current rule after this change.
