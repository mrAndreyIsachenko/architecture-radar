# Evidence-Carrying Execution Envelopes

- Canonical name: Evidence-Carrying Execution Envelopes
- Aliases: evidence envelope, provenance envelope, lineage event envelope, checkpoint envelope, episode evidence envelope
- Avoided duplicate names: execution graph events, trace wrappers, provenance records, lineage packets
- Last updated: 2026-08-29

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
- Sidecar-backed agent envelope: Google AX persists conversation events in a controller-owned event log, preserves the recorded harness identity across resumes, and gates local or remote harness execution on explicit readiness checks.
- File-first session envelope: Duragent persists an append-only `events.jsonl` plus atomic `state.json`, serializes session mutations through a dedicated actor, and keeps malformed replay lines from breaking recovery.
- Governed graph checkpoint envelope: AgentFlow4J stores checkpoints, run logs, approval gates, budgets, and state-policy decisions together so a paused graph can resume from the exact next node rather than replaying from scratch.
- Filesystem-native run ledger: PageLedger persists page-level provenance, quality, rerun, and verification evidence as plain files so rerun planning and audit checks can be replayed without a database.
- Structured command evidence envelope: `mavsdk_drone_show` persists command identity, lifecycle phase, per-target evidence, and append-only events in a durable SQLite journal, while `ReadOnlyEvidenceBundle` packages sanitized read-only answer evidence with source refs and confidence for operator follow-up.

## Known Repositories

- `langchain-ai/langgraph` reviewed at `b2926a0ff9589c28c7e01fe7cdbb337b86d5a4b4`.
- `OpenLineage/OpenLineage` reviewed at `13f1b0ac406bc276b3fa23445062c2f119b4fe91`.
- `getzep/graphiti` reviewed at `7cf0cab4b43f55d768b64584ffa9829bbeec1e9d`.
- `clearideas/agent-runtime` reviewed at `c8a4856863405c817315bbd8ff89a07fea6b24a5`.
- `microsoft/agent-framework-durable-extension` reviewed at `ad941eff53617840c0a046498be36d0b3871329b`.
- `google/ax` reviewed at `b77731302075b3630b200af5e2cf63ac93b5f315`.
- `giosakti/duragent` reviewed at `c39a858fa75de93b9d76bdf62b681b378b7882d9`.
- `datallmhub/agentflow4j` reviewed at `f11300c039a385889e10ed7c1bf1f8aa0d3c12d0`.
- `peterbussch/pageledger` reviewed at `fd1c1da0fbdc366222170f24fb22890f8a19f8a0`.
- `alireza787b/mavsdk_drone_show` reviewed at `39ce5601e9d47eafdd3a6ccffd3c1caba3f08cad`.

## Comparison Of Implementations

LangGraph is strongest for runtime recovery. Its checkpoint envelope captures execution state, parent checkpoint links, channel versions, and pending writes, but not first-class evidence hashes or source references.

OpenLineage is strongest for cross-system provenance. Its envelope requires producer and schema URL, separates base event identity from facets, and models parent/root run causality, but it does not by itself guarantee replay or factual correctness.

Graphiti is strongest for temporal memory around relationship facts. Its episode/fact model preserves source episodes and invalidates contradictory edges over time, but entity node attributes are mutable summaries in the reviewed source and extraction/contradiction resolution are LLM-mediated, so it needs explicit confidence, validation, and attribute-history layers before adoption.

ClearIdeas Agent Runtime is strongest for manifest-first workflow replay. Its checkpoint envelope keeps the execution cursor, attempt fencing, and durable budget/transcript state together, so resume can validate against the exact manifest hash instead of replaying from an ambiguous log stream.

Microsoft Agent Framework durable extension is strongest for session-scoped orchestration durability. It couples durable agent entities to workflow composition and child orchestrations, which makes human-in-the-loop and nested workflow recovery explicit, but it is narrower than a generic provenance graph and still depends on the host's durable backend.

Google AX is strongest for sidecar-backed conversational execution. Its controller keeps resumption anchored to recorded conversation events and harness identity, while the sidecar wrapper adds explicit readiness and PID management. That makes it useful as a recoverable agent harness pattern, but it still depends on a file-backed event log and an external runtime substrate.

Duragent is strongest for file-first session persistence. The dedicated session actor serializes mutations, while the file store keeps append-only history and atomic snapshots together. That makes replay and crash recovery easy to reason about, but it also means correctness still depends on filesystem durability and the replay discipline around malformed lines.

AgentFlow4J is strongest for governed checkpoint resumes. Its graph runtime treats approval gates, budgets, state writes, and checkpoint persistence as policy-aware state transitions, so a paused run can resume from the exact next node. The trade-off is stronger Spring/backend coupling and more policy interaction to validate.

