# document-ai-demand signal note, 2026-10-27

- Source date range: 2026-10-01 to 2026-10-27 crawl.
- Family: `document-ai-demand`
Signal type: `operational-risk`
Source class: `github`
Evidence label: `M2 repeated pain`
Labels: `M2 repeated pain`
Notes: Docling still has recurring OCR, layout, and reading-order failures, but the public evidence does not yet show a paid external review workflow.
- Topic family: `document-ai-demand`

## Sources

| Source | URL | Date | Signal type | Source class | Evidence label | Notes |
|---|---|---|---|---|---|---|
| Docling issue 4489 | https://github.com/docling-project/docling/issues/4489 | Opened Oct 2026 | operational-risk | github | `M2 repeated pain` | Shape-triggered OCR now makes programmatic PDFs 8 to 12 times slower with unchanged output. |
| Docling issue 4181 | https://github.com/docling-project/docling/issues/4181 | Opened Sep 2026 | operational-risk | github | `M2 repeated pain` | Table-form grids can drop words entirely when the grid does not cover them. |
| Docling issue 2204 | https://github.com/docling-project/docling/issues/2204 | Opened Aug 2026 | operational-risk | github | `M2 repeated pain` | Reading order for a standard two-column PDF is still wrong. |
| Docling issue 4762 | https://github.com/docling-project/docling/issues/4762 | Opened Oct 2026 | operational-risk | github | `M2 repeated pain` | Text clipped at a cell border can be assigned to the wrong table cell. |
| Docling issue 4632 | https://github.com/docling-project/docling/issues/4632 | Opened Oct 2026 | operational-risk | github | `M2 repeated pain` | The reading-order model can get stuck processing forever and block conversion. |
