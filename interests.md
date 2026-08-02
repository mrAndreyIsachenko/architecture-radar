# Architecture Radar Interests

This file is the authoritative source for Architecture Radar research priorities. Repository analysis must connect findings to concrete problems listed here rather than inferred project needs.

## Current Priorities

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

We need mechanisms for interpreting blockchain transactions beyond raw indexing.

Open problems:

- Reconstruct user intent from contract calls, internal transfers, logs, traces, and token movements.
- Map low-level execution traces to domain-level events.
- Explain causality across transactions, contracts, addresses, and time windows.
- Maintain provenance from interpretation back to chain evidence.
- Handle reorgs, partial data, ambiguous ABIs, and protocol-specific semantics.

Useful mechanisms:

- Incremental indexing.
- Event sourcing.
- Trace decoding pipelines.
- Entity resolution.
- Confidence-aware interpretation.
- Reorg-safe materialization.

Avoid:

- Indexers that only expose generic SQL over raw chain data.
- Hard-coded protocol interpretations without provenance.
- Architectures that cannot recover from chain reorganizations.

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
