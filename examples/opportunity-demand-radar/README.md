# Opportunity Demand Radar

This example adapts Architecture Radar from open-source architecture research to opportunity and demand research.

The goal is not to generate startup ideas from vibes. The goal is to collect evidence-backed signals about:

- repeated pain points;
- fast-growing tool categories;
- unsolved workflow gaps;
- buyer urgency;
- broken incumbent solutions;
- open-source projects that may indicate emerging demand;
- infrastructure shifts that create new surface area.

Use this when you want an agent to open reviewable PRs about market demand rather than send a noisy newsletter.

## Files

- `interests.md` — example opportunity research priorities.
- `research-scope.md` — discovery surface and signal definitions.
- `watchlist.yml` — seed sources and projects the radar should not miss.

## How To Use

The root repository now includes a separate Opportunity Radar mode. Use this example as a template when replacing those root files:

```bash
cp examples/opportunity-demand-radar/interests.md opportunity-interests.md
cp examples/opportunity-demand-radar/research-scope.md docs/opportunity-research-scope.md
cp examples/opportunity-demand-radar/watchlist.yml opportunity-watchlist.yml
```

Then run `Opportunity Radar` manually from GitHub Actions, or let the weekly
schedule run after the root workflow is configured.

## Quality Bar

The radar should reject an opportunity unless it can connect:

```text
observed demand signal -> evidence source -> repeated pain -> plausible buyer/user -> testable next step
```

Every selected opportunity should also name the paid wedge, distribution
channel, private-data barrier, OSS commoditization risk, product shape, pricing
hypothesis, technology shift, buyer, expensive workflow, existing spend, paid
experiment, source classes, and the signal required before more build work.

GitHub-only pain should stay watchlisted. Use `sell-before-build` when the next
useful action is a paid/manual report, audit, review, or sample transformation
before implementation.

Useful output is a small number of evidence-backed opportunities, not a large list of plausible markets.
