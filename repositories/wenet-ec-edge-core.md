# wenet-ec/edge-core

- Repository: https://github.com/wenet-ec/edge-core
- Review date: 2026-08-11
- Current commit reviewed: `82290162021a4158f9ba8298fa64fb7e148f198f`
- Commit date: 2026-08-11T15:16:50+07:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `privacy-networking-vpn` and `agent runtime and long-running workflows`. The reusable mechanism is the command-execution state machine and WireGuard health probe, not the broader admin UI or deployment packaging.

## Verified Flow

Admin posts a command -> `CommandExecutionController.create/2` validates and stores the execution -> `Commands.create_command_execution_and_enqueue_worker/1` inserts the row and enqueues `ExecuteCommandWorker` -> `ExecuteCommandWorker.perform/1` reloads the row, claims `:pending` work, and either expires it or runs it -> `Commands.execute_single_command/1` shells out through `hostscript`, registers the task in `ExecutionRegistry`, truncates oversized output, and completes the row -> `ReportExecutionWorker.perform/1` calls `Commands.report_unreported_executions/0` -> successful reports delete local rows, while 404/409/422 responses are treated as terminal and discarded locally. The VPN side is separately observable through `WireguardInterface.check/0`, which probes the host interface with `ip -j`.

- E1 source verified: `edge_agent/lib/edge_agent/commands/commands.ex:198-615` implements recoverable enqueueing, FIFO reporting, execution claiming, command completion, cancellation, and Oban job cancellation.
- E1 source verified: `edge_agent/lib/edge_agent/commands/workers/execute_command_worker.ex:41-103` claims pending rows, handles expiration, retries running rows after crash recovery, and re-enqueues reporting.
- E1 source verified: `edge_agent/lib/edge_agent/commands/workers/report_execution_worker.ex:33-41` delegates the reporting pass to the Commands context.
- E1 source verified: `edge_agent/lib/edge_agent/diagnostics/wireguard_interface.ex:9-86` inspects the WireGuard interface, routes, and addresses through `ip -j` and classifies the interface as ok/warn/error.
- E2 test verified: `edge_agent/test/edge_agent/commands/command_execution_results_test.exs:15-177` pins exit-code categorization, payload truncation, and reporting shape.
- E2 test verified: `edge_agent/test/edge_agent/diagnostics/wireguard_interface_test.exs:7-31` verifies up/down/no-route interface classification.

## Architecture

Principal components:

- `Commands` as the orchestration and persistence boundary.
- Oban workers for execution and reporting.
- `ExecutionRegistry` for task PID tracking and cancellation.
- `WireguardInterface` for host-side VPN diagnostics.
- JSON/controller modules for admin-facing state transitions.

Most interesting mechanism: the command execution flow is durable and restartable because it is represented as persistent row state (`pending`, `running`, `completed`, `expired`) plus a task registry and unique Oban jobs. Cancellation and reporting both reconcile state instead of assuming the worker process is authoritative.

Baseline comparison: a simpler remote-execution service would run a command and return output, or would push results immediately without durable recovery. This implementation keeps local state, resumes recoverable work after restart, and finalizes results only after explicit reporting.

## Reuse Guidance

Reusable:

- Model remote command execution as a persistent state machine with explicit recovery statuses.
- Separate claim, execute, report, and cancel paths.
- Treat reporting errors as batch-control decisions, not just exceptions.
- Make health probes produce structured ok/warn/error details instead of a single boolean.

Do not copy:

- Do not copy the entire access-platform surface or hostscript assumption.
- Do not assume WireGuard diagnostics are portable without the same `ip`/route model.
- Do not hide row-state transitions behind a single opaque job state.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The command state machine is explicitly modeled and tested.
- Duplicate jobs are prevented by Oban uniqueness.
- Reporting handles terminal HTTP statuses and transient transport failures differently.
- The WireGuard diagnostic path is deterministic and test-covered.

Experimental or incomplete for our needs:

- The repo is still coupled to a specific admin/control-plane architecture.
- The actual command execution depends on `/usr/local/bin/hostscript`.
- VPN health checks are host-environment sensitive.

Hidden costs and failure modes:

- Row state can diverge from task state if cancellation races with completion.
- The reporting loop depends on repeated cron/worker execution for recovery.
- Health probes can fail for environmental reasons unrelated to real tunnel health.

Adoption experiment:

Prototype a small internal command runner that stores `pending/running/completed` rows, kills task PIDs on cancel, and replays unreported completions on a periodic worker.

## Candidate Patterns

- `recoverable command queue`
- `stateful command finalization`
- `WireGuard health probe`
