# drones-robotics-demand signal note, 2026-10-27

- Source date range: 2026-09-10 to 2026-10-27 crawl.
- Family: `drones-robotics-demand`
Signal type: `operational-risk`
Source class: `github`
Evidence label: `M2 repeated pain`
Labels: `M2 repeated pain`, `M4 workaround evidence`, `H hypothesis`
Notes: Degla is only a launch seed, while ArduPilot issues and docs still show telemetry and failsafe pain with private-log validation required for a commercial wedge.
- Topic family: `drones-robotics-demand`

## Sources

| Source | URL | Date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|---|
| Degla YC profile | https://www.ycombinator.com/companies/degla-inc | 2026-10-27 crawl | company-launch | launch | `H hypothesis` | Launch seed for natural-language multi-drone mission execution, not demand proof by itself. |
| ArduPilot issue 34365 | https://github.com/ArduPilot/ardupilot/issues/34365 | Opened Sep 2026 | operational-risk | github | `M2 repeated pain` | AP_Logger can silently disable SD card logging when FSINFO is stale. |
| ArduPilot issue 34226 | https://github.com/ArduPilot/ardupilot/issues/34226 | Opened Aug 2026 | operational-risk | github | `M2 repeated pain` | Mission Planner can show incorrect rxrssi even when RC failsafe is still triggered. |
| ArduPilot issue 32905 | https://github.com/ArduPilot/ardupilot/issues/32905 | Opened Apr 2026 | operational-risk | github | `M2 repeated pain` | Users still want native DShot and BDShot telemetry error counters for ESC-link monitoring. |
| ArduPilot telemetry logs wiki | https://github.com/ArduPilot/ardupilot_wiki/blob/master/planner/source/docs/mission-planner-telemetry-logs.rst | 2026-10-27 crawl | workaround-economy | docs | `M4 workaround evidence` | Docs explain manual telemetry logging, playback, and replay review for diagnosis. |
