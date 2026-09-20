# nasa/fprime

- Repository: https://github.com/nasa/fprime
- Review date: 2026-09-19
- Current commit reviewed: `3d9c014b0bc23d2c8ba0aaa981e172d311b284c2`
- Commit date: 2026-09-17T07:51:50-07:00
- Branch: `devel`
- Previous commit reviewed: `198092c8f2f58a89e2922404bddf4b68eaaa3dbb`
- Material changes since previous review: adds CFDP transaction-management evidence and extends the packet-routing analysis; the command-dispatch, health/watchdog, and bounded router findings from the 2026-09-13 and 2026-09-16 reviews remain applicable.
- Decision: track

## Problem Fit

This repository informs `satellites-space-systems`, especially command/telemetry loops, delayed-connectivity workflows, packet routing, and file-transfer recovery. The reusable mechanism is the combination of explicit packet dispatch, context preservation, and CFDP transaction management, not the broader flight-software framework.

## Verified Flow

Incoming packet or command -> `FprimeRouter` classifies packet type and restores the originating context from its buffer table -> `CommandDispatcherImpl` resolves opcode handlers, tracks sequence/overflow state, and emits command responses -> `CfdpManager` creates and cycles the CFDP engine for file transfer requests -> tests verify command routing, file routing, unknown-packet handling, out-of-order buffer returns, and CFDP error cases.

- E1 source verified: `Svc/FprimeRouter/FprimeRouter.cpp` dispatches packet types, preserves buffer/context association in a fixed-size table, and restores context on `fileBufferReturnIn`.
- E1 source verified: `Svc/CmdDispatcher/CommandDispatcherImpl.cpp` maintains the opcode dispatch table, sequence tracking, command overflow handling, and command response routing.
- E1 source verified: `Svc/Ccsds/CfdpManager/CfdpManager.cpp` owns CFDP engine lifetime, file-transfer initiation, queueing of file requests, and the 1 Hz processing cycle.
- E2 test verified: `Svc/FprimeRouter/test/ut/FprimeRouterTester.cpp` covers command routing, file routing, unknown packet routing, context round-trip, multi-buffer out-of-order return, and table-full degradation.
- E2 test verified: `Svc/CmdDispatcher/test/ut/CommandDispatcherTester.cpp` covers dispatch-table behavior, response routing, and command status handling.
- E2 test verified: `Svc/Ccsds/CfdpManager/test/ut/CfdpManagerCommandTests.cpp` covers file-send success and failure paths, invalid inputs, and transaction handling.

Previously established evidence retained from the prior review:

- E1 source verified: `Svc/Health/HealthComponentImpl.cpp:72-149` implements ping return validation, warning/fatal timeout progression, telemetry updates, and watchdog strobes.
- E2 test verified: `Svc/Health/test/ut/HealthTester.cpp:140-583` covers nominal telemetry, warning/fatal timeout behavior, monitoring enable/disable, watchdog checks, and command handler behavior.

## Architecture

Principal components:

- `Svc/FprimeRouter` for packet demultiplexing and context restoration.
- `Svc/CmdDispatcher` for command table management and response accounting.
- `Svc/Health` for ping-cycle monitoring and watchdog signaling.
- `Svc/Ccsds/CfdpManager` for CFDP engine ownership and file-transfer workflow.
- Unit-test harnesses for router, dispatcher, and CFDP regression coverage.

Most interesting mechanism: `FprimeRouter` preserves packet-origin context across routing and out-of-order returns instead of treating buffers as anonymous payloads. That lets the flight-software stack reconnect response data to the right caller even when buffers come back in a different order.

Baseline comparison: a simpler flight stack would route packets by type alone and rely on implicit caller assumptions for buffer ownership. F Prime keeps a concrete context table and routes command/file/unknown packets through explicit handlers.

## Reuse Guidance

Reusable:

- Preserve buffer-to-context association across asynchronous packet routing.
- Keep command dispatch, telemetry response, and file-transfer logic separate but coordinated.
- Model health checking as an explicit ping cycle with warning, fatal, and watchdog behavior.
- Treat file-transfer engines as owned runtime components with a visible cycle.
- Test out-of-order buffer returns and table-full behavior, not just nominal dispatch.

Do not copy:

- Do not copy the whole flight-framework stack unless you need the same deployment model.
- Do not assume the context table is sufficient without resource-lifetime discipline.
- Do not treat CFDP as a general-purpose queue; it is a protocol-specific workflow.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Strong unit-test coverage for router, dispatcher, and CFDP error handling.
- Source- and test-backed health monitoring, timeout progression, and watchdog behavior.
- Explicit ownership of dispatch state and CFDP engine lifecycle.
- Clear separation between packet routing and protocol-specific handlers.

Experimental or incomplete for our needs:

- The review did not run the broader deployment or integration harness locally.
- CFDP and router behavior are operationally sensitive to queue depth and packet ordering.
- The framework is large and flight-software-specific.

Hidden costs and failure modes:

- Fixed-size context tables can degrade when traffic exceeds the table size.
- Packet context recovery requires careful buffer lifecycle discipline.
- File-transfer behavior depends on protocol timing and ground-link assumptions.

Adoption experiment:

Use the F Prime router pattern in a delayed-connectivity control plane, then force out-of-order buffer returns and a table-full condition to confirm the caller context is preserved and the system degrades cleanly.

## Candidate Patterns

- `bounded context-preserving packet router`
- `opcode-tracked command dispatcher`
- `watchdog-ping cycle monitor`
- `clear-tracking response fan-out`
- `command response dispatch table`
- `CFDP transaction manager`
