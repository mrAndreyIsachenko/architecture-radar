# Opportunity Radar Research Scope

Domain configuration for Opportunity Radar. This file answers what to look for. The operating rules live in [`opportunity-agent-rules.md`](opportunity-agent-rules.md).

## Topic Families

Use these families for signal accounting and selection:

- `ai-llm-demand`
- `blockchain-demand`
- `privacy-networking-demand`
- `drones-robotics-demand`
- `document-ai-demand`
- `observability-demand`
- `developer-tooling-demand`
- `data-infrastructure-demand`
- `security-demand`
- `cloud-infrastructure-demand`
- `fintech-payments-demand`
- `api-infrastructure-demand`
- `robotics-demand`
- `geospatial-demand`
- `healthcare-infrastructure-demand`
- `logistics-industrial-demand`

## Discovery Sources

Use public, inspectable sources such as:

- GitHub issues, discussions, releases, dependency links, and project roadmaps;
- Hacker News, Reddit, public forums, mailing lists, and public launch comments;
- product docs, pricing pages, public changelogs, and public support pages;
- job posts and role descriptions that reveal workflow pain or budget;
- benchmark, dataset, model-release, and hardware-release discussions;
- app reviews or marketplace listings when they are public and attributable.

Do not use private communities, authenticated exports, personal data, or outbound outreach in the first implementation.

## Structural Opportunity Pattern

Prefer candidates matching this sequence:

```text
recent primitive/provider growth
-> fragmentation
-> manual comparison, routing, reconciliation, or fallback
-> measurable objective function
-> software can progress from observe to recommend to choose to execute
```

The target is an aggregation, optimization, routing, execution, procurement,
reconciliation, or control layer. A directory, newsletter, or comparison page is
not enough unless it can plausibly evolve toward choosing or executing the
workflow.

## Commercial Opportunity Filter

Fragmentation is necessary but not sufficient. Prefer candidates where the
missing layer sits between independent vendors, infrastructure providers,
protocols, data sources, or organizations:

```text
few providers
-> rapid provider proliferation
-> fragmentation
-> multi-provider usage
-> manual integration, comparison, reconciliation, routing, or switching
-> new intermediary software layer
```

The key commercial distinction is:

```text
core technology inside one buyer -> likely internal build
cross-company glue across providers -> stronger buy signal
```

For every selected, deferred, or watchlisted opportunity, estimate:

- what fragmented, naming concrete providers, protocols, products, APIs,
  vendors, or data sources;
- who uses more than one provider or must interoperate across providers;
- what boundary work appears, such as normalization, adapters, routing,
  comparison, reconciliation, failover, orchestration, identity mapping, schema
  translation, policy enforcement, auditing, verification, settlement, billing
  reconciliation, migration, cross-vendor monitoring, or unified reporting;
- why the buyer will not simply build it internally;
- `internal_build_likelihood`: `low`, `medium`, or `high`;
- who already pays whom in the underlying ecosystem;
- why the workflow recurs instead of being one-time integration;
- how to validate the wedge without incumbent permission, private code/data, or
  hardware deployment;
- the smallest non-platform wedge.

Prefer non-core but necessary workflows and cross-company coordination problems.
Penalize core IP, full-stack owners, large internal engineering teams,
one-provider customer behavior, and hardware-first validation.

## Structural Discovery Signals

Use these as discovery signals only:

- many competing providers appearing in a short period;
- multiple APIs implementing similar capabilities;
- frequent "X vs Y vs Z" or "alternatives to X" discussions;
- compatibility layers, adapters, gateways, routers, aggregators, proxies, or
  unified APIs;
- provider switching, fallback logic, migration between vendors, or multiple
  dashboards;
- internal scripts, glue code, spreadsheets, or "we built our own" workflows;
- manual comparison, export/import, reconciliation, normalization, or copy/paste
  between tools;
- users comparing pricing, latency, quality, reliability, availability,
  accuracy, risk, or resource usage.
