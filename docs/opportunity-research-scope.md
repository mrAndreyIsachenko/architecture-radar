# Opportunity Radar Research Scope

Domain configuration for Opportunity Radar. This file answers what to look for. The operating rules live in [`opportunity-agent-rules.md`](opportunity-agent-rules.md).

## Topic Families

Use these families for signal accounting and selection:

- `ai-llm-demand`
- `blockchain-demand`
- `privacy-networking-demand`
- `drones-robotics-demand`
- `document-ai-demand`

## Discovery Sources

Use public, inspectable sources such as:

- GitHub issues, discussions, releases, dependency links, and project roadmaps;
- Hacker News, Reddit, public forums, mailing lists, and public launch comments;
- product docs, pricing pages, public changelogs, and public support pages;
- job posts and role descriptions that reveal workflow pain or budget;
- benchmark, dataset, model-release, and hardware-release discussions;
- app reviews or marketplace listings when they are public and attributable.

Do not use private communities, authenticated exports, personal data, or outbound outreach in the first implementation.

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

Score every selected, deferred, and watchlisted opportunity from 0 to 5:

- `pain_score`;
- `spend_score`;
- `reachability_score`;
- `timing_score`;
- `buildability_score`.

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

Select no more than three opportunities per manual run.

Selecting zero is valid when evidence is thin, noisy, or not connected to a testable next step.

Do not select an opportunity because it is exciting. Select it because there is enough evidence to justify a small experiment.

If the paid wedge is unclear, if `spend_score < 2`, if `reachability_score < 2`, if the opportunity is GitHub-only, or if the useful next test requires private code or private data, keep the opportunity in watchlist. Do not select it and do not mark it selected for build.

Use `sell-before-build` when the next useful action is a paid/manual offer,
sample transformation, report, audit, or review before implementation. Do not
recommend building unless the paid experiment has already been validated by
evidence in the report.
