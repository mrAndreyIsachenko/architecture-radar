# deepseek-ai/deepseek-harness

- Repository: https://github.com/deepseek-ai/deepseek-harness
- Review date: 2026-10-04
- Current commit reviewed: `5badb15009ae1756c3afe0ae0cef1faafc290ccc`
- Commit date: 2026-10-03T11:48:13+08:00
- Branch: `master`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `ai-llm-systems`, especially recoverable agent-loop execution, exact-version plugin approval, and replay-safe session persistence. The reusable mechanism is the harness boundary that keeps CLI dispatch, plugin gating, and session recovery aligned.

## Verified Flow

`runCli()` parses the command mode and dispatches to profile, plugin, or config-dump execution. The plugin path checks exact-version exemptions before allowing package operations, and the session backend registers a JSONL persistence provider whose handles serialize writes on a single mutation chain, enforce monotonic reads, and drain live writes through the same durable path.

- E1 source verified: `apps/cli/src/bin.ts:26-78` dispatches the public CLI into profile, plugin, and config-dump modes.
- E1 source verified: `apps/cli/src/plugin.ts:16-107` applies exact-version exemptions, profile locking, and plugin command execution.
- E1 source verified: `packages/session/session-persistence-jsonl/src/index.ts:239-280` registers the JSONL backend and makes session materialization lazy.
- E1 source verified: `packages/session/session-persistence-jsonl/src/storage.ts:79-315` keeps one active write chain per handle, preserves monotonic reads, batches live events, and closes by draining before release.
- E2 test verified: `apps/cli/tests/profiles/headless/tests/semantic-checkpoint.expected.e2e.ts:39-140` seeds an interrupted session and verifies the resumed semantic checkpoint output.
- E2 test verified: `packages/session/session-persistence-jsonl/tests/lease.two-process.e2e.ts:33-69` proves a live writer blocks a second process until SIGKILL releases the kernel lock.

## Architecture

Principal components:

- CLI entrypoint and mode dispatcher.
- Plugin command handler with profile-scoped exact-version approvals.
- JSONL session persistence backend.
- Per-handle mutation chain and live write buffer.
- Replay fixture and two-process lock contention tests.

Most interesting mechanism: the runtime keeps its CLI, approval gate, and session persistence tied together so recovery is not an afterthought. The session handle is the durable boundary, not a loose transcript, and the tests exercise both replay and write-lock takeover.

Baseline comparison: a conventional agent harness often treats the CLI, plugin installation, and session state as separate concerns and reconstructs state from transcripts later. This implementation keeps a durable session store, exact-version approvals, and replay fixtures in one recoverable path.

## Reuse Guidance

Reusable:

- Model the harness as a replay-safe CLI boundary with explicit command dispatch.
- Keep plugin approvals exact-version scoped instead of broad allowlists.
- Use a single write chain per session handle and require monotonic read behavior.
- Add replay fixtures that prove interrupted semantic checkpoints resume to the expected output.

Do not copy:

- Do not copy the exact profile-specific command surface as a generic product API.
- Do not assume JSONL plus kernel locking is the right durability layer for every workload.
- Do not treat the replay fixture as sufficient without a live restart or process-kill test on the same session flow.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The CLI, plugin manager, and persistence backend are all explicit source modules.
- Session locking is exercised across two real processes, not just in-memory mocks.
- The replay fixture validates resumed semantic output rather than only low-level file shape.

Experimental or incomplete for our needs:

- The repository still reads as a harness/runtime rather than a hardened service.
- The review did not validate a real process-kill and restart cycle on the same semantic checkpoint path.
- The replay discipline still depends on filesystem durability and exact-version plugin policy.

Hidden costs and failure modes:

- File-based replay can hide corruption if malformed lines are skipped too quietly.
- Exact-version approval reduces drift but adds operational friction when a package is intentionally upgraded.
- Lock takeover is kernel-dependent, so portability still depends on the host filesystem and process model.

Adoption experiment:

Run a live profile session, kill the process after a side-effecting turn, restart the same profile, and confirm the replayed checkpoint matches the fixture without reissuing the side effect or duplicating the tool call.

## Candidate Patterns

- `replay-safe session harness`
- `exact-version plugin approval`
- `single-writer JSONL session store`
