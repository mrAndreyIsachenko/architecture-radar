# deepseek-ai/deepseek-harness

- Repository: https://github.com/deepseek-ai/deepseek-harness
- Review date: 2026-10-13
- Current commit reviewed: `d743267388641bc76f17c45ce8b4c231aed1d32c`
- Commit date: 2026-10-09T17:31:32+08:00
- Branch: `master`
- Previous commit reviewed: `d743267388641bc76f17c45ce8b4c231aed1d32c`
- Material changes since previous review: no upstream commit change since 2026-10-10. This additional source review examines checkpoint-before-dispatch and sandbox-mode replay at the same pinned commit; the earlier review examined the synchronous SDK and bundled-runtime lifecycle.
- Decision: track

## Problem Fit

This repository informs `ai-llm-systems`, especially durable agent workflows, tool-use recovery, and checkpointed execution around model and shell dispatch. The reusable mechanism is the semantic checkpoint barrier: session state is flushed before model or top-level tool execution, and sandbox mode is replayed from durable session state instead of being treated as ephemeral request context.

## Verified Flow

Session- and tool-level input -> `session-checkpoint-policy.apply` intercepts `llm/stream`, `tools/execute`, and `agent/pre-step` -> `ctx.sessions.flush(...)` forces a durability barrier before the next model request, top-level tool dispatch, or agent step -> `SessionPersistence`/`SessionHandle` keep session events contiguous from seq 0 and make `flush()` the persistence boundary -> `JsonlSessionPersistence` materializes immutable generation files under a write lease and validates storage fail-closed -> `sandbox-policy` reads and writes durable sandbox mode events so the shell runtime can replay the same mode decision after restart -> crash-recovery tests verify that the checkpoint boundary prevents dispatch after a checkpoint failure and preserves the logged prefix.

- E1 source verified: `packages/session/session-persistence/src/index.ts:117-180,182-203` defines the append-only session-storage contract, per-session handles, and `flush()` as the durability barrier.
- E1 source verified: `packages/session/session-checkpoint-policy/src/index.ts:20-82` flushes session state before model dispatch, top-level tool execution, and agent pre-step execution, and fail-closes on checkpoint failure.
- E1 source verified: `packages/session/session-persistence-jsonl/src/index.ts:61-75,245-260` defines the JSONL backend, its format/compression contract, and the session-persistence service binding.
- E1 source verified: `packages/sandbox/sandbox-policy/src/index.ts` and `packages/sandbox/sandbox-policy/src/session-mode.ts` keep sandbox mode as durable session state rather than ephemeral request-only state.
- E2 test verified: `packages/session/session-checkpoint-policy/tests/crash-recovery.e2e.ts` and `packages/session/session-checkpoint-policy/tests/session-checkpoint-policy.spec.ts` cover checkpoint-before-dispatch behavior and fail-closed recovery on crashes.
- E2 test verified: `packages/session/session-persistence-jsonl/tests/lease.spec.ts` covers cross-process write ownership, inode verification, and stale lock handling.
- E2 test verified: `packages/sandbox/sandbox-policy/tests/policy.spec.ts` covers default mode/root resolution, override replay, and durable sandbox-mode switching.

## Architecture

Principal components:

- Session persistence service with per-session handles and a durability barrier.
- JSONL backend with immutable generation files, migration preparation, and write leasing.
- Semantic checkpoint policy that flushes before model and tool boundaries.
- Sandbox policy and shell integration that replay durable mode decisions.
- Workspace registry that keeps durable session metadata and archived/pinned workspace state.

Most interesting mechanism: the runtime treats flush-before-dispatch as the safety boundary. The system does not wait for the entire conversation to end; a checkpoint failure prevents downstream dispatch. This does not establish at-most-once external execution: a crash after an external effect but before its result is persisted still requires idempotency or reconciliation on recovery.

Baseline comparison: a simpler agent runtime would append logs asynchronously and let the shell or model adapter proceed on the assumption that a later flush will be fine. Deepseek Harness instead makes persistence a semantic precondition for model/tool dispatch and uses durable sandbox mode state to replay the same execution posture.

## Reuse Guidance

Reusable:

- Put durability barriers directly in model/tool dispatch hooks.
- Treat sandbox mode or execution posture as durable state, not request-local metadata.
- Use a handle-based session store so the runtime can flush one session or every active write handle explicitly.
- Keep the storage backend fail-closed when it encounters unknown or torn records.

Do not copy:

- Do not copy the runtime without a real restart or process-kill validation on the same session ledger.
- Do not assume the JSONL generation layout is a generic format; it is tightly coupled to this runtime's session and migration contract.
- Do not treat flush-before-dispatch as free: it buys safety by adding latency and backend pressure.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The checkpoint barrier is enforced at the semantic boundary where side effects can start.
- The session persistence contract is explicit about contiguity, ownership, and durability.
- The backend validates leases and storage state rather than trusting a best-effort append.
- Crash-recovery and policy tests cover the intended safety boundary.

Experimental or incomplete for our needs:

- The reviewed evidence still needs a live process-kill and restart cycle on the same runtime path, not only source-level crash-recovery tests.
- The shell/workspace integration is strong, but it remains a runtime boundary with file-system and lease semantics that need operational proof under contention.

Hidden costs and failure modes:

- Flush-before-dispatch can amplify backend latency into user-visible pauses.
- A stale or lost write lease can make replay and recovery dependent on filesystem behavior.
- Session-mode replay only helps if every side-effecting path routes through the same persistence barrier.

Adoption experiment:

Kill the runtime after a request prefix or top-level tool call has been flushed, restart the same session ledger, and confirm that the same request prefix, sandbox mode, and tool intent reappear without duplicate side effects.

## Candidate Patterns

- `semantic checkpoint barrier before dispatch`
- `durable sandbox-mode replay`
- `single-owner session write lease`

## Previous Reviews

The [2026-10-10 report](../reports/2026-10-10.md) examined SDK transport, notification routing, and bundled-runtime cleanup at the same commit. The [2026-10-04 report](../reports/2026-10-04.md) examined CLI/plugin approvals and JSONL replay at `5badb15009ae1756c3afe0ae0cef1faafc290ccc`. The [previous card](https://github.com/mrAndreyIsachenko/architecture-radar/blob/d1fe321f3a0a08355405865a6407c86a683ed560/repositories/deepseek-ai-deepseek-harness.md) preserves those source references. Their open runtime and restart experiments remain in the backlog; this review does not mark them completed.
