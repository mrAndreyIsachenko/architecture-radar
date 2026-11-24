# PX4/PX4-Autopilot

- Repository: https://github.com/PX4/PX4-Autopilot
- Review date: 2026-11-24
- Current commit reviewed: `d090301e480480ceb128280a21f2727091466db2`
- Commit date: 2026-11-24T12:15:45+0100
- Branch: `main`
- Previous commit reviewed: `07a2faab0dd4621e3b85d1818a7f6e4af63cf87f`
- Material changes since previous review: the current head keeps the commander/failsafe safety model intact while changing the fixed-wing landing path so wingtip-strike roll limits use terrain altitude during landing flare. The command-acknowledgment matrix remains intact; the new landing safety guard is the material delta.
- Decision: track

## Problem Fit

This repository informs `drones-robotics-autonomy`: mission planning, telemetry, safety envelopes, command acknowledgments, landing flare logic, and recovery from sensor loss or flight-mode loss. The reusable mechanisms are the commander-side command-acknowledgment matrix and the fixed-wing landing guard that bases near-ground roll limits on terrain altitude instead of a takeoff-ground proxy.

## Verified Flow

MAVLink command / mission input -> `Commander::handle_command` classifies the command and assigns an ACK result -> `Commander::answer_command` publishes the ACK back to MAVLink -> `Commander::arm` / `disarm` enforce preflight, health, and failsafe gates -> `test/test_mavlink_param_validation.py` validates unsupported parameter slots at the mission/command boundary -> `test/mavsdk_tests/test_multicopter_failsafe.cpp` and `autopilot_tester.cpp` execute GPS, baro, and magnetometer-loss missions until the vehicle reaches the expected recovery state -> `FixedWingModeManager::control_auto_landing_straight` resolves terrain altitude and uses it to cap flare and wingtip-strike roll limits near ground.

- E1 source verified: `src/modules/commander/Commander.hpp` wires in failsafe, mission, offboard, `mission_result`, `vehicle_command_ack`, and health-check subsystems.
- E1 source verified: `src/modules/commander/Commander.cpp:862-930,2827-2865` classifies incoming `vehicle_command` messages, assigns accepted/denied/temporarily-rejected results, and publishes the ACK.
- E1 source verified: `src/modules/commander/Commander.cpp:667-760` enforces preflight, throttle, and health checks before arming.
- E1 source verified: `src/modules/rc_update/rc_update.cpp` handles RC function mapping and fallback behavior when parameters or calibration state change.
- E1 source verified: `src/modules/fw_mode_manager/FixedWingModeManager.cpp:1523-1618,1686-1687,1762-1902,2553-2710` derives landing terrain altitude, uses it in flare and wingtip-strike roll limits, and keeps the near-ground landing guard terrain-aware.
- E2 test verified: `test/test_mavlink_param_validation.py:108-260` rejects mission items and commands with unsupported parameter slots and accepts valid variants.
- E2 test verified: `test/mavsdk_tests/test_multicopter_failsafe.cpp:37-167` exercises mission continuation or landing after GPS, baro, and magnetometer loss.
- E2 test verified: `test/mavsdk_tests/autopilot_tester.cpp` supports the integration harness that arms, runs, and degrades missions under sensor-loss injection.

## Architecture

Principal components:

- Commander state machine that owns command dispatch, mode transitions, arming, and failsafe coordination.
- Health and arming checks that gate high-risk transitions.
- Mission and command validation harnesses that pin the ACK matrix against the MAVLink parameter contract.
- MAVSDK integration tests that simulate sensor loss and mission continuation.
- Fixed-wing mode manager landing helpers that translate terrain altitude into flare and wingtip-strike roll limits.

Most interesting mechanism: the command path is explicit about accept, deny, temporary reject, unsupported, and failed outcomes, and the landing path now makes the near-ground roll envelope depend on terrain altitude so flare behavior follows the actual ground profile instead of a generic fixed-height proxy.

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
- The new terrain-aware landing guard still needs full SITL validation with landing, sensor-loss, and terrain-estimate churn.

Hidden costs and failure modes:

- The behavior depends on hardware/sensor availability and simulator fidelity.
- Command/mode semantics are distributed across several subsystems.
- ACK semantics and mission validation can change in subtle ways when new command cases are added, so regressions need explicit coverage.
- Terrain-altitude gating can only be trusted if the terrain estimate stays coherent through the landing phase; stale or invalid terrain data can still distort the roll-limit guard.

Adoption experiment:

Use the PX4 command-ACK model as a template for an internal autonomy agent: every high-risk transition must return accepted, denied, temporarily rejected, unsupported, or failed, and the test suite must cover sensor-loss recovery, terrain-estimate churn, and landing flare validation.

## Candidate Patterns

- `failsafe command acknowledgment matrix`
- `mission sensor-loss recovery`
- `parameter-slot mission validation gate`
- `terrain-aware landing roll guard`
