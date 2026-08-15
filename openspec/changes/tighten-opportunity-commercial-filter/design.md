## Context

Opportunity Radar has three selection layers today:

```text
public demand evidence
        -> money-first readiness
        -> fragmentation/control-layer structure
```

The new problem is commercial false positives. A market can be fragmented and technically painful, yet still weak if the natural buyer owns the whole stack, treats the solution as core IP, has a large engineering team, and can build the missing layer internally. The desired target is narrower: repeated cross-company glue where many participants integrate independent providers and the work is necessary but not differentiating.

## Goals / Non-Goals

**Goals:**

- Add build-vs-buy evidence as a first-class Opportunity Radar gate.
- Prefer provider/protocol/data-source proliferation that creates multi-provider customer workflows.
- Require explicit internal-build likelihood and penalize high internal-build likelihood.
- Require a narrow smallest wedge rather than "platform for X" language.
- Keep the new filter machine-checkable in reports, state, and opportunity files.

**Non-Goals:**

- Do not add a new radar workflow or artifact family.
- Do not remove the existing money-first or structural-fragmentation gates.
- Do not require exact market sizing, provider counts, or private procurement data.
- Do not run a live Opportunity Radar research pass as part of implementation.

## Decisions

1. Add commercial-filter fields to each opportunity entry.

   Each entry in `selected`, `deferred`, and `watchlisted` will include:

   - `fragmented_providers`;
   - `multi_provider_user`;
   - `boundary_workflow`;
   - `build_vs_buy_reason`;
   - `internal_build_likelihood`;
   - `money_flow`;
   - `recurrence`;
   - `permissionless_validation`;
   - `smallest_wedge`;
   - `intermediary_maturity`.

   The field set is intentionally narrative rather than numeric. The validator only checks shape, stage gates, and obvious anti-patterns.

2. Add a commercial-filter report table.

   Reports will include `## Commercial Filter` with one row per comparable opportunity. The row gives the reviewer the commercial question first: who multi-homes, where money flows, why they buy rather than build, the internal-build likelihood, and the wedge.

3. Make `internal_build_likelihood` a hard selected gate.

   Allowed values are `low`, `medium`, and `high`. A `high` value can remain watchlisted, but it cannot be selected, `sell-before-build`, or `selected-for-build`.

4. Treat missing multi-provider usage and money flow as blockers.

   If `multi_provider_user`, `money_flow`, `boundary_workflow`, `build_vs_buy_reason`, or `smallest_wedge` is unclear, the opportunity stays watchlisted.

5. Reject platform-shaped wedges.

   The first wedge must be a small artifact such as normalization, reconciliation, routing, invoice/usage comparison, adapter generation, migration, audit trail, or cross-source disagreement detection. The validator will reject selected opportunities whose `smallest_wedge` looks like a broad platform instead of a narrow workflow.

## Risks / Trade-offs

- [Risk] The stronger filter may produce fewer selected opportunities. -> Mitigation: watchlisted remains valid, and the next report should prefer quality over count.
- [Risk] Narrative fields are harder to validate than enumerations. -> Mitigation: validate required fields, obvious unclear markers, internal-build likelihood, and platform anti-patterns.
- [Risk] Existing opportunities need migration. -> Mitigation: add conservative metadata without changing their existing decisions unless the new gate requires keeping them watchlisted.
- [Risk] High internal-build likelihood is context-dependent. -> Mitigation: require an explicit explanation and keep the value reviewable in reports and state.
