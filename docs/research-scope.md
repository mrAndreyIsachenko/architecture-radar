# Research Scope

Domain configuration for the Architecture Radar agent. This file answers **what to look for**.

The operating rules — how to discover, verify, and record findings — live in [`agent-rules.md`](agent-rules.md) and are domain-independent. To point the radar at a different subject area, replace this file and `interests.md`; leave `agent-rules.md` alone.

`interests.md` remains authoritative for concrete unresolved problems. This file only widens or narrows the search surface.

## Topic Families

Use these families for candidate accounting and per-topic selection. They match the families defined in `interests.md`:

- `ai-llm-systems`
- `document-ai-ocr`
- `blockchain-intelligence`
- `privacy-networking-vpn`
- `drones-robotics-autonomy`

## Research Areas

Prioritize repositories related to:

- AI systems and LLM infrastructure
- AI agents and agent runtimes
- LLM evaluation, memory, context engineering, and tool use
- document AI, OCR, VLM document parsing, layout extraction, PDF/table/form parsing, and multimodal evidence ingestion
- OCR/document parsing model releases, runtime adapters, eval harnesses, and deployment failure modes
- event intelligence and event correlation
- OSINT and real-time monitoring
- knowledge graphs and GraphRAG
- semantic layers and metadata systems
- data lineage and provenance
- evidence-backed reasoning
- execution traces and observability
- codebase intelligence
- blockchain indexing and transaction interpretation
- wallets, protocol analysis, and on-chain intelligence
- VPN, privacy networking, secure tunnels, traffic routing, and access control
- drones, robotics, autonomy, mission planning, telemetry, and fleet coordination
- durable workflows and long-running agents

Every selected repository must map to at least one concrete unresolved problem or research priority explicitly present in `interests.md`.

Broad topical similarity alone is insufficient.

## Mechanisms Of Interest

Examples of the abstraction level worth extracting. Not a checklist — a calibration of granularity:

- delta detection
- event correlation
- temporal memory
- evidence provenance
- page and region provenance
- layout-aware extraction
- entity resolution
- workflow recovery
- semantic execution graphs
- confidence propagation
- tool registries
- incremental indexing
- human review queues
- consistency guards
- policy generation and invalidation
- deterministic projection from event logs
- model release watchlists when a model materially changes an evidence-ingestion capability

A mechanism at this level survives removal of the repository's branding, UI, and product domain. A finding that does not survive that removal is a product observation, not a mechanism.

## Discovery Seeds

Use these as search anchors and comparison baselines, not as automatic selections.

Document AI / OCR / multimodal evidence ingestion:

- `baidu/Unlimited-OCR`
- `deepseek-ai/DeepSeek-OCR`
- `PaddlePaddle/PaddleOCR`
- `studio-dots-ai/dots.ocr`
- `allenai/olmocr`
- `ds4sd/docling`
- `datalab-to/marker`
- `run-llama/ParseBench`
- `Layout-Parser/layout-parser`

When a seed is model-heavy or benchmark-heavy rather than source-heavy, apply the model/research release watch rules in `docs/agent-rules.md` instead of forcing a deep review.

## Watchlist

`watchlist.yml` is the explicit override for repositories or adjacent artifacts that broad discovery must not miss. The watchlist is for high-signal items that may fail normal discovery because they lack GitHub Releases, topics, large source trees, or obvious architecture keywords.

Watchlist entries are not automatic recommendations. They force accounting:

- inspect or explicitly defer the entry;
- record the exact decision in the candidate ledger;
- use `watch-model`, `watch-dataset`, `watch-benchmark`, `watch-runtime`,
  `watch-company`, `watch-product`, or `watch-launch` when source-level deep
  review is not the right unit;
- perform company-to-repository expansion for company, product, launch, or
  runtime seeds before deciding that there is no inspectable source;
- prefer companion runtime/eval/adapter repositories when the primary
  repository is model-heavy or the company launch points to adjacent code under
  a different organization or product name.
