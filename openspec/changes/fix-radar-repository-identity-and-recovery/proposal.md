## Why

Architecture Radar run 36121754617 failed on 2026-09-25 because the report used
`bumblebee` while its validation backlog used `Sri-Krishna-V/bumblebee`.
The research completed, but strict validation blocked publication and the
ephemeral runner left no downloadable research artifact for recovery.

## What Changes

- Repair abbreviated report repository identities only when structured source
  references establish one unambiguous canonical identity; retain strict rejection
  of conflicting or ambiguous identities.
- Require consistent repository identity in the candidate ledger, backlog table,
  radar state, and research-agent completion checks.
- Preserve allowlisted generated research files and run metadata on failure,
  without uploading credentials, external clones, or raw agent logs.
- Recover the September 25 output from available log evidence where complete,
  and validate it without a new paid research run.
- Add regression coverage for the observed mismatch and recovery boundaries.

Non-goals: changing research ranking, model selection, cadence, branch protection,
the separate pending-approval/check-marker incident, automatic merging, or
automatically launching paid retries.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `architecture-radar`: deterministic repository-identity repair and recoverable
  generated output when research or validation fails.

## Impact

`scripts/repair-radar-report-structure.py`, its focused tests,
`scripts/run-codex-radar.sh`, `.github/workflows/architecture-radar.yml`, and
related operational documentation. Recovery may restore generated research
artifacts, but must not publish them without passing the existing validators.
No new runtime dependency is required for identity repair.
