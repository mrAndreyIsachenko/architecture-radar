# GitHub Actions Setup

Architecture Radar can run as scheduled GitHub Actions workflows.

For a fork-to-first-PR setup path, start with [`../QUICKSTART.md`](../QUICKSTART.md). This page documents the workflow mechanics in more detail.

## Required Secret

Create a repository secret:

- `OPENAI_API_KEY` - API key used by `codex login --with-api-key`.

The workflow uses the built-in `GITHUB_TOKEN` only in the final publish step. The Codex research step does not receive `GITHUB_TOKEN`.

## Repository Permissions

In repository settings, ensure Actions can:

- write repository contents;
- create pull requests.

The workflow also declares:

```yaml
permissions:
  contents: write
  pull-requests: write
```

## Schedule

Architecture Radar runs at 05:00 UTC, which is 08:00 Europe/Moscow. A cadence gate lets the expensive research step run every three days.

Weekly Synthesis runs at 04:30 UTC every Monday, which is 07:30 Europe/Moscow. It reads committed artifacts and writes `weekly-reports/YYYY-Www.md`; it does not perform new discovery.

Manual runs are available through `workflow_dispatch`. The optional `run_date` input overrides the report date and must use `YYYY-MM-DD`.

## Execution Model

1. Check out `main`.
2. Install Codex CLI from npm.
3. Authenticate Codex with `OPENAI_API_KEY`.
4. Create a dated branch.
5. Run Codex against `docs/agent-rules.md` plus `docs/research-scope.md`.
6. Validate required artifacts and `radar.json`.
7. Commit changes.
8. Push the branch.
9. Open a pull request.

The agent is instructed not to commit, push, edit remotes, or open pull requests itself.

## Reviewing Generated Pull Requests

Use the local helper to decide whether a review notification is warranted:

```bash
python3 scripts/radar-pr-review.py --format markdown --include-failed-log
```

The helper checks open radar pull requests before returning a no-work result. On a cadence day, if the scheduled run is missing, queued, or still in progress, it prints `DONT_NOTIFY` so the heartbeat can wait for a later check instead of claiming there is no PR. For fresh radar PRs, it summarizes the PR metadata, checks, changed radar artifacts, changed report files, and a `looks_mergeable` or `needs_manual_review` recommendation.

For failed runs, `--include-failed-log` includes a short actionable excerpt from `gh run view --log-failed`.

After checking out the PR branch, summarize the report for review:

```bash
python3 scripts/summarize-radar-report.py reports/YYYY-MM-DD.md --format markdown
```

To summarize an open PR without a local checkout of its branch:

```bash
python3 scripts/summarize-radar-pr.py PR_NUMBER --format markdown
```

## Expected Failure Modes

- Missing `OPENAI_API_KEY`: the workflow fails before research starts.
- Missing report file for the run date: validation fails.
- Missing weekly synthesis report for the week id: weekly validation fails.
- No file changes: the publish step exits without opening a PR.
- GitHub token lacks write permissions: publish fails after research artifacts are produced in the runner.
