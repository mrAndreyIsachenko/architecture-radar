# Agent Governance

These instructions are mandatory for Codex and any other coding agent working in
this repository.

## Authorization Boundary

- Treat `готово`, `done`, `merged`, `смёрджил`, and equivalent completion
  acknowledgements only as confirmation that the previous step is complete.
- Do not infer permission to start a follow-up, archive an OpenSpec change,
  create a branch, commit, push, open a pull request, merge, or close a pull
  request from an acknowledgement.
- Start new work only when the latest user message explicitly requests that
  work.
- If the user says to continue in an existing pull request, continue in that
  branch and pull request. Do not create another branch or pull request.
- If scope is unclear, stop and ask. Do not fill ambiguity with assumptions.

## OpenSpec Boundary

- Use OpenSpec before non-trivial behavior changes to workflows, validators,
  scripts, agent rules, research scopes, Codex skills, setup checks, or
  persistent process rules.
- Generated radar artifacts under `reports/`, `repositories/`, `patterns/`,
  `radar.json`, `opportunity-reports/`, `opportunities/`, `signals/`,
  `opportunities.json`, and `weekly-reports/` do not need their own OpenSpec
  change when they are only generated research output.
- Archive OpenSpec changes only when explicitly requested, or in the same pull
  request when the user explicitly requests no follow-up pull requests for that
  work.

## Pull Request Boundary

Agent-authored pull requests must record:

- `User request:` with the explicit latest user request being implemented.
- `Scope confirmed: yes` only after scope is confirmed by the user or is
  unambiguous in the latest request.
- `Autonomous follow-up: no`.

The `validate` check enforces these fields and rejects governed behavior changes
without OpenSpec evidence in the same pull request.

