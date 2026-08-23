# chaindexing/chaindexing-rs

- Repository: https://github.com/chaindexing/chaindexing-rs
- Review date: 2026-08-23
- Current commit reviewed: `90caa25f5e1f6abf68455e685956b69401d9bfb3`
- Commit date: 2026-08-23
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `blockchain-intelligence`, especially reorg-safe indexing, transaction interpretation, and durable downstream side effects. The reusable mechanism is the split between indexing finality and side-effect finality, plus the explicit Postgres repair path that rewrites canonical state at the fork point.

## Verified Flow

`ReorgMode` maps operational posture to indexing and side-effect finality -> `IndexingFinality` and `SideEffectFinality` drive how far the ingester advances -> `PostgresRepo::sync_blocks` loads canonical blocks, computes the fork point, writes a reorg record, marks blocks/scans/transactions/call traces reorged, and upserts the canonical block set -> `delete_events_from_block_number` marks head-adjacent events reorged in a bounded window -> `dispatch_pending_outbox_jobs` releases durable outbox work after finality rules allow it -> integration tests verify tables, checkpoint dual-write, idempotent event inserts, and outbox dispatch.

- E1 source verified: `chaindexing/src/chain_reorg.rs` defines `ReorgMode`, `IndexingFinality`, `SideEffectFinality`, and the posture mapping between them.
- E1 source verified: `chaindexing/src/repos/postgres_repo.rs` implements `sync_blocks`, `delete_events_from_block_number`, checkpoint upsert, and canonical-state repair.
- E1 source verified: `chaindexing/src/outbox.rs` models durable outbox jobs and cancels pending work when the upstream event has already reorged.
- E2 test verified: `chaindexing-tests/src/tests/integration.rs` verifies internal table creation, event idempotency, checkpoint dual-write, and outbox dispatch.
- E2 test verified: `chaindexing/src/chain_reorg.rs` tests the finality mapping for realtime, balanced, and finality-first modes.

## Architecture

Principal components:

- Finality policy: `ReorgMode`, `IndexingFinality`, and `SideEffectFinality`.
- Postgres repository: canonical block, event, trace, checkpoint, and outbox mutations.
- Reorg handling: fork-point detection and canonical-state repair.
- Handlers: ingestion and side-effect processing that respect finality posture.
- Integration tests: database-backed verification of checkpointing, idempotency, and dispatch.

Most interesting mechanism: side effects are not treated as a byproduct of indexing; they are gated independently by finality. That lets the system keep low-latency indexing while still delaying or cancelling durable downstream actions until a safer boundary is reached.

Baseline comparison: a simpler blockchain indexer often appends blocks and hopes downstream consumers deduplicate. This repository instead makes the canonical/reorg boundary explicit and rewrites related derived tables before promoting the new chain view.

## Reuse Guidance

Reusable:

- Separate chain-ingestion finality from downstream side-effect finality.
- Persist checkpoints and outbox state alongside canonical chain rows.
- Make fork-point repair explicit and database-backed.
- Use integration tests to prove the checkpoint/outbox contract, not just the ingestion path.

Do not copy:

- Do not copy the Postgres schema or Diesel-specific implementation details without adaptation.
- Do not assume the same finality choices are correct for every chain or sink.
- Do not treat the outbox as optional if downstream effects matter for correctness.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The repository has database-backed integration tests for the important paths.
- Idempotency, checkpointing, and outbox dispatch are all represented in source and tests.
- Finality policies are typed rather than encoded as comments.

Experimental or incomplete for our needs:

- Production validation still depends on a live chain backend and Postgres.
- Side-effect correctness depends on the consumer honoring the finality boundary.
- The reorg repair path is only as strong as the canonical-block query and fork-point detection.

Hidden costs and failure modes:

- Misconfigured finality can either lag too far behind or promote data too early.
- Repairing chain state in Postgres increases write volume and operational complexity.
- Outbox dispatch can still lag or fail if the downstream dispatcher is unavailable.

Adoption experiment:

Apply the same finality split to one chain ingestion path in our stack, then inject a fork and verify that the canonical tables, checkpoints, and pending side effects all converge on the same repaired fork point.

## Candidate Patterns

- `finality-split blockchain ingestion`
- `fork-point canonical repair with durable outbox`
