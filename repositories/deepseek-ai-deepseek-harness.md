# deepseek-ai/deepseek-harness

- Repository: https://github.com/deepseek-ai/deepseek-harness
- Review date: 2026-10-10
- Current commit reviewed: `d743267388641bc76f17c45ce8b4c231aed1d32c`
- Commit date: 2026-10-09T17:31:32+08:00
- Branch: `master`
- Previous commit reviewed: `5badb15009ae1756c3afe0ae0cef1faafc290ccc`
- Material changes since previous review: The earlier review covered CLI/plugin approvals and JSONL replay; this review examines the synchronous SDK, notification routing, and bundled-runtime lifecycle.
- Decision: track

## Problem Fit

This repository informs `ai-llm-systems`, especially long-running agent sessions, tool-use orchestration, runtime packaging, and traceable turn completion. The reusable mechanism is a synchronous Python SDK around a stateful session runtime, not the DeepSeek UI or model branding.

## Verified Flow

`DeepSeekHarness.start()` launches the runtime subprocess through `HarnessClient.start()` -> `HarnessClient.initialize()` sends a JSON-RPC initialize request with cwd/provider/model settings -> `Session.run()` normalizes the input, subscribes to the session subtree of runtime notifications, and sends `session/prompt` -> the client waits for the `agent/inbox/spliced` receipt, then collects `session.event` notifications until `session.status == idle` -> `final_response()` and `finish_reason()` project the session event stream into a stable return value.

- E1 source verified: `python/sdk/src/deepseek_harness/api.py:13-131,149-258` implements the public SDK facade, session wrapper, event projection, and finish-reason extraction.
- E1 source verified: `python/sdk/src/deepseek_harness/client.py:39-189,239-320` implements the subprocess-owned JSON-RPC transport, notification routing, runtime diagnostics, and bundled-runtime launch resolution.
- E1 source verified: `python/sdk/src/deepseek_harness/office.py:24-219` implements the subprocess-backed Office conversion/rendering adapter with explicit CLI/result parsing and cleanup semantics.
- E2 test verified: `python/sdk/tests/test_client.py:16-219` exercises the fake runtime session flow, auto-review error projection, environment propagation, and notification capture.
- E2 test verified: `python/sdk/tests/test_bundled_runtime.py:48-106` covers bundled-runtime boot, profile patch application, and plugin-load failure surfacing.
- E2 test verified: `python/sdk/tests/test_office.py:1-152` and `python/sdk/tests/test_office_interrupts.py:1-110` cover Office argv translation, JSON output parsing, CLI error reporting, and process-tree interruption handling.

## Architecture

Principal components:

- `DeepSeekHarness` as the synchronous SDK facade.
- `HarnessClient` as the JSON-RPC subprocess transport and notification router.
- `deepseek_harness_runtime` launch resolution for bundled exe/node carriers.
- `office.py` as a separate subprocess adapter for local document operations.
- Tests that pin runtime launch, session replay, and subprocess cleanup.

Most interesting mechanism: the SDK turns a streaming runtime into a blocking session API without hiding the event stream. The session tree subscription and the inbox-receipt gate make `run()` behave deterministically while still preserving intermediate runtime events.

Baseline comparison: a simpler wrapper would launch a CLI and wait for stdout once. This SDK preserves session identity, notification ordering, runtime diagnostics, and structured turn completion.

## Reuse Guidance

Reusable:

- Treat the agent runtime as a long-lived subprocess with explicit start/stop ownership.
- Normalize session completion from event streams instead of raw stdout.
- Keep bundled-runtime resolution separate from the SDK facade.
- Surface runtime diagnostics when initialize or shutdown fails.

Do not copy:

- Do not copy the developer-preview packaging assumptions as an adoption default.
- Do not assume the bundled runtime will exist on every host.
- Do not collapse the notification tree back into a single blocking request/response call.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The SDK has a clear facade/transport split.
- Notification routing is explicit and session-scoped.
- Bundled-runtime launch failure and plugin failure are test-covered.
- Office subprocess handling already models cleanup and interrupts separately from the main session runtime.

Experimental or incomplete for our needs:

- The repository explicitly calls itself developer preview and warns about compatibility-breaking changes.
- The review did not run a real packaged end-to-end turn on the actual runtime binary.
- The runtime and Office carriers still depend on local launch artifacts being present.

Hidden costs and failure modes:

- `DSH_HOME` is mandatory and the SDK refuses to guess a hidden default.
- The runtime/client split increases the number of failure surfaces for launch, initialize, and shutdown.
- Session completion depends on stable runtime event sequencing.

Adoption experiment:

Run one real packaged session against the bundled runtime, confirm `initialize` and `session/prompt` complete, then verify the returned final response and finish reason still match the projected notification stream.

## Candidate Patterns

- `session-normalized synchronous harness`
- `bundled runtime resolution guardrail`
- `notification-tree subscription`
- `bounded subprocess shutdown`

## Previous Review

The earlier review covered CLI/plugin approvals and JSONL replay; this review examines the synchronous SDK, notification routing, and bundled-runtime lifecycle.

Earlier evidence remains pinned to `5badb15009ae1756c3afe0ae0cef1faafc290ccc` in the [report for 2026-10-04](../reports/2026-10-04.md) and the [previous card](https://github.com/mrAndreyIsachenko/architecture-radar/blob/591083a2bcc57b16fc2596c8fd2d78759c4c4f7a/repositories/deepseek-ai-deepseek-harness.md). Its open validation experiments remain in the backlog; this source review does not mark them completed.
