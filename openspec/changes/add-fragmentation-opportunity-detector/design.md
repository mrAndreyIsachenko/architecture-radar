## Context

Opportunity Radar already has a weekly/manual workflow, separated artifacts, money-first selection, report/state consistency validation, and source-class gates. It currently asks "where is the shortest credible path to first money?" but does not force the agent to identify the market structure that makes an opportunity non-obvious.

The new detector should make the 1inch-style pattern explicit:

```text
primitive/provider growth
        -> fragmentation
        -> manual comparison/routing/reconciliation
        -> measurable objective
        -> executable choice
        -> aggregation, optimization, routing, or control layer
```

## Goals / Non-Goals

**Goals:**
- Add structural fragmentation evidence as a first-class Opportunity Radar filter.
- Keep selected opportunities constrained by money-first gates.
- Require weighted structural score breakdowns backed by evidence.
- Preserve existing artifacts under `opportunity-reports/`, `opportunities/`, `signals/`, and `opportunities.json`.
- Make AI one possible ecosystem, not the default answer.

**Non-Goals:**
- Do not create a new workflow or directory family.
- Do not run a live research pass as part of this implementation change.
- Do not require exact provider counts when public evidence is insufficient.
- Do not allow structural excitement to bypass paid wedge, private-data, or source-diversity requirements.

## Decisions

1. Add structural fields to each comparable opportunity entry.

   Each entry in `selected`, `deferred`, and `watchlisted` will include:

   - `structural_pattern`;
   - `primitive_growth`;
   - `fragmentation_summary`;
   - `manual_workflow`;
   - `objective_function`;
   - `execution_ladder`;
   - `economic_pain`;
   - `timing_reason`;
   - `competitors`;
   - `structural_scores`.

   This keeps comparison in `opportunities.json` while preserving narrative detail in `opportunities/*.md`.

2. Validate structural score fields deterministically.

   `structural_scores` will contain eight 0-5 integers plus `total`:

   - `fragmentation`;
   - `manual_pain`;
   - `economic_value`;
   - `objective_measurability`;
   - `execution_potential`;
   - `timing`;
   - `competition_gap`;
   - `prototype_feasibility`;
   - `total`.

   The validator will recompute `total` using weights 15/15/20/10/10/10/10/10 and compare it to the stored integer total. This prevents arbitrary LLM total scores from drifting away from dimension scores.

3. Add report-level structural visibility.

   Reports will add:

   - `## Structural Candidate Ranking`;
   - `## Structural Score Breakdown`.

   The ranking table gives the reviewer the first screen: rank, opportunity, ecosystem, score, why now, manual workflow, and wedge. The score breakdown table makes the structural dimensions auditable.

4. Keep selection gates conservative.

   Selected entries must have a concrete manual workflow, objective function, execution ladder, timing reason, competitors, and score metadata. Weak entries can remain watchlisted with lower scores or unclear fields, but they cannot be selected when the manual workflow, objective function, or execution path is unclear.

## Risks / Trade-offs

- [Risk] More required fields raise the burden on the research agent. -> Mitigation: fields are structured and reusable; weak candidates can remain watchlisted rather than forcing selection.
- [Risk] Provider-count evidence may be incomplete. -> Mitigation: allow narrative `primitive_growth`, but require explicit uncertainty instead of fabricated counts.
- [Risk] Existing opportunity entries need migration. -> Mitigation: update the committed current entries in `opportunities.json` and opportunity files with conservative structural metadata.
- [Risk] Weighted scores may imply false precision. -> Mitigation: scores are used as review aids; evidence labels and gates still decide whether to test or build.
