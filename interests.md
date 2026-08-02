# Architecture Radar Interests

This file is the authoritative source for Architecture Radar research priorities. Repository analysis must connect findings to concrete problems listed here rather than inferred project needs.

## Topic Scope

The radar should cast a wider net than the initial project list. Repositories may be relevant when they expose reusable engineering mechanisms in:

- AI systems, LLM infrastructure, agents, evaluation, memory, context engineering, and tool use.
- Blockchain indexing, transaction interpretation, wallets, protocol analysis, and on-chain intelligence.
- VPN, privacy networking, secure tunnels, traffic routing, access control, censorship resistance, and network observability.
- Drones, robotics, autonomy, fleet coordination, mission planning, telemetry, ground control, perception, and safety/recovery systems.

Broad topical relevance is not enough. A selected repository still needs an inspectable mechanism, source evidence, and a concrete link to an open problem below.

Use these top-level topic families for candidate accounting and per-topic selection:

- `ai-llm-systems`: AI agents, LLM infrastructure, evaluation, memory, context engineering, knowledge layers, event intelligence, OSINT, metadata, lineage, observability, and codebase intelligence.
- `blockchain-intelligence`: blockchain indexing, transaction interpretation, wallets, protocol analysis, address/entity attribution, and on-chain intelligence.
- `privacy-networking-vpn`: VPN, private networking, secure tunnels, mesh networking, traffic routing, access control, censorship resistance, and network observability.
- `drones-robotics-autonomy`: drones, robotics, autonomy, mission planning, telemetry, ground control, perception, fleet coordination, safety, and recovery systems.

## Current Priorities

### LLM systems, evaluation, memory, and context engineering

We need mechanisms for building reliable LLM-powered systems beyond simple chat or prompt wrappers.

Open problems:

- Evaluate agent, tool-use, retrieval, and reasoning behavior with reproducible evidence.
- Version prompts, model settings, context construction, tools, memory writes, and evaluation datasets.
- Preserve provenance from source material through context assembly to model outputs and downstream actions.
- Manage long-context selection, compression, eviction, and retrieval without losing auditability.
- Compare models and agent policies using task-level traces rather than isolated benchmark scores.

Useful mechanisms:

- LLM evaluation harnesses.
- Trace-backed model comparison.
- Context assembly pipelines.
- Memory write policies.
- Prompt and tool-schema versioning.
- Evidence-aware judges and graders.
- Regression tests for agent behavior.

Avoid:

- Prompt collections.
- Generic chat UIs.
- Benchmarks with no reproducible harness or source evidence.
- Memory systems that cannot explain why information was written, retrieved, or trusted.

### Evidence-backed semantic execution graph

We need a way to represent agent, workflow, data, and research activity as evidence-carrying execution graphs.

Open problems:

- Model execution steps, tool calls, inputs, outputs, retries, and derived artifacts with stable provenance.
- Preserve parent-child causality across long-running workflows and human review.
- Attach evidence hashes, source references, confidence, and decision rationale to derived conclusions.
- Support replay, audit explanations, and partial recomputation.

Useful mechanisms:

- Semantic execution graphs.
- Evidence envelopes.
- Deterministic projection from event logs.
- Provenance propagation.
- Confidence scoring.
- Trace normalization across tools.

Avoid:

- Unverifiable narrative summaries.
- Graph models that cannot preserve source evidence.
- Systems that require all execution to happen inside one proprietary runtime.

### Blockchain transaction interpretation

We need mechanisms for interpreting blockchain transactions and protocol behavior beyond raw indexing.

Open problems:

- Reconstruct user intent from contract calls, internal transfers, logs, traces, and token movements.
- Map low-level execution traces to domain-level events.
- Explain causality across transactions, contracts, addresses, and time windows.
- Maintain provenance from interpretation back to chain evidence.
- Handle reorgs, partial data, ambiguous ABIs, and protocol-specific semantics.
- Detect suspicious flows, bridge behavior, MEV, liquidation, wallet behavior, and protocol-specific state transitions.

Useful mechanisms:

- Incremental indexing.
- Event sourcing.
- Trace decoding pipelines.
- Entity resolution.
- Confidence-aware interpretation.
- Reorg-safe materialization.
- Address clustering and wallet/entity attribution with explicit uncertainty.
- Protocol adapters with provenance-preserving outputs.

Avoid:

- Indexers that only expose generic SQL over raw chain data.
- Hard-coded protocol interpretations without provenance.
- Architectures that cannot recover from chain reorganizations.
- Wallet dashboards that do not expose interpretation evidence.

### Privacy networking, VPN, and traffic-control systems

We need mechanisms for secure private networking, policy-controlled tunnels, and observable network access without turning the radar into consumer VPN product tracking.

Open problems:

- Provision peers, keys, routes, DNS, and access policies safely across many devices or environments.
- Rotate and revoke credentials without breaking active sessions unexpectedly.
- Support split tunneling, policy routing, NAT traversal, relay fallback, and multi-hop paths.
- Preserve useful observability while minimizing sensitive traffic/content exposure.
- Detect misconfiguration, DNS leaks, route leaks, captive portals, blocked transports, and degraded connectivity.
- Apply least-privilege access control to networks, hosts, services, and developer/admin workflows.

Useful mechanisms:

- WireGuard/OpenVPN control planes.
- Mesh networking coordination.
- Policy-based routing.
- Key lifecycle management.
- Capability-scoped network access.
- Connectivity probes and health models.
- DNS and traffic leak detection.
- Relay selection and failover.

