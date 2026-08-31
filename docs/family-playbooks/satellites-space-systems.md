# Satellites Space Systems Playbook

## Family

`satellites-space-systems`

Use this playbook for satellite operations, ground stations, RF/geospatial pipelines, space-domain awareness, delayed connectivity, telemetry/command loops, scheduling, and constellation coordination.

## Mechanisms To Search

- Delayed and intermittent connectivity workflows.
- Telemetry/command loops with explicit ACK, timeout, retry, and rejection handling.
- Ground-station automation and pass-window orchestration.
- Observation, downlink, contact, and task scheduling under resource constraints.
- Safe-mode, fault recovery, and anomaly-response state machines.
- RF signal-processing and decoding pipelines with reproducible provenance.
- Geospatial evidence generation with source, time, region, sensor, and confidence metadata.
- Constellation coordination and fleet-level task allocation.

## Evidence Bar

- Source evidence for command, telemetry, scheduling, processing, or recovery behavior.
- Tests, simulations, replays, sample telemetry, RF recordings, or operational docs for failure paths.
- Explicit handling of stale telemetry, missed contacts, rejected commands, partial uploads, and mode transitions.
- Provenance from observation or RF input to derived artifact.

## Selection Bias

Prefer mechanisms that survive outside the specific mission: delayed-connectivity recovery, command/telemetry audit trails, pass-window scheduling, safe-mode state, and provenance-preserving RF/geospatial pipelines.

## Rejection Triggers

- Mission, hardware, or company page with no inspectable source.
- Dashboard-only project with no command, telemetry, scheduling, or recovery model.
- Single-purpose decoder with no provenance, tests, replay data, or operational failure handling.
- Space-domain awareness claim with no reproducible data or source-backed pipeline.

## Validation Evidence

- Simulated or replayed pass window.
- Command ACK, timeout, reject, and retry traces.
- Missed-contact and reconnect recovery behavior.
- Safe-mode transition and recovery evidence.
- RF recording to decoded artifact provenance.
- Geospatial output tied to source observation time, sensor, region, and confidence.

## Useful Search Seeds

- `ground station automation`, `satellite telemetry command`, `satnogs client`, `openmct telemetry`, `spacecraft command ack`, `mission control scheduler`, `TLE pass scheduler`, `RF signal processing satellite`, `space domain awareness open source`, `geospatial provenance`
