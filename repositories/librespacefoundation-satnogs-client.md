# librespacefoundation/satnogs-client

- Repository: https://gitlab.com/librespacefoundation/satnogs/satnogs-client
- Review date: 2026-11-18
- Current commit reviewed: `363856875948ae5dd04cd03b19f9b39cc4fdf830`
- Commit date: 2026-10-02T13:00:48+03:00
- Branch: `master`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: selected

## Problem Fit

This repository informs `satellites-space-systems`, especially pass-window execution, Doppler and rotator tracking, artifact capture, and delayed network upload. The reusable mechanism is the observation runner that turns a scheduled job into a serialized, recoverable capture session.

## Verified Flow

`scheduler/tasks.py::spawn_observer` receives a job payload, parses the TLE and end time, and serializes the run behind `OBSERVER_LOCK` -> `Observer.setup` resolves the station location, output paths, receiver device, and tracking inputs -> `Observer.observe` optionally runs pre/post scripts, starts rotator and rig workers, starts the GNU Radio flowgraph, and waits until the observation end time -> `WorkerTrack` and `WorkerFreq` call `pinpoint`, `find_observation_pass_midpoint`, and Doppler-adjusted frequency logic while the pass is active -> `post_data` scans the output directory and uploads payload, waterfall, or demodulated data back to the network API, keeping or removing files based on the response -> `test_artifacts.py` and the Robot suite exercise artifact creation, startup, no-job, upload, rotator-flip, and concurrency behavior.

- E1 source verified: `satnogsclient/scheduler/tasks.py::spawn_observer`, `post_data`, `upload_observation_data`, and `get_jobs` implement the job intake, file upload, and job polling loop.
- E1 source verified: `satnogsclient/observer/observer.py::setup`, `observe`, `run_rot`, `run_rig`, and `poll_gnu_proc_status` implement the serialized observation session and cleanup path.
- E1 source verified: `satnogsclient/observer/worker.py::WorkerTrack` and `::WorkerFreq` implement the rotator and frequency tracking loops, including midpoint-based flip handling and Doppler adjustment.
- E1 source verified: `satnogsclient/observer/orbital.py::pinpoint` and `::find_observation_pass_midpoint` translate TLE and station geometry into tracking inputs.
- E2 test verified: `satnogsclient/tests/test_artifacts.py::test_artifacts` covers artifact creation from waterfall data.
- E2 test verified: `robot/testsuites/SatNOGS_client.robot` covers startup, job polling, observation completion, rotator flip behavior, upload posting, and concurrent observation serialization.

## Architecture

Principal components:

- Scheduler loop that polls the network API for observation jobs and posts completed data.
- Observer session that owns the capture lifecycle for one pass.
- Rotator and rig workers that update antenna direction and Doppler-corrected frequency.
- Artifact and file-posting helpers that upload results after the pass window.
- Robot and unit tests for startup and capture-path behavior.

Most interesting mechanism: the client serializes each observation session with a lock, computes pass geometry and midpoint-based flip behavior, then keeps capture, file creation, and upload in one end-to-end pass-bound loop.

Baseline comparison: a simpler ground-station client would run a decoder and leave the operator to manage job timing, tracking, and upload separately. This repository coordinates those steps as one observation session with explicit pass timing.

## Reuse Guidance

Reusable:

- Serialize observation runs with a lock when the radio chain cannot safely overlap jobs.
- Keep pass geometry and midpoint logic separate from the file-upload path.
- Stage output files first, then upload them to the remote API in a distinct post-run step.
- Preserve the distinction between audio, waterfall, and demodulated outputs when sending results upstream.

Do not copy:

- Do not copy the SatNOGS-specific radio assumptions without the same tracking and upload workflow.
- Do not assume file uploads are reliable enough to run inline with the capture loop.
- Do not rely on the current retry behavior for mission-critical uploads without stronger validation.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The observation runner is explicit about setup, capture, and cleanup phases.
- Rotator and rig tracking are isolated in their own workers.
- The Robot suite covers startup, job polling, and concurrency behavior.

Experimental or incomplete for our needs:

- The reviewed tests are present, but this runner could not execute them here because `pytest` is unavailable.
- Upload failures are logged, but the code does not aggressively retry or reconcile partial uploads in this review.
- Live radio, Hamlib, and API integration still need an operational run to prove the full pass loop.

Hidden costs and failure modes:

- A long observation monopolizes the lock and delays the next job.
- A bad `find_observation_pass_midpoint` result can disable antenna flip behavior.
- Upload failures can leave files on disk or in the incomplete directory, which is correct but operationally noisy.

Adoption experiment:

Run one real pass against a live API endpoint, then verify that the lock prevents overlap, the rotator and rig loops track through the pass, and the post-run file upload either succeeds or leaves a clearly recoverable artifact set.

## Candidate Patterns

- `serialized observation session`
- `pass-bound tracking and upload loop`
- `lock-gated job execution`