Avoid:

- Consumer VPN ranking sites or marketing clients.
- Projects whose only mechanism is wrapping WireGuard commands with a UI.
- Traffic inspection designs that require unnecessary content capture.
- Security claims without tests, threat model, or operational evidence.

### Drones, robotics, autonomy, and telemetry

We need mechanisms from drone and robotics systems that can inform long-running autonomous agents, real-time monitoring, evidence capture, fleet coordination, and safety-aware execution.

Open problems:

- Represent missions, waypoints, constraints, geofences, telemetry, events, and operator interventions as auditable state.
- Coordinate multiple vehicles, ground stations, sensors, and control loops under intermittent connectivity.
- Recover safely from lost links, partial commands, sensor failures, low battery, localization drift, and mission aborts.
- Fuse telemetry, perception, maps, and external events while preserving provenance and confidence.
- Simulate, replay, and evaluate autonomy behavior before deployment.
- Bridge low-level protocols such as MAVLink, PX4, ArduPilot, ROS 2, and ground-control software into higher-level mission models.

Useful mechanisms:

- Mission planning state machines.
- Telemetry ingestion and event correlation.
- Safety envelopes and geofence enforcement.
- Command acknowledgment and retry models.
- Simulation and replay harnesses.
- Fleet coordination protocols.
- Sensor fusion with confidence propagation.
- Human override and review queues.

Avoid:

- Pure hardware projects with no reusable software mechanism.
- Demo flight scripts with no recovery or safety model.
- Black-box autonomy claims without logs, simulation, or test evidence.
- Projects focused only on visual dashboards without mission or telemetry semantics.

### AI knowledge layer and metadata systems

We need a durable knowledge layer that can connect operational systems, analytical artifacts, semantic metadata, and AI-generated reasoning.

Open problems:

- Connect Airflow, dbt, warehouse models, documents, Slack context, code, and external evidence.
- Track lineage between raw evidence, transformations, metrics, conclusions, and recommendations.
- Support GraphRAG or knowledge graph retrieval without losing evidence boundaries.
- Keep metadata incrementally fresh as source systems change.
- Separate verified facts from inferred or model-generated claims.

Useful mechanisms:

- Metadata graphs.
- Semantic layers.
- Data lineage and provenance.
- Incremental metadata indexing.
- Evidence-backed retrieval.
- Schema and contract evolution.

Avoid:

- Knowledge graphs populated only by LLM extraction without validation.
- Semantic layers with no connection to operational lineage.
- Systems that collapse facts, interpretations, and hypotheses into the same representation.

### Agent runtime and long-running workflows

We need patterns for reliable AI-agent execution over tasks that may run for minutes, hours, or days.

Open problems:

- Durable execution with retries, heartbeats, cancellation, and resumability.
- Tool-call authorization and scoped permissions.
- Long-lived sandbox identity and state.
- Recovery after process, worker, or infrastructure failure.
- Observability and auditability of agent decisions and actions.
- Human review checkpoints for high-risk actions.

Useful mechanisms:

- Durable workflows.
- Saga and compensation patterns.
- Policy generations and invalidation.
- Capability tokens.
- Workflow recovery.
- Execution tracing.
- Human approval queues.

Avoid:

- Stateless chat loops pretending to be agent runtimes.
- Tool registries without permission boundaries.
- Sandboxes that cannot explain or replay actions.

### Event intelligence and OSINT monitoring

We need mechanisms for detecting, correlating, and explaining changes across noisy external sources.

Open problems:

- Detect meaningful deltas across feeds, websites, social platforms, documents, and structured APIs.
- Resolve entities across inconsistent names, identifiers, languages, and time.
- Correlate weak signals into evidence-backed events.
- Maintain confidence and uncertainty across sources.
- Support real-time monitoring without flooding users with duplicate or low-value alerts.

Useful mechanisms:

- Delta detection.
- Event correlation.
- Entity resolution.
- Evidence accumulation.
- Temporal memory.
- Alert deduplication.
- Human review queues.

Avoid:

- Simple feed aggregators.
- Systems that produce alerts without evidence trails.
- Fully automated OSINT conclusions with no uncertainty model.

### Codebase intelligence

We need mechanisms for understanding codebases, tracing architectural decisions, and attributing code changes to agents, humans, tasks, and evidence.

Open problems:

- Map source files, symbols, commits, issues, traces, and generated artifacts into a coherent model.
- Attribute lines or changes to sessions, tools, models, and prompts with explicit confidence.
- Detect architectural drift and repeated implementation patterns.
- Support repository-level reasoning grounded in concrete source evidence.

Useful mechanisms:

- Code indexing.
- Symbol graphs.
- Trace-to-code attribution.
- Commit and diff provenance.
- Incremental repository analysis.
- Evidence-backed code review.

Avoid:

- Generic repository summaries with no file or symbol evidence.
- Line attribution that presents heuristic guesses as facts.
- Indexing approaches that require full recomputation for small changes.

## Research Preferences

Prefer repositories with:

- Recent meaningful source development.
- Nontrivial implementation beyond demos and wrappers.
- Identifiable reusable architectural mechanisms.
- Tests or executable examples.
- Clear data models, persistence choices, and recovery behavior.
- Documentation that explains operational trade-offs or architecture.

Stars are a weak signal. Use them only as supporting context.

## Decision Standard

Every recommendation must connect:

`problem in interests.md -> observed mechanism -> source evidence -> proposed experiment or decision`

When evidence is insufficient, say so explicitly and avoid project-specific recommendations.
