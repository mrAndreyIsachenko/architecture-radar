# ArduPilot/ardupilot

- Repository: https://github.com/ArduPilot/ardupilot
- Review date: 2026-09-13
- Current commit reviewed: `acef45eb0f0145943a9c2ba341d3825b8af34472`
- Commit date: 2026-09-12T19:46:43-03:00
- Branch: `master`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: selected

## Problem Fit

This repository informs `drones-robotics-autonomy`: mission failsafes, RTL fallback, telemetry/status reporting, and SITL-backed recovery verification.

## Verified Flow

Main loop stall or RC/GPS loss -> `failsafe_check()` detects stalled scheduler ticks and enters failsafe after a bounded timeout -> motors are reduced to minimum and then disarmed repeatedly until recovery -> `ModeRTL` transitions through explicit stages for return-to-launch and falls back to landing when terrain or position assumptions fail -> MAVLink system status reports critical state when any failsafe is active -> SITL tests inject RC/GPS failures and verify RTL, Land, SmartRTL, and guided/mission recovery behavior.

- E1 source verified: `ArduCopter/failsafe.cpp::failsafe_check` detects a 2-second loop stall, reduces motor output, logs the failure, and then disarms every second while the failsafe remains active.
- E1 source verified: `ArduCopter/mode_rtl.cpp::init`, `run`, `return_start`, and `restart_without_terrain` implement a staged RTL state machine with terrain fallback.
- E1 source verified: `ArduCopter/GCS_MAVLink_Copter.cpp::vehicle_system_status` reports `MAV_STATE_CRITICAL` when any failsafe has triggered.
- E2 test verified: `Tools/autotest/arducopter.py::ThrottleFailsafe` covers RC-failure disabled, RTL, Land, SmartRTL, GPS-failure fallback, guided continuation, and mission continuation paths.
- E2 test verified: `Tools/autotest/run_mission.py` provides a SITL mission runner that loads a mission, arms, enters AUTO, and waits for disarm.

## Architecture

Principal components:

- Copter failsafe monitor in the 1 kHz timer path.
- RTL flight-mode state machine with terrain-aware fallback.
- MAVLink status reporting to GCS clients.
- SITL/autotest harness for mission and failsafe regression coverage.

Most interesting mechanism: the system does not collapse all failure handling into a single emergency land. It detects main-loop stall explicitly, reduces outputs before full disarm, exposes the critical state upstream, and lets RTL choose between return, loiter, descent, or land based on mode and sensor availability.

Baseline comparison: a conventional emergency controller often has one hard stop action. ArduPilot encodes a tiered recovery path that can preserve mission intent when safe, then degrades to land when the necessary inputs are no longer trustworthy.

## Reuse Guidance

Reusable:

- Use a fast, periodic watchdog to distinguish healthy operation from main-loop lockup.
- Keep return-to-home, land, and guided continuation as explicit states rather than a single callback.
- Expose failsafe severity to operator-facing status channels.

Do not copy:

- Do not copy flight-mode policy without the sensor and mission assumptions that make it safe.
- Do not assume a restart or reconnect path is harmless without SITL or hardware-in-loop coverage.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Strong watchdog, mode, and status separation.
- Extensive autotest coverage around RC and GPS loss.
- Explicit fallback when terrain data or position assumptions fail.

Experimental or incomplete for our needs:

- The review did not validate hardware-in-the-loop behavior or fleet-level coordination.
- The model depends on simulator coverage for several recovery branches we care about.

Hidden costs and failure modes:

- False-positive stall detection can force a spurious failsafe.
- Mode transitions can flap if sensor availability changes during recovery.
- Mission continuation after RC loss still depends on the exact `FS_OPTIONS` policy and the current mode.

Adoption experiment:

Run SITL failure injection for RC and GPS loss, then verify the vehicle transitions through the expected RTL/Land/SmartRTL states and that status reporting matches the failsafe state at each step.

## Candidate Patterns

- `mission failsafe fallback state machine`

