# 84hero/evm-scanner

- Repository: https://github.com/84hero/evm-scanner
- Review date: 2026-08-26
- Current commit reviewed: `2fccb37c9f888a9f288f7b9acee01541379e217b`
- Commit date: 2025-12-19T23:59:27+08:00
- Branch: `master`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `blockchain-intelligence`, especially incremental event scanning, resumable cursor management, and reorg-aware delivery of decoded blockchain events. The reusable mechanism is the scanner loop and its storage/rpc split, not the marketing claim that it is "production-ready."

## Verified Flow

`cmd/scanner-cli/main.go` loads config, builds pools, starts gRPC streaming, and wires the scanner to output sinks -> `pkg/scanner/scanner.go` determines the starting block from saved cursor or rewind config, polls the chain, computes a safe head using the confirmation window, scans block ranges, and advances the cursor -> `pkg/rpc/client.go` chooses the best RPC node and falls back across nodes when one fails -> `pkg/storage/memory.go` and `pkg/storage/postgres.go` persist cursor state -> `pkg/sink` fans decoded outputs into database, webhook, and queue sinks -> tests verify start-block selection, bloom gating, scan-range delivery, cursor persistence, and RPC failover.

I verified the package surface with `go test ./pkg/...`, which passed.

## Architecture

Principal components:

- `pkg/scanner` for the polling loop, confirmation window, and block-range scanning.
- `pkg/rpc` for node selection, failover, and RPC request dispatch.
- `pkg/storage` for cursor persistence across memory, Redis, and PostgreSQL.
- `pkg/sink` for downstream delivery.
- `cmd/scanner-cli` for config assembly and process wiring.

Most interesting mechanism: the scanner only processes `safeHead = head - ReorgSafe`, so it deliberately trades immediate head tracking for a confirmation window. That keeps cursor advancement simple and makes reorg exposure explicit rather than hidden inside the delivery path.

Baseline comparison: a naive indexer would stream blocks directly from one RPC endpoint and advance a cursor after every response. EVM Scanner adds a confirmation window, multi-RPC failover, cursor rewind on restart, and a Bloom-based fast path for sparse scans.

## Reuse Guidance

Reusable:

- Keep a confirmation window around live event scanning.
- Persist a resumable cursor separate from the delivery sink.
- Use multiple RPC nodes and choose among them rather than assuming a single backend is stable.
- Make the fast path explicitly opt-in with tests around the gating heuristics.

Do not copy:

- Do not confuse this with a full blockchain state indexer; it is explicitly scoped to events.
- Do not rely on the in-memory store for anything durable.
- Do not treat the reorg tolerance claim as a full orphan-branch repair system.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The repository has a real Go test suite covering scanner startup, scan-range behavior, storage backends, and RPC failover.
- The storage layer has separate memory, Redis, and PostgreSQL implementations.
- The scanner loop keeps the control flow straightforward enough to reason about with tests.

Experimental or incomplete for our needs:

- The README is explicit that the project does not do balance indexing or state reconstruction.
- Reorg handling is confirmation-window based rather than full branch reconciliation.
- Final correctness still depends on the reliability of upstream RPC endpoints and sink behavior.

Hidden costs and failure modes:

- A too-small confirmation window can expose the scanner to short reorgs.
- A too-large window increases lag and delays downstream observability.
- Memory-backed cursor storage is not durable.
- Multi-RPC selection adds operational complexity and can hide backend inconsistency if the scoring logic is wrong.

Adoption experiment:

Run one scan against a controlled RPC pair, restart mid-stream, and verify that the cursor resumes correctly, the safe-head window holds back unfinalized blocks, and the downstream sink sees no duplicate writes.

## Candidate Patterns

- `confirmation-capped event scanner`
- `multi-RPC cursor scanner`
- `sink-separated delivery pipeline`
