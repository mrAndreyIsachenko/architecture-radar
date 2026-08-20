# Reorg-Safe Materialization Windows

- Canonical name: Reorg-Safe Materialization Windows
- Aliases: reorg-safe indexing, rollback-window indexing, reorg-aware incremental indexing, finalized/provisional block split
- Avoided duplicate names: eventual chain sync, naive block replay, raw head polling
- Last updated: 2026-08-11

## Problem

Blockchain indexers need to process fast-moving heads without permanently materializing data that may still be reverted by a chain reorganization. If the system cannot separate provisional blocks from finalized blocks, downstream materializations can become inconsistent, duplicate, or irrecoverable after a rollback.

## Mechanism

Process chain data in two windows:

- A provisional window near the head that can still be rolled back.
- A finalized window beyond a reorg threshold that can be trusted for forward scanning and broader range queries.

Persist checkpoint state separately from derived materializations, and split recovery roles so live indexing, catchup/backfill, manual repair, and retry work do not all share the same code path.

## Invariants

- Progress markers must be monotonic within each confirmed window.
- Unsafe head-adjacent materializations must remain reversible.
- Retry and catchup state must survive process restarts.
- Downstream sinks must be idempotent or able to tolerate replay.
- Reorg rollback must not rely on heuristics that assume every upstream block is final.

## Implementation Variants

- Threshold-based block stream: Graph Node uses a reorg threshold to decide when to revert or advance and keeps storage-level cleanup bounded.
- Worker-ring indexer: MultiChain Indexer uses regular, catchup, manual, and rescanner workers with KV/Redis state and explicit retry queues.
- Layered chain toolkit: ChainFoundry combines a sliding block tracker, explicit reorg classification, configurable checkpoint persistence, and segmented backfill workers so rollback, recovery, and live indexing stay separate.
- Liveness-capped sync worker: Blockbook keeps a resync loop around `SyncWorker`, separates `ResyncIndex`, `connectBlocks`, `BulkConnectBlocks`, and `ParallelConnectBlocks`, and restarts when a block hash disappears or the local tip forks.

## Known Repositories

- `graphprotocol/graph-node` reviewed at `2adda68a79dff3703ab444ac8d846c189d9ce3c0`.
- `fystack/multichain-indexer` reviewed at `90f4b3156c36bf048ec513e395f7dadef66f32e1`.
- `DarshanKumar89/chainfoundry` reviewed at `090279cb7acb35b52803c711e353d91c85fa6bd4`.
- `trezor/blockbook` reviewed at `6ce54d0b22cccccabf09aea3b096197195b5bb5a`.
- `bitcoincore-dev/nakamoto-electrs` reviewed at `f9fc5ba17f38f6d45812e467a5299d194b086af8`.

## Comparison Of Implementations

Graph Node keeps the safety boundary close to chain ingestion and storage. Its block stream uses a reorg threshold, while the Postgres layer persists chain/deployment state and cleans up caches and logs under explicit controllers.

MultiChain Indexer moves more of the recovery logic into cooperating workers. Regular workers handle live indexing and rollback, catchup workers backfill ranges, manual workers drain missing ranges, and rescanners repair failures from persisted state.

ChainFoundry keeps the boundary split across smaller primitives: `BlockTracker` owns the sliding window, `ReorgDetector` classifies the failure mode, `CheckpointManager` persists the last confirmed position, and `BackfillEngine` handles batched historical recovery. The mechanism is the same shape, but the implementation is packaged as a reusable Rust toolkit rather than a single indexer.

Blockbook applies the same recovery idea from a different angle. Instead of explicit finalized/provisional windows, `SyncWorker` treats the local tip as a recoverable projection, probes the remote chain hash-by-hash, restarts on missing-block or fork mismatch, and keeps bulk/parallel sync bounded by a wall-clock stall cap. That makes it a useful comparison point for liveness-first recovery, especially when the downstream sink is a mutable RocksDB projection rather than a pure event stream.

Nakamoto-electrs shows the same family on the SPV/Electrum side. `NakamotoBlockSource` turns nakamoto's connected/disconnected/synced stream into a local rollback-capable projection, and `Indexer` uses a height-indexed reverse map so a `Disconnected` event can remove every history entry recorded at that height. It is a tighter bridge than Blockbook's full-node sync loop, but it validates the same invariant: head-adjacent materialization must remain reversible.

