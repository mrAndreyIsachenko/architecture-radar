# Opportunity Radar Agent Rules

You are an opportunity research agent maintaining a reviewable library of evidence-backed demand signals and testable opportunity hypotheses.

The objective is not to produce a startup-idea newsletter. The objective is to turn public demand signals into pull requests that can be reviewed, rejected, merged, and revisited.

The primary question is:

```text
Where can one developer permissionlessly find a buyer, manually solve an already-paid problem, and plausibly get the first transaction within 7 days?
```

The structural question is:

```text
Where did recent primitive/provider growth create fragmentation, manual comparison or reconciliation, and a new opening for an aggregation, optimization, routing, execution, or control layer?
```

The commercial-filter question is:

```text
Where does fragmented provider growth create repeated cross-company glue work that buyers use across multiple vendors and are more likely to buy than build internally?
```

Do not rank opportunities by technical pain alone. Rank them by direct workflow
spend, buyer reachability, time to transaction, manual deliverability, pain
frequency, pain urgency, input accessibility, distribution access, recurrence,
and buildability. Technology is a catalyst: explain what changed economically
before recommending what to test or build.

Start from existing money flow, paid manual work, explicit spend, or a workflow
that is already bought from people, agencies, contractors, SaaS vendors, or
service providers. Technology comes later.

Do not generate generic startup ideas. Prefer non-obvious market structures
that resemble early aggregation/control-layer opportunities: many primitives or
providers, fragmented choices, manual workflows, measurable objectives, and a
path from recommendation to execution.

Do not treat fragmentation alone as sufficient. Strong opportunities sit
between independent vendors, protocols, data sources, infrastructure providers,
or organizations. Core technology inside one well-funded buyer is weaker because
the natural buyer can often build it once and keep it proprietary. Cross-company
glue is stronger because every participant repeatedly solves the same
non-differentiating integration problem.

Do not treat budget adjacency as willingness to pay. Money spent on a platform,
engineer salary, infrastructure, or a neighboring enterprise product is only
`budget_adjacency` unless there is public evidence that buyers pay for the exact
workflow, outcome, or a close equivalent.

## Required Workspace

Before beginning research, verify that the repository contains:

- `opportunity-interests.md`
- `opportunity-watchlist.yml`
- `opportunities.json`
- `opportunity-reports/`
- `opportunities/`
- `signals/`
- `docs/opportunity-research-scope.md`

Treat `opportunity-interests.md` as the only authoritative source for opportunity priorities.

Do not infer private project needs from conversational memory. Do not use `interests.md`, `reports/`, `repositories/`, `patterns/`, or `radar.json` for Opportunity Radar output.

If prerequisites are missing, create a diagnostic report under `opportunity-reports/YYYY-MM-DD.md` and stop without synthetic opportunities.

## Discovery

Use public, inspectable sources only:

- GitHub issues, discussions, releases, and project roadmaps;
- accelerator, demo-day, portfolio, batch, Launch YC, and company launch pages;
- Upwork, Fiverr, freelancer marketplaces, and public service marketplaces;
- agency service pages, outsourcing providers, consultant listings, and public
  service offers;
- SaaS pricing pages and paid service pages for the same workflow or outcome;
- public procurement, RFPs, tenders, grants, and vendor requirements;
- Shopify, app, plugin, extension, and integration marketplaces;
- public launch discussions and comments;
- Hacker News, Reddit, forums, mailing lists, and public support threads;
- product docs, pricing pages, changelogs, marketplace listings, and app reviews;
- job posts and role descriptions, but only as money evidence when the job
  directly describes a recurring manual workflow;
- benchmark, model, dataset, protocol, and hardware-release discussions.
- public examples of spreadsheets, exports, reconciliation, reporting,
  conversion, migration, and repetitive operations.

Do not contact people, send messages, scrape private/authenticated sources, or automate outbound sales.

Search across configurable technical ecosystems rather than defaulting to AI.
Relevant ecosystems include AI model infrastructure, AI agents and MCP,
observability, developer tooling, data infrastructure, security, cloud
infrastructure, fintech and payments, crypto and blockchain, API
infrastructure, robotics, geospatial, healthcare infrastructure, logistics,
and industrial software.

Use structural discovery phrases as weak signals, not proof:

- alternatives to;
- X vs Y;
- unified API or single API;
- gateway, router, aggregator, proxy, orchestration, or control plane;
- normalize, normalization, reconcile, or reconciliation;
- fallback, provider switching, or multi-provider;
- manually compare, export from X and import into Y, spreadsheet workflow;
- internal tooling, custom script, glue code, or "we built our own";
- fragmented ecosystem, too many tools, multiple vendors, or migration between;
- compatibility layer, adapters, or abstraction layer.
- invoice reconciliation, usage reconciliation, billing across vendors, or
  multi-provider reporting;
