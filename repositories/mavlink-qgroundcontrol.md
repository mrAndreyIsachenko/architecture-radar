# mavlink/qgroundcontrol

- Repository: https://github.com/mavlink/qgroundcontrol
- Review date: 2026-08-02
- Current commit reviewed: `de77da5f84aa95a8dcafd314eb45072e6810dfe6`
- Commit date: 2026-08-01T16:49:48-07:00
- Branch: `master`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `drones-robotics-autonomy`: mission management, onboard log recovery, telemetry observability, and cancel-safe operator workflows.

## Verified Flow

Active vehicle -> `OnboardLogController` -> log list retrieval over messages or FTP -> selected log download to a directory -> cancellation or vehicle disconnect tears down state and removes partial files -> tests verify message transport fallback, FTP fallback, cancel, and disconnect behavior.

- E1 source verified: `src/AnalyzeView/OnboardLogs/OnboardLogController.cc` chooses message or FTP transport, reconnects on active-vehicle changes, and cleans up download state.
- E1 source verified: `test/AnalyzeView/OnboardLogDownloadTest.cc` exercises list completion, download, cancel, vehicle disconnect, erase-all, and FTP fallback.
- E1 source verified: `test/AnalyzeView/MavlinkLogTest.cc` verifies lost-log cleanup, save-on-arm behavior, and temp-file deletion.
- E1 source verified: `src/MissionManager/*` contains the mission-planning and mission-item system that sits beside the log analysis path.

## Architecture

Principal components:

- Onboard log controller with transport selection and retry logic.
- FTP and message-based log retrieval.
- QML-facing list model and test scaffolding.
- Mission manager and log analysis subsystems in the larger app.

Most interesting mechanism: the controller is cancel-safe and teardown-safe. It explicitly tears down in-progress downloads when the active vehicle changes, which is the right shape for operator-facing long-running telemetry jobs.

Baseline comparison: a simple ground station would just download logs and hope the vehicle stays connected. QGroundControl treats transport fallback, vehicle churn, and partial-file cleanup as first-class concerns.

## Reuse Guidance

Reusable:

- Keep cancel and disconnect paths as explicit test cases for long-running downloads.
- Fall back between log transports instead of assuming one channel will always work.
- Remove partial artifacts when the active data source disappears.

Do not copy:

- Do not copy the GUI-heavy surface as the mechanism.
- Do not assume download success unless teardown and cancellation are also exercised.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Integration tests cover the operational edge cases that matter here.
- The controller actively manages lifecycle and teardown.
- The app supports both message and FTP retrieval for logs.

Experimental or incomplete for our needs:

- The review stayed on one controller path and one log test family.
- Mission planning mechanics are broader than the verified log-recovery path.

Hidden costs and failure modes:

- Active-vehicle churn can invalidate in-progress work.
- Partial downloads require explicit file cleanup.
- Multiple transports increase state-machine complexity.

Adoption experiment:

Apply the same cancel-safe pattern to an internal telemetry fetcher: if the source disappears mid-download, tear down all state, delete the partial file, and assert the model returns to idle.

## Candidate Patterns

- `transport-fallback log recovery pipeline`
- `cancel-safe telemetry teardown`
