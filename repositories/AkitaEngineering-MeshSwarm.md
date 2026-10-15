# AkitaEngineering/MeshSwarm

- Repository: https://github.com/AkitaEngineering/MeshSwarm
- Review date: 2026-10-07
- Current commit reviewed: `bd7f2d1a5791f06abcc6254279b42b79d69a7219`
- Commit date: 2026-09-16
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `drones-robotics-autonomy`, especially mesh-drone telemetry freshness, encrypted control delivery, ACK replay handling, and failsafe recovery to RTL. The reusable mechanism is the safety loop, not the GCS app or simulator framing.

## Verified Flow

`gcs_app.on_receive` routes framed telemetry and ACK packets to the proper handlers -> `send_command` validates the control request, rate limits non-heartbeat commands, encrypts the command, and optionally waits for ACK -> `_heartbeat_loop` keeps heartbeat traffic flowing -> `meshtastic_thread` reconnects with backoff and re-subscribes on interface failure -> `send_control_command` and `handle_encrypted_ack` maintain encrypted control state and ACK tracking -> `maybe_failsafe` reads telemetry freshness, geofence state, battery state, GPS state, and GCS presence, then queues MAVLink RTL when a fail condition is latched -> `handle_control_plaintext` rejects stale/replayed control commands and turns accepted commands into MAVLink actions -> the test suite covers control, status, rate limiting, startup gating, replay rejection, and simulator ACK flow.

- E1 source verified: `gcs_app.py::on_receive`, `/api/control`, `_heartbeat_loop`, `_connect_interface`, and `meshtastic_thread` implement framed dispatch and reconnect behavior.
- E1 source verified: `meshtastic_control.py::send_control_command`, `handle_encrypted_ack`, `wait_for_ack`, and `request_seq_sync` implement encrypted command/ACK sequencing.
- E1 source verified: `main/main.cpp::maybe_failsafe`, `handle_control_plaintext`, `task_meshtastic_rx`, and `task_telemetry_tx` implement failsafe and telemetry loops.
- E2 test verified: `tests/test_gcs_app.py`, `tests/test_qa_simulator.py`, and `tests/test_meshtastic_telemetry_on_receive.py` cover command encryption, rate limiting, startup gating, replay rejection, geofence marking, and simulator ACKs.

## Architecture

Principal components:

- Flask ground-station API with auth, rate limiting, and ACK wait logic.
- Mesh control library with encrypted control frames and sync/replay handling.
- ESP32-side control loop with MAVLink ACK service and latching failsafe logic.
- Test simulator and telemetry tests for offline verification.

Most interesting mechanism: the mesh loop separates control sequencing from actuation, then latches the failsafe path so repeated lost-link or geofence events still converge on the same RTL command instead of oscillating.

Baseline comparison: a basic mesh controller would only forward packets and hope the drone state stays coherent. MeshSwarm keeps sequence sync, ACK replay protection, and fail-safe escalation explicit.

## Reuse Guidance

Reusable:

- Treat ACK and telemetry replay as first-class protocol state.
- Keep the reconnect loop separate from the failsafe loop.
- Make stale or replayed control commands rejectable before actuation.
- Latch the fail-safe transition so repeated triggers do not spam the actuation path.

Do not copy:

- Do not copy the Meshtastic-specific transport assumptions unless that is your actual mesh.
- Do not reuse the heartbeat cadence or thresholds without revalidation on hardware.
- Do not assume simulator coverage proves real flight-controller behavior.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Encrypted control framing and ACK tracking are explicit source code paths.
- The failsafe decision is driven by telemetry freshness and safety thresholds.
- Tests cover replay rejection and simulator ACK behavior.

Experimental or incomplete for our needs:

- The control loop still needs restart and operational validation on a real mesh and flight-controller path.
- The simulator does not prove multi-node fleet behavior under real link churn.
- The code path remains tightly coupled to specific Meshtastic and MAVLink assumptions.

Hidden costs and failure modes:

- Sequence synchronization bugs can silently reject valid commands or accept stale ones.
- Failsafe latching can hide upstream health issues if the operator expects faster recovery.
- Reconnect backoff can mask flaky transports rather than fixing them.

Adoption experiment:

Run a live mesh with forced disconnects, command replay, and FCU restarts, then confirm the GCS reconnects, ACK state resynchronizes, and the drone converges back to the same canonical RTL path without duplicate stale commands.

## Candidate Patterns

- `Mission Failsafe Fallback State Machine`
- `encrypted mesh ACK sequencing`
