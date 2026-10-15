# yaogdu/AgentLedger

- Repository: https://github.com/yaogdu/AgentLedger
- Review date: 2026-09-28
- Current commit reviewed: `dd966e3b3d9eb54032c51701d30efcfbaa2379b0`
- Commit date: 2026-08-31T17:32:53+08:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: selected

## Problem Fit

This repository informs `ai-llm-systems`, especially durable agent execution, tool governance, replayable evidence, and provenance-carrying execution graphs. The reusable mechanism is the runtime envelope around agent steps and side effects, not the dashboard or the multi-language packaging.

## Verified Flow

`Runtime.run_once` claims one step lease, reconstructs `AgentContext`, appends an `agent_started` event, runs the agent, and commits the pending state patch with a checkpoint id -> `ReplayEngine.replay` walks the stored events and artifacts without calling tools again -> `EvidenceExporter.export` builds an evidence bundle with the run, steps, tool ledger, approvals, artifacts, media artifacts, stream checkpoints, cost records, and a bundle hash -> tests verify crash retry, replay without tool execution, high-risk tool denial, schema validation, stale-lease rejection, evidence export, and inspector round-tripping.

- E1 source verified: `src/agentledger/runtime.py:120-187` claims the run step, builds `AgentContext`, appends `agent_started`, commits the state patch, and classifies retryable failures, approval waits, and simulated crashes.
- E1 source verified: `src/agentledger/replay.py:25-62` reconstructs replay from stored events and artifacts without re-invoking tools or providers.
- E1 source verified: `src/agentledger/evidence.py:29-155` writes the evidence bundle and HTML inspector output from persisted run state, steps, tool ledger, approvals, artifacts, and cost records.
- E2 test verified: `tests/test_runtime.py:262-305` covers crash retry, replay non-execution, low-risk tool commit, and high-risk tool denial.
- E2 test verified: `tests/test_runtime.py:414-447` covers evidence bundle export, evidence regression evaluation, and inspector round-tripping.

## Architecture

Principal components:

- `Runtime` as the step executor and tool gateway.
- `ToolLedger` / policy / budget / sandbox gates around tool dispatch.
- `SQLiteStore` and `LocalBlobStore` as the default durable state and evidence stores.
- `ReplayEngine` and `EvidenceExporter` as the replay and audit surfaces.
- Inspector and CLI tooling as read-only views over persisted runs.

Most interesting mechanism: the runtime turns agent execution into a durable, policy-governed ledger where step state, tool calls, and evidence bundles are first-class. The replay engine validates evidence availability without ever re-calling providers or tools, which keeps audit and replay separate from live execution.

Baseline comparison: a conventional agent loop would hold state in memory, call tools directly, and rebuild history from logs after the fact. AgentLedger instead persists the execution envelope itself so replay, audit, and idempotency checks are part of the runtime contract.

## Reuse Guidance

Reusable:

- Keep step claims and state commits separate.
- Make tool governance a runtime concern, not a caller convention.
- Export an evidence bundle that can be hashed and inspected without rerunning tools.
- Treat replay as a read-only operation over the persisted envelope.

Do not copy:

- Do not copy the dashboard or the multi-language packaging unless those are already part of the target platform.
- Do not assume the default in-process tool model is a security boundary.
- Do not rely on the current adapter breadth without trimming it to the actual deployment surface.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Strong coverage for crash retry, replay, schema validation, stale-lease rejection, and evidence export.
- The replay path is explicit about never calling tools again.
- The evidence bundle is stable enough to hash and inspect.

Experimental or incomplete for our needs:

- Some adapters and runtime integrations are optional or experimental.
- The review did not validate a live worker-kill / restart cycle on the same ledger.
- The default tooling surface is broad enough that integration scope matters.

Hidden costs and failure modes:

- Tool governance can become policy-heavy if the tool catalog grows without discipline.
- Replay safety depends on the store and blob invariants holding under real crashes.
- A misconfigured sandbox or adapter can still leak side effects outside the ledger.

Adoption conditions:

- Verify process-kill recovery against a real side effect.
- Pin the tool idempotency contract for any effectful tool.
- Keep the evidence bundle and replay semantics stable across runtime upgrades.

## Candidate Patterns

- `evidence-carrying execution envelope`
- `tool-ledger replay boundary`
- `policy-governed dispatch gate`
- `evidence bundle exporter`
