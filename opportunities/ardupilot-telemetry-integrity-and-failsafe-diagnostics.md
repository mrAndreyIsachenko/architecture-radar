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

## Structural Pattern
Telemetry-integrity diagnostic layer for drone operations where flight-controller signals, ESC telemetry, logs, and failsafe interpretation diverge.

## Primitive Growth
ArduPilot telemetry, log-diagnosis discussion, DShot telemetry counters, and autonomous mission workflows create more visible telemetry surfaces to reconcile.

## Fragmentation
Evidence is split across flight logs, telemetry counters, ESC or protocol behavior, failsafe settings, operator reports, and forum diagnosis workflows.

## Manual Workflow
Operators manually inspect logs, forum guidance, telemetry counters, and mission events to decide whether packet loss or telemetry gaps affected safety.

## Objective Function
Maximize telemetry trust and failsafe explainability while minimizing false alarms, missed integrity gaps, and manual post-flight diagnosis time.

## Execution Ladder
- Observe: Read representative flight logs, telemetry counters, failsafe settings, and operator annotations when available.
- Recommend: Classify telemetry gaps, packet-loss patterns, and suspicious failsafe transitions for manual operator review.
- Choose: Rank remediation options such as telemetry tuning, protocol checks, or maintenance actions by risk and evidence strength.
- Execute: Generate a post-flight report only; operational control or autonomous remediation is blocked until private log validation exists.

## Economic Pain
The likely pain is operator safety-review time and mission reliability risk, but public evidence does not yet prove budget for an external diagnostic.

## Timing Reason
Recent public work around telemetry counters and log diagnosis makes the workflow more inspectable, but the market timing remains weaker than the AI/runtime case.

## Competitors
- ArduPilot log tools
- community forum diagnosis
- operator-specific analysis scripts
- manual flight-test review

## Structural Scores
- Fragmentation: 3
- Manual pain: 4
- Economic value: 2
- Objective measurability: 3
- Execution potential: 2
- Timing: 3
- Competition gap: 2
- Prototype feasibility: 2
- Total: 5

## Repeated Pain Or Demand Signal
Teams need a way to know when telemetry is incomplete or unreliable before it affects mission safety, tuning, or post-flight analysis.

## Likely User Or Buyer
UAV operators, robotics labs, integrators, and flight-test engineers using ArduPilot with Mission Planner or companion telemetry systems.

## Current Workaround Or Money Signal
Manual log review, Mission Planner stats windows, firmware updates, and repeated bench tests are used to isolate telemetry faults.

## Technology Shift
- What changed: telemetry-heavy drone operations and public automation work make log integrity and diagnosis more visible as a workflow.
- When: 2026-02-27 through 2026-04-24, with new public log-diagnosis discussion in 2026.
- Old constraint: telemetry and failsafe debugging depended on operator-specific logs and manual log inspection.
- New capability: a log analyzer or report can classify packet loss, telemetry gaps, and reliability issues if representative logs are available.
- Cost delta: unclear; no public paid operator diagnostic evidence found.
- Quality delta: potentially safer post-flight review, but the evidence is still issue- and forum-centric.
- Latency delta: unclear.
- Accessibility delta: useful validation likely requires operator logs, which creates a private-data barrier.
- Affected workflows: post-flight telemetry integrity review, failsafe diagnosis, and mission operations safety review.

## Buyer
UAV operators, robotics labs, integrators, and flight-test engineers using ArduPilot.

## Expensive Workflow
Operators need to reconstruct telemetry integrity and failsafe causes from representative logs.

## Existing Spend
Public forum work shows manual diagnosis effort, and a 2026 ArduPilot log-diagnosis project suggests interest in automated review, but no direct public spend is visible.

## Paid Experiment
Ask one integrator or three operators to upload logs for a paid telemetry-integrity review; success is one paid review request or three sample-log submissions.

## Money-First Scores
- Pain: 4
- Spend: 1
- Reachability: 2
- Timing: 2
- Buildability: 2

## Source Classes
- github
- forum

## Paid Wedge
Unclear; telemetry integrity pain is visible, but there is no direct public proof that teams pay for external log diagnostics.

## Distribution Channel
Likely report or CLI for UAV operators and integrators, but acquisition requires direct operator validation.

## Private Data Barrier
private-data-required

## OSS Commoditization Risk
medium

## Product Shape
report

## Pricing Hypothesis
unclear

## Do Not Build Until
At least 3 operators share representative logs for analysis, or 1 integrator asks for a paid telemetry integrity review.

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
Watchlisted. Do not build until representative private-log access and a paid review signal are confirmed.
