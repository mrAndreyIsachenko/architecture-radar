# trezor/blockbook

- Repository: https://github.com/trezor/blockbook
- Review date: 2026-08-11
- Current commit reviewed: `6ce54d0b22cccccabf09aea3b096197195b5bb5a`
- Commit date: 2026-08-07T11:52:14+02:00
- Branch: `master`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `blockchain-intelligence`, especially restart-safe indexing, reorg recovery, transaction interpretation, and sink-safe materialization. The reusable mechanism is the liveness-capped `SyncWorker` recovery loop, not the full explorer/API surface.

## Verified Flow

Process startup and signal handling -> `NewSyncWorkerWithConfig` normalizes retry configuration and enforces a positive max stall duration -> `ResyncIndex` compares local and remote best hashes -> `resyncIndex` switches between no-op, fork recovery, sequential sync, `BulkConnectBlocks`, and `ParallelConnectBlocks` -> `handleFork` disconnects orphaned blocks and re-enters the resync path -> `connectBlocks` and the parallel/bulk variants persist blocks into RocksDB through `db.ConnectBlock` / bulk-connect helpers -> tests inject missing-block and shutdown scenarios and verify the index recovers to the expected height/hash.

- E1 source verified: `db/sync.go:22-245` defines `SyncWorker`, `MissingBlockRetryConfig`, retry normalization, liveness caps, and the top-level `ResyncIndex` orchestration.
- E1 source verified: `db/sync.go:247-438` handles fork detection, disconnect/reconnect recovery, and shutdown-aware sequential connection.
- E1 source verified: `db/sync.go:446-920` implements abort-aware worker coordination for `ParallelConnectBlocks` and `BulkConnectBlocks`, including the missing-block retry path and stall deadline.
- E2 test verified: `tests/sync/handlefork.go:17-220` simulates a missing block that later resolves, then verifies the index reconnects to the real chain state.
- E2 test verified: `tests/sync/connectblocks.go:36-220` verifies sequential connect, parallel connect, and shutdown interruption behavior.

## Architecture

Principal components:

- `SyncWorker` and its retry configuration.
- RocksDB as the local projection store.
- Chain adapter interface for backend hash/block probes.
- Sequential, parallel, and bulk connection paths.
- Integration tests with fake chains and recovery scenarios.

Most interesting mechanism: Blockbook treats chain sync as a recoverable projection with a bounded retry loop. It will re-probe chain state after repeated missing-block errors, restart on hash mismatch, and cap the wall-clock time a single block can spend in the retry loop so the worker cannot spin forever behind a lagging or rolled-back backend.

Baseline comparison: a naive indexer would fetch blocks in order and commit them directly, relying on the backend to never roll back. Blockbook adds explicit fork detection, disconnect/reconnect recovery, abort-aware worker coordination, and a liveness cap for the retry loop.

## Reuse Guidance

Reusable:

- Put a hard time cap around missing-block retry loops.
- Probe the chain again before declaring a reorg or rollback.
- Split sequential, parallel, and bulk recovery paths so they can be reasoned about separately.
- Keep worker abort channels buffered so one error can unwind the pipeline cleanly.

Do not copy:

- Do not trust the chain probe path without a second validation step if the backend is load-balanced.
- Do not assume RocksDB-specific projection semantics are portable.
- Do not expose the retry knobs without operator-facing guidance.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The sync worker has explicit retry normalization and shutdown handling.
- Fork recovery and missing-block recovery are both covered by integration tests.
- The code distinguishes `resync`, `get_block_hash`, `get_block`, and `connect_block` error labels.

Experimental or incomplete for our needs:

- The projection still depends on backend-specific RPC behavior.
- The recovery path is complex enough that tuning matters.
- The repo is broader than the sync worker alone.

Hidden costs and failure modes:

- Load-balanced or lagging backends can cause over-disconnection when `GetBlockHash` or `GetBlock` is transiently inconsistent.
- Liveness caps can mask a backend that is simply too slow to catch up.
- Parallel sync requires careful abort coordination to avoid wedged workers.

Adoption experiment:

Run one internal replay that injects a missing block, one that injects a hash mismatch, and one that interrupts sync mid-flight, then verify the projection restarts to the same best height/hash without wedging the worker.

## Candidate Patterns

- `reorg-safe materialization windows`
- `liveness-capped chain probe`
- `abort-aware worker ring`
