# bit2swaz/shadow-index

- Repository: https://github.com/bit2swaz/shadow-index
- Review date: 2026-08-29
- Current commit reviewed: `2757f31da1e4a6eb9acb6f2b69b924cb9b4cf729`
- Commit date: 2026-02-18T02:32:50+05:30
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `blockchain-intelligence`, especially reorg-safe materialization, incremental chain backfill, and durable cursor recovery. The reusable mechanism is the in-process reth ExEx that batches canonical and reverted chain materializations into ClickHouse while keeping restart progress in a separate cursor file.

## Verified Flow

`ShadowExEx::poll` first performs `backfill_historical_blocks()` from the saved cursor to the head -> live notifications from reth are handled as `ChainCommitted`, `ChainReverted`, or `ChainReorged` -> `process_chain()` transforms blocks, receipts, and state diffs into signed rows, increments metrics, and batches them -> `ClickHouseWriter::flush()` writes each table with retry-aware inserts and a circuit-breaker exit path -> `CursorManager::update_cursor()` atomically renames a temp file into the cursor file after a successful flush -> the benchmark and cursor tests verify write-back, restart persistence, and the atomic temp-file contract.

- E1 source verified: `src/exex/mod.rs:24-30,60-123,124-204,213-311` defines the ExEx runtime, the backfill pass, live reorg handling, and the flush-on-shutdown path.
- E1 source verified: `src/db/writer.rs:6-198` implements retry-bounded ClickHouse insertion, transient/permanent error discrimination, and table-by-table flush logic.
- E1 source verified: `src/utils/cursor.rs:5-65` implements the durable cursor file with temp-rename updates and restartable `last_processed_block` state.
- E2 test verified: `src/utils/cursor.rs:73-164` covers new-file startup, update/reload persistence, multi-update persistence, and atomic temp-file cleanup.
- E2 test verified: `tests/benchmark.rs` exercises the ClickHouse write path and cursor/batch behavior against the benchmark harness.

## Architecture

Principal components:

- ExEx notification loop for canonical and reverted chain events.
- Block/log/storage-diff transform layer.
- Batcher and ClickHouse writer for columnar sinks.
- Cursor manager for restart-safe progress.
- Benchmark harness for throughput and backfill behavior.

Most interesting mechanism: the indexer does not treat chain motion as a single forward-only stream. It explicitly handles committed, reverted, and reorged windows, and the cursor advances only after the batch is durably flushed.

Baseline comparison: a naive chain scanner would read a head, write rows, and assume the chain stays put. Shadow-index keeps the reorg/revert path in the same runtime loop and separates durable progress from the sink writes.

## Reuse Guidance

Reusable:

- Keep a durable cursor separate from the sink tables.
- Treat chain reorgs as first-class notifications, not exceptional log noise.
- Update the cursor only after the sink flush succeeds.
- Bound retries and expose circuit-breaker failure when the sink remains unavailable.

Do not copy:

- Do not copy the ClickHouse schema or row shapes directly.
- Do not rely on a single sink backend if the sink semantics differ from ClickHouse.
- Do not let a sink flush advance the cursor before the batch is durable.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The code separates notification handling, transform logic, sink writes, and cursor persistence.
- Retry and circuit-breaker behavior is explicit in source.
- The cursor implementation has restart and atomic-write tests.

Experimental or incomplete for our needs:

- The implementation is strongly shaped around reth ExEx and ClickHouse.
- The sink contract is not a generic event-store abstraction.
- Live chain correctness still depends on the upstream node and sink durability.

Hidden costs and failure modes:

- A bad cursor update can replay or skip chain ranges.
- ClickHouse backpressure can trip the circuit breaker and halt the node.
- Reorg and revert processing can double the write volume around unstable heads.

Adoption experiment:

Run the indexer against a reorg-injecting chain fixture, stop it mid-flush, restart it, and verify that the cursor and sink rows converge without duplicate active rows.

## Candidate Patterns

- `reorg-safe exex materialization`
- `atomic cursor checkpoint`
- `retry-bounded columnar sink`
