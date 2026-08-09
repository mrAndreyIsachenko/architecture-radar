# ArduPilot Telemetry Integrity And Failsafe Diagnostics

## Opportunity Summary
ArduPilot users repeatedly report telemetry loss, missing ESC log data, and replay or arming failures that make it hard to trust the stack in flight. The opportunity is a diagnostics tool that scores telemetry integrity from logs and flags unsafe or degraded behavior.

## Evidence
- M2 repeated pain: `#9752` (2018-11-10) reports about 80% MAVLink packet loss in Mission Planner or Solex over UDP.
- M2 repeated pain: `#27746` (2024-08-03) says ESC temperature telemetry is visible in Mission Planner but lost in OSD on v4.5.5.
- M2 repeated pain: `#32351` (2026-03-02) says bidirectional DShot telemetry sometimes fails to start until the user power-cycles hardware.
- M2 repeated pain: `#32905` (2026-04-24) asks for native DShot/BDShot telemetry error counters because partial telemetry is hard to trust.
- M4 workaround evidence: `#28807` (2024-12-05) shows users comparing Mission Planner output with logs to prove the firmware bug, which is a manual workaround.
- M4 workaround evidence: `#11929` and related reports show operators inferring thrust-loss behavior from plots and manual analysis instead of a reliability score.

## Repeated Pain Or Demand Signal
Teams need a way to know when telemetry is incomplete or unreliable before it affects mission safety, tuning, or post-flight analysis.

## Likely User Or Buyer
UAV operators, robotics labs, integrators, and flight-test engineers using ArduPilot with Mission Planner or companion telemetry systems.

## Current Workaround Or Money Signal
Manual log review, Mission Planner stats windows, firmware updates, and repeated bench tests are used to isolate telemetry faults.

## Proposed Offer
A log analyzer that scores telemetry integrity, detects missing ESC or MAVLink frames, and produces a simple flight-readiness report.

## Success Threshold
At least 3 teams or labs upload real logs in one week, or 1 integrator asks for a paid follow-on analysis after seeing the report.

## Falsification Threshold
The reports mostly reduce to one-off wiring mistakes, with no recurring software or workflow gap to solve.

## Evidence Gaps
- No budget evidence yet.
- Need more confirmation that a diagnostics layer would be used in routine operations, not only after failures.

## Decision
Selected.
