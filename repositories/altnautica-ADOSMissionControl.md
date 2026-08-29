# altnautica/ADOSMissionControl

- Repository: https://github.com/altnautica/ADOSMissionControl
- Review date: 2026-08-29
- Current commit reviewed: `f367a7b4ca1b6c549df79d123dc18bc59daadf09`
- Commit date: 2026-08-27T20:37:35+05:30
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `drones-robotics-autonomy`, especially mission-command delivery, telemetry relay recovery, and signing-key ownership. The reusable mechanism is the lease/ack command queue plus the bridge and key-management code that keep command delivery auditable and recoverable.

## Verified Flow

`convex/cmdDroneCommands.ts` validates and enqueues commands, then `claimCommands()` atomically leases pending or expired delivering rows, caps batch size, and fails rows that exceed the attempt budget -> `ackCommand()` checks device ownership and marks the terminal result -> `pruneTerminalCommands()` removes old completed or failed rows in bounded batches -> `convex/cmdSigningKeys.ts` gates key CRUD by authenticated user, validates key shape, manages per-drone link IDs, and records key ownership state -> `tools/mavlink-bridge/src/udp-ws.ts` binds UDP and WebSocket endpoints, learns or fixes the peer, and rebonds with exponential backoff on socket errors.

- E1 source verified: `convex/cmdDroneCommands.ts:20-241` implements vocabulary validation, queue insertion, claim leasing, acking, and terminal-row pruning.
- E1 source verified: `convex/cmdSigningKeys.ts:35-229` implements user-scoped signing-key lookup, upsert, link-id allocation, and release.
- E1 source verified: `tools/mavlink-bridge/src/udp-ws.ts:51-214` implements the UDP/WebSocket relay with peer learning, broadcast, shutdown, and rebind backoff.
- E2 test verified: `tests/lib/agent/status-mapper-transforms.test.ts`, `tests/lib/agent/status-mapper-install-health.test.ts`, `tests/unit/local-pair-client.test.ts`, and `tests/unit/lan-pair-config-route.test.ts` cover the command/status bridge surfaces and the pairing and auth edges around the relay.

## Architecture

Principal components:

- Convex command queue for cloud relay delivery.
- Signing-key registry with per-drone ownership state.
- UDP/WebSocket bridge for MAVLink stream forwarding.
- Status-mapper and pairing layers for operator-facing views.
- Broad client/UI layer built around the underlying drone transport model.

Most interesting mechanism: the command relay uses a lease, not a fire-and-forget queue. That makes crash recovery explicit, keeps delivery attempts bounded, and lets the agent reclaim stale work without assuming the previous poll completed.

Baseline comparison: a typical drone control UI would dispatch commands directly to the flight controller and rely on UI retries. This repository puts a transactional queue in front of command execution and separates ownership checks from transport forwarding.

## Reuse Guidance

Reusable:

- Use a lease/ack queue for operator commands that can be lost in transit.
- Fail a row after a bounded number of delivery attempts.
- Keep signing-key ownership separate from command delivery.
- Bridge UDP and WebSocket with explicit peer learning and backoff.

Do not copy:

- Do not copy the product-specific UI surface.
- Do not copy the Convex/Next.js coupling without a matching platform reason.
- Do not depend on the cloud signing-key sync path as production-ready yet; the source keeps it disabled.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Queue claims are transactional and bounded.
- Ownership checks exist at the command and key boundaries.
- The UDP/WebSocket relay handles socket errors, shutdown, and peer churn explicitly.

Experimental or incomplete for our needs:

- `cloudSigningKeyUploadsEnabled()` currently returns `false`, so the cloud-sync path is intentionally disabled.
- The repository is still heavily shaped by its app UI and operator workflows.
- A lot of the code surface is visualization and pairing glue rather than transport mechanics alone.

Hidden costs and failure modes:

- Lease expiry can cause commands to be retried later than an operator expects.
- The attempt cap converts repeated failure into a terminal error state, which is good for safety but can hide persistent transport issues.
- Key management and transport relay are coupled to the same product surface, so reuse needs extraction.

Adoption experiment:

Force a command queue crash between claim and ack, then verify the lease expires, the row is reclaimed once, and terminal cleanup eventually removes the row without breaking device ownership checks.

## Candidate Patterns

- `lease-bounded command relay`
- `ownership-scoped signing-key registry`
- `udp/websocket peer-learning bridge`