- customers reconciling usage, invoices, settlement, identity, policy, audit
  trails, or reports across several vendors;
- multi-homing, fallback provider usage, brokered capacity, or provider
  switching;
- duplicated adapters, connectors, consultants, integration teams, or customer
  glue code around the same boundary.

Do not select a candidate from keywords alone. Require multiple public signals
and state whether each claim is evidence-backed or interpretation.

## Technology Shifts

For every selected or watchlisted opportunity, identify the technology,
platform, regulatory, hardware, distribution, or cost shift that makes the
workflow newly worth revisiting.

Record:

- `what_changed`;
- `when`;
- `old_constraint`;
- `new_capability`;
- `cost_delta`;
- `quality_delta`;
- `latency_delta`;
- `accessibility_delta`;
- `affected_workflows`.

Use `unclear` explicitly when a delta is not evidenced. Do not treat a model
launch, repository release, or viral announcement as demand by itself; connect
the shift to an expensive workflow and a reachable buyer.

For structural opportunities, distinguish old known pain from pain caused by a
recent increase in ecosystem complexity. Where public evidence allows, estimate:

- relevant primitives/providers 12-24 months ago;
- relevant primitives/providers now;
- recent release, funding, repository, pricing, or adoption activity;
- why the opportunity became materially more interesting in 2025-2026 or
  another recent period.

## Signal Types

Classify each reviewed signal:

- `repeated-pain` - multiple independent users describe the same problem.
- `paid-demand` - users appear to pay for a product, service, workaround, or role addressing the pain.
- `competitor-proof` - existing vendors, projects, or paid tools indicate the problem has buyers or users.
- `workaround-economy` - users maintain scripts, spreadsheets, forks, or manual process because tooling is missing.
- `integration-gap` - active projects need glue between systems that do not fit cleanly.
- `operational-risk` - failures are expensive, risky, or hard to debug.
- `infrastructure-shift` - a new model, protocol, hardware, regulation, or platform change creates fresh demand.
- `incumbent-friction` - adopted tools create recurring complaints about cost, complexity, lock-in, reliability, or missing features.
- `fragmentation` - rapid primitive/provider growth creates too many choices or incompatible surfaces.
- `manual-comparison` - users compare, reconcile, route, export/import, or switch providers manually.
- `optimization-gap` - a workflow has a measurable objective but no trusted chooser or executor.
- `execution-gap` - users can identify the right choice but still need software to perform the action.
- `commercial-glue` - independent providers create repeated non-core integration work that buyers plausibly buy.
- `internal-build-risk` - pain is real, but the natural buyer likely builds the layer internally as core IP.

## Required Analysis

For each selected opportunity, explain:

1. What demand signal was observed.
2. Which evidence sources support it.
3. Whether the signal repeats across independent sources.
4. Which source classes support it and whether it is GitHub-only.
5. What technology or market shift makes the timing relevant.
6. Who likely buys or approves the spend.
7. What expensive workflow or budget it attaches to.
8. What existing spend, labor, procurement, hiring, consultant, tool, or workaround evidence exists.
9. What exactly someone would pay for.
10. What paid/manual experiment can be sold before building.
11. How the artifact would be installed, bought, or adopted.
12. Whether the next useful validation requires private code or private data.
13. Whether an upstream OSS PR could commoditize the opportunity.
14. Which smallest product shape fits the next test: CLI, GitHub Action, browser extension, hosted API, or report.
15. Whether the pricing hypothesis is free, team, pro, or unclear.
16. What signal is required before more build work.
17. What current alternatives exist.
18. Why those alternatives appear insufficient.
19. What small experiment could test demand within one week.
20. What would falsify the opportunity.
21. What should explicitly not be built.
22. Which primitives, providers, tools, APIs, or vendors multiplied recently.
23. Why the ecosystem is fragmented.
24. What manual comparison, routing, reconciliation, fallback, or migration
    workflow exists today.
