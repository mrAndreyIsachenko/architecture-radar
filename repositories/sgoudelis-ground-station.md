# sgoudelis/ground-station

- Repository: https://github.com/sgoudelis/ground-station
- Review date: 2026-11-27
- Current commit reviewed: `83aa44f674014189036762f1f59fdafd38b5702c`
- Commit date: 2026-11-27T13:16:05+02:00
- Branch: `main`
- Previous commit reviewed: `430d4aa774a58df46ed3290782dbcde8ea2f1e3f`
- Material changes since previous review: current head refreshes the release-note surface while keeping the same persisted orbital-sync snapshot and observation-session envelope intact.
- Decision: selected

## Problem Fit

This repository informs `satellites-space-systems`, especially delayed-connectivity command and telemetry loops, observation scheduling, and restart recovery for orbital sync state. The reusable mechanism is the explicit sync-state and persistence envelope around source refreshes so automated observations can survive restarts and remain separate from human sessions.

## Verified Flow

`logic.synchronize_satellite_data_internal` acquires `_sync_lock`, emits a sync-state object, fetches each enabled source in order, and persists the resulting `SatelliteSyncState` -> `persist.save_orbital_sync_state` stores the terminal snapshot in `TrackingState` -> `persist.load_orbital_sync_state` rehydrates the saved snapshot on startup -> `startup.py` loads that snapshot before the background task manager starts -> `syncstate.py` projects the phase, source status, and progress counters into a UI-facing model -> the backend tests cover successful sync, source-failure persistence, and empty-source handling.

- E1 source verified: `backend/tlesync/logic.py::synchronize_satellite_data_internal` drives the ordered refresh and progress-tracking path.
- E1 source verified: `backend/tlesync/persist.py::load_orbital_sync_state` and `save_orbital_sync_state` persist and restore the terminal orbital-sync snapshot.
- E1 source verified: `backend/server/startup.py` hydrates the persisted sync state on startup before the background scheduler begins work.
- E1 source verified: `backend/celestial/syncstate.py` projects sync phase, source status, and progress counters into a UI-facing model.
- E2 test verified: `backend/tests/testsync.py` verifies source success, fetch failure persistence, and empty-source handling.
- E2 test verified: `backend/tests/testperformancemonitor.py` exercises the operational monitoring surface around the sync loop.

## Architecture

Principal components:

- `backend/tlesync/logic.py` for the ordered orbital-sync loop and source iteration.
- `backend/tlesync/persist.py` for snapshot persistence and restoration.
- `backend/server/startup.py` for startup hydration before background task execution.
- `backend/celestial/syncstate.py` for the projected status model.
- The backend tests for ordered refresh, failure persistence, and empty-source behavior.

Most interesting mechanism: sync state is materialized as an explicit snapshot, persisted, and rehydrated before the scheduler starts. That makes the operational envelope recoverable across restart boundaries instead of relying on a transient progress bar.

Baseline comparison: a conventional ground-station app might keep the progress indicator in memory and recompute only from the current screen state. This repo makes the sync lifecycle explicit, which is the part that survives beyond the UI.

## Reuse Guidance

Reusable:

- Model automated sync as an explicit snapshot with a persisted terminal state.
- Keep source fetch, persistence, and startup hydration separate but coordinated through one flow.
- Preserve the distinction between progress projection and durable state.
- Use tests that assert failure persistence, hydration, and empty-source behavior.

Do not copy:

- Do not copy the entire UI or observation surface if you only need the sync-state mechanism.
- Do not treat the projected sync-state object as the source of truth; the persisted snapshot is.
- Do not assume the current tests validate a live SDR, antenna, or ground-station deployment.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The repository has a focused backend test surface around orbital sync and operational monitoring.
- Sync persistence and startup hydration are source-backed instead of implied.
- The current head keeps the same persistence boundary while refreshing the release notes.

Experimental or incomplete for our needs:

- The strongest evidence is ordered sync and persistence behavior, not a live field exercise with real hardware.
- The current run still does not validate a rotator, SDR, or antenna deployment.
- Several paths remain hardware-dependent and are therefore harder to validate in CI.

Hidden costs and failure modes:

- Snapshot hydration must stay aligned with the persisted state model or the runtime can present stale progress.
- Source refresh ordering must remain stable or the projected sync-state can drift from the actual fetch loop.
- Hardware-dependent state can diverge from the simulated or mocked test environment.

Adoption experiment:

Run a live orbital-sync session through source refresh, persistence, restart, and rehydration, then confirm the projected sync state matches the persisted snapshot and does not regress to a stale phase after restart.

## Candidate Patterns

- `Evidence-Carrying Execution Envelopes`
- `persisted orbital sync snapshot`
- `sync-state progress tracker`
