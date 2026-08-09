# GitHub Actions Setup

Architecture Radar can run as a scheduled GitHub Actions workflow.

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

The workflow runs at 05:00 UTC, which is 08:00 Europe/Moscow.

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
python3 scripts/radar-pr-review-status.py --format markdown
```

The helper checks open radar pull requests before returning a no-work result. On a cadence day, if the scheduled run is missing, queued, or still in progress, it prints `DONT_NOTIFY` so the heartbeat can wait for a later check instead of claiming there is no PR.

For failed runs, add `--include-failed-log` to include a short actionable excerpt from `gh run view --log-failed`.

## Expected Failure Modes

- Missing `OPENAI_API_KEY`: the workflow fails before research starts.
- Missing report file for the run date: validation fails.
- No file changes: the publish step exits without opening a PR.
- GitHub token lacks write permissions: publish fails after research artifacts are produced in the runner.
