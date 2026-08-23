# alireza787b/mavsdk_drone_show

- Repository: https://github.com/alireza787b/mavsdk_drone_show
- Review date: 2026-08-23
- Current commit reviewed: `39ce5601e9d47eafdd3a6ccffd3c1caba3f08cad`
- Commit date: 2026-08-22
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `drones-robotics-autonomy`, especially mission admission, callback safety, restart recovery, and durable command tracking. It also informs `evidence-backed reasoning` and `durable workflows` because the interesting surface is the command journal and the structured evidence bundle, not the drone-show branding.

## Verified Flow

`command_execution_policy.enforce_command_submission_policy` checks typed submission authority, mission class, and strict-sync timing -> `command_submission_pipeline.ensure_sitl_callback_endpoint_matches` fails closed when the active SITL fleet points to a different GCS endpoint -> `record_launch_preparations` persists readiness as preparation evidence rather than as an ACK -> `_dispatch_command` requires a live fleet RPC service and returns delivery-unknown when dispatch cannot proceed -> `CommandJournal` persists immutable command identity, per-target execution state, and append-only events in SQLite WAL while keeping the callback capability in a separate secured file -> `ReadOnlyEvidenceBundle` and `ReadOnlyEvidenceItem` package sanitized answer evidence for operator-facing follow-up -> restart-safety tests prove the tracker survives process loss and replay.

- E1 source verified: `gcs-server/command_execution_policy.py` enforces mission-specific admission rules, immediate-only test missions, and strict-sync trigger timing.
- E1 source verified: `gcs-server/command_submission_pipeline.py` guards SITL callback routing, records launch readiness as preparation evidence, and treats missing fleet RPC as delivery unknown.
- E1 source verified: `gcs-server/command_journal.py` uses SQLite WAL plus a separate callback-key file to persist the durable command journal.
- E1 source verified: `gcs-server/agent_runtime/evidence.py` defines the structured `ReadOnlyEvidenceBundle` and `ReadOnlyEvidenceItem` envelopes.
- E2 test verified: `tests/test_command_journal.py` covers restart-queryability, callback-capability survival, idempotency replay, mid-fanout recovery, and permissions.
- E2 test verified: `tests/test_command_execution_policy.py` and `tests/test_command_submission_coordinator.py` exercise strict-sync timing, recovery reservation, and terminalization behavior.

## Architecture

Principal components:

- Mission policy: typed authority and mission-specific admission checks.
- Submission pipeline: endpoint guard, launch preparation, dispatch, and ACK recording.
- Command journal: durable SQLite WAL source of truth plus secured callback capability.
- Evidence envelope: compact read-only evidence objects for operator follow-up and audit.
- Tracker/coordinator tests: restart-safety and recovery behavior.

Most interesting mechanism: the runtime splits preparation evidence, delivery acknowledgements, and execution state into separate persisted channels. That keeps the journal durable without forcing every operator-facing fact through one mutable status blob, and it makes restart recovery explicit instead of implied.

Baseline comparison: a conventional ground-control system often stores commands in a single mutable record and assumes the live process remains available. This repository instead persists the lifecycle, the callback capability, and the evidence trail separately so replay after restart can reconstruct the command safely.

## Reuse Guidance

Reusable:

- Separate preparation evidence from delivery acknowledgements.
- Keep callback capability material out of the main database and lock it down separately.
- Persist command lifecycle as append-only or WAL-backed state.
- Package operator-facing evidence as structured envelopes instead of Markdown summaries only.

Do not copy:

- Do not copy the whole drone control plane as-is; the reusable part is the persistence and admission split.
- Do not treat the journal as multi-writer safe when the runtime assumes one command-owning GCS process.
- Do not copy the mission catalog without adapting it to your own domain semantics.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The journal uses SQLite WAL, full synchronous mode, and explicit permissions.
- The callback key is integrity-checked and kept separate from the main DB.
- Restart-safety tests cover replay and partial-fanout recovery.

Experimental or incomplete for our needs:

- The supported runtime is still a single owning GCS process.
- The codebase is broad and domain-specific, with many SITL and fleet assumptions.
- Operational correctness still depends on external fleet services and endpoint consistency.

Hidden costs and failure modes:

- Mission semantics are tightly coupled to the drone domain.
- External fleet RPC or SITL mismatches can block dispatch entirely.
- The runtime surface is large enough that maintenance cost is nontrivial.

Adoption experiment:

Apply the same lifecycle split to one of our durable command systems, then restart the process mid-fanout and verify that the journal reconstructs the missing target states without redispatching completed work.

## Candidate Patterns

- `secured callback-capability journal`
- `read-only evidence bundle for operator follow-up`
