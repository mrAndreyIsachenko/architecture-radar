# 2026-09-29 Document AI Demand Signals

- Family: `document-ai-demand`
- Source date range: 2026-09-29 crawl, with current issues, discussions, and provenance docs.
- Signal type: `operational-risk`
- Source class: `github`
- Signal types: `operational-risk`, `workaround-economy`
- Source classes: `github`, `docs`
- Market evidence labels: `M2 repeated pain`, `M4 workaround evidence`
- Labels: `M2 repeated pain`, `M4 workaround evidence`
- Notes: Docling still shows recurring OCR, provenance, and layout pain. The public evidence is strong on technical friction but still weak on direct willingness to pay for an external review service.

## Sources

- `https://github.com/docling-project/docling/issues/3887` | source class: `github` | signal type: `operational-risk` | evidence label: `M2 repeated pain` | note: Full-page OCR is blocked by a UnicodeDecodeError before OCR can run.
- `https://github.com/docling-project/docling/issues/960` | source class: `github` | signal type: `operational-risk` | evidence label: `M2 repeated pain` | note: Users still report unreadable or gibberish output on messy PDFs.
- `https://github.com/docling-project/docling/discussions/3192` | source class: `github` | signal type: `workaround-economy` | evidence label: `M4 workaround evidence` | note: Users describe OCR quality problems and ask for force-full-page-OCR style workarounds.
- `https://github.com/docling-project/docling/discussions/3437` | source class: `github` | signal type: `workaround-economy` | evidence label: `M4 workaround evidence` | note: A small quality checker project exists because users want a separate validation layer before downstream use.
- `https://github.com/docling-project/docling-graph/blob/main/docs/fundamentals/graph-management/provenance.md` | source class: `docs` | signal type: `workaround-economy` | evidence label: `M4 workaround evidence` | note: Provenance docs show the structured metadata path that downstream teams want to inspect and reconcile.

| URL | Source date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|
| https://github.com/docling-project/docling/issues/3887 | 2026-09-29 crawl | operational-risk | github | M2 repeated pain | Full-page OCR is blocked by a UnicodeDecodeError before OCR can run. |
| https://github.com/docling-project/docling/issues/960 | 2026-09-29 crawl | operational-risk | github | M2 repeated pain | Users still report unreadable or gibberish output on messy PDFs. |
| https://github.com/docling-project/docling/discussions/3192 | 2026-09-29 crawl | workaround-economy | github | M4 workaround evidence | Users describe OCR quality problems and ask for force-full-page-OCR style workarounds. |
| https://github.com/docling-project/docling/discussions/3437 | 2026-09-29 crawl | workaround-economy | github | M4 workaround evidence | A small quality checker project exists because users want a separate validation layer before downstream use. |
| https://github.com/docling-project/docling-graph/blob/main/docs/fundamentals/graph-management/provenance.md | 2026-09-29 crawl | workaround-economy | docs | M4 workaround evidence | Provenance docs show the structured metadata path that downstream teams want to inspect and reconcile. |
