# Mission Failsafe Fallback State Machine

- Canonical name: Mission Failsafe Fallback State Machine
- Aliases: RTL fallback machine, safe-mode mission controller, staged recovery state machine, autonomy failsafe ladder
- Avoided duplicate names: emergency lander, panic stop, autopilot watchdog, mission abort switch
- Last updated: 2026-09-13

## Problem

Autonomy systems need deterministic behavior when links fail, sensors degrade, or the main loop stalls. A single emergency action is often too coarse: the system needs to detect the fault, reduce output safely, preserve operator visibility, and choose among return, land, or controlled continuation based on the current mission and sensor state.

## Mechanism

Combine a fast watchdog with explicit mission fallback states:

- Detect main-loop lockup or transport loss on a tight timer.
- Enter a failsafe state after a bounded timeout.
- Reduce actuator output before full disarm so the failure is visible and controlled.
- Model return-to-launch as a staged state machine with explicit climb, return, loiter, descent, and land phases.
- Restart RTL without terrain when terrain data becomes invalid, or degrade into landing when safe navigation inputs are missing.
- Expose the active failsafe severity through telemetry/status channels.
- Validate the behavior in SITL or HIL with radio, GPS, and mission continuation injection.

## Invariants

- Safety reduction happens before final disarm.
- Recovery states must be explicit and ordered, not inferred from logs.
- Terrain or position uncertainty must force a conservative fallback.
- Operator-facing status must match the current failsafe condition.
- Recovery behavior must be testable under simulated failure injection.

## Implementation Variants

- Stall-watchdog codeline: ArduPilot detects scheduler stagnation at 1 kHz and disarms after a two-second stall.
- Staged RTL controller: ArduPilot's RTL mode moves through start, climb, return, loiter, descent, and land states, with terrain restart when needed.
- Mission/safety regression harness: ArduPilot autotests inject RC and GPS failures and verify the resulting mode transitions and mission continuation behavior.
- Command-response safety matrix: PX4 uses a different control structure, but still encodes explicit failsafe and mission recovery policies that can be compared against the staged RTL approach.

## Known Repositories

- `ArduPilot/ardupilot` reviewed at `acef45eb0f0145943a9c2ba341d3825b8af34472`.
- `PX4/PX4-Autopilot` reviewed at `d57d7f3b11c044b86195a12cfb933d17fac85b34`.

## Comparison Of Implementations

ArduPilot is strongest for making the fallback ladder explicit in both source and SITL tests. The staged RTL machine makes the transition from mission intent to conservative landing easy to audit.

PX4 is the useful comparison baseline because it provides a separate autonomy stack with its own failsafe and mission recovery design. That helps distinguish reusable safety structure from ArduPilot-specific implementation details.

The conventional baseline is a single "land now" emergency response. That is simpler, but it loses the ability to preserve mission intent when the system can still navigate safely.

## Failure Modes

- False positive stall detection can trigger a spurious failsafe.
- Mode transitions can flap if sensor confidence changes during recovery.
- Mission continuation policies can keep flying when the operator expected an abort.
- Terrain-data mismatch can force repeated RTL restarts or a conservative land.

## Trade-Offs

- More explicit recovery states improve auditability but increase state-machine complexity.
- Safety-first fallback may interrupt missions that could have continued with more permissive policy.
- SITL coverage is cheap compared with flight testing, but it can still miss hardware timing and sensor edge cases.

## Applicability To Interests

- `drones-robotics-autonomy`: directly applicable to mission planning, telemetry, safety recovery, and operator override.
- `satellites-space-systems`: a close analogue for safe-mode recovery and delayed command/telemetry loops.
- `ai-llm-systems`: useful as a pattern for agent fallbacks that need explicit safe modes instead of one-shot aborts.

## Adoption Conditions

- Validate RC-loss, GPS-loss, and mission-continuation cases in SITL or HIL.
- Verify that telemetry/status matches the active fallback stage.
- Test recovery and restart behavior after both transient and persistent sensor loss.

## Evidence References

- E1 source verified: ArduPilot `ArduCopter/failsafe.cpp::failsafe_check` detects stalled main-loop ticks, reduces motor output, and disarms repeatedly while failsafe remains active.
- E1 source verified: ArduPilot `ArduCopter/mode_rtl.cpp::run`, `return_start`, `restart_without_terrain`, and `climb_return_run` encode the staged RTL ladder and terrain fallback.
- E1 source verified: ArduPilot `ArduCopter/GCS_MAVLink_Copter.cpp::vehicle_system_status` reports critical state when any failsafe is active.
- E2 test verified: ArduPilot `Tools/autotest/arducopter.py::ThrottleFailsafe` injects RC and GPS failures and checks RTL, Land, SmartRTL, guided continuation, and mission continuation behavior.
- E2 test verified: ArduPilot `Tools/autotest/run_mission.py` runs a mission in SITL and waits for completion/disarm.
