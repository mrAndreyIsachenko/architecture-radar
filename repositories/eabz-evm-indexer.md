# eabz/evm-indexer

- Repository: https://github.com/eabz/evm-indexer
- Review date: 2026-09-28
- Current commit reviewed: `e4ca46486837b85aadccd009ca742f1799801a67`
- Commit date: 2026-09-21T08:45:14-06:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: selected

## Problem Fit

This repository informs `blockchain-intelligence`, especially reorg-safe indexing, gap healing, module backfills, and coverage-floor semantics. The reusable mechanism is the reorg / purge / reinsert control plane around ClickHouse materialization, not the chain-specific analytics modules or the control panel.

## Verified Flow

`README.md` defines the coverage floor and the read-path contract -> `src/reorg/mod.rs` defines the fork search, `ReorgGuard`, `Purger::purge_range`, epochs, and the no-DELETE repair model -> `src/pipeline/backfill.rs` scans stored logs, detects differences, purges only the changed module rows, bumps the chain epoch, and reinserts chunked rows -> `src/reorg/tests.rs` and `src/pipeline/sync_tests.rs` cover shallow/deep reorgs, max-depth fatal errors, start-block floors, holes, and restart / failure behavior.

- E1 source verified: `src/reorg/mod.rs:1-27, 73-145, 159-260` documents the reorg model, `ReorgStore`, `Purger`, epoch semantics, and the insert-only repair contract.
- E1 source verified: `src/reorg/fork.rs:1-108, 110-196` implements the growing-window fork-point search with explicit floor and max-depth bounds.
- E1 source verified: `src/pipeline/backfill.rs:1-33, 61-218` defines the scan / purge / reinsert backfill contract and the chunking logic for monthly partition boundaries.
- E2 test verified: `src/reorg/tests.rs:67-200` covers shallow and deep forks, max-depth fatal behavior, start-block floors, holes, and genesis mismatch handling.
- E2 test verified: `src/pipeline/sync_tests.rs:1-240` covers resume, gap healing, live tail behavior, and failure handling without HyperSync or ClickHouse.

## Architecture

Principal components:

- Reorg primitives and fork-point search.
- Epoch-based purge and repair over ClickHouse tables.
- Module-specific backfill over stored logs and transactions.
- Live sync loop with restart and gap-healing support.
- Test-only in-memory stores and chains for deterministic reorg verification.

Most interesting mechanism: the indexer never treats a replayed module as a fresh append. It first scans and compares stored data, then purges just the changed module rows, bumps the epoch, and reinserts the repaired rows so aggregates stay consistent without a full resync.

Baseline comparison: a naive blockchain indexer would either delete and rebuild whole tables or force a full chain resync on every decoder fix. EVM Indexer instead keeps a stable coverage floor, repairs only the affected module range, and makes the reorg boundary explicit.

## Reuse Guidance

Reusable:

- Keep a coverage floor and a bounded fork search.
- Separate scan, purge, and reinsert phases.
- Use epochs or equivalent generation markers for aggregate repair.
- Make backfill idempotent when the decoded rows already match storage.

Do not copy:

- Do not copy the ClickHouse / HyperSync deployment assumptions without the same operational envelope.
- Do not treat the control panel or chain-specific analytics as the mechanism itself.
- Do not rely on live indexing and backfill racing unless the same epoch semantics are preserved.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Clear read-path and repair rules in the binding design docs.
- Deterministic fork-point search with explicit fatal limits.
- Tests for reorg depth, holes, start blocks, and restart behavior.

Experimental or incomplete for our needs:

- The review did not run a live HyperSync / ClickHouse operational workload.
- Monthly partition boundaries and backfill chunking are workload-sensitive.
- The operational envelope is narrower than a fully general chain-ETL framework.

Hidden costs and failure modes:

- The wrong coverage floor can hide data outside the intended window.
- A too-deep reorg becomes fatal by design, which is correct but operator-visible.
- ClickHouse partitioning and chunk splitting add operational tuning burden.

Adoption conditions:

- Validate the same repair path against live chain churn and storage pressure.
- Confirm epoch repair keeps aggregates coherent after restart.
- Keep the coverage floor and decoder contract under version control.

## Candidate Patterns

- `reorg-safe materialization window`
- `purge-and-reinsert module backfill`
- `epoch-based aggregate repair`
- `bounded fork-point search`
