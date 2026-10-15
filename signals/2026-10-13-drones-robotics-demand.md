# 2026-10-13 drones-robotics-demand

- Source date range: 2026-03-07 to 2026-10-13
- Family: `drones-robotics-demand`
Signal type: `operational-risk`
Source class: `github`
Evidence label: `M2 repeated pain`
Labels: `H hypothesis`, `M2 repeated pain`, `M4 workaround evidence`
Notes: Degla is a launch seed for autonomous drone execution, while ArduPilot issues and docs continue to show telemetry and failsafe pain. The validation path still depends on operator-specific logs and safety trust, so it stays watchlisted.
- Topic family: `drones-robotics-demand`

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://www.ycombinator.com/companies/degla-inc | 2026-10-13 crawl | company-launch | launch | H hypothesis | Degla is a launch seed for multi-drone mission execution, not demand proof by itself. |
| https://github.com/ArduPilot/ardupilot/issues/33017 | 2026-05-10 | operational-risk | github | M2 repeated pain | SIM_RC_FAIL still does not produce the expected virtual failsafe behavior in SITL. |
| https://github.com/ArduPilot/ardupilot/issues/32905 | 2026-04-24 | operational-risk | github | M2 repeated pain | Users still want native DShot/BDShot telemetry error counters for ESC-link monitoring. |
| https://github.com/ArduPilot/ardupilot_wiki/blob/master/sub/source/docs/failsafe-landing-page.rst | 2026-10-13 crawl | workaround-economy | docs | M4 workaround evidence | The failsafe docs show the amount of configuration and mode-specific testing operators still have to perform. |
| https://github.com/ArduPilot/ardupilot_wiki/blob/master/planner/source/docs/mission-planner-telemetry-logs.rst | 2026-10-08 crawl | workaround-economy | docs | M4 workaround evidence | Telemetry logs are still manually recorded and replayed for analysis. |
- Topic family: `drones-robotics-demand`

## Sources
- `https://www.ycombinator.com/companies/degla-inc`
  - Signal: `company-launch`
  - Class: `launch`
  - Label: `H hypothesis`
  - Note: Degla is a launch seed for multi-drone mission execution, not demand proof by itself.
- `https://github.com/ArduPilot/ardupilot/issues/33017`
  - Signal: `operational-risk`
  - Class: `github`
  - Label: `M2 repeated pain`
  - Note: SIM_RC_FAIL still does not produce the expected virtual failsafe behavior in SITL.
- `https://github.com/ArduPilot/ardupilot/issues/32905`
  - Signal: `operational-risk`
  - Class: `github`
  - Label: `M2 repeated pain`
  - Note: Users still want native DShot/BDShot telemetry error counters for ESC-link monitoring.
- `https://github.com/ArduPilot/ardupilot_wiki/blob/master/sub/source/docs/failsafe-landing-page.rst`
  - Signal: `workaround-economy`
  - Class: `docs`
  - Label: `M4 workaround evidence`
  - Note: The failsafe docs show the amount of configuration and mode-specific testing operators still have to perform.
- `https://github.com/ArduPilot/ardupilot_wiki/blob/master/planner/source/docs/mission-planner-telemetry-logs.rst`
  - Signal: `workaround-economy`
  - Class: `docs`
  - Label: `M4 workaround evidence`
  - Note: Telemetry logs are still manually recorded and replayed for analysis.
