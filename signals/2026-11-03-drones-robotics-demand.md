# 2026-11-03 drones-robotics-demand

- Source date range: 2026-09-05 to 2026-11-03
- Family: `drones-robotics-demand`
- Signal type: `operational-risk`
- Source class: `github`
- Evidence labels: `M2 repeated pain`, `M4 workaround evidence`, `H hypothesis`
- Labels: `M2 repeated pain`, `M4 workaround evidence`, `H hypothesis`
- Notes: Degla is still only a launch seed, while ArduPilot issues and docs keep surfacing telemetry, replay, and failsafe friction. The workflow is real, but public money evidence is still too weak for selection.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://www.ycombinator.com/companies/degla-inc | 2026-11-03 crawl | company-launch | launch | H hypothesis | Degla is a launch seed for natural-language multi-drone mission execution, but launch status alone is not demand proof. |
| https://github.com/ArduPilot/ardupilot/issues/34365 | 2026-09-10 | operational-risk | github | M2 repeated pain | AP_Logger can silently disable SD-card logging when FAT32 FSINFO is stale. |
| https://github.com/ArduPilot/ardupilot/issues/33017 | 2026-06-2026 issue | operational-risk | github | M2 repeated pain | `SIM_RC_FAIL` still does not produce the expected virtual failsafe behavior in SITL. |
| https://github.com/ArduPilot/ardupilot/issues/31989 | 2026-01-22 | workaround-economy | github | M4 workaround evidence | Operators are already enabling replay-related logging and dealing with very large log files. |
| https://github.com/ArduPilot/ardupilot_wiki/blob/master/planner/source/docs/mission-planner-telemetry-logs.rst | 2026-11-03 crawl | workaround-economy | docs | M4 workaround evidence | Telemetry logs are a standard manual artifact in Mission Planner workflows. |
