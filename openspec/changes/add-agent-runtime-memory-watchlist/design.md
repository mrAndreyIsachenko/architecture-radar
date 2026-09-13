## Context

Architecture Radar already supports file-backed discovery through `docs/research-scope.md`, `watchlist.yml`, and `docs/agent-rules.md`. The missed DeepSeek Harness and TencentDB Agent Memory cases show that broad search can land on secondary artifacts while failing to account for the canonical source repository.

## Goals / Non-Goals

**Goals:**

- Make the two current high-signal AI runtime and memory launches impossible to miss in normal Architecture Radar runs.
- Preserve the existing distinction between discovery evidence and source-verified architecture evidence.
- Ensure secondary DeepSeek/Tencent artifacts trigger canonical source expansion before rejection.

**Non-Goals:**

- Do not select either repository automatically.
- Do not add a new workflow, validator, dependency, or generated report.
- Do not weaken coverage requirements for VPN/privacy, drones, satellites, blockchain, or document-AI families.

## Decisions

- Add explicit watchlist entries rather than relying only on broad search terms.
  - Rationale: `watchlist.yml` already has the contract that active entries must be represented in the candidate ledger.
  - Alternative considered: adding only search terms to `docs/research-scope.md`; this would still allow the run to miss the exact repositories.

- Add the repositories as discovery seeds in `docs/research-scope.md`.
  - Rationale: seeds steer broad search and provide comparison baselines even after watchlist entries are satisfied or cooled down.
  - Alternative considered: keeping them only in watchlist; that would solve the immediate miss but not improve adjacent discovery.

- Update `docs/agent-rules.md` with a canonical-source expansion rule for secondary runtime and memory artifacts.
  - Rationale: the DeepSeek case failed because a handbook hit was rejected without forcing a canonical runtime lookup.
  - Alternative considered: encoding only DeepSeek-specific behavior; the more durable mechanism is secondary-artifact-to-canonical-source expansion for named launches.

## Risks / Trade-offs

- AI runtime coverage can dominate future runs -> keep these entries as watchlist accounting, not automatic selections, and preserve per-family coverage rules.
- Canonical source can be ambiguous for vendor ecosystems -> record mapping evidence and ambiguity in the candidate ledger rather than fabricating source confidence.
- A watchlist entry can become stale -> allow normal cooldown/defer decisions after the repo has been accounted for at a stable commit or release.
