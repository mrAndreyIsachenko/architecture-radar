# 2026-11-10 document-ai-demand

- Source date range: 2026-09-13 to 2026-11-10
- Family: `document-ai-demand`
Signal type: `operational-risk`
Source class: `github`
Evidence label: `M2 repeated pain`
Labels: `M2 repeated pain`, `M4 workaround evidence`
Notes: Docling continues to show recurring OCR, table, and provenance pain, but the buyer path is still weak because the useful validation path usually needs a customer's own PDFs.
- Topic family: `document-ai-demand`

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://github.com/docling-project/docling/discussions | 2026-11-09 crawl | operational-risk | github | M2 repeated pain | The discussion board still shows recurring OCR, layout, provenance, and deployment questions. |
| https://github.com/docling-project/docling/discussions/4238 | 2026-10-09 | optimization-gap | github | M2 repeated pain | Users are benchmarking an adaptive OCR fast path because the default pipeline is too slow on born-digital PDFs. |
| https://github.com/docling-project/docling/issues/3473 | 2026-05-18 | operational-risk | github | M2 repeated pain | OCR'd table text can vanish from the markdown serializer when the body tree never references it. |
| https://github.com/docling-project/docling/issues/4762 | 2026-10-10 | operational-risk | github | M2 repeated pain | Text clipped at a cell border can be assigned to neighboring cells, which breaks extraction quality. |
| https://github.com/docling-project/docling/blob/main/docs/concepts/OCR.md | 2026-11-03 crawl | workaround-economy | docs | M4 workaround evidence | The OCR docs enumerate multiple engines and flags because teams still tune extraction behavior by hand. |
- Topic family: `document-ai-demand`

## Sources
- `https://github.com/docling-project/docling/discussions`
  - Signal: `operational-risk`
  - Class: `github`
  - Label: `M2 repeated pain`
  - Note: The discussion board still shows recurring OCR, layout, provenance, and deployment questions.
- `https://github.com/docling-project/docling/discussions/4238`
  - Signal: `optimization-gap`
  - Class: `github`
  - Label: `M2 repeated pain`
  - Note: Users are benchmarking an adaptive OCR fast path because the default pipeline is too slow on born-digital PDFs.
- `https://github.com/docling-project/docling/issues/3473`
  - Signal: `operational-risk`
  - Class: `github`
  - Label: `M2 repeated pain`
  - Note: OCR'd table text can vanish from the markdown serializer when the body tree never references it.
- `https://github.com/docling-project/docling/issues/4762`
  - Signal: `operational-risk`
  - Class: `github`
  - Label: `M2 repeated pain`
  - Note: Text clipped at a cell border can be assigned to neighboring cells, which breaks extraction quality.
- `https://github.com/docling-project/docling/blob/main/docs/concepts/OCR.md`
  - Signal: `workaround-economy`
  - Class: `docs`
  - Label: `M4 workaround evidence`
  - Note: The OCR docs enumerate multiple engines and flags because teams still tune extraction behavior by hand.
