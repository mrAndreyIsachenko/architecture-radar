# TencentCloud/TencentDB-Agent-Memory

- Repository: https://github.com/TencentCloud/TencentDB-Agent-Memory
- Review date: 2026-10-28
- Current commit reviewed: `42c6711c218b40d38d1d6b0ed4767bcc6069cbfd`
- Commit date: 2026-10-28T10:49:21+08:00
- Branch: `feat/server_team`
- Previous commit reviewed: `274e549069ad780e411d70e6fff51f6a977d81d3`
- Material changes since previous review: the current head adds a team-memory master switch, account-level session-default resolution, skill-selection mediation, and session-trace normalization on top of the existing marker-gated rewrite pipeline.
- Decision: track

## Problem Fit

This repository informs `ai-llm-systems`, especially provenance-aware request rewriting, memory injection, tool selection, and session-init orchestration. The reusable mechanism is no longer just a proxy rewrite pipeline; it is now a staged session-init path that combines team-memory gating, validated user defaults, and adaptive skill loading while preserving visible degraded-storage behavior.

## Verified Flow

HTTP request -> `createApp()` wires the Hono app, access-key middleware, storage activation, and route guards -> `stageTeamMemorySwitch()` checks whether team memory is enabled for the current instance and fails open on stage errors -> `resolveUserSessionDefault()` fetches the user default, verifies team membership, agent visibility, and task validity, then either returns a preset or a typed fallback reason -> `SkillSelectionService.select()` gathers candidates, builds a selection context, asks the configured strategy to pick one, and only loads content for the chosen skill/version -> `parseSseData()` and the session-trace helpers rebuild streamed SSE blocks into a stable reply model for downstream recording.

- E1 source verified: `MemoryProxy/src/server.ts:28-120,150-220` registers the main app factory, storage activation, marker gates, and session-management endpoints.
- E1 source verified: `MemoryProxy/src/pipeline/stages/team-memory-switch.ts:2-49` gates team memory per instance and fails open on stage errors.
- E1 source verified: `MemoryProxy/src/session/user-default.ts:2-182` resolves account defaults with lazy validation and typed fallback reasons instead of throwing.
- E1 source verified: `MemoryProxy/src/skill/selection/service.ts:2-165` performs candidate retrieval, strategy selection, and content loading with explicit skip reasons.
- E1 source verified: `MemoryProxy/src/session-trace/assemble.ts:1-88` reconstructs streamed model replies from SSE event blocks.
- E2 test verified: `MemoryProxy/scripts/qa/p1-api-test.sh:61-220` exercises model gating, session-init, and memory-command paths.
- E2 test verified: `MemoryProxy/scripts/qa/p1-dump-verify.py:1-220` verifies the outbound body actually contains the injected rewrite.
- E2 test verified: `MemoryProxy/scripts/qa/cc-session-reset-smoke.py:1-110` covers the real CLI reset flow and the re-prompt behavior after reset.

## Architecture

Principal components:

- Hono route factory with explicit marker gates and auxiliary bridge endpoints.
- Team-memory switch that lets the proxy disable or preserve memory behavior per instance.
- User-default resolver that validates stored defaults against the live team/agent/task catalog.
- Skill-selection service that separates candidate retrieval, strategy choice, and content loading.
- Session-trace assembly and reply normalization for streamed upstream content.
- Persistent storage and QA scripts that keep degraded behavior observable.

Most interesting mechanism: session-init is now a composition of gates, validated defaults, and adaptive selection rather than a single hidden branch. The proxy can fail open on stage errors, but it still preserves explicit fallback reasons, visible health degradation, and a bounded selection surface for skills.

Baseline comparison: a generic proxy would forward traffic, maybe add a static system prompt, and stop there. This implementation separates identity resolution, team-memory policy, request rewriting, and skill loading into independent stages with explicit fallbacks and observability.

## Reuse Guidance

Reusable:

- Use explicit feature gates for team-level behavior instead of hard-coding it into the main rewrite path.
- Validate stored defaults lazily against the live catalog so stale configuration degrades to a typed fallback rather than an exception.
- Separate candidate retrieval from selection and loading.
- Keep degraded-storage health visible when a shared backend is expected.

Do not copy:

- Do not copy the large route matrix without the same operational need for it.
- Do not assume process-local storage is acceptable in multi-instance deployments.
- Do not depend on model-mediated skill selection without a deterministic fallback and explicit logging.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The main app factory and route wiring are explicit rather than implicit.
- Fallback reasons for user defaults are typed and logged instead of being swallowed.
- Selection and loading are separated, which keeps candidate evaluation and content fetches independently observable.
- The QA scripts still cover gating, injection, and reset recovery at the current head.

Experimental or incomplete for our needs:

- The live proxy deployment against a real upstream and persistent backend still needs operational proof.
- The team-memory switch is fail-open, so the real operational contract still depends on downstream services behaving consistently.
- The selection service is only as deterministic as the configured strategy model.

Hidden costs and failure modes:

- The route surface is large and protocol-specific, which increases coupling to client conventions.
- Process-local fallback storage can silently reduce correctness if health is ignored.
- Team-memory and skill-selection decisions depend on catalog freshness and request identity being correct.

Adoption experiment:

Run the proxy with a live upstream and non-mocked storage backend, then exercise session init, memory injection, `mem:` commands, and degraded health reporting under real traffic.

## Candidate Patterns

- `team-memory master switch`
- `lazy validated user-session default`
- `candidate-gated skill loading`
- `streamed session-trace assembly`

## Previous Reviews

The [2026-10-10 report](../reports/2026-10-10.md) examined the marker-gated request rewrite pipeline and session-scoped memory injection at `274e549069ad780e411d70e6fff51f6a977d81d3`. The [2026-10-04 report](../reports/2026-10-04.md) examined layered session recovery at `8b86874a2daea49e3ff0fb53d699203146c5c77d`. The [previous card](https://github.com/mrAndreyIsachenko/architecture-radar/blob/591083a2bcc57b16fc2596c8fd2d78759c4c4f7a/repositories/TencentCloud-TencentDB-Agent-Memory.md) preserves those source references. The live backend experiment remains in the backlog; this review does not mark it completed.
