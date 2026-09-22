# Drones Robotics Demand Signals 2026-09-22

- Family: `drones-robotics-demand`
- Source date range: `2026-05-10` to `2026-09-22`
- Signal type: `company-launch`
- Source class: `launch`
- Signal types: `company-launch`, `operational-risk`, `workaround-economy`
- Source classes: `launch`, `github`, `docs`
- Evidence labels: `H hypothesis`, `M2 repeated pain`, `M4 workaround evidence`
- Labels: `H hypothesis`, `M2 repeated pain`, `M4 workaround evidence`
- Notes: Degla is a useful launch seed, and ArduPilot still shows real failsafe pain, but the buyer path remains weak because the useful evidence often sits behind operator logs and safety review context.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://www.ycombinator.com/companies/degla-inc | 2026-09-22 crawl | company-launch | launch | H hypothesis | Degla is a launch seed for natural-language multi-drone mission execution. |
| https://github.com/ArduPilot/ardupilot/issues/33017 | 2026-05-10 | operational-risk | github | M2 repeated pain | SIM_RC_FAIL does not produce virtual failsafe behavior in SITL as expected. |
| https://github.com/ArduPilot/ardupilot_wiki/blob/master/sub/source/docs/radio-failsafe.rst | 2026-09-16 crawl | workaround-economy | docs | M4 workaround evidence | The failsafe docs show how much operator-specific configuration and testing is still required. |
