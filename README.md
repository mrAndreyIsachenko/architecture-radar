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
- `.github/workflows/architecture-radar.yml` - scheduled GitHub Actions runner.

## Current Radar Highlights

- [Schema-Faceted Provenance Event Envelope](patterns/schema-faceted-provenance-event-envelope.md) - typed, producer-scoped event facets for evidence-backed execution graphs.
- [Finality-Aware Hot/Cold Projection](patterns/finality-aware-hot-cold-projection.md) - reorg-aware blockchain materialization with finalized and hot block state.

## Operating Principles

- Treat `interests.md` as authoritative.
- Prefer verified source evidence over README summaries.
- Pin every repository review to a full commit SHA.
- Select zero repositories when no candidate clears the quality bar.
- Extract narrow reusable mechanisms, not product recommendations.
- Update `README.md` only when the cumulative architecture radar materially changes.

## Scheduled Research

The GitHub Actions workflow runs daily at 08:00 Europe/Moscow and can also be started manually from the Actions tab.

Required repository setup:

- Add an `OPENAI_API_KEY` repository secret.
- Ensure GitHub Actions has permission to write repository contents and create pull requests.

The workflow lets Codex modify research artifacts, then a deterministic wrapper commits the changes to a dated branch and opens a pull request. The agent step does not receive `GITHUB_TOKEN`.
