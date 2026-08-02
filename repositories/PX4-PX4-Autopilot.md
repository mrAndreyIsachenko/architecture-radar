# PX4/PX4-Autopilot

- Repository: https://github.com/PX4/PX4-Autopilot
- Review date: 2026-08-02
- Current commit reviewed: `43cccdea0e57cf92a58562d2d7a1cba0854395f7`
- Commit date: 2026-08-01T13:02:45-06:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `drones-robotics-autonomy`: mission planning, telemetry, safety envelopes, command acknowledgments, and recovery from sensor loss or flight-mode loss.

## Verified Flow

MAVLink command / mission input -> commander / health checks / mission state -> `vehicle_command_ack` result or failsafe transition -> mission or offboard logic continues or aborts -> MAVSDK tests simulate GPS, baro, and magnetometer loss while the vehicle remains in a known recovery path.

- E1 source verified: `src/modules/commander/Commander.hpp` wires in failsafe, mission, offboard, `mission_result`, `vehicle_command_ack`, and health-check subsystems.
- E1 source verified: `src/modules/commander/Commander.cpp` maps incoming `vehicle_command` messages to accepted, denied, or temporarily rejected ACKs and handles mode transitions.
- E1 source verified: `src/modules/rc_update/rc_update.cpp` handles RC function mapping and fallback behavior when parameters or calibration state change.
- E1 source verified: `test/test_mavlink_param_validation.py` rejects mission items and commands with unsupported parameter slots and accepts valid variants.
- E1 source verified: `test/mavsdk_tests/test_multicopter_failsafe.cpp` exercises mission continuation or landing after GPS, baro, and magnetometer loss.
- E2 test verified: `test/mavsdk_tests/test_multicopter_mission.cpp` exercises mission execution and RTL transitions.

## Architecture

Principal components:

- Commander and failsafe subsystems for flight-state enforcement.
- RC update and mode-management logic for operator input.
- MAVLink param-validation regression tests.
- MAVSDK integration tests for mission and sensor-failure recovery.

Most interesting mechanism: the command path is explicit about accept, deny, and temporary reject outcomes, and the safety model is validated against mission and sensor-loss scenarios instead of only nominal flight.

Baseline comparison: a simpler autopilot would accept commands opportunistically and rely on manual operator recovery. PX4 couples command acknowledgment to health, mode, and mission state so invalid or unsafe transitions are rejected early.

## Reuse Guidance

Reusable:

- Treat command ACKs as part of the safety contract, not an afterthought.
- Model sensor loss and mission continuation in tests.
- Keep mission, offboard, and RC paths separate enough to reason about failures.

Do not copy:

- Do not copy the hardware-specific complexity.
- Do not assume the commander alone is the whole autonomy stack.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Strong test coverage for mission, sensor-loss, and parameter-validation behavior.
- Explicit failsafe and health-check plumbing.
- Clear separation between mission, RC, and command handling.

Experimental or incomplete for our needs:

- The source is heavily embedded and simulation-dependent.
- The review did not run the simulator or flight tests locally.

Hidden costs and failure modes:

- The behavior depends on hardware/sensor availability and simulator fidelity.
- Command/mode semantics are distributed across several subsystems.

Adoption experiment:

Use the PX4 command-ACK model as a template for an internal autonomy agent: every high-risk transition must return accepted, denied, or temporarily rejected, and the test suite must cover sensor-loss recovery.

## Candidate Patterns

- `failsafe command acknowledgment matrix`
- `mission sensor-loss recovery`
