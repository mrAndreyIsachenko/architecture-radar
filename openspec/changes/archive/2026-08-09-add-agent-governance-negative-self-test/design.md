## Context

The governance validator already rejects invalid PR metadata and governed
behavior changes without OpenSpec evidence. The missing layer is proof that
those failure paths stay wired into CI.

## Decision

Add `scripts/test-agent-governance-negative.py`.

The script loads fixture cases from
`tests/fixtures/agent-governance/negative_cases.json`, calls the same validation
functions used by `scripts/validate-agent-governance.py`, and requires every
fixture to produce an expected error substring.

CI runs the script in `radar-validation.yml`. If the validator stops rejecting a
negative case, the self-test exits non-zero and the required `validate` check
fails.

## Non-Goals

- Do not create real GitHub pull requests during validation.
- Do not contact the GitHub API.
- Do not mutate repository state.
- Do not duplicate the full positive validation suite.
