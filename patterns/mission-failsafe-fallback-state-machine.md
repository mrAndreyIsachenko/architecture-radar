# Mission Failsafe Fallback State Machine

- Canonical name: Mission Failsafe Fallback State Machine
- Aliases: RTL fallback machine, safe-mode mission controller, staged recovery state machine, autonomy failsafe ladder
- Avoided duplicate names: emergency lander, panic stop, autopilot watchdog, mission abort switch
- Last updated: 2026-10-07

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
- Carry ACK replay, command sequencing, and telemetry freshness into the same failsafe ladder so mesh control traffic and vehicle recovery stay aligned.

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
- Mission-state hold boundary: `EspiroFares/Autonomous-UAV` routes world-model freshness into mission states, forces stale or silent setpoints into a canonical hold, and keeps the FCU bridge as the only actuation gateway.
- Mesh failsafe ladder: `AkitaEngineering/MeshSwarm` latches RTL when geofence, low battery, lost link, no GCS, or GPS loss trips, while encrypted control and ACK sync keep the mesh command path replay-safe.

## Known Repositories

- `ArduPilot/ardupilot` reviewed at `acef45eb0f0145943a9c2ba341d3825b8af34472`.
- `PX4/PX4-Autopilot` reviewed at `d57d7f3b11c044b86195a12cfb933d17fac85b34`.
- `EspiroFares/Autonomous-UAV` reviewed at `8df4f467332fcf7a93cf93dc596d5f8d78f94396`.
- `AkitaEngineering/MeshSwarm` reviewed at `bd7f2d1a5791f06abcc6254279b42b79d69a7219`.

## Comparison Of Implementations

ArduPilot is strongest for making the fallback ladder explicit in both source and SITL tests. The staged RTL machine makes the transition from mission intent to conservative landing easy to audit.

PX4 is the useful comparison baseline because it provides a separate autonomy stack with its own failsafe and mission recovery design. That helps distinguish reusable safety structure from ArduPilot-specific implementation details.

`EspiroFares/Autonomous-UAV` shows the same fallback idea at a more application-level autonomy stack: mission state, freshness checks, and a canonical hold command are enough to keep the FCU bridge from seeing stale setpoints. The implementation is smaller than ArduPilot, so it is a useful safety-pattern variant but not a replacement for flight-stack-grade validation.

`AkitaEngineering/MeshSwarm` shows the same fallback idea over a mesh control path: encrypted commands are ACKed and replay-checked, then the ESP32 loop latches RTL on geofence, low battery, lost link, no GCS, or GPS loss. It is useful for replay-safe mesh recovery, but it still needs live restart validation on the real mesh and flight-controller path.

The conventional baseline is a single "land now" emergency response. That is simpler, but it loses the ability to preserve mission intent when the system can still navigate safely.

## Failure Modes

- False positive stall detection can trigger a spurious failsafe.
- Mode transitions can flap if sensor confidence changes during recovery.
- Mission continuation policies can keep flying when the operator expected an abort.
- Terrain-data mismatch can force repeated RTL restarts or a conservative land.
- Canonical hold policies can become overconservative if freshness thresholds are too strict or one node stops publishing.
- Replay or sequence-sync bugs can make the mesh command path reject the wrong command or accept a stale one.

## Trade-Offs

- More explicit recovery states improve auditability but increase state-machine complexity.
- Safety-first fallback may interrupt missions that could have continued with more permissive policy.
- SITL coverage is cheap compared with flight testing, but it can still miss hardware timing and sensor edge cases.
- Pure hold policies make the safety decision easy to test, but they can mask whether the upstream controller is actually healthy.

## Applicability To Interests

- `drones-robotics-autonomy`: directly applicable to mission planning, telemetry, safety recovery, and operator override.
- `satellites-space-systems`: a close analogue for safe-mode recovery and delayed command/telemetry loops.
- `ai-llm-systems`: useful as a pattern for agent fallbacks that need explicit safe modes instead of one-shot aborts.
- `privacy-networking-vpn`: useful where reconnect recovery and policy state must converge before control resumes.

## Adoption Conditions

- Validate RC-loss, GPS-loss, and mission-continuation cases in SITL or HIL.
- Verify that telemetry/status matches the active fallback stage.
- Test recovery and restart behavior after both transient and persistent sensor loss.
- Validate repeated target-loss, world-model silence, and bridge-restart cases in SITL so the canonical hold path is exercised more than once.
- Validate command replay rejection, ACK sync, and mesh reconnect recovery on real hardware before depending on the mesh ladder.

## Evidence References

- E1 source verified: ArduPilot `ArduCopter/failsafe.cpp::failsafe_check` detects stalled main-loop ticks, reduces motor output, and disarms repeatedly while failsafe remains active.
- E1 source verified: ArduPilot `ArduCopter/mode_rtl.cpp::run`, `return_start`, `restart_without_terrain`, and `climb_return_run` encode the staged RTL ladder and terrain fallback.
- E1 source verified: ArduPilot `ArduCopter/GCS_MAVLink_Copter.cpp::vehicle_system_status` reports critical state when any failsafe is active.
- E2 test verified: ArduPilot `Tools/autotest/arducopter.py::ThrottleFailsafe` injects RC and GPS failures and checks RTL, Land, SmartRTL, guided continuation, and mission continuation behavior.
- E2 test verified: ArduPilot `Tools/autotest/run_mission.py` runs a mission in SITL and waits for completion/disarm.
- E1 source verified: `EspiroFares/Autonomous-UAV/software/drone_ws/src/drone_behavior/src/mission_manager_node.cpp` tracks mission state from world-model validity and publishes `follow_enabled`.
- E1 source verified: `EspiroFares/Autonomous-UAV/software/drone_ws/src/drone_control/src/follow_controller_node.cpp` clamps and freshness-gates the control output, then degrades to safe hover or hold.
- E1 source verified: `EspiroFares/Autonomous-UAV/software/drone_ws/src/drone_safety/include/drone_safety/hold_policy.hpp` normalizes all unsafe states into a canonical hold command.
- E1 source verified: `EspiroFares/Autonomous-UAV/software/drone_ws/src/drone_state/src/fcu_bridge_node.cpp` zeroes unsafe actuation and remains the only gateway to the FCU.
- E2 test verified: `EspiroFares/Autonomous-UAV/software/drone_ws/src/drone_safety/test/test_hold_policy.cpp` and `test_safety_checks.cpp` verify silence, veto, and staleness behavior.
- E1 source verified: `AkitaEngineering/MeshSwarm/gcs_app.py::on_receive`, `/api/control`, `_heartbeat_loop`, `_connect_interface`, and `meshtastic_thread` implement the reconnectable mesh control loop.
- E1 source verified: `AkitaEngineering/MeshSwarm/meshtastic_control.py::send_control_command`, `handle_encrypted_ack`, `wait_for_ack`, and `request_seq_sync` implement ACK and sequence replay handling.
- E1 source verified: `AkitaEngineering/MeshSwarm/main/main.cpp::maybe_failsafe`, `handle_control_plaintext`, `task_meshtastic_rx`, and `task_telemetry_tx` implement the mesh failsafe ladder.
- E2 test verified: `AkitaEngineering/MeshSwarm/tests/test_gcs_app.py`, `tests/test_qa_simulator.py`, and `tests/test_meshtastic_telemetry_on_receive.py` cover command encryption, rate limiting, simulator ACKs, replay rejection, and geofence marking.
