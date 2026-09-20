# ArduPilot Demand Signals 2026-09-15

- Family: `drones-robotics-demand`
- Source date range: 2026-03-01 to 2026-08-31
- Signal type: `operational-risk`
- Source class: `forum`
- Evidence labels: `M2 repeated pain`, `M4 workaround evidence`
- Labels: `M2 repeated pain`, `M4 workaround evidence`
- Notes: ArduPilot shows recurring telemetry and failsafe workarounds, but the private-log barrier and buyer path are still weak.

## Sources
- `M4 workaround evidence` | `workaround-economy` | `forum` | https://discuss.ardupilot.org/t/gsoc-2026-alda-ai-assisted-log-diagnosis-demo-v0-1-dijo/143000 | The ALDA demo shows people are trying to automate log diagnosis because manual review is still painful.
- `M4 workaround evidence` | `workaround-economy` | `forum` | https://discuss.ardupilot.org/t/introducing-an-ai-assisted-log-diagnosis-engine-tracing-root-causes-in-bin-files/142646 | The log-diagnosis project shows recurring manual analysis of flight logs.
- `M2 repeated pain` | `operational-risk` | `github` | https://github.com/ArduPilot/ardupilot/issues/32905 | Native DShot telemetry error counters are requested because current diagnostics are weak.
- `M2 repeated pain` | `operational-risk` | `github` | https://github.com/ArduPilot/ardupilot/issues/28612 | Release issue lists keep accumulating telemetry, failsafe, and hardware-debug work.
- `M2 repeated pain` | `operational-risk` | `github` | https://github.com/ArduPilot/ardupilot/blob/master/AntennaTracker/ReleaseNotes.txt | Release notes show repeated fixes around failsafe, telemetry, and flight-control behavior.
