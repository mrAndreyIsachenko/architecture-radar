# 2026-11-17 document-ai-demand

- Source date range: 2026-05-18 to 2026-11-03
- Family: `document-ai-demand`
- Signal type: `operational-risk`
- Source class: `github`
- Labels: `M2 repeated pain`, `M4 workaround evidence`
- Notes: Docling still shows OCR, layout, and provenance failures, and users are already building recovery logic around its output. Public evidence still stops short of direct spend for a standalone review service.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://github.com/docling-project/docling/issues/4083 | 2026-08-27 | operational-risk | github | M2 repeated pain | CJK PDFs still produce table row and cell misalignment after the layout-driven OCR pipeline change. |
| https://github.com/docling-project/docling/discussions/4238 | 2026-09-13 | optimization-gap | github | M2 repeated pain | Users are benchmarking an adaptive OCR fast path because the default pipeline is too slow on born-digital PDFs. |
| https://github.com/docling-project/docling/issues/3473 | 2026-08-11 | workaround-economy | github | M4 workaround evidence | OCR text inside table regions can vanish from markdown, so users build downstream recovery logic. |
| https://github.com/docling-project/docling/issues/3839 | 2026-07-26 | operational-risk | github | M2 repeated pain | OCR text on rotated images is still dropped in a real reproduction. |
| https://github.com/docling-project/docling/issues/5157 | 2026-11-03 | operational-risk | github | M2 repeated pain | Invisible OCR text layers can duplicate output instead of merging cleanly. |

## Sources
- `https://github.com/docling-project/docling/issues/4083`
- `https://github.com/docling-project/docling/discussions/4238`
- `https://github.com/docling-project/docling/issues/3473`
- `https://github.com/docling-project/docling/issues/3839`
- `https://github.com/docling-project/docling/issues/5157`
