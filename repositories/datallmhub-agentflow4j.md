# datallmhub/agentflow4j

- Repository: https://github.com/datallmhub/agentflow4j
- Review date: 2026-08-29
- Current commit reviewed: `f11300c039a385889e10ed7c1bf1f8aa0d3c12d0`
- Commit date: 2026-06-11T09:47:59+02:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `ai-llm-systems`, especially governed agent graphs, resumable checkpoints, approval gates, and runtime policy enforcement. The reusable mechanism is the graph runtime that combines state policy, budget policy, approval gating, checkpoint persistence, and run logging in one execution model.

## Verified Flow

`AgentGraph.invoke(initial, runId)` persists an initial checkpoint when a checkpoint store is configured -> `run()` walks the graph node by node, checks interrupt/time-out/max-iteration conditions, and records run-log events -> `gateApproval` can return an interrupt that is checkpointed before execution continues -> `enforceStatePolicy` and `executeWithPolicy` apply node policies and surface failures through the configured error policy -> `resume(runId, additional...)` loads the stored checkpoint, optionally appends new messages, and continues from `nextNode` -> `JdbcCheckpointStore.save/load/delete` uses a transaction template and validated table name to upsert or fetch checkpoints -> the checkpoint-resume and run-log tests verify resume, approval, and policy behavior.

- E1 source verified: `agentflow4j-graph/src/main/java/io/github/datallmhub/agentflow4j/graph/AgentGraph.java:24-61,127-259` defines the graph runtime, explicit `runId` checkpointing, resume path, approval checkpointing, budget and state policy enforcement, and error handling.
- E1 source verified: `agentflow4j-checkpoint/src/main/java/io/github/datallmhub/agentflow4j/checkpoint/JdbcCheckpointStore.java:18-94` implements transactional checkpoint upsert/load/delete with table-name validation.
- E2 test verified: `agentflow4j-graph/src/test/java/io/github/datallmhub/agentflow4j/graph/CheckpointTests.java`, `RunLogTests.java`, and `ApprovalGateTests.java` cover checkpoint resume, run-log emission, and approval behavior.
- E2 test verified: `agentflow4j-checkpoint/src/test/java/io/github/datallmhub/agentflow4j/checkpoint/CheckpointResumeE2ETests.java` verifies interrupt, persist, restart, resume, and cleanup against JDBC and Redis checkpoint stores.

## Architecture

Principal components:

- Graph runtime with nodes, edges, and execution policies.
- Checkpoint store abstractions and concrete JDBC/Redis backends.
- Run-log store for observability and audit.
- Approval gate, budget policy, state policy, retry policy, and error policy.
- Test suite that exercises checkpoints, run logs, and the approval workflow.

Most interesting mechanism: the graph is not just a control-flow API. It treats policy decisions and interrupt points as first-class resumable state, so the exact node boundary can be resumed after a human review or budget interruption.

Baseline comparison: a simpler agent graph would run nodes and return an interrupted flag to the caller. AgentFlow4J persists the pause point, stores the audit trail, and makes resumption an explicit part of the runtime contract.

## Reuse Guidance

Reusable:

- Persist checkpoint state at policy boundaries, not only at the end of a run.
- Keep approval, budget, and state policy checks separate so each can be tested independently.
- Store run logs alongside resumable state.
- Validate checkpoint storage with a real restart/resume test, not just unit serialization.

Do not copy:

- Do not copy the Spring/JDBC wiring without adaptation.
- Do not assume the policy defaults are safe for every workload.
- Do not treat the in-memory checkpoints as a production substitute.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The runtime models approval, retries, budgets, and state writes as explicit policies.
- Checkpoint persistence is transactional in the JDBC implementation.
- The repository includes restart/resume coverage for checkpoint backends.

Experimental or incomplete for our needs:

- The runtime is still relatively opinionated around Spring-style application wiring.
- Some of the API surface is tutorial-driven and may require trimming before reuse.
- The value depends on integrating a real checkpoint backend rather than using the in-memory default.

Hidden costs and failure modes:

- Policy overlap can create hard-to-debug abort paths if the ordering is not understood.
- Checkpoint recovery depends on the persistence backend staying available.
- The graph can still fail fast on errors that the caller expected to retry.

Adoption experiment:

Run one graph with an approval gate and one with a budget breach, then restart each from the saved checkpoint and confirm the resumed run picks up from the recorded `nextNode` rather than replaying from the entry node.

## Candidate Patterns

- `governed checkpointed execution graph`
- `approval-gated resume point`
- `policy-layered node execution`
