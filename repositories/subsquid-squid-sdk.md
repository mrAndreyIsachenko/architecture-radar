# subsquid/squid-sdk

- Repository: https://github.com/subsquid/squid-sdk
- Review date: 2026-08-02
- Branch: `master`
- Commit reviewed: `26f7703e127604a40522449eedff3823d6183662`
- Commit date: 2026-07-30T15:44:59Z
- Release/tag: `@subsquid/squid-sdk_v0.5.0`, repository tag `2026-07-30`
- Previous commit reviewed: none
- Current decision: strong mechanism source for reorg-aware blockchain projection; evaluate with a protocol-specific interpretation prototype before adopting.

## Problem Fit

Subsquid SDK directly informs the `Blockchain transaction interpretation` priority. It is primarily an ETL/indexing toolkit, but its reusable architecture is the hot/cold processor boundary for finalized versus unfinalized blocks, plus explicit fork rollback handling.

## Source Structure

- `processor/batch-processor/src/run.ts` contains the generic `Processor` state machine.
- `processor/batch-processor/src/database.ts` defines final and hot database contracts.
- `processor/batch-processor/src/test/processor.test.ts` covers linear progress, hot writes, finality-only updates, forks, deep reorgs, and known test gaps.
- `evm/evm-processor/src/processor.ts` exposes `EvmBatchProcessor`, query registration, finality configuration, and runner construction.
- `evm/evm-processor/src/ds-rpc/client.ts` implements the EVM RPC hot/finalized data source.
- `evm/evm-stream/src/builder.ts` and `evm/evm-stream/src/portal/source.ts` implement Portal stream requests and parent-hash continuity.

## Verified Flow

`EvmBatchProcessor query registration -> archive/RPC data source selection -> generic Runner/Processor -> block batches split by finalized head -> database transaction with baseHead/newBlocks -> handler side effects -> fork exception rollback -> retry from common base`

- E1 source verified: `EvmBatchProcessor.addLog`, `addTransaction`, `addTrace`, `addStateDiff`, and `setBlockRange` accumulate range-bounded data requests in `evm/evm-processor/src/processor.ts`.
- E1 source verified: `EvmBatchProcessor.setFinalityConfirmation` records how far behind head blocks are considered finalized; `getHotDataSource` refuses to construct an RPC hot source without this setting.
- E1 source verified: `EvmRpcDataSource.getFinalizedHeight` computes `height - finalityConfirmation`, and `_getColdSplit` annotates consistency errors with a finality-confirmation hint in `evm/evm-processor/src/ds-rpc/client.ts`.
- E1 source verified: `Processor.run` chooses `getHead/getStream` for hot databases and `getFinalizedHead/getFinalizedStream` for final-only databases, initializes state from `db.connect`, and catches `ForkException` only when the database supports hot blocks.
- E1 source verified: `Processor.processBatch` forwards `finalizedHead`, `baseHead`, and `newBlocks` to `db.transactHot2`; finality-only batches with no blocks still reach hot storage.
- E1 source verified: `ProcessorState.handleFork` locates a common base with `findRollbackIndex`; if no common base exists and finalized state is present, it raises `Unable to process fork`.
- E2 test verified: `processor.test.ts::handles a deep reorg (>10 blocks) via ForkException` exercises rollback and replay after divergence.
- E2 test verified: `processor.test.ts::processes a finality-only batch` ensures finalized-head advancement is persisted even when no new blocks arrive.
- E2 test verified: `processor.test.ts` explicitly leaves `deep EVM reorg end-to-end: EvmRpcDataSource + Processor + TypeormDatabase` as a todo.

## Architecture

Principal components:

- Request builder: range-bounded filters for logs, transactions, traces, and state diffs.
- Data sources: Portal/archive for finalized blocks, RPC hot source for head-following data.
- Generic processor: consumes `BlockBatch` objects and maintains finalized plus unfinalized heads.
- Storage contract: `FinalDatabase` for finalized-only projections, `HotDatabase` for reorg-aware projections.
- Transaction envelope: `HotTxInfo` carries `finalizedHead`, `baseHead`, and `newBlocks` into persistence.
- Fork recovery: data sources raise fork exceptions; processor rewinds state to a known common base and retries.

Most interesting mechanism: projection writes are parameterized by chain head evidence (`baseHead`, `newBlocks`, `finalizedHead`) rather than treating indexing progress as a single height counter.

## Comparison

Baseline: a simple indexer consumes blocks in height order and stores the last processed height. That approach is fragile near chain head because a reorg requires deleting or compensating rows without knowing which block hashes were used. Subsquid's hot database contract makes the fork boundary explicit.

Genuinely unusual:

- I interpretation: passing `baseHead` and `newBlocks` to the database lets persistence own row promotion, rollback, and hot/final grouping.
- I interpretation: finality-only batches are an important edge case because rows may need promotion even when no new block payload is processed.

Standard engineering:

- Range requests, block filters, Prometheus metrics, and RPC/archive source selection are standard indexing infrastructure.

## Production Qualities

- E1 source verified: the processor rejects non-continuous block data before invoking handlers.
- E1 source verified: Prometheus metrics can include both processor and data-source metrics.
- E2 test verified: tests cover linear final processing, hot processing, sparse hot state, deep and cascading fork handling, finality forwarding, handler crash propagation, and disjoint-fork failure.

## Limitations

- E2 test verified: the repository marks deep EVM reorg through `EvmRpcDataSource + Processor + TypeormDatabase` as an explicit unverified todo.
- I interpretation: the SDK solves ingestion/projection mechanics, not domain-level intent reconstruction from transactions.
- H hypothesis: protocol-specific interpretation still requires ABI management, entity resolution, confidence scoring, and provenance from decoded semantic events back to chain traces.

## Reuse

Reusable mechanism:

- Use a hot/cold projection contract where storage receives `baseHead`, `newBlocks`, and `finalizedHead`.
- Preserve a sparse chain of unfinalized heads and roll back to the nearest verified common base on fork signals.
- Treat finality changes as first-class batches even when there are no new blocks.

Do not copy:

- Do not stop at generic block/log indexing if the goal is transaction interpretation.
- Do not copy finality-confirmation constants blindly across chains or protocols.

Evidence still required before adoption:

- End-to-end reorg test with a real or high-fidelity EVM RPC mock plus target storage.
- ABI ambiguity and protocol-specific decoding strategy.
- Provenance model connecting decoded user-intent events back to transactions, logs, traces, and block hashes.

## Extracted Patterns

- [Finality-Aware Hot/Cold Projection](../patterns/finality-aware-hot-cold-projection.md)