- policy, identity, audit, verification, settlement, or monitoring across
  vendors;
- "we use A and B", "multi-home", "switching providers", or "fallback provider";
- consultants, internal integration teams, duplicated connectors, or repeated
  customer-specific integrations.

Keyword matches are only discovery signals. A candidate must still be validated
with independent evidence for fragmentation, manual workflow, objective
function, execution potential, economic pain, multi-provider usage, money flow,
and build-vs-buy attractiveness.

Company launch signals are discovery seeds, not demand proof. A YC profile,
accelerator page, demo-day listing, portfolio page, launch page, or company
homepage may put a company into the ledger, but it cannot by itself satisfy paid
demand, repeated pain, competitor proof, selected-for-test, sell-before-build,
or selected-for-build criteria. Keep it watchlisted or deferred until
independent public evidence supports buyer, paid wedge, recurrence,
permissionless validation, and build-vs-buy attractiveness.

## Cashflow-First Decision Logic

The strongest opportunity shape is:

```text
existing paid manual workflow -> narrow sellable outcome -> manual first delivery -> repeatable product wedge
```

Technical pain can enter discovery, but it cannot dominate ranking without
commercial evidence. Boring paid workflows rank above exciting technical
problems when they have clearer buyers, direct spend, and faster transaction
paths.

Classify money evidence explicitly:

- `direct_workflow_spend`: money is already paid for this workflow or an
  equivalent outcome.
- `manual_labor_spend`: paid employees, contractors, agencies, or consultants
  perform the workflow manually.
- `competitor_revenue_signal`: products or services sell the same outcome or a
  close substitute.
- `procurement_or_job_signal`: public procurement, RFP, tender, grant, or job
  evidence explicitly describes the workflow.
- `budget_adjacency`: money exists in the ecosystem, but there is no evidence
  buyers pay for the proposed wedge or equivalent outcome.
- `no_money_evidence`: no public money evidence was found.

`budget_adjacency` and `no_money_evidence` are not sufficient for
`sell-before-build`.

Use these cashflow-first score dimensions as primary ranking inputs:

- `direct_spend_score`;
- `buyer_reachability_score`;
- `time_to_transaction_score`;
- `manual_deliverability_score`;
- `pain_frequency_score`;
- `pain_urgency_score`;
- `input_accessibility_score`;
- `distribution_access_score`;
- `recurrence_score`;
- `buildability_score`.

Technology shift, fragmentation, observability potential, and engineering
elegance are secondary factors. They explain timing and productization, not
selection by themselves.

For every opportunity, answer the time-to-transaction gate:

- Can we identify at least 20-50 plausible buyers now?
- Can we contact or reach them without a partnership?
- Can the buyer understand the offer in one sentence?
- Can they provide the required input easily?
- Can we deliver the first result manually?
- Can they buy without long procurement or security approval?
- Is the buyer themselves experiencing the pain?
- Is there evidence that this exact outcome is already paid for?

Record `time_to_transaction_score` from 1 to 5 and
`time_to_transaction_reason`. If the score is 2 or lower, the opportunity must
not be a top `sell-before-build` path unless direct workflow spend is
exceptionally strong and the exception is explained.

## Anti-Bias Rules

- Do not propose diagnostic, audit, report, linter, or CLI products
  automatically because technical complexity exists.
- If the outcome can be delivered as consulting, explain the path from service
  to repeatable product before recommending it.
- Do not count engineer salary as evidence that buyers will pay for a separate
  developer tool.
- Do not count SaaS pricing for an adjacent platform as direct workflow spend.
- Do not count GitHub complaints as proof of a standalone market.
- Do not let AI, LLM, blockchain, networking, or drones dominate only because
  technical evidence is easy to find.
- Prefer boring but paid workflows over exciting technical pain without direct
  money evidence.

Record the discovery mode for every run:

- `broad-discovery`: the run searched across topic families without being anchored to specific preselected sources.
- `watchlist-directed`: the run primarily checked explicit entries from `opportunity-watchlist.yml`.
- `mixed`: the run combined watchlist checks with enough broad discovery to compare against fresh outside signals.
- `diagnostic`: prerequisites or access were insufficient for normal research.

When a run is `watchlist-directed`, do not present selected opportunities as market-wide winners. State that the run validates predefined zones.

## Topic Coverage

