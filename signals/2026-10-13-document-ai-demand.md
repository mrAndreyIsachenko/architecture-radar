# 2026-10-13 document-ai-demand

- Source date range: 2026-05-12 to 2026-10-13
- Family: `document-ai-demand`
Signal type: `operational-risk`
Source class: `github`
Evidence label: `M2 repeated pain`
Labels: `M2 repeated pain`, `M4 workaround evidence`
Notes: Docling discussions and issues keep surfacing OCR, provenance, and layout failures, and users are already building downstream quality checks around its output. Public evidence still stops short of paid demand for a standalone review service.
- Topic family: `document-ai-demand`

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://github.com/docling-project/docling/discussions | 2026-10-13 crawl | operational-risk | github | M2 repeated pain | The discussion board still shows recurring OCR, layout, provenance, and deployment questions. |
| https://github.com/docling-project/docling/discussions/4238 | 2026-09-13 | optimization-gap | github | M2 repeated pain | Users are benchmarking an adaptive OCR fast path because the default pipeline is too slow on born-digital PDFs. |
| https://github.com/docling-project/docling/discussions/3437 | 2026-05-12 | workaround-economy | github | M4 workaround evidence | Users are already building a downstream quality checker around Docling JSON output. |
| https://github.com/docling-project/docling/issues/3887 | 2026-07-27 | operational-risk | github | M2 repeated pain | Full-page OCR is blocked by a UnicodeDecodeError before OCR can run. |
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
- `https://github.com/docling-project/docling/discussions/3437`
  - Signal: `workaround-economy`
  - Class: `github`
  - Label: `M4 workaround evidence`
  - Note: Users are already building a downstream quality checker around Docling JSON output.
- `https://github.com/docling-project/docling/issues/3887`
  - Signal: `operational-risk`
  - Class: `github`
  - Label: `M2 repeated pain`
  - Note: Full-page OCR is blocked by a UnicodeDecodeError before OCR can run.
