# 2026-11-17 drones-robotics-demand

- Source date range: 2026-03-02 to 2026-11-17
- Family: `drones-robotics-demand`
- Signal type: `operational-risk`
- Source class: `github`
- Labels: `M2 repeated pain`, `M4 workaround evidence`, `H hypothesis`
- Notes: Degla is a fresh launch seed for drone autonomy, while ArduPilot docs and issues still expose repeated telemetry and failsafe pain. Public evidence still stops short of a paid external diagnostic wedge.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://www.ycombinator.com/companies/degla-inc | 2026-11-17 crawl | company-launch | launch | H hypothesis | Degla is a launch seed for multi-drone mission execution, not demand proof by itself. |
| https://github.com/ArduPilot/ardupilot/issues/32351 | 2026-03-02 | operational-risk | github | M2 repeated pain | Bidirectional DShot telemetry still fails to start on some AM32 ESCs. |
| https://github.com/ArduPilot/ardupilot/issues/34219 | 2026-08-30 | operational-risk | github | M2 repeated pain | Early motor-interlock release can produce a hard-start in TRAD_HELI setups. |
| https://github.com/ArduPilot/ardupilot_wiki/blob/master/rover/source/docs/rover-failsafes.rst | 2026-11-12 crawl | workaround-economy | docs | M4 workaround evidence | The failsafe docs enumerate many operator settings because telemetry and GCS loss still need explicit handling. |
| https://github.com/ArduPilot/MethodicConfigurator/blob/master/GUIDE_log_analysis.md | 2026-10-15 crawl | optimization-gap | docs | M4 workaround evidence | The guide shows log analysis is a manual workflow for detecting ESC and telemetry problems. |

## Sources
- `https://www.ycombinator.com/companies/degla-inc`
- `https://github.com/ArduPilot/ardupilot/issues/32351`
- `https://github.com/ArduPilot/ardupilot/issues/34219`
- `https://github.com/ArduPilot/ardupilot_wiki/blob/master/rover/source/docs/rover-failsafes.rst`
- `https://github.com/ArduPilot/MethodicConfigurator/blob/master/GUIDE_log_analysis.md`
