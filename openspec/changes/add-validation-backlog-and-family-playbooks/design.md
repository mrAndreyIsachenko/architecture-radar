## Context

See `proposal.md` for motivation. Architecture Radar already has file-backed topic scope, watchlist accounting, report structure validation, and evidence-label validation. The missing piece is a persistent bridge from "this mechanism looks useful but evidence is insufficient" to "this is the concrete validation we should run next."

## Goals / Non-Goals

**Goals:**

- Make privacy networking, drones/robotics, and satellites/space systems less dependent on generic repository search terms.
- Preserve family-specific evidence bars without hard-coding all domain detail into `docs/agent-rules.md`.
- Convert recurring runtime/failure evidence gaps into a durable backlog that can be sorted, reviewed, and tested later.
- Keep the generated report concise while making the next validation step machine-checkable.

**Non-Goals:**

- Do not execute validation experiments in the radar workflow.
- Do not add credentials, simulators, cloud services, VPN clients, or drone/satellite runtimes.
- Do not change Opportunity Radar demand selection in this change.
- Do not force a selected repository in every family when evidence is weak.

## Decisions

### 1. Family Playbooks Are Markdown Files

Add `docs/family-playbooks/<family>.md` for:

- `privacy-networking-vpn`
- `drones-robotics-autonomy`
- `satellites-space-systems`

Each playbook should use stable headings:

- `Family`
- `Mechanisms To Search`
- `Evidence Bar`
- `Selection Bias`
- `Rejection Triggers`
- `Validation Evidence`
- `Useful Search Seeds`

Rationale: the files are easy for humans and agents to read, diff, and tune. A structured YAML format would be stricter, but it would make the playbooks less useful as research guidance. Validation should check presence and headings, not parse every bullet.

### 2. Backlog State Is A Small YAML Ledger

Add `experiments/failure-injection-backlog.yml` with a top-level `items` list. Each item uses stable scalar fields:

- `id`
- `family`
- `source_report`
- `source_repository`
- `mechanism`
- `evidence_gap`
- `validation_type`
- `proposed_validation`
- `success_condition`
- `priority`
- `status`
- `created`
- `last_updated`

Allowed `validation_type` values:

- `runtime`
- `failure-injection`
- `restart-recovery`
- `reconnect-recovery`
- `replay`
- `sitl`
- `fleet`
- `operational`

Allowed `priority` values: `high`, `medium`, `low`.

Allowed `status` values: `open`, `planned`, `running`, `passed`, `failed`, `deferred`, `closed`.

Rationale: YAML is already used for watchlists and is adequate for a small manually reviewable backlog. JSON would be easier to validate, but less pleasant for incremental edits.

### 3. Reports Link To Backlog Through A Required Section

Add a required `Validation Backlog Updates` section to generated Architecture Radar reports. It should either contain a compact Markdown table:

`| Backlog item | Repository | Family | Validation type | Reason | Status |`

or an explicit "No validation backlog update required" statement.

Rationale: this keeps the report reviewable without requiring humans to infer backlog changes from prose. It also gives the PR review helper a deterministic place to surface follow-up tests later.

### 4. Validation Stays Conservative

`scripts/validate-radar-state.py` should validate:

- family playbook files exist and contain required headings;
- `experiments/failure-injection-backlog.yml` exists and has valid item fields;
- changed reports contain `Validation Backlog Updates`;
- referenced backlog ids exist and match report repository/family values;
- selected-report evidence gaps with runtime validation keywords do not omit backlog linkage.

The final rule should use explicit report structure first. If the report uses a table in `Unresolved Evidence Gaps`, validate rows with a runtime/failure validation type. If the report uses prose, require at least one backlog reference when runtime/failure keywords appear with selected repositories.

Rationale: fully understanding arbitrary Markdown prose is brittle. The validator should reward structured sections but still catch the most common failure mode: "needs SITL/restart/replay validation" with no durable backlog item.

### 5. Workflow Prompt Reminds, Validator Enforces

`scripts/run-codex-radar.sh` should remind the agent to read family playbooks and update the validation backlog. The validator remains authoritative in CI.

Rationale: prompt text improves generation quality, but deterministic validation prevents drift.

## Risks / Trade-offs

- Backlog may grow without execution -> Mitigation: include priority, status, source report, and success condition so weekly synthesis can prune or promote items later.
- Keyword detection may miss subtle evidence gaps -> Mitigation: prefer structured `Validation Backlog Updates` and keep the keyword fallback conservative.
- Playbooks may become stale -> Mitigation: keep them short and update them only when reports reveal missed families or bad selections.
- Satellites can pull in broad aerospace repos with weak source evidence -> Mitigation: require mechanisms such as delayed connectivity, command/telemetry loops, safe-mode recovery, scheduling, RF/geospatial pipelines, or constellation coordination.
