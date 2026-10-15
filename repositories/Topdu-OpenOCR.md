# Topdu/OpenOCR

- Repository: https://github.com/Topdu/OpenOCR
- Review date: 2026-10-07
- Current commit reviewed: `1ccfc6ee6161f7133b192e16af3a9265273997ba`
- Commit date: 2026-09-21
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `document-ai-ocr`, especially layout-aware extraction, page/region provenance, structured document output, and multi-task OCR dispatch. The reusable mechanism is the document pipeline, not the demo wrapper around it.

## Verified Flow

`OpenOCR.__init__` validates the task and dispatches to the task-specific model constructor -> `OpenOCR.__call__` routes each request to `det`, `rec`, `ocr`, `unirec`, or `doc` -> `OpenOCR._init_doc_task` builds `OpenDocONNX` for document parsing -> `OpenDocONNX.predict` preprocesses pages, optionally runs layout detection, gathers crops, and yields `PaddleOCRVLResult` objects that carry page, layout, and block metadata -> `get_layout_parsing_results` merges layout blocks, tokenizes table/formula/image regions, and emits `PaddleOCRVLBlock` objects -> the test harness exercises the Python API and the doc serialization helpers.

- E1 source verified: `openocr.py` dispatches `det`, `rec`, `ocr`, `unirec`, and `doc` tasks and instantiates `OpenDocONNX` for document parsing.
- E1 source verified: `tools/infer_doc.py::predict` and `get_layout_parsing_results` build layout detections, image crops, parsing results, and `layout_det_res` / `parsing_res_list` output records.
- E1 source verified: `openocr.py::save_to_json`, `save_to_markdown`, and `save_visualization` serialize doc outputs only on the `doc` task.
- E2 test verified: `test_openocr.py::test_python_api` exercises `det`, `rec`, `ocr`, `unirec`, and `doc` flows and verifies the doc save helpers.

## Architecture

Principal components:

- Unified task dispatcher for OCR, recognition, universal recognition, and document parsing.
- Document parsing backend with layout detection, crop gathering, and per-page structured output.
- Serialization helpers for JSON, Markdown, and visualization.
- API test harness that validates all supported task modes.

Most interesting mechanism: the doc task keeps layout detection, block cropping, and structured serialization inside one flow, so page-level provenance survives past the model call and into the saved artifact shape.

Baseline comparison: a conventional OCR wrapper would emit raw text or page images and leave layout reconstruction to the caller. OpenOCR instead keeps the page and block structure in the output object.

## Reuse Guidance

Reusable:

- Preserve page-level and block-level metadata in the parsed output.
- Separate task dispatch from document parsing and serialization.
- Use one doc pipeline that can serialize JSON, Markdown, and visualization from the same result object.

Do not copy:

- Do not copy the task menu as-is unless you need the same OCR feature set.
- Do not assume model auto-download behavior is acceptable in a production pipeline without explicit pinning.
- Do not rely on doc outputs without runtime validation on representative PDFs and scans.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The doc path is source-backed, not just described in README prose.
- The output carries page, layout, and block metadata instead of flattening to plain text.
- The test harness exercises the Python API and the save helpers.

Experimental or incomplete for our needs:

- The repository still reads as a model/application bundle, not a hardened service.
- The reviewed source does not prove mixed-document runtime behavior under partial failures.
- The doc serialization path still needs corpus-level validation.

Hidden costs and failure modes:

- Layout detection and chart recognition increase model and runtime complexity.
- Structured outputs are only as stable as the upstream page detection and tokenization steps.
- Auto-download and backend selection can hide deployment drift.

Adoption experiment:

Run the doc task over a mixed PDF corpus with tables, formulas, charts, and malformed pages, then confirm `layout_det_res`, `parsing_res_list`, and the JSON/Markdown exporters stay aligned under partial failure.

## Candidate Patterns

- `layout-aware extraction pipeline`
- `structured document output serialization`
