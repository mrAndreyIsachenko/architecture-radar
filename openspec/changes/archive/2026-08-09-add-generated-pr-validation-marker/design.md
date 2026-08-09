# Design: Generated PR Validation Marker

## Trigger

Add `.github/workflows/generated-pr-validation.yml` using `workflow_run` for:

- `Architecture Radar`
- `Opportunity Radar`
- `Weekly Synthesis`

The job runs only when the source workflow completed successfully.

## Matching

Generated branches already include the source workflow run number:

- `architecture-radar/YYYY-MM-DD-RUN_NUMBER`
- `opportunity-radar/YYYY-MM-DD-RUN_NUMBER`
- `weekly-synthesis/YYYY-Www-RUN_NUMBER`

The marker script receives the source workflow name and run number from `github.event.workflow_run`, lists open pull requests, and selects PRs whose head branch has the expected prefix and suffix.

## Marker

For each matched PR, create a completed check-run:

- `name`: `validate`
- `head_sha`: PR head SHA
- `conclusion`: `success`
- `details_url`: source workflow run URL

This is not a replacement for validation. It is a marker that the generator workflow already completed its deterministic validation steps before publishing.

## Permissions

The marker workflow needs:

- `contents: read`
- `pull-requests: read`
- `checks: write`

## Failure Behavior

If the source workflow failed, do nothing.

If no matching PR exists, exit successfully; some generator runs legitimately produce no changes.

If creating a marker fails, fail the marker workflow so the issue is visible.
