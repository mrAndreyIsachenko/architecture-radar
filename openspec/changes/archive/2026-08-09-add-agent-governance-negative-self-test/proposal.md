## Why

Agent governance is enforced by CI, but the repository also needs a deterministic
negative self-test proving that invalid pull request scenarios are rejected. A
passing validator on a valid PR is not enough evidence that the gate blocks bad
metadata or governed behavior changes without OpenSpec evidence.

## What Changes

Add fixture-backed negative tests for the governance validator and run them in
the required `validate` workflow.

The self-test covers:

- missing explicit user request;
- autonomous follow-up marked as allowed;
- governed behavior changes without OpenSpec evidence.

## Capabilities

### Updated Capabilities

- `agent-governance`: adds deterministic negative self-test coverage for CI
  enforcement.

## Impact

- Adds negative fixture data.
- Adds a CLI self-test runner.
- Wires the runner into `radar-validation.yml`.
- Updates setup doctor coverage and unit tests.
