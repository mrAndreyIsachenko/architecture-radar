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

## Operating Principles

- Treat `interests.md` as authoritative.
- Prefer verified source evidence over README summaries.
- Pin every repository review to a full commit SHA.
- Select zero repositories when no candidate clears the quality bar.
- Extract narrow reusable mechanisms, not product recommendations.
- Update `README.md` only when the cumulative architecture radar materially changes.

## Current Radar Themes

- Evidence-carrying execution envelopes: checkpoint, lineage-event, and source-episode envelopes that preserve producer/schema identity, parent-child causality, recovery state, and links from derived claims back to source evidence.
- Reorg-safe materialization windows: provisional/finalized block splits plus explicit rollback and catchup workers that keep blockchain indexes recoverable after chain reorganizations.

## Scheduled Research

The GitHub Actions workflow checks cadence daily, but runs the expensive Codex research step every three days at 08:00 Europe/Moscow. It can also be started manually from the Actions tab.

The default Codex model is `gpt-5.4-mini` to keep recurring research costs under control. To switch recurring runs to another allowed model, set the repository variable `ARCHITECTURE_RADAR_CODEX_MODEL`; manual runs can also override the model from the Actions tab, for example to use `gpt-5.5` for a high-stakes follow-up.

Same-day manual reruns are guarded to avoid spending model tokens when `reports/YYYY-MM-DD.md` already exists. The guard still allows a supplemental run when `interests.md` or `docs/architecture-radar-agent.md` changed after the existing report. In that case the agent writes `reports/YYYY-MM-DD-supplement-N.md` and focuses on changed or under-covered topic families. Use the `force_research` workflow input only when you explicitly want another same-day supplement without a scope change.

Required repository setup:

- Add an `OPENAI_API_KEY` repository secret.
- Ensure GitHub Actions has permission to write repository contents and create pull requests.

The workflow lets Codex modify research artifacts, then a deterministic wrapper commits the changes to a dated branch and opens a pull request. The agent step does not receive `GITHUB_TOKEN`.
