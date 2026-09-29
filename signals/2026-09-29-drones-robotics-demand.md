# 2026-09-29 Drones / Robotics Demand Signals

- Family: `drones-robotics-demand`
- Source date range: 2026-09-29 crawl, with one launch seed and current ArduPilot issue/docs coverage.
- Signal type: `operational-risk`
- Source class: `github`
- Signal types: `company-launch`, `operational-risk`, `workaround-economy`
- Source classes: `launch`, `github`, `docs`
- Market evidence labels: `H hypothesis`, `M2 repeated pain`, `M4 workaround evidence`
- Labels: `H hypothesis`, `M2 repeated pain`, `M4 workaround evidence`
- Notes: Degla is still only a launch seed, while ArduPilot’s public issue and docs trail shows recurring failsafe and validation pain. The commercial path is still weak because the useful next test likely needs logs or hardware-adjacent validation.

## Sources

- `https://www.ycombinator.com/companies/degla-inc` | source class: `launch` | signal type: `company-launch` | evidence label: `H hypothesis` | note: YC launch page positions natural-language multi-drone mission execution, but it is only a discovery seed.
- `https://github.com/ArduPilot/ardupilot/issues/33017` | source class: `github` | signal type: `operational-risk` | evidence label: `M2 repeated pain` | note: SIM_RC_FAIL does not produce the expected virtual failsafe behavior while SITL is running.
- `https://github.com/ArduPilot/ardupilot/issues/32795` | source class: `github` | signal type: `operational-risk` | evidence label: `M2 repeated pain` | note: Battery failsafe behavior may not execute a valid fallback action in SITL.
- `https://github.com/ArduPilot/ardupilot_wiki/blob/master/sub/source/docs/radio-failsafe.rst` | source class: `docs` | signal type: `workaround-economy` | evidence label: `M4 workaround evidence` | note: The failsafe docs show how much operator-specific configuration and testing still remains.
- `https://github.com/ArduPilot/ardupilot_wiki/blob/master/common/source/docs/common-downloading-and-analyzing-data-logs-in-mission-planner.rst` | source class: `docs` | signal type: `workaround-economy` | evidence label: `M4 workaround evidence` | note: Log replay and analysis require explicit logging setup, which underscores the manual validation burden.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://www.ycombinator.com/companies/degla-inc | 2026-09-29 crawl | company-launch | launch | H hypothesis | YC launch page positions natural-language multi-drone mission execution, but it is only a discovery seed. |
| https://github.com/ArduPilot/ardupilot/issues/33017 | 2026-09-29 crawl | operational-risk | github | M2 repeated pain | SIM_RC_FAIL does not produce the expected virtual failsafe behavior while SITL is running. |
| https://github.com/ArduPilot/ardupilot/issues/32795 | 2026-09-29 crawl | operational-risk | github | M2 repeated pain | Battery failsafe behavior may not execute a valid fallback action in SITL. |
| https://github.com/ArduPilot/ardupilot_wiki/blob/master/sub/source/docs/radio-failsafe.rst | 2026-09-29 crawl | workaround-economy | docs | M4 workaround evidence | The failsafe docs show how much operator-specific configuration and testing still remains. |
| https://github.com/ArduPilot/ardupilot_wiki/blob/master/common/source/docs/common-downloading-and-analyzing-data-logs-in-mission-planner.rst | 2026-09-29 crawl | workaround-economy | docs | M4 workaround evidence | Log replay and analysis require explicit logging setup, which underscores the manual validation burden. |
