# drillcoder/voryn

- Repository: https://github.com/drillcoder/voryn
- Review date: 2026-10-19
- Current commit reviewed: `9cd57337332258c4019b4e7bfecfe21301b41450`
- Commit date: 2026-10-13T13:08:15Z
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: selected

## Problem Fit

This repository informs `blockchain-intelligence` through incremental indexing with explicit reorg handling, versioned worker cursors, and leader-locked workers. The useful mechanism is the ordered commit pipeline around the chain cursor, not the surrounding TypeScript service wrappers.

## Verified Flow

`HeadService.execute` reads the latest chain head, computes the safe floor, initializes or rebases the chain cursor, and enqueues missing block jobs -> `FetchService.execute` claims queued jobs, fetches block data, and marks jobs fetched or failed -> `SequencerService.execute` verifies the next fetched block, checks the parent hash, advances the chain cursor, or rolls back to the common ancestor and rewinds worker cursors -> `ReactionService.execute` waits for confirmations, loads events or transactions, processes them in batches, and advances reaction cursors only if the reorg version still matches.

- E1 source verified: `src/services/head-service.ts::HeadService.execute`, `::initializeCursor`, and `::rebaseCursorAndEnqueue` seed, rebase, and enqueue jobs around the live head.
- E1 source verified: `src/services/fetch-service.ts::FetchService.execute` and `::processClaimedJob` claim jobs, fetch block data, and mark jobs fetched or failed with retry handling.
- E1 source verified: `src/services/sequencer-service.ts::SequencerService.execute`, `::rollbackReorg`, and `::findCommonAncestor` enforce parent-hash continuity, delete orphaned rows, and rewind worker cursors when the chain forks.
- E1 source verified: `src/services/reaction-service.ts::ReactionService.execute` and `src/repositories/postgres/worker-cursors-repository.ts::advanceIfVersion`, `::rewindForReorg` gate reaction progress by reorg version and cursor position.
- E2 test verified: `test/integration/services/reaction-history-gap.test.ts::test("${stream} gap update blocks concurrent retention until its cursor is saved")` and `::test("${stream} rejects a gap detected before a PostgreSQL reorg rollback")` verify history-gap handling and rollback coordination.
- E2 test verified: `test/integration/services/transactional-reactions.test.ts::test("${streamType} commits business writes and progress together and resumes after restart")` verifies transactional progress and restart behavior.
- E2 test verified: `test/unit/services/sequencer-service.test.ts::test("sequencer service rolls back to common ancestor on parent hash mismatch")`, `test/unit/repositories/postgres/worker-cursors-repository.test.ts::test("rewindForReorg updates affected and lagging cursors in one statement")`, and `test/unit/postgres/leader-lock.test.ts::test("unlocks and returns a healthy client")` pin the reorg rewind, cursor update, and leader-lock behavior.

## Architecture

Principal components:

- Head service for safe floor calculation and job enqueueing.
- Fetch service for claim/fetch/save retry loops.
- Sequencer service for ordered commit and reorg rollback.
- Reaction service for confirmation windows and cursor advancement.
- Postgres worker-cursor repository and leader lock for concurrency control.

Most interesting mechanism: the indexer separates live head movement from committed state and then protects reaction progress with a reorg version. That means a stale batch cannot advance once a rollback has changed the cursor lineage.

Baseline comparison: a naive indexer would poll the chain and write derived data directly off the latest head. Voryn instead keeps fetched jobs, committed state, and reaction cursors distinct, so reorg recovery can be explicit rather than inferred after the fact.

## Reuse Guidance

Reusable:

- Keep head polling, fetch, commit, and reaction stages separate.
- Gate cursor advancement on a reorg version so stale work cannot win.
- Treat orphan deletion and cursor rewind as part of the same transaction.
- Use leader locks and claim semantics to keep one worker owning the commit stream.

Do not copy:

- Do not copy the Postgres schema as a general-purpose chain model without the same commit semantics.
- Do not assume the tests prove live RPC churn or storage pressure.
- Do not advance reaction cursors before the commit transaction completes.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The repository has clean stage boundaries between head, fetch, sequencer, reaction, and repository layers.
- The tests cover leader locking, reorg rewind, transactional progress, and history-gap handling.

Experimental or incomplete for our needs:

- Live chain churn and restart pressure still need operational proof.
- The evidence is strongest for source-level correctness, not for fleet-scale behavior.

Hidden costs and failure modes:

- A bad RPC endpoint or a missing block job can stall the pipeline.
- Reorg rollback depends on the downstream stores tolerating deletions and replay.
- Version gating can cause reaction batches to stop early, which is correct but operationally visible.

Adoption experiment:

Run the pipeline against a live RPC feed or forked chain, inject reorgs and storage pressure, and confirm the cursor, worker versions, and rollback deletes stay coherent across restart.

## Candidate Patterns

- `Reorg-Safe Materialization Windows`
- `strict ordered chain commit`
- `worker-cursor reorg rewind`
- `singleton leader lock`
