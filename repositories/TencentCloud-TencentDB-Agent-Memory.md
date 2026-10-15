# TencentCloud/TencentDB-Agent-Memory

- Repository: https://github.com/TencentCloud/TencentDB-Agent-Memory
- Review date: 2026-10-04
- Current commit reviewed: `8b86874a2daea49e3ff0fb53d699203146c5c77d`
- Commit date: 2026-09-29T16:48:48+08:00
- Branch: `feat/server_team`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `ai-llm-systems`, especially team-level memory, session recovery, and multi-agent routing. The reusable mechanism is the layered recovery chain that keeps in-memory state, durable session rows, and binding rows synchronized across proxy restarts.

## Verified Flow

`createApp()` eagerly activates storage and binding backends, installs marker-gated routes, and exposes health and agent-specific endpoints. Session recovery then hydrates initialized rows from the durable repository, probes the live L2a row, falls through to L2b bindings when needed, and rebuilds the session from binding plus metadata before writing the recovered state back to L1 and L2a.

- E1 source verified: `MemoryProxy/src/server.ts:20-105` eagerly activates storage, gates `/cost-guard` and `/analyse`, and exposes health and bridge routes.
- E1 source verified: `MemoryProxy/src/server.ts:281-352` registers DeepSeek, OpenCode, Codex, Workbuddy, and generic agent routes behind the proxy dispatcher.
- E1 source verified: `MemoryProxy/src/session/store.ts:279-433` hydrates initialized sessions from disk, probes L2a, falls back to L2b bindings, and dispatches to rebuild or history-scan recovery.
- E1 source verified: `MemoryProxy/src/session/store.ts:451-668` validates L2a rows, deduplicates rebuilds, reconstructs session identity, and writes the rebuilt state back through the repo.
- E1 source verified: `MemoryProxy/src/db/sessionRepo.ts:161-260` defines the durable session repository contract and the SQLite-backed load/get/upsert path.
- E1 source verified: `MemoryProxy/src/db/binding-repo.ts:23-123` persists binding rows with TTL, key serialization, and last-seen refresh.
- E1 source verified: `MemoryCore/src/gateway/chat-memory-handlers.ts:183-219` clears chat-memory content without deleting the asset record, keeping ownership and routing intact.
- E2 test verified: `MemoryProxy/src/__tests__/opencode-user-input.test.ts:21-52` strips recalled memory from the human message before classification.
- E2 test verified: `MemoryProxy/src/__tests__/opencode-reporting.test.ts:33-189` keeps reporting aligned to the user text rather than the recalled memory.

## Architecture

Principal components:

- Hono HTTP proxy and route gate.
- L1 in-memory session cache.
- L2a durable session repository.
- L2b binding repository for recovery.
- Metadata-backed rebuild path.
- Memory-content clear path that preserves asset ownership.

Most interesting mechanism: the session store does not treat one cache as authoritative. It explicitly layers L1, durable L2a rows, L2b bindings, and a history-scan fallback, then promotes recovered state back into the cache and repository so later requests do not repeat recovery work.

Baseline comparison: a simpler memory proxy would keep state in memory and recreate sessions from request history after restart. This implementation keeps durable rows, binding recovery, and rebuild promotion in separate stages so the restart path is explicit.

## Reuse Guidance

Reusable:

- Model recoverable session state as a layered chain instead of a single cache.
- Keep a durable session row and a binding row separate when the binding may outlive or outscope a single request.
- Promote recovered state back into the hot cache and durable store once recovery succeeds.
- Preserve memory content and asset identity as separate operations.

Do not copy:

- Do not copy the route table or product-specific agent prefixes as a generic integration shape.
- Do not assume the current recovery chain is sufficient without a live restart test.
- Do not let fallback scanning become a silent bypass for truly new sessions or identity mismatches.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The proxy, repository, binding, and content-clear paths are all explicit source modules.
- Recovery validates user identity and stale-pending expiration before reusing state.
- Tests verify that recalled memory is not mistaken for fresh human input.

Experimental or incomplete for our needs:

- The review did not validate a real proxy restart with live persisted sessions.
- The L2b rebuild path still depends on external metadata availability.
- Marker-gated routing and agent prefixes are product-specific integration details.

Hidden costs and failure modes:

- Cross-node recovery can degrade to bypass when metadata is unavailable.
- Stale cache entries can still produce confusing behavior if identity checks are bypassed upstream.
- Multi-layer recovery raises operational complexity and makes failure attribution harder when a request falls through several stages.

Adoption experiment:

Restart the proxy while initialized sessions exist in L2a and L2b, then confirm the process rehydrates the same session identity and memory injection state without replaying the initial form flow.

## Candidate Patterns

- `layered session recovery chain`
- `durable session promotion after rebuild`
- `content-only memory clear`