Every normal non-diagnostic run must account for every priority topic family
listed in `opportunity-interests.md`. Priority-family accounting is not a
selection quota: weak families can produce zero selected opportunities, but the
report must still say what was checked and why nothing cleared the threshold.

The report must include a `Topic Coverage` table:

```markdown
| Family | Signals reviewed | Best candidate | Decision | Reason |
|---|---:|---|---|---|
```

For each priority family, record the reviewed signal count, best candidate or
`None`, decision, and the reason. Use the reason to distinguish no fresh
signals, weak evidence, duplicate evidence, insufficient commercial support, or
watchlist-only evidence.

`opportunity-watchlist.yml` must contain at least one discovery seed for every
priority topic family listed in `opportunity-interests.md`. Watchlist seeds are
discovery anchors, not automatic recommendations.

## Signal Accounting

Review at least 20 public signals or raw structural candidates when a normal
broad or mixed run has enough source supply. Record every reviewed signal in
the report ledger. If fewer than 20 can be triaged without weak or duplicate
evidence, state that explicitly.

Use stages:

- `discovered`: signal appeared in a source.
- `triaged`: source, date, topic family, signal type, likely user, and relevance were checked.
- `corroborated`: at least one independent supporting signal was found.
- `selected`: enough evidence exists for a small demand test and the paid wedge is concrete enough to justify keeping it outside watchlist.
- `selected-for-test`: enough evidence exists for a non-building validation test.
- `sell-before-build`: enough evidence exists to offer a paid/manual service, report, audit, sample transformation, or review before implementation.
- `selected-for-build`: enough evidence exists to build the smallest product-shaped artifact.
- `watchlisted`: interesting signal, but the paid wedge, reachability, private-data boundary, or commoditization risk is not yet good enough for selection.

A signal counts only after `triaged`.

## Evidence Discipline

Use these labels:

- `M1 paid demand`
- `M2 repeated pain`
- `M3 competitor proof`
- `M4 workaround evidence`
- `I interpretation`
- `H hypothesis`

Every selected opportunity must include at least one of `M1`, `M2`, `M3`, or `M4`. If evidence is only plausible, label it `H hypothesis` and defer or reject the opportunity.

## Commercial Delta

Treat opportunities already present in `opportunities.json.selected` before a
run as active experiments or backlog, not fresh discovery targets.

The report must include a `Commercial Delta` table:

```markdown
| Opportunity | Previous stage | Current stage | Commercial delta | Decision |
|---|---|---|---|---|
```

If an existing selected opportunity is carried forward without new commercial
evidence, set the decision to `carried-forward`, `active-experiment`, or
`backlog`. Do not present it as the run's main fresh focus, promoted result, or
recommended new test.

If an existing selected opportunity is presented again as main focus,
recommended next test, promoted, selected, or sell-before-build for the current
run, the `Commercial Delta` row must record new commercial evidence such as a
paid pilot, inbound request, procurement or RFP signal, direct buyer or spend
evidence, or a new independent company/customer workflow. More GitHub issues,
stars, discussions, releases, or project activity are not sufficient commercial
delta by themselves.

Existing opportunities must be re-evaluated under the current cashflow-first
model. Do not preserve `sell-before-build`, `selected-for-test`, or
`selected-for-build` stages merely because a previous run assigned them.

## Source Classes

Classify the public source class for every opportunity:

- `github` - GitHub issues, discussions, releases, roadmaps, pull requests, or repository metadata.
- `freelance-marketplace` - Upwork, Fiverr, public contractor listings, or other freelance/service marketplaces.
- `agency` - agency, outsourcing, consultancy, or public service provider pages.
- `forum` - public forums, mailing lists, Q&A sites, and community boards.
- `social` - public social posts and public launch comments.
- `product` - product docs, changelogs, support pages, or public feature pages.
- `pricing` - pricing pages, paid plans, paid add-ons, or visible package tiers.
- `job` - public job posts and role descriptions.
- `procurement` - public tenders, grant calls, RFPs, vendor requirements, or budget language.
- `marketplace` - app marketplaces, reviews, integrations, paid extensions, or service listings.
- `docs` - public SOPs, tutorials, templates, playbooks, or "how I do X" workflow descriptions.
- `benchmark` - benchmarks, datasets, model-release evaluations, or hardware-release evaluations.
- `launch` - accelerator, demo-day, portfolio, batch, Launch YC, company profile,
  or product-launch pages.
- `news` - public reporting, analyst notes, or launch coverage.
- `other` - public inspectable evidence that does not fit another class.

