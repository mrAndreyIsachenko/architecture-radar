# getzep/graphiti

- Repository: https://github.com/getzep/graphiti
- Review date: 2026-08-02
- Current commit reviewed: `7cf0cab4b43f55d768b64584ffa9829bbeec1e9d`
- Commit date: 2026-08-01T18:57:42Z
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: watch

## Problem Fit

Graphiti informs the `AI knowledge layer and metadata systems`, `Evidence-backed semantic execution graph`, and `Event intelligence and OSINT monitoring` priorities in `interests.md`: temporal memory, evidence-backed retrieval, entity resolution, evidence accumulation, and separation of raw evidence from inferred facts.

## Verified Flow

Episode input (`name`, body, source description, reference time, source type, group) -> group/schema validation and previous episode retrieval -> `EpisodicNode` creation -> LLM-assisted entity extraction -> semantic/deterministic/LLM node resolution -> LLM-assisted edge extraction -> hybrid search for duplicates and invalidation candidates -> edge resolution/expiration -> bulk save of episode, episodic edges, entity nodes, and entity edges -> hybrid search retrieves edges/nodes/episodes/communities.

- E1 source verified: `graphiti_core/nodes.py` at `7cf0cab...` defines `EpisodeType` for `message`, `json`, `text`, and `fact_triple`; base `Node` carries `uuid`, `name`, `group_id`, labels, and `created_at`.
- E1 source verified: `graphiti_core/graphiti.py`, `add_episode` validates entity/group inputs, creates or retrieves an `EpisodicNode`, records `source_description`, `content`, `created_at`, and `valid_at`, then calls extraction/resolution functions.
- E1 source verified: `graphiti_core/utils/maintenance/node_operations.py`, `extract_nodes` builds context from episode content, previous episodes, timestamps, source description, entity types, and episode attribution; `_call_extraction_llm` selects prompts by episode type.
- E1 source verified: `graphiti_core/utils/maintenance/node_operations.py`, `resolve_extracted_nodes` first collects candidates, uses similarity resolution, and falls back to LLM resolution for unresolved nodes.
- E1 source verified: `graphiti_core/utils/maintenance/edge_operations.py`, `extract_edges` builds context from episode content, known nodes, previous episodes, reference time, and edge type constraints, then validates returned entity names against known nodes.
- E1 source verified: `graphiti_core/utils/maintenance/edge_operations.py`, `resolve_extracted_edges` deduplicates exact extracted edges, embeds them, retrieves endpoint-local related edges, performs broader hybrid search for invalidation candidates, and resolves each edge.
- E1 source verified: `graphiti_core/utils/maintenance/edge_operations.py`, `resolve_edge_contradictions` sets `invalid_at` and `expired_at` when a newer edge contradicts an older valid edge.
- E1 source verified: `graphiti_core/graphiti.py`, `_process_episode_data` builds episodic edges from nodes to episode UUIDs, stores raw episode content unless disabled, and bulk saves episodes, episodic edges, nodes, and entity edges.
- E1 source verified: `graphiti_core/search/search.py` executes edge, node, episode, and community searches concurrently and supports BM25, cosine similarity, BFS, RRF, MMR, cross-encoder, node-distance, and episode-mentions reranking.
- E2 test verified: `tests/test_add_triplet.py::test_add_triplet_edge_uuid_with_different_nodes_creates_new_edge` verifies UUID collision handling preserves the original edge and creates a distinct edge when endpoints differ.
- E2 test verified: `tests/utils/maintenance/test_edge_operations.py` covers duplicate/episode attachment and invalidation-related edge resolution cases.

## Architecture

Principal components:

- Episodic nodes: raw or redacted source records with `valid_at`, source type, and source description.
- Entity nodes and entity edges: extracted graph facts partitioned by `group_id`.
- Episodic edges: provenance links from episodes to mentioned entities.
- Extraction pipeline: prompt-based node and edge extraction with structured Pydantic response models.
- Resolution pipeline: semantic search, deterministic exact matching, LLM deduplication, contradiction detection, temporal invalidation, and attribute extraction.
- Search pipeline: parallel hybrid retrieval across graph scopes with multiple rerankers and tracing spans.

Most interesting mechanism: Graphiti keeps episodes as first-class provenance anchors and links derived facts back to episode UUIDs while preserving temporal validity (`valid_at`, `invalid_at`, `expired_at`). This is useful even if the product-specific memory layer is not adopted.

Baseline comparison: a typical GraphRAG ingestion pipeline chunks text, embeds chunks, extracts entities, and upserts a graph without preserving raw evidence boundaries or temporal invalidation. Graphiti preserves episodes and invalidates facts instead of blindly overwriting them.

## Reuse Guidance

Reusable:

- Keep raw evidence episodes distinct from extracted entities/facts.
- Store episode-to-entity/fact provenance links so retrieval can cite evidence-bearing source records.
- Treat contradictions as temporal invalidations (`valid_at`/`invalid_at`) rather than destructive overwrites.
- Use hybrid retrieval for candidate deduplication before invoking an LLM.

Do not copy:

- Do not copy LLM-extracted facts into a trusted knowledge layer without confidence, evidence hashes, and validation policy.
- Do not make LLM contradiction detection the sole arbiter for high-impact OSINT or operational facts.
- Do not expose `group_id` as a database selector without reviewing tenancy and authorization implications.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Rich implementation beyond a demo: graph drivers, search, extraction, maintenance utilities, tests, MCP server, and tracing.
- Tests cover graph operations, edge update semantics, driver behavior, search security, and integrations.
- Source code explicitly tracks episode provenance and temporal validity.

Experimental or incomplete for our needs:

- Confidence scoring is not first-class in the reviewed flow.
- Important extraction, deduplication, contradiction, and timestamp decisions rely on LLM calls.
- Evidence hashes/source references beyond episode UUIDs are not first-class.
- The review did not run Graphiti tests locally.

Hidden costs and failure modes:

- Sequential ingestion is recommended in the source docstring; concurrent ingestion may create duplicate or stale resolution states without external ordering.
- Hybrid search and LLM resolution can be expensive at scale.
- Raw episode storage must be governed because it may contain sensitive source text.

Adoption experiment:

Prototype an episode-anchored fact memory for a small OSINT/event-monitoring feed. Require every extracted fact to carry `episode_uuid`, source URL/hash, extraction prompt/version, confidence, and reviewer status. Measure duplicate alert reduction and false invalidations before using it for automated conclusions.
