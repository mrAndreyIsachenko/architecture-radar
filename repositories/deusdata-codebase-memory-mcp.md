# DeusData/codebase-memory-mcp

- Repository: https://github.com/DeusData/codebase-memory-mcp
- Review date: 2026-08-02
- Current commit reviewed: `d6be58ef9d43c574a2d1b0827ecc1e3c4846f0fe`
- Commit date: 2026-07-31T22:47:36+02:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `ai-llm-systems`, specifically codebase intelligence, long-context context assembly, incremental indexing, and evidence-aware tool use. Its useful mechanism is not the product wrapper, but the combination of repository indexing, coverage checks, trace search, and post-index plausibility gates.

## Verified Flow

`cli index_repository` / daemon auto-index admission -> pipeline indexing and graph build -> `dump_verify` post-dump gate compares committed node counts with persisted SQLite rows -> CLI/test surfaces `search_graph`, `trace_path`, `check_index_coverage`, `detect_changes`, and `manage_adr` -> logs and activation events record daemon/session behavior.

- E1 source verified: `src/foundation/dump_verify.h` gates `index_repository` output after indexing by comparing committed and persisted node counts.
- E1 source verified: `tests/test_daemon_application.c` exercises `index_repository`, auto-index admission, file-limit enforcement, and `manage_adr`/`index_repository` tool pairing.
- E1 source verified: `tests/test_cli.c` verifies `search_graph`, `trace_path`, `check_index_coverage`, and prompt/tool profile wiring for codebase-memory sessions.
- E1 source verified: `tests/test_agent_profiles.c` checks profile-specific tool sets, including `check_index_coverage` and `detect_changes`.
- E1 source verified: `tests/test_cpp_index_hang.sh` exists to catch `index_repository` hangs.
- E2 test verified: `tests/test_daemon_application.c::daemon_application_auto_index_honors_tracked_file_limit` and related tests validate the auto-index governor and retry behavior.

## Architecture

Principal components:

- Daemon and CLI orchestration for repo admission, tool routing, and session state.
- Pipeline passes for environment scan, git history, semantic extraction, and cross-repo stitching.
- Foundation gates for dump verification, locking, and persistence integrity.
- Test harnesses that cover indexing, tool exposure, profile routing, and hang detection.

Most interesting mechanism: the repository does not trust a completed index by default. It adds a post-dump plausibility gate and auto-index admission limits so the graph snapshot must look structurally sane before it is treated as usable evidence.

Baseline comparison: a conventional code search index just writes a graph or embedding store and assumes success if the process exits cleanly. This repo adds admission control, post-index verification, and tool-specific coverage assertions.

## Reuse Guidance

Reusable:

- Use a post-build plausibility gate for any local codebase snapshot or derived graph export.
- Treat tool coverage as a first-class artifact, not just a docs concern.
- Keep auto-index admission bounded so background refresh cannot silently explode cost.

Do not copy:

- Do not copy the UI/product shell as the architectural mechanism.
- Do not assume the persisted graph is trustworthy without a structural sanity gate.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Extensive tests around CLI, daemon lifecycle, profiles, and hang recovery.
- Explicit configuration and logging hooks for index admission and activation events.
- Multiple core source directories for graph, semantic, daemon, and pipeline behavior.

Experimental or incomplete for our needs:

- The review did not run the test suite locally.
- The useful mechanism is tightly coupled to this project’s graph model and MCP surface.

Hidden costs and failure modes:

- The post-dump ratio gate can reject sparse repositories if configured too aggressively.
- Auto-index admission can hide freshness issues if operators tune limits too low.
- Product-level abstractions make it harder to isolate a generic indexing primitive.

Adoption experiment:

Apply the dump-verification gate idea to an internal code intelligence indexer: persist a checkpoint, compare committed vs. materialized nodes, and fail the run if the ratio drops below a threshold unless the repo is explicitly sparse.

## Candidate Patterns

- `post-dump plausibility gate`
- `auto-index admission governor`
