# PX4/PX4-Autopilot

- Repository: https://github.com/PX4/PX4-Autopilot
- Review date: 2026-10-31
- Current commit reviewed: `789389fd46fcfb8473544d2fb3eeabd85893294c`
- Commit date: 2026-10-31T18:19:50+10:00
- Branch: `main`
- Previous commit reviewed: `07a2faab0dd4621e3b85d1818a7f6e4af63cf87f`
- Material changes since previous review: the current head adds protocol-recovery logic for MAVLink parameters and missions. Rejected parameter writes now still receive a current-value acknowledgement, failed uploads release transfer state, and recoverable in-range mission requests keep the expected sequence instead of resetting the transfer.
- Decision: track

## Problem Fit

This repository informs `drones-robotics-autonomy`: mission planning, telemetry, command reliability, and recovery from partial MAVLink transaction failure. The reusable mechanism is no longer only a failsafe ACK matrix. The current head explicitly recovers parameter and mission transactions so a ground-control retry can converge without corrupting the active transfer state.

## Verified Flow

MAVLink `PARAM_SET` / `PARAM_REQUEST_READ` input -> `MavlinkParametersManager::handle_message` classifies the target, enforces type and read-only checks, and calls `send_error` or `send_param` -> `send_param` returns the current value as the acknowledgement payload, while a TX-buffer stall returns a distinct code instead of misreporting "does not exist" -> MAVLink `MISSION_REQUEST_LIST` / `MISSION_REQUEST(_INT)` input -> `MavlinkMissionManager::handle_mission_request_list` resets the transfer only when the request is compatible or the previous send is already complete -> `handle_mission_request_both` accepts the expected sequence, tolerates a duplicate previous item, and treats an unexpected in-range request as recoverable without advancing the cursor -> `handle_mission_item` and `handle_mission_item_int` either accept the item, reject it with an explicit mission result, or release transfer state when the item is invalid or cannot be written -> tests cover the parameter FTP stream, mission parameter-slot validation, and the live MAVSDK mission harness.

- E1 source verified: `src/modules/mavlink/mavlink_parameters.cpp:228-315` handles parameter writes, read-only rejection, type mismatch, and the current-value acknowledgement path.
- E1 source verified: `src/modules/mavlink/mavlink_parameters.cpp:318-379` handles parameter reads, missing parameters, load failures, and the distinct TX-buffer-full path.
- E1 source verified: `src/modules/mavlink/mavlink_parameters.cpp:657-755` implements `send_param`, including the return code that separates buffer saturation from missing parameters.
- E1 source verified: `src/modules/mavlink/mavlink_mission.cpp:701-855` handles mission ACKs, mission list requests, and the resend-safe transition back to idle when a completed transfer is retried.
- E1 source verified: `src/modules/mavlink/mavlink_mission.cpp:858-972` handles mission request replay, duplicate previous-item requests, and recoverable in-range requests without advancing the transfer cursor.
- E1 source verified: `src/modules/mavlink/mavlink_mission.cpp:1160-1365` handles mission item writes, duplicate terminal-item ACKs, write failures, and transfer completion.
- E2 test verified: `test/mavsdk_tests/test_param_ftp.py:73-119` compares the PARAM_VALUE stream against FTP download/upload behavior.
- E2 test verified: `test/mavsdk_tests/test_mavlink_param_validation.py:108-220` exercises mission uploads and command validation with supported and unsupported parameter slots.
- E2 test verified: `test/mavsdk_tests/test_multicopter_mission.py:17-48` exercises mission execution and return-to-launch behavior in the MAVSDK harness.

## Architecture

Principal components:

- MAVLink parameter manager with explicit reject, current-value, and buffer-saturation paths.
- MAVLink mission manager with an explicit transfer cursor and recoverable replay rules.
- Dataman-backed mission storage and completion tracking.
- MAVSDK and Python regression tests that validate protocol-level semantics instead of only the flight loop.

Most interesting mechanism: PX4 does not collapse protocol failure into a generic "retry later". Parameter writes are always acknowledged with the current value, and mission downloads preserve their expected sequence even when a recoverable request arrives out of order. That makes the transport robust against duplicate requests and partial uploads without losing the active transfer state.

Baseline comparison: a simpler MAVLink implementation would either drop a rejected parameter write on the floor or abort a mission transfer on any unexpected request. PX4 instead distinguishes missing, rejected, recoverable, and saturated cases so the ground station can converge without corrupting the session.

## Reuse Guidance

Reusable:

- A rejected write should still return the current value so the transaction can finish cleanly.
- Recoverable out-of-range mission requests should not reset the cursor.
- Differentiate buffer saturation from "missing parameter" so the operator can retry correctly.
- Keep mission transfer state explicit enough to survive duplicate terminal requests.

Do not copy:

- Do not copy the full embedded stack or hardware-specific mode logic.
- Do not assume the transport recovery rules are sufficient without a live simulator run.
- Do not collapse every protocol error into one return code if the caller needs to retry intelligently.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The protocol paths are explicit about accepted, rejected, saturated, and recoverable cases.
- The parameter and mission tests pin the expected transport semantics.
- The current head adds a concrete recovery rule instead of just another validation branch.

Experimental or incomplete for our needs:

- The review is still source-backed; it does not prove the behavior under a full SITL run on this host.
- Mission and parameter recovery depend on simulator fidelity and ground-station behavior.
- The embedded codebase is large enough that new command cases can still introduce subtle regressions.

Hidden costs and failure modes:

- If the current-value acknowledgement is omitted, parameter transactions can wedge on retries.
- If recoverable mission requests advance the cursor, a reconnect can skip items or mis-ack the session.
- If buffer-saturation is misreported as "missing parameter", the ground station may stop retrying too early.

Adoption experiment:

Run a mission upload and a parameter write against SITL, inject duplicate and out-of-order requests, and confirm that rejected parameter writes still complete via current-value acknowledgement while recoverable mission requests preserve the transfer cursor.

## Candidate Patterns

- `failsafe command acknowledgment matrix`
- `mission sensor-loss recovery`
- `parameter-slot mission validation gate`
- `parameter current-value acknowledgement`
- `recoverable mission cursor`

## Previous Review

The [2026-10-13 report](../reports/2026-10-13.md) and the previous card recorded the commander-side ACK matrix and sensor-loss behavior at `07a2faab0dd4621e3b85d1818a7f6e4af63cf87f`. This current review adds the parameter and mission transaction-recovery paths at `789389fd46fcfb8473544d2fb3eeabd85893294c`.
