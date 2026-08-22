## Context

Opportunity Radar currently captures many useful fields, but the decision model
still lets technical pain plus adjacent ecosystem spend become
`sell-before-build`. That is too loose. A paid platform, engineering salaries,
or GitHub issue cluster proves that money exists near a problem, not that a
buyer will pay for a new narrow wedge.

The new model keeps the existing artifact family and validators, but changes
the ranking center from technical sophistication to first-transaction
probability.

## Goals / Non-Goals

**Goals:**

- Make direct or near-direct workflow spend the strongest ranking signal.
- Block `sell-before-build` when evidence is only budget adjacency.
- Require every sell-before-build path to name buyer, offer, price, acquisition
  path, manual delivery, and a 7-day falsification test.
- Keep technical pain as useful context but not as the primary selector.
- Re-evaluate current selected opportunities without hardcoded exceptions.

**Non-Goals:**

- Do not create a new radar mode or repository.
- Do not remove technical priority topics; demote them from hard discovery
  boundaries to context and optional filters.
- Do not automate outreach or use private/authenticated marketplaces.
- Do not require live paid validation in CI.

## Decisions

1. Bump `opportunities.json` to schema version 2.

   Rationale: the comparable state shape changes materially. Keeping version 1
   while adding new required gates would hide migration risk.

2. Add money evidence classes rather than overloading `money_signal`.

   Rationale: `money_signal=medium` was too ambiguous. The validator needs to
   know whether evidence is direct workflow spend, manual labor spend,
   competitor revenue, procurement/job demand, budget adjacency, or absent.

3. Treat `time_to_transaction_score` as a gate, not only a score.

   Rationale: opportunities that cannot plausibly produce a first transaction
   in 7 days should not be top-ranked sell-before-build items, even if the
   technical pain is real.

4. Validate the report's first-transaction table against `opportunities.json`.

   Rationale: the report should make the commercial decision obvious without
   relying on prose. State/report drift is the easiest way to regress.

5. Re-evaluate current opportunities with a deterministic dry-run report.

   Rationale: this change intentionally invalidates at least one previous
   decision. A dry-run report makes that visible without pretending a full live
   market scan happened.

## Risks / Trade-offs

- Stricter sell-before-build gates will produce fewer selected opportunities ->
  this is intended; watchlist is the right place for technical pain without
  direct money evidence.
- Marketplace and agency sources can be noisy -> classify evidence precisely
  and keep weak findings watchlisted.
- Concrete price hypotheses can look speculative -> allow "unclear" outside
  sell-before-build, but require a concrete starting price for top paths.
- Existing reports remain in old format -> validators focus on changed/current
  artifacts and schema v2 state going forward.
