## ADDED Requirements

### Requirement: Report Repository Identity Repair Requires Unambiguous Evidence

Architecture Radar SHALL expand a bare repository name in structured report
tables only when its source URL, radar record, and referenced backlog item, when
present, agree on one canonical repository identity. It MUST preserve forge
identity, reject conflicting identities, and keep strict validation enabled.

#### Scenario: Bare name agrees with source and backlog

- **WHEN** a selected ledger row identifies `bumblebee` with the source URL for
  `Sri-Krishna-V/bumblebee` and its referenced backlog item names that repository
- **THEN** repair replaces the abbreviated identity in the ledger and backlog
  report table with `Sri-Krishna-V/bumblebee`
- **AND** a second repair run makes no further changes

#### Scenario: Conflicting or ambiguous identity

- **WHEN** a short name maps to multiple owners or forges, or an explicit owner
  conflicts with the referenced backlog or source URL
- **THEN** repair does not guess or rewrite the explicit identity
- **AND** strict validation rejects the inconsistent output before publication

#### Scenario: Missing identity evidence

- **WHEN** a bare name has no complete source reference establishing its owner
- **THEN** repair leaves the value unchanged and reports the unresolved identity
- **AND** a mismatch remains a validation failure

### Requirement: Agent Completion Includes Artifact Validation

The research agent SHALL be instructed to use canonical repository identities
and run the full radar-state validator before declaring its output complete.
The workflow MUST independently validate artifacts before publication.

#### Scenario: Syntax checks pass but references disagree

- **WHEN** JSON parsing and whitespace checks pass but a report and backlog
  disagree on repository identity
- **THEN** syntax-only success is not sufficient completion evidence
- **AND** the workflow blocks publication until strict validation passes

### Requirement: Failed Research Output Is Recoverable Without Credentials

Architecture Radar SHALL attempt to preserve allowlisted generated output and
run provenance when an executed research run fails before publication. The
recovery bundle MUST exclude credentials, raw agent logs, external clones,
symlinks, and files outside the research allowlist. It MUST NOT convert a failed
run to success or publish an invalid PR.

#### Scenario: Validation fails after generation

- **WHEN** research writes output and subsequent strict validation fails
- **THEN** a downloadable recovery bundle contains the available generated
  files, base commit, run ID, attempt, and report date with bounded retention
- **AND** the run remains failed and publication remains blocked

#### Scenario: Research fails partway through generation

- **WHEN** an executed research step fails after writing some output
- **THEN** recovery preserves the available allowlisted files as incomplete
- **AND** it excludes credentials and unrelated workspace content

#### Scenario: Cadence skips research

- **WHEN** no research step executes because the run is not due or is a duplicate
- **THEN** the workflow does not upload a misleading recovery bundle

### Requirement: Incident Recovery Does Not Invent Missing Research

Recovery of run 36121754617 SHALL use only complete observable file contents or
patches applied against the recorded base commit. Recovered output MUST pass the
existing validators before publication; paid regeneration requires explicit
authorization.

#### Scenario: Logs contain recoverable changes

- **WHEN** complete patches or contents can be recovered from the failed run logs
- **THEN** recovery reconstructs the available output in an isolated checkout
  and records which files were recovered and corrected
- **AND** it runs strict validation without another model invocation

#### Scenario: Logs do not contain a complete output file

- **WHEN** a required output is missing or truncated in the available logs
- **THEN** recovery reports that specific gap rather than fabricating the file
- **AND** it does not launch paid research automatically
