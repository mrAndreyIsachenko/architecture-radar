# DarshanKumar89/chainfoundry

- Repository: https://github.com/DarshanKumar89/chainfoundry
- Review date: 2026-08-08
- Current commit reviewed: `090279cb7acb35b52803c711e353d91c85fa6bd4`
- Commit date: 2026-04-21T20:35:45+02:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `blockchain-intelligence`, especially incremental indexing, reorg recovery, checkpoint persistence, and transaction interpretation. The reusable mechanism is the layered reorg detector plus sliding block window and checkpoint manager, not the chain-specific packaging around it.

## Verified Flow

`BackfillEngine::run` validates config and splits a range into segments -> worker tasks fetch batches with retry/backoff -> `BlockTracker::push` maintains a sliding window and detects parent-hash mismatches -> `ReorgDetector::check` / `check_finalized` classifies short reorgs, deep reorgs, and RPC inconsistencies -> `CheckpointManager::maybe_save` / `force_save` persists the last confirmed block -> indexer state transitions keep backfill, live, reorg recovery, and error states explicit.

- E1 source verified: `chainindex/crates/chainindex-core/src/backfill.rs` builds segmented backfill work, applies bounded concurrency, and retries failed segments with exponential backoff.
- E1 source verified: `chainindex/crates/chainindex-core/src/tracker.rs` keeps a sliding block window, detects parent-hash mismatches, and rewinds to a confirmed block.
- E1 source verified: `chainindex/crates/chainindex-core/src/reorg.rs` classifies short reorgs, deep reorgs, and finalized-height inconsistencies into explicit reorg events.
- E1 source verified: `chainindex/crates/chainindex-core/src/checkpoint.rs` stores `chain_id`, `indexer_id`, block number, block hash, and timestamp, and saves on a configurable interval.
- E1 source verified: `chainindex/crates/chainindex-core/src/indexer.rs` models explicit `Idle`, `Backfilling`, `Live`, `ReorgRecovery`, `Stopping`, `Stopped`, and `Error` states.
- E1 source verified: `chainindex/crates/chainindex-core/src/factory.rs` snapshots and restores dynamic child-contract tracking for factory-style protocols.
- E2 test verified: `chainindex/crates/chainindex-core/src/reorg.rs::no_reorg_on_normal_chain`, `detects_short_reorg`, and `rpc_inconsistency_detected` verify reorg classification.
- E2 test verified: `chainindex/crates/chainindex-core/src/tracker.rs::push_detects_reorg` and `rewind_to` verify window-based rollback.
- E2 test verified: `chainindex/crates/chainindex-core/src/checkpoint.rs::memory_store_roundtrip` and `checkpoint_save_interval` verify persisted checkpoint recovery.
- E2 test verified: `chainindex/crates/chainindex-core/src/backfill.rs` tests cover segment planning, retry behavior, and progress reporting.

## Architecture

Principal components:

- `BackfillEngine` for batched historical indexing.
- `BlockTracker` for recent-head verification and rollback depth.
- `ReorgDetector` for reorg classification and finalized-height sanity checks.
- `CheckpointManager` and storage traits for crash recovery.
- Dynamic factory tracking and multi-chain state machines.

Most interesting mechanism: the repo keeps the reorg boundary explicit in code. A sliding window detects what is safe to retain, a detector classifies the failure mode, and a checkpoint manager persists the last confirmed position separately from the live head.

Baseline comparison: a simpler indexer stores the latest block number and hopes the chain stays canonical. This implementation keeps provisional indexing, rollback, and checkpoint persistence separate so recovery is defined instead of implied.

## Reuse Guidance

Reusable:

- Use a tracked head window rather than a single latest pointer.
- Persist checkpoints independently from transient worker state.
- Make reorg type explicit so recovery behavior can branch.
- Keep dynamic contract discovery snapshot-able across restarts.

Do not copy:

- Do not copy the whole monorepo or all chain-specific bindings.
- Do not treat the in-memory checkpoint store as a production backend.
- Do not assume downstream sinks are idempotent just because the indexer is reorg-aware.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Clear separation of tracker, detector, checkpointing, and backfill orchestration.
- Tests cover the main reorg, checkpoint, and retry paths.
- The state model makes live, backfill, and recovery phases explicit.

Experimental or incomplete for our needs:

- The reviewed commit is an older monorepo snapshot relative to the current date.
- The indexer is one module inside a broader blockchain toolkit.
- I did not run the Rust test suite locally.

Hidden costs and failure modes:

- Segment retries and checkpoint cadence add tuning complexity.
- Sliding windows can misclassify deep reorgs if configured too small.
- Multi-chain orchestration and dynamic factory tracking add state that must be persisted consistently.

Adoption experiment:

Reuse the sliding-window/checkpoint split in a small deposit monitor, inject a one- to three-block reorg plus an RPC-height regression, and confirm the sink only finalizes blocks beyond the confirmation boundary.

## Candidate Patterns

- `sliding reorg window`
- `checkpoint interval save`
- `explicit reorg state machine`
