# Drones Robotics Demand Signals - 2026-10-06

Date: 2026-10-06
Family: `drones-robotics-demand`
Signal type: `operational-risk`
Source class: `github`
Labels: `M2 repeated pain`, `M4 workaround evidence`, `H hypothesis`
Notes: This note groups Degla as a launch seed with ArduPilot telemetry and failsafe docs that still require manual operator checks.

| Source | URL | Date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|---|
| Degla YC profile | https://www.ycombinator.com/companies/degla-inc | 2026-10-06 crawl | company-launch | launch | H hypothesis | Launch seed only; it is a timing signal for multi-drone autonomy, not direct spend proof. |
| ArduPilot issues page | https://github.com/ArduPilot/ardupilot/issues | 2026-10-03 crawl | operational-risk | github | M2 repeated pain | Current issue feed still shows SITL, telemetry, and failsafe debugging pain. |
| Rover failsafes docs | https://github.com/ArduPilot/ardupilot_wiki/blob/master/rover/source/docs/rover-failsafes.rst | 2026-09-10 crawl | workaround-economy | docs | M4 workaround evidence | Failsafe docs show the amount of operator-specific configuration and testing still required. |
| Radio failsafe docs | https://github.com/ArduPilot/ardupilot_wiki/blob/master/sub/source/docs/radio-failsafe.rst | 2026-09-22 crawl | workaround-economy | docs | M4 workaround evidence | The docs still teach manual checks for transmitter and telemetry loss behavior. |

## Notes
- M2 repeated pain: ArduPilot issue threads keep surfacing telemetry and failsafe gaps.
- M4 workaround evidence: the docs expose a manual configuration-and-testing workflow, not a turnkey paid review market.
- Degla remains a launch seed; it is not demand proof by itself.