PageLedger is strongest for filesystem-native rerun evidence. Its manifests, route maps, quality queues, and rerun manifests remain plain files, so the run directory itself becomes the ledger. That is a good fit for replayable document-extraction workflows, but it also means the verification contract is only as strong as the caller's discipline around the run directory.

`mavsdk_drone_show` is strongest for command-lifecycle evidence. The journal separates command state, per-target evidence, and callback capability state, so restart recovery can rebuild the live tracker without collapsing everything into a mutable status blob. The read-only evidence bundle then gives operator-facing answers a compact provenance container that can be audited and routed without re-parsing markdown.

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
- File-based replay can hide upstream corruption if malformed lines are silently skipped without alerting operators.
- Session-scoped durable entities can still lose observability if the durable backend is unavailable or if the orchestration host cannot rehydrate the exact continuation state.
- Sidecar-backed runtimes can wedge on PID-file mismatches, readiness probes, or host-level process restarts.
- Filesystem-native ledgers can be tampered with if callers skip the verification pass or treat the run directory as immutable without enforcement.

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
- For file-first session stores, require crash/restart tests that verify malformed replay lines are handled intentionally and not silently ignored in a way that hides corruption.

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
- E1 source verified: Google AX `internal/controller/controller.go:Exec` ties conversation resumption to logged events and recorded harness identity, while `internal/controller/eventlog/sql.go:Append` and `Events` persist ordered step events.
- E1 source verified: Google AX `cmd/ax/harness.go:runAntigravityHarness`, `runAntigravityInteractionsHarness`, and `serveReadyz` couple sidecar startup, readiness gating, and signal forwarding to the harness lifecycle.
- E1 source verified: Google AX `internal/pythonsidecar/sidecar.go:Start` writes a PID file, attaches to existing working processes, and waits for readiness before returning.
- E2 test verified: Google AX `cmd/ax/doctor_test.go`, `internal/controller/controller_test.go`, and `internal/harness/substrate/substrate_test.go` verify doctor registration, controller resume behavior, and substrate health/stream wiring.
- E1 source verified: Duragent `crates/duragent/src/session/actor.rs:41-223` owns session mutation, writes `SessionStart` before commands, and records recovered versus fresh startup paths.
- E1 source verified: Duragent `crates/duragent/src/store/file/session.rs:25-192` stores append-only JSONL events plus atomic snapshots, serializes writes through a keyed lock, and skips malformed replay lines during recovery.
- E2 test verified: Duragent `crates/duragent/tests/session_persistence_test.rs` covers event ordering, snapshot restoration, and crash-recovery replay behavior.
- E1 source verified: AgentFlow4J `agentflow4j-graph/src/main/java/io/github/datallmhub/agentflow4j/graph/AgentGraph.java:24-259` persists checkpoints at entry, approval, interrupt, and next-node boundaries.
- E1 source verified: AgentFlow4J `agentflow4j-checkpoint/src/main/java/io/github/datallmhub/agentflow4j/checkpoint/JdbcCheckpointStore.java:18-94` upserts checkpoints transactionally with validated table names.
- E2 test verified: AgentFlow4J `agentflow4j-checkpoint/src/test/java/io/github/datallmhub/agentflow4j/checkpoint/CheckpointResumeE2ETests.java` verifies JDBC and Redis resume paths.
- E1 source verified: PageLedger `pageledger/runner.py:run` and `rerun` preserve page-level lineage, parent run identity, and source checksums across reruns.
- E1 source verified: PageLedger `pageledger/artifacts.py:build_manifest`, `build_audit`, and `build_rerun_manifest` keep run evidence in plain files, including page ids, rerun depth, and previous grades.
- E1 source verified: PageLedger `pageledger/verify.py:verify_run` enforces artifact presence, hash coherence, and symlink-safe paths before the rerun manifest is trusted.
- E2 test verified: PageLedger `tests/pageledger/test_quality.py`, `tests/pageledger/test_verify.py`, and `tests/pageledger/test_rerun.py` cover quality queues, run verification, and rerun lineage semantics.
- E1 source verified: `mavsdk_drone_show/gcs-server/command_journal.py:1-206` persists the immutable command lifecycle, per-target state, and append-only event stream in SQLite WAL.
- E1 source verified: `mavsdk_drone_show/gcs-server/command_submission_pipeline.py:46-97` and `:199-220` separate SITL endpoint validation from readiness evidence.
- E1 source verified: `mavsdk_drone_show/gcs-server/agent_runtime/evidence.py:23-198` builds compact read-only evidence bundles and items with hashes, source refs, and confidence.
- E2 test verified: `mavsdk_drone_show/tests/test_command_journal.py:83-185` and `:188-220` verify restart-queryability, replay idempotency, and mid-fanout recovery.
