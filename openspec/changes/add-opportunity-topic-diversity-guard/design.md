## Context

`opportunity-interests.md` lists five priority families: AI/LLM, blockchain, privacy networking, drones/robotics, and document AI. The current watchlist seeds only three of those families, and reports do not have a required place to show per-family coverage. A run can therefore satisfy structural validation while spending most attention on a previous selected opportunity.

The validator already checks report sections, signal ledgers, signal-note coverage, build readiness, money readiness, structural scores, commercial filters, state schema, and watchlist syntax. This change should reuse that validation style and avoid introducing external dependencies.

## Goals / Non-Goals

**Goals:**

- Make priority-family coverage explicit in every normal Opportunity Radar report.
- Prevent stale selected opportunities from being framed as new main discoveries unless the report records new commercial evidence.
- Seed the missing priority families so broad discovery has anchors outside LangGraph/Tailscale/ArduPilot.
- Keep the rule permissive enough to allow fewer than three selected opportunities when the evidence is weak.

**Non-Goals:**

- Do not require one selected opportunity per topic family.
- Do not force weak candidates into `selected`.
- Do not rewrite historical generated reports.
- Do not merge Architecture Radar and Opportunity Radar artifacts.

## Decisions

1. Parse priority families from `opportunity-interests.md`, not from the broader research-scope list.

   Rationale: `docs/opportunity-research-scope.md` contains additional optional ecosystems. The user-facing priority list lives in `opportunity-interests.md`, so the coverage guard should follow that file.

   Alternative considered: require every family in `docs/opportunity-research-scope.md`. That would create noise because the scope includes broad optional families such as healthcare and logistics.

2. Require a `Topic Coverage` markdown table in reports.

   Rationale: a visible table is reviewable in PRs and machine-checkable by the validator. The table must include every priority family, but a family may have zero reviewed signals if the report explains why.

3. Require a `Commercial Delta` markdown table in reports.

   Rationale: repeated selected opportunities are acceptable as carried-forward experiments. They become a problem only when the run presents them as the new main focus without new buyer, spend, procurement, inbound, paid pilot, or independent customer evidence.

4. Validate repeated selected opportunities against the base branch when available.

   Rationale: CI can compare the PR state to `origin/main`. Local validation may not always have a base ref; in that case the validator still enforces table shape and required sections but does not fail on missing base history.

5. Add watchlist seeds for blockchain and document AI.

   Rationale: this reduces the current anchoring bias while preserving watchlist-directed runs. Seeds are discovery anchors, not automatic selection.

## Risks / Trade-offs

- Older generated reports will not have the new sections. Mitigation: validation only targets changed reports or the explicitly requested run date.
- Base-branch comparison can be unavailable in some local runs. Mitigation: repeated-focus validation becomes best-effort without blocking local edits.
- A coverage table can become ceremonial. Mitigation: the validator requires every priority family to appear, and the prompt requires a concrete decision/reason per family.
