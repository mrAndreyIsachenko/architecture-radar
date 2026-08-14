# Evidence-Carrying Execution Envelopes

- Canonical name: Evidence-Carrying Execution Envelopes
- Aliases: evidence envelope, provenance envelope, lineage event envelope, checkpoint envelope, episode evidence envelope
- Avoided duplicate names: execution graph events, trace wrappers, provenance records, lineage packets
- Last updated: 2026-08-14

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
- Run checkpoint envelope: ClearIdeas Agent Runtime stores manifest hash, contract version, runtime version, cursor, state, step results, transcript, artifacts, optional continuation, and budget in each checkpoint, while the run store fences attempts and checkpoint sequence numbers.
- Durable agent session envelope: Microsoft Agent Framework durable agents persist conversation state in durable entities, and the extension composes nested workflows into child orchestrations with session-scoped execution state.

## Known Repositories

- `langchain-ai/langgraph` reviewed at `b2926a0ff9589c28c7e01fe7cdbb337b86d5a4b4`.
- `OpenLineage/OpenLineage` reviewed at `13f1b0ac406bc276b3fa23445062c2f119b4fe91`.
- `getzep/graphiti` reviewed at `7cf0cab4b43f55d768b64584ffa9829bbeec1e9d`.
- `clearideas/agent-runtime` reviewed at `c8a4856863405c817315bbd8ff89a07fea6b24a5`.
- `microsoft/agent-framework-durable-extension` reviewed at `ad941eff53617840c0a046498be36d0b3871329b`.

## Comparison Of Implementations

LangGraph is strongest for runtime recovery. Its checkpoint envelope captures execution state, parent checkpoint links, channel versions, and pending writes, but not first-class evidence hashes or source references.

OpenLineage is strongest for cross-system provenance. Its envelope requires producer and schema URL, separates base event identity from facets, and models parent/root run causality, but it does not by itself guarantee replay or factual correctness.

Graphiti is strongest for temporal memory around relationship facts. Its episode/fact model preserves source episodes and invalidates contradictory edges over time, but entity node attributes are mutable summaries in the reviewed source and extraction/contradiction resolution are LLM-mediated, so it needs explicit confidence, validation, and attribute-history layers before adoption.

ClearIdeas Agent Runtime is strongest for manifest-first workflow replay. Its checkpoint envelope keeps the execution cursor, attempt fencing, and durable budget/transcript state together, so resume can validate against the exact manifest hash instead of replaying from an ambiguous log stream.

Microsoft Agent Framework durable extension is strongest for session-scoped orchestration durability. It couples durable agent entities to workflow composition and child orchestrations, which makes human-in-the-loop and nested workflow recovery explicit, but it is narrower than a generic provenance graph and still depends on the host's durable backend.

## Failure Modes

- Valid envelopes can contain false claims if producers emit bad data.
- Parent links can become incomplete when side effects occur outside the instrumented runtime.
- Schema/facet drift can make consumers silently drop evidence fields.
- LLM extraction can collapse facts, interpretations, and hypotheses unless claims are typed.
- Relationship-level temporal validity can be mistaken for full graph temporality when node attributes are still mutable.
- Async checkpoint persistence can leave crash windows unless durability mode is explicit.
- User-visible streamed state can diverge from persisted checkpoint state unless cancellation and disconnect paths flush or record partial state.
- Sensitive source content can leak if raw evidence retention is not governed.
- Manifest drift can invalidate a resumed checkpoint if the runtime does not hash and compare the manifest before resuming.
- Session-scoped durable entities can still lose observability if the durable backend is unavailable or if the orchestration host cannot rehydrate the exact continuation state.

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
- Durable workflow orchestration: applicable for session cursors, child orchestrations, and replay-safe review gates in agent runtimes.

## Adoption Conditions

- Define an internal base envelope with required producer, schema version, event/step ID, parent ID, source refs, evidence hashes, and claim type.
- Add typed facets for agent tool calls, human approvals, retries, model calls, data lineage, source documents, code changes, and confidence.
- Require deterministic projection from envelopes into the knowledge graph.
- Require tests showing replay, partial recomputation, parent-child causality, and evidence citation.
- Add policy for sensitive raw evidence retention and redaction.
- For checkpointed runtimes, require manifest hashing and attempt fencing before resume, plus tests for suspend, cancel, and failed-checkpoint paths.
- For durable agent entities, require recovery tests that cover nested workflows, external event waits, and backend rehydration.

## Evidence References

- E1 source verified: LangGraph `libs/checkpoint/langgraph/checkpoint/memory/__init__.py` stores checkpoint blobs, metadata, parent checkpoint ID, and pending writes.
- E2 test verified: LangGraph `libs/langgraph/tests/test_retry.py::test_graph_error_handler_error_context_survives_checkpoint_resume` verifies error context survives checkpoint resume.
- E3 maintainer stated: OpenLineage `spec/OpenLineage.json` requires `eventTime`, `producer`, and `schemaURL` on base events and `_producer`, `_schemaURL` on base facets.
- E3 maintainer stated: OpenLineage `spec/facets/ParentRunFacet.json` models parent/root run and job identity.
- E1 source verified: Graphiti `graphiti_core/graphiti.py` creates episodic nodes and saves episode UUID links to derived entity edges.
- E1 source verified: Graphiti `graphiti_core/utils/maintenance/edge_operations.py` invalidates contradictory edges by setting `invalid_at` and `expired_at`.
- E1 source verified: Graphiti `graphiti_core/nodes.py` gives `EntityNode` mutable attributes without edge-style `valid_at`/`invalid_at` fields.
- E3 issue stated: LangGraph issues #5672/#7714 and Graphiti issues #1166/#1684 identify adoption risks around streamed-state persistence, checkpoint serialization cost, node-attribute temporality, and `group_id` routing.
- E1 source verified: ClearIdeas Agent Runtime `packages/core/src/agent-runtime.ts:726-783` validates resume state against the stored manifest and checkpoint hash before continuing a run.
- E1 source verified: ClearIdeas Agent Runtime `packages/core/src/agent-runtime.ts:1002-1058` persists suspended, cancelled, and failed runs as distinct lifecycle states.
- E1 source verified: ClearIdeas Agent Runtime `packages/core/src/agent-runtime.ts:1391-1438` writes checkpoint envelopes with manifest hash, contract/runtime versions, cursor, state, artifacts, continuation, and budget.
- E2 test verified: ClearIdeas Agent Runtime `packages/core/src/agent-runtime.test.ts:312-345` verifies that a failed checkpoint stops later steps.
- E2 test verified: ClearIdeas Agent Runtime `packages/core/src/agent-runtime.test.ts:919-1005` verifies manifest mismatch rejection and nested continuation resume.
- E1 source verified: Microsoft Agent Framework durable extension `python/samples/11_subworkflow/worker.py:126-189` composes a nested workflow and auto-registers durable child orchestrations.
- E1 source verified: Microsoft Agent Framework durable extension `dotnet/samples/DurableAgents/ConsoleApps/05_AgentOrchestration_HITL/Program.cs:47-117` uses a durable agent session, waits for external approval, and reruns on rejection.
- E2 test verified: Microsoft Agent Framework durable extension `dotnet/tests/Microsoft.Agents.AI.DurableTask.UnitTests/State/DurableAgentStateMessageTests.cs:11-46` round-trips durable agent state messages through JSON serialization.
