## Context

The PR governance gate validates pull request body fields for all pull_request
events. Generated PR publishers must therefore emit the same metadata that a
human-authored agent PR is expected to record.

## Decision

Update the three publisher scripts:

- `scripts/publish-radar-run.sh`;
- `scripts/publish-opportunity-radar-run.sh`;
- `scripts/publish-weekly-synthesis-run.sh`.

Each script will add an `Agent Governance` section to the generated body before
the review checklist. The `User request` value will describe the workflow event
that created the PR. `Scope confirmed` will be `yes` because the workflow
allowlist controls which paths are staged. `Autonomous follow-up` will be `no`
because these PRs are the direct output of scheduled or manually dispatched
workflows, not continuation work inferred from a chat acknowledgement.

Generated research artifacts remain exempt from requiring OpenSpec evidence by
the existing validator; the body still records `OpenSpec change: Not required;
generated research artifact PR.`

## Non-Goals

- Do not change generated artifact content.
- Do not change workflow schedules.
- Do not make generated PRs merge automatically.
- Do not weaken `scripts/validate-agent-governance.py`.
