# PX4/PX4-Autopilot

- Repository: https://github.com/PX4/PX4-Autopilot
- Review date: 2026-11-15
- Current commit reviewed: `c4b8f107ae97d643fc784a394e3874f34caec563`
- Commit date: 2026-11-15T11:31:22+11:00
- Branch: `main`
- Previous commit reviewed: `07a2faab0dd4621e3b85d1818a7f6e4af63cf87f`
- Material changes since previous review: the current head keeps the commander/failsafe safety model intact while expanding the validation surface around parameter slots, ACK handling, and mission-loss tests. The new/updated Python tests make the command contract more explicit, and the MAVSDK harness now documents the retry-and-ACK path more clearly.
- Decision: track

## Problem Fit

This repository informs `drones-robotics-autonomy`: mission planning, telemetry, safety envelopes, command acknowledgments, and recovery from sensor loss or flight-mode loss. The reusable mechanism is the commander-side command-acknowledgment matrix and the safety gates that decide whether a high-risk transition should be accepted, denied, temporarily rejected, or failed. The current head broadens the validation surface for that mechanism by making unsupported parameter slots and sensor-loss recoveries explicit in the Python test layer.

## Verified Flow

MAVLink command / mission input -> `Commander::handle_command` classifies the command and assigns an ACK result -> `Commander::answer_command` publishes the ACK back to MAVLink -> `Commander::arm` / `disarm` enforce preflight, health, and failsafe gates -> `test/test_mavlink_param_validation.py` validates unsupported parameter slots at the mission/command boundary -> `test/mavsdk_tests/test_multicopter_failsafe.py` and `autopilot_tester.py` execute GPS, baro, and magnetometer-loss missions until the vehicle reaches the expected recovery state.

- E1 source verified: `src/modules/commander/Commander.hpp` wires in failsafe, mission, offboard, `mission_result`, `vehicle_command_ack`, and health-check subsystems.
- E1 source verified: `src/modules/commander/Commander.cpp:866-930,2858-2896` classifies incoming `vehicle_command` messages, assigns accepted/denied/temporarily-rejected results, and publishes the ACK.
- E1 source verified: `src/modules/commander/Commander.cpp:667-760` enforces preflight, throttle, and health checks before arming.
- E1 source verified: `src/modules/rc_update/rc_update.cpp` handles RC function mapping and fallback behavior when parameters or calibration state change.
- E2 test verified: `test/test_mavlink_param_validation.py:108-260` rejects mission items and commands with unsupported parameter slots and accepts valid variants.
- E2 test verified: `test/mavsdk_tests/test_multicopter_failsafe.py:12-70` exercises mission continuation or landing after GPS, baro, and magnetometer loss.
- E2 test verified: `test/mavsdk_tests/autopilot_tester.py:810-863` supports the integration harness that arms, runs, and degrades missions under sensor-loss injection.

## Architecture

Principal components:

- Commander state machine that owns command dispatch, mode transitions, arming, and failsafe coordination.
- Health and arming checks that gate high-risk transitions.
- Mission and command validation harnesses that pin the ACK matrix against the MAVLink parameter contract.
- MAVSDK integration tests that simulate sensor loss and mission continuation.

Most interesting mechanism: the command path is explicit about accept, deny, temporary reject, unsupported, and failed outcomes, and the safety model is validated against mission and sensor-loss scenarios instead of only nominal flight.

Baseline comparison: a simpler autopilot would accept commands opportunistically and rely on manual operator recovery. PX4 couples command acknowledgment to health, mode, and mission state so invalid or unsafe transitions are rejected early.

## Reuse Guidance

Reusable:

- Treat command ACKs as part of the safety contract, not an afterthought.
- Keep mission and command parameter validation aligned with the actual MAVLink result codes, not with a generic success/failure bit.
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
- Some command and mission semantics still depend on simulator fidelity and vehicle configuration, so a source-only review cannot prove the whole recovery envelope.

Hidden costs and failure modes:

- The behavior depends on hardware/sensor availability and simulator fidelity.
- Command/mode semantics are distributed across several subsystems.
- ACK semantics and mission validation can change in subtle ways when new command cases are added, so regressions need explicit coverage.

Adoption experiment:

Use the PX4 command-ACK model as a template for an internal autonomy agent: every high-risk transition must return accepted, denied, temporarily rejected, unsupported, or failed, and the test suite must cover sensor-loss recovery and parameter validation.

## Candidate Patterns

- `failsafe command acknowledgment matrix`
- `mission sensor-loss recovery`
- `parameter-slot mission validation gate`

## Previous Reviews

The [2026-10-13 report](../reports/2026-10-13.md) examined the same commander/failsafe contract at the previous commit. The [previous card](https://github.com/mrAndreyIsachenko/architecture-radar/blob/d1fe321f3a0a08355405865a6407c86a683ed560/repositories/PX4-PX4-Autopilot.md) preserves those source references. The current head broadens the validation surface but does not replace the need for live SITL validation.
