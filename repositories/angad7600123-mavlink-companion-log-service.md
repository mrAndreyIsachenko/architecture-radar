# angad7600123/Mavlink-companion-log-service

- Repository: https://github.com/angad7600123/Mavlink-companion-log-service
- Review date: 2026-08-05
- Current commit reviewed: `8326e3366ca696632167b79826fe4afe30a1341e`
- Commit date: 2026-07-13T20:59:58+05:30
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `drones-robotics-autonomy`, specifically telemetry observability, mission recovery, and safe log archival. The reusable mechanism is the streaming download and recovery logic, not the companion app shell around it.

## Verified Flow

`DroneLogService::run` service loop -> heartbeat/arm/disarm events from `FlightMonitor` -> download state machine transitions between wait/connect/archive/reconnect states -> `StreamDownloadSession::run` requests log chunks, tracks received ranges, fills gaps, computes hashes, and detects overlaps -> companion protocol tests validate status and job acknowledgments -> range and coverage tests validate completion behavior.

- E1 source verified: `src/DroneLogService.cpp`, the service loop initializes storage/database, starts the companion UDP server if enabled, drains companion commands, and runs the state machine until shutdown.
- E1 source verified: `src/DroneLogService.cpp`, connection loss is suppressed during active archival so long downloads are not torn down mid-cycle.
- E1 source verified: `src/StreamDownloadSession.cpp`, the session drains queued chunks, writes them to the requested range, tracks received bytes, computes hashes, and requests merged gap fills when progress stalls.
- E1 source verified: `src/StreamDownloadSession.cpp`, overlap conflicts can abort the session and short EOF can complete the range cleanly.
- E1 source verified: `include/mcls/StreamDownloadSession.hpp`, the session result records success/failure, range coverage, hash state, and probe metadata.
- E2 test verified: `tests/test_received_ranges.cpp::ReceivedRangesTest.DetectsGapsAndCompletion` verifies range-gap detection and completion.
- E2 test verified: `tests/test_chunk_coverage.cpp::ChunkCoverageTrackerTest.DetectsOverlapConflict` verifies overlap detection.
- E2 test verified: `tests/test_companion_protocol.cpp::CompanionProtocol.StatusNeverExceedsBudget` verifies the status envelope stays within the response budget.
- E2 test verified: `tests/test_companion_protocol.cpp::CompanionProtocol.JobAckAlreadyRunningIsSuccess` verifies idempotent job-ack behavior.

## Architecture

Principal components:

- `DroneLogService`: main lifecycle and state machine for log archiving.
- `StreamDownloadSession`: byte-range streaming, gap fill, hashing, and conflict detection.
- `CompanionProtocol` and `CompanionUdpServer`: control-plane status and job requests.
- Storage/database/log parser helpers: persistence and telemetry bookkeeping.

Most interesting mechanism: the log session is not a blind file pull. It tracks received byte ranges, re-requests only the gaps, and treats overlap conflicts and short EOF as first-class outcomes. That makes archival resilient to dropped chunks and partial transport failure.

Baseline comparison: a conventional downloader would either restart the whole transfer or trust a single sequential stream. This implementation keeps coverage state and resumes only the missing ranges.

## Reuse Guidance

Reusable:

- Use range coverage tracking when a transfer may arrive out of order or with holes.
- Treat “already running” and “short EOF” as valid states, not exceptional user-facing failures.
- Keep the operator-facing protocol separate from the download engine so status and recovery remain inspectable.

Do not copy:

- Do not copy the Android or companion-service shell as the reusable mechanism.
- Do not assume the download session is fully generic; it is tuned to MAVLink log chunk semantics.
- Do not treat the protocol budget as an optional nicety; it is part of the operator contract.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The state machine and streaming session are explicit and test-backed.
- The companion protocol has budget and idempotency tests.
- Range coverage and overlap conflict handling are directly tested.

Experimental or incomplete for our needs:

- The review did not run the C++ test suite locally.
- Recovery depends on MAVLink log semantics and FC behavior, not just transport behavior.
- The archival flow is companion-service specific even if the recovery mechanism is reusable.

Hidden costs and failure modes:

- Range recovery adds complexity around gap requests, overlap conflicts, and hashing state.
- Transport reconnect policy depends on download classifications and can be hard to tune.
- The state machine has many states, so regressions can hide in transitions.

Adoption experiment:

Reuse the range-coverage loop in a separate telemetry downloader, inject dropped chunks and duplicate chunks, and confirm that the receiver can finish the range without restarting the whole transfer or accepting overlapped data.

## Candidate Patterns

- `range-tracked streaming log recovery`
- `idle gap fill request loop`
