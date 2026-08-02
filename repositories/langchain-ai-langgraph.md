# langchain-ai/langgraph

- Repository: https://github.com/langchain-ai/langgraph
- Review date: 2026-08-02
- Current commit reviewed: `b2926a0ff9589c28c7e01fe7cdbb337b86d5a4b4`
- Commit date: 2026-07-30T14:57:02-04:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

LangGraph informs the `Agent runtime and long-running workflows` priority in `interests.md`, specifically durable execution with retries, cancellation/resumability, observability, auditability, and human review checkpoints. It also partially informs `Evidence-backed semantic execution graph` because graph state, tasks, checkpoints, and pending writes can be treated as execution graph evidence.

## Verified Flow

`StateGraph` input schema and nodes -> `compile(checkpointer=...)` -> Pregel stream/invoke execution -> checkpoint saver stores channel versions, parent checkpoint IDs, and pending writes -> later invocation/get_state resumes or inspects state -> stream/task/checkpoint/debug outputs expose observable execution state.

- E1 source verified: `libs/langgraph/langgraph/graph/state.py` at `b2926a0...`, `StateGraph` defines typed shared state and reducer-backed keys, and the builder cannot execute until compiled.
- E1 source verified: `libs/langgraph/langgraph/graph/state.py`, `StateGraph.compile` accepts `checkpointer`, `store`, `interrupt_before`, and `interrupt_after`; the docstring states that a checkpointer enables pause, resume, and replay by `thread_id`.
- E1 source verified: `libs/langgraph/langgraph/pregel/main.py`, `Pregel.stream` supports `values`, `updates`, `messages`, `checkpoints`, `tasks`, and `debug` stream modes plus durability modes `sync`, `async`, and `exit`.
- E1 source verified: `libs/checkpoint/langgraph/checkpoint/memory/__init__.py`, `InMemorySaver.put` stores checkpoint payloads, metadata, parent checkpoint ID, and per-channel version blobs by `(thread_id, checkpoint_ns, channel, version)`.
- E1 source verified: `libs/checkpoint/langgraph/checkpoint/memory/__init__.py`, `get_tuple` reconstructs checkpoints with `channel_values`, `metadata`, `pending_writes`, and `parent_config`.
- E2 test verified: `libs/langgraph/tests/test_retry.py::test_graph_error_handler_error_context_survives_checkpoint_resume` pauses before an error handler, resumes with serialized error context, and verifies recovery.
- E2 test verified: `libs/langgraph/tests/test_retry.py::test_graph_error_handler_does_not_swallow_interrupt_concurrent` verifies that a concurrent `interrupt()` remains pending rather than being swallowed by error handling.

## Architecture

Principal components:

- `StateGraph`: typed graph builder, schema registry, node/edge/branch definition, and compile-time validation.
- Pregel runtime: executes graph supersteps over named channels and exposes stream modes for values, updates, LLM messages, checkpoints, tasks, and debug data.
- Checkpoint savers: storage abstraction for checkpoint tuples, pending writes, channel blobs, and parent checkpoint links.
- Interrupt/error mechanisms: graph-level interrupt gates and per-node error handlers that can be persisted and resumed.

Most interesting mechanism: checkpoint tuples are not just snapshots. They carry channel versions, parent checkpoint configuration, metadata, pending writes, and task paths. This is a reusable execution envelope for resumable workflows.

Baseline comparison: a conventional stateless agent loop stores a transcript or final state and retries from the top. LangGraph instead records resumable graph state keyed by `thread_id` and can pause around interrupt/error boundaries.

## Reuse Guidance

Reusable:

- Use a typed graph state plus appendable checkpoint metadata as the runtime audit spine for long-running agents.
- Model human review as an interrupt in the execution graph, not as an external side channel.
- Store parent checkpoint links and pending writes so recovery can explain what was already persisted versus what is still pending.
- Expose task/checkpoint/debug streams as observable output for audit and replay.

Do not copy:

- Do not adopt LangGraph as the only execution boundary for all systems; `interests.md` explicitly avoids systems that require all execution inside one proprietary runtime.
- Do not rely on in-memory checkpointing for production recovery; the source labels it non-production and recommends a persistent saver.
- Do not treat stream debug output as sufficient evidence hashes or source references. Those would need to be added.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Broad test surface under `libs/langgraph/tests`, `libs/checkpoint/tests`, and `libs/checkpoint-postgres/tests`.
- Persistent checkpointer implementations and schema/migration code exist beyond the in-memory saver.
- Tests cover resume after error context and interrupt preservation.

Experimental or incomplete for our needs:

- Evidence hashes, source references, confidence, and decision rationale are not first-class checkpoint fields.
- The review did not run the repository test suite locally.
- The source evidence verifies durable execution mechanics, not an end-to-end production deployment.

Hidden costs and failure modes:

- `async` durability can persist while the next step executes; users must understand crash windows.
- Checkpoint namespace/thread ID design becomes an operational contract.
- Human review and authorization policies remain application responsibilities.

Adoption experiment:

Build a thin adapter that maps a LangGraph checkpoint tuple into an internal evidence envelope with `step_id`, `parent_step_id`, `tool_call`, `input_hash`, `output_hash`, `decision_rationale`, and `source_refs`. Test crash/resume around a human interrupt and verify that replay can reconstruct parent-child causality.
