# run-llama/liteparse

- Repository: https://github.com/run-llama/liteparse
- Review date: 2026-08-23
- Current commit reviewed: `59b63ede9b3d7cde037b3e81e8b8d905691783c8`
- Commit date: 2026-08-22
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `document-ai-ocr`, especially layout-aware extraction, page and region provenance, and mixed-mode parsing where structural text should be available before expensive raster work. The reusable mechanism is the separation between cheap structural parsing and optional screenshot/OCR promotion, not the product name.

## Verified Flow

`LiteParseConfig` turns on/off OCR, screenshots, block extraction, page-error tolerance, provenance, crop bounds, and other output switches -> `LiteParse::parse` resolves `target_pages`, validates output mode, loads the document, extracts pages and outline, computes optional complexity, renders screenshots only when requested, and returns a `ParseResult` -> `apply_layout` runs classification once and fans the result out to markdown and optional block exports -> `screenshot_input` converts non-PDF input to PDF and rejects text-based formats instead of guessing -> tests verify screenshot rendering, block geometry, page numbering, and batch behavior.

- E1 source verified: `crates/liteparse/src/config.rs` defines the feature surface for OCR hedging, screenshots, block extraction, provenance, crop bounds, and page-error handling.
- E1 source verified: `crates/liteparse/src/parser.rs` defines `ParseResult`, `ScreenshotResult`, `apply_layout`, `parse`, and `screenshot_input`.
- E1 source verified: `crates/liteparse/src/layout.rs` defines the public serializable `LayoutBlock` / `LayoutCell` shape used across Rust, JSON, Python, Node, and WASM.
- E2 test verified: `crates/liteparse/tests/integration_test.rs` verifies screenshot rendering, screenshot rejection for text files, block geometry retention, and page alignment.
- E2 test verified: `packages/python/tests/test_parse_e2e.py`, `test_batch_e2e.py`, and `test_screenshot_e2e.py` exercise the Python surface, bounding boxes, max-pages behavior, and screenshot output shape.

## Architecture

Principal components:

- Configuration gate: `LiteParseConfig` defines the parse, OCR, render, and provenance knobs.
- Document parser: `LiteParse` loads input, merges OCR, and produces `ParseResult`.
- Layout projection: `apply_layout` and `layout.rs` expose the same structural decomposition to all bindings.
- Screenshot renderer: `render::render_document_pages` is only called when screenshots are requested.
- Integration tests: Rust and Python tests lock the public contract across bindings.

Most interesting mechanism: LiteParse keeps the structural parse authoritative and treats screenshots or block exports as opt-in projections of the same underlying document state. The classification pass is shared, the public layout shape is stable, and the screenshot path stays separate from the Markdown path.

Baseline comparison: a conventional document pipeline often rasterizes everything first or makes OCR a prerequisite for all downstream outputs. This repository does the opposite: parse structurally, then promote only the expensive artifacts that the caller actually asked for.

## Reuse Guidance

Reusable:

- Parse structure first and promote pixels only when a downstream consumer needs them.
- Expose one serializable layout shape across language bindings instead of separate native and foreign shapes.
- Keep page numbering and geometry stable even when optional outputs are disabled.
- Treat text-file screenshot rejection as a hard boundary, not a best-effort fallback.

Do not copy:

- Do not copy the whole backend matrix or assume every optional backend is available.
- Do not copy the document-conversion assumptions without adapting them to the target parser.
- Do not treat every config flag as a stable public contract unless you are willing to support it long term.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The config surface is explicit and well documented.
- The parser and layout types are intentionally cross-language.
- Integration tests cover screenshot output, block geometry, and page-order behavior.

Experimental or incomplete for our needs:

- The parser has many knobs and optional backends.
- Some behaviors depend on OCR or conversion tooling outside the repo.
- The public surface is broad enough that workload-specific validation is still required.

Hidden costs and failure modes:

- Optional screenshot and OCR paths can make runtime characteristics hard to predict.
- Crop, page-error, and form-field settings can change output shape in subtle ways.
- A caller that treats screenshots or blocks as canonical rather than derived can miss the distinction between source structure and promoted artifacts.

Adoption experiment:

Use the structural-first pattern for one document pipeline in our stack, then verify that turning screenshots and block exports on and off does not perturb the parsed text or page numbering.

## Candidate Patterns

- `layout-preserving structural parse with optional promotion`
