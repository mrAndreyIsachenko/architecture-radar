# datalab-to/marker

- Repository: https://github.com/datalab-to/marker
- Review date: 2026-08-08
- Current commit reviewed: `e1a6226adfaab4cd573cfa96e12d60905ee38036`
- Commit date: 2026-08-07T06:33:06+00:00
- Branch: `master`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `document-ai-ocr`, especially layout-aware extraction, OCR fallback, table reconstruction, repeat-loop scrubbing, and markdown/JSON output generation. The reusable mechanism is the pdftext-first conversion pipeline with deferred high-resolution promotion and table-specific fallback, not the product shell or service wrappers around it.

## Verified Flow

`PdfConverter.__call__` -> `DocumentBuilder.build_document` constructs lowres page groups and per-page highres loaders -> `LayoutBuilder.__call__` chooses balanced or fast layout and can skip or force OCR depending on mode -> `render_highres` promotes only pages that need the expensive image -> `OcrBuilder` runs full-page or block OCR, then `clean_html` strips debug attributes and drops repetition loops -> `TableProcessor` reconstructs digital tables from the text layer first and falls back to OCR only when heuristics fail -> the renderer emits markdown or JSON.

- E1 source verified: `marker/converters/pdf.py` defines `PdfConverter.__call__`, device-appropriate mode selection, and the builder/processor/renderer orchestration.
- E1 source verified: `marker/builders/document.py` defines lowres page creation, the per-page highres loader, `page_needs_highres`, and `render_highres`.
- E1 source verified: `marker/builders/layout.py` defines the `balanced`/`fast` mode split, the `force_ocr` shortcut, and the pdftext-reading-order optimization.
- E1 source verified: `marker/builders/ocr.py` defines `build_block_requests`, `apply_block_html`, and `clean_html`, including repetition-loop dropping and tag balancing.
- E1 source verified: `marker/processors/table.py` reconstructs digital tables from the PDF text layer, applies an OCR fallback only for unresolved tables/forms, and removes contained blocks after promotion.
- E2 test verified: `tests/builders/test_document_builder.py::test_document_builder` and `::test_document_builder_inline_eq` verify pdftext-first structure, line/span preservation, and text-layer retention.
- E2 test verified: `tests/processors/test_table_processor.py::test_table_processor`, `::test_avoid_double_ocr`, and `::test_split_rows` verify table HTML promotion, no double OCR, and table row recovery.
- E2 test verified: `tests/builders/test_ocr_builder.py::test_clean_html` verifies debug-attribute stripping and repetition-loop suppression.
- E2 test verified: `tests/converters/test_pdf_converter.py::test_pdf_converter` and `tests/converters/test_modes.py::test_fast_mode_digital` verify end-to-end markdown conversion and mode-specific pdftext behavior.

## Architecture

Principal components:

- A builder/processor/renderer split with a small converter orchestration layer.
- Layout and OCR builders that switch between balanced GPU/VLM paths and fast CPU paths.
- A table processor that reconstructs digital tables from pdftext and only OCRs the leftovers.
- Renderers that can emit markdown, JSON, HTML, or chunked output.

Most interesting mechanism: the pipeline does not treat OCR as the default. It starts with structural parsing, renders high-resolution pages only when a later step proves they are needed, and then uses pdftext heuristics plus OCR fallback to preserve table fidelity. The HTML cleaner also strips repetition loops, which is a practical guardrail against model degeneration.

Baseline comparison: a conventional document parser either rasterizes everything up front or runs OCR on every page. Marker instead tries to keep born-digital pages on the cheaper pdftext path and spends OCR/model budget only on the pages and blocks that need it.

## Reuse Guidance

Reusable:

- Start with a structural parse and promote expensive pixels only when needed.
- Reconstruct tables from the text layer before spending OCR budget.
- Drop degenerate repeated output before it reaches downstream consumers.
- Keep page-level lazy loaders or promotion gates separate from the conversion output.

Do not copy:

- Do not copy the full product surface, service clients, or model-serving assumptions.
- Do not rely on mode names or specific Surya model classes as architectural concepts.
- Do not assume table heuristics are reliable enough to replace validation.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The repository has explicit tests for document construction, OCR cleanup, table promotion, and end-to-end converter behavior.
- The mode split is visible in source and tests, not just in docs.
- The table path includes cleanup and fallback rather than a single brittle heuristic.

Experimental or incomplete for our needs:

- The pipeline depends on several external model/service components.
- Table reconstruction still falls back to OCR when the text-layer heuristic cannot reach confidence.
- The high-resolution path is controlled by heuristics that can drift when model behavior changes.

Hidden costs and failure modes:

- The balanced path can still be expensive on GPU-heavy workloads.
- The lazy high-resolution path can miss content if page classification is wrong.
- Repetition-loop scrubbing can discard useful output if a model emits a legitimate repeated string.
- The repo is tuned around its own document schema, so direct reuse requires adapter work.

Adoption experiment:

Run one mixed-quality PDF corpus through a lowres-first pipeline, then force a table-heavy sample and a repetition-loop sample to verify that table promotion, HTML cleanup, and markdown output remain stable when the expensive path is only used for the needed pages.

## Candidate Patterns

- `Deferred Image Materialization`
- `pdftext-first table reconstruction with OCR fallback`
- `repeat-loop HTML scrubbing`
- `balanced/fast layout split`
