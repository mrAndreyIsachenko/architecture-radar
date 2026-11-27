# fractal-bitcoin/fractal-indexer

- Repository: https://github.com/fractal-bitcoin/fractal-indexer
- Review date: 2026-11-27
- Current commit reviewed: `74339027c25e19c8ee1a69ff34daf0de45242d3c`
- Commit date: 2026-11-27T10:32:14-03:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: selected

## Problem Fit

This repository informs `blockchain-intelligence`, especially incremental indexing, transaction interpretation, and reorg-safe materialization. The reusable mechanism is the WAL-backed repair path that keeps provisional chain materialization reversible while ClickHouse mutations clean up orphaned rows.

## Verified Flow

`main.go` parses config, enables WAL and reorg settings, and initializes Redis/ClickHouse -> `task.CheckAndRecover()` reconciles current height and reorg state -> `task/serial/sync_block.go` parses blocks and writes them in the serial sync path -> `task/serial/sync_revert.go` emits revert rows for spent UTXOs, new outputs, and NFT identifiers -> `store/process_sync.go` issues ClickHouse mutations for orphan cleanup and polls for completion -> `api/lib/brc20_swap/indexer/indexer.go` and `store_into_data_test.go` cover the data-shaping side of the swap indexer.

- E1 source verified: `main.go` wires WAL, reorg limits, and the process initialization path.
- E1 source verified: `task/block.go` and `task.CheckAndRecover()` coordinate chain height and recovery state.
- E1 source verified: `task/serial/sync_block.go` implements the serial block sync and write path.
- E1 source verified: `task/serial/sync_revert.go` emits the revert records used to repair provisional data.
- E1 source verified: `store/process_sync.go` drives the ClickHouse mutation and orphan-removal polling loop.
- E2 test verified: `api/lib/brc20_swap/indexer/store_into_data_test.go` verifies swap-indexer data shaping.
- E2 test verified: `task/serial/inscription_key_test.go` verifies the inscription-key parsing behavior used by the indexing pipeline.

## Architecture

Principal components:

- Chain-sync bootstrap and recovery orchestration.
- Serial block parsing and revert-row generation.
- ClickHouse mutation and orphan cleanup loop.
- Application-specific swap indexer and parser tests.

Most interesting mechanism: the indexer does not merely append blocks. It pairs WAL-backed sync with explicit revert rows and mutation polling so a repaired chain segment can be re-materialized without pretending the head was final.

Baseline comparison: a conventional chain indexer would materialize the head directly into its sink and hope reorgs stay shallow. This repository keeps the repair path explicit and uses ClickHouse mutation polling to converge after chain churn.

## Reuse Guidance

Reusable:

- Keep provisional materialization separate from repair materialization.
- Emit explicit revert data rather than relying on implicit deletes.
- Poll storage mutations to completion before treating a repair as finished.

Do not copy:

- Do not copy the Fractal-specific parsing surfaces if you only need the repair mechanism.
- Do not assume the mutation polling contract is free; it adds operational latency.
- Do not treat the current tests as proof of live reorg handling under production pressure.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Reorg repair is explicit in source rather than implied.
- The mutation cleanup path is separated from the normal parse path.
- The codebase includes targeted parser and data-shaping tests.

Experimental or incomplete for our needs:

- The review did not validate live chain reorg churn.
- The operational behavior under storage pressure still needs proof.
- The repair path depends on ClickHouse mutation semantics remaining stable.

Hidden costs and failure modes:

- A slow mutation queue can lengthen the repair window.
- A wrong revert scope can leave orphaned rows or double-materialized data.
- WAL and reorg configuration can drift from the downstream sink assumptions.

Adoption experiment:

Run the indexer with WAL enabled against a chain source that injects a real reorg, then confirm the revert rows, orphan cleanup, and height reconciliation converge without leaving duplicate materializations behind.

## Candidate Patterns

- `Reorg-Safe Materialization Windows`
- `WAL-backed ClickHouse reorg repair`
- `orphan-part mutation polling`
