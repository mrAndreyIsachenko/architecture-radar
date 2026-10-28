# deepseek-ai/deepseek-harness

- Repository: https://github.com/deepseek-ai/deepseek-harness
- Review date: 2026-10-28
- Current commit reviewed: `f3803c96974ad4a94195fb97e5c637e9c2a3afe3`
- Commit date: 2026-10-28T02:17:58+08:00
- Branch: `master`
- Previous commit reviewed: `d743267388641bc76f17c45ce8b4c231aed1d32c`
- Material changes since previous review: the current release head refreshes CLI/profile boot composition, exact-version plugin approval, and headless semantic-checkpoint fixtures while leaving the same durable session ledger and checkpoint barrier in place.
- Decision: track

## Problem Fit

This repository informs `ai-llm-systems`, especially durable agent workflows, tool-use recovery, and checkpointed execution around model dispatch and profile composition. The reusable mechanism is the semantic checkpoint barrier plus layered profile boot: the launcher assembles a profile tree from durable patches, and dispatch remains gated on persistence success instead of optimistic follow-up flushes.

## Verified Flow

Profile invocation -> `prepareProfile()` composes the profile tree and rewrites the empty root config -> `createAppReady()` delays readiness until boot and host setup succeed -> `runPlugin()` accepts only exact-version exemption commands before normal package operations -> `semantic-checkpoint.expected.e2e.ts` seeds an interrupted JSONL session and replays the unknown tool outcome through the headless stream-json app -> `checkpoints.expected.e2e.ts` turns checkpoint storage failure into a failed dispatch instead of a best-effort model request.

- E1 source verified: `apps/cli/src/profile-boot.ts:44,108,194-195,230,295` defines readiness gating, profile replacement, composed profile loading, and the boot path that only commits readiness after setup succeeds.
- E1 source verified: `apps/cli/src/plugin.ts:2,71-98` implements exact-version plugin approval and version-exemption handling around profile package operations.
- E2 test verified: `apps/cli/tests/profiles/headless/tests/semantic-checkpoint.expected.e2e.ts:103-138` seeds an interrupted session and verifies replay of the unknown tool outcome through the headless app.
- E2 test verified: `apps/cli/tests/profiles/sdk/checkpoints.expected.e2e.ts:15-46` proves checkpoint storage failure suppresses model dispatch unless the policy is explicitly disabled.

## Architecture

Principal components:

- Layered profile boot that composes shipped bundles, profile-local patches, user overlays, and launch overlays.
- Launcher-owned readiness signal that only commits after the boot sequence and host setup finish.
- Plugin approval flow with explicit, exact-version compatibility exemptions.
- Semantic-checkpoint fixtures that preserve interrupted session history across replay.

Most interesting mechanism: profile assembly is treated as a durable composition problem, not a one-shot config read. The boot path writes a real root config, layers patches in a fixed order, and only becomes ready after the composed profile and process setup are complete. That same durability boundary is then exercised by the checkpoint tests.

Baseline comparison: a simpler launcher would read one config file and start dispatch immediately. DeepSeek Harness instead composes explicit layers, tracks launch readiness separately, and makes checkpoint failure a hard stop rather than a warning.

## Reuse Guidance

Reusable:

- Compose launch configuration from immutable layers rather than patching one mutable blob.
- Gate runtime readiness on successful boot and host setup.
- Keep plugin compatibility approvals exact to a package and runtime version.
- Make checkpoint failure suppress dispatch instead of deferring failure handling to later code.

Do not copy:

- Do not copy the profile replacement flow without the same filesystem and rename semantics.
- Do not assume the JSONL session layout is portable outside this runtime contract.
- Do not treat semantic checkpoint replay as enough by itself; side-effecting paths still need idempotency and restart validation.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Boot completion is explicit and separated from the underlying host setup.
- Exact-version plugin approvals make compatibility risk visible and narrow in scope.
- Replay fixtures and checkpoint-failure tests pin the intended behavior instead of relying on manual inspection.

Experimental or incomplete for our needs:

- The review still does not exercise a live packaged session against the bundled runtime on this host.
- The restart path still needs a real process-kill proof on the same session ledger.
- Current head is a release sweep, so the value is in refreshed boot/replay surfaces rather than a new checkpoint algorithm.

Hidden costs and failure modes:

- Layered boot adds launch-time complexity and can surface filesystem edge cases during profile replacement.
- Flush-before-dispatch adds latency and backend pressure.
- A replayable checkpoint only helps if every side effect routes through the same persistence boundary.

Adoption experiment:

Kill the runtime after a request prefix or top-level tool call has been flushed, restart the same session ledger, and confirm that the same request prefix, sandbox mode, and tool intent reappear without duplicate side effects.

## Candidate Patterns

- `profile-layered boot composition`
- `exact-version plugin approval gate`
- `headless semantic-checkpoint recovery`

## Previous Reviews

The [2026-10-13 report](../reports/2026-10-13.md) examined checkpoint-before-dispatch and sandbox-mode replay at `d743267388641bc76f17c45ce8b4c231aed1d32c`. The [2026-10-10 report](../reports/2026-10-10.md) examined the synchronous SDK and bundled-runtime lifecycle. The [previous card](https://github.com/mrAndreyIsachenko/architecture-radar/blob/d1fe321f3a0a08355405865a6407c86a683ed560/repositories/deepseek-ai-deepseek-harness.md) preserves those source references. The live restart experiment remains in the backlog; this review does not mark it completed.
