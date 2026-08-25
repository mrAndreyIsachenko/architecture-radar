# Docling Provenance And Layout Extraction Diagnostics

## Opportunity Summary
Docling users keep hitting OCR, layout, provenance, and large-PDF failure modes. The opportunity is a manual extraction-quality review that tells a document-AI team whether their pipeline is trustworthy before they spend more time on backend tuning or reruns.

## Evidence
- M2 repeated pain: issue `#3002` reports native PDF content being parsed as images, which breaks downstream extraction.
- M2 repeated pain: issue `#3671` reports failures or silent errors on large PDFs and points at memory accumulation issues.
- M2 repeated pain: issue `#2036` asks how to include page numbers in markdown and conditional OCR when text is missing.
- M4 workaround evidence: discussions and issues describe exporting to PDF, switching backends, or using custom chunkers/serializers to recover provenance and page numbering.
- M3 competitor proof: the Rust port and conformance material show active productization and a growing tooling ecosystem around document extraction.
- H hypothesis: public sources show pain, but not direct spend for an external review service.

## Structural Pattern
Extraction and provenance control layer for multimodal document workflows.

## Primitive Growth
Docling, Docling.rs, OCR and layout models, and multimodal document ingestion workflows all became more visible in 2025-2026.

## Fragmentation
Teams still juggle OCR, layout recovery, provenance, page numbering, embedded images, and backend choices.

## Manual Workflow
People rerun documents, split PDFs, swap backends, and inspect outputs by hand to understand why extraction quality changed.

## Objective Function
Maximize extraction fidelity, provenance completeness, and layout recovery while minimizing memory use and manual QA time.

## Execution Ladder
- Observe: inspect sample PDFs, error logs, and output diffs.
- Recommend: flag likely OCR, layout, or provenance failure modes.
- Choose: rank backend or preprocessing options against accuracy and memory constraints.
- Execute: deliver a manual extraction-quality report before any software is built.

## Economic Pain
Bad extraction causes reruns, broken RAG inputs, manual QA, and engineering time spent on backend tuning.

## Timing Reason
Multimodal document extraction, OCR quality pressure, and the Rust port make the workflow more inspectable in 2025-2026, but the commercial proof is still weak.

## Competitors
- Docling.rs
- pypdfium2 or other backend workarounds
- custom chunkers and serializers
- internal extraction scripts

## Structural Scores
- Fragmentation: 4
- Manual pain: 4
- Economic value: 3
- Objective measurability: 4
- Execution potential: 3
- Timing: 4
- Competition gap: 2
- Prototype feasibility: 4
- Total: 7

## Repeated Pain Or Demand Signal
Teams want extraction that preserves page structure and provenance without silent failures or repeated reruns.

## Likely User Or Buyer
Document AI teams, compliance workflows, and RAG teams processing messy PDFs and office documents.

## Current Workaround Or Money Signal
People switch backends, split PDFs, inspect markdown manually, or build custom chunkers to recover page numbers and provenance.

## Money Evidence Type
no_money_evidence

## Money Evidence
Public issues show technical pain and manual diagnosis, but no direct public spend for an external extraction-quality report was found.

## Existing Paid Workflow
Teams already spend on OCR, parsing, cloud compute, and document-processing labor, but not clearly on a third-party Docling review.

## Current Workaround
Teams rerun documents, split PDFs, swap OCR backends, and inspect outputs by hand to recover quality and provenance.

## Current Cost
Engineering time and rerun cost; no clean public dollar estimate was found.

## Why Buy From Us
A buyer would only buy if a short report identifies the true failure mode faster than repeated reruns and backend experiments.

## Why Buyer Would Buy From Us
A buyer would only buy if a short report identifies the true failure mode faster than repeated reruns and backend experiments.

## Build-vs-buy Reason
This is near the core of document-processing quality, so many buyers will build or tune internally unless a report proves recurring value.

## Smallest Sellable Outcome
One manual extraction-quality report for a small failing document bundle.

## Manual First Delivery
Run a few sample PDFs, compare outputs, and summarize quality, provenance, and layout gaps by hand.

