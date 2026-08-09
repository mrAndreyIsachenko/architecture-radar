# Architecture Radar Specification

## Purpose

Architecture Radar maintains an evidence-backed library of reusable engineering mechanisms discovered in open-source repositories. It is a scheduled research system, not a newsletter.

## Requirements

### Requirement: Scheduled Research Produces Pull Requests

The system SHALL run Architecture Radar research through GitHub Actions and publish generated research artifacts as pull requests rather than pushing directly to `main`.

#### Scenario: Scheduled run produces artifacts

- **WHEN** the scheduled Architecture Radar workflow completes a research run with file changes
- **THEN** it opens or updates a pull request containing only allowed research artifacts

#### Scenario: No generated change

- **WHEN** the workflow determines that no research run is due or no artifacts changed
- **THEN** it exits without opening a new pull request

### Requirement: Research Scope Is File-Backed

The system SHALL treat repository files as the authoritative research configuration.

#### Scenario: Agent starts a run

- **WHEN** the research agent starts
- **THEN** it reads `interests.md`, `watchlist.yml`, `docs/agent-rules.md`, and `docs/research-scope.md`

#### Scenario: Missing prerequisites

- **WHEN** required workspace files are missing
- **THEN** the run produces a diagnostic report instead of synthetic research reviews

### Requirement: Repository Reviews Are Evidence-Labeled

Generated reports and repository reviews SHALL distinguish source-verified facts, test-verified behavior, maintainer claims, interpretation, and hypotheses.

#### Scenario: Source evidence path is documentation

- **WHEN** a generated artifact labels a README, documentation, changelog, NEWS, release, issue, or ADR path as `E1 source verified`
- **THEN** validation fails and requires a weaker evidence label

#### Scenario: Source evidence path is a test

- **WHEN** a generated artifact labels a test path as `E1 source verified`
- **THEN** validation fails and requires `E2 test verified`

### Requirement: Candidate Accounting Is Preserved

Generated reports SHALL include candidate counts, selected repositories, rejected or deferred candidates, evidence gaps, and one concrete next action.

#### Scenario: A report is validated

- **WHEN** `scripts/validate-radar-state.py` validates a changed report
- **THEN** required report sections and candidate-ledger columns must be present

### Requirement: The Research Agent Cannot Publish Its Own Changes

The workflow SHALL separate model execution from GitHub publication authority.

#### Scenario: Agent step runs

- **WHEN** the Codex research step runs
- **THEN** it receives OpenAI credentials but no GitHub token

#### Scenario: Publish step runs

- **WHEN** the deterministic publish step runs
- **THEN** it stages only the allowlisted artifact paths
