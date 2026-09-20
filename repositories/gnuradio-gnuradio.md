# gnuradio/gnuradio

- Repository: https://github.com/gnuradio/gnuradio
- Review date: 2026-09-16
- Current commit reviewed: `aee9fd3f79389c4282a98e8d62c8405c73fd91df`
- Commit date: 2026-08-26T13:30:17+05:30
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `satellites-space-systems`, especially RF processing, delayed-connectivity ground loops, and long-running flowgraph reconfiguration. The reusable mechanism is the top-block runtime that can flatten, validate, start, stop, lock, unlock, and restart a signal-processing graph without rebuilding the entire application around it.

## Verified Flow

`top_block_impl::start` flattens the hierarchy, validates the resulting flowgraph, wires connections, optionally exports perf counters, and instantiates a scheduler -> `stop` shuts the scheduler down and clears the flat graph -> `wait` drains jobs and only returns to IDLE when lock state permits -> `lock` stops the scheduler while holding the mutex so a graph can be reconfigured safely -> `unlock` decrements the lock count and calls `restart` when the graph should resume -> `restart` re-flattens, revalidates, merges old connections into the new flat graph, and starts a new scheduler -> `qa_gr_top_block.cc`, `qa_gr_flowgraph.cc`, `qa_gr_hier_block2.cc`, `qa_flowgraph.py`, and `qa_realtime.py` cover run/start/stop/wait, lock/unlock reconfiguration, validation edges, empty graphs, and the realtime binding path.

- E1 source verified: `gnuradio-runtime/lib/top_block_impl.cc:94-205` implements start, stop, wait, lock, unlock, and restart semantics.
- E1 source verified: `gnuradio-runtime/include/gnuradio/top_block.h:38-106` exposes the top-block contract and documents the lock/unlock lifecycle.
- E2 test verified: `gr-blocks/lib/qa_gr_top_block.cc:25-315` exercises run, start/stop/wait, lock/unlock, reconfigure, max-output settings, buffer settings, and shared-pointer release behavior.
- E2 test verified: `gr-blocks/lib/qa_gr_flowgraph.cc:86-292` covers connect/disconnect validation and graph partitioning behavior.
- E2 test verified: `gnuradio-runtime/python/gnuradio/gr/qa_flowgraph.py:16-30` and `qa_realtime.py:15-42` cover empty flowgraph lifecycle and realtime scheduling bindings.

## Architecture

Principal components:

- Top-block orchestration layer over a flattened runtime graph.
- Scheduler abstraction that can be stopped and recreated on restart.
- Lock/unlock path for safe live reconfiguration.
- Regression suites for flowgraph validation, lifecycle, and binding behavior.

Most interesting mechanism: restart is not a best-effort restart of threads. The runtime re-flattens the graph, validates it again, merges old connections into the new graph, and recreates the scheduler so a live reconfiguration can proceed from a coherent graph description.

Baseline comparison: a standard DSP application often treats its graph as static after startup. GNU Radio makes graph restart and lock-based reconfiguration part of the runtime contract, which is the more reusable piece.

## Reuse Guidance

Reusable:

- Separate graph validation from scheduler creation.
- Make live reconfiguration an explicit lock/unlock contract.
- Rebuild the flattened graph on restart rather than mutating a stale scheduler in place.
- Keep lifecycle and binding tests close to the top-block surface.

Do not copy:

- Do not copy the full scheduler selection stack without matching workload needs.
- Do not rely on the restart contract without validating it on the actual signal-processing workload.
- Do not assume a lock/unlock API is safe unless you can enforce the calling-thread constraints.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The runtime contract is explicit in the public API and in the implementation.
- Lock/unlock and reconfigure behavior are covered by concrete tests.
- Restart recreates a validated flat graph rather than continuing with stale wiring.

Experimental or incomplete for our needs:

- The runtime is large and general-purpose, so the reusable mechanism is easy to miss behind the breadth.
- The current evidence is lifecycle and validation behavior, not mission-specific RF fault recovery.
- Signal-processing workloads still need corpus and hardware-specific tuning.

Hidden costs and failure modes:

- Unlocking the wrong thread can deadlock reconfiguration.
- A bad restart can rebuild a valid graph that is still semantically wrong for the intended RF chain.
- Broader scheduler/runtime complexity means more operational variability than a narrow domain runtime.

Adoption experiment:

Run a live flowgraph, lock it, swap in a new block chain, force a restart, and confirm the scheduler resumes without deadlock, lost buffers, or stale connections.

## Candidate Patterns

- `lock-gated flowgraph restart`
- `validated flat-flowgraph reconfiguration`
- `scheduler recreation on unlock`
