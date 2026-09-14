# nasa/fprime

- Repository: https://github.com/nasa/fprime
- Review date: 2026-09-13
- Current commit reviewed: `4dee010c3002bce6a66f1372b89e1fed47289c57`
- Commit date: 2026-09-11T20:22:07-07:00
- Branch: `devel`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: selected

## Problem Fit

This repository informs `satellites-space-systems`: delayed-connectivity uplink routing, command/file packet handling, and bounded context recovery for command and telemetry loops.

## Verified Flow

Received F Prime packet -> `FprimeRouter::dataIn_handler()` inspects APID packet type -> command packets are copied into `Fw::ComBuffer` and sent immediately to `commandOut` -> file and unknown packets are handed off without copying, with buffer-to-context state stored in a fixed table -> `fileBufferReturnIn_handler()` restores the original context before returning ownership upstream -> unit tests cover routing, round-trip context restoration, out-of-order return, and table-full degradation.

- E1 source verified: `Svc/FprimeRouter/FprimeRouter.cpp::dataIn_handler` routes command, file, and unknown packets based on `context.get_apid()`.
- E1 source verified: `Svc/FprimeRouter/FprimeRouter.cpp::insertContext` and `takeContext` maintain a fixed-size buffer-to-context table keyed by the buffer data pointer.
- E1 source verified: `Svc/FprimeRouter/FprimeRouter.cpp::fileBufferReturnIn_handler` restores saved context before returning ownership to the deframer.
- E2 test verified: `Svc/FprimeRouter/test/ut/FprimeRouterTester.cpp::testRouteComInterface`, `testRouteFileInterface`, and `testRouteUnknownPacket` verify the three routing branches.
- E2 test verified: `Svc/FprimeRouter/test/ut/FprimeRouterTester.cpp::testFileContextRoundTrip` and `testMultiBufferContextRoundTrip` verify context preservation, including out-of-order returns.
- E2 test verified: `Svc/FprimeRouter/test/ut/FprimeRouterTester.cpp::testContextTableFull` verifies graceful degradation when the table overflows.
- E3 maintainer stated: `Svc/FprimeRouter/docs/sdd.md` documents guarded input serialization, fixed-size table behavior, and warning/degrade semantics.

## Architecture

Principal components:

- `Svc::FprimeRouter` packet router component.
- Fixed-size buffer/context association table.
- GTest-based component harness and execution tests.
- File packet schema used by the router as a delayed-return payload.

Most interesting mechanism: the router preserves context across a non-copying hand-off by remembering the buffer pointer at send time and restoring the original `FrameContext` when the same buffer comes back. That is a small but useful pattern for command/file uplinks that need ownership transfer without losing route provenance.

Baseline comparison: a simpler packet switch would either copy everything or drop context on asynchronous return. F Prime instead keeps the router stateless from a payload perspective while retaining a bounded, explicit return map.

## Reuse Guidance

Reusable:

- Keep command packets on a fast copy-and-return path.
- Track context separately for buffers that leave the router and later return.
- Fail safe by degrading to warnings and empty context when the return table overflows.

Do not copy:

- Do not depend on the buffer pointer trick unless the same buffer identity is guaranteed on return.
- Do not expand the table without validating the uplink pool size and the maximum outstanding return set.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The component is small, explicit, and well covered by unit tests.
- The docs state the routing contract and the bounded context table behavior.
- Overflow and missing-buffer paths degrade instead of misrouting data.

Experimental or incomplete for our needs:

- The review did not validate the mechanism under flight-like concurrency or real mission traffic.
- The table capacity remains a configuration trade-off that must be sized correctly for the packet pool.

Hidden costs and failure modes:

- If a downstream consumer returns a different buffer object, context restoration will miss.
- If the table is undersized, the router degrades to empty context on overflow.
- The delayed-return model adds state that must be serialized by guarded ports.

Adoption experiment:

Run the router in a realistic uplink stack with concurrent file and unknown packets, then verify context survives return ordering and table overflow only produces warning degradation, not misrouted ownership.

## Candidate Patterns

- `bounded context-preserving packet router`

