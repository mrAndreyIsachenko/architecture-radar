# deepseek-ai/deepseek-harness

- Repository: https://github.com/deepseek-ai/deepseek-harness
- Review date: 2026-11-27
- Current commit reviewed: `4b399c39a6d1479cd84ca591b4d7c88e24d38a96`
- Commit date: 2026-11-22T16:50:28+08:00
- Branch: `master`
- Previous commit reviewed: `d743267388641bc76f17c45ce8b4c231aed1d32c`
- Material changes since previous review: current head merges `worktree-release-dsh-0.2.3-alpha.2` and refreshes the bounded shutdown and profile-boot surface while keeping the same durable session contract.
- Decision: selected

## Problem Fit

This repository informs `ai-llm-systems`, especially long-running agent sessions, shutdown safety, replay-safe harness behavior, and profile composition for launcher surfaces. The reusable mechanism is the bounded shutdown and profile boot envelope, not the DeepSeek branding.

## Verified Flow

`prepareProfile()` composes the boot profile from bundle patches, user overlays, telemetry settings, and shutdown options -> `composeProfile()` passes the shutdown budget into the runtime surface -> `createProcessShutdown()` creates one pending shutdown promise, arms a forced-exit timeout, and coalesces interrupts into a single exit path -> `apps/cli/tests/process-shutdown.spec.ts` verifies normal completion, forced exit, and repeated interrupt escalation -> `apps/cli/tests/web-agent-shutdown.e2e.ts` verifies cleanup across the web-agent shutdown path.

- E1 source verified: `apps/cli/src/profile-boot.ts` composes the runtime profile, overlays, telemetry switch, and bounded shutdown options.
- E1 source verified: `apps/cli/src/process-shutdown.ts` implements the single pending shutdown promise, forced-exit timeout, and repeated-interrupt escalation path.
- E2 test verified: `apps/cli/tests/process-shutdown.spec.ts` verifies normal completion, timeout forcing, and interrupt escalation behavior.
- E2 test verified: `apps/cli/tests/web-agent-shutdown.e2e.ts` verifies cleanup behavior through the web-agent shutdown path.

## Architecture

Principal components:

- Profile boot layer that merges bundle patches, user overlays, and telemetry configuration.
- Process-shutdown coordinator that bounds shutdown duration and escalates repeated interrupts.
- CLI and web-agent tests that pin the runtime shutdown contract.

Most interesting mechanism: the runtime does not rely on an unbounded exit path. It turns shutdown into a bounded, single-owner promise with a forced-exit deadline, which keeps the launcher from hanging indefinitely when the surrounding session is already unstable.

Baseline comparison: a conventional CLI launcher would let each shutdown path race on its own and hope the process exits cleanly. This repository centralizes the shutdown envelope so the runtime can coalesce interrupts and force an exit when needed.

## Reuse Guidance

Reusable:

- Use a single shutdown promise and a bounded timeout for CLI or agent runtimes.
- Compose runtime profile boot from explicit patches and overlays instead of scattering setup logic.
- Test both normal completion and forced exit.

Do not copy:

- Do not copy the product-specific plugin surface without the same launcher semantics.
- Do not assume a forced exit is a substitute for recovery; it is only the safety backstop.
- Do not treat the tests as proof of live process-kill recovery on real workloads.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Shutdown behavior is explicit and test-covered.
- Profile boot is factored into reusable composition helpers.
- The current head preserves the same contract while refreshing the release branch.

Experimental or incomplete for our needs:

- The repository still needs live process-kill and restart validation on the same session ledger.
- The strongest evidence is shutdown choreography, not a full production workload run.
- External side effects are only bounded by the timeout; they are not inherently idempotent.

Hidden costs and failure modes:

- Forced exit can hide lingering side effects if the upstream runtime does not flush cleanly.
- Coalesced interrupts can mask the root cause if operators only watch the final exit code.
- Profile boot composition can accumulate coupling if overlays become too implicit.

Adoption experiment:

Run one real packaged session through startup, request dispatch, and shutdown, then kill and restart the process mid-flight to confirm the shutdown envelope does not duplicate side effects or lose the profile state needed to replay the session safely.

## Candidate Patterns

- `bounded subprocess shutdown`
- `profile composition guardrail`
- `single-owner shutdown promise`

## Previous Review

The earlier review focused on the semantic checkpoint and durable session-storage surface. This review pins the current head at `4b399c39a6d1479cd84ca591b4d7c88e24d38a96` and shifts the emphasis to the bounded shutdown and profile boot mechanism while the same runtime gap remains open.
