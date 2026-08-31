# Drones Robotics Autonomy Playbook

## Family

`drones-robotics-autonomy`

Use this playbook for drone, robotics, autonomy, mission-control, telemetry, ground-control, perception, fleet, and safety/recovery candidates.

## Mechanisms To Search

- Mission planning state machines and waypoint acceptance models.
- Command ACK, retry, idempotency, timeout, and safe teardown behavior.
- Failsafe transitions for low battery, lost link, geofence breach, localization drift, and operator aborts.
- Telemetry ingestion, event correlation, anomaly detection, and provenance-preserving logs.
- SITL, mission replay, log replay, and simulation harnesses.
- Fleet coordination, fanout, role assignment, and degraded connectivity handling.
- Human override, review queues, and operator intervention audit trails.

## Evidence Bar

- Source evidence for mission, command, telemetry, and safety state transitions.
- Tests, SITL scenarios, mission replay, or log replay proving recovery behavior.
- Explicit handling of partial commands, missing ACKs, telemetry loss, and teardown after abort.
- Compatibility evidence for MAVLink, PX4, ArduPilot, ROS 2, or ground-control integrations.

## Selection Bias

Prefer software that makes autonomy auditable and recoverable. A visual ground-control UI is only interesting when command, telemetry, state, or recovery semantics are inspectable in source.

## Rejection Triggers

- Demo flight script with no command ACK, retry, or failsafe path.
- Hardware-only project without reusable software mechanisms.
- Dashboard-only project without mission or telemetry semantics.
- Autonomy claims without logs, SITL, replay, tests, or source-level control flow.

## Validation Evidence

- SITL run covering mission upload, mission start, lost link, abort, and restart.
- Command ACK and timeout traces.
- Telemetry-loss and reconnect handling.
- Failsafe state transition evidence.
- Mission replay or log replay artifacts.
- Fleet fanout or multi-vehicle coordination tests.

## Useful Search Seeds

- `MAVLink mission ack`, `PX4 SITL failsafe`, `ArduPilot telemetry`, `ROS 2 autonomy recovery`, `drone mission replay`, `ground control station command ack`, `multi drone coordination`, `UAV geofence failsafe`, `mavsdk mission`
