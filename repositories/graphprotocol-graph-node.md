# graphprotocol/graph-node

- Repository: https://github.com/graphprotocol/graph-node
- Review date: 2026-08-02
- Current commit reviewed: `2adda68a79dff3703ab444ac8d846c189d9ce3c0`
- Commit date: 2026-07-20T16:43:47-07:00
- Branch: `master`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `blockchain-intelligence`, especially deterministic indexing, reorg handling, call-cache materialization, and queryable log storage.

## Verified Flow

Ethereum block stream -> reorg-threshold reconciliation -> chain-store persistence and call-cache maintenance -> subgraph deployment/store state updates -> `_logs` query and log-store backends expose observable output; tests cover indexed-store behavior and subgraph data-source flows.

- E1 source verified: `chain/ethereum/src/polling_block_stream.rs` applies a reorg threshold, chooses revert vs forward progression, and aligns block ranges with data-source start blocks.
- E1 source verified: `store/postgres/src/chain_store.rs` maintains call-cache indices and deletes stale calls in bounded batches.
- E1 source verified: `docs/log-store.md` and `NEWS.md` describe the queryable log-store abstraction and the `_logs` GraphQL field.
- E1 source verified: `graph/tests/subgraph_datasource_tests.rs` exercises triggers-adapter behavior over source entity ranges.
- E2 test verified: `store/test-store/tests/postgres/subgraph.rs` covers subgraph deployment reassignment and store-event behavior.

## Architecture

Principal components:

- Ethereum chain ingestion and polling block stream.
- Postgres-backed chain store and deployment store.
- Subgraph execution and store event model.
- Queryable log-store abstraction for operator visibility.

Most interesting mechanism: the indexer uses a reorg threshold to decide when block numbers are safe to trust, and it makes the storage layer explicitly responsible for bounded cache cleanup and deployment-state transitions.

Baseline comparison: a simpler indexer would just replay blocks until the head and hope reorgs are rare. Graph Node splits the safe/unsafe windows, persists deployment state, and surfaces logs through a stable query API.

## Reuse Guidance

Reusable:

- Separate provisional block processing from finalized materialization windows.
- Make cache cleanup and deployment state explicit and bounded.
- Expose operational logs through the same query surface used for indexed data.

Do not copy:

- Do not copy the full subgraph platform unless you need its chain-specific semantics.
- Do not assume log storage backends are free; the abstraction still carries operational cost.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Strong source depth across chain, store, graph, and tests.
- Recent release notes document real bug fixes and capability changes.
- The code and docs explicitly discuss reorgs, deterministic errors, and queryable logs.

Experimental or incomplete for our needs:

- The broader platform is much larger than the mechanism we want.
- The review focused on one chain path and one store path, not the whole system.

Hidden costs and failure modes:

- Reorg handling and cache cleanup require careful threshold tuning.
- Log-store backends add infrastructure overhead.
- Deterministic indexing assumptions can break on provider or manifest edge cases.

Adoption experiment:

Use Graph Node as the reference model for a reorg-safe materialization layer: keep a safety window, persist block checkpoints, and force the replay path to respect the same finalized/provisional split.

## Candidate Patterns

- `reorg-safe materialization window`
- `queryable log store abstraction`
