# Design

## Behavior

`scripts/repair-radar-report-structure.py` already runs after the model writes
Architecture Radar artifacts and before `scripts/validate-radar-state.py`.
This change extends that repair step to canonicalize recoverable validation
type phrases in:

- `experiments/failure-injection-backlog.yml`
- the report `Validation Backlog Updates` table

The repair chooses one primary enum value from the existing allowlist:

- `runtime`
- `failure-injection`
- `restart-recovery`
- `reconnect-recovery`
- `replay`
- `sitl`
- `fleet`
- `operational`

Specific recovery or execution modes win over broader terms. For example,
`runtime validation and failure-injection` normalizes to
`failure-injection`, while the remaining nuance belongs in `evidence_gap` or
`proposed_validation`.

## Failure Mode

If the value cannot be mapped to a known enum, repair leaves it unchanged so
strict validation still fails with the existing schema error.

## Cost And Security

The change is local and deterministic. It does not add network calls,
credentials, dependencies, or model usage.
