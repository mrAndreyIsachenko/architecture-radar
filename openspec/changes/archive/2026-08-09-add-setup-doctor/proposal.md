## Why

Architecture Radar is now public, released, and forkable, but a new user can still fail late: missing files, missing GitHub permissions, missing branch protection, no `OPENAI_API_KEY`, stale OpenSpec setup, or absent community/release metadata.

The current documentation describes setup steps, but it does not provide a single command that checks whether a checkout or GitHub repository is ready to run before spending tokens on a workflow run.

## What Changes

Add a local setup doctor command:

```bash
python3 scripts/check-radar-setup.py
```

The doctor should report repository readiness across local files, validation tooling, GitHub repository metadata, Actions workflow configuration, branch protection, secrets, release/tag state, OpenSpec, and community files.

The command must be diagnostic-only. It should not mutate repository settings, create secrets, enable branch protection, or publish anything.

## Capabilities

### New Capabilities

- `setup-doctor`: local diagnostic command for Architecture Radar repository readiness.

### Modified Capabilities

- `architecture-radar`: documentation and validation workflows should include setup doctor checks where appropriate, without changing scheduled research behavior.

## Impact

- Adds `scripts/check-radar-setup.py`.
- Adds unit tests for setup doctor parsing and result classification.
- Documents the command in `README.md`, `QUICKSTART.md`, and release checklist.
- Keeps GitHub API checks best-effort so the command works offline for local file checks.
