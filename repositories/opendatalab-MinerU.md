# opendatalab/MinerU

- Repository: https://github.com/opendatalab/MinerU
- Review date: 2026-08-11
- Current commit reviewed: `79d6d8d79fb8f3ddba5cc34c07a16f0ec36f56c7`
- Commit date: 2026-07-10T11:51:49Z
- Branch: `master`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `document-ai-ocr`, especially batch PDF conversion, OCR-vs-text routing, page-window processing, and GPU/NPU-aware inference selection. The reusable mechanism is the windowed pipeline plus hybrid OCR promotion logic, not the broader model zoo or demo surface.

## Verified Flow

`doc_analyze_streaming` validates aligned PDF/image/lang inputs -> opens each PDF with pdfium and records page counts in per-document contexts -> groups pages into processing windows sized by `get_processing_window_size` -> `load_images_from_pdf_doc` materializes only the current window into PIL images -> `batch_image_analyze` chooses a batch ratio from device memory and backend type -> `append_batch_results_to_middle_json` merges model output back into `middle_json` -> `_finalize_processing_window_context` finalizes output, calls `on_doc_ready`, and closes pdfium handles.

- E1 source verified: `mineru/backend/pipeline/pipeline_analyze.py:157-328` defines the multi-document processing-window loop, page loading, result batching, progress handling, and context finalization.
- E1 source verified: `mineru/backend/pipeline/pipeline_analyze.py:331-360` selects batch ratios from detected VRAM and backend capabilities before dispatching to `BatchAnalyze`.
- E1 source verified: `mineru/backend/hybrid/hybrid_analyze.py:117-240` gates image analysis by effort level and performs OCR-det cropping with formula masking and batch/non-batch split behavior.
- E2 test verified: `tests/unittest/test_e2e.py:23-71` runs both `parse_method="txt"` and `parse_method="ocr"` against sample PDFs and checks image/table/text/equation content in the emitted content list.
- E2 test verified: `tests/unittest/test_e2e.py:74-190` verifies output generation, HTML validity, and content assertions for the conversion flow.

## Architecture

Principal components:

- `pipeline_analyze.py` for multi-document, windowed orchestration.
- `hybrid_analyze.py` for OCR, layout, formula, and image-analysis gating.
- Model wrappers under `mineru/model/` for OCR, layout, table, formula, and VLM backends.
- Content conversion and writer helpers for turning model output into markdown, JSON, and page artifacts.

Most interesting mechanism: the pipeline slices multiple documents into bounded page windows and reuses a single inference pass per window, while the hybrid path can suppress image analysis in `medium` effort mode and promote only the relevant crops through OCR-det and formula masking.

Baseline comparison: a conventional PDF parser would process one document end-to-end and eagerly run image/OCR work for every page. MinerU batches across documents, keeps the conversion loop windowed, and narrows expensive OCR work to the blocks that need it.

## Reuse Guidance

Reusable:

- Keep document conversion in explicit page windows instead of whole-file passes.
- Gate expensive image analysis behind an effort level or backend capability check.
- Retain per-document context so a batch can emit partial results and still close handles safely.
- Use tests that assert the text and OCR paths both produce stable content lists.

Do not copy:

- Do not copy the full model/backend matrix unless you need that exact deployment spread.
- Do not treat the VLM/hybrid heuristics as source provenance.
- Do not tie adoption to MinerU-specific backend package names.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The core flow is source-backed and windowed instead of ad hoc.
- The hybrid path has explicit effort gating and OCR-det handling.
- The end-to-end test covers both text-first and OCR-first modes.

Experimental or incomplete for our needs:

- Source provenance is still page-oriented, not an evidence envelope.
- The repository is coupled to external model/runtime choices and hardware availability.
- The test surface is e2e-focused rather than a broad failure-injection matrix.

Hidden costs and failure modes:

- Window sizing interacts with memory pressure and throughput.
- The hybrid path can skip expensive image analysis and lose detail if effort is set too low.
- Backend selection and GPU/NPU availability can change behavior materially across deployments.

Adoption experiment:

Run one mixed PDF batch with `parse_method="txt"` and `parse_method="ocr"`, then compare the output content list against a known-good page set while forcing a small window size and a low-memory device profile.

## Candidate Patterns

- `windowed batch document analyzer`
- `effort-gated OCR promotion`
- `backend-capability-aware batch sizing`
