# ArduPilot/ardupilot

- Repository: https://github.com/ArduPilot/ardupilot
- Review date: 2026-10-22
- Current commit reviewed: `3d24375e579203b8af27605df841dc1022f0e9e1`
- Commit date: 2026-10-22T13:53:23+11:00
- Branch: `master`
- Previous commit reviewed: `acef45eb0f0145943a9c2ba341d3825b8af34472`
- Material changes since previous review: expands rover autotest coverage with LOITER_TURNS circle-direction and AMSL altitude checks, broadens shared circle helpers, and keeps the copter failsafe/RTL ladder intact.
- Decision: track

## Problem Fit

This repository informs `drones-robotics-autonomy`: mission failsafes, RTL fallback, telemetry/status reporting, circle-direction validation, and SITL-backed recovery verification. The reusable mechanism is the combination of explicit safety state machines and shared autotest helpers that prove both recovery ladder behavior and mission geometry assertions.

## Verified Flow

Main-loop stall or RC/GPS loss -> `failsafe_check()` detects stalled scheduler ticks and enters failsafe after a bounded timeout -> motors are reduced to minimum and then disarmed repeatedly until recovery -> `ModeRTL` transitions through explicit stages for return-to-launch and falls back to landing when terrain or position assumptions fail -> Rover mission upload -> `PositionTargetGlobalIntAltFrame()` uses `MAV_CMD_NAV_LOITER_TURNS` to enter circle mode and verifies `POSITION_TARGET_GLOBAL_INT.alt` in AMSL -> `wait_circling_point_with_radius()` and `wait_circle_direction()` assert that the vehicle stays on the circle and travels in the requested direction -> `test_gcs_failsafe()` exercises telemetry loss, RTL recovery, mission continuation, and timeout behavior.

- E1 source verified: `ArduCopter/failsafe.cpp:1-72` detects a 2-second main-loop lockup, reduces motor output, logs the failure, and then disarms every second while the failsafe remains active.
- E1 source verified: `ArduCopter/mode_rtl.cpp:80-226,245-260` implements staged RTL setup, terrain-aware fallback, and explicit stage transitions through return, hold, descent, and land.
- E1 source verified: `Tools/autotest/rover.py:5919-5955` triggers Rover circle mode with `MAV_CMD_NAV_LOITER_TURNS` and checks that `POSITION_TARGET_GLOBAL_INT.alt` is AMSL-correct.
- E1 source verified: `Tools/autotest/rover.py:1986-2074` drives GCS-failsafe disabled, enabled, recovery, mission continuation, and timeout cases.
- E1 source verified: `Tools/autotest/vehicle_test_suite.py:19533-19625` provides reusable helpers for radius and circle-direction assertions.
- E2 test verified: `Tools/autotest/rover.py:5919-5955` pins the AMSL altitude expectation for Rover circle mode.
- E2 test verified: `Tools/autotest/rover.py:1986-2074` pins GCS-failsafe recovery and mission continuation behavior.
- E2 test verified: `Tools/autotest/vehicle_test_suite.py:19585-19625` pins the helper behavior that raises on wrong circle direction.

## Architecture

Principal components:

- Copter failsafe monitor in the 1 kHz timer path.
- RTL flight-mode state machine with terrain-aware fallback.
- Rover mission harness that exercises circle submodes and altitude frames.
- Shared autotest helpers for radius and direction assertions.
- MAVLink/GCS failsafe tests that pin behavior under telemetry loss and recovery.

Most interesting mechanism: the repository does not trust a nominal waypoint or a single recovery branch. It explicitly checks rover circle direction, altitude frame semantics, and GCS-failsafe recovery while the copter-side state machine keeps the emergency ladder staged rather than collapsing everything into a single land command.

Baseline comparison: a simpler autopilot would expose one generic failsafe action and treat mission success as a binary outcome. ArduPilot keeps the failure ladder and the mission geometry checks separate so recovery behavior remains explicit and testable.

## Reuse Guidance

Reusable:

- Keep watchdog/failsafe logic separate from the mission-mode state machine.
- Use shared autotest helpers for geometry assertions, not one-off checks.
- Encode recovery as a staged state machine with explicit fallback.
- Verify altitude-frame projections and directionality in simulator tests, not just nominal mission completion.

Do not copy:

- Do not copy vehicle-specific policy without the corresponding sensor and mission assumptions.
- Do not assume a passing SITL mission proves hardware recovery.
- Do not conflate circle-direction and altitude-frame checks with the generic failsafe ladder.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The failsafe and RTL paths are explicit and bounded.
- The autotest harness covers both telemetry-loss recovery and mission geometry assertions.
- Shared helpers reduce duplication between different rover-style checks.

Experimental or incomplete for our needs:

- The review still needs a live SITL run for the current rover circle-direction path and the current recovery ladder.
- Hardware-in-the-loop and fleet-level coordination were not validated here.
- Simulator fidelity still matters for circle geometry and altitude-frame correctness.

Hidden costs and failure modes:

- False-positive stall detection can force a spurious failsafe.
- Mode transitions can flap if sensor availability changes during recovery.
- Rover circle checks can pass in a simulator that does not reflect the real vehicle's ground-truth behavior.

Adoption experiment:

Run Rover SITL with `MAV_CMD_NAV_LOITER_TURNS` in both clockwise and counter-clockwise configurations, verify `POSITION_TARGET_GLOBAL_INT.alt` remains AMSL-correct, and combine that with a GCS-failsafe loss/recovery cycle to confirm the mission state does not drift across recovery.

## Candidate Patterns

- `mission failsafe fallback state machine`
- `circle-direction SITL assertion harness`
- `AMSL position-target projection`
