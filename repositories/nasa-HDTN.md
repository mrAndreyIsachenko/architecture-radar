# nasa/HDTN

- Repository: https://github.com/nasa/HDTN
- Review date: 2026-09-22
- Current commit reviewed: `7fbe90cdbe3c8c737efaacb5985f881f95fc7d2a`
- Commit date: 2026-02-25T12:34:23-05:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `satellites-space-systems`, especially delayed-connectivity command/telemetry loops, contact-plan-driven routing, and bundle storage/replay. The reusable mechanism is the route-and-storage control plane for disruption-tolerant delivery, not the broader DTN platform branding.

## Verified Flow

`Router::Impl` initializes from the contact plan, waits for outduct telemetry, loads and filters contacts, computes routes, and emits link-state and route-update messages -> `Egress::Impl` consumes route updates and link-status changes, applies rate changes, and manages outduct callbacks -> `BundleStorageManagerBase` stores bundles in segmented disk-backed storage, restores state from disk, and tracks free space and segment chains -> `HdtnCliRunner` parses contact-plan and connection options and sends requests into a running HDTN instance -> unit tests cover CLI parsing, router behavior, and storage restore paths.

- E1 source verified: `module/router/src/router.cpp` loads contact plans, recomputes routes on link changes, and sends route and link-state updates to other modules.
- E1 source verified: `module/egress/src/EgressAsync.cpp` reacts to router events, outduct status, and send-rate changes.
- E1 source verified: `module/storage/src/BundleStorageManagerBase.cpp` manages segmented bundle storage, restore-from-disk behavior, and free-space accounting.
- E1 source verified: `module/udp_delay_sim/src/UdpDelaySimRunner.cpp` and `module/udp_delay_sim/src/UdpDelaySim.cpp` provide delayed/lossy transport simulation.
- E1 source verified: `module/cli/src/HdtnCliRunner.cpp` parses CLI options and forwards contact-plan updates and requests to a live HDTN instance.
- E2 test verified: `module/router/unit_tests/RouterTests.cpp`, `module/storage/unit_tests/BundleStorageManagerMtTests.cpp`, and `module/cli/test/TestHdtnCliRunner.cpp` exercise route, storage, and CLI behavior.

## Architecture

Principal components:

- Router that converts contact-plan and physical-link state into routes and link notifications.
- Egress module that applies route updates and transmit-rate changes.
- Disk-backed bundle storage manager with restore support.
- UDP delay simulator for lossy or delayed transport conditions.
- CLI runner for updating a live HDTN instance.

Most interesting mechanism: the router does not just hold a route table. It composes physical link state, time-based contacts, and storage availability into a route decision, then pushes link and rate updates to the other modules so the control plane stays synchronized with the current contact plan.

Baseline comparison: a simpler DTN implementation might treat route updates as mostly static configuration. HDTN instead treats contact-plan and storage state as live inputs that can force reroutes and transmission-rate changes.

## Reuse Guidance

Reusable:

- Treat contact-plan changes as live events, not just startup configuration.
- Couple routing decisions to link-state broadcasts and rate updates.
- Keep storage restore separate from route recomputation.
- Use a delay simulator or equivalent harness when validating disruption-tolerant behavior.

Do not copy:

- Do not copy the full HDTN control-plane topology unless you need the same DTN deployment model.
- Do not assume the current route logic is enough without load and restart validation.
- Do not couple application logic directly to the CLI request path.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The repo has clearly separated router, egress, storage, delay-simulation, and CLI modules.
- The source comments document the threading and event-flow model.
- The storage manager has explicit restore and accounting logic.

Experimental or incomplete for our needs:

- The review did not validate the router and storage behavior under a live contact-plan churn scenario.
- The bundle-storage path is operationally sensitive to restore and free-space pressure.
- The code base is large and protocol-heavy, so adoption should be scoped narrowly.

Hidden costs and failure modes:

- Route churn can amplify operational complexity when contacts and physical links disagree.
- Storage exhaustion can suppress otherwise valid routes.
- Delayed transports can hide timing-dependent issues that unit tests will not catch.

Adoption experiment:

Run a live contact-plan churn scenario with delayed transport, intentional storage pressure, and outduct telemetry changes, then confirm route updates, link notifications, and storage restore behavior stay coherent without stale forwarding state.

## Candidate Patterns

- `contact-plan driven route recomputation`
- `storage-gated DTN forwarding`
- `live delay-simulation transport`
- `route-update fan-out to egress`
