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
4. Who likely experiences the pain.
5. What workflow or budget it attaches to.
6. What current alternatives exist.
7. Why those alternatives appear insufficient.
8. What small experiment could test demand within one week.
9. What would falsify the opportunity.
10. What should explicitly not be built.

## Evidence Labels

Use market-specific labels:

- `M1 paid demand`: public evidence that users pay, hire, procure, subscribe, or allocate budget for the problem.
- `M2 repeated pain`: independent public evidence that the same pain repeats across users, issues, posts, or forums.
- `M3 competitor proof`: existing products, hosted services, consultants, or OSS projects indicate active demand.
- `M4 workaround evidence`: users maintain scripts, spreadsheets, forks, manual processes, or brittle glue to solve the problem.
- `I interpretation`: synthesis derived from evidence.
- `H hypothesis`: plausible but not sufficiently verified.

Use `H hypothesis` when evidence is thin. Do not relabel source code or docs as market evidence unless they show demand, pain, competitor proof, or workaround behavior.

## Selection Rule

Select no more than three opportunities per manual run.

Selecting zero is valid when evidence is thin, noisy, or not connected to a testable next step.

Do not select an opportunity because it is exciting. Select it because there is enough evidence to justify a small experiment.
