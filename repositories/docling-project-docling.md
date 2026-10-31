# docling-project/docling

- Repository: https://github.com/docling-project/docling
- Review date: 2026-10-31
- Current commit reviewed: `764b5d4dc22b03ea87afd4c2207f510300b27a5b`
- Commit date: 2026-10-31T13:14:48+08:00
- Branch: `main`
- Previous commit reviewed: `890dd42d017497c955a56a1d2cfc3f0af5bc2aa9`
- Material changes since previous review: the current head adds spreadsheet-specific rich-value image handling. XLSX cells that carry image payloads now become picture-backed table cells, fallback error cells can be re-associated with their image content, and singleton image sheets can be promoted without losing table provenance or section labels.
- Decision: track

## Problem Fit

This repository informs `document-ai-ocr`, especially spreadsheet provenance, layout-aware extraction, and mixed text/image document parsing. The reusable mechanism is narrower than the broader deferred-image pattern: Docling now materializes cell-level images only when the XLSX rich-value metadata or fallback cell state proves that a cell actually contains an image payload.

## Verified Flow

`DocumentConverter.convert` / `DocumentConverter.__call__` -> `MsExcelBackend` opens the workbook and routes through rich-value parsing -> `_read_rich_value_images` inspects the workbook relationships and extracts image references attached to cells -> `_find_cell_images` maps both explicit rich-value cells and fallback error cells back to their image payloads -> `_find_data_tables` and `_split_leading_section_label` preserve table boundaries and leading labels -> `doc.add_table`, `doc.add_table_cell`, `RichTableCell`, and `_add_cell_image` attach the image to the table structure -> singleton promotion through `treat_singleton_as_text` keeps one-cell image sheets from being flattened into a useless table shell -> tests assert image-cell promotion, singleton handling, and label retention.

- E1 source verified: `docling/backend/msexcel_backend.py:360-494` reads rich-value image metadata and resolves cell-level image references.
- E1 source verified: `docling/backend/msexcel_backend.py:1395-1485` maps fallback error cells back to image content and builds table-aware cell records.
- E1 source verified: `docling/backend/msexcel_backend.py:2101-2165` preserves table structure while promoting singleton or image-heavy sheets through the table pipeline.
- E1 source verified: `docling/datamodel/backend_options.py:466-476` exposes the spreadsheet backend option that controls singleton treatment.
- E2 test verified: `tests/test_backend_msexcel.py:1290-1319` verifies image cells are surfaced through the rich-value path.
- E2 test verified: `tests/test_backend_msexcel.py:1321-1339` verifies singleton image-sheet promotion does not corrupt the output shape.
- E2 test verified: `tests/test_backend_msexcel.py:1341-1369` verifies section labels and table provenance remain intact.

## Architecture

Principal components:

- XLSX backend logic that inspects workbook metadata before emitting table cells.
- Rich-value image extraction and fallback cell recovery.
- Table assembly helpers that preserve provenance while attaching image payloads.
- Backend options that tune how singleton sheets are promoted.
- Regression tests that pin image-cell, singleton, and label behavior.

Most interesting mechanism: the backend does not treat every spreadsheet cell as text-first. It inspects XLSX rich-value relationships and fallback error cells, then materializes picture-backed table cells only where the workbook itself proves there is image content. That keeps the parse structurally honest while still preserving image evidence.

Baseline comparison: a simpler spreadsheet extractor would either ignore cell images or flatten them into generic blobs. Docling instead keeps the table structure, associates the image with the cell, and retains section labels so downstream consumers can reason over provenance.

## Reuse Guidance

Reusable:

- Materialize image payloads only when workbook metadata proves the cell carries them.
- Preserve table provenance when promoting cell images into the parse tree.
- Keep singleton image-sheet promotion behind an explicit option.
- Retain section labels even when the data path upgrades a sheet into a richer structure.

Do not copy:

- Do not copy the XLSX-specific parsing assumptions into a format that does not have workbook relationships.
- Do not flatten rich-value images into unlabelled attachments if provenance matters.
- Do not treat singleton promotion as a universal default without checking consumer expectations.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The rich-value path is implemented in source rather than left as a docstring-only promise.
- Tests cover the new spreadsheet behavior and the provenance-preserving promotion rules.
- The backend option makes the singleton promotion policy explicit.

Experimental or incomplete for our needs:

- The current evidence is source-and-test backed, but it still needs a runtime validation pass on mixed workbook corpora.
- The promotion logic is specific to XLSX semantics; other spreadsheet formats may need different provenance handling.
- The path is careful about structure, but it still depends on workbook metadata being accurate.

Hidden costs and failure modes:

- If rich-value metadata is missing or malformed, image cells can degrade to plain text or fallback cells.
- Over-promoting singleton sheets can obscure when a workbook was actually just a single figure.
- Misaligned table provenance can make downstream consumers believe a cell belongs to the wrong table.

Adoption experiment:

Run a mixed workbook corpus with rich-value image cells, plain error cells, singleton image sheets, and section labels, then confirm that image cells become picture-backed table cells, fallback cells retain their image content, and the output preserves table provenance.

## Candidate Patterns

- `Deferred Image Materialization`
- `spreadsheet rich-value image projection`
- `table-provenance preserving image promotion`

## Previous Review

The [2026-09-19 report](../reports/2026-09-19.md) and the previous card covered the broader PDF and layout pipeline at `890dd42d017497c955a56a1d2cfc3f0af5bc2aa9`. This current review adds the XLSX rich-value image-cell path at `764b5d4dc22b03ea87afd4c2207f510300b27a5b`.
