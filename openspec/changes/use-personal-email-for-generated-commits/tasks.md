## Implementation

- [x] Update Architecture Radar prepare script to configure the shared generated-commit identity.
- [x] Update Opportunity Radar prepare script to configure the shared generated-commit identity.
- [x] Update Weekly Synthesis prepare script to configure the shared generated-commit identity.
- [x] Add regression tests for generated workflow commit identity defaults.

## Validation

- [ ] Run targeted identity tests.
- [ ] Run full unit test suite.
- [ ] Run `openspec validate use-personal-email-for-generated-commits --strict`.
- [ ] Run `scripts/validate-agent-governance.py`.
- [ ] Run `git diff --check`.
