# Research Scope

Domain configuration for the Architecture Radar agent. This file answers **what to look for**.

The operating rules — how to discover, verify, and record findings — live in [`agent-rules.md`](agent-rules.md) and are domain-independent. To point the radar at a different subject area, replace this file and `interests.md`; leave `agent-rules.md` alone.

`interests.md` remains authoritative for concrete unresolved problems. This file only widens or narrows the search surface.

## Topic Families

Use these families for candidate accounting and per-topic selection. They match the families defined in `interests.md`:

- `ai-llm-systems`
- `blockchain-intelligence`
- `privacy-networking-vpn`
- `drones-robotics-autonomy`

## Research Areas

Prioritize repositories related to:

- AI systems and LLM infrastructure
- AI agents and agent runtimes
- LLM evaluation, memory, context engineering, and tool use
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

A mechanism at this level survives removal of the repository's branding, UI, and product domain. A finding that does not survive that removal is a product observation, not a mechanism.
