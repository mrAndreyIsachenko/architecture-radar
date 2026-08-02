# getzep/graphiti

- Repository: https://github.com/getzep/graphiti
- Review date: 2026-08-02
- Branch: `main`
- Commit reviewed: `7cf0cab4b43f55d768b64584ffa9829bbeec1e9d`
- Commit date: 2026-08-01T18:57:42Z
- Release/tag: package version `graphiti-core` 0.29.3 in `pyproject.toml`
- Previous commit reviewed: none
- Current decision: watch for temporal knowledge-graph mechanisms; do not adopt as a whole runtime yet.

## Problem Fit

Graphiti informs the `AI knowledge layer and metadata systems` and `Evidence-backed semantic execution graph` interests. It targets real-time knowledge graph construction for agent memory, with explicit episode nodes, entity nodes, relationship facts, temporal fields, and source episode links.

## Source Structure

- `graphiti_core/graphiti.py` orchestrates ingestion, extraction, resolution, persistence, saga summaries, and search.
- `graphiti_core/nodes.py` defines `EpisodicNode`, `EntityNode`, `CommunityNode`, and `SagaNode`.
- `graphiti_core/edges.py` defines `EpisodicEdge`, `EntityEdge`, `HasEpisodeEdge`, and `NextEpisodeEdge`.
- `graphiti_core/utils/maintenance/node_operations.py` and `edge_operations.py` implement LLM extraction, dedupe, contradiction handling, and timestamp extraction.
- `graphiti_core/driver/**` contains Neo4j, FalkorDB, Kuzu, and Neptune persistence operations.
- Tests inspected: `tests/test_add_triplet.py`, `tests/test_edge_db_queries.py`, and `tests/test_graphiti_mock.py`.

## Verified Flow

`episode body -> EpisodicNode -> node extraction -> node resolution -> edge extraction and contradiction resolution -> temporal entity edge persistence -> episodic provenance edge -> observable AddEpisodeResults`

- E1 source verified: `Graphiti.add_episode` validates entity settings, chooses or validates `group_id`, retrieves previous episodes, creates or loads an `EpisodicNode`, then calls `extract_nodes`, `resolve_extracted_nodes`, `_extract_and_resolve_edges`, `extract_attributes_from_nodes`, and `_process_episode_data` in `graphiti_core/graphiti.py`.
- E1 source verified: `EpisodicNode` carries `source`, `content`, `source_description`, `created_at`, and `valid_at`; `EntityEdge` carries `fact`, `episodes`, `valid_at`, `invalid_at`, and `reference_time` in `graphiti_core/nodes.py` and `graphiti_core/edges.py`.
- E1 source verified: `resolve_extracted_edge` performs exact duplicate reuse before invoking an LLM dedupe prompt, validates duplicate indices, separates duplicate facts from contradiction candidates, and extracts timestamps through `_extract_edge_timestamps` in `graphiti_core/utils/maintenance/edge_operations.py`.
- E1 source verified: `EntityEdge.save` persists `source_uuid`, `target_uuid`, `fact`, `episodes`, `expired_at`, `valid_at`, `invalid_at`, and `reference_time`; Kuzu serializes attributes differently because relationship facts are modeled as intermediate nodes.
- E2 test verified: `tests/test_edge_db_queries.py::test_entity_edge_return_query_selects_reference_time` prevents read paths from dropping `reference_time`.
- E2 test verified: `tests/test_add_triplet.py::test_add_triplet_merges_attributes` verifies node attribute merge rather than replacement when a user-provided triplet resolves to an existing node.

## Architecture

Principal components:

- Temporal source layer: `EpisodicNode` preserves raw or summarized input episodes and reference time.
- Canonical graph layer: `EntityNode` and `EntityEdge` store resolved entities and facts.
- Provenance layer: `EpisodicEdge` links episodes to mentioned entities; `EntityEdge.episodes` tracks episode UUIDs supporting a fact.
- Resolution layer: LLM extraction plus exact-match and graph-search dedupe paths.
- Persistence adapter layer: graph-driver operations isolate Neo4j/FalkorDB/Kuzu/Neptune differences.
- Saga layer: `SagaNode`, `HAS_EPISODE`, and `NEXT_EPISODE` preserve parent-child episode sequences for long-running threads.

Most interesting mechanism: the system separates raw episodic evidence from canonical entity facts while keeping temporal validity and supporting episodes on the canonical edge. That is more useful to Architecture Radar than the broader memory product.

## Comparison

Baseline: a conventional RAG memory store appends chunks to a vector index and stores an LLM summary per conversation. Graphiti instead uses a graph write path that produces evidence episodes, resolved entities, relation facts, temporal validity, and mention/provenance edges.

Genuinely unusual:

- I interpretation: retaining both episode-level evidence and canonical fact edges gives a better substrate for audit and partial recomputation than summary-only memory.
- I interpretation: saga watermarks distinguish ingestion time from event/reference time, which is useful for backfilled evidence.

Standard engineering:

- Pydantic models, graph database adapters, embeddings, cross-encoder reranking, and LLM prompt-based extraction are standard for modern GraphRAG systems.

## Production Qualities

- E1 source verified: provider-specific driver paths exist for Neo4j, FalkorDB, Kuzu, and Neptune.
- E1 source verified: OpenTelemetry spans are accepted through `Graphiti.__init__` and `add_episode` records counts and duration on the span.
- E2 test verified: tests cover triplet merge behavior, edge query shape, search behavior, and multiple graph operations.

## Limitations

- E3 maintainer stated: `Graphiti.add_episode` documentation recommends sequentially awaiting episode additions; this limits concurrent ingestion unless callers serialize per graph partition.
- E1 source verified: contradiction and timestamp extraction depend on LLM responses; invalid duplicate indices are filtered, but semantic correctness remains model-dependent.
- I interpretation: Graphiti does not yet provide cryptographic evidence hashes or a deterministic replay log for extracted conclusions.
- H hypothesis: high-volume ingestion costs may be dominated by LLM extraction, embedding generation, and graph write amplification.

## Reuse

Reusable mechanism:

- Use an episodic evidence graph: raw episode nodes plus canonical fact edges that carry `episodes`, `valid_at`, `invalid_at`, and `reference_time`.
- Keep sequence edges for long-running workflows (`NEXT_EPISODE`) and parent containers (`SagaNode`) separate from extracted facts.

Do not copy:

- Do not copy LLM contradiction results as trusted truth without a confidence model and review queue.
- Do not copy the whole memory API if the target system only needs the evidence/fact data model.

Evidence still required before adoption:

- Deterministic replay behavior across model changes.
- Evidence hash propagation from raw episode to extracted fact.
- Load and concurrency behavior under multi-writer ingestion.
- A test fixture showing partial recomputation after an episode changes or is withdrawn.

## Extracted Patterns

- Candidate pattern: episodic evidence graph with temporal canonical facts.
- Related standalone pattern: [Schema-Faceted Provenance Event Envelope](../patterns/schema-faceted-provenance-event-envelope.md).

