## 1. Scope And Playbooks

- [x] 1.1 Add `satellites-space-systems` to `interests.md` and `docs/research-scope.md`, and verify the family list is consistent across both files
- [x] 1.2 Create `docs/family-playbooks/privacy-networking-vpn.md` with the required headings and verify it names VPN/privacy mechanisms and evidence bars
- [x] 1.3 Create `docs/family-playbooks/drones-robotics-autonomy.md` with the required headings and verify it names command ACK, failsafe, telemetry-loss, mission replay, SITL, and fleet evidence
- [x] 1.4 Create `docs/family-playbooks/satellites-space-systems.md` with the required headings and verify it names delayed connectivity, telemetry/command loops, ground-station automation, scheduling, safe-mode recovery, RF/geospatial pipelines, and constellation coordination

## 2. Report And Backlog Contract

- [x] 2.1 Update `docs/agent-rules.md` so Architecture Radar reads family playbooks, reports under-covered family gaps, and writes `Validation Backlog Updates`; verify the output contract names the new section and table columns
- [x] 2.2 Add `experiments/failure-injection-backlog.yml` with an empty or seed `items` list and verify its schema fields match the design
- [x] 2.3 Update `scripts/run-codex-radar.sh` so generated runs are prompted to read family playbooks and update the validation backlog; verify the prompt mentions the three playbook families and backlog linkage

## 3. Validation And Tests

- [x] 3.1 Update `scripts/validate-radar-state.py` to validate playbook existence/headings and `experiments/failure-injection-backlog.yml`; verify malformed backlog fixtures fail in tests
- [x] 3.2 Update `scripts/validate-radar-state.py` to require `Validation Backlog Updates` in changed reports and validate referenced backlog ids against repository/family values; verify missing or mismatched references fail in tests
- [x] 3.3 Update report structure repair or summary helpers only where needed for the new required section, and verify existing summary tests still pass
- [x] 3.4 Run `python3 -m unittest discover -s tests`, `openspec validate --all --strict --no-interactive`, and `git diff --check`
