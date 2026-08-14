# clearideas/agent-runtime

- Repository: https://github.com/clearideas/agent-runtime
- Review date: 2026-08-14
- Current commit reviewed: `c8a4856863405c817315bbd8ff89a07fea6b24a5`
- Commit date: 2026-08-10T21:46:37-04:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `ai-llm-systems`, especially durable agent runtimes, checkpointed workflows, execution recovery, and evidence-carrying run state. The reusable mechanism is the manifest-hashed checkpoint envelope with explicit resume/fail/suspend state transitions, not the broader agent product surface.

## Verified Flow

`AgentRuntime.#run` loads an existing run only when `resume` is requested, validates the manifest, enforces the step limit, checks that the latest checkpoint exists, and rejects a resume when the manifest hash does not match -> `buildExecutionWaves` computes contiguous execution waves with concurrency barriers so only tool-free prompt steps without runtime extensions can fan out -> step execution writes a checkpoint before advancing the cursor -> `AgentRuntime.#checkpoint` persists the run envelope through the configured store -> `AgentRuntime.#run` finalizes the run as `completed`, `suspended`, `cancelled`, or `failed` depending on the terminal path -> the file and SQLite stores fence attempts, sequence numbers, and lifecycle transitions so recovery remains deterministic across restarts.

- E1 source verified: `packages/core/src/agent-runtime.ts:726-847` validates resume state, load order, manifest hash, step limits, checkpoint presence, and attempt fencing before continuing a run.
- E1 source verified: `packages/core/src/execution-plan.ts:75-131` computes contiguous execution waves and only parallelizes tool-free prompt steps without runtime extensions.
- E1 source verified: `packages/core/src/agent-runtime.ts:1002-1058` persists suspended, cancelled, and failed runs as distinct lifecycle states and clears in-memory attempt/event cursors afterward.
- E1 source verified: `packages/core/src/agent-runtime.ts:1391-1438` writes checkpoint envelopes with manifest hash, contract/runtime versions, cursor, state, step results, transcript, artifacts, continuation, and budget.
- E1 source verified: `packages/store-local/src/run-store.file.ts:48-249` uses atomic same-directory rename, run locks, checkpoint sequence fencing, and attempt checks for file-backed durability.
- E1 source verified: `packages/store-sqlite/src/index.ts:28-238` uses a durable SQLite store with `BEGIN IMMEDIATE`, WAL mode, sequence validation, and attempt fencing.
- E2 test verified: `packages/core/src/agent-runtime.test.ts:312-345` verifies that a checkpoint failure prevents later steps from executing.
- E2 test verified: `packages/core/src/agent-runtime.test.ts:919-1005` verifies manifest mismatch rejection and nested continuation resume.
- E2 test verified: `packages/store-local/src/run-store.file.test.ts:64-180` verifies atomic run/checkpoint writes, terminal lifecycle persistence, and same-process fencing.

## Architecture

Principal components:

- `AgentRuntime` as the orchestration loop.
- `buildExecutionWaves` as the execution planner.
- `RunStore` implementations for local files and SQLite.
- `RunCheckpoint` as the durable envelope for resume state.
- Event emission and token-budget tracking as side channels attached to the run lifecycle.

Most interesting mechanism: the runtime treats the checkpoint as the authoritative replay boundary. The checkpoint is not just a log entry; it carries the manifest hash, cursor, execution state, active tails, and budget snapshot, so resume can reject drift before work restarts.

Baseline comparison: a simpler workflow runner would replay from the top, rely on volatile process memory, or treat a checkpoint as an informational audit row. This implementation couples execution planning with recoverable state and makes lifecycle transitions explicit in the store.

## Reuse Guidance

Reusable:

- Put the manifest hash on the checkpoint and refuse resume when the live manifest diverges.
- Fence retries with an attempt counter so a resumed run cannot overwrite another attempt's state.
- Keep atomic file writes or SQLite transactions as the storage primitive for run recovery.
- Separate suspended, failed, cancelled, and completed records instead of collapsing them into one terminal state.

Do not copy:

- Do not copy the whole agent surface or manifest schema unless the same recovery semantics are required.
- Do not copy the parallel-wave planner if the runtime does not need ordered checkpoint replay.
- Do not assume the file-backed store is sufficient for cross-process takeover; the repository itself says SQLite or another CAS-capable backend is needed for that.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Resume, suspend, cancel, fail, and complete are all represented in the runtime and the stores.
- The store implementations enforce sequence monotonicity and attempt ownership.
- The execution planner explicitly avoids unsafe fan-out.
- Tests cover checkpoint failures, manifest mismatch, nested continuation, and store fencing.

Experimental or incomplete for our needs:

- The checkpoint envelope is runtime-specific rather than a generic provenance standard.
- Parallel execution is intentionally conservative and limited to a narrow step shape.
- Cross-process takeover still depends on the chosen store backend and its coordination guarantees.

Hidden costs and failure modes:

- Checkpointing every committed step adds storage and serialization overhead.
- Resume safety depends on stable manifest hashing and consistent step ordering.
- The file store is durable for a single process, but not by itself a multi-writer coordination mechanism.
- A failed checkpoint leaves the run in a partial state and requires explicit recovery semantics upstream.

Adoption conditions:

- Require a manifest hash check, attempt fencing, and at least one failure-injection test before adopting the pattern.
- Validate the store backend under concurrent resume and crash-recovery load.
- Confirm that any downstream state projection can tolerate replay from the checkpoint cursor.

## Candidate Patterns

- `manifest-hashed checkpoint envelope`
- `attempt-fenced run recovery`
- `dependency-safe execution waves`
