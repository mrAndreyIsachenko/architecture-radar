# fystack/multichain-indexer

- Repository: https://github.com/fystack/multichain-indexer
- Review date: 2026-08-02
- Current commit reviewed: `90f4b3156c36bf048ec513e395f7dadef66f32e1`
- Commit date: 2026-07-10T22:12:15+07:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `blockchain-intelligence`, especially transaction interpretation, deposit detection, restart-safe indexing, and reorg-safe materialization.

## Verified Flow

RPC block fetch -> worker mode selection -> bloom-filter address matching -> NATS JetStream emission for matched transfers -> KV/Redis persistence for progress and failed ranges -> regular worker handles reorg checks, catchup ranges, manual ranges, and rescans -> tests verify per-chain worker isolation and catchup state bootstrapping.

- E1 source verified: `README.md` describes live blocks, gap backfill, failed retries, manual rescans, bloom filters, JetStream, and KV-based restart safety.
- E1 source verified: `internal/worker/regular.go` persists latest blocks, queues catchup ranges, handles reorg rollback, and advances progress only after successful processing.
- E1 source verified: `internal/worker/manual.go` drains missing ranges from Redis, processes them, and removes completed ranges.
- E1 source verified: `internal/worker/factory_test.go` verifies per-chain failed-channel isolation and catchup-range bootstrapping into the status registry.

## Architecture

Principal components:

- Regular, catchup, manual, and rescanner worker modes.
- Bloom filter matcher for address fanout.
- KV store for progress and failed-block persistence.
- Redis-backed queue for missing ranges.
- NATS JetStream for downstream event delivery.

Most interesting mechanism: the system splits indexing into a small set of cooperating workers, each with a separate recovery role. The result is a restart-safe, reorg-aware indexer that can resume exactly where it left off and still backfill gaps.

Baseline comparison: a conventional chain listener would subscribe to head blocks and emit events directly. This repo adds durable progress markers, explicit catchup/backfill, and a separate manual repair loop.

## Reuse Guidance

Reusable:

- Split live indexing, catchup, manual repair, and retry paths into distinct workers.
- Persist progress and failure state separately from the event sink.
- Keep a separate explicit reorg-handling path rather than folding rollback into the hot loop.

Do not copy:

- Do not trust the bloom filter for ledger-critical crediting without a second validation step.
- Do not copy the product claim that the filter itself is authoritative; it is probabilistic.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Clear worker decomposition and recovery roles.
- Tests cover cross-chain isolation and catchup bootstrap.
- The README documents failure and recovery semantics explicitly.

Experimental or incomplete for our needs:

- The repo still needs chain-specific validation before money movement is triggered.
- The review did not run the live indexer locally.

Hidden costs and failure modes:

- Bloom filters can generate false positives.
- Reorg windows and retry queues create operational tuning pressure.
- Multi-chain concurrency increases provider and state complexity.

Adoption experiment:

Prototype a blockchain deposit monitor that persists latest block numbers, queues reorg-safe catchup ranges, and refuses to credit the ledger until a second validation step confirms the destination address.

## Candidate Patterns

- `reorg-safe materialization workers`
- `bloom-filter address fanout`
