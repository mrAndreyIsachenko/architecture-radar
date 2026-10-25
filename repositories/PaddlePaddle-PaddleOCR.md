# PaddlePaddle/PaddleOCR

- Repository: https://github.com/PaddlePaddle/PaddleOCR
- Review date: 2026-10-25
- Current commit reviewed: `dab3fe35379033fdcb2d0e9572fac0b36c9a9ebf`
- Commit date: 2026-09-16T03:30:53Z
- Branch: `main`
- Previous commit reviewed: `n/a`
- Material changes since previous review: first review for this repository in the radar; the current head was reviewed for the synchronous client facade, poll-backed result retrieval, and the structure parsing pipeline.
- Decision: track

## Problem Fit

This repository informs `document-ai-ocr` through a structured OCR and document-parsing pipeline. The reusable mechanism is the job-client plus parser stack that keeps page-level provenance, markdown output, and raw payloads available instead of collapsing the result into plain extracted text.

## Verified Flow

User input file or URL -> `PaddleOCRClient.ocr()` or `parse_document()` resolves the model and options -> `_submit()` validates that the caller supplied exactly one source, builds the payload, and sends the request -> `Poller.poll_until_done()` polls the job state with bounded backoff until the job is `done` or `failed` -> `parse_ocr_result()` or `parse_doc_parsing_result()` builds typed result objects and preserves page-level raw payloads -> `StructureSystem.__call__()` combines layout detection, OCR, table recognition, and formula recognition into region-level structure output.

- E1 source verified: `paddleocr/_api_client/client.py::PaddleOCRClient.parse_document`, `ocr`, `submit_document_parsing`, `submit_ocr`, and `_submit` validate the source and submit async jobs.
- E1 source verified: `paddleocr/_api_client/_poller.py::poll_until_done`, `parse_ocr_result`, and `parse_doc_parsing_result` implement bounded polling and typed result parsing with raw payload retention.
- E1 source verified: `ppstructure/predict_system.py::StructureSystem.__init__`, `__call__`, and `_predict_text` compose layout, OCR, table, and formula subsystems.
- E2 test verified: `tests/pipelines/test_pp_structurev3.py::test_predict` and `test_predict_params` exercise the PPStructureV3 pipeline and parameter forwarding.
- E2 test verified: `tests/api_client/test_core.py` covers payload key conversion, raw-field preservation, model resolution, and input validation.

## Architecture

Principal components:

- Synchronous client facade over asynchronous OCR/document-parsing jobs.
- Poller with explicit job-state validation and bounded backoff.
- Structure pipeline that composes layout, text, table, and formula subsystems.
- Result mappers that preserve raw payloads, exports, images, and page-level metadata.

Most interesting mechanism: the parsed document result keeps markdown, image references, exports, input-image links, and raw items together in one typed page object. That gives downstream systems provenance instead of a flattened text blob.

Baseline comparison: a conventional OCR wrapper would run inference once and return extracted text. PaddleOCR instead wraps a job API, polls until completion, and keeps structured page data with explicit provenance fields.

## Reuse Guidance

Reusable:

- Treat async OCR jobs as typed polling workflows.
- Preserve raw result fragments alongside parsed fields.
- Keep layout-aware filtering separate from the transport/client layer.
- Validate input source selection before the backend call.

Do not copy:

- Do not copy the synchronous facade without live runtime validation against a representative document batch.
- Do not collapse page-level provenance back into plain text if downstream consumers need markdown, images, or export artifacts.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Client and parser code are explicit about job state, payload shape, and parse errors.
- The structure pipeline composes multiple document subsystems instead of hard-coding one extraction mode.
- Tests cover parameter forwarding and the basic pipeline path.

Experimental or incomplete for our needs:

- The reviewed evidence still needs live runtime validation on a representative document batch against the actual backend path.

Hidden costs and failure modes:

- Polling and backoff introduce runtime latency and timeout sensitivity.
- Multi-stage document parsing can fail at any stage, so result stability depends on every backend response staying schema-compatible.
- Layout-aware filtering can hide text if upstream layout detection is wrong.

Adoption experiment:

Run `parse_document()` on a mixed PDF/image batch, then verify that the returned pages preserve markdown, images, exports, raw payloads, and stable page counts without timeout or parse failure.

## Candidate Patterns

- `poll-backed document parsing client`
- `layout-aware structure pipeline`
- `typed document page provenance`

## Previous Reviews

First review for this repository in the radar.
