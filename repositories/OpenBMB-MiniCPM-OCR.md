# OpenBMB/MiniCPM-OCR

- Repository: https://github.com/OpenBMB/MiniCPM-OCR
- Review date: 2026-11-21
- Current commit reviewed: `c21a3ca524263ef8166cb6d350864b10c3056b61`
- Commit date: 2026-11-19T22:58:22+08:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `document-ai-ocr`, especially layout-aware extraction, streaming document parsing, page and region provenance, and partial-success recovery. The reusable mechanism is a staged OCR pipeline that separates backend validation, layout detection, recognition, and assembly into explicit phases.

## Verified Flow

`validate_engine_config` rejects unsupported backend types and incomplete connection data -> `create_backend` builds a backend client only after config validation -> `parse_layout_run`, `prepare_run`, `infer_run`, and `pipelined_run` split layout detection from recognition, write per-page and per-block runtime records, preserve page order, and keep partial page failures from aborting the whole run -> `assemble_document_json` and `assemble_documents_json` preserve input order and report partial or failed documents instead of collapsing everything into a single binary result -> tests verify layout worker scaling, deterministic page order, streamed page delivery, and partial-success document JSON.

- E1 source verified: `sdk/minicpmvocr/backends/__init__.py::validate_engine_config` and `create_backend` enforce explicit engine configuration and backend selection.
- E1 source verified: `sdk/minicpmvocr/backends/client.py::VLMClient` handles multiple endpoints, readiness checks, retry-on-overflow behavior, streaming deltas, and per-request latency metrics.
- E1 source verified: `sdk/minicpmvocr/pipeline/staged.py::parse_layout_run`, `prepare_run`, and `infer_run` define the staged parse path and its runtime records.
- E1 source verified: `sdk/minicpmvocr/pipeline/overlapped.py::pipelined_run` executes layout and OCR work concurrently while preserving page completion ordering and failure isolation.
- E2 test verified: `sdk/tests/test_layout_parallelism.py`, `sdk/tests/test_multi_input.py`, and `sdk/tests/test_stream_pages.py` cover deterministic page order, layout worker scaling, partial-success document JSON, and streamed page delivery.

## Architecture

Principal components:

- `sdk/minicpmvocr/backends/` for backend selection, dialect mapping, and request execution.
- `sdk/minicpmvocr/layouts/` for layout-detector registration and aliasing.
- `sdk/minicpmvocr/pipeline/staged.py` for the staged parse and infer path.
- `sdk/minicpmvocr/pipeline/overlapped.py` for concurrent page/layout/OCR scheduling.
- `sdk/minicpmvocr/pipeline/_response.py` and `sdk/minicpmvocr/postprocess/crosspage.py` for document assembly and cross-page merging.
- `sdk/tests/` for layout parallelism, multi-input assembly, streaming, and configuration behavior.

Most interesting mechanism: the layout-first, overlap-aware pipeline. Layout is detected first, recognition is dispatched only for the resulting blocks, and the assembly layer keeps page ordering and partial failures visible. That is useful because it preserves structure while still allowing concurrency and mixed success.

Baseline comparison: a conventional OCR pipeline often rasterizes everything first or makes OCR a prerequisite for all outputs. This repository does the opposite: validate the backend, detect layout, recognize only the derived blocks, and keep the original page ordering intact even when some pages fail.

## Reuse Guidance

Reusable:

- Separate layout detection from recognition so structural information remains authoritative.
- Validate backend configuration before opening live connections.
- Preserve input order and explicit partial-success states in the document assembler.
- Keep streamed page delivery and batch document assembly on the same underlying pipeline.

Do not copy:

- Do not copy the full backend matrix without workload-specific validation.
- Do not treat optional outputs as canonical input.
- Do not assume the current tests prove the live backend will behave the same under real latency and server failures.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The config surface is explicit and the backend entry point is guarded.
- The pipeline has clear stage boundaries and keeps page-level failure visible.
- The tests cover ordering, parallelism, and multi-input assembly rather than only one happy path.

Experimental or incomplete for our needs:

- The repo still depends on live backends and workload-specific validation.
- The orchestration looks robust in tests, but the retry and streaming behavior still needs a real mixed-corpus run.

Hidden costs and failure modes:

- Backend latency and request retry logic can change throughput and queueing behavior in subtle ways.
- Order preservation adds coordination cost when pages finish out of order.
- Optional outputs can drift if callers treat them as canonical rather than derived.

Adoption experiment:

Run a mixed PDF/image corpus against a live backend, slow or restart the server mid-run, and confirm retry, streaming, ordering, and partial-success results still converge without losing page structure.

## Candidate Patterns

- `layout-first staged OCR pipeline`
- `stream-order preserving page pipeline`
- `partial-success document assembly`

