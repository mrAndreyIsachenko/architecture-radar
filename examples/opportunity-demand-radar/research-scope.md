# Opportunity Demand Research Scope

Domain configuration for the Opportunity Demand Radar. This file answers what to look for.

The operating rules live in `docs/agent-rules.md` and remain domain-independent. `interests.md` is still authoritative for concrete priorities.

## Topic Families

Use these families for candidate accounting and selection:

- `ai-llm-demand`
- `blockchain-demand`
- `privacy-networking-demand`
- `drones-robotics-demand`
- `document-ai-demand`

## Discovery Sources

Use a mix of:

- GitHub repositories, issues, discussions, releases, and dependency links;
- open-source project roadmaps and changelogs;
- Hacker News, Reddit, Discord/Slack exports when available, forums, and mailing lists;
- product launch comments and public feedback threads;
- job posts and role descriptions that reveal repeated workflow pain;
- benchmark, dataset, or model-release discussions;
- documentation pages where maintainers describe limitations;
- competing product docs and pricing pages when relevant.

Prefer primary evidence. Treat social posts and launch comments as weak signals unless the same pain repeats across independent sources.

## Signal Types

Classify each candidate signal:

- `repeated-pain` — multiple independent users describe the same problem.
- `workaround-economy` — users maintain scripts, spreadsheets, forks, or manual process because tooling is missing.
- `integration-gap` — active projects need glue between systems that do not fit cleanly.
- `operational-risk` — failures are expensive, risky, or hard to debug.
- `infrastructure-shift` — new model, protocol, hardware, regulation, or platform change creates fresh demand.
- `incumbent-friction` — existing tools are adopted but users repeatedly complain about cost, complexity, lock-in, reliability, or missing features.
- `open-source-commercialization` — strong OSS usage but clear need for hosted, managed, secure, or enterprise-ready workflows.

## Required Analysis

For each selected opportunity, explain:

1. What demand signal was observed.
2. Which evidence sources support it.
3. Whether the signal is repeated across independent sources.
4. Which source classes support it and whether it is GitHub-only.
5. What technology or market shift makes the timing relevant.
6. Who likely buys or approves the spend.
7. What workflow or budget it attaches to.
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

## Evidence Discipline

Use market-specific labels:

- `M1 paid demand`: public evidence that users pay, hire, procure, subscribe, or allocate budget for the problem.
- `M2 repeated pain`: independent public evidence that the same pain repeats across users, issues, posts, or forums.
- `M3 competitor proof`: existing products, hosted services, consultants, or OSS projects indicate active demand.
- `M4 workaround evidence`: users maintain scripts, spreadsheets, forks, manual processes, or brittle glue to solve the problem.
- `I interpretation`: synthesis derived from evidence.
- `H hypothesis`: plausible but not sufficiently verified.

Do not relabel public comments or docs as paid demand unless they show actual budget, procurement, hiring, subscription, or paid workaround evidence.

## Selection Rule

Select no more than three opportunities per run.

Selecting zero is valid when evidence is thin, noisy, or not connected to a testable next step.

Do not select an opportunity because it is exciting. Select it because there is enough evidence to justify a small experiment.

If the paid wedge is unclear, if spend evidence is weak, if reachability is weak, if evidence is GitHub-only, or if the useful next test requires private code or private data, keep the opportunity in watchlist. Do not select it and do not mark it selected for build.

Use `sell-before-build` when the next useful action is a paid/manual offer,
sample transformation, report, audit, or review before implementation.
