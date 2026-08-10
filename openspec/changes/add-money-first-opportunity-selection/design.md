## Context

The current Opportunity Radar state already stores `score`, `money_signal`,
`reachability`, `paid_wedge`, `distribution_channel`, `private_data_barrier`,
`product_shape`, `pricing_hypothesis`, and `do_not_build_until`.

That prevents the worst build mistakes, but it still allows a report to treat
"well-documented pain" as selected even when direct money evidence is weak.
The report for 2026-08-09 exposed this: GitHub issue evidence proved repeated
pain, while direct spend/procurement/hiring evidence remained absent.

## Decision

Add a money-first selection layer to every comparable opportunity entry:

```json
{
  "pain_score": 0,
  "spend_score": 0,
  "reachability_score": 0,
  "timing_score": 0,
  "buildability_score": 0,
  "technology_shift": {
    "what_changed": "...",
    "when": "...",
    "old_constraint": "...",
    "new_capability": "...",
    "cost_delta": "...",
    "quality_delta": "...",
    "latency_delta": "...",
    "accessibility_delta": "...",
    "affected_workflows": []
  },
  "buyer": "...",
  "expensive_workflow": "...",
  "existing_spend": "...",
  "paid_experiment": "...",
  "source_classes": []
}
```

`source_classes` uses stable public-source classes:

- `github`
- `forum`
- `social`
- `product`
- `pricing`
- `job`
- `procurement`
- `marketplace`
- `docs`
- `benchmark`
- `news`
- `other`

The validator can enforce structure and deterministic gates. It cannot prove a
market. The rule is intentionally mechanical:

- selected entries require `spend_score >= 2`, `reachability_score >= 2`, and
  at least two source classes;
- `selected-for-build` requires `spend_score >= 3`, `reachability_score >= 3`,
  `timing_score >= 2`, `buildability_score >= 3`, at least three source
  classes, and a non-unclear paid experiment;
- GitHub-only entries cannot be `selected`, `selected-for-test`,
  `sell-before-build`, or `selected-for-build`;
- weak/unclear spend remains `watchlisted`.

Add `sell-before-build` as a selected-array stage. It means the next action is
a manual paid offer or sample-request test, not implementation. This gives the
radar a first-money path without forcing fake product work.

## Report Shape

The existing `Build Readiness` table stays stable to avoid churn in historical
reports. A new `Money Readiness` section is required for changed reports and
contains:

```markdown
| Opportunity | Pain | Spend | Reachability | Timing | Buildability | Buyer | Existing spend | Paid experiment | Source classes | Stage |
```

The table must match `opportunities.json` by title or id and agree on the
money-first fields.

Selected opportunity files add sections for technology shift, buyer, expensive
workflow, existing spend, paid experiment, source classes, and money-first
scores.

## Non-Goals

- Do not rename Opportunity Radar to Money Radar in this change.
- Do not change Architecture Radar.
- Do not contact buyers or automate outbound sales.
- Do not remove historical opportunity artifacts that predate this schema.
