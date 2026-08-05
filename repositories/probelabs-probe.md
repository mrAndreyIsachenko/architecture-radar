# probelabs/probe

- Repository: https://github.com/probelabs/probe
- Review date: 2026-08-05
- Current commit reviewed: `76f0843cb0221e0eb79ca4982b63c931082dd706`
- Commit date: 2026-07-31T09:05:32+03:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `ai-llm-systems`, specifically codebase intelligence, context engineering, incremental indexing, and tool use. The reusable mechanism is the structured search engine and daemon behavior, not the chat wrapper around it.

## Verified Flow

CLI input -> query parsing and query-plan construction in `src/search/query.rs` -> search execution in `src/search/search_runner.rs` -> file processing and AST-aware block filtering in `src/search/file_processing.rs` -> early ranking and block merging -> branch-aware workspace management in `lsp-daemon/src/workspace/branch.rs` -> tests verify file processing, query planning, and branch operations.

- E1 source verified: `src/search/query.rs`, `create_query_plan` parses a query into an AST, collects terms, precomputes required-term metadata, and builds an evaluation cache.
- E1 source verified: `src/search/file_processing.rs`, `filter_code_block_with_ast` uses precomputed term matches and fast-path AST evaluation to accept or reject a block.
- E1 source verified: `src/search/early_ranker.rs`, early ranking combines content matches, filename matches, and coverage weighting into a BM25-like score.
- E1 source verified: `src/main.rs`, CLI search input normalizes paths, handles configuration defaults, and routes into the search and extraction pipeline.
- E1 source verified: `lsp-daemon/src/workspace/branch.rs`, branch switching checks dirty state, computes changed files, invalidates caches, and forces reindexing after branch changes.
- E2 test verified: `src/search/file_processing_tests.rs::test_process_file_with_results_single_line` verifies block extraction around a matching line.
- E2 test verified: `src/search/query_tests.rs::test_create_term_patterns` verifies query-plan term pattern generation and escaping.
- E2 test verified: `lsp-daemon/tests/branch_operations_tests.rs::test_branch_switching_basic` and `test_branch_switching_with_file_changes` exercise branch switching and workspace synchronization.

## Architecture

Principal components:

- Rust search core: query parsing, structured patterns, AST evaluation, ranking, and block extraction.
- LSP daemon: workspace, git, and indexing coordination for multi-repo or multi-branch state.
- Node/CLI tooling: prompt/tool orchestration and higher-level agent wrappers.

Most interesting mechanism: Probe does not treat search as a flat substring lookup. It builds a query plan with AST metadata, uses that metadata to skip irrelevant blocks early, and carries branch context into the daemon so cached indexes do not outlive the git state they were built from.

Baseline comparison: a conventional code search tool would run ripgrep-like scanning and rank afterward. Probe precomputes query structure, evaluates code blocks against that structure, and couples workspace state to branch changes.

## Reuse Guidance

Reusable:

- Use a query-plan object with precomputed structural metadata to reduce repeated evaluation cost.
- Separate filename relevance, content relevance, and AST block inclusion so ranking can be tuned independently.
- Treat git branch switches as indexing invalidation events, not just filesystem changes.

Do not copy:

- Do not copy the product wrapper or chat shell as the architecture.
- Do not assume the AST path alone is enough for all languages; the implementation still depends on language-specific parsing and caches.
- Do not treat the ranking layer as a proven universal IR; it is tuned for codebase search.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Large search and daemon test surface.
- Multiple language-specific parser tests and integration tests.
- Clear separation between search core and higher-level orchestration.

Experimental or incomplete for our needs:

- The codebase mixes several optimization phases, so the effective behavior depends on the current query/ranking path.
- The review did not run the local test suite.
- Some functionality is still framed as phased optimization rather than a frozen contract.

Hidden costs and failure modes:

- Query-plan caching and AST evaluation add complexity that can regress if term indexing or precedence rules change.
- Branch-aware reindexing must stay aligned with git operations or stale caches can mislead search.
- The daemon’s multi-workspace behavior adds operational state that simpler search tools avoid.

Adoption experiment:

Clone the query-plan and branch-invalidation idea into an internal code intelligence tool, then run the same query before and after a git branch switch to verify that cached results are invalidated only when the branch actually changes.

## Candidate Patterns

- `AST-backed search plan`
- `branch-sensitive reindexing`
