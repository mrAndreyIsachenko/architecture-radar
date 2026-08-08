# Architecture Radar Supplement: 2026-08-08

## Prerequisites And State

- Run date: 2026-08-08 Europe/Moscow.
- Existing daily report present: `true`.
- Supplement required by CI context: `true`.
- Supplement report path: `reports/2026-08-08-supplement-1.md`.
- Scope files changed after the existing daily report: `docs/agent-rules.md`, `docs/research-scope.md`, `interests.md`, `watchlist.yml`.
- Required workspace verified: `interests.md`, `watchlist.yml`, `radar.json`, `reports/`, `repositories/`, and `patterns/` exist.
- The existing daily report was read first so the supplement could avoid repeating prior deep reviews.
- Temporary clones were placed under `/tmp/architecture-radar-candidates`.
- CI constraint observed: no commits, pushes, remote edits, or pull requests were created by the agent.

## Candidate Counts

Highest stage reached:

- `triaged`: 4
- `source-inspected`: 3
- `deeply-reviewed`: 2

Total candidates reaching at least `triaged`: 4.

## Candidate Counts By Family And Artifact Type

- `document-ai-ocr`: 4 candidates
- `repository` artifacts: 3
- `model` artifacts: 1

## Watchlist Coverage

- Active watchlist entries: 1
- Unsatisfied watchlist entries: none
- `baidu/Unlimited-OCR` was accounted for explicitly as a `watch-model` entry and not deep-reviewed because the repository is still a model-release surface with thin inspectable implementation relative to the source-heavy document parsers in this supplement.

## Selected Repositories

- `docling-project/docling` at `8050c42be2b179504445cb8f3c75655e27cbb662`
- `datalab-to/marker` at `e1a6226adfaab4cd573cfa96e12d60905ee38036`

## Executive Summary

This supplement covers the document-AI/OCR scope that was under-covered in the existing daily report. Two source-backed repositories clear the bar:

- `docling-project/docling` adds a threaded PDF conversion pipeline with explicit timeout handling, partial-success recovery, page-number retention, and confidence aggregation.
- `datalab-to/marker` adds a pdftext-first document builder with deferred high-resolution promotion, layout-mode switching, table reconstruction from the text layer, and repeat-loop scrubbing.

The supplement also records the watchlist model release `baidu/Unlimited-OCR` as a `watch-model` decision and defers `allenai/olmocr` as a benchmark-heavy baseline that was source-inspected but not selected.

The main pattern update is [Deferred Image Materialization](../patterns/deferred-image-materialization.md), which captures the shared lowres-first / promote-later shape across Docling and Marker.

## Material Changes Since The Previous Run

- The supplement scope shifted to document AI / OCR and model-release watching because `interests.md`, `docs/research-scope.md`, `docs/agent-rules.md`, and `watchlist.yml` changed after the prior daily report.
- The new supplement covers a topic family that was missing from the prior 2026-08-08 daily report.
- The watchlist now forces explicit accounting for `baidu/Unlimited-OCR`, which was recorded as a watch-model rather than disappearing into broad discovery.
- The radar now has a new cross-repo document-parsing mechanism: deferred image materialization.

## Detailed Reviews

- [docling-project/docling](../repositories/docling-project-docling.md)
- [datalab-to/marker](../repositories/datalab-to-marker.md)

## Extracted Or Updated Patterns

- Created [Deferred Image Materialization](../patterns/deferred-image-materialization.md).

## Relevance To Explicit Problems In `interests.md`

- `document-ai-ocr`: source-backed layout-aware extraction, page/region provenance, OCR fallback, table reconstruction, and repeat-loop guardrails.
- `document-ai-ocr`: batch processing and resumability through partial-success recovery, page retention, and time-bounded shutdown.
- `document-ai-ocr`: evaluation and confidence handling through tests that exercise conversion, table promotion, and cleanup behavior.

## Candidate Ledger

