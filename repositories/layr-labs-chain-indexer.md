# Layr-Labs/chain-indexer

- Repository: https://github.com/Layr-Labs/chain-indexer
- Review date: 2026-08-05
- Current commit reviewed: `7d774750b49b0d8b527edc2124bb6f248f56d006`
- Commit date: 2026-07-31T09:05:32+03:00
- Branch: `master`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: watch

## Problem Fit

This repository informs `blockchain-intelligence`, specifically transaction interpretation, incremental indexing, and reorg recovery. The reusable mechanism is the block poller and reorg reconciliation path, not the convenience README or sample usage.

## Verified Flow

`EVMChainPoller.Start` -> last processed block lookup in persistence -> initial genesis/latest block bootstrap if needed -> `processNextBlock` fetches canonical blocks in order -> `processBlockLogs` fetches logs, decodes them, passes them to the block handler, stores the block, and prunes old history -> `reconcileReorg` and `findOrphanedBlocks` walk backward to the common ancestor and delete orphaned blocks -> tests verify no reorg, simple reorg, and max-depth reorg behavior.

- E1 source verified: `pkg/chainPollers/evm/evmChainPoller.go`, `Start` bootstraps the poller from stored state or a genesis/latest block and persists the first block record.
- E1 source verified: `pkg/chainPollers/evm/evmChainPoller.go`, `processNextBlock` fetches canonical blocks in order, detects parent-hash mismatches, and routes reorgs to reconciliation.
- E1 source verified: `pkg/chainPollers/evm/evmChainPoller.go`, `processBlockLogs` decodes logs, calls the block handler, writes block records, and prunes old history using `BlockHistorySize`.
- E1 source verified: `pkg/chainPollers/evm/evmChainPoller.go`, `findOrphanedBlocks` walks backward toward a common ancestor, backfills missing canonical blocks into storage, and returns orphaned block records.
- E1 source verified: `pkg/chainPollers/persistence/memory/memory.go`, the in-memory store keeps last-processed blocks and block records behind a mutex and supports close semantics.
- E2 test verified: `pkg/chainPollers/evm/evmChainPoller_test.go::TestFindOrphanedBlocks_NoReorg_AllBlocksMatch` verifies the no-reorg path.
- E2 test verified: `pkg/chainPollers/evm/evmChainPoller_test.go::TestFindOrphanedBlocks_SimpleReorg_FindsOrphanedAndAncestor` verifies ancestor discovery and orphaned-block detection.
- E2 test verified: `pkg/chainPollers/evm/evmChainPoller_test.go::TestFindOrphanedBlocks_DeepReorg_HitsMaxDepth` verifies bounded reorg depth behavior.
- E2 test verified: `pkg/chainPollers/persistence/test_suite.go` exercises persistence lifecycle and concurrent access for any store implementation.

## Architecture

Principal components:

- `EVMChainPoller`: block polling, reorg detection, log fetching, and block-handler dispatch.
- Persistence interface: last-processed block and block-record storage.
- Contract store and transaction log parser: address selection and log decoding.

Most interesting mechanism: the poller does not merely advance a head pointer. It preserves enough block history to walk back to a common ancestor, backfills missing canonical blocks, and deletes orphaned records explicitly when a reorg is detected.

Baseline comparison: a forward-only indexer would trust block number monotonicity and lose correctness on chain reorgs. This implementation makes parent-hash checks and orphan cleanup part of the normal control flow.

## Reuse Guidance

Reusable:

- Use parent-hash validation plus backward ancestor search as the default reorg recovery path.
- Keep a bounded block-history window and prune old materializations after successful processing.
- Make persistence an interface so the reorg logic can be tested with in-memory stores.

Do not copy:

- Do not copy the README’s production implications literally; the project itself says it is still under active development and not audited.
- Do not rely on forward-only block numbers as a correctness signal.
- Do not assume the in-memory store is a production recovery backend.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Clear test coverage for reorg scenarios and persistence lifecycle.
- Simple persistence interface that makes the reorg logic testable.
- The control flow is explicit and easy to reason about.

Experimental or incomplete for our needs:

- The repository explicitly says it is under active development and not audited.
- The live poller only processes one chain-specific stream at a time and depends on external Ethereum RPC behavior.
- The review did not run the local test suite.

Hidden costs and failure modes:

- Reorg recovery depends on a sufficient history window; a deep enough reorg will hit `MaxReorgDepth`.
- Log fetching is parallelized and can fail as a batch even when some batches succeed.
- The persistence contract has to survive process restarts and concurrent access to remain useful.

Adoption experiment:

Build a tiny chain monitor that intentionally injects a parent-hash mismatch and confirm that orphaned blocks are removed, missing ancestor blocks are backfilled, and downstream handlers do not see a duplicated canonical event stream.

## Candidate Patterns

- `reorg-safe block reconciliation`
- `block-history pruning window`
