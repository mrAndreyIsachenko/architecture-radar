## ADDED Requirements

### Requirement: Weekly Synthesis Uses Separate Reports

Weekly synthesis SHALL store generated synthesis output separately from Architecture Radar and Opportunity Radar run artifacts.

#### Scenario: Weekly synthesis report is generated

- **WHEN** the weekly synthesis workflow completes with file changes
- **THEN** it writes the report under `weekly-reports/`
- **AND** it does not write repository reviews under `repositories/`
- **AND** it does not write pattern files under `patterns/`
- **AND** it does not write opportunity records under `opportunities/`
- **AND** it does not modify `radar.json` or `opportunities.json`

### Requirement: Weekly Synthesis Does Not Perform Discovery

Weekly synthesis SHALL synthesize already committed radar artifacts rather than discovering new external candidates.

#### Scenario: Synthesis agent runs

- **WHEN** the model step runs
- **THEN** it reads existing repository artifacts
- **AND** it does not clone external repositories
- **AND** it does not perform live web or GitHub discovery for new candidates

### Requirement: Weekly Synthesis Produces A Focused Next Step

Weekly synthesis SHALL identify the strongest next-week focus from accumulated evidence.

#### Scenario: Weekly report is written

- **WHEN** a weekly synthesis report is produced
- **THEN** it summarizes pattern movement, topic coverage, repeated candidates or signals, decisions and experiments, evidence gaps, and one next-week focus

### Requirement: Weekly Synthesis Publishes Pull Requests

Weekly synthesis SHALL publish generated reports through pull requests rather than pushing directly to `main`.

#### Scenario: Weekly workflow produces changes

- **WHEN** the workflow has generated weekly report changes
- **THEN** the deterministic publish step commits only allowlisted weekly synthesis artifacts
- **AND** opens a pull request against `main`
