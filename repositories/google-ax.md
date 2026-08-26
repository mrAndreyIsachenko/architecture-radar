# google/ax

- Repository: https://github.com/google/ax
- Review date: 2026-08-26
- Current commit reviewed: `b77731302075b3630b200af5e2cf63ac93b5f315`
- Commit date: 2026-08-19T22:56:39-07:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `ai-llm-systems`, especially long-running agent workflows, durable execution, and evidence-backed execution graphs. The reusable mechanism is not the branding or demo harness; it is the controller-owned session state, the append-only event log, and the sidecar-backed harness lifecycle that can be resumed after interruption.

## Verified Flow

`cmd/ax/main.go` parses the CLI and loads config -> `cmd/ax/harness.go` selects the harness, forks or attaches the Python sidecar, and serves `/readyz` -> `internal/controller/controller.go:Exec` checks resumption state, preserves the recorded harness ID, logs inputs, and routes streamed responses through a handler -> `internal/controller/eventlog/sql.go:Append` and `Events` persist and reconstruct ordered conversation events -> `internal/harness/substrate/substrate.go:Start`, `Run`, and `Close` create or resume the remote actor, wait for health, stream requests and responses, and suspend the actor on close -> `internal/pythonsidecar/sidecar.go:Start` manages the PID file, readiness check, and restart/attach behavior.

I verified the runtime path with `go test ./cmd/ax ./internal/controller ./internal/harness/...`, which passed.

## Architecture

Principal components:

- `cmd/ax` for CLI dispatch and harness selection.
- `internal/controller` for single-writer execution orchestration and resumption checks.
- `internal/controller/eventlog` for durable step-event storage.
- `internal/harness/substrate` for remote actor creation, health gating, and stream draining.
- `internal/harness/antigravity` and `internal/pythonsidecar` for process-backed local harness execution.

Most interesting mechanism: the controller does not treat the current process as authoritative. It reads recorded conversation events, preserves the harness identity that originally handled the conversation, and drives both local and remote harnesses through explicit health-gated start, run, and close phases.

Baseline comparison: a conventional agent CLI would keep only a transcript or final output and restart from scratch after interruption. AX instead persists the conversation event log and sidecar lifecycle state so resumption is anchored to recorded execution history.

## Reuse Guidance

Reusable:

- Model agent turns as durable conversation events with explicit resume checks.
- Gate work on sidecar readiness instead of assuming process spawn implies service readiness.
- Keep the harness identity part of the resumable state.
- Separate control-plane orchestration from harness implementation details.

Do not copy:

- Do not copy the specific SubstrATE and Python sidecar assumptions without an adapter layer.
- Do not rely on the current in-repo event log as a production-scale backend without further hardening.
- Do not treat the CLI surface as the reusable mechanism; the resumption contract is the valuable part.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The controller and sidecar path is source-backed and test-covered.
- The sidecar wrapper handles PID files, attach/reuse behavior, and readiness polling.
- The substrate harness tests cover health gating, connect/stream behavior, and suspend-on-close.

Experimental or incomplete for our needs:

- The repository is explicitly in early development and warns that breaking architecture changes are still expected.
- The code still contains TODOs for incomplete resume semantics and remote harness support.
- Durable state is not backed by an external production service in the reviewed source path.

Hidden costs and failure modes:

- PID-file management and process supervision add coupling to the host filesystem.
- Readiness probes can succeed on one layer while deeper harness state is still inconsistent.
- Session resumption depends on the integrity of the stored event log and harness ID.

Adoption experiment:

Run one agent turn, kill the sidecar mid-stream, and confirm that a restart reuses the same conversation identity, reconstructs the last event log state, and only proceeds once the harness reports ready again.

## Candidate Patterns

- `single-writer conversational event log`
- `readiness-gated sidecar runtime`
- `resume-stable harness identity`
