# microsoft/agent-framework-go

- Repository: https://github.com/microsoft/agent-framework-go
- Review date: 2026-08-05
- Current commit reviewed: `421d96b86baf8f0e307a64ce4c63fc1d5b06cd18`
- Commit date: 2026-08-05T02:57:38Z
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `ai-llm-systems`, specifically the `Agent runtime and long-running workflows` priority and the related `Evidence-backed semantic execution graph` priority. The reusable mechanism is not the SDK surface itself, but the combination of resumable workflow checkpoints, approval-aware tool invocation, and observable workflow output.

## Verified Flow

`workflow/agentworkflow` builder input -> workflow execution with a checkpoint manager -> `workflow/checkpoint/jsonstore.go` persists JSON checkpoints and an append-only index -> `agent/harness/toolautocall/autocall.go` intercepts function calls, approvals, and retries -> later agent invocation or session restore resumes from stored checkpoint state -> tests verify checkpoint round-trips, index flush, approval translation, and resumed sessions.

- E1 source verified: `workflow/checkpoint/jsonstore.go`, `FileSystemJSONStore.CreateCheckpoint` validates session data, writes checkpoint JSON to disk, appends an index entry, and syncs the index immediately.
- E1 source verified: `workflow/checkpoint/jsonstore.go`, `RetrieveCheckpoint` and `RetrieveIndex` reconstruct checkpoint data and parent-filtered histories from the durable index.
- E1 source verified: `workflow/checkpoint/manager.go`, `jsonManager` serializes workflow checkpoints to JSON and delegates persistence to the store, while `inMemoryManager` keeps session-scoped checkpoint caches behind a mutex.
- E1 source verified: `agent/harness/toolautocall/autocall.go`, the middleware converts provider function calls into approval requests, can inject messages, enforces iteration and error caps, and optionally runs concurrent tool calls.
- E1 source verified: `workflow/observability/observability.go`, workflow spans have explicit kinds, attributes, and trace context plumbing for observable execution.
- E2 test verified: `workflow/checkpoint/jsonstore_test.go::TestFileSystemJSONStore_PersistsIndexImmediately` checks that the index is flushed before close.
- E2 test verified: `workflow/checkpoint/jsonstore_test.go::TestFileSystemJSONStore_PersistsToDisk` reloads a store from disk and reuses the saved checkpoint/index.
- E2 test verified: `agent/harness/toolautocall/autocall_approval_test.go::TestFunctionInvoking_AllFunctionCallsReplacedWithApprovalsWhenAllRequireApproval` verifies approval requests are synthesized from tool calls.
- E2 test verified: `workflow/agentworkflow/workflow_test.go::TestNew_SerializedSessionResumesFromCheckpoint` verifies session serialization and resumption through checkpoint state.

## Architecture

Principal components:

- `workflow/checkpoint`: durable JSON checkpoint persistence, index maintenance, and checkpoint lookup.
- `workflow/agentworkflow`: workflow-to-agent adaptation, session plumbing, and execution orchestration.
- `agent/harness/toolautocall`: approval handling, tool-loop retry control, and message injection.
- `workflow/observability`: telemetry and trace-context abstraction for workflow execution.

Most interesting mechanism: the file-backed checkpoint store is more than a snapshot. It writes an index entry immediately, preserves parent checkpoint links, and rehydrates session state for later resume. Combined with approval translation, it gives a long-running agent an auditable recovery boundary.

Baseline comparison: a conventional agent loop stores only a transcript or final output and retries from scratch after interruption. This repo persists workflow state and turns tool approval into part of the execution model instead of a side-channel.

## Reuse Guidance

Reusable:

- Use an append-only checkpoint index to make recovery explainable, not just possible.
- Model human review as an approval translation step inside the tool loop.
- Keep workflow observability separate from business logic so execution traces can be consumed independently.

Do not copy:

- Do not rely on the in-memory checkpoint manager for recovery beyond tests.
- Do not assume the approval middleware alone is enough for policy; caller-side authorization still matters.
- Do not treat the repository as a complete execution graph standard. It is an implementation pattern, not a universal schema.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- Strong test coverage for checkpoint persistence, session replay, approval conversion, and workflow execution.
- Clear separation between JSON checkpoint storage and in-memory checkpoint handling.
- Observability abstractions are explicit instead of hidden in the runtime.

Experimental or incomplete for our needs:

- The review did not run the local test suite.
- The durable store is file-based here; production adoption needs the persistent backend and crash-recovery path tested under load.
- Evidence hashes and claim metadata are not native checkpoint fields.

Hidden costs and failure modes:

- File-backed checkpointing introduces an index and file-locking contract that callers must respect.
- Tool-approval translation can obscure what the provider originally emitted unless the surrounding session capture is preserved.
- Message injection can create more rounds than expected if tool code enqueues aggressively.

Adoption experiment:

Wrap one long-running agent task in a JSON checkpoint manager, force a crash after a tool approval request, and confirm that the session can resume from the stored checkpoint with the same parent-child history and the same approval decision trail.

## Candidate Patterns

- `approval-gated tool loop`
- `durable checkpoint index`
