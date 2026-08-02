# Architecture Radar

Evidence-backed research into reusable architectural mechanisms found in open-source projects.

This repository is a persistent knowledge base, not a newsletter archive. Each run should improve our ability to make engineering decisions by recording verified mechanisms, trade-offs, evidence, and adoption conditions.

## Structure

- `interests.md` - current projects, unresolved problems, constraints, and research priorities.
- `reports/` - dated research runs and candidate ledgers.
- `repositories/` - source-level reviews pinned to specific commits.
- `patterns/` - reusable architectural patterns extracted across repositories.
- `radar.json` - structured radar metadata.
- `docs/architecture-radar-agent.md` - operating prompt for the research agent.

## Operating Principles

- Treat `interests.md` as authoritative.
- Prefer verified source evidence over README summaries.
- Pin every repository review to a full commit SHA.
- Select zero repositories when no candidate clears the quality bar.
- Extract narrow reusable mechanisms, not product recommendations.
- Update `README.md` only when the cumulative architecture radar materially changes.
