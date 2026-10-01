# PeterJBurke/droneserver

- Repository: https://github.com/PeterJBurke/droneserver
- Review date: 2026-10-01
- Current commit reviewed: `06b7d1a6a967553f1f8c025bb6b1fc79d346fd53`
- Commit date: 2026-09-20T16:52:17+00:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `drones-robotics-autonomy`, especially command safety, mission continuity, restart recovery, and operator-visible audit trails for an LLM-driven MAVLink control plane. The reusable mechanism is a server-side guard pipeline that treats the model as untrusted and requires explicit proof before dangerous commands run.

## Verified Flow

`SafeFastMCP.tool()` wraps every tool registration in the guard pipeline -> `droneserver.safety.middleware.guard` authenticates the caller, refreshes vehicle state when needed, computes the effective tier, checks scope, rate limits, confirmation tokens, parameter bounds, geofence, and preconditions, and only then executes the tool -> `safety.config.SafetySettings` defines the default-on controls and cached environment-backed limits -> `safety.audit.AuditLog` writes an append-only JSONL record with verdict, rule, latency, and guard flags -> `tools.safety_ops.inject_failure` and `calibrate` expose simulation-only failure and calibration operations through the same guard surface -> `missions.runner.MissionRunner` creates a mission record, checkpoints after every event, persists the mission state to JSON, resumes after restart, and audits mission transitions -> the mission state machine uses the geofence and the launch elevation it stamped at mission start to decide whether to continue, fail, or command descent.

- E1 source verified: `src/droneserver/safety/config.py::SafetySettings` defines the cached, env-backed safety envelope, including tiers, geofence, preconditions, and rate limiting.
- E1 source verified: `src/droneserver/safety/audit.py::AuditLog.write` and `AuditRecord.to_json` implement the append-only JSONL audit path and preserve the guard flags in the record.
- E1 source verified: `src/droneserver/safety/middleware.py::SafetyLayer` and `guard` implement the authenticate -> state -> tier -> authorize -> rate limit -> confirmation -> bounds -> geofence -> precondition -> execute -> record sequence.
- E1 source verified: `src/droneserver/safety/tiers.py` classifies tools into `read_only`, `normal`, `critical`, and `emergency`, with escalation rules for flight-sensitive arguments.
- E1 source verified: `src/droneserver/tools/safety_ops.py::inject_failure` and `calibrate` route failure experiments and calibration through the same safety wrappers.
- E1 source verified: `src/droneserver/missions/runner.py::MissionRunner` checkpoints mission state, records events, and reloads active missions on restart.
- E2 test verified: `tests/test_spend_accounting.py` covers the offline ledger/correction path that the paper uses to prove the cost model and guard projection, including the measured-versus-unmeasured split.
- E2 test verified: `tests/test_mission_ground_datum.py` covers the mission runner's datum handling, ground-state inference, and restart-sensitive mission bookkeeping.
- E3 maintainer stated: `docs/adversarial_results.md` records 29/29 SITL adversarial cases, including confirmation tokens, geofence rejection, rate limiting, and state-precondition behavior.

## Architecture

Principal components:

- `safety/middleware.py` for the policy gate and execution wrapper.
- `safety/config.py`, `safety/audit.py`, `safety/tiers.py`, and `safety/validation.py` for the guardrails, audit, and classification logic.
- `tools/` for operator-visible drone commands and simulation-only experiments.
- `missions/runner.py` and `missions/state.py` for restartable server-side mission control.
- `docs/safety_review.md`, `docs/adversarial_results.md`, and `docs/reproduce.md` for the paper-style safety narrative and verification evidence.

Most interesting mechanism: the model never gets a raw unsafe action surface. Critical commands are token-gated, audited, scope-checked, and rate-limited before they can reach the vehicle, and mission behavior is checkpointed on the server so the client can disconnect without losing control-plane state.

Baseline comparison: a conventional MCP or drone API would expose the flight command and rely on the caller to behave. This repo makes the server the authority and treats the caller as potentially malicious or confused.

## Reuse Guidance

Reusable:

- Keep a server-side wrapper around every command surface.
- Separate tiering, authorization, rate limiting, confirmation, and geofence checks so each rule can fail closed independently.
- Write an append-only audit line for every command and carry the guard flags in the record.
- Persist long-running mission state on the server so client reconnects do not reset the mission to zero.

Do not copy:

- Do not copy the full LLM-facing tool surface unless you need the same control-plane design.
- Do not rely on docs alone; the safety value comes from the guard and audit code paths.
- Do not use the simulation-only failure tools as evidence of real-aircraft resilience.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The guard order is explicit and the audit schema is stable.
- The repository has large SITL and adversarial coverage, plus mission-state tests.
- The mission runner checkpoints after every event and can resume active missions.

Experimental or incomplete for our needs:

- Real-aircraft operational validation is still outside the repository evidence.
- The safety review itself explicitly says the stack is implemented and tested in simulation, not yet cleared for real hardware.
- The control surface is intentionally paper-shaped and broader than a minimal production API.

Hidden costs and failure modes:

- The audit log is durable, but write latency is part of the command path.
- A bad environment-backed safety setting can still cause a refusal on startup, which is correct but operationally noisy.
- The mission checkpointing and audit pipeline increase the amount of state that needs to be kept coherent under restart.

Adoption experiment:

Run the safety layer with guardrails on and off, then replay a short mission sequence and confirm the server rejects unsafe calls, logs the reason, and resumes the mission state after restart without losing the checkpoint history.

## Candidate Patterns

- `Evidence-Carrying Execution Envelopes`
- `confirmation-token safety gate`
- `append-only command audit log`
