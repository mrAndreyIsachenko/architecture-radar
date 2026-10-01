# hoyla/fusion-ocr

- Repository: https://github.com/hoyla/fusion-ocr
- Review date: 2026-10-01
- Current commit reviewed: `ebe76ec91a2c1c774ecd1ed36a1f1127c7b30f39`
- Commit date: 2026-09-16T21:48:10+01:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `document-ai-ocr`, especially hybrid OCR, page/region provenance, long-document batch handling, and output-shape stability under mixed deterministic and VLM-backed reads. The reusable mechanism is the split between deterministic geometry and VLM semantics, with the deterministic path retained as the canonical overlay geometry and the VLM path used only for reading.

## Verified Flow

`pipeline.process` hashes the source PDF and resumes from per-stage snapshots -> `Triage.run` strips zero-width contamination, preserves clean text-layer segments, and marks pages needing OCR when the text layer is absent, contaminated, or only partially present -> `Layout.run` uses PP-DocLayoutV2 to attach page regions and reading order from the upright raster -> `OcrDet.run` chooses PaddleOCR, Apple Vision, or RapidOCR by route and writes line segments in page space -> `VlmRead.run` skips born-digital pages, routes OCR-bound pages to a model, rejects refusal/repetition outputs, and stores page-level readings -> `Fusion.run` aligns VLM text to deterministic boxes, keeps `det_text` and `vlm_text` beside `best_text`, and falls back honestly when the alignment is weak -> `Render.run` and storage write the final artifacts under the content-addressed job directory -> `eval.harness.evaluate_pdf` renders born-digital pages into image-only PDFs and scores recovered text against the embedded layer.

- E1 source verified: `src/fusion_ocr/pipeline.py::process` persists per-stage snapshots and restores the latest matching recipe fingerprint before continuing a run.
- E1 source verified: `src/fusion_ocr/stages/triage.py::Triage.run` and `_triage_page` decide OCR need from text-layer contamination, image coverage, and page-level content, while preserving clean text-layer segments.
- E1 source verified: `src/fusion_ocr/stages/layout.py::Layout.run` attaches PP-DocLayoutV2 regions and reading order in page space.
- E1 source verified: `src/fusion_ocr/stages/ocr_det.py::OcrDet.run` and `_engine_for` select the deterministic reader and disable orientation/unwarping so box coordinates remain stable.
- E1 source verified: `src/fusion_ocr/stages/vlm_read.py::VlmRead.run` and `_looks_like_refusal` reject hallucination-shaped reads and keep the deterministic fallback visible.
- E1 source verified: `src/fusion_ocr/stages/fusion.py::Fusion.run` and `_word_distribute` align VLM prose to deterministic line clusters and fall back to line-level alignment when the anchor chain is weak.
- E2 test verified: `tests/test_pipeline.py::test_end_to_end_emits_artifacts` verifies a PDF flows end-to-end, emits `segment_index.json` and `doc.json`, and preserves per-stage timing.
- E2 test verified: `tests/test_eval_harness.py::test_each_page_is_rendered_to_a_scan_and_scored_exactly` verifies the born-digital eval path renders image-only pages and compares them against the text layer.
- E2 test verified: `tests/test_routing.py::test_rapidocr_engine_seam` verifies the route selector keeps the default Paddle path unless RapidOCR is explicitly available and requested.

## Architecture

Principal components:

- `pipeline.py` for stage orchestration, content-addressed job directories, and resumable per-stage snapshots.
- `stages/triage.py`, `layout.py`, `ocr_det.py`, `vlm_read.py`, `fusion.py`, and `render.py` for the geometry/semantics split.
- `routing.py`, `engines/`, and `vlm/` for backend selection and OpenAI-compatible reader integration.
- `eval/` for born-digital scoring, page rendering, and corpus-level harness execution.
- `storage.py`, `jobs.py`, and `api.py` for resumable artifact storage and asynchronous job boundaries.

Most interesting mechanism: the deterministic OCR boxes stay canonical even when the VLM reading is better. The VLM is never allowed to invent geometry; it only supplies text that is then aligned back onto deterministic boxes or rejected if the output looks like a refusal, repetition loop, or weak alignment chain.

Baseline comparison: a conventional OCR pipeline either trusts the VLM reading outright or treats OCR and layout as one coupled step. This repo separates geometry from semantics and preserves both raw and fused evidence so later consumers can decide what to trust.

## Reuse Guidance

Reusable:

- Preserve deterministic geometry as the canonical coordinate layer.
- Keep VLM output separate from geometry and gate it against refusal/repetition patterns.
- Use stage snapshots plus a recipe fingerprint so reruns can resume without silently colliding with stale outputs.
- Keep evaluation code in the repo so the OCR path can be measured without hand-labeling every page.

Do not copy:

- Do not copy the model-routing surface without the anti-hallucination gates.
- Do not collapse `det_text`, `vlm_text`, and `best_text` into a single opaque output.
- Do not assume the eval corpus is representative of live mixed-quality batches.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The repository has a large, focused test suite around pipeline, routing, evaluation, and storage behavior.
- The runtime is resumable through content-addressed snapshots and a recipe fingerprint.
- The worker/API split makes batch processing and operator-driven reruns explicit.

Experimental or incomplete for our needs:

- The live behavior still depends on external OCR and VLM backends.
- The strongest validation is eval-driven and born-digital; mixed degraded scans still need real batch validation.
- Thresholds for routing, refusal detection, and fusion remain tunable policy points.

Hidden costs and failure modes:

- Route selection can drift if backend availability or thresholds change unexpectedly.
- Weak alignment can drop output rather than pin it, which is safer but can hide sparse evidence.
- Resuming from snapshots is only as good as the recipe fingerprint and the stage-level cache discipline.

Adoption experiment:

Run a mixed PDF batch with one blocking stage and one malformed page, then verify the content-addressed output directory still preserves page numbering, partial outputs, and overlay provenance while the VLM refusal gate rejects hallucination-shaped reads.

## Candidate Patterns

- `Deferred Image Materialization`
- `provenance-carrying OCR overlay`
- `recipe-fingerprinted resumable pipeline`
