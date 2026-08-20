# xberg-io/xberg

- Repository: https://github.com/xberg-io/xberg
- Review date: 2026-08-20
- Current commit reviewed: `531e0f7895e53f083c7d4f183123dea4f866e4eb`
- Commit date: 2026-08-19T13:31:23+02:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `document-ai-ocr`, especially batch extraction, environment diagnostics, and scan-aware routing. The reusable mechanism is the separation between extraction, host probing, batch-scoped concurrency, and scan-confidence gating.

## Verified Flow

`extract` and `extract_batch` expose the stable API -> `DEFAULT_ENGINE` delegates to engine internals -> `collect_batch` configures semaphore-bound batch execution and ordered result collection -> `with_batch_mode` marks the task-local batch context -> `doctor` probes configured backends and reports pass/warn/fail/skip verdicts -> `score_page` and `detect` compute scan confidence -> CLI tests verify the JSON timing envelope and backend validation behavior.

- E1 source verified: `crates/xberg/src/core/extract/mod.rs` exposes `extract` and `extract_batch` as the stable public extraction entry points.
- E1 source verified: `crates/xberg/src/core/extractor/batch.rs` implements `collect_batch`, `run_timed_extraction`, and ordered batch result handling with semaphore gating and cancellation-aware timeouts.
- E1 source verified: `crates/xberg/src/core/batch_mode.rs` uses tokio task-local storage to scope batch mode to the current future.
- E1 source verified: `crates/xberg/src/doctor/mod.rs` defines `ProbeStatus`, `DoctorCheck`, `DoctorReport`, and `doctor`, giving the runtime a host diagnostics pass before extraction.
- E1 source verified: `crates/xberg/src/pdf/scan_detect.rs` scores page scan signals from image coverage, invisible text ratio, codec class, and producer prior.
- E2 test verified: `crates/xberg/src/core/batch_mode.rs` includes unit tests proving the batch flag is scoped to the future and reset afterward.
- E2 test verified: `crates/xberg/src/pdf/scan_detect.rs` contains scan-threshold tests for boundary conditions and threshold clamping.
- E2 test verified: `crates/xberg-cli/tests/extract_envelope.rs` verifies the JSON timing envelope, `ocr_used` flag, and stage-timing behavior for CLI extraction and batch runs.
- E2 test verified: `crates/xberg/src/extractors/pdf/ocr.rs::test_scanned_empty_page_still_routes_to_ocr` shows that scanned pages still reach OCR when the gate says they should.

## Architecture

Principal components:

- Public extraction API over a lazily created engine.
- Batch executor with semaphore-based concurrency and ordered result assembly.
- Task-local batch flag so extraction internals can switch execution strategy.
- Doctor subsystem for backend viability and cache hygiene.
- PDF scan detection and OCR gating heuristics.
- CLI envelope and instrumentation around extraction timing.

Most interesting mechanism: the runtime makes batch processing explicit at the task-local level and then uses that context to choose the right concurrency strategy while keeping the batch result order stable. Combined with `doctor`, this gives the pipeline both a preflight environment check and a controlled runtime envelope.

Baseline comparison: a simple OCR wrapper would expose one extraction call and one backend choice, then leave operators to discover configuration failures after the first document breaks. Xberg adds host diagnostics, batch-scoped concurrency, scan scoring, and timing envelopes before and during the extraction path.

## Reuse Guidance

Reusable:

- Use task-local batch context to switch heavy extractors into parallel mode without leaking that mode into single-file execution.
- Run a doctor/probe pass before the first extraction when backend availability matters.
- Treat scan detection as a scoreable, testable gate rather than a binary heuristic hidden inside the OCR code path.
- Emit a JSON timing envelope around the CLI so batch behavior can be measured without parsing logs.

Do not copy:

- Do not copy the entire backend matrix unless we need it.
- Do not assume the heuristic thresholds are portable without workload-specific validation.
- Do not couple the task-local flag to public API semantics unless there is a clear reason.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The batch mode state is unit-tested.
- The scan detector has explicit threshold tests.
- The CLI envelope is integration-tested.
- The doctor subsystem gives clear operational feedback without making network calls by default.

Experimental or incomplete for our needs:

- The backend matrix is broad and workload-dependent.
- Some extraction decisions rely on heuristics that will need corpus-specific tuning.
- The repository is larger than the reusable batch/diagnostics core.

Hidden costs and failure modes:

- False positives or negatives in scan detection can route documents down the wrong extraction path.
- Batch mode is scoped to the future, so nested or detached tasks can miss the flag if the code is not careful.
- More backends means more environment-specific failure modes and more validation burden.

Adoption experiment:

Run one controlled batch extraction and one single-file extraction against the same corpus, then compare timing, order preservation, and scan-routing decisions under a forced backend failure.

## Candidate Patterns

- `batch-aware extraction envelope`
- `doctor-probed backend selection`
- `scan confidence heuristic`
