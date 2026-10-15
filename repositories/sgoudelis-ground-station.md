# sgoudelis/ground-station

- Repository: https://github.com/sgoudelis/ground-station
- Review date: 2026-10-01
- Current commit reviewed: `430d4aa774a58df46ed3290782dbcde8ea2f1e3f`
- Commit date: 2026-10-01T05:47:06+03:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `satellites-space-systems`, especially session lifecycle management, internal observation isolation, antenna/SDR control, and scheduled observation state. The reusable mechanism is the explicit session-and-tracker envelope around SDR ownership so automated observations can survive restarts and remain separate from human sessions.

## Verified Flow

`SessionService.configure_sdr` writes session configuration and registers the SDR relationship in `SessionTracker` -> `SessionService.start_streaming` asks the process manager to start or join the worker and unregisters the relationship if startup fails -> `SessionService.register_internal_observation` synthesizes an internal session ID, registers the observation as internal, configures the SDR, and starts streaming -> `SessionTracker` keeps separate maps for SDR ownership, VFO selection, metadata, and internal-session membership -> `cleanup_sdr_session` and `cleanup_internal_observation` stop the worker, clear tracker state, and remove the session/configuration entry -> the backend tests verify internal-session registration, metadata, SDR/VFO mapping, isolation from user sessions, and cleanup behavior -> the broader backend and frontend suites cover tracker slots, session routing, and hardware/status UI behavior.

- E1 source verified: `backend/session/service.py::SessionService.configure_sdr`, `start_streaming`, `register_internal_observation`, and `cleanup_internal_observation` implement the session lifecycle envelope for automated observations.
- E1 source verified: `backend/session/tracker.py::SessionTracker` maintains separate maps for SDR ownership, VFO selection, metadata, and internal-session membership.
- E1 source verified: `backend/common/appconfig.py::load_app_config` and `DEFAULT_APP_CONFIG` define the runtime settings used by the backend/session stack.
- E2 test verified: `backend/tests/test_session_internal_observations.py` verifies registration, metadata, SDR/VFO mapping, user-vs-internal isolation, counting, unregistration, and cleanup.
- E2 test verified: `backend/tests/test_tracker_runner_slots.py` verifies tracker-slot allocation, stop behavior, orphan repair, and observation-slot isolation from target-slot limits.
- E2 test verified: `backend/tests/test_sdrtakeover.py` verifies internal-observation-aware client conflict reporting.

## Architecture

Principal components:

- `backend/session/service.py` for the façade that coordinates configuration, worker startup, and cleanup.
- `backend/session/tracker.py` for the in-memory runtime model of sessions, SDR ownership, VFO state, metadata, and internal observations.
- `backend/common/appconfig.py` for runtime configuration defaults and persisted settings.
- The backend test suite for session lifecycle, tracker slot allocation, and internal observation isolation.
- The frontend test suite and e2e flows for UI/state surfaces around passes, hardware, and navigation.

Most interesting mechanism: internal observation sessions are first-class runtime objects. They are tagged as internal, mapped to SDRs and VFOs, and cleaned up through the same service boundary that handles human sessions, so automatic observations do not leak into user state or vice versa.

Baseline comparison: a conventional ground-station UI might keep only a flat list of connected clients. This repo makes session identity, SDR ownership, and observation scope explicit, which is the part that survives beyond the UI.

## Reuse Guidance

Reusable:

- Model automated observations as internal sessions with explicit metadata and ownership.
- Keep session configuration, tracker ownership, and worker lifecycle separate but coordinated through one façade.
- Maintain separate lifecycle cleanup paths for internal observations and user sessions.
- Use tests that assert isolation, slot accounting, and orphan cleanup.

Do not copy:

- Do not copy the full frontend or decoder surface if you only need the session lifecycle pattern.
- Do not treat the tracker maps as durable storage; they are runtime coordination state.
- Do not assume the current tests validate a live SDR/rotator field deployment.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The repository has a very large backend and frontend test surface plus e2e coverage.
- Internal observations have explicit isolation tests and slot-accounting tests.
- The app is actively maintained, with current commits and release activity.

Experimental or incomplete for our needs:

- The core session tracker is an in-memory runtime model, not a persistence layer.
- The strongest evidence is session and UI behavior, not a live field exercise with real SDR hardware.
- Several paths remain hardware-dependent and are therefore harder to validate in CI.

Hidden costs and failure modes:

- Session cleanup must stay aligned with the process manager or the runtime can leak stale ownership.
- The internal-session model is only as good as the caller's cleanup discipline.
- Hardware-dependent state can diverge from the simulated or mocked test environment.

Adoption experiment:

Run an internal observation through connect, stream, stop, and cleanup, then restart the backend and confirm the session tracker and observation flags recover coherently without leaking the internal observation into the normal user-session view.

## Candidate Patterns

- `Evidence-Carrying Execution Envelopes`
- `internal observation session envelope`
- `session-to-SDR ownership façade`
