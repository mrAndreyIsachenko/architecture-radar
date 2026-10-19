# utkarsh5026/Docpipe

- Repository: https://github.com/utkarsh5026/Docpipe
- Review date: 2026-10-19
- Current commit reviewed: `5b97ea634c289f9cf98ce5d37786612600376057`
- Commit date: 2026-08-12T21:36:07+05:30
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: selected

## Problem Fit

This repository informs `document-ai-ocr` through a structural-first document pipeline with adaptive preprocessing, backend routing, provenance-aware extraction, and calibrated confidence. The useful mechanism is the page-quality-driven pipeline, not the package’s single-file packaging or README framing.

## Verified Flow

`ingest_*` normalizes PDFs, images, emails, and directories -> `preprocess` applies page-quality policy and records preprocessing history -> `default_router` selects an OCR or VLM backend per page -> `read` executes the chosen backend -> `extract` combines schema evidence with `page_quality_prior` and confidence fusion -> `EvalSuite` scores corpus runs -> `Pipeline` wraps the same flow for one-call execution.

- E1 source verified: `docpipe.py` defines `ingest_pdf`, `ingest_image`, `ingest_tiff`, `ingest_email`, `ingest`, `ingest_dir`, `preprocess`, `default_router`, `read`, `extract`, `page_quality_prior`, `EvalSuite`, and `Pipeline`.
- E2 test verified: `tests/test_integration.py::test_degraded_scan_survives_the_whole_pipeline`, `::test_preprocessing_history_is_a_full_audit_trail`, `::test_native_text_is_read_free_and_exactly`, `::test_mixed_attachments_land_in_one_document`, `::test_each_page_is_routed_on_its_own_merits`, and `::test_a_degraded_page_lowers_confidence_for_the_same_answer` verify routing, auditability, and confidence behavior.
- E2 test verified: `tests/test_backends.py::test_degraded_pages_prefer_a_vision_model`, `tests/test_extract.py::test_signals_are_recorded_for_auditing`, `tests/test_extract.py::test_low_confidence_lists_what_a_human_should_check`, and `tests/test_eval.py::test_confidence_curve_is_produced` verify backend choice, evidence signals, and evaluation output.

## Architecture

Principal components:

- Ingest helpers for PDFs, images, TIFFs, emails, and directories.
- Page-quality policy and preprocessing history tracking.
- Backend router and backend-specific `read` implementations.
- Schema-driven extraction with page-quality priors and confidence fusion.
- Evaluation harness and one-call pipeline wrapper.

Most interesting mechanism: the pipeline changes behavior based on page quality without losing document shape. A degraded page can be routed differently, but the document still retains enough provenance and confidence metadata to audit what happened.

Baseline comparison: a conventional document converter either flattens outputs into text or renders every page before deciding where to spend OCR effort. Docpipe instead keeps the structural parse authoritative and defers expensive reads until page quality justifies them.

## Reuse Guidance

Reusable:

- Keep preprocessing history as part of the document record.
- Route pages independently so a degraded page does not force a degraded document.
- Treat confidence as calibrated, page-aware metadata.
- Use the evaluation harness to compare pipeline behavior across corpora.

Do not copy:

- Do not copy the single-file packaging as a design goal.
- Do not assume backend availability or latency is stable without runtime validation.
- Do not treat the confidence score as a substitute for source-backed provenance.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The same mechanism is exercised by integration tests, backend tests, extraction tests, confidence tests, and evaluation tests.
- The repo keeps audit history and confidence signals close to the core pipeline.

Experimental or incomplete for our needs:

- Live mixed-corpus validation with real OCR and VLM backends is still missing.
- The current evidence is stronger for source-level correctness than for deployed latency or recovery behavior.

Hidden costs and failure modes:

- Adaptive routing can drift if page-quality thresholds are tuned against the wrong corpus.
- Backend diversity increases integration and deployment cost.
- Confidence fusion can hide bad pages if downstream consumers only read document-level summaries.

Adoption experiment:

Run a mixed corpus through one OCR backend and one VLM backend, inject blur and malformed pages, and confirm provenance, page history, and calibrated confidence remain stable under partial failure.

## Candidate Patterns

- `Deferred Image Materialization`
- `adaptive page-quality-driven preprocessing`
- `calibrated confidence fusion`
- `page-history provenance ledger`
