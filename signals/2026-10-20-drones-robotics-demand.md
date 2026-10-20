# 2026-10-20 drones-robotics-demand

- Source date range: 2026-05-10 to 2026-10-20
- Family: `drones-robotics-demand`
- Signal type: `operational-risk`
- Source class: `github`
- Evidence label: `M2 repeated pain`
- Labels: `H hypothesis`, `M2 repeated pain`, `M4 workaround evidence`
- Signal types: `company-launch`, `operational-risk`, `workaround-economy`
- Source classes: `launch`, `github`, `docs`
- Evidence labels: `H hypothesis`, `M2 repeated pain`, `M4 workaround evidence`
- Notes: Degla is a launch seed for natural-language multi-drone execution. ArduPilot still shows recurring SITL and failsafe pain, but buyers likely keep the diagnostics internal unless logs are easy to share.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://www.ycombinator.com/companies/degla-inc | 2026-10-19 crawl | company-launch | launch | H hypothesis | YC profile confirms the autonomy positioning but not buyer willingness to pay for an external review. |
| https://github.com/ArduPilot/ardupilot/issues | 2026-10-20 crawl | operational-risk | github | M2 repeated pain | The issue feed still shows SITL, logging, and failsafe pain across the stack. |
| https://github.com/ArduPilot/ardupilot/issues/33017 | 2026-05-10 issue | operational-risk | github | M2 repeated pain | SIM_RC_FAIL does not produce the expected virtual failsafe behavior while SITL is running. |
| https://github.com/ArduPilot/ardupilot/issues/32795 | 2026-04-16 issue | operational-risk | github | M2 repeated pain | Battery failsafe behavior in SITL appears unsafe and inconsistent with documentation. |
| https://github.com/ArduPilot/ardupilot_wiki/blob/master/plane/source/docs/advanced-failsafe-configuration.rst | 2026-10-17 crawl | workaround-economy | docs | M4 workaround evidence | The failsafe configuration docs explain a complex testing and scripting workflow around failures. |