## One-Sentence Offer
Send me a failing PDF bundle and we will return a provenance and extraction-quality report within 48 hours.

## Price Hypothesis
unclear

## Buyer Acquisition Path
Docling issues and discussions, document AI communities, RAG teams, and public data-extraction vendors.

## Time To Transaction
2

## Time To Transaction Reason
The pain is obvious, but direct spend is missing and useful validation may still require the buyer's own documents.

## Productization Path
If repeated reviews land, convert the report into a small CLI or hosted check that scores extraction quality and provenance.

## Cashflow Falsification Test
If three teams with failing PDFs will not share examples or pay for a manual review, keep this in watchlist.

## Technology Shift
- What changed: Docling.rs, newer OCR/model options, and larger multimodal document pipelines made quality tradeoffs more visible.
- When: 2025-2026, with the strongest public issue cluster in 2026.
- Old constraint: teams had to debug layout, provenance, and OCR failures by manually reading outputs.
- New capability: a report can compare backends and quality failures across sample documents.
- Cost delta: unclear.
- Quality delta: better extraction is possible, but silent failures still appear.
- Latency delta: unclear.
- Accessibility delta: public issues, docs, and the Rust port make the workflow easier to inspect.
- Affected workflows: PDF extraction, RAG ingestion, provenance capture, and large-document processing.

## Buyer
Document AI teams, compliance workflows, and RAG teams processing messy PDFs and office documents.

## Expensive Workflow
Rerunning documents, inspecting outputs, and tuning OCR or layout pipelines after extraction failures.

## Existing Spend
Teams already spend on OCR, parsing, cloud compute, and document-processing labor.

## Paid Experiment
Ask three reachable teams with failing PDFs whether they would pay for a manual extraction-quality report before proposing software.

## Money-First Scores
- Pain: 4
- Spend: 1
- Reachability: 3
- Timing: 3
- Buildability: 3

## Source Classes
- github

## Fragmented Providers
Docling, Docling.rs, OCR backends, layout models, provenance serializers, and downstream document pipelines.

## Multi-Provider User
Document teams often mix Docling with OCR engines, parsing backends, storage systems, and downstream embedding or RAG tooling.

## Boundary Workflow
The boundary workflow is reconciling OCR output, layout recovery, provenance, page numbering, and backend choice across document-processing stages.

## Build-vs-Buy Reason
This is near the core of document-processing quality, so many buyers will build or tune it internally unless a report proves recurring value.

## Internal Build Likelihood
high

## Money Flow
Money flows through OCR vendors, cloud compute, parsing labor, and downstream application teams, but not through a proven third-party review workflow.

## Recurrence
Every new document type, backend change, or failing PDF revives the same extraction and provenance debugging work.

## Permissionless Validation
Public examples can demonstrate formatting and output diffs, but a real buyer likely needs its own documents for final validation.

## Smallest Wedge
One failing document bundle reviewed for extraction quality, provenance, and layout drift.

## Intermediary Maturity
Partial: the ecosystem has several tools and backends, but the independent review layer is immature.

## Paid Wedge
Reduce reruns and manual QA on document extraction failures.

## Distribution Channel
Report-first outreach through document AI communities and public issue/discussion threads.

## Private Data Barrier
private-data-required

## OSS Commoditization Risk
medium

## Product Shape
report

## Pricing Hypothesis
unclear

## Do Not Build Until
One team pays for a manual extraction-quality report or three teams share representative failing documents for analysis.

## Proposed Offer
Send me a failing PDF bundle and we will return a provenance and extraction-quality report within 48 hours.

## Success Threshold
One team pays for a manual extraction-quality report or three teams share representative failing documents for analysis.

## Falsification Threshold
If three teams with failing PDFs will not share examples or pay for a manual review, keep this in watchlist.

## Evidence Gaps
- Docling pain is repeatable, but public money evidence is still missing for an external extraction-quality review.

## Labels
- M2 repeated pain
- M4 workaround evidence
- M3 competitor proof
- H hypothesis

## Decision
Watchlisted. Technical pain is real, but direct money evidence and fast validation are still missing.
