# librespacefoundation/satnogs-network

- Repository: https://gitlab.com/librespacefoundation/satnogs/satnogs-network
- Review date: 2026-11-18
- Current commit reviewed: `8f5a9b6ee19311e4bceb94ef42ec219d2ec18c99`
- Commit date: 2026-11-18T02:59:43+02:00
- Branch: `master`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: selected

## Problem Fit

This repository informs `satellites-space-systems`, especially pass-window scheduling, future-observation refresh, station eligibility, and delayed observation cleanup. The reusable mechanism is the network-side materialization of future observation state with explicit station/client gates.

## Verified Flow

`ObservationManager.is_future` and `StationManagerQueryset.connected_and_located` define the scheduling slice -> `has_schedule_perms` and `has_perm_to_schedule_on_station` gate who can schedule and where -> `update_future_observations_with_new_tle_sets` refreshes future observations only when the station/client version and hard-limit filters allow it -> `update_future_observations_with_new_transmitter_details` revalidates transmitter metadata against station range and bulk-updates the future rows -> `clean_observations` and `zip_audio_files` process stale audio and archive batches -> the permission tests verify the schedule gate for owners, operators, moderators, and superusers.

- E1 source verified: `network/base/managers.py::ObservationManager.is_future`, `StationManagerQueryset.connected`, `located`, and `connected_and_located` define the connected, located, and future slices used by the scheduling flow.
- E1 source verified: `network/base/perms.py::has_schedule_perms`, `has_perm_to_schedule_on_station`, and `get_schedule_permissions_per_station` gate scheduling by ownership, availability, and role.
- E1 source verified: `network/base/tasks.py::update_future_observations_with_new_tle_sets` and `::update_future_observations_with_new_transmitter_details` refresh future observations with cached TLE and transmitter data before the scheduled pass.
- E1 source verified: `network/base/tasks.py::clean_observations`, `::process_audio`, and `::zip_audio_files` handle post-observation cleanup and archive batching.
- E2 test verified: `network/base/tests.py::test_user_can_schedule` and `::test_user_can_schedule_on_station` cover the scheduling permission matrix for owners, operators, moderators, superusers, and testing/non-testing stations.

## Architecture

Principal components:

- Django queryset managers for connected, located, and future observation slices.
- Permission helpers for schedule eligibility and station-level access control.
- Celery tasks for future-observation refresh, audio cleanup, and archive batching.
- Model factories and tests that encode the scheduling matrix.

Most interesting mechanism: the scheduler does not treat future observations as static rows. It re-materializes TLE and transmitter data for eligible future observations, while the permission layer narrows who can schedule and on which station based on connection and station state.

Baseline comparison: a simpler scheduler would only validate the user once and leave future rows stale until the observation starts. This repository keeps the future schedule and transmitter metadata synchronized ahead of the pass window.

## Reuse Guidance

Reusable:

- Keep a dedicated future-observation refresh task instead of mutating schedule rows on demand.
- Filter by station connectivity, location, and client compatibility before materializing updates.
- Batch refreshes with `bulk_update` once the eligibility set is known.
- Encode the permission matrix in tests so station ownership and role-based scheduling stay explicit.

Do not copy:

- Do not copy the SatNOGS-specific database/API assumptions without the same delayed-connectivity workflow.
- Do not treat cache locks and bulk updates as a substitute for actual operational validation.
- Do not rely on the current client-version exclusions without rechecking them against your own fleet.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The scheduling matrix is explicit and test-covered.
- Future-observation updates are separated from post-observation cleanup.
- The queryset layer gives a clear model of connected and located stations.

Experimental or incomplete for our needs:

- The reviewed source does not prove a live scheduler run against the current backend or API.
- Client-version exclusions and hard-limit filters are policy choices that need corpus-specific tuning.
- `pytest` was not available in this runner, so the Python suite was source-verified but not executed here.

Hidden costs and failure modes:

- The `now()+10 minutes` threshold can suppress legitimate near-term updates.
- Cache-backed lock behavior can drop work if the backing cache is unavailable or misconfigured.
- `bulk_update` can leave stale future rows if upstream TLE or transmitter data is delayed or inconsistent.

Adoption experiment:

Run the network scheduler against a live station and API backend, then verify that future observations get updated once, skip excluded station/client combinations, and remain consistent after a transient cache or API failure.

## Candidate Patterns

- `future-observation materialization gate`
- `cache-locked observation refresh`
- `station-eligibility scheduling matrix`
