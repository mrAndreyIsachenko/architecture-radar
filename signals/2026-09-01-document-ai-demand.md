# Document AI Demand Signals 2026-09-01

- Family: `document-ai-demand`
- Source date range: 2025-08-05 to 2026-09-01
- Signal type: operational-risk
- Source class: github
- Evidence labels: `M2 repeated pain`, `M3 competitor proof`, `M4 workaround evidence`
- Labels: `M2 repeated pain`, `M3 competitor proof`, `M4 workaround evidence`
- Notes: Docling pain repeats across extraction, provenance, and OCR backend choice, but public money evidence is still missing.

## Sources
- `M2 repeated pain` | `operational-risk` | `github` | https://github.com/docling-project/docling/issues/3419 | Docling can silently produce empty output after a full pipeline run.
- `M2 repeated pain` | `workaround-economy` | `github` | https://github.com/docling-project/docling/discussions/1012 | Users still need custom provenance handling for page numbers.
- `M3 competitor proof` | `competitor-proof` | `github` | https://github.com/docling-project/docling.rs/blob/master/docs/PDF_CONFORMANCE.md | Docling.rs conformance docs show adjacent productization around provenance and layout.
- `M2 repeated pain` | `fragmentation` | `github` | https://github.com/docling-project/docling/issues/2495 | Users ask for alternate OCR backends to improve extraction quality.

## Notes
- The pain repeats, but there is still no public proof that teams buy an external extraction-quality review.
- Keep the family watchlisted until a paid document bundle review is requested.
