# Sri-Krishna-V/bumblebee

- Repository: https://github.com/Sri-Krishna-V/bumblebee
- Review date: 2026-09-28
- Current commit reviewed: `c108cd33664b57ee64fa80b47a89e1c943749a80`
- Commit date: 2026-08-25T22:17:46+05:30
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: selected

## Problem Fit

This repository informs `document-ai-ocr`, especially layout-aware extraction, resumable OCR batches, text-layer trust decisions, and adaptive retry under resource pressure. The reusable mechanism is the streaming document pipeline and its completion-marker contract, not the hosted API or the studio UI.

## Verified Flow

`Pipeline.stream` orders documents by size, processes them concurrently, and streams each document through render -> layout -> text-layer trust -> crop -> OCR -> format -> stats -> write -> return -> `textlayer.py` trusts embedded PDF text only when page coverage is high enough, otherwise it falls back to OCR -> `runs.py` writes `content.md`, `layout.json`, optional `chunks.jsonl`, and `stats.json` last so `stats.json` remains the completion marker -> tests cover chunking, image cleanup, empty PDFs, render failures, OCR failures, adaptive retry, and storage refiltering.

- E1 source verified: `src/bumblebee/pipeline.py:115-140` streams documents concurrently and cancels in-flight tasks on early close.
- E1 source verified: `src/bumblebee/pipeline.py:170-217` runs render, layout, text-layer extraction, crop, and OCR per page chunk, then applies adaptive retry.
- E1 source verified: `src/bumblebee/pipeline.py:305-377` retries low-confidence regions once at 2x DPI with a bounded retry budget.
- E1 source verified: `src/bumblebee/textlayer.py:41-105` extracts embedded text and only trusts the text layer when coverage meets the threshold.
- E1 source verified: `src/bumblebee/runs.py:53-80` writes outputs and persists `stats.json` last as the completion marker.
- E2 test verified: `tests/test_pipeline.py:103-219` covers end-to-end flow, page-image cleanup, chunking, payload bypass, empty PDFs, render failures, and OCR failures.
- E2 test verified: `tests/test_pipeline.py:222-260` covers adaptive retry and the 10% retry budget.
- E2 test verified: `tests/test_storage.py:16-68` covers storage round-trips, PDF listing, and cloud-storage scheme dispatch.

## Architecture

Principal components:

- Async pipeline orchestration over render, layout, crop, OCR, and format stages.
- Text-layer fast path with per-page trust policy.
- Run-target storage layer with resumability and completion markers.
- GPU and storage backends split behind protocol / storage abstractions.
- Batch-policy and chunking logic for resumable document runs.

Most interesting mechanism: the pipeline keeps OCR and layout in flight per page chunk while preserving resumability at the file level. That makes the first pages of a large document start OCR before the later pages finish rendering, while `stats.json` still decides whether the document is complete.

Baseline comparison: a conventional OCR batch would render the entire PDF first, then layout, then OCR, and only afterward decide whether the run completed. Bumblebee lowers latency and preserves auditability by making the streaming stage boundaries explicit and by writing completion state last.

## Reuse Guidance

Reusable:

- Keep a completion marker separate from the derived document payload.
- Gate embedded text by a per-page coverage threshold instead of assuming every text layer is trustworthy.
- Bound adaptive retry so it improves the worst regions without turning into an unbounded repair loop.
- Close page images as soon as a chunk is consumed.

Do not copy:

- Do not copy the exact model pair or the Modal / web packaging unless those are already requirements.
- Do not rely on the current 10% retry budget without workload-specific tuning.
- Do not assume PDFium / GPU constraints generalize unchanged to other document stacks.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Clear resumability contract anchored on `stats.json`.
- Good GPU-free tests for the stream shape, completion handling, and storage behavior.
- Explicit failure handling for render and OCR stages.

Experimental or incomplete for our needs:

- Real GPU and model latency were not exercised in this review.
- The retry budget and confidence thresholds are corpus-sensitive.
- The text-layer trust path depends on the PDFium extraction behavior remaining stable.

Hidden costs and failure modes:

- A bad text layer can suppress OCR if the coverage threshold is too permissive.
- Adaptive retry can mask low-confidence regions if the corpus is outside the tuned distribution.
- More concurrency improves throughput but raises GPU and storage pressure.

Adoption conditions:

- Validate on a mixed-quality corpus with actual GPU / OCR latency.
- Confirm resumability against partially written targets.
- Tune the confidence threshold and retry budget against representative PDFs.

## Candidate Patterns

- `chunk-streamed OCR pipeline`
- `text-layer trust gate`
- `resumable completion marker`
- `bounded adaptive OCR retry`
