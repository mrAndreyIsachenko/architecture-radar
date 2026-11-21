# SuperDeMan/drone-agent

- Repository: https://github.com/SuperDeMan/drone-agent
- Review date: 2026-11-21
- Current commit reviewed: `50046dff00a41e398fe9bbb8e95ccb03ebf963bc`
- Commit date: 2026-10-24T14:11:07+08:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `drones-robotics-autonomy`, especially mission planning, command authorization, replay-safe telemetry, and fail-safe recovery. The reusable mechanism is the separation between a human-reviewable `MissionSpec`, a compiled `MissionPackage`, and a guardian that only accepts leased, signed, package-bound intents.

## Verified Flow

`MissionSpec` rejects control-level keys in task parameters and validates the DAG -> `compile_spec` expands inspection tasks into framework nodes, fills registry-bound defaults without overwriting authored values, and computes a deterministic package hash -> `admit` checks capability, spatial, time, energy, and parameter binding -> `verify_package` rejects unsigned, tampered, expired, wrong-robot, and wrong-key packages -> `Guardian` installs leases, rejects stale epochs and replayed heartbeats, binds each intent to a declared phase, and only dispatches when the lease, heartbeat, and package remain coherent -> uplink tests and safety-runtime tests verify version rollback rejection, accepted-package forwarding, and restart-safe replay.

- E1 source verified: `src/drone_agent/contracts/mission.py::TaskNode`, `_validate_dag`, and `MissionSpec` enforce the planner boundary, control-key filtering, DAG validation, and approved-scope fields.
- E1 source verified: `src/drone_agent/admission/compiler.py::compile_spec` and `lower_inspection` lower the authored spec into a deterministic package without overwriting authored values.
- E1 source verified: `src/drone_agent/admission/admission.py` applies capability, scope, and parameter binding checks before a package is accepted.
- E1 source verified: `src/drone_agent/runtime/signing.py::verify_package` and `src/drone_agent/guardian/core.py::install_lease`, `heartbeat`, and `submit` gate command execution on signature, lease, replay, and phase checks.
- E2 test verified: `tests/admission/test_compiler_and_admission.py`, `tests/contracts/test_package_signatures.py`, `tests/runtime/test_uplink.py`, and `tests/runtime/test_safety_runtime.py` cover package binding, signature rejection, rollback protection, accepted-package forwarding, and restart-safe guardian replay.

## Architecture

Principal components:

- `src/drone_agent/contracts/mission.py` for the authored mission envelope and DAG rules.
- `src/drone_agent/admission/compiler.py` for deterministic lowering into a machine-executable package.
- `src/drone_agent/admission/admission.py` for fail-closed checks before package acceptance.
- `src/drone_agent/runtime/signing.py` and `src/drone_agent/runtime/robot_state.py` for package signing and rollback protection.
- `src/drone_agent/guardian/core.py` and `src/drone_agent/runtime/uplink.py` for lease-gated command execution and operator routing.
- `src/drone_agent/runtime/recording.py` and the runtime tests for replay-safe journals and recovery.

Most interesting mechanism: the approval hash plus lease epoch fence. The package hash binds the compiled mission to the human approval, while the lease and heartbeat logic keep the guardian from accepting stale or replayed work. That is stronger than a simple command queue because it treats the mission envelope itself as a security and recovery boundary.

Baseline comparison: a simpler mission scheduler might accept mutable commands or task parameters and rely on downstream checks. This repo instead makes the mission package immutable, signed, and explicitly leased before the guardian dispatches anything.

## Reuse Guidance

Reusable:

- Model the mission as an authored spec plus a compiled, signed package.
- Reject control-plane fields that try to smuggle commands through task parameters.
- Bind command execution to an approved package hash and a lease epoch.
- Keep restart-safe journals and replay checks separate from the live adapter.

Do not copy:

- Do not copy the full flight stack or the guardian/runtime layout unless you need the same onboard control model.
- Do not assume the current SITL and simulated-adapter tests prove field readiness.
- Do not weaken the package boundary by allowing mutable task parameters to bypass the approval hash.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The repository has explicit contracts for mission spec, approval, signing, and guardian state.
- The tests cover signature rejection, rollback prevention, heartbeat freshness, and restart-safe replay.
- The source makes the approval and lease boundaries visible instead of burying them in one big command loop.

Experimental or incomplete for our needs:

- The repository still needs operational validation beyond SITL and simulated adapters.
- Real aircraft, HIL, or fleet conditions can still expose lease, heartbeat, or restart gaps that the current tests do not cover.

Hidden costs and failure modes:

- Lease or heartbeat contention can block legitimate work if the recovery boundary is too strict.
- Replay windows still depend on the integrity of the journals and the exact adapter restart path.
- Real aircraft validation may surface timing or hardware-state mismatches that the tests do not model.

Adoption experiment:

Run an operational or hardware-backed mission through approval, lease install, dispatch, restart, and recovery, then confirm the package hash, lease epoch, heartbeat checks, and replay journal still converge without duplicate dispatches.

## Candidate Patterns

- `mission-spec / mission-package boundary`
- `lease-fenced guardian submit path`
- `restart-aware onboard journal`

