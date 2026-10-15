# TencentCloud/TencentDB-Agent-Memory

- Repository: https://github.com/TencentCloud/TencentDB-Agent-Memory
- Review date: 2026-10-10
- Current commit reviewed: `274e549069ad780e411d70e6fff51f6a977d81d3`
- Commit date: 2026-10-10T10:31:39+08:00
- Branch: `feat/server_team`
- Previous commit reviewed: `8b86874a2daea49e3ff0fb53d699203146c5c77d`
- Material changes since previous review: The earlier review covered layered session recovery; this review examines marker-gated request rewriting, session-init orchestration, and outbound-body verification.
- Decision: track

## Problem Fit

This repository informs `ai-llm-systems`, especially agent memory, context engineering, tool injection, provenance-aware request rewriting, and session-scoped memory writes. The reusable mechanism is the proxy plus staged pipeline, not the product-facing memory branding.

## Verified Flow

`src/index.ts` parses config, initializes logging, tracing, auth, storage, and optional control-plane features -> `createApp()` in `src/server.ts` installs marker gates, health checks, bridge routes, and agent-prefixed endpoints -> `InjectionPipeline.process()` parses the request body into an agent context, resolves the agent profile from URL identity, executes hooks, and serializes the modified body -> `stageSessionInitOrchestrate()` recovers or initializes the session state machine, decides whether to intercept, and normalizes the response path -> `stageMemCommand()` recognizes `mem:` commands, executes them, and returns the intercepted response envelope -> `SqliteStorage` and `FsStorage` provide atomic KV persistence, CAS writes, prefix deletion, and TTL behavior for the proxy state.

- E1 source verified: `MemoryProxy/src/index.ts:1-118` initializes the proxy subsystems, request-preparation lifecycle, and graceful shutdown path.
- E1 source verified: `MemoryProxy/src/server.ts:1-260` registers the marker gates, health endpoint, bridge routes, session-management endpoints, and agent-prefixed protocol routes.
- E1 source verified: `MemoryProxy/src/injection/pipeline.ts:1-260` implements adapter parsing, agent-profile lookup, hook execution, observer callbacks, and safe continuation on hook failures.
- E1 source verified: `MemoryProxy/src/pipeline/stages/session-init-orchestrate.ts:1-230` factors the shared session-init recovery/state-machine logic into a parameterized orchestration stage.
- E1 source verified: `MemoryProxy/src/pipeline/stages/mem-command.ts:1-121` isolates `mem:` command parsing and execution from the protocol handlers.
- E1 source verified: `MemoryProxy/src/storage/sqlite-storage.ts:19-134` and `MemoryProxy/src/storage/fs-storage.ts:19-164` implement the persistence backends with atomic writes, CAS semantics, prefix deletion, and TTL sweeps or cleanup.
- E2 test verified: `MemoryProxy/scripts/qa/p1-api-test.sh:61-220` exercises model gating, header preselection, session-init, and memory-command paths.
- E2 test verified: `MemoryProxy/scripts/qa/p1-dump-verify.py:1-220` captures outbound requests to prove injection is present in the final body rather than only in intermediate logs.
- E2 test verified: `MemoryProxy/scripts/qa/cc-session-reset-smoke.py:1-110` exercises the real CLI reset flow and the re-prompt behavior after reset.

## Architecture

Principal components:

- Hono route factory with path markers for guarded behavior.
- Injection pipeline that parses protocol-specific bodies into a common agent context.
- Shared session-init orchestrator that deduplicates the state machine across runners.
- Memory-command intercept stage for `mem:` tools and reset flows.
- Pluggable storage backends with SQLite, filesystem, memory, and COS-style behavior.
- QA scripts that validate route gating, outbound rewrite, and reset recovery.

Most interesting mechanism: marker-gated request rewriting with session-scoped recovery. A request can be gated, prewarmed, rewritten, or bypassed based on URL shape and headers, while the session-init stage recovers previously bound state and the memory-command stage can short-circuit to a dedicated response path.

Baseline comparison: a generic proxy would forward the request and perhaps add one static system prompt. This proxy carries a much richer control plane, including identity selection, per-request injection, session recovery, health degradation, and command interception.

## Reuse Guidance

Reusable:

- Use explicit URL markers for opt-in request rewriting.
- Separate session recovery from command interception.
- Keep storage backends swappable, but make degraded storage visible in health.
- Treat outbound-body inspection as the source of truth for injection verification.

Do not copy:

- Do not copy the large protocol matrix without the same operational needs.
- Do not assume header preselection or agent identity can be implicit.
- Do not treat process-local storage as acceptable in multi-instance deployments.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Health reporting distinguishes shared-storage expectations from degraded process-local fallbacks.
- Session-init and mem-command behavior are factored into reusable stages instead of being duplicated in each runner.
- The repository ships runnable QA scripts that cover both functional and observational validation.
- Storage semantics are explicit about atomicity and TTL buckets.

Experimental or incomplete for our needs:

- The refactor is still in progress and the pipeline remains highly parameterized.
- The review did not execute the proxy against a full live upstream/storage deployment.
- The operator still needs to provide the right identity headers for the richer session flows.

Hidden costs and failure modes:

- The route surface is large and protocol-specific, which increases coupling to client conventions.
- Process-local storage fallback can silently reduce deployment correctness if health is ignored.
- Session-init and memory-command behavior depend on the correctness of injected identity and preselection headers.

Adoption experiment:

Run the proxy against a real upstream and a real persistent backend, then validate that session init, memory injection, and `mem:` commands still work while the health endpoint reports degraded storage only when shared storage is genuinely unavailable.

## Candidate Patterns

- `marker-gated request rewrite pipeline`
- `session-scoped memory injection stage`
- `degraded storage health gate`
- `session-init recovery orchestrator`
- `atomic prefix-backed proxy KV`

## Previous Review

The earlier review covered layered session recovery; this review examines marker-gated request rewriting, session-init orchestration, and outbound-body verification.

Earlier evidence remains pinned to `8b86874a2daea49e3ff0fb53d699203146c5c77d` in the [report for 2026-10-04](../reports/2026-10-04.md) and the [previous card](https://github.com/mrAndreyIsachenko/architecture-radar/blob/591083a2bcc57b16fc2596c8fd2d78759c4c4f7a/repositories/TencentCloud-TencentDB-Agent-Memory.md). Its open validation experiments remain in the backlog; this source review does not mark them completed.
