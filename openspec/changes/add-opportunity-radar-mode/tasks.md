## 1. OpenSpec Adoption

- [x] 1.1 Add OpenSpec project configuration and baseline Architecture Radar spec.
- [x] 1.2 Add the `add-opportunity-radar-mode` proposal, design, tasks, and delta spec.
- [x] 1.3 Document that non-trivial behavior changes should start with OpenSpec, while generated radar artifacts do not require OpenSpec changes.
- [x] 1.4 Add OpenSpec validation to the project checks.

## 2. Opportunity Radar Scaffold

- [ ] 2.1 Add `opportunity-interests.md` with opportunity research priorities.
- [ ] 2.2 Add `docs/opportunity-agent-rules.md`.
- [ ] 2.3 Add `docs/opportunity-research-scope.md`.
- [ ] 2.4 Add `opportunity-watchlist.yml`.
- [ ] 2.5 Add empty structured state in `opportunities.json`.
- [ ] 2.6 Add artifact directories `opportunity-reports/`, `opportunities/`, and `signals/`.

## 3. Validation

- [ ] 3.1 Add `scripts/validate-opportunity-radar-state.py`.
- [ ] 3.2 Validate required opportunity files and directories.
- [ ] 3.3 Validate opportunity evidence labels and required report sections.
- [ ] 3.4 Validate `opportunities.json` schema.
- [ ] 3.5 Add unit tests for the opportunity validator.

## 4. Workflow

- [ ] 4.1 Add `.github/workflows/opportunity-radar.yml` as manual-only.
- [ ] 4.2 Add `scripts/run-codex-opportunity-radar.sh`.
- [ ] 4.3 Add a deterministic publish allowlist for opportunity artifacts.
- [ ] 4.4 Keep OpenAI credentials out of the publishing step and GitHub credentials out of the model step.

## 5. First Run Review

- [ ] 5.1 Run one manual Opportunity Radar pass.
- [ ] 5.2 Review whether selected opportunities include evidence, repeated pain, money/workaround signal, and a testable offer.
- [ ] 5.3 Decide whether to keep manual-only mode, add cadence guards, or close the mode as insufficiently useful.