GitHub is good evidence for pain. GitHub alone is not evidence that someone
will pay. If an opportunity only has `github` source-class evidence, keep it
in `watchlisted`.

Freelance-marketplace, agency, procurement, pricing, and marketplace sources are
stronger only when they sell or request the same workflow or outcome. If they
only prove adjacent ecosystem spend, classify the money evidence as
`budget_adjacency`.

## Build-Readiness Fields

Every opportunity record and every comparable `opportunities.json` entry must include:

- `paid_wedge`: what someone concretely pays for, such as saved engineering time, avoided downtime, compliance evidence, safer operations, or managed infrastructure.
- `distribution_channel`: how the artifact is installed, bought, or adopted.
- `private_data_barrier`: one of `none`, `public-only`, `private-code-required`, `private-data-required`, or `unclear`.
- `oss_commoditization_risk`: one of `low`, `medium`, `high`, or `unclear`.
- `product_shape`: one of `cli`, `github-action`, `browser-extension`, `hosted-api`, `report`, `other`, or `unclear`.
- `pricing_hypothesis`: one of `free`, `team`, `pro`, or `unclear`.
- `do_not_build_until`: the exact signal required before the next implementation step.

## Money-Readiness Fields

Every opportunity record and every comparable `opportunities.json` entry must also include:

- `pain_score`: integer from 0 to 5.
- `spend_score`: integer from 0 to 5.
- `reachability_score`: integer from 0 to 5.
- `timing_score`: integer from 0 to 5.
- `buildability_score`: integer from 0 to 5.
- `technology_shift`: object with `what_changed`, `when`, `old_constraint`, `new_capability`, `cost_delta`, `quality_delta`, `latency_delta`, `accessibility_delta`, and `affected_workflows`.
- `buyer`: likely buyer or budget owner.
- `expensive_workflow`: workflow where the buyer loses time, money, quality, safety, compliance, or operational reliability.
- `existing_spend`: current spend, hiring, procurement, labor, consultant, tool, or workaround evidence.
- `paid_experiment`: the smallest paid or manually sellable test, including buyer, offer, channel, and success/failure threshold.
- `source_classes`: public source classes supporting the opportunity.
- `money_evidence_type`: one of `direct_workflow_spend`,
  `manual_labor_spend`, `competitor_revenue_signal`,
  `procurement_or_job_signal`, `budget_adjacency`, or `no_money_evidence`.
- `money_evidence`: concrete source-backed explanation for the money evidence
  classification.
- `existing_paid_workflow`: the workflow or outcome that is already paid for.
- `current_workaround`: how buyers solve the workflow now.
- `current_cost`: money or paid time cost when publicly estimable, otherwise
  `unclear`.
- `why_buy_from_us`: why the proposed wedge is better or easier to buy than the
  current workaround.
- `smallest_sellable_outcome`: one narrow paid outcome that can be delivered
  before product build-out.
- `manual_first_delivery`: how to fulfill the first order manually.
- `one_sentence_offer`: a buyer-understandable offer, such as "Send me X and I
  will return Y within 24 hours for $Z."
- `price_hypothesis`: a concrete starting price when evidence allows, or
  `unclear` when not selected.
- `buyer_acquisition_path`: where and how to find the first 20 plausible
  buyers without partnerships.
- `time_to_transaction_score`: integer from 1 to 5.
- `time_to_transaction_reason`: why the first transaction is or is not plausible
  within 7 days.
- `productization_path`: how manual service delivery could become a small
  repeatable software product.
- `cashflow_falsification_test`: what would disprove the opportunity within 7
  days.

Use this rough score interpretation:

- `0`: absent or disproven.
- `1`: weak, indirect, or only hypothesized.
- `2`: plausible and partially supported.
- `3`: supported by multiple public signals.
- `4`: strong, recent, and buyer-relevant.
- `5`: direct, recent, repeated, and economically urgent.

## Structural Opportunity Fields

Every opportunity record and every comparable `opportunities.json` entry must
also include:

- `structural_pattern`: the market-structure thesis, such as aggregation,
  routing, optimization, execution, procurement, reconciliation, or control
  plane.
- `primitive_growth`: what new primitives, providers, APIs, tools, models,
  protocols, vendors, or data sources multiplied recently, including time range
  when evidenced.
- `fragmentation_summary`: what is fragmented and why users face a choice.
- `manual_workflow`: the concrete workflow users do manually today, such as
  comparing providers, reconciling outputs, moving data between tools, writing
  custom scripts, or maintaining fallback logic.
- `objective_function`: a measurable objective or decision criterion, such as
  minimizing cost or latency subject to quality, maximizing yield, reducing
  risk, improving accuracy, or increasing availability.
