## Why

The repository needs enforceable guardrails that prevent autonomous agent follow-up loops. Chat-only rules are insufficient: they do not survive context shifts and they cannot be reviewed by CI.

The failure mode to prevent is an agent interpreting ambiguous messages such as "готово" as permission to create more branches, commits, pull requests, or OpenSpec archive follow-ups.

## What Changes

Add repository-level agent instructions and deterministic pull request validation.

The guardrails require:

- OpenSpec evidence for non-trivial behavior changes;
- explicit user request metadata in pull request bodies;
- explicit scope confirmation before implementation;
- no autonomous follow-ups after "готово", "done", "merged", or similar completion messages;
- no automatic OpenSpec archive pull requests without explicit user instruction;
- reuse of the existing pull request when the user asks not to create more PRs.

## Capabilities

### Added Capabilities

- `agent-governance`: repository and CI rules for agent behavior.

## Impact

- Adds `AGENTS.md`.
- Adds a deterministic PR governance validator.
- Updates pull request template and validation workflow.
- Updates setup doctor coverage.
- Adds unit tests.
