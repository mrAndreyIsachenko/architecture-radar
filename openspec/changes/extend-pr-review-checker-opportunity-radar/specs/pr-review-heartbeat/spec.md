## ADDED Requirements

### Requirement: Heartbeat Checks Architecture And Opportunity Radar
The local PR-review heartbeat SHALL check both Architecture Radar and Opportunity Radar by default.

#### Scenario: No fresh pull requests exist
- **WHEN** the heartbeat runs with the default radar selection
- **THEN** it checks recent runs for `architecture-radar.yml`
- **AND** it checks recent runs for `opportunity-radar.yml`
- **AND** it checks open pull requests matching either generated radar PR pattern before reporting no work

#### Scenario: Caller requests one radar
- **WHEN** the heartbeat is run for only `architecture` or only `opportunity`
- **THEN** it limits workflow, PR, failure, and waiting checks to the requested radar

### Requirement: Heartbeat Detects Opportunity Radar Pull Requests
The local PR-review heartbeat SHALL detect fresh Opportunity Radar pull requests by title or branch.

#### Scenario: Opportunity pull request is open
- **WHEN** an open pull request title matches `Opportunity Radar YYYY-MM-DD`
- **OR** its head branch matches `opportunity-radar/YYYY-MM-DD-*`
- **THEN** the heartbeat reports it as a fresh reviewable Opportunity Radar PR
- **AND** it does not classify the PR as an Architecture Radar PR

### Requirement: Heartbeat Summarizes Opportunity Radar Reports
The local PR-review heartbeat SHALL summarize changed Opportunity Radar reports using opportunity-specific fields.

#### Scenario: Opportunity report is changed
- **WHEN** a fresh Opportunity Radar PR changes `opportunity-reports/YYYY-MM-DD.md`
- **THEN** the summary includes reviewed signal count
- **AND** selected opportunities
- **AND** signal count rows
- **AND** build readiness rows
- **AND** money readiness rows
- **AND** recommended next test
- **AND** evidence gaps

### Requirement: Heartbeat Applies Opportunity Weekly Waiting
The local PR-review heartbeat SHALL wait through GitHub Actions schedule delay on Opportunity Radar due days.

#### Scenario: Opportunity schedule is due but missing
- **WHEN** the current local date is the configured Opportunity Radar weekly due day
- **AND** the scheduled run due time has passed
- **AND** no same-day scheduled Opportunity Radar run exists
- **AND** no fresh Opportunity Radar PR exists
- **THEN** the heartbeat returns `DONT_NOTIFY`

#### Scenario: Opportunity schedule is not due
- **WHEN** the current local date is not the configured Opportunity Radar weekly due day
- **AND** no fresh Opportunity Radar PR exists
- **AND** no latest completed Opportunity Radar run failed
- **THEN** the heartbeat does not wait for an Opportunity Radar run

### Requirement: Heartbeat Reports Failures For Either Radar
The local PR-review heartbeat SHALL report a failed latest completed run for either monitored radar when no fresh PR is waiting for review.

#### Scenario: Opportunity Radar failed
- **WHEN** the latest completed Opportunity Radar run has conclusion `failure`
- **AND** no fresh generated radar PR exists
- **THEN** the heartbeat reports the failed Opportunity Radar run with its run URL and actionable log excerpt when requested