25. Whether "better" can be expressed as an objective function with constraints.
26. Whether the product can move from observe to recommend to choose to execute.
27. Which competitors or adjacent products cover part of the control layer.
28. Which concrete providers, protocols, products, APIs, vendors, or data
    sources fragmented.
29. Which buyer or user uses more than one provider, and how often.
30. What cross-provider boundary workflow repeats today.
31. Why the buyer would buy rather than build internally.
32. Whether `internal_build_likelihood` is low, medium, or high.
33. Who already pays whom in the underlying ecosystem.
34. Whether validation can happen without incumbent permission, private
    code/data, or hardware deployment.
35. The smallest wedge that is not a platform.

Score every selected, deferred, and watchlisted opportunity from 0 to 5:

- `pain_score`;
- `spend_score`;
- `reachability_score`;
- `timing_score`;
- `buildability_score`.

Also score structural dimensions from 0 to 5:

- `fragmentation`;
- `manual_pain`;
- `economic_value`;
- `objective_measurability`;
- `execution_potential`;
- `timing`;
- `competition_gap`;
- `prototype_feasibility`.

Compute structural `total` as a weighted 0-10 score using:

- fragmentation: 15%;
- manual pain: 15%;
- economic value: 20%;
- objective measurability: 10%;
- execution potential: 10%;
- timing: 10%;
- competition gap: 10%;
- prototype feasibility: 10%.

## Evidence Labels

Use market-specific labels:

- `M1 paid demand`: public evidence that users pay, hire, procure, subscribe, or allocate budget for the problem.
- `M2 repeated pain`: independent public evidence that the same pain repeats across users, issues, posts, or forums.
- `M3 competitor proof`: existing products, hosted services, consultants, or OSS projects indicate active demand.
- `M4 workaround evidence`: users maintain scripts, spreadsheets, forks, manual processes, or brittle glue to solve the problem.
- `I interpretation`: synthesis derived from evidence.
- `H hypothesis`: plausible but not sufficiently verified.

Use `H hypothesis` when evidence is thin. Do not relabel source code or docs as market evidence unless they show demand, pain, competitor proof, or workaround behavior.

In generated reports and opportunity files, write the full label text, for example `M2 repeated pain`, not only `M2`.

## Selection Rule

Select no more than five opportunities per manual run.

Selecting zero is valid when evidence is thin, noisy, or not connected to a testable next step.

Do not select an opportunity because it is exciting. Select it because there is enough evidence to justify a small experiment.

If the paid wedge is unclear, if `spend_score < 2`, if `reachability_score < 2`, if the opportunity is GitHub-only, if the useful next test requires private code or private data, if the manual workflow is unclear, if no objective function exists, or if the execution path cannot move beyond recommendation, keep the opportunity in watchlist. Do not select it and do not mark it selected for build.

Also keep the opportunity in watchlist if multi-provider usage is unclear, money
flow is unclear, the boundary workflow is one-time, the smallest wedge is a
broad platform, or `internal_build_likelihood` is `high`.

Use `sell-before-build` when the next useful action is a paid/manual offer,
sample transformation, report, audit, or review before implementation. Do not
recommend building unless the paid experiment has already been validated by
evidence in the report.

## Anti-Patterns

Penalize or reject:

- generic AI wrappers without fragmentation, manual workflow, and economic
  mechanism;
- pure directories of tools unless they can evolve toward routing,
  optimization, execution, procurement, or another valuable action;
- developer annoyance with no spend, labor cost, operational risk, expensive
  mistake, revenue impact, or willingness-to-pay signal;
- mature markets where a dominant aggregation or control layer already owns the
  workflow unless a new fragmentation boundary has appeared;
- old known pain with no recent ecosystem complexity increase.
- opportunities where the obvious buyer owns the whole stack and treats the
  layer as core IP;
- customers that normally choose one provider and do not multi-home;
- one-time migrations or integrations with no recurring workflow;
- wedges that require hardware deployment before validation;
- broad "platform for X" products with no narrow first paid workflow;
- markets with providers but no evidence that money already flows through the
  underlying ecosystem.
