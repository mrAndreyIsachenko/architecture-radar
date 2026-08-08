# intuit/infigraph

- Repository: https://github.com/intuit/infigraph
- Review date: 2026-08-08
- Current commit reviewed: `cf0c1fcda3137e17472f9e624a3677a856cc06a8`
- Commit date: 2026-08-08T00:50:27+05:30
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `ai-llm-systems`, especially codebase intelligence, incremental indexing, context construction, and evidence-aware tool use. The reusable mechanism is the persistent code graph with hash-skipping rebuilds, cross-file resolution, and session-aware compression, not the product shell around it.

## Verified Flow

`infigraph index` -> `Infigraph::init` opens the graph with lock-aware retry -> `Infigraph::index_via_backend` hashes files and skips unchanged content -> `extract::extract_file` builds `FileExtraction` from AST/tree-sitter and grammar plugins -> `GraphStore::upsert_files_bulk` persists symbols, edges, and statements -> `resolve_calls` resolves cross-file call and inheritance edges -> `Infigraph::index` prints progress/stats and updates embeddings/docs.

- E1 source verified: `crates/infigraph-cli/src/index.rs` drives the CLI index command, handles full rebuilds, and routes into `Infigraph::index`.
- E1 source verified: `crates/infigraph-core/src/lib.rs` defines `Infigraph::init`, `open_kuzu_with_retry`, and `Infigraph::index_via_backend`, including hash-skipping incremental rebuild and stale-file pruning.
- E1 source verified: `crates/infigraph-core/src/graph/store_write.rs` persists `Module`, `File`, `Symbol`, `Statement`, and typed edge rows, including bulk `CALLS`, `INHERITS`, `TESTED_BY`, `IMPORTS`, `READS`, and `WRITES` edges.
- E1 source verified: `crates/infigraph-core/src/resolve/calls.rs` resolves cross-file calls, inheritance, and custom edges from the full symbol table.
- E1 source verified: `crates/infigraph-core/src/graph/session_store.rs` persists sessions as JSON, migrates old Kuzu session state, and applies confidence decay plus archive/purge thresholds.
- E2 test verified: `crates/infigraph-core/tests/search_routes_security.rs::test_scan_project_sql_injection` verifies security scanning on indexed code.
- E2 test verified: `crates/infigraph-mcp/src/session_context.rs::test_dedup_same_content_returns_placeholder` and `test_prior_session_dedup_matching_hash` verify session-level output deduplication and prior-session reuse.

## Architecture

Principal components:

- CLI orchestration for indexing, querying, route detection, security scanning, and export.
- Core graph store with Kuzu-backed persistence and optional Neo4j/Postgres remote mode.
- AST extraction, language registry, cross-file resolution, and embeddings.
- Session store and MCP-side context compression/dedup.

Most interesting mechanism: the repository treats indexing as a content-hash-driven graph rebuild rather than a blanket rescan. The lock-aware open path, stale-file pruning, and session dedup make the tool usable in repeated agent loops without blindly reprocessing the same repository state.

Baseline comparison: a conventional code search tool either rescans on every run or exposes raw search results without a durable graph. Infigraph keeps a persisted structural model, resolves cross-file references, and reuses prior session context when content is unchanged.

## Reuse Guidance

Reusable:

- Hash-skip unchanged files before rebuilding derived structure.
- Treat graph open failures as lock contention first, corruption second.
- Keep session output dedup and confidence decay separate from the code graph.
- Preserve cross-file call resolution as a distinct pass.

Do not copy:

- Do not copy the full product surface or agent UI as the mechanism.
- Do not assume Kuzu/Neo4j-specific persistence semantics are generic.
- Do not treat session compression as a substitute for evidence provenance.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Clear CLI/core split, multiple backends, and explicit retry logic.
- Incremental indexing, pruning, and cross-file resolution are source-backed.
- Session state has concrete persistence and migration code.

Experimental or incomplete for our needs:

- The mechanism is broad and product-shaped.
- The review did not run the local test suite.
- Evidence provenance is still implicit; the graph is durable, but it is not yet an explicit claim envelope.

Hidden costs and failure modes:

- Multi-backend support increases operational complexity.
- Session compression/dedup can hide useful context if thresholds are mis-tuned.
- Large language-registry and plugin surfaces increase startup and maintenance cost.

Adoption experiment:

Use the hash-skip rebuild flow on a small internal code graph, then force a no-op rerun and a single-file edit to confirm only the changed slice is reindexed and the prior session summary is reused correctly.

## Candidate Patterns

- `content-hash incremental graph rebuild`
- `lock-aware graph reopen`
- `confidence-decayed session dedup`
