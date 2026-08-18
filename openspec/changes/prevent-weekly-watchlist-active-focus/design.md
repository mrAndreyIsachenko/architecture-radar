## Context

Weekly Synthesis reads both Architecture Radar and Opportunity Radar artifacts
and emits one weekly report. The current validator checks report shape but does
not verify that Opportunity Radar state is respected. As a result, a report can
turn a `watchlisted` opportunity into an active build recommendation even when
`opportunities.json.selected` is empty.

## Goals / Non-Goals

**Goals:**

- Make `opportunities.json.selected` the only source of active opportunity
  experiments in weekly reports.
- Prevent `watchlisted` and `deferred` opportunities from appearing as active
  next-week build/run/sell recommendations.
- Keep watchlist mentions allowed when they are framed as blocked or requiring
  validation.
- Cover the failure deterministically in tests.

**Non-Goals:**

- Changing Opportunity Radar scoring or selection.
- Regenerating weekly reports.
- Blocking architecture-only weekly focus recommendations.
- Creating a semantic natural-language classifier for every possible report
  phrasing.

## Decisions

1. Add the rule to the weekly synthesis prompt.

   The model should be told the state boundary before writing the report. This
   reduces failed CI loops and makes the generated artifact more likely to be
   correct on the first pass.

2. Add deterministic validation based on `opportunities.json`.

   Prompt rules are not enough. The validator will inspect the active weekly
   sections, identify references to non-selected opportunities, and fail when
   those references are paired with active work language such as build, run,
   sell, active experiment, paid pilot, or next-step experiment.

3. Validate only active recommendation sections.

   Watchlisted opportunities can still be discussed in `Evidence Gaps`,
   `Repeated Candidates Or Signals`, and explanatory notes. The restricted
   sections are `Decisions And Experiments` and `Next Week Focus`, because they
   drive action.

## Risks / Trade-offs

- False positives from simple text matching -> keep matching scoped to active
  sections and require both a non-selected opportunity reference and active
  action language.
- False negatives from unusual phrasing -> include multiple identifiers per
  opportunity: id, title, file path, and title-derived slug.
- Reports with architecture-only action remain allowed -> validation is tied to
  opportunity references rather than generic action verbs alone.
