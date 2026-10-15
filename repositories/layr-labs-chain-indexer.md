# Layr-Labs/chain-indexer

- Repository: https://github.com/Layr-Labs/chain-indexer
- Review date: 2026-10-01
- Current commit reviewed: `7d774750b49b0d8b527edc2124bb6f248f56d006`
- Commit date: 2026-04-24T17:33:58-05:00
- Branch: `master`
- Tag: `v0.3.1`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `blockchain-intelligence`, especially incremental indexing, reorg recovery, event decoding, and contract-registry fanout. The reusable mechanism is a block poller that treats reorgs as a first-class rollback condition and keeps derived storage separate from the live chain cursor.

## Verified Flow

`NewEVMChainPoller` normalizes config defaults and wires the chain client, log parser, contract store, persistence store, and block handler -> `Start` loads the last processed block or seeds from genesis/latest and persists the starting point -> `pollForBlocks` wakes on a ticker and calls `processNextBlock` -> `processNextBlock` compares the stored tip to the latest chain block, fetches each intervening block, and checks parent hashes -> a parent mismatch triggers `reconcileReorg`, which calls `findOrphanedBlocks`, deletes orphaned records from persistence, and notifies the block handler through `HandleReorgBlock` -> a matched block flows into `processBlockLogs`, which fetches logs in concurrent batches, decodes them, invokes `HandleLog`, and then persists the block record and prunes old history -> the in-memory persistence store maintains the latest processed block plus per-block records.

- E1 source verified: `pkg/chainPollers/evm/evmChainPoller.go::Start`, `processNextBlock`, `processBlockLogs`, `reconcileReorg`, and `findOrphanedBlocks` implement the live poll / detect / reconcile / persist loop.
- E1 source verified: `pkg/clients/ethereum/client.go::GetLatestBlock`, `GetBlockByNumber`, and `GetLogsForAddresses` provide the RPC surface the poller uses.
- E1 source verified: `pkg/clients/ethereum/handlers.go` defines the request/response parsers for block, receipt, and log calls.
- E1 source verified: `pkg/chainPollers/persistence/memory/memory.go` stores per-chain tips and block records behind a mutex-backed in-memory persistence layer.
- E1 source verified: `pkg/chainPollers/contractRegistry/inMemory.go` keeps a concurrent contract registry that can be updated while the poller is running.
- E2 test verified: `pkg/chainPollers/evm/evmChainPoller_test.go` covers no-reorg, simple reorg, deep-reorg, dynamic contract registration, and batch concurrency cases.
- E2 test verified: `pkg/chainPollers/evm/evmChainPoller_integration_test.go` exercises Base Sepolia log fetching, contract-registry fanout, and the factory-style dynamic registration path against a live RPC endpoint when `BASE_RPC_URL` is present.
- E2 test verified: `pkg/chainPollers/persistence/memory/memory_test.go` and the contract-registry tests cover store and registry behavior in isolation.

## Architecture

Principal components:

- `EVMChainPoller` for live head polling, reorg reconciliation, and block log processing.
- `ethereum.Client` for RPC request construction and response parsing.
- `IChainPollerPersistence` and the in-memory store for tip/block state.
- `IContractRegistry` for dynamic contract discovery and fanout.
- `IBlockHandler` for downstream interpretation of decoded logs and reorg notices.

Most interesting mechanism: the indexer keeps the live cursor and the derived materialization separate. A reorg does not mutate the final output in place; it walks back through stored block records, deletes orphaned blocks, and lets downstream handlers react to the reorg explicitly.

Baseline comparison: a naive indexer would poll the chain head and write logs directly to the sink without a rollback window or a block record store. This repo instead has explicit parent-hash validation, orphan collection, and concurrent log batching.

## Reuse Guidance

Reusable:

- Keep a reversible window near the head and store block hashes alongside the cursor.
- Separate live poll, orphan detection, and downstream log handling into distinct interfaces.
- Treat contract discovery as a separate registry so the poller can fan out new addresses without rewriting the whole pipeline.
- Batch RPC log fetches, but keep the batch size and timeout configurable.

Do not copy:

- Do not adopt the in-memory store as-is for production durability.
- Do not assume the current integration coverage proves a real chain reorg in the wild.
- Do not let log decoding failures silently advance the cursor.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The reorg path is directly tested at the poller level.
- The registry and persistence layers are separated from the poller logic.
- The dynamic contract-registration path is exercised in integration tests against a live RPC endpoint.

Experimental or incomplete for our needs:

- The shipped store is in-memory, so production persistence still needs an external backend.
- Live RPC tests depend on an environment variable and a reachable testnet endpoint.
- A deep reorg is covered in tests, but not by an operational rollback harness in this repository.

Hidden costs and failure modes:

- A bad RPC endpoint or a slow log batch can block the poller loop.
- Reorg recovery depends on the downstream handler being able to tolerate explicit rollback notifications.
- The history pruning path can leave old records in storage if deletion fails and the caller ignores the warning.

Adoption experiment:

Run the poller against a real chain feed with a forced reorg or equivalent replay harness, then confirm the orphaned blocks are removed, the block handler receives explicit rollback notices, and the cursor only advances after decoded logs are handed off.

## Candidate Patterns

- `Reorg-Safe Materialization Windows`
- `reorg-aware poller loop`
- `dynamic contract-registry log fanout`
