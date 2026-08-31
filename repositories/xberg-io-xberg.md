# xberg-io/xberg

- Repository: https://github.com/xberg-io/xberg
- Review date: 2026-08-29
- Current commit reviewed: `3025e8cbb22bd653443428a4ac352489a7f9b831`
- Commit date: 2026-08-28T21:51:09+02:00
- Branch: `main`
- Previous commit reviewed: `531e0f7895e53f083c7d4f183123dea4f866e4eb`
- Material changes since previous review: the PDF path gained a pixel-free layout gate, per-page gate reasons are now recorded into metadata, and the OCR path can reuse or bypass layout results explicitly instead of treating layout as an opaque backend detail.
- Decision: track

## Problem Fit

This repository informs `document-ai-ocr`, especially layout-aware extraction, OCR routing, and auditable page selection. The reusable mechanism is the separation between cheap page signals, expensive layout rendering, and metadata that records why a page was promoted or skipped.

## Verified Flow

`extract` and `extract_batch` expose the public API -> `core` and `engine` route work into format-specific extractors -> `pdf/layout_gate.rs` grades pages from spans, rules, graphics, and form widgets without decoding pixels -> `extractors/pdf/mod.rs` turns gate decisions into recorded metadata and reuses layout results for OCR only when the pages are safe to share -> `doctor` still probes runtime backends before extraction -> regression tests cover the skip/promote cases for prose, missing text, sparse pages, multi-column pages, table-like grids, rules, graphics, and forms.

- E1 source verified: `crates/xberg/src/lib.rs:50-70` exports the extraction core, cancellation, engine, doctor, pdf, OCR, and layout modules that make the public surface composable rather than monolithic.
- E1 source verified: `crates/xberg/src/pdf/layout_gate.rs:1-17,185-209,432-438` defines the pixel-free page gate, the per-page decision model, and the infallible `decide_pages` path.
- E1 source verified: `crates/xberg/src/extractors/pdf/mod.rs:706-742,763-860` converts gate decisions into OCR metadata and only reuses layout output when all pages ran the model and rotations are normalized.
- E2 test verified: `crates/xberg/src/pdf/layout_gate.rs:475-670` covers the page gate's skip/promote behavior across prose, sparse, column, table, ruled-line, graphics, and form cases.
- E2 test verified: `crates/xberg/tests/reading_order.rs`, `crates/xberg/tests/pipeline_integration.rs`, and `crates/xberg/tests/pdf_table_detection.rs` exercise downstream reading-order and PDF pipeline behavior against the promoted layout path.

## Architecture

Principal components:

- Public extraction API over a lazily composed engine and backend catalog.
- PDF layout gate that uses cheap geometry before any render-heavy pass.
- OCR/layout reuse bridge that stores gate decisions in metadata.
- Doctor subsystem for backend viability and cache hygiene.
- Cancellation and batch-mode helpers that keep long runs interruptible and scoped.
- Regression corpus that encodes the known document-edge cases.

Most interesting mechanism: the runtime now distinguishes three states for a PDF page, not two. A page can be skipped, promoted for layout, or reused for OCR metadata, and the gate reasons are preserved so the decision is auditable rather than implicit.

Baseline comparison: a simple OCR wrapper would render everything, run the model everywhere, and hide the reason a page was expensive. Xberg adds page-level pre-screening, metadata for the gate decision, and a reuse check that prevents layout output from being blindly recycled into OCR.

## Reuse Guidance

Reusable:

- Use a cheap, pixel-free gate before a heavy layout pass.
- Preserve gate reasons in metadata so skip/promote decisions stay explainable.
- Reuse layout output only when the runtime can prove the page set is compatible.
- Keep backend probing separate from the extraction path.

Do not copy:

- Do not copy the entire backend matrix unless we need it.
- Do not copy the PDF heuristics without corpus-specific validation.
- Do not couple reuse of layout output to undocumented side effects.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The gate logic is pure and unit-tested.
- The gate metadata is derived from the same decision model that drives extraction.
- The PDF path keeps OCR reuse and layout promotion explicit.
- The repository still carries substantial regression coverage around edge-case documents.

Experimental or incomplete for our needs:

- The backend matrix is broad and workload-dependent.
- Some extraction decisions still rely on heuristics that need corpus-specific tuning.
- The repository is large enough that the reusable core is easy to miss if you only read the top-level API.

Hidden costs and failure modes:

- False positives in the page gate can skip a page that should have been rendered.
- Over-promotion can erase the memory savings the gate is trying to create.
- Task-local batch mode can still be missed by detached work if the call tree is not careful.
- More backends means more environment-specific failure modes and more validation burden.

Adoption experiment:

Run one controlled PDF corpus through the layout gate, then compare the gate decisions, page-order metadata, and OCR reuse behavior against a forced backend failure and a forced all-layout pass.

## Candidate Patterns

- `layout-gated page pre-screen`
- `gate-reason metadata projection`
- `doctor-probed backend selection`