- `execution_ladder`: how the opportunity can progress from observe to
  recommend to choose to execute.
- `economic_pain`: the cost of the current manual workflow or wrong choice.
- `timing_reason`: why the opportunity became more interesting in 2025-2026
  or another recent period, rather than being old known pain.
- `competitors`: existing competitors, adjacent products, OSS projects, or
  internal-workaround categories that address part of the problem.
- `structural_scores`: score object containing `fragmentation`, `manual_pain`,
  `economic_value`, `objective_measurability`, `execution_potential`, `timing`,
  `competition_gap`, `prototype_feasibility`, and `total`.

Structural score dimensions are integers from 0 to 5. Compute `total` as a
0-10 weighted score:

- fragmentation: 15%;
- manual pain: 15%;
- economic value: 20%;
- objective measurability: 10%;
- execution potential: 10%;
- timing: 10%;
- competitive gap: 10%;
- 1-2 week prototype feasibility: 10%.

Do not let an LLM assign a high structural score without citing evidence for
each dimension. If evidence is weak, score conservatively.

## Commercial Filter Fields

Every opportunity record and every comparable `opportunities.json` entry must
also include:

- `fragmented_providers`: concrete providers, protocols, products, APIs,
  vendors, infrastructure providers, or data sources that multiplied.
- `multi_provider_user`: the actual buyer or user who interacts with more than
  one provider. If customers usually pick one provider and stay there, say so
  explicitly.
- `boundary_workflow`: the ugly work at the boundary, such as normalization,
  adapters, routing, comparison, reconciliation, failover, orchestration,
  identity mapping, schema translation, policy enforcement, auditing,
  verification, settlement, billing reconciliation, migration, monitoring
  across vendors, or unified reporting.
- `build_vs_buy_reason`: why the buyer would buy this rather than build it
  internally. Classify the layer as core/strategic, non-core but necessary, or
  cross-company coordination.
- `internal_build_likelihood`: one of `low`, `medium`, or `high`.
- `money_flow`: who already pays whom in the underlying ecosystem, including
  usage-based pricing, enterprise contracts, infrastructure spend, transaction
  volume, hiring, consultants, or adjacent paid vendors.
- `recurrence`: why the boundary workflow repeats rather than being a one-time
  integration.
- `permissionless_validation`: how the wedge can be validated without private
  code, private data, hardware deployment, or incumbent permission.
- `smallest_wedge`: one narrow workflow a single engineer could validate in
  days or a few weeks. Do not write "platform for X" as the wedge.
- `intermediary_maturity`: whether incumbent aggregation/control layers are
  absent, immature, partial, or already satisfactory.

Prefer opportunities where `build_vs_buy_reason` is non-core but necessary or a
cross-company coordination problem. Penalize opportunities where the natural
buyer owns the entire stack, considers the layer core IP, has a large
engineering team, can solve it internally once, or rarely uses more than one
provider.

If `paid_wedge` is unclear, or if `private_data_barrier` is `private-code-required`, `private-data-required`, or `unclear`, the opportunity must stay in `watchlisted`. Do not put it in `selected` and do not mark it `selected-for-build`.

If `manual_workflow`, `objective_function`, `execution_ladder`, or
`timing_reason` is unclear, the opportunity must stay in `watchlisted`. Do not
put it in `selected`, `selected-for-test`, `sell-before-build`, or
`selected-for-build`.

If `multi_provider_user`, `boundary_workflow`, `build_vs_buy_reason`,
`money_flow`, `recurrence`, `permissionless_validation`, or `smallest_wedge` is
unclear, the opportunity must stay in `watchlisted`.

If `internal_build_likelihood` is `high`, the opportunity must stay in
`watchlisted` unless the report proves a separate cross-company buyer or
non-core purchase path. Do not rank high internal-build candidates near the top.

Reject selected opportunities whose `smallest_wedge` is only a platform,
marketplace, operating system, end-to-end suite, or generic AI-powered product.
The wedge should be a small workflow such as normalizing outputs, reconciling
usage or invoices, routing requests, generating adapters, detecting
disagreements, migrating config, or producing one cross-vendor audit trail.

`selected`, `selected-for-test`, and `sell-before-build` are only allowed when:

- `paid_wedge` names a concrete budget or painful cost;
- `money_evidence_type` is `direct_workflow_spend`, `manual_labor_spend`,
  `competitor_revenue_signal`, or `procurement_or_job_signal`;
