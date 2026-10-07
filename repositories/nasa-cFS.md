# nasa/cFS

- Repository: https://github.com/nasa/cFS
- Review date: 2026-10-07
- Current commit reviewed: `13ebc15286ec7f56cc9ac2a6b313a4aaeda16f9b`
- Commit date: 2026-10-06T21:52:54Z
- Branch: `dev`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `satellites-space-systems`, especially command/telemetry loops, housekeeping, scheduler integration, and ground-system behavior in a bundled flight-software stack. The reusable mechanism is the bundle-level command/telemetry architecture, not the demo framing.

## Verified Flow

`SC_AppMain` initializes, enters the run loop, waits on the software bus, and dispatches each message through `SC_ProcessRequest` -> `TO_LAB_AppMain` waits for startup sync, forwards telemetry, processes commands, and manages subscription tables -> `HK_AppMain` receives command messages, handles housekeeping work on timeout, and routes messages through the housekeeping pipe -> the submodule unit tests exercise the command and telemetry handlers directly, while the README describes the build/execute/send-telemetry bundle behavior.

- E1 source verified: `apps/sc/fsw/src/sc_app.c::SC_AppMain` uses the cFE run loop, receives SB buffers, and calls `SC_ProcessRequest`.
- E1 source verified: `apps/to_lab/fsw/src/to_lab_app.c::TO_LAB_AppMain`, `TO_LAB_forward_telemetry`, `TO_LAB_process_commands`, and `TO_LAB_ManageTables` implement telemetry forwarding and subscription-table management.
- E1 source verified: `apps/hk/fsw/src/hk_app.c::HK_AppMain` receives SB messages and runs housekeeping work on timeout.
- E2 test verified: `apps/sc/unit-test/sc_rtsrq_tests.c` exercises RTS start and group-start command behavior.
- E2 test verified: `apps/hk/unit-test/hk_cmds_tests.c` exercises combined-packet, HK, noop, and reset-counter commands.
- E3 maintainer stated: `README.md` says the bundle can build, execute, send commands, receive telemetry, and run unit tests, but is not a fully verified flight distribution.

## Architecture

Principal components:

- Stored-command scheduler app with SB message dispatch.
- Telemetry-output lab app with subscription-table management and telemetry forwarding.
- Housekeeping app with command processing and timeout-driven maintenance.
- Unit-test submodules for command and housekeeping behavior.

Most interesting mechanism: the bundle treats command and telemetry as explicit app loops wired through cFE services, rather than as an opaque monolith. That makes the ground-system path visible enough to reason about in source.

Baseline comparison: a simpler demo bundle would only show a static startup script or sample telemetry. cFS exposes the command/telemetry and housekeeping loops as first-class source paths.

## Reuse Guidance

Reusable:

- Keep command dispatch and telemetry forwarding in distinct loops.
- Treat subscription tables and table management as explicit runtime state.
- Separate housekeeping timeout work from nominal message handling.
- Use unit tests at the app boundary, not only at the framework boundary.

Do not copy:

- Do not copy the demo bundle as a flight-ready distribution.
- Do not assume the open bundle is operationally verified for your mission.
- Do not couple application logic directly to the ground-system examples without mission-specific adaptation.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The command/telemetry path is source-backed and unit-tested.
- The bundle has explicit app boundaries for scheduler, telemetry, and housekeeping.
- The README is honest about what the bundle is and is not.

Experimental or incomplete for our needs:

- The repository is explicitly not fully verified as an operational system.
- The demo bundle is broader than a narrowly scoped mission product.
- The validation surface is good for architecture inspection but not enough for mission adoption by itself.

Hidden costs and failure modes:

- Subscription-table drift can suppress telemetry or create brittle startup behavior.
- The demo bundle can give a false sense of readiness if its nominal path is mistaken for mission qualification.
- Cross-app coordination remains a coupling point that needs integration testing.

Adoption experiment:

Run the bundle through a full operational harness with a real or emulated ground system, then confirm the command path, housekeeping loop, and telemetry forwarding stay coherent under startup and runtime churn.

## Candidate Patterns

- `bundle-level command/telemetry loop`
- `table-driven telemetry subscription management`
