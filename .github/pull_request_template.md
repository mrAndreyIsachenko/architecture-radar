## Summary

- Describe the change in one or two bullets.

## Type

- [ ] Workflow or publishing safety
- [ ] Validation or tests
- [ ] Research scope or examples
- [ ] Generated radar artifacts
- [ ] Documentation
- [ ] Other

## Impact

- Does this affect scheduled `Architecture Radar` runs?
- Does this affect generated artifacts under `reports/`, `repositories/`, `patterns/`, or `radar.json`?
- Does this affect GitHub credentials, Actions permissions, branch protection, or publication behavior?

## Validation

- [ ] `openspec validate --all --strict --no-interactive`
- [ ] `python3 -m unittest discover -s tests`
- [ ] `python3 -m py_compile scripts/*.py tests/*.py`
- [ ] `bash -n scripts/*.sh`
- [ ] `python3 scripts/check-radar-setup.py --skip-github`
- [ ] `scripts/validate-radar-state.py`
- [ ] `git diff --check`
- [ ] Not applicable; explain why:

## Research Artifact Checklist

Complete this section only for generated radar output.

- [ ] Report date is clear.
- [ ] Candidate counts and candidate ledger are present.
- [ ] Deep reviews are pinned to commit SHAs.
- [ ] Important claims carry evidence labels.
- [ ] `E1` is not used for tests, README, docs, changelog, NEWS, releases, or issues.
- [ ] Rejected or deferred candidates include reasons.
- [ ] Next action is concrete and testable.
