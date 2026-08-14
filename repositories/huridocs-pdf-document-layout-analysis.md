# huridocs/pdf-document-layout-analysis

- Repository: https://github.com/huridocs/pdf-document-layout-analysis
- Review date: 2026-08-14
- Current commit reviewed: `cb47514458a29cadbc1e3a667050c1a6de1d25a5`
- Commit date: 2026-07-13T18:26:17+03:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `document-ai-ocr`, especially layout-aware extraction, OCR promotion, page provenance, and memory control in PDF conversion services. The reusable mechanism is the structural-first PDF analysis pipeline with late promotion to high-resolution rendering only for the segment types that need it.

## Verified Flow

`AnalyzePDFUseCase.execute` chooses the fast or regular analysis path -> `PDFAnalysisServiceAdapter.analyze_pdf_layout` saves the PDF to a temporary path, builds a structural `PdfImages` representation, and sends it to the layout predictor -> the optional `parse_tables_and_math` branch reopens the same PDF at 200 dpi and runs formula/table conversion only for the predicted segments -> the adapter deletes the temp PDF unless `keep_pdf` is set -> `PdfToMarkupServiceAdapter._get_styled_content_parts` assigns segment IDs, extracts links, renders page images only when picture segments exist, and then processes segments in page order -> `FileSystemRepository` provides the temp-file, XML, and markdown persistence boundary -> end-to-end tests exercise the API paths for analysis, TOC extraction, HTML/text output, XML save/load, and malformed segment handling.

- E1 source verified: `src/use_cases/pdf_analysis/analyze_pdf_use_case.py:6-32` routes the request to either the slow or fast analysis path and keeps `keep_pdf` as an explicit control.
- E1 source verified: `src/adapters/infrastructure/pdf_analysis_service_adapter.py:24-49` saves the PDF once, builds a structural image representation, predicts layout, promotes to 200 dpi only for tables and formulas, and deletes the temp file by default.
- E1 source verified: `src/adapters/infrastructure/pdf_analysis_service_adapter.py:51-72` mirrors the same fast-path shape with the fast model service and the same conditional promotion logic.
- E1 source verified: `src/adapters/infrastructure/markup_conversion/pdf_to_markup_service_adapter.py:348-405` assigns segment IDs, extracts links, renders page images only when picture segments exist, and emits content in page order.
- E1 source verified: `src/adapters/storage/file_system_repository.py:9-55` writes temp PDFs, XML, and markdown to explicit paths and deletes temp PDFs through the repository boundary.
- E2 test verified: `src/tests/test_end_to_end.py:55-152` verifies regular and fast analysis paths plus XML save/load.
- E2 test verified: `src/tests/test_end_to_end.py:188-253` verifies TOC extraction in both modes and TOC-from-XML reuse.
- E2 test verified: `src/tests/test_end_to_end.py:255-497` verifies text extraction, HTML extraction, segment-box handling, and malformed segment rejection.

## Architecture

Principal components:

- `AnalyzePDFUseCase` as the request router.
- `PDFAnalysisServiceAdapter` as the PDF-to-segments execution boundary.
- `PdfToMarkupServiceAdapter` as the layout-aware HTML/Markdown conversion layer.
- `FileSystemRepository` as the persistence and cleanup boundary.
- `PdfImages`, `SegmentBox`, and layout/prediction services as the structural and visual data model.

Most interesting mechanism: the pipeline separates the structural pass from the expensive image pass and only promotes to higher DPI when a downstream converter actually needs tables or formulas. Picture segments trigger page rendering, but other segment types stay on the cheap path.

Baseline comparison: a conventional OCR service would rasterize all pages at the highest useful DPI up front and keep the rendered images around for the whole pipeline. This implementation narrows the expensive path to the segments that need it and deletes the temporary PDF unless the caller opts out.

## Reuse Guidance

Reusable:

- Parse structure first, then promote only the elements that need high-resolution pixels.
- Keep a visible `keep_pdf` or equivalent flag so cleanup is explicit instead of implicit.
- Preserve page order and segment provenance while mixing structural and image-based conversion.
- Use end-to-end tests to pin the cheap path, the promoted path, and malformed segment rejection.

Do not copy:

- Do not copy the full service API or deployment packaging if only the promotion boundary is useful.
- Do not assume the same picture/table heuristics are correct for a different layout model or OCR backend.
- Do not rely on the temp-file delete path without an explicit retention option for debugging or review.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The slow and fast analysis paths share the same lifecycle boundary.
- Temporary PDFs are cleaned up by default.
- TOC, text, HTML, and XML output are all covered by end-to-end tests.
- The converter keeps page order and segment identity stable during post-processing.

Experimental or incomplete for our needs:

- The fast path still depends on segment-classification quality.
- The high-resolution promotion logic is service-specific rather than a general document pipeline abstraction.
- Error handling is mostly exercised through HTTP tests rather than lower-level unit isolation.

Hidden costs and failure modes:

- Misclassified tables or images can remain on the cheap path and lose fidelity.
- Promoting too many segments erodes the latency and memory savings.
- If the converter renders pictures too aggressively, the pipeline can regress into eager rasterization.
- Temp-file cleanup failures can leak local disk usage.

Adoption conditions:

- Confirm that the structural pass is sufficient for the majority of documents in the target workload.
- Add tests that prove page numbering, provenance, and output shape remain stable when promotion is disabled.
- Verify that cleanup and retention flags behave correctly on failure paths.

## Candidate Patterns

- `structural-first PDF conversion`
- `late DPI promotion for OCR`
- `picture-gated page rendering`
