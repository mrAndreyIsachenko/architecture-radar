# RightNow-AI/autokernel

- Repository: https://github.com/RightNow-AI/autokernel
- Review date: 2026-11-12
- Current commit reviewed: `77bfaa4b2d45ec19f33d6582080b44c3784929b7`
- Commit date: 2026-11-08T16:29:39-08:00
- Branch: `main`
- Previous commit reviewed: `78435821cc3d5756ba6ee1785c397f6d8fa8c90d`
- Material changes since previous review: current head adds a dedicated TTFT benchmark lane, cache validation, and end-to-end verification around the persisted optimization loop.
- Decision: track

## Problem Fit

This repository informs `ai-llm-systems`, especially long-running optimization loops that must decide when to continue, revert, or stop based on evidence rather than intuition. The reusable mechanism is not the GPU branding around kernel tuning; it is the persisted orchestration state, the repeatable benchmark gate, and the final verification step that force each candidate through the same safety checks.

## Verified Flow

`extract.py` builds `workspace/optimization_plan.json` from profiling output -> `orchestrate.py` loads the plan, persists `workspace/orchestration_state.json`, and marks kernels `pending`, `optimizing`, `done`, or `skipped` -> `prepare.py` verifies CUDA/Triton/PyTorch, generates deterministic test data, and smoke-tests the current kernel -> `engine/prefill_ttft.py` times streamed requests, validates cached tokens, and emits TTFT summaries -> `verify.py` plugs optimized kernels back into the model, compares outputs, and saves a verification report -> `kernelbench/bench_kb.py` repeats the correctness/performance loop as a reusable evaluation harness.

- E1 source verified: `orchestrate.py` defines `MOVE_ON_CRITERIA`, loads `workspace/optimization_plan.json`, and records keep/revert/failure decisions into the orchestration state and TSV results.
- E1 source verified: `engine/prefill_ttft.py` defines the TTFT benchmark contract, cache validation, cold and warm modes, and streamed-request timing.
- E1 source verified: `prepare.py` verifies the CUDA stack, generates deterministic test data, and performs a kernel smoke test before optimization work begins.
- E1 source verified: `verify.py` loads the model, substitutes optimized kernels, compares outputs with dtype-specific tolerances, and writes the final verification result.
- E1 source verified: `kernelbench/bench_kb.py` defines a reusable correctness/stability/determinism/performance evaluation loop with timeout protection and VRAM tracking.
- E2 test verified: `tests/test_gqa_prefill_attention.py` covers the calibrated attention oracle, paged KV handling, page-size overrides, and calibration behavior.
- E2 test verified: `tests/test_calibrate_attention.py` covers calibration and backend-selection behavior.
- E2 test verified: `tests/test_gqa_prefill_attention_kernel.py` covers the kernel-facing prefill attention path.
- E3 maintainer stated: `kernelbench/program_kb.md` and `README.md` describe the keep/revert contract, the five-stage correctness harness, and the result schema.

## Architecture

Principal components:

- `extract.py`: profile-to-plan extraction.
- `orchestrate.py`: stateful kernel scheduler with move-on criteria.
- `prepare.py`: environment and deterministic input setup.
- `engine/prefill_ttft.py`: TTFT benchmark and cache validation.
- `verify.py`: end-to-end model reintegration and final comparison.
- `kernelbench/bench_kb.py`: reusable correctness, stability, determinism, and performance harness.
- `kernelbench/bridge.py` and `kernelbench/scorer.py`: adapter and scoring utilities around the harness.

Most interesting mechanism: the optimization loop is explicitly stateful and reversible. A candidate kernel is not just benchmarked; it is recorded in workspace state, checked against deterministic setup data, run through correctness and TTFT gates, and only then promoted or reverted using explicit thresholds.

Baseline comparison: a conventional kernel-optimization workflow would rely on ad hoc benchmarking plus manual judgment. This repository instead forces every candidate through a repeatable state machine and a fixed evaluation harness.

## Reuse Guidance

Reusable:

- Treat candidate optimization as a persisted state machine, not a one-shot benchmark.
- Separate setup, correctness, performance, and final verification into explicit phases.
- Keep deterministic test-data generation next to the harness that consumes it.
- Make move-on thresholds explicit and machine-readable.

Do not copy:

- Do not copy the hard-coded `kernel.py` and `workspace/` file conventions without an adapter.
- Do not treat the workspace TSV files as a production persistence layer.
- Do not assume the move-on thresholds are universally valid without workload-specific calibration.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The harness includes deterministic inputs, timeouts, stability checks, and reproducible summaries.
- `verify.py` validates the optimized path against the original model instead of trusting a single microbenchmark.
- The orchestration state is persisted rather than held only in memory.

Experimental or incomplete for our needs:

- The repo is benchmark-driven and GPU-dependent.
- It is shaped around a local workspace rather than a general-purpose orchestration backend.
- There is no conventional automated test suite; the benchmark harness is the main safety surface.

Hidden costs and failure modes:

- Thresholds can be too aggressive or too lax for different kernels.
- Deterministic data generation can mask workload diversity if it becomes the only signal.
- The workflow depends on a functioning CUDA/Triton environment and the local filesystem workspace.

Adoption experiment:

Use the same state-machine shape for one of our agentic optimization loops, then verify that a failed correctness stage prevents promotion and that the stored workspace state can reconstruct the current candidate set after restart.

## Candidate Patterns

- `benchmark-gated optimization loop`
- `workspace-backed experiment ledger`
