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
4. Who likely experiences the pain.
5. What workflow or budget it attaches to.
6. What current alternatives exist.
7. Why those alternatives appear insufficient.
8. What small experiment could test demand within one week.
9. What would falsify the opportunity.
10. What should explicitly not be built.

## Evidence Discipline

Keep the same evidence labels used by Architecture Radar:

- `E1 source verified` for implementation evidence.
- `E2 test verified` for tests or reproducible evaluation code.
- `E3 maintainer stated` for docs, changelogs, roadmaps, issues, posts, and comments.
- `I interpretation` for the agent's synthesis.
- `H hypothesis` for plausible but unverified opportunity claims.

For demand research, most market signals will be `E3`, `I`, or `H`. Do not relabel public comments or docs as `E1`.

## Selection Rule

Select no more than three opportunities per run.

Selecting zero is valid when evidence is thin, noisy, or not connected to a testable next step.

Do not select an opportunity because it is exciting. Select it because there is enough evidence to justify a small experiment.
