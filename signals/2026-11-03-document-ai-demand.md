# 2026-11-03 document-ai-demand

- Source date range: 2026-05-17 to 2026-11-03
- Family: `document-ai-demand`
- Signal type: `operational-risk`
- Source class: `github`
- Evidence labels: `M2 repeated pain`, `M4 workaround evidence`
- Labels: `M2 repeated pain`, `M4 workaround evidence`
- Notes: Docling keeps surfacing OCR, table, order, and provenance issues. There is strong technical pain, but the public spend signal for an external review wedge is still absent.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://github.com/docling-project/docling/issues/4489 | 2026-10-01 | operational-risk | github | M2 repeated pain | PDF-aware OCR selection gets 8-12x slower with unchanged output on many admin documents. |
| https://github.com/docling-project/docling/issues/3473 | 2026-05-18 | operational-risk | github | M2 repeated pain | OCR text inside a table region vanishes from `md_content`. |
| https://github.com/docling-project/docling/issues/4189 | 2026-09-06 | optimization-gap | github | M2 repeated pain | Table cell matching can merge adjacent columns and produce self-inconsistent output. |
| https://github.com/docling-project/docling/issues/3464 | 2026-05-17 | workaround-economy | github | M4 workaround evidence | Users want OCR skipped when a usable text layer already exists. |
| https://github.com/docling-project/docling/issues/2204 | 2026-08-17 | operational-risk | github | M2 repeated pain | Two-column PDFs still produce incorrect reading order. |
