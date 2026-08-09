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

Use this when you want a recurring agent to open reviewable PRs about market demand rather than send a noisy newsletter.

## Files

- `interests.md` — example opportunity research priorities.
- `research-scope.md` — discovery surface and signal definitions.
- `watchlist.yml` — seed sources and projects the radar should not miss.

## How To Use

Copy these files into the root repository:

```bash
cp examples/opportunity-demand-radar/interests.md interests.md
cp examples/opportunity-demand-radar/research-scope.md docs/research-scope.md
cp examples/opportunity-demand-radar/watchlist.yml watchlist.yml
```

Then run `Architecture Radar` manually from GitHub Actions.

## Quality Bar

The radar should reject an opportunity unless it can connect:

```text
observed demand signal -> evidence source -> repeated pain -> plausible buyer/user -> testable next step
```

Useful output is a small number of evidence-backed opportunities, not a large list of plausible markets.
