## Why

Recent Architecture Radar reports repeatedly found the same quality gaps: VPN/privacy remains under-covered, drones/autonomy reviews lack runtime and SITL validation evidence, and selected repositories often produce useful ideas without a follow-up path for testing them. The radar also needs a new satellites/space systems topic family, where delayed connectivity, telemetry, command acknowledgement, and safe recovery are first-class architecture concerns.

## What Changes

- Add file-backed family playbooks for high-risk or under-covered Architecture Radar topic families.
- Add `satellites-space-systems` as an Architecture Radar topic family in scope and interests.
- Require Architecture Radar runs to use family playbooks when searching, selecting, and recording topic gaps for privacy networking, drones/robotics, and satellites/space systems.
- Add a persistent validation backlog for source-backed mechanisms that need runtime, failure-injection, SITL, replay, restart, reconnect, or operational validation before adoption.
- Require generated Architecture Radar reports to connect runtime/failure evidence gaps to backlog items when a selected repository exposes an otherwise useful mechanism.
- Validate the backlog schema and report-to-backlog references deterministically.
- Non-goal: this does not execute experiments, provision infrastructure, or make Opportunity Radar market-demand decisions.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `architecture-radar`: Architecture Radar must use family playbooks for under-covered topic families, include satellites/space systems in candidate accounting, and preserve testable validation backlog items for selected mechanisms with runtime/failure evidence gaps.

## Impact

- Affected configuration and docs: `interests.md`, `docs/research-scope.md`, `docs/agent-rules.md`, new `docs/family-playbooks/*.md`.
- Affected generated-state validation: `scripts/validate-radar-state.py`, tests under `tests/`.
- Affected workflow prompts: `scripts/run-codex-radar.sh`.
- New persistent state: `experiments/failure-injection-backlog.yml`.
