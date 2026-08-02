# Evidence-Carrying Execution Envelopes

- Canonical name: Evidence-Carrying Execution Envelopes
- Aliases: evidence envelope, provenance envelope, lineage event envelope, checkpoint envelope, episode evidence envelope
- Avoided duplicate names: execution graph events, trace wrappers, provenance records, lineage packets
- Last updated: 2026-08-02

## Problem

The projects in `interests.md` need agent, workflow, data, and research activity represented as execution graphs with stable provenance. A plain log line, transcript, graph edge, or database row is not enough because derived conclusions must remain auditable back to source evidence, parent steps, schemas, producers, and replay/recovery state.

## Mechanism

Wrap each execution step, lineage event, or source episode in a structured envelope that carries:

- Stable identity for the event, run, step, episode, or checkpoint.
- Producer/runtime identity.
- Schema or model version.
- Parent/root causality.
- Input and output references.
- Extension facets or typed metadata.
- Persistence/recovery state when the envelope participates in a long-running workflow.
- Links from derived facts back to source records.

The envelope is then projected into a graph, trace, checkpoint store, or knowledge layer. Consumers should preserve the envelope rather than collapsing it into an unverifiable narrative summary.

## Invariants

- Every derived claim must retain a link to at least one source envelope.
- Parent-child causality must be explicit, not inferred only from timestamps or names.
- Producer and schema/version identity must travel with the evidence.
- Runtime recovery metadata and semantic interpretation metadata should be separable fields.
- LLM-derived facts must be distinguishable from source-verified facts.
- The envelope must be usable outside a single proprietary runtime.

## Implementation Variants

- Checkpoint envelope: LangGraph stores checkpoint ID, thread ID, namespace, parent checkpoint ID, channel versions, metadata, and pending writes.
- Lineage event envelope: OpenLineage stores event time, producer, schema URL, run/job/dataset identity, input/output datasets, parent run facets, and typed facets.
- Episode evidence envelope: Graphiti stores source episodes with source type, source description, valid time, raw content policy, entity edges, and derived relationship fact links.

## Known Repositories

- `langchain-ai/langgraph` reviewed at `b2926a0ff9589c28c7e01fe7cdbb337b86d5a4b4`.
- `OpenLineage/OpenLineage` reviewed at `13f1b0ac406bc276b3fa23445062c2f119b4fe91`.
- `getzep/graphiti` reviewed at `7cf0cab4b43f55d768b64584ffa9829bbeec1e9d`.

## Comparison Of Implementations

LangGraph is strongest for runtime recovery. Its checkpoint envelope captures execution state, parent checkpoint links, channel versions, and pending writes, but not first-class evidence hashes or source references.

OpenLineage is strongest for cross-system provenance. Its envelope requires producer and schema URL, separates base event identity from facets, and models parent/root run causality, but it does not by itself guarantee replay or factual correctness.

Graphiti is strongest for temporal memory around relationship facts. Its episode/fact model preserves source episodes and invalidates contradictory edges over time, but entity node attributes are mutable summaries in the reviewed source and extraction/contradiction resolution are LLM-mediated, so it needs explicit confidence, validation, and attribute-history layers before adoption.

## Failure Modes

- Valid envelopes can contain false claims if producers emit bad data.
- Parent links can become incomplete when side effects occur outside the instrumented runtime.
- Schema/facet drift can make consumers silently drop evidence fields.
- LLM extraction can collapse facts, interpretations, and hypotheses unless claims are typed.
- Relationship-level temporal validity can be mistaken for full graph temporality when node attributes are still mutable.
- Async checkpoint persistence can leave crash windows unless durability mode is explicit.
- User-visible streamed state can diverge from persisted checkpoint state unless cancellation and disconnect paths flush or record partial state.
- Sensitive source content can leak if raw evidence retention is not governed.

## Trade-Offs

- More metadata improves auditability but increases schema governance and storage costs.
- Cross-runtime envelopes are more reusable than runtime-native checkpoints but usually need a separate projector for replay.
- Typed facets preserve extension boundaries but require version negotiation.
- Keeping raw evidence enables review and re-extraction but creates privacy and retention obligations.

## Applicability To Interests

- Evidence-backed semantic execution graph: directly applicable as the base representation for steps, tool calls, retries, derived artifacts, parent-child causality, replay, and audit explanations.
- Agent runtime and long-running workflows: applicable for resumable checkpoints, human review gates, and recovery records.
- AI knowledge layer and metadata systems: applicable for lineage between raw evidence, transformations, metrics, conclusions, and recommendations.
- Event intelligence and OSINT monitoring: applicable for episode-backed event correlation and uncertainty-preserving fact updates.
- Codebase intelligence: applicable for commit/diff/session provenance if extended with code-specific facets.

## Adoption Conditions

- Define an internal base envelope with required producer, schema version, event/step ID, parent ID, source refs, evidence hashes, and claim type.
- Add typed facets for agent tool calls, human approvals, retries, model calls, data lineage, source documents, code changes, and confidence.
- Require deterministic projection from envelopes into the knowledge graph.
- Require tests showing replay, partial recomputation, parent-child causality, and evidence citation.
- Add policy for sensitive raw evidence retention and redaction.

## Evidence References

- E1 source verified: LangGraph `libs/checkpoint/langgraph/checkpoint/memory/__init__.py` stores checkpoint blobs, metadata, parent checkpoint ID, and pending writes.
- E2 test verified: LangGraph `libs/langgraph/tests/test_retry.py::test_graph_error_handler_error_context_survives_checkpoint_resume` verifies error context survives checkpoint resume.
- E1 source verified: OpenLineage `spec/OpenLineage.json` requires `eventTime`, `producer`, and `schemaURL` on base events and `_producer`, `_schemaURL` on base facets.
- E1 source verified: OpenLineage `spec/facets/ParentRunFacet.json` models parent/root run and job identity.
- E1 source verified: Graphiti `graphiti_core/graphiti.py` creates episodic nodes and saves episode UUID links to derived entity edges.
- E1 source verified: Graphiti `graphiti_core/utils/maintenance/edge_operations.py` invalidates contradictory edges by setting `invalid_at` and `expired_at`.
- E1 source verified: Graphiti `graphiti_core/nodes.py` gives `EntityNode` mutable attributes without edge-style `valid_at`/`invalid_at` fields.
- E3 issue stated: LangGraph issues #5672/#7714 and Graphiti issues #1166/#1684 identify adoption risks around streamed-state persistence, checkpoint serialization cost, node-attribute temporality, and `group_id` routing.
