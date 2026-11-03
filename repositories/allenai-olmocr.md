# allenai/olmocr

- Repository: https://github.com/allenai/olmocr
- Review date: 2026-11-03
- Current commit reviewed: `f7cfe4c22098b154c76b6ec950d1c0a464eecf8d`
- Commit date: 2026-03-25T17:52:36Z
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `document-ai-ocr`, especially batch PDF conversion, page-level provenance, repeated-output guardrails, and runtime adapters for large OCR workloads. The reusable mechanism is the queue-backed document pipeline with rotation-aware retry and fallback behavior, not the model-release branding around it.

## Verified Flow

Source path -> `cli_main()` -> `main()`/`worker()` -> `WorkQueue.initialize_queue()` / `get_work()` -> `process_pdf()` -> `process_single_pdf()` -> `process_page()` -> `try_single_page_with_backoff()` -> `try_single_page()` -> `apost()` -> `FrontMatterParser` -> `build_dolma_document()` -> workspace JSONL and markdown paths.

- E1 source verified: `olmocr/pipeline.py` defines the page query, retry ladder, fallback result, worker loop, PDF/tarball ingestion, Dolma document assembly, markdown path mapping, and CLI entry point.
- E1 source verified: `olmocr/work_queue.py` defines deterministic work-group hashing, stale lock handling, done flags, and queue rehydration from storage.
- E1 source verified: `olmocr/repeatdetect.py` implements the repeat counter used to detect repeated text patterns in generated output.
- E1 source verified: `olmocr/bench/benchmark.py` defines the benchmark evaluator that scores candidate outputs against JSONL tests and aggregates per-test results.
- E2 test verified: `tests/test_pipeline.py` exercises image rotation, rotation-correction handling, and the model-request/response path around `process_page()`.
- E2 test verified: `tests/test_integration.py` checks that real workspace outputs contain expected text fragments in the generated markdown/results path.
- E2 test verified: `olmocr/bench/tests.py` exercises the benchmark test types, repeat detection, ordering, and table/math validation logic.

## Architecture

Principal components:

- `pipeline.py` for page-level inference orchestration and document assembly.
- `work_queue.py` for deterministic batching, stale-lock handling, and done tracking.
- `repeatdetect.py` for repeat-pattern detection.
- `bench/` for benchmark scoring, table/maths checks, and report generation.
- `data/` and `train/` for dataset preparation and model-training support.

Most interesting mechanism: page processing has a structured recovery ladder. `process_page()` first attempts normal inference, then retries with rotation correction when the model flags bad orientation, and finally switches from sequential to parallel retries when the queue is empty before falling back to anchor-text extraction.

Baseline comparison: a conventional OCR pipeline would render a page, call the model once, and either accept or fail the result. `olmocr` instead keeps page status, rotation correction, fallback pages, and batch scheduling explicit so the job can continue even when individual pages misbehave.

## Reuse Guidance

Reusable:

- Keep batch partitioning and stale-lock handling outside the page inference code.
- Treat rotation correction as a recovery path, not a post-hoc cleanup step.
- Preserve page spans and fallback counts in the final document projection.
- Use repeat detection as a guardrail for model-generated text that starts looping.

Do not copy:

- Do not copy the model-specific prompt stack or the benchmark corpus as-is.
- Do not copy the manual HTTP transport without a reason to avoid a library client.
- Do not assume the queue/retry policy generalizes to a different OCR model without revalidation.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The work-queue backend isolates locking and completion state from the pipeline body.
- The pipeline has explicit page-failure and document-failure thresholds.
- The benchmark suite covers a broad set of OCR failure modes and document shapes.
- The test suite exercises rotation correction and output-path behavior.

Experimental or incomplete for our needs:

- The runtime still depends on model behavior for page interpretation and rotation correction.
- The HTTP transport is intentionally custom and bypasses a standard client.
- The repo is still an alpha OCR system rather than a hardened service.

Hidden costs and failure modes:

- Queue pressure and parallel retries can amplify resource use when the model is unstable.
- Fallback text can hide model quality issues if consumers only inspect the final document.
- The `apost()` transport and remote inference endpoint are coupled to the availability and semantics of the configured server.

Adoption experiment:

Run a mixed PDF corpus through the pipeline with tables, formulas, rotated pages, malformed pages, and repeated-output cases, then confirm the final page spans, fallback counts, and markdown paths remain stable under load.

## Candidate Patterns

- `queue-backed batch OCR conversion`
- `rotation-aware retry ladder`
- `repeat-detection fallback guard`
- `page-span-preserving Dolma assembly`