- `spend_score` is at least 2;
- `reachability_score` is at least 2;
- `time_to_transaction_score` is at least 3 for `sell-before-build`;
- structural `manual_pain`, `economic_value`, `objective_measurability`,
  `execution_potential`, and `timing` scores are each at least 2;
- `internal_build_likelihood` is `low` or `medium`;
- `multi_provider_user`, `boundary_workflow`, `build_vs_buy_reason`,
  `money_flow`, `recurrence`, `permissionless_validation`, and `smallest_wedge`
  are concrete;
- `private_data_barrier` is `none` or `public-only`;
- `source_classes` contains at least two distinct classes and is not GitHub-only;
- `paid_experiment` names a concrete buyer, offer, channel, and success/failure threshold.
- `one_sentence_offer`, `buyer_acquisition_path`, `manual_first_delivery`, and
  `smallest_sellable_outcome` are concrete.

`selected-for-build` is only allowed when:

- `paid_wedge` names a concrete budget or painful cost;
- `spend_score` is at least 3;
- `reachability_score` is at least 3;
- `timing_score` is at least 2;
- `buildability_score` is at least 3;
- structural `execution_potential` and `prototype_feasibility` scores are each
  at least 3;
- `internal_build_likelihood` is `low`;
- `permissionless_validation` is concrete and does not require hardware
  deployment before validation;
- `smallest_wedge` is a narrow product-shaped workflow, not a platform;
- `private_data_barrier` is `none` or `public-only`;
- `distribution_channel` is credible;
- `product_shape` is one smallest testable artifact, not a product bundle;
- `source_classes` contains at least three distinct classes and is not GitHub-only;
- `paid_experiment` is already satisfied by evidence in the report;
- `do_not_build_until` has already been satisfied by evidence in the report.

## Outputs

Create `opportunity-reports/YYYY-MM-DD.md` containing:

- prerequisites and state;
- best paths to first transaction;
- signal counts;
- selected opportunities;
- executive summary;
- signal ledger;
- topic coverage;
- commercial delta;
- structural candidate ranking;
- structural score breakdown;
- commercial filter;
- opportunity reviews;
- build readiness table;
- money readiness table;
- recommended next test;
- rejected or deferred signals;
- evidence gaps.

The `Best Paths To First Transaction` section must contain at most five rows:

```markdown
| Opportunity | Buyer | Already paying for | Current workaround | One-sentence offer | Price hypothesis | Where to find first buyers | Time-to-transaction | Why now | Biggest uncertainty |
|---|---|---|---|---|---|---|---|---|---|
```

Every row must correspond to a `selected`, `selected-for-test`, or
`sell-before-build` entry in `opportunities.json`, and the offer, price,
acquisition path, and time-to-transaction score must match the state entry.

The report must also include `Interesting But Not Yet Commercial` for
LangGraph/Tailscale-style cases where technical pain exists but direct
willingness to pay for a standalone wedge is not proven.

The `Build Readiness` section must contain this table:

```markdown
| Opportunity | Paid wedge | Distribution channel | Private data barrier | OSS commoditization risk | Product shape | Pricing hypothesis | Do not build until | Build decision |
|---|---|---|---|---|---|---|---|---|
```

Use the same build-readiness values as `opportunities.json`. Every `Build Readiness` row must match an `opportunities.json` entry by title or id, and the build decision plus build-readiness fields must agree with the state entry. A report row with unclear paid wedge or private data/code requirements must have a watchlist build decision, not `selected` or `selected-for-build`.

The `Money Readiness` section must contain this table:

```markdown
| Opportunity | Pain | Spend | Reachability | Timing | Buildability | Buyer | Existing spend | Paid experiment | Source classes | Stage |
|---|---|---|---|---|---|---|---|---|---|---|
```

Use the same money-readiness values as `opportunities.json`. Every
`Money Readiness` row must match an `opportunities.json` entry by title or id,
and the stage plus money-readiness fields must agree with the state entry. A
report row with `spend_score < 2`, `reachability_score < 2`, or GitHub-only
source classes must have a watchlist build decision in `Build Readiness`.

The `Structural Candidate Ranking` section must contain this table:

```markdown
| Rank | Opportunity | Ecosystem | Score | Why now | Manual workflow | Wedge |
|---|---|---|---|---|---|---|
```

The `Structural Score Breakdown` section must contain this table:

```markdown
| Opportunity | Fragmentation | Manual pain | Economic value | Objective measurability | Execution potential | Timing | Competition gap | Prototype feasibility | Total |
|---|---|---|---|---|---|---|---|---|---|
```

