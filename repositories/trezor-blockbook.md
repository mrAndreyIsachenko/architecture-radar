# trezor/blockbook

- Repository: https://github.com/trezor/blockbook
- Review date: 2026-10-16
- Current commit reviewed: `c6d8d181fb7645a15c655c5371bb7205af5f9086`
- Commit date: 2026-10-16T08:02:29+02:00
- Branch: `master`
- Previous commit reviewed: `6ce54d0b22cccccabf09aea3b096197195b5bb5a`
- Material changes since previous review: The new head keeps the same recovery loop but adds Ethereum pseudo-token transfer suppression for Polygon `0x...1010` and EIP-7708 system-address flows.
- Decision: track

## Problem Fit

This repository informs `blockchain-intelligence`, especially restart-safe indexing, reorg recovery, transaction interpretation, and sink-safe materialization. The reusable mechanism is the liveness-capped `SyncWorker` recovery loop, not the full explorer/API surface.

## Verified Flow

Process startup and signal handling -> `NewSyncWorkerWithConfig` normalizes retry configuration and enforces a positive max stall duration -> `ResyncIndex` compares local and remote best hashes -> `resyncIndex` switches between no-op, fork recovery, sequential sync, `BulkConnectBlocks`, and `ParallelConnectBlocks` -> `handleFork` disconnects orphaned blocks and re-enters the resync path -> `connectBlocks` and the parallel/bulk variants persist blocks into RocksDB through `db.ConnectBlock` / bulk-connect helpers -> `bchain/coins/eth/ethparser.go` filters pseudo-token transfers that originate from the Polygon `0x...1010` and EIP-7708 system address -> tests inject missing-block and shutdown scenarios and verify the index recovers to the expected height/hash while the ignored-contract tests verify the filter path.

- E1 source verified: `db/sync.go:22-245` defines `SyncWorker`, `MissingBlockRetryConfig`, retry normalization, liveness caps, and the top-level `ResyncIndex` orchestration.
- E1 source verified: `db/sync.go:247-438` handles fork detection, disconnect/reconnect recovery, and shutdown-aware sequential connection.
- E1 source verified: `db/sync.go:446-920` implements abort-aware worker coordination for `ParallelConnectBlocks` and `BulkConnectBlocks`, including the missing-block retry path and stall deadline.
- E1 source verified: `bchain/coins/eth/ethparser.go` adds the contract/address suppression logic that excludes pseudo-token transfers from the token-transfer stream.
- E2 test verified: `tests/sync/handlefork.go:17-220` simulates a missing block that later resolves, then verifies the index reconnects to the real chain state.
- E2 test verified: `tests/sync/connectblocks.go:36-220` verifies sequential connect, parallel connect, and shutdown interruption behavior.
- E2 test verified: `bchain/coins/eth/ignored_contract_test.go` covers the Polygon `0x...1010` and EIP-7708 exclusion cases.

## Architecture

Principal components:

- `SyncWorker` and its retry configuration.
- RocksDB as the local projection store.
- Chain adapter interface for backend hash/block probes.
- Sequential, parallel, and bulk connection paths.
- Integration tests with fake chains and recovery scenarios.

Most interesting mechanism: Blockbook treats chain sync as a recoverable projection with a bounded retry loop. It will re-probe chain state after repeated missing-block errors, restart on hash mismatch, and cap the wall-clock time a single block can spend in the retry loop so the worker cannot spin forever behind a lagging or rolled-back backend. The new Ethereum parser filter is the same style of explicit projection rule applied one layer higher: suppress pseudo-token transfers before they contaminate the materialized event stream.

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
- Do not rely on token-transfer output without the chain-specific exclusion rules being replay-validated.

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
Replay a Polygon/EIP-7708 token-transfer window and confirm the pseudo-token transfers disappear while legitimate token and native transfers still index correctly.

## Candidate Patterns

- `reorg-safe materialization windows`
- `liveness-capped chain probe`
- `abort-aware worker ring`
- `pseudo-token transfer suppression gate`

## Previous Review

The earlier review covered the recovery loop and the missing-block replay path. This review updates the same sync worker with current-head evidence around Ethereum pseudo-token filtering.

Earlier evidence remains pinned to `6ce54d0b22cccccabf09aea3b096197195b5bb5a` in the [2026-08-11 report](../reports/2026-08-11.md). The replay gap for the new Ethereum filter remains open.
