# Finality-Aware Hot/Cold Projection

- Canonical name: Finality-Aware Hot/Cold Projection
- Aliases: reorg-safe materialization, hot block projection, finalized/hot split, fork-aware projection
- Avoided duplicate names: blockchain indexer checkpoint, last-height cursor, simple reorg handler
- Last updated: 2026-08-02

## Problem

Blockchain transaction interpretation must handle reorgs, partial data, protocol-specific semantics, and provenance from interpreted events back to chain evidence. A single last-processed height is insufficient near chain head because data may be unfinalized and later invalidated.

## Mechanism

Split projection state into finalized and hot sections. Data sources emit block batches with block hashes and a finalized-head view. Persistence receives a transaction envelope containing the previous base head, new block heads, and finalized head. On fork signals, the processor rolls back to the nearest known common block hash and replays from that base. Finality advancement is processed even when no new blocks arrive.

## Invariants

- Block height alone is never enough; block hash must be part of progress.
- Handler side effects for hot blocks must be reversible, replaceable, or isolated from finalized rows.
- The database transaction receives enough head evidence to promote, rollback, and rewrite hot rows.
- Finality updates are first-class events.
- If no common base exists after finalized state, processing fails rather than silently corrupting state.

## Implementation Variants

- Generic processor with `FinalDatabase` and `HotDatabase` contracts.
- Chain-specific data source with finality-confirmation distance from head.
- Portal/archive finalized source plus RPC hot source.
- Storage-backed implementation that groups hot rows by block hash and promotes rows when finalized.

## Known Repositories

- subsquid/squid-sdk at `26f7703e127604a40522449eedff3823d6183662`: generic batch processor, EVM finality configuration, hot database transaction envelope, and fork tests.
- graphprotocol/graph-node at `2adda68a79dff3703ab444ac8d846c189d9ce3c0`: triaged as a mature alternative blockchain indexing implementation; source flow not reviewed in this run.

## Comparison

Subsquid makes the hot/final database boundary explicit in the SDK contract. A conventional indexer that stores only the latest height must add ad hoc deletion logic for reorgs and cannot explain which block hashes produced current materialized rows.

## Failure Modes

- Finality confirmation is too small for the chain and finalized data later changes.
- Sparse hot state cannot prove the true fork point, causing deeper replay.
- Domain interpretation writes irreversible side effects before finality.
- Source-specific fork behavior is insufficiently tested end to end.
- Protocol semantics are decoded without preserving log, trace, transaction, and block-hash provenance.

## Trade-Offs

- Reorg safety increases storage and transaction complexity.
- Hot rows enable low-latency monitoring but require rollback and promotion logic.
- Conservative finality reduces reorg risk but increases interpretation latency.

## Applicability

Applies directly to `Blockchain transaction interpretation` in `interests.md`, especially `reorg-safe materialization`, `trace decoding pipelines`, and provenance from interpretation back to chain evidence.

## Adoption Conditions

- Start with a protocol-specific prototype that decodes one transaction family into domain events.
- Store provenance for transaction hash, block number, block hash, log index, trace path, ABI source, and decoder version.
- Test a reorg scenario end to end through data source, processor, persistence, and interpreted event projection.
- Keep unfinalized interpretations labeled as provisional until finalized.

## Evidence References

- E1 source verified: Subsquid `processor/batch-processor/src/database.ts` defines `HotTxInfo` with `finalizedHead`, `baseHead`, and `newBlocks`.
- E1 source verified: Subsquid `processor/batch-processor/src/run.ts` handles fork exceptions, computes rollback index, and forwards finality-only batches to `transactHot2`.
- E1 source verified: Subsquid `evm/evm-processor/src/ds-rpc/client.ts` computes finalized height from chain height minus finality confirmation.
- E2 test verified: Subsquid `processor/batch-processor/src/test/processor.test.ts` covers deep reorg, cascading forks, finality-only batches, and disjoint-fork failure.