## Failure Modes

- Misconfigured thresholds can push provisional data into the finalized path too early.
- Restart recovery can re-emit already processed data if downstream sinks are not idempotent.
- Catchup queues can drift from live head state if progress bookkeeping is incomplete.
- Probabilistic prefilters can create false positives unless a second validation step exists.
- Operational tuning can become difficult when reorg depth, catchup range sizing, and retry limits all interact.
- Liveness caps can hide a backend that is too slow to catch up if operators only look for hard failures.
- Hash-probe retries can over-disconnect on load-balanced or lagging backends when the probe target is not the canonical node.

## Trade-Offs

- Lower latency near the chain head costs more rollback risk.
- More explicit recovery workers improve correctness but increase operational complexity.
- Persisting extra checkpoints and retry state reduces reprocessing ambiguity but increases storage and coordination overhead.

## Applicability To Interests

- Blockchain indexing: directly applicable to reorg-safe materialization and incremental chain sync.
- Blockchain transaction interpretation: necessary before higher-level attribution or event inference can be trusted.
- Wallet and deposit monitoring: useful when credits must not be finalized until after a safety window.

## Adoption Conditions

- Define explicit provisional/finalized block boundaries.
- Persist block hashes, latest processed block, and retry state separately from sink side effects.
- Add reorg-injection tests and restart tests that prove replay does not corrupt downstream state.
- Require idempotent or deduplicated downstream writes.

## Evidence References

- E1 source verified: Graph Node `chain/ethereum/src/polling_block_stream.rs` uses `reorg_threshold` to choose reorg vs forward scanning.
- E1 source verified: Graph Node `store/postgres/src/chain_store.rs` bounds call-cache cleanup and maintains explicit indices.
- E1 source verified: MultiChain Indexer `internal/worker/regular.go` persists latest blocks, queues catchup ranges, and handles reorg rollback.
- E1 source verified: MultiChain Indexer `internal/worker/manual.go` drains missing ranges from Redis and removes completed ranges.
- E2 test verified: MultiChain Indexer `internal/worker/factory_test.go` checks worker isolation and catchup bootstrapping.
- E1 source verified: ChainFoundry `chainindex/crates/chainindex-core/src/reorg.rs` classifies short reorgs, deep reorgs, and RPC inconsistencies.
- E1 source verified: ChainFoundry `chainindex/crates/chainindex-core/src/tracker.rs` tracks a sliding block window and rewinds on fork detection.
- E1 source verified: ChainFoundry `chainindex/crates/chainindex-core/src/checkpoint.rs` persists block hash/number checkpoints on a configurable interval.
- E2 test verified: ChainFoundry `chainindex/crates/chainindex-core/src/backfill.rs` and `src/tracker.rs` tests cover retry, progress, and rollback behavior.
- E1 source verified: Blockbook `db/sync.go:22-245` defines `SyncWorker`, `MissingBlockRetryConfig`, retry normalization, liveness caps, and top-level `ResyncIndex` orchestration.
- E1 source verified: Blockbook `db/sync.go:247-438` handles fork detection, disconnect/reconnect recovery, and shutdown-aware sequential connection.
- E1 source verified: Blockbook `db/sync.go:446-920` implements abort-aware worker coordination for `ParallelConnectBlocks` and `BulkConnectBlocks`, including the missing-block retry path and stall deadline.
- E2 test verified: Blockbook `tests/sync/handlefork.go:17-220` simulates a missing block that later resolves, then verifies the index reconnects to the real chain state.
- E2 test verified: Blockbook `tests/sync/connectblocks.go:36-220` verifies sequential connect, parallel connect, and shutdown interruption behavior.
- E1 source verified: bitcoincore-dev/nakamoto-electrs `src/nakamoto_source.rs:1-320` converts nakamoto events into bitcoin 0.30 blocks and broadcasts connected/disconnected/synced transitions.
- E1 source verified: bitcoincore-dev/nakamoto-electrs `src/indexer.rs:93-220` keeps a height-indexed rollback map and removes all entries at a disconnected height.
- E2 test verified: bitcoincore-dev/nakamoto-electrs `tests/integration_tests.rs:333-407` verifies rollback-on-disconnect and reorg replacement behavior.
