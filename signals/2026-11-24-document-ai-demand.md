# 2026-11-24 document-ai-demand

- Source date range: 2026-09-13 to 2026-11-24
- Family: `document-ai-demand`
- Signal type: `operational-risk`
- Source class: `github`
- Labels: `M2 repeated pain`, `M4 workaround evidence`
- Topic family: `document-ai-demand`

Notes: Docling still shows repeated OCR, layout, provenance, and performance regressions, but the public evidence still looks like technical pain rather than proven standalone spend.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://github.com/docling-project/docling/issues | 2026-11-24 crawl | operational-risk | github | M2 repeated pain | The live issue feed keeps surfacing OCR, layout, and provenance regressions. |
| https://github.com/docling-project/docling/discussions | 2026-11-24 crawl | optimization-gap | github | M2 repeated pain | The discussion board still contains repeated questions about OCR quality and extraction strategy. |
| https://github.com/docling-project/docling/issues/4489 | 2026-10-01 | optimization-gap | github | M2 repeated pain | PDF-aware OCR selection is 8-12x slower with unchanged output on some documents. |
| https://github.com/docling-project/docling/issues/5157 | 2026-11-03 | operational-risk | github | M2 repeated pain | OCR text can be duplicated beside flat text-layer cells. |
| https://github.com/docling-project/docling/discussions/4238 | 2026-09-13 | optimization-gap | github | M2 repeated pain | An adaptive OCR fast path was proposed because the default pipeline is too slow on born-digital PDFs. |
| https://github.com/docling-project/docling/blob/main/docs/concepts/OCR.md | 2026-11-24 crawl | workaround-economy | docs | M4 workaround evidence | The OCR docs show a complex, tunable pipeline with separate layout and OCR options. |
