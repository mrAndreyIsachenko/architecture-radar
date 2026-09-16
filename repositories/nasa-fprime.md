# nasa/fprime

- Repository: https://github.com/nasa/fprime
- Review date: 2026-09-16
- Current commit reviewed: `198092c8f2f58a89e2922404bddf4b68eaaa3dbb`
- Commit date: 2026-09-15T14:09:56-07:00
- Branch: `devel`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `satellites-space-systems`, especially delayed command/telemetry loops, health monitoring, and safe recovery after operator or hardware faults. The reusable mechanism is not the flight-software branding; it is the command dispatcher plus health component that keep command acceptance, ping cadence, and watchdog signaling consistent under load.

## Verified Flow

`CommandDispatcherImpl::seqCmdBuff_handler` deserializes a command buffer, resolves the opcode in the dispatch map, allocates a sequence number, optionally inserts a pending tracker entry, forwards the command to the destination component, and emits rejection/status events when validation or routing fails -> `CMD_CLEAR_TRACKING_cmdHandler` clears outstanding pending entries while preserving its own acknowledgement path -> `HealthImpl::Run_handler` drains queued messages, pings each enabled entry, records late pings, and strobes the watchdog -> `HealthImpl::PingReturn_handler` validates the return key before resetting counters -> the `CommandDispatcherTester` and `HealthTester` unit suites exercise nominal dispatch, invalid opcode handling, queue overflow, clear-tracking behavior, ping timeout thresholds, and watchdog stroke paths.

- E1 source verified: `Svc/CmdDispatcher/CommandDispatcherImpl.cpp:104-158` implements deserialization, opcode lookup, pending-command tracking, failure responses, and invalid-opcode consumption.
- E1 source verified: `Svc/CmdDispatcher/CommandDispatcherImpl.cpp:185-229` implements clear-tracking fan-out, ping echoing, and queue-overflow accounting.
- E1 source verified: `Svc/Health/HealthComponentImpl.cpp:72-149` implements ping return validation, warning/fatal timeout progression, telemetry updates, and watchdog strobes.
- E2 test verified: `Svc/CmdDispatcher/test/ut/CommandDispatcherTester.cpp:59-91,95-360,543-841` covers command registration, nominal dispatch, invalid command rejection, failure paths, overflow handling, and clear-tracking behavior.
- E2 test verified: `Svc/Health/test/ut/HealthTester.cpp:140-583` covers nominal telemetry, warning/fatal timeout behavior, monitoring enable/disable, watchdog checks, and command handler behavior.

## Architecture

Principal components:

- Command dispatcher component with opcode routing and sequence tracking.
- Health monitor component with ping send/return logic and watchdog strobes.
- Event and telemetry surfaces that make late or invalid states observable.
- Unit-test harnesses that exercise queue, timeout, and rejection edges.

Most interesting mechanism: the dispatcher makes pending command tracking conditional on a connected status path, which keeps the fast path lean while still giving the operator a deterministic failure or clear-status path when the downstream component cannot confirm completion.

Baseline comparison: a conventional command router would forward opcodes and leave ack handling to ad hoc call sites. Fprime keeps the command lifecycle explicit, with sequence tracking, status return paths, and clear-tracking semantics in one component boundary.

## Reuse Guidance

Reusable:

- Keep command acceptance, pending-state tracking, and completion reporting in one boundary.
- Treat malformed or unroutable commands as first-class observable failures.
- Model health checking as a ping cycle with explicit warning and fatal thresholds.
- Surface watchdog strobes as part of the health loop, not a side effect hidden in operator code.

Do not copy:

- Do not copy the concrete port layout or generated FPP naming without an adapter.
- Do not assume the current in-tree command-tracker design is enough for high-rate ground links without runtime validation.
- Do not treat the unit tests as a substitute for flight-target or hardware-in-the-loop exercise.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The command path and the health path are both source-backed and test-backed.
- Invalid opcode, malformed buffer, queue overflow, warning, and fatal paths all have explicit observable behavior.
- Clear-tracking preserves the caller's own acknowledgement instead of wiping the whole response path blindly.

Experimental or incomplete for our needs:

- The repository is still shaped around generated component interfaces and target-specific deployment plumbing.
- The current evidence is source and unit tests, not a target runtime with injected fault handling.
- Recovery behavior after process restart is not yet validated against a real mission build.

Hidden costs and failure modes:

- Pending-state growth can hide liveness problems if the downstream completion path is unhealthy.
- Clear-tracking can suppress useful state if operators use it too aggressively.
- Health thresholds need target-specific tuning; warning and fatal values are not universal.

Adoption experiment:

Kill the command dispatcher mid-flight on a target or emulator build, restart it, and confirm that pending command tracking, command responses, and ping/watchdog behavior return to a consistent state without duplicate acknowledgements.

## Candidate Patterns

- `opcode-tracked command dispatcher`
- `watchdog-ping cycle monitor`
- `clear-tracking response fan-out`
