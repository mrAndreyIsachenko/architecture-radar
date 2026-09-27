# EspiroFares/Autonomous-UAV

- Repository: https://github.com/EspiroFares/Autonomous-UAV
- Review date: 2026-09-22
- Current commit reviewed: `8df4f467332fcf7a93cf93dc596d5f8d78f94396`
- Commit date: 2026-09-01T01:12:38+02:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `drones-robotics-autonomy`, especially mission-state fallback, sensor freshness, single-gateway flight-controller control, and hardware-free autonomy testing. The useful mechanism is the safety-gated autonomy stack, not the demo framing around person following.

## Verified Flow

`mission_manager_node` turns world-model validity into mission state and publishes `follow_enabled` -> `follow_controller_node` reads target position and lidar height, applies freshness checks, and emits safe velocity setpoints or a hover/hold command -> `hold_policy.hpp` decides whether the upstream setpoint may pass through or must be converted to canonical hold based on supervisor silence, veto, or staleness -> `fcu_bridge_node` is the only gateway to the flight controller, zeroes unsafe commands, republishes vehicle state, and projects lidar height after tilt compensation -> the test suite checks the freshness envelope, hold policy, safety checks, and range/physics gating.

- E1 source verified: `software/drone_ws/src/drone_behavior/src/mission_manager_node.cpp` implements the mission state machine with `IDLE`, `SEARCH`, `TRACKING`, `FOLLOWING`, `TARGET_LOST`, and `SAFETY_HOLD`.
- E1 source verified: `software/drone_ws/src/drone_control/src/follow_controller_node.cpp` computes yaw, forward speed, and altitude hold with freshness checks and safe degradation.
- E1 source verified: `software/drone_ws/src/drone_safety/include/drone_safety/hold_policy.hpp` contains the pure hold-vs-pass-through decision logic and canonical hold command.
- E1 source verified: `software/drone_ws/src/drone_state/src/fcu_bridge_node.cpp` acts as the sole ROS-to-flight-controller gateway and zeros unsafe or stale commands.
- E1 source verified: `software/drone_ws/src/drone_state/src/mock_fcu_node.cpp` and `software/drone_ws/src/drone_state/src/world_model_node.cpp` support hardware-free testing and synthetic world-state input.
- E2 test verified: `software/drone_ws/src/drone_control/test/test_setpoint_limits.cpp`, `software/drone_ws/src/drone_safety/test/test_hold_policy.cpp`, `software/drone_ws/src/drone_safety/test/test_safety_checks.cpp`, and `software/drone_ws/src/drone_perception/test/test_range_model.cpp` cover envelope, veto, and range-model behavior.

## Architecture

Principal components:

- Mission state machine that derives follow eligibility from world-model freshness.
- Follow controller with bounded yaw, velocity, and altitude loops.
- Pure hold policy that normalizes every unsafe path into one canonical hold command.
- FCU bridge that remains the only command gateway to MAVROS.
- Mock FCU and test suites for hardware-free validation.

Most interesting mechanism: the stack separates mission intent, control generation, and safety veto into distinct nodes, but every unsafe branch converges on the same canonical hold path before anything reaches the FCU. That keeps the controller expressive without letting the flight bridge become permissive.

Baseline comparison: a simpler autonomy stack would let control nodes talk straight to the FCU or rely on ad hoc null commands. This repository instead makes freshness, veto, and hold behavior explicit and testable.

## Reuse Guidance

Reusable:

- Use a pure veto policy to normalize all unsafe states into one canonical hold output.
- Keep the flight-controller bridge as the single command gateway.
- Publish mission state separately from actuation so the operator can see why the stack is holding.
- Test freshness, silence, and envelope limits at the policy boundary.

Do not copy:

- Do not copy the ROS package layout as-is unless you are already on ROS 2 + MAVROS.
- Do not rely on the current demo control tuning for a different vehicle or mission.
- Do not assume SITL parity with real airframes without flight validation.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The safety logic is pushed into a pure header and covered by unit tests.
- The FC bridge is a clearly identifiable control boundary.
- The repository provides mock nodes and testable inputs for hardware-free validation.

Experimental or incomplete for our needs:

- The repo is still organized around a simulated person-following scenario.
- The safety hold path was not validated here in a longer SITL mission with repeated dropout and restart churn.
- The tuning is exposed for live adjustment, which is useful but also means behavior is sensitive to parameters.

Hidden costs and failure modes:

- Stale perception or height data forces hold, which is safe but may interrupt useful work.
- The controller depends on freshness assumptions across several nodes.
- A single FCU bridge is safer, but it becomes a critical chokepoint.

Adoption experiment:

Run a long SITL mission with repeated target-loss, world-model silence, and FCU bridge restarts, then confirm the stack always falls back to the same canonical hold command and never sends stale actuation through the bridge.

## Candidate Patterns

- `mission-state-driven follow gating`
- `canonical hold command`
- `single flight-controller gateway`
- `pure safety veto policy`
