# docling-project/docling

- Repository: https://github.com/docling-project/docling
- Review date: 2026-08-08
- Current commit reviewed: `8050c42be2b179504445cb8f3c75655e27cbb662`
- Commit date: 2026-08-08T08:02:29+02:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `document-ai-ocr`, especially batch PDF conversion, page-number retention under failure, confidence propagation, and mixed backend/runtime control. The reusable mechanism is the threaded PDF pipeline with explicit recovery and post-assembly image materialization, not the broader format-adapter surface around it.

## Verified Flow

`DocumentConverter.convert`/`__call__` normalizes string or `BytesIO` input -> `PdfFormatOption` selects `StandardPdfPipeline` and a PDF backend -> `StandardPdfPipeline._build_document` streams pages through a producer thread and bounded pipeline stages -> `_integrate_results` records `SUCCESS`, `PARTIAL_SUCCESS`, or `FAILURE` and keeps page/failure state separate -> `_assemble_document` builds the final document, generates requested page and element images, aggregates confidence, and backfills missing page slots -> the renderer consumes the completed conversion result.

- E1 source verified: `docling/document_converter.py` defines `PdfFormatOption`, default pipeline selection, and the input normalization path used by `DocumentConverter`.
- E1 source verified: `docling/pipeline/standard_pdf_pipeline.py` defines `_build_document`, `_integrate_results`, `_assemble_document`, and `_add_failed_pages_to_document`, including page-streaming, timeout handling, confidence aggregation, and page-number backfill.
- E1 source verified: `docling/pipeline/standard_pdf_pipeline.py` retains page sizes and error items separately from the success path so downstream output can still render page breaks correctly.
- E2 test verified: `tests/test_failed_pages.py::test_failed_pages_added_to_document_1page` and `::test_failed_pages_added_to_document_2pages` verify that failed pages remain present in `DoclingDocument.pages` and the result status becomes `PARTIAL_SUCCESS`.
- E2 test verified: `tests/test_threaded_pipeline.py::test_threaded_pipeline_stage_shutdown_timeout` verifies the stage shutdown timeout path when a blocking model call does not return.
- E2 test verified: `tests/test_settings_load.py::test_scoped_settings_restores_state` verifies the settings wrapper restores the original state after a scoped override fails.

## Architecture

Principal components:

- `DocumentConverter` and `FormatOption` dispatch by input format and backend type.
- `StandardPdfPipeline` coordinates producer, stage workers, timeout handling, and result integration.
- Backend adapters isolate PDF/HTML/word-processing specifics from the pipeline skeleton.
- Datamodel objects carry page sizes, confidence, errors, and conversion status.

Most interesting mechanism: the pipeline treats failure as a first-class outcome. Pages that fail to parse are still retained in the document, timeout is explicitly surfaced as `PARTIAL_SUCCESS`, and the final document aggregates confidence from page-level scores instead of collapsing them into a single opaque result.

Baseline comparison: a conventional document conversion tool either returns a flat success/failure result or drops failed pages from the output. Docling keeps page numbering stable, preserves error structure, and continues to produce usable output for the pages that did succeed.

## Reuse Guidance

Reusable:

- Preserve page numbering even when some pages fail.
- Keep pipeline recovery separate from backend adapters.
- Aggregate confidence at document scope, but derive it from page-level state.
- Make stage shutdown time-bounded so blocking model calls do not freeze the whole job.

Do not copy:

- Do not copy the full backend zoo unless you need the same format coverage.
- Do not assume that page backfill alone gives provenance; it only preserves document shape.
- Do not tie adoption to Docling-specific backend names or model packages.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The pipeline has explicit timeout, partial-success, and page-retention paths in source.
- Threaded execution is exercised by tests that cover successful runs and blocking-stage shutdown.
- The settings layer has tests for scoped overrides and backend option defaults.

Experimental or incomplete for our needs:

- The surface is broad and product-shaped.
- Source-level provenance is page-oriented, but not an explicit evidence-envelope model.
- Backend/model combinations remain externally coupled.

Hidden costs and failure modes:

- Broad backend support increases operational and maintenance cost.
- Blocking producers can be abandoned after timeout, which protects the job but can leak resources briefly.
- Confidence aggregation can hide a bad tail if downstream consumers only inspect document-level summaries.

Adoption experiment:

Run one internal batch on mixed-quality PDFs, force a page failure and a blocking-stage timeout, then confirm the final document still preserves page numbering, error items, and confidence aggregation without hanging the worker process.

## Candidate Patterns

- `Deferred Image Materialization`
- `page-number-preserving partial-success pipeline`
- `timeout-bounded stage shutdown`
- `confidence aggregation across page outputs`