| Repository | URL | Commit | Discovery source | Family | Stage | Categories | Activity signal | Mechanism signal | Relevance signal | Decision | Rejection or deferral reason | watchlist_priority | artifact_type | review_mode | external_artifacts | satisfied_by |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `docling-project/docling` | https://github.com/docling-project/docling | `8050c42be2b179504445cb8f3c75655e27cbb662` | GitHub search for document parsing / OCR pipelines | `document-ai-ocr` | deeply-reviewed | document parsing; layout-aware extraction; confidence propagation | Commit 2026-08-08; active pipeline, backend, and test surface | threaded stage pipeline, timeout recovery, confidence aggregation, page backfill | Direct fit for batch document conversion and recovery | selected | Source-backed batch pipeline cleared the bar |  | repository | deep-review |  |  |
| `datalab-to/marker` | https://github.com/datalab-to/marker | `e1a6226adfaab4cd573cfa96e12d60905ee38036` | GitHub search for PDF-to-markdown / OCR pipelines | `document-ai-ocr` | deeply-reviewed | document parsing; layout-aware extraction; OCR fallback | Commit 2026-08-07; active converter, builder, and test surface | pdftext-first conversion, deferred highres promotion, table reconstruction, repeat-loop scrubbing | Direct fit for layout-aware extraction and OCR guardrails | selected | Source-backed parsing mechanism cleared the bar |  | repository | deep-review |  |  |
| `allenai/olmocr` | https://github.com/allenai/olmocr | `f7cfe4c22098b154c76b6ec950d1c0a464eecf8d` | GitHub search for OCR evaluation and runtime harnesses | `document-ai-ocr` | source-inspected | benchmark harness; retry orchestration; queueing | Commit 2026-03-25; bench, pipeline, and work-queue code present | rotation retry loop, exponential backoff, S3/local work queue, repeated-generation benchmark | Relevant evaluation harness, but older and more benchmark-heavy than the selected repos | deferred | Good baseline for OCR evaluation, but not selected in this supplement |  | repository | source-inspect |  |  |
| `baidu/Unlimited-OCR` | https://github.com/baidu/Unlimited-OCR | `d49ff64afffc1f47ab563dc1c589bc2f78808fa4` | Watchlist / GitHub discovery | `document-ai-ocr` | triaged | model release; runtime adapter; long-horizon OCR | Commit 2026-07-29; README, inference script, and external runtime links present | constant-KV long-horizon parsing claim, vLLM support, batch-inference surface | High relevance as a model-release watch, but source is still thin | watch-model | Watchlist requires explicit accounting; not deep-reviewed because the source surface is model-heavy | high | model | watch-model | `https://huggingface.co/baidu/Unlimited-OCR`, `https://arxiv.org/abs/2606.23050`, `https://recipes.vllm.ai/baidu/Unlimited-OCR` | watch-model |

## Recommended Next Action

Run one internal OCR ingestion experiment with three failure injections: disable high-resolution promotion for a table-heavy page set, force a partial page failure, and feed a repetition-loop sample through the table/OCR path. Confirm that the output still preserves page numbering, confidence state, and cleanup behavior without rendering every page at high resolution.

## Notable Rejected Or Deferred Candidates

- `allenai/olmocr` was source-inspected but deferred because it is older and primarily functions as an evaluation/retry baseline rather than a current parser/runtime selection.
- `baidu/Unlimited-OCR` was recorded as `watch-model` rather than selected because the repository is a model-release surface with thin inspectable source.

## Unresolved Evidence Gaps

- No local test suite was run in this CI pass.
- `docling-project/docling` still needs local validation against the exact backend/model combination that would be used in production.
- `datalab-to/marker` still depends on external model services and heuristic thresholds that should be validated against real workloads.
- `baidu/Unlimited-OCR` remains a watch-model because the main architectural questions live in the runtime recipe and model release rather than deep source code.
