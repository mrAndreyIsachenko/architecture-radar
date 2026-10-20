# 2026-10-20 document-ai-demand

- Source date range: 2026-02-08 to 2026-10-20
- Family: `document-ai-demand`
- Signal type: `operational-risk`
- Source class: `github`
- Evidence label: `M2 repeated pain`
- Labels: `M2 repeated pain`, `M4 workaround evidence`
- Signal types: `operational-risk`, `optimization-gap`, `workaround-economy`
- Source classes: `github`, `docs`
- Evidence labels: `M2 repeated pain`, `M4 workaround evidence`
- Notes: Docling users still hit OCR, layout, and provenance failures, but the public evidence still looks like technical pain rather than a proven standalone spend path.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://github.com/docling-project/docling/discussions | 2026-10-20 crawl | operational-risk | github | M2 repeated pain | The discussion board still shows recurring OCR, layout, provenance, and deployment questions. |
| https://github.com/docling-project/docling/discussions/4238 | 2026-09-13 discussion | optimization-gap | github | M2 repeated pain | The adaptive OCR fast-path proposal shows users benchmarking performance because the default pipeline is slow on some PDFs. |
| https://github.com/docling-project/docling/issues/4489 | 2026-10-01 issue | operational-risk | github | M2 repeated pain | PDF-aware OCR selection can become 8-12x slower with unchanged output. |
| https://github.com/docling-project/docling/issues/3780 | 2026-07-09 issue | operational-risk | github | M2 repeated pain | Layout misclassification can break export and chunking for a document. |
| https://github.com/docling-project/docling/issues/2963 | 2026-02-08 issue | operational-risk | github | M2 repeated pain | Corrupted PDF text layers can force a fallback to OCR. |
| https://github.com/docling-project/docling/blob/main/docs/examples/full_page_ocr.py | 2026-10-19 crawl | workaround-economy | docs | M4 workaround evidence | The example exists because users need an explicit full-page OCR fallback path. |
