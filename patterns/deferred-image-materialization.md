# Deferred Image Materialization

- Canonical name: Deferred Image Materialization
- Aliases: lazy high-res page promotion, lowres-first page promotion, page-image promotion after structural parse, page crop promotion
- Avoided duplicate names: eager rasterization, always-highres OCR, full-page first pass, blanket page rendering
- Last updated: 2026-08-08

## Problem

Document pipelines waste memory and latency when they render every page or crop at high resolution before they know which pages or regions actually need it. That is especially expensive for mixed born-digital and scanned PDFs, large batch runs, and conversion jobs that may fail partway through.

## Mechanism

Materialize a cheap structural representation first. Decide which pages or elements actually need detailed pixels. Render high-res page images or element crops only for that subset, preferably in a single batched pass. Preserve lazy loaders or provenance so later processors can still retrieve the expensive image on demand. Keep failure handling separate so skipped pages still keep stable numbering.

## Invariants

- Structural parsing happens before expensive image rendering.
- Only pages or elements with a downstream consumer are promoted.
- Page numbering and provenance survive failed or skipped pages.
- High-res rendering is repeatable and bounded by explicit options.
- Fallback processors should not re-run if a block already has trustworthy HTML.

## Implementation Variants

- Marker: `DocumentBuilder.build_document` creates lowres pages and per-page lazy loaders, then `render_highres` promotes only pages that `page_needs_highres`; `TableProcessor` crops and OCRs only unresolved tables or forms.
- Docling: `StandardPdfPipeline._assemble_document` delays page and element image generation until after structural assembly, then crops only `PictureItem` and `TableItem` regions using `prov` metadata; failed pages are backfilled to keep numbering stable.

## Known Repositories

- `datalab-to/marker` reviewed at `e1a6226adfaab4cd573cfa96e12d60905ee38036`.
- `docling-project/docling` reviewed at `8050c42be2b179504445cb8f3c75655e27cbb662`.

## Comparison Of Implementations

Marker is more explicit about the promotion boundary. It starts with lowres page objects, attaches a page-local highres loader, and decides promotion from layout or OCR state plus block type. Docling is broader: it assembles pages first, then emits page images or cropped element images only when the output format or downstream processor asks for them. Docling's failure retention is stronger; Marker’s per-page lazy loader is sharper.

## Failure Modes

- Misclassifying a page as lowres-only can hide math, tables, or diagrams.
- Over-promotion can erase the memory savings the pattern is supposed to create.
- Lazy loaders that reopen renderers repeatedly can increase latency and resource churn.
- Promotion based on heuristics can drift when model thresholds change.
- If failed pages are not retained, page numbering breaks downstream.

## Trade-Offs

- Deferred rendering lowers peak memory and avoids unnecessary work, but adds control-flow branches.
- High fidelity now costs less if only a few pages need it; it costs more if most pages need promotion.
- Keeping lazy loaders improves correctness but complicates lifecycle management.

## Applicability To Interests

- Directly relevant to `document-ai-ocr` batch processing, layout-aware extraction, page/region provenance, and memory control.
- Useful for document parsing runtimes that need to stay resumable under mixed scanned and born-digital inputs.

## Adoption Conditions

- Add tests that prove the cheap path remains stable when the expensive path is disabled.
- Add tests that prove promoted pages keep stable provenance and page numbering.
- Set explicit memory and promotion thresholds.
- Verify that fallback OCR or crop extraction does not re-render already accepted content.

## Evidence References

- E1 source verified: `docling/pipeline/standard_pdf_pipeline.py` `StandardPdfPipeline._assemble_document` renders page images and cropped element images only after structural assembly, using provenance-backed page lookups.
- E1 source verified: `docling/pipeline/standard_pdf_pipeline.py` `StandardPdfPipeline._add_failed_pages_to_document` preserves missing page numbers after partial failures.
- E2 test verified: `tests/test_failed_pages.py::test_failed_pages_added_to_document_1page` and `::test_failed_pages_added_to_document_2pages` verify page-number retention under partial failure.
- E2 test verified: `tests/test_threaded_pipeline.py::test_threaded_pipeline_stage_shutdown_timeout` verifies stage shutdown and abandonment behavior when a blocking stage hangs.
- E1 source verified: `marker/builders/document.py` `DocumentBuilder.build_document` creates lowres pages, attaches a per-page highres loader, and `render_highres` promotes only pages that need it.
- E1 source verified: `marker/processors/table.py` `TableProcessor.run_ocr_fallback` renders highres crops only for unresolved tables and forms.
- E2 test verified: `tests/builders/test_document_builder.py::test_document_builder_inline_eq` verifies the pdftext-first path and embedded text layer.
- E2 test verified: `tests/builders/test_ocr_builder.py::test_clean_html` and `tests/processors/test_table_processor.py::test_table_processor` verify HTML cleanup, repeat-loop suppression, and table HTML promotion.
