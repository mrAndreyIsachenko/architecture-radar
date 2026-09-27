# rmax-ai/durable-agent-runtime-lab

- Repository: https://github.com/rmax-ai/durable-agent-runtime-lab
- Review date: 2026-09-22
- Current commit reviewed: `e6beca0f0f0bf7095fee4f1d271e9076c68fb0c3`
- Commit date: 2026-07-22T20:27:00Z
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `ai-llm-systems`, especially durable agent execution, bounded proposal verification, deterministic fault injection, and replay-safe persistence. The reusable mechanism is the durable runtime boundary, not the benchmark harness or model-provider abstraction.

## Verified Flow

`DurableRuntime.run_goal` creates a workflow, compiles and plans it, checks for circular dependencies, promotes ready tasks through the scheduler, asks the model for a proposal, verifies the proposal at the boundary, executes the approved command, and then commits or fails the workflow while appending events and state transitions through the engine.

- E1 source verified: `src/durable_agent_runtime/experiments/durable.py` wires the full runtime path through `OrchestratorEngine`, `BoundaryService`, `ProcessExecutor`, `TaskScheduler`, the model provider, and the optional `FaultInjector`.
- E1 source verified: `src/durable_agent_runtime/orchestration/engine.py` owns workflow creation, state transitions, approval state, and append-only event recording against the durable stores.
- E1 source verified: `src/durable_agent_runtime/persistence/event_store.py` appends JSONL events with hash chaining and fsync-backed durability.
- E1 source verified: `src/durable_agent_runtime/boundary/service.py` enforces schema, idempotency, budget, and sandbox-path checks before execution.
- E1 source verified: `src/durable_agent_runtime/experiments/fault_injection.py` triggers deterministic faults at configured event or tool occurrences.
- E2 test verified: `tests/integration/test_e2e_runtime.py` covers the end-to-end workflow path.
- E2 test verified: `tests/unit/test_orchestrator.py`, `tests/unit/test_fault_injection.py`, `tests/integration/test_human_approval.py`, and `tests/integration/test_boundary_and_tools.py` cover state transitions, deterministic fault injection, approval gating, and boundary rejection behavior.

## Architecture

Principal components:

- Durable runtime entrypoint that runs a goal through planning, verification, execution, and commit.
- Deterministic orchestrator with workflow and task state.
- Append-only event ledger with hash chaining.
- SQLite-backed state projection and idempotency tracking.
- Proposal boundary that rejects unsafe, duplicate, or over-budget actions.
- Fault injector for deterministic event- and tool-triggered failure modes.

Most interesting mechanism: the runtime keeps proposal generation, verification, execution, and durable state updates in separate modules, but the `run_goal` path still makes them behave like one deterministic workflow. That gives a clear place to inject faults and a clear place to reject proposals before side effects happen.

Baseline comparison: a conventional agent loop usually lets the model, executor, and state updates blur together. This runtime keeps the proposal boundary explicit and stores the durable record separately from the execution side effect.

## Reuse Guidance

Reusable:

- Model the agent loop as a deterministic workflow with explicit proposal, verification, and commit stages.
- Keep the durable event ledger append-only and hash chained.
- Use a separate state projection for task/workflow lookup and idempotency.
- Add deterministic event- or tool-triggered fault injection for regression tests.

Do not copy:

- Do not copy the benchmark-specific wiring as a general agent product.
- Do not assume JSONL plus SQLite is the right scale boundary for every deployment.
- Do not treat the current boundary checks as sufficient without exercising them under live restart and failure conditions.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The workflow engine, ledger, boundary, and fault injector are all explicit source modules.
- Tests cover the main durable-flow decisions rather than only the happy path.
- The runtime clearly separates proposal generation from commit.

Experimental or incomplete for our needs:

- The repository still reads as a lab for comparing runtime styles rather than a hardened production service.
- The restart/recovery path was not validated under live process failure in this review.
- The runtime currently depends on local filesystem semantics for durability.

Hidden costs and failure modes:

- JSONL replay can hide corruption if callers do not notice skipped malformed lines.
- Hash-chained events improve tamper evidence but not external storage availability.
- Deterministic fault injection is useful for testing but can make the runtime feel more complex than a simple agent loop.

Adoption experiment:

Run a workflow with deterministic fault injection that kills the process after the workflow is created, restart the runtime, and confirm the event ledger, state projection, and idempotency checks replay the same workflow without duplicate side effects.

## Candidate Patterns

- `deterministic proposal boundary`
- `append-only hash-chained workflow ledger`
- `event-triggered fault injection harness`
- `durable workflow state projection`
