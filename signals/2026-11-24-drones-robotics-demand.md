# 2026-11-24 drones-robotics-demand

- Source date range: 2026-01-22 to 2026-11-24
- Family: `drones-robotics-demand`
- Signal type: `company-launch`
- Source class: `launch`
- Labels: `M2 repeated pain`, `M4 workaround evidence`, `H hypothesis`
- Topic family: `drones-robotics-demand`

Notes: Degla is a launch seed for autonomy software, while ArduPilot still exposes recurring log, replay, and failsafe work that operators must manage manually.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://www.ycombinator.com/companies/industry/drones | 2026-11-24 crawl | company-launch | launch | H hypothesis | The YC drones page is a launch seed showing Degla's mission-language autonomy positioning, not demand proof by itself. |
| https://github.com/ardupilot/ardupilot/issues | 2026-11-24 crawl | operational-risk | github | M2 repeated pain | The live issue feed still shows failsafe, telemetry, and mission-planning bugs. |
| https://github.com/ArduPilot/ardupilot_wiki/blob/master/common/source/docs/common-downloading-and-analyzing-data-logs-in-mission-planner.rst | 2026-11-23 | workaround-economy | docs | M4 workaround evidence | The replay logging docs show users must enable special logging to diagnose EKF/AHRS issues by hand. |
| https://github.com/ArduPilot/ardupilot/blob/master/libraries/AP_Logger/AP_Logger.cpp | 2026-11-23 | workaround-economy | docs | M4 workaround evidence | The logger parameters document the manual setup required for replay-quality logs. |
| https://github.com/ArduPilot/ardupilot/issues/31989 | 2026-01-22 | operational-risk | github | M2 repeated pain | Users still report replay/logging pain around LOG_FILE_DSRMROT and recurring EKF troubleshooting. |
