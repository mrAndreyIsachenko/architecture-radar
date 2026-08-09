## 1. Specification

- [x] 1.1 Add OpenSpec proposal for setup doctor.
- [x] 1.2 Add OpenSpec design for local and GitHub checks.
- [x] 1.3 Add setup doctor requirement delta.

## 2. Implementation

- [x] 2.1 Add `scripts/check-radar-setup.py`.
- [x] 2.2 Implement local file, directory, JSON, workflow, OpenSpec, community, release-note, and script checks.
- [x] 2.3 Implement best-effort GitHub checks through `gh`.
- [x] 2.4 Support `--json`, `--repo`, and `--skip-github`.
- [x] 2.5 Return non-zero only when required checks fail.

## 3. Tests

- [x] 3.1 Add unit tests for local check classification.
- [x] 3.2 Add unit tests for JSON output shape.
- [x] 3.3 Add unit tests for GitHub check parsing.
- [x] 3.4 Add unit tests for failure exit behavior.

## 4. Documentation

- [x] 4.1 Document setup doctor in README.
- [x] 4.2 Document setup doctor in QUICKSTART.
- [x] 4.3 Add setup doctor to CONTRIBUTING and release checklist validation commands.
- [x] 4.4 Mention setup doctor in publication checklist.

## 5. Validation

- [x] 5.1 Run `openspec validate --all --strict --no-interactive`.
- [x] 5.2 Run Python tests.
- [x] 5.3 Run script syntax checks.
- [x] 5.4 Run `scripts/check-radar-setup.py --skip-github`.
- [x] 5.5 Run `scripts/check-radar-setup.py --json --skip-github`.
- [x] 5.6 Run `scripts/check-radar-setup.py` with GitHub checks.
