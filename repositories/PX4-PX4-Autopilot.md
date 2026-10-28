# PX4/PX4-Autopilot

- Repository: https://github.com/PX4/PX4-Autopilot
- Review date: 2026-10-28
- Current commit reviewed: `87c833ddd1046bece995628d8304ca7887e673b3`
- Commit date: 2026-10-28T11:49:07+01:00
- Branch: `main`
- Previous commit reviewed: `07a2faab0dd4621e3b85d1818a7f6e4af63cf87f`
- Material changes since previous review: the current head keeps the commander/failsafe safety model intact while expanding EKF/gen-nav validation and MAVSDK mission-failure coverage, including the new Gen Nav estimator test path.
- Decision: track

## Problem Fit

This repository informs `drones-robotics-autonomy`: mission planning, telemetry, safety envelopes, command acknowledgments, and recovery from sensor loss or flight-mode loss. The reusable mechanism is the commander-side command-acknowledgment matrix and the safety gates that decide whether a high-risk transition should be accepted, denied, temporarily rejected, unsupported, or failed.

## Verified Flow

MAVLink command / mission input -> `Commander::handle_command()` classifies the command and chooses an ACK result -> `Commander::answer_command()` publishes the ACK back to MAVLink -> `Commander::arm()` / `disarm()` enforce preflight, health, and failsafe gates -> `FailsafeTest` pins the policy around lost-control, mission, wind, and offboard transitions -> `EscChecksTest` verifies stale or undercurrent ESC reports block arming and latch motor-failure state -> `test_multicopter_failsafe.py` drives mission execution while injecting GPS or magnetometer failures through `AutopilotTester`.

- E1 source verified: `src/modules/commander/Commander.cpp:865-1779,2850` classifies incoming `vehicle_command` messages, assigns ACK results, and publishes the reply.
- E1 source verified: `src/modules/commander/HealthAndArmingChecks/escChecksTest.cpp:162-252` verifies offline ESCs, arming-timeout behavior, undercurrent latching, and reversible-motor handling.
- E2 test verified: `src/modules/commander/failsafe/failsafe_test.cpp:1-220` exercises the policy matrix for manual-control loss, GCS loss, mission failure, wind limits, and user takeover.
- E2 test verified: `test/mavsdk_tests/test_multicopter_failsafe.py:27-48` injects GPS and magnetometer failures during a mission and checks the recovery behavior.
- E2 test verified: `test/mavsdk_tests/autopilot_tester.py:1-220` provides the MAVSDK integration harness that arms, starts missions, injects failures, and waits for mission completion or disarm.
- E2 test verified: `src/modules/ekf2/test/test_EKF_gen_nav.cpp` extends the current head's estimator validation surface with Gen Nav flight-condition coverage.

## Architecture

Principal components:

- Commander state machine that owns command dispatch, mode transitions, arming, and failsafe coordination.
- Health and arming checks that gate high-risk transitions.
- Failsafe policy tests that pin the response matrix for mission, control-loss, and wind conditions.
- MAVSDK integration tests and helpers that simulate sensor loss and mission continuation.
- Estimator tests that expand flight-condition coverage for the current head.

Most interesting mechanism: the command path is explicit about accept, deny, temporary reject, unsupported, and failed outcomes, and the safety model is validated against mission and sensor-loss scenarios instead of only nominal flight. That makes the ACK matrix itself a reusable safety contract.

Baseline comparison: a simpler autopilot would accept commands opportunistically and rely on manual recovery. PX4 couples command acknowledgment to health, mode, and mission state so invalid or unsafe transitions are rejected early and consistently.

## Reuse Guidance

Reusable:

- Treat command ACKs as part of the safety contract, not an afterthought.
- Keep mission and command parameter validation aligned with the actual MAVLink result codes.
- Model sensor loss and mission continuation in tests.
- Keep mission, offboard, and RC paths separate enough to reason about failures.

Do not copy:

- Do not copy the hardware-specific complexity.
- Do not assume the commander alone is the whole autonomy stack.
- Do not treat simulator-only validation as a substitute for flight or SITL evidence.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Strong test coverage for mission, sensor-loss, and parameter-validation behavior.
- Explicit failsafe and health-check plumbing.
- Clear separation between mission, RC, and command handling.
- The current head expands the validation surface without changing the safety contract.

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

 The [2026-10-13 report](../reports/2026-10-13.md) examined the explicit command-acknowledgment matrix and mission/sensor-loss validation surface at `07a2faab0dd4621e3b85d1818a7f6e4af63cf87f`. The [2026-10-10 report](../reports/2026-10-10.md) examined the earlier commander refresh at `fe24ec2280b62f50fe6b8e206a41a5d1687786fe`. The live SITL experiment remains in the backlog; this review does not mark it completed.
