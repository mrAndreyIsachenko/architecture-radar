# bitcoincore-dev/nakamoto-electrs

- Repository: https://github.com/bitcoincore-dev/nakamoto-electrs
- Review date: 2026-08-20
- Current commit reviewed: `f9fc5ba17f38f6d45812e467a5299d194b086af8`
- Commit date: 2026-08-20T00:38:26-04:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `blockchain-intelligence`, especially reorg-safe indexing and Electrum-compatible transaction history. The reusable mechanism is the bridge from a push-based block source to a rollback-capable script-hash index.

## Verified Flow

`NakamotoBlockSource::new` starts event and block threads -> `BlockEvent::Connected`, `Disconnected`, and `Synced` are broadcast to subscribers -> `Indexer::start` listens to those events and applies or rolls back block-derived history -> `ElectrumServer` answers JSON-RPC requests from the current index state -> integration tests verify rollback and reorg replacement behavior.

- E1 source verified: `src/block_source.rs` defines the `BlockEvent` abstraction and the `BlockSource` trait used by the indexer.
- E1 source verified: `src/nakamoto_source.rs` converts nakamoto 0.29 wire types into bitcoin 0.30 types, runs separate event and block threads, and broadcasts connected/disconnected/synced events.
- E1 source verified: `src/indexer.rs` keeps per-script history plus a `by_height` reverse map so it can remove all entries for a disconnected height.
- E1 source verified: `src/indexer.rs` applies blocks on `Connected` and rolls back history on `Disconnected`.
- E1 source verified: `src/electrum_server.rs` dispatches Electrum JSON-RPC methods such as history, balance, headers, and transaction lookups against the current index and source.
- E2 test verified: `tests/integration_tests.rs::indexer_rollback_on_disconnected_event` verifies that a disconnected block is removed from history.
- E2 test verified: `tests/integration_tests.rs::indexer_reorg_replaces_history` verifies that a rollback followed by a replacement block at the same height removes the old history and preserves the new one.
- E2 test verified: `tests/integration_tests.rs` also covers tip advancement and metrics updates.

## Architecture

Principal components:

- `BlockSource` abstraction for push events plus point queries.
- `NakamotoBlockSource` bridge that converts nakamoto events into the crate's internal types.
- `Indexer` with script-hash histories and a height-indexed rollback map.
- Electrum JSON-RPC server.
- Integration tests and mock block sources.

Most interesting mechanism: the source bridge uses two background threads and a cross-version wire-format conversion boundary to turn nakamoto's event stream into a local block projection. The indexer then treats `Disconnected` as a first-class rollback signal and removes every history entry recorded at that height.

Baseline comparison: a conventional block indexer would append every connected block and hope the chain never reorgs. This repository instead models reorgs explicitly in the event stream and keeps a reverse lookup map so rollback is deterministic rather than heuristic.

## Reuse Guidance

Reusable:

- Treat block disconnection as a first-class event, not an exceptional shutdown path.
- Maintain a height-indexed reverse map for rollback instead of scanning the entire history.
- Keep the chain source behind a narrow trait so mocks and alternate backends can share the indexer.
- Test reorg replacement explicitly, not just forward sync.

Do not copy:

- Do not copy the placeholder Electrum semantics as-is if we need full wallet/account correctness.
- Do not rely on the bridge without live validation against the intended chain backend.
- Do not assume the current UTXO limitations are acceptable for production wallet features.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The rollback path is unit- and integration-tested.
- The event bridge is explicit about version conversion and subscription fan-out.
- The code distinguishes connected, disconnected, and synced transitions.

Experimental or incomplete for our needs:

- `get_balance` and `transaction.get` remain partial because there is no full UTXO set in the current design.
- Transaction broadcast is not yet fully wired to the nakamoto handle.
- The indexer is intentionally scoped to Electrum-style history rather than a full node wallet stack.

Hidden costs and failure modes:

- The bridge depends on event ordering and background thread liveness.
- Reorg depth configuration still matters for how far rollback can safely go.
- Placeholder Electrum responses can be misread as full wallet support if the limitations are not documented.

Adoption experiment:

Replay one controlled disconnect/reconnect sequence against a live backend and verify that history, tip height, and Electrum responses match the expected post-reorg chain state.

## Candidate Patterns

- `reorg-safe materialization windows`
- `rollback-capable script-hash index`