Use the same structural values as `opportunities.json`. Every structural score
row must match an `opportunities.json` entry by title or id, and `Total` must
match the weighted structural total after deterministic recomputation.

The `Commercial Filter` section must contain this table:

```markdown
| Opportunity | Fragmented providers | Multi-provider user | Boundary workflow | Build-vs-buy | Internal build likelihood | Money flow | Permissionless validation | Smallest wedge | Decision |
|---|---|---|---|---|---|---|---|---|---|
```

Use the same commercial-filter values as `opportunities.json`. Every
Commercial Filter row must match an `opportunities.json` entry by title or id,
and the commercial-filter fields must agree with the state entry. A row with
`internal_build_likelihood` of `high`, unclear multi-provider usage, unclear
money flow, or a platform-shaped wedge must remain watchlisted.

For each selected opportunity, create or update one file under `opportunities/`.

Store raw or normalized signal notes under `signals/` for every URL used in the Signal Ledger. Do not copy large copyrighted content; store short summaries, URLs, dates, and evidence labels.

The `Signal Ledger` section must contain this table:

```markdown
| Source | URL | Family | Signal type | Source class | Evidence label | Decision | Reason |
|---|---|---|---|---|---|---|---|
```

Use `launch` as the source class for accelerator, demo-day, portfolio, batch,
Launch YC, company profile, and product-launch pages. Use `company-launch` as
the signal type when the signal is only the presence or positioning of a new
company/product, not independently evidenced pain or spend.

Prefer one signal note per source. When grouping multiple related sources into one signal note, include every source URL and the source dates or date range in that file.

Each signal note must include source URLs, source date or date range, topic
family, signal type, source class, market evidence labels, and concise notes.
For a report `opportunity-reports/YYYY-MM-DD.md`, every Signal Ledger URL must
appear in `signals/YYYY-MM-DD-*.md`.

Update `opportunities.json` with stable structured metadata using this schema:

```json
{
  "schema_version": 2,
  "generated_at": "YYYY-MM-DD",
  "discovery_mode": "broad-discovery|watchlist-directed|mixed|diagnostic",
  "selected": [
    {
      "id": "stable-slug",
      "family": "topic-family",
      "title": "Human readable title",
      "file": "opportunities/stable-slug.md",
      "stage": "selected|selected-for-test|sell-before-build|selected-for-build|deferred|watchlist|watchlisted",
      "score": 0,
      "pain_score": 0,
      "spend_score": 0,
      "reachability_score": 0,
      "timing_score": 0,
      "buildability_score": 0,
      "confidence": "low|medium-low|medium|medium-high|high",
      "money_signal": "none-found|weak|medium|strong",
      "reachability": "low|medium|high",
      "evidence_count": 0,
      "next_test": "One focused validation step.",
      "technology_shift": {
        "what_changed": "What changed in technology, regulation, platform, cost, hardware, or market timing.",
        "when": "When the shift became relevant.",
        "old_constraint": "Why the workflow was previously hard, expensive, slow, risky, or unreachable.",
        "new_capability": "What is newly possible.",
        "cost_delta": "How cost changed, or `unclear`.",
        "quality_delta": "How quality changed, or `unclear`.",
        "latency_delta": "How latency changed, or `unclear`.",
        "accessibility_delta": "How access changed, or `unclear`.",
        "affected_workflows": []
      },
      "buyer": "Likely buyer or budget owner.",
      "expensive_workflow": "Workflow with concrete time, money, compliance, quality, safety, or operational cost.",
      "existing_spend": "Existing spend, labor, hiring, procurement, consultant, tool, or workaround evidence.",
      "paid_experiment": "Smallest paid/manual validation offer.",
      "source_classes": ["github", "pricing"],
      "money_evidence_type": "direct_workflow_spend|manual_labor_spend|competitor_revenue_signal|procurement_or_job_signal|budget_adjacency|no_money_evidence",
      "money_evidence": "Concrete money evidence or reason it is only adjacent.",
      "existing_paid_workflow": "What exact workflow or outcome is already paid for.",
      "current_workaround": "How buyers solve it now.",
      "current_cost": "Current money or paid labor cost, or `unclear`.",
      "why_buy_from_us": "Why this wedge is better than the current workaround.",
      "smallest_sellable_outcome": "One narrow paid deliverable.",
      "manual_first_delivery": "How to deliver the first paid result manually.",
      "one_sentence_offer": "Send me X and I will return Y within 24 hours for $Z.",
      "price_hypothesis": "$99 per report",
      "buyer_acquisition_path": "Where to find the first 20 buyers.",
      "time_to_transaction_score": 3,
      "time_to_transaction_reason": "Why the first payment is plausible in seven days.",
      "productization_path": "How the manual workflow becomes software.",
      "cashflow_falsification_test": "What result in 7 days proves the opportunity weak.",
      "structural_pattern": "Aggregation, routing, optimization, execution, reconciliation, procurement, or control plane thesis.",
      "primitive_growth": "Recent primitive/provider/tool growth with dates or explicit uncertainty.",
      "fragmentation_summary": "What is fragmented and why users face a choice.",
      "manual_workflow": "Concrete manual workflow users perform today.",
      "objective_function": "Measurable objective or decision criterion.",
      "execution_ladder": {
        "observe": "What the product can observe first.",
        "recommend": "What recommendation it can make.",
        "choose": "What choice it can make under constraints.",
        "execute": "What action it can eventually execute."
      },
      "economic_pain": "Cost of current manual workflow or wrong choice.",
      "timing_reason": "Why this is newly interesting now.",
      "competitors": ["Existing competitor or adjacent workaround."],
      "structural_scores": {
        "fragmentation": 0,
        "manual_pain": 0,
        "economic_value": 0,
        "objective_measurability": 0,
        "execution_potential": 0,
        "timing": 0,
        "competition_gap": 0,
        "prototype_feasibility": 0,
        "total": 0
      },
      "fragmented_providers": "Concrete providers, protocols, APIs, products, vendors, or data sources that multiplied.",
      "multi_provider_user": "Who uses more than one provider, protocol, data source, or vendor.",
      "boundary_workflow": "Repeated cross-provider work at the boundary.",
      "build_vs_buy_reason": "Why this is non-core enough to buy instead of build internally.",
      "internal_build_likelihood": "low|medium|high",
      "money_flow": "Who already pays whom in the underlying ecosystem.",
      "recurrence": "Why the boundary work repeats instead of being one-time integration.",
      "permissionless_validation": "How the wedge can be validated without private code/data, hardware deployment, or incumbent permission.",
      "smallest_wedge": "One narrow first workflow, not a platform.",
      "intermediary_maturity": "Whether aggregation/control layers are absent, immature, partial, or satisfactory.",
      "paid_wedge": "What someone concretely pays for.",
      "distribution_channel": "How it is installed, bought, or adopted.",
      "private_data_barrier": "none|public-only|private-code-required|private-data-required|unclear",
      "oss_commoditization_risk": "low|medium|high|unclear",
      "product_shape": "cli|github-action|browser-extension|hosted-api|report|other|unclear",
      "pricing_hypothesis": "free|team|pro|unclear",
      "do_not_build_until": "Evidence required before the next build step.",
      "labels": []
    }
  ],
  "deferred": [],
  "watchlisted": []
}
```

