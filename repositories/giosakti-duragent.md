# giosakti/duragent

- Repository: https://github.com/giosakti/duragent
- Review date: 2026-08-29
- Current commit reviewed: `c39a858fa75de93b9d76bdf62b681b378b7882d9`
- Commit date: 2026-02-18T15:46:59+07:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `ai-llm-systems`, especially durable agent sessions, resumable message histories, and crash-safe file-backed state. The reusable mechanism is not the chat UI; it is the per-session actor plus file store that keeps event history, snapshots, and recovery behavior consistent.

## Verified Flow

`SessionActor::spawn` creates a dedicated actor and `run` writes `SessionStart` plus an initial snapshot before it accepts commands -> `command_loop` serializes all mutations through a single receiver and flush timer -> `FileSessionStore::append_events` serializes events, acquires a per-session lock, and uses one `spawn_blocking` file-I/O block for append + fsync -> `load_events` skips malformed lines on recovery, `load_snapshot` validates schema compatibility, and `spawn_recovered` rebuilds the actor from persisted snapshot state -> `tests/session_persistence_test.rs` and the actor/store unit tests verify append ordering, snapshot round-trips, and crash-safe recovery paths.

- E1 source verified: `crates/duragent/src/session/actor.rs:41-223` defines the per-session actor, recovered spawn path, startup `SessionStart` write, and serialized command loop.
- E1 source verified: `crates/duragent/src/store/file/session.rs:25-192` implements the file-backed session store with per-session locks, append-only event files, atomic snapshot reads, and a single blocking file-I/O section per append.
- E1 source verified: `crates/duragent/src/store/session.rs:15-73` defines the storage contract, including append, snapshot, and compaction semantics.
- E2 test verified: `crates/duragent/tests/session_persistence_test.rs` covers event round-trips, append ordering, snapshot restoration, and malformed-line recovery.
- E2 test verified: `crates/duragent/src/session/actor.rs` test module verifies crash-safe `SessionStart` flushing, retry behavior, and snapshot persistence.

## Architecture

Principal components:

- Session actor for serialized mutation handling.
- File-backed session store with JSONL event log and JSON snapshot.
- Session registry / recovery path for fresh and recovered actors.
- Keyed lock helper for per-session compaction and append exclusion.
- Tests and docs that describe the session lifecycle and crash-recovery contract.

Most interesting mechanism: the actor owns state mutation, while the store owns durable representation. That split lets the runtime keep the mutable state path single-writer and still make crash recovery read from a plain file layout.

Baseline comparison: a conventional agent session store often writes directly from many call sites and reconstructs state from a transcript later. Duragent instead isolates the writer in a session actor and makes the file store the authoritative replay source.

## Reuse Guidance

Reusable:

- Model a long-lived session as a single-writer actor.
- Put append-only history and the latest snapshot in separate files.
- Serialize file writes outside the async lock and fsync inside one blocking section.
- Treat malformed history entries as recoverable noise during replay.

Do not copy:

- Do not copy the concrete file layout without an adapter.
- Do not assume the current file store is the right scale boundary for high-volume production workloads.
- Do not rely on the in-repo compaction and locking strategy without validation under real concurrency.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The session store and actor both have explicit crash-safety comments and tests.
- Event append, snapshot load, and recovery behavior are all source-backed.
- The store avoids holding async locks across repeated await points.

Experimental or incomplete for our needs:

- The implementation is still file-first rather than external-database-first.
- Session deletion and compaction are present but not exposed as a broad operational surface.
- The repository still carries early-development design churn in docs and specs.

Hidden costs and failure modes:

- File-based recovery couples correctness to local filesystem durability.
- Per-session locking can become a bottleneck if the session fan-out gets large.
- Malformed lines are skipped on recovery, which is pragmatic but can hide upstream corruption.

Adoption experiment:

Run a session through a forced mid-turn process kill, then restart it and confirm the recovered actor replays the same session history from `events.jsonl` plus `state.json` without duplicate writes.

## Candidate Patterns

- `single-writer session actor`
- `append-only session ledger`
- `atomic snapshot after session start`
