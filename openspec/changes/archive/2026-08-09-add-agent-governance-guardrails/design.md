## Context

Architecture Radar uses autonomous agents to modify workflow prompts, validators, OpenSpec files, and generated research artifacts. The project already has OpenSpec, but the enforcement boundary is too weak unless CI validates that PRs carry user authorization and OpenSpec evidence.

## Decision

Add `AGENTS.md` as the repository-authoritative policy for Codex and other coding agents.

Add `scripts/validate-agent-governance.py` to the `validate` workflow. On pull requests, it reads the GitHub event payload and changed files. It enforces:

- PR body contains `User request:` with a non-placeholder value;
- PR body contains `Scope confirmed: yes`;
- PR body contains `Autonomous follow-up: no`;
- governed behavior changes include OpenSpec evidence in the same PR, either active change files or archived change files;
- generated research artifacts do not require OpenSpec evidence by themselves.

Governed behavior paths include workflows, scripts, OpenSpec specs, Codex skills, agent rules, research scopes, PR template, setup doctor, and `AGENTS.md`.

## Non-Goals

- Do not validate private chat contents.
- Do not contact external services from the validator.
- Do not block generated radar artifacts solely because they lack OpenSpec changes.
- Do not infer user intent from branch names.
