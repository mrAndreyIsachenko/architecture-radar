# Reorg-Safe Materialization Windows

- Canonical name: Reorg-Safe Materialization Windows
- Aliases: reorg-safe indexing, rollback-window indexing, reorg-aware incremental indexing, finalized/provisional block split
- Avoided duplicate names: eventual chain sync, naive block replay, raw head polling
- Last updated: 2026-08-08

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

## Known Repositories

- `graphprotocol/graph-node` reviewed at `2adda68a79dff3703ab444ac8d846c189d9ce3c0`.
- `fystack/multichain-indexer` reviewed at `90f4b3156c36bf048ec513e395f7dadef66f32e1`.
- `DarshanKumar89/chainfoundry` reviewed at `090279cb7acb35b52803c711e353d91c85fa6bd4`.

## Comparison Of Implementations

Graph Node keeps the safety boundary close to chain ingestion and storage. Its block stream uses a reorg threshold, while the Postgres layer persists chain/deployment state and cleans up caches and logs under explicit controllers.

MultiChain Indexer moves more of the recovery logic into cooperating workers. Regular workers handle live indexing and rollback, catchup workers backfill ranges, manual workers drain missing ranges, and rescanners repair failures from persisted state.

ChainFoundry keeps the boundary split across smaller primitives: `BlockTracker` owns the sliding window, `ReorgDetector` classifies the failure mode, `CheckpointManager` persists the last confirmed position, and `BackfillEngine` handles batched historical recovery. The mechanism is the same shape, but the implementation is packaged as a reusable Rust toolkit rather than a single indexer.

## Failure Modes

- Misconfigured thresholds can push provisional data into the finalized path too early.
- Restart recovery can re-emit already processed data if downstream sinks are not idempotent.
- Catchup queues can drift from live head state if progress bookkeeping is incomplete.
- Probabilistic prefilters can create false positives unless a second validation step exists.
- Operational tuning can become difficult when reorg depth, catchup range sizing, and retry limits all interact.

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