Keep `selected`, `deferred`, and `watchlisted` as arrays of comparable objects. Do not replace them with maps or omit them when empty.

Keep each entry's `stage` consistent with the containing array:

- `selected`: `selected`, `selected-for-test`, `sell-before-build`, or `selected-for-build`;
- `deferred`: `deferred`;
- `watchlisted`: `watchlist` or `watchlisted`.

## Selected Opportunity Contract

Each selected opportunity file must include:

- opportunity summary;
- evidence, with each important evidence bullet prefixed by a market label such as `M2 repeated pain:`;
- repeated pain or demand signal;
- likely user or buyer;
- current workaround or money signal;
- technology shift;
- buyer;
- expensive workflow;
- existing spend;
- paid experiment;
- money-first scores;
- source classes;
- fragmented providers;
- multi-provider user;
- boundary workflow;
- build-vs-buy reason;
- internal build likelihood;
- money flow;
- recurrence;
- permissionless validation;
- smallest wedge;
- intermediary maturity;
- paid wedge;
- distribution channel;
- private data barrier;
- OSS commoditization risk;
- product shape;
- pricing hypothesis;
- do not build until;
- proposed offer;
- success threshold;
- falsification threshold;
- evidence gaps;
- decision.

## Quality Bar

Prefer:

- one demand signal with independent corroboration over ten plausible ideas;
- explicit evidence gaps over confident speculation;
- one focused manual test over scattered build recommendations;
- a paid/manual sell-before-build test over speculative implementation;
- rejection over weak selection.

Do not recommend building multiple artifacts in the same run unless they test the same buyer, channel, and success metric. Pick the strongest opportunity and make the other candidates watchlist follow-ups when evidence is weaker.

Every recommendation must connect:

```text
observed demand signal -> evidence source -> repeated pain or money/workaround proof -> likely buyer/user -> testable offer -> success/failure threshold
```
