# ArduPilot telemetry integrity notes

- Sources:
  - https://github.com/ArduPilot/ardupilot/issues/9752
  - https://github.com/ArduPilot/ardupilot/issues/27746
  - https://github.com/ArduPilot/ardupilot/issues/28807
  - https://github.com/ArduPilot/ardupilot/issues/32351
  - https://github.com/ArduPilot/ardupilot/issues/32905
- Date range: 2018-11-10 to 2026-04-24
- Family: drones-robotics-demand
- Signal type: operational-risk
- Labels: M2 repeated pain, M4 workaround evidence
- Notes: packet loss, lost ESC telemetry, and DShot start failures recur; users manually compare GCS output and logs to diagnose reliability.
