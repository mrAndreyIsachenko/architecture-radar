# Validation Evidence

Implementation base: `e8e7441cb82e03ef52f71133615d38aa4ef40a70` (main fetched on
2026-09-25). The workspace moved to this commit without creating a branch,
discarding user changes, committing, or publishing anything.

## Incident Recovery

Source: https://github.com/mrAndreyIsachenko/architecture-radar/actions/runs/36121754617

The downloaded log archive SHA-256 is
`497bfc37c3ac4299f7c28d65b4b41c1325a77d2e7bb4ff771d519b2134d8236d`.
Final complete diff blocks were parsed as data, with hunk lengths checked,
allowlisted paths only, and `git apply --check` against the recorded base.
No commands from the log were executed. All ten reconstructed file blob hashes
matched the full destination hashes printed in the log:

| File | Original recovered Git blob |
|---|---|
| experiments/failure-injection-backlog.yml | 08e1523841acc82d20acf2d38d630b01db5b5b2c |
| patterns/deferred-image-materialization.md | dca610c862ae7f33920e77f499148dc7e82b2d6c |
| patterns/mission-failsafe-fallback-state-machine.md | b879ea5878b0f3cb7e940c31d5ca5c61f93a3ace |
| patterns/policy-guarded-route-reconciliation-loop.md | aee8ded3512f02e000955a467c75e4f65ca6917c |
| radar.json | c728da6510b4485735fdd9261a3c07ae3d21d256 |
| reports/2026-09-25.md | bbe99de1cddacc4a92d1123cb9a5b7a2b82e667b |
| repositories/Amirhat-riftroute.md | 14488d74cbcc9ccfe0a411b7fb773507efbd6c81 |
| repositories/Pratyush150-ros2-drone-bringup.md | 8472d8dcc67438b5b2367c6e169ac5842206a4d7 |
| repositories/bumblebee.md | 4a3a8d4d4e4064f9f5c1b0b4c902fda830dd7989 |
| repositories/miksrv-cubesat-sim.md | 71ec4bef0fe47489ee282a8ebb0b44c7a7bead60 |

No file listed in the agent's final output was missing or truncated. This proves
reconstruction of the generated data, not independent verification of research
claims or production readiness of the reviewed repositories.

The unchanged recovered output reproduced the exact strict validation failure:

```text
repository mismatch: bumblebee != Sri-Krishna-V/bumblebee
```

In an independent reconstruction, the new repair script alone fixed this
identity mismatch and the unmodified full validator printed
`radar artifacts validated`. It used the complete `.git` source URL in radar
and matching backlog reference; local clone paths were not treated as evidence.

The delivery copy additionally replaces eleven temporary ledger URLs with the
public URLs observed in the run's clone commands. The repair then expands the
four short names in structured cells; prose and research conclusions are not
rewritten. Full validation passes on this copy too.

Local recovery checkout: `/tmp/radar-recovery-36121754617`.
Independent regression checkout: `/tmp/radar-regression-36121754617`.
Original verified patch: `/tmp/radar-recovery-36121754617.patch`.
Per-file inventory: `/tmp/radar-recovery-36121754617-inventory.json`.
These are local temporary artifacts, not published GitHub artifacts.

## Local Checks

- `python3 -m unittest discover -s tests`: 186 passed, including 22 new tests.
- `openspec validate --all --strict --no-interactive`: 27 passed, 0 failed.
- `actionlint` 1.7.7 on `architecture-radar.yml`: passed (shellcheck disabled;
  changed shell script checked separately with `bash -n`).
- Architecture, opportunity, and weekly state validators: passed.
- Setup doctor: 169 pass, 1 warning for intentionally skipped remote checks.
- Agent-governance negative self-test: passed.
- Python compilation, changed shell syntax, and `git diff --check`: passed.

Unit tests reproduce strict rejection before identity repair and acceptance
after repair while rejecting conflicting references. They also cover recovery
allowlisting, file and directory symlinks, empty and
partial output, provenance filtering, workflow failure/skip conditions, and
preservation of failed status. These tests are not proof of a hosted upload.

## Remaining Acceptance

Task 3.4 remains open until hosted proof is recorded. The manual `recovery_smoke`
input skips production research and runs the real validator against an invalid
fixture, with the identical recovery steps and read-only job permissions. No
paid model invocation is needed. Expected proof: validator failed, publication
sentinel skipped, recovery uploaded, downloaded checksums verified, and failed
workflow conclusion. Do not mark the change fully operational before that proof.
