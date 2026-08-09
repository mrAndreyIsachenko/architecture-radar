# agent-governance Specification

## Purpose
Define enforceable repository rules that prevent coding agents from starting
unauthorized follow-up work, creating extra branches or pull requests, or
changing governed behavior without explicit OpenSpec evidence.

## Requirements
### Requirement: Agents Require Explicit User Authorization

Coding agents SHALL NOT treat ambiguous completion messages as permission to continue with new work.

#### Scenario: User signals prior work is complete

- **WHEN** the user says "готово", "done", "merged", "смёрджил", or an equivalent completion acknowledgement
- **THEN** the agent treats it only as completion of the previous step
- **AND** the agent does not create a new branch, commit, pull request, or OpenSpec archive follow-up unless the user explicitly requests that action

#### Scenario: Agent opens or updates a pull request

- **WHEN** a pull request is created or updated by an agent
- **THEN** the pull request body records the explicit user request
- **AND** the pull request body records that scope was confirmed
- **AND** the pull request body records that it is not an autonomous follow-up

### Requirement: Behavior Changes Carry OpenSpec Evidence

Non-trivial behavior changes SHALL include OpenSpec evidence in the same pull request.

#### Scenario: Governed behavior changes

- **WHEN** a pull request changes workflows, scripts, OpenSpec specs, Codex skills, agent rules, research scopes, setup checks, or PR governance files
- **THEN** the pull request includes active or archived OpenSpec change artifacts describing the change

#### Scenario: Generated research artifacts change

- **WHEN** a pull request only changes generated radar artifacts
- **THEN** OpenSpec evidence is not required

### Requirement: Governance Is Enforced In CI

The required `validate` check SHALL enforce agent governance on pull requests.

#### Scenario: Pull request lacks authorization metadata

- **WHEN** a pull request body lacks user request, scope confirmation, or autonomous-follow-up status
- **THEN** validation fails

#### Scenario: Governed behavior changes lack OpenSpec evidence

- **WHEN** a pull request changes governed behavior paths without OpenSpec evidence
- **THEN** validation fails
