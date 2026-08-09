# Quick Start

Use this guide to run your own scheduled research radar from this repository.

## 1. Fork Or Clone

Fork the repository on GitHub, or clone it into a new repository that will hold your research artifacts.

```bash
git clone git@github.com:YOUR_ORG_OR_USER/architecture-radar.git
cd architecture-radar
```

The repository must contain these files and directories:

- `interests.md`
- `watchlist.yml`
- `docs/agent-rules.md`
- `docs/research-scope.md`
- `radar.json`
- `reports/`
- `repositories/`
- `patterns/`

## 2. Configure GitHub Actions

In repository settings, enable workflow write access:

1. Open `Settings -> Actions -> General`.
2. Under `Workflow permissions`, choose `Read and write permissions`.
3. Enable `Allow GitHub Actions to create and approve pull requests`.

The workflow also declares the required token permissions:

```yaml
permissions:
  contents: write
  pull-requests: write
```

## 3. Add OpenAI Credentials

Create a repository secret:

- `OPENAI_API_KEY`

GitHub path:

`Settings -> Secrets and variables -> Actions -> New repository secret`

The Codex research step receives this OpenAI key. It does not receive `GITHUB_TOKEN`. Publishing happens later in a separate workflow step with an explicit file allowlist.

## 4. Choose A Model

The workflow defaults to:

```text
gpt-5.4-mini
```

That is the recommended default for recurring runs because the radar can spend a lot of input tokens while inspecting repositories.

To change the default, add a repository variable:

- `ARCHITECTURE_RADAR_CODEX_MODEL`

GitHub path:

`Settings -> Secrets and variables -> Actions -> Variables -> New repository variable`

You can also override the model for one manual run from the workflow dispatch form.

## 5. Replace The Research Scope

Edit these files before the first real run:

| File | What to change |
|---|---|
| `interests.md` | Your concrete projects, unresolved problems, constraints, useful mechanisms, and things to avoid |
| `docs/research-scope.md` | Topic families, search areas, mechanism examples, and discovery seeds |
| `watchlist.yml` | Repositories, models, datasets, or benchmarks that broad discovery must not miss |

Keep `docs/agent-rules.md` stable unless you are changing how the agent operates. That file is the domain-independent research protocol.

For a ready-made non-architecture example, see [`examples/opportunity-demand-radar/`](examples/opportunity-demand-radar/).

## 6. Run It Manually Once

Open:

`Actions -> Architecture Radar -> Run workflow`

Useful inputs:

| Input | Use |
|---|---|
| `run_date` | Optional `YYYY-MM-DD` report date override |
| `model` | Optional one-run model override |
| `force_research` | Run even when today's report already exists |

Manual runs bypass the cadence gate. Same-day reruns still respect the rerun guard unless `force_research` is enabled or the scope files changed.

## 7. Review The Generated PR

After a successful run, the workflow opens a PR titled like:

```text
Architecture Radar YYYY-MM-DD
```

Use the helper locally to summarize what changed:

```bash
python3 scripts/radar-pr-review.py --format markdown --include-failed-log
```

For a specific open PR:

```bash
python3 scripts/summarize-radar-pr.py PR_NUMBER --format markdown
```

After checking out the PR branch, summarize the report directly:

```bash
python3 scripts/summarize-radar-report.py reports/YYYY-MM-DD.md --format markdown
```

Do not auto-merge generated research PRs. The workflow is designed to make the output reviewable, not to make it self-authorizing.

## 8. Protect `main`

For public or shared use, add a branch protection rule for `main`:

- require pull requests before merging;
- require the `validate` status check;
- require conversation resolution if you use PR review comments;
- block force pushes and branch deletion.

This keeps generated research artifacts behind deterministic validation and human review.

## 9. Understand The Cost Model

Recurring cost is mostly driven by:

- number of candidate repositories inspected;
- amount of source read per candidate;
- model choice;
- whether the rerun guard skips unchanged days;
- whether manual `force_research` runs are used frequently.

The default schedule wakes daily but runs expensive research every three days. Same-day reruns become supplements only when the scope changed or `force_research` is set.

## 10. Privacy Notes

The model sees the repository contents needed for research, including `interests.md`, `docs/research-scope.md`, and generated artifacts. Do not put secrets or sensitive internal architecture details in those files unless your OpenAI project and GitHub repository settings are configured for that data.

The generated PRs may include external repository links, commit SHAs, file paths, and evidence summaries. Review them before merging into a public repository.

Before actively promoting a public fork, run through [`docs/publication-checklist.md`](docs/publication-checklist.md).
