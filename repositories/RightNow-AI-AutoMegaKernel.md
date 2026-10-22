# RightNow-AI/AutoMegaKernel

- Repository: https://github.com/RightNow-AI/AutoMegaKernel
- Review date: 2026-10-22
- Current commit reviewed: `884534c4d2dbed4381576f81a79ae97feca53c34`
- Commit date: 2026-06-30T03:58:13+03:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `ai-llm-systems`, especially long-running agent loops that must search, validate, and keep only correctness-bearing CUDA schedule candidates. The reusable mechanism is not the branding around megakernel synthesis; it is the locked edit surface, correctness-gated evaluation, and persisted trial log that let an agent optimize latency without trusting a wrong kernel.

## Verified Flow

Model graph -> `schedule.graph.ModelGraph` normalizes the decoder into explicit op and weight metadata -> `harness.propose` exposes the current `ScheduleConfig` plus the editable search surface -> `schedule.search.search` lowers a candidate, validates it, predicts or measures latency, and keeps it only when it improves the incumbent -> `eval.bench.bench` refuses to emit latency for an incorrect kernel -> `harness.loop` logs every trial to `results.tsv` and keeps the best valid schedule -> `autoresearch` checkpointing tests prove the campaign resumes from persisted state and keeps the honesty rule intact -> `tests/test_harness.py` and `tests/test_autoresearch.py` pin the propose/evaluate/loop invariants, rejected-config behavior, and resumable campaign state.

- E1 source verified: `harness.py:13-37` defines the `propose` / `evaluate` / `loop` contract and states that latency is never emitted without correctness.
- E1 source verified: `harness.py:91-129` normalizes kernel knobs, preserves default identity, and keeps the schedule ID stable when knobs are untouched.
- E1 source verified: `schedule/graph.py:5-28,127-185` turns a decoder into a structural graph IR with explicit weights, tensor shapes, and model metadata.
- E1 source verified: `schedule/search.py:13-33,85-145,239-260` implements explore/exploit search, lower-before-score, and keep/revert selection around validated candidates.
- E1 source verified: `eval/bench.py:5-26,127-209` enforces the correctness gate and refuses to report a latency for a wrong kernel.
- E1 source verified: `eval/__init__.py:1-12` states the honesty invariant for the fixed eval surface.
- E2 test verified: `tests/test_harness.py:41-155` covers proposal shape, correct vs broken evaluation, crash-free rejection, loop logging, and CLI smoke.
- E2 test verified: `tests/test_autoresearch.py:33-100` covers unattended runs, results logging, corpus population, checkpoint/resume, move-on plateau behavior, and warm starts.

## Architecture

Principal components:

- Graph importer that turns a known decoder family into an explicit IR.
- Schedule search that mutates only a bounded, validated config surface.
- Correctness-gated benchmark that refuses to quote timings for wrong kernels.
- Flywheel logging and corpus persistence for trial retention and warm starts.
- Autoresearch/orchestrator glue that checkpoints campaigns and resumes them.

Most interesting mechanism: the runtime treats correctness as a hard precondition for any timing claim. A candidate can be rejected, measured, or kept, but it cannot silently become a performance result unless the reference/eager comparison passes first. That makes the search loop usable as an autonomous agent rather than a benchmark script.

Baseline comparison: a conventional GPU-tuning workflow would benchmark candidate schedules first and trust the fastest one. This repository narrows that space by making validation a gate, not a post-hoc check, and by persisting the full trial history so the campaign can resume instead of restarting from scratch.

## Reuse Guidance

Reusable:

- Put the correctness gate in front of every latency number.
- Keep the editable search surface explicit and bounded.
- Persist trial history and best-known state so the campaign can resume.
- Separate graph import, schedule lowering, and benchmarking into distinct layers.
- Keep predictions and measurements labeled differently.

Do not copy:

- Do not copy the CUDA-specific search space as a generic tuning API.
- Do not treat the local results TSV as a durable system of record beyond this workflow.
- Do not assume the measured-gpu path exists on every host; the CPU fallback is a reference path only.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The harness distinguishes valid, correct, measured, and predicted states explicitly.
- Invalid configs fail cleanly instead of crashing the loop.
- The test suite covers loop logging, checkpoint/resume, and warm-start behavior.
- `results.tsv` and the corpus give the agent a persistent trail instead of ephemeral state.

Experimental or incomplete for our needs:

- The repository still needs a live CUDA run on a real GPU to validate the measured path under actual device timing.
- The current evidence is strongest on the toy model and harness invariants, not on large-model or multi-host deployment behavior.
- The benchmark path is correct by construction, but it still depends on hardware-specific execution and a stable local environment.

Hidden costs and failure modes:

- A wrong kernel can still waste search budget even if it cannot be promoted.
- The search can overfit the local benchmark shape if the candidate surface is too narrow.
- The honesty guarantee depends on all measured latencies flowing through the same benchmark gate.

Adoption experiment:

Run `autoresearch` on a real CUDA-capable host, force one invalid schedule and one valid schedule through the loop, and confirm the invalid candidate never emits a measured latency while the valid candidate produces a persisted best schedule and a resumable trial log.

## Candidate Patterns

- `correctness-gated search loop`
- `truthful latency reporting`
- `flywheel-backed trial ledger`
