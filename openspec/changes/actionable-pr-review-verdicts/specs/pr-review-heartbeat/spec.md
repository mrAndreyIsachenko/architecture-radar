## ADDED Requirements

### Requirement: Heartbeat Review Verdicts Are Actionable
The local PR-review heartbeat SHALL give the user an actionable verdict for generated Architecture Radar and Opportunity Radar pull requests.

#### Scenario: Generated PR passes automated review checks
- **WHEN** a generated radar pull request has a passing required validation check
- **AND** the pull request is not a draft
- **AND** the pull request is mergeable or GitHub reports mergeability as unknown
- **AND** the changed report files are summarized successfully
- **THEN** the review recommendation is `looks_mergeable`
- **AND** the next action tells the user whether to merge, close, or request a specific fix
- **AND** the next action does not tell the user to manually read the report or evidence as the primary next step

#### Scenario: Generated PR has a blocking condition
- **WHEN** validation failed, validation is missing or pending, no generated report file changed, report summarization failed, the PR is draft, or GitHub reports a non-mergeable state
- **THEN** the review recommendation is `needs_manual_review`
- **AND** the next action identifies the smallest blocking condition to resolve

#### Scenario: Agent lacks merge authorization
- **WHEN** a generated PR review recommendation is `looks_mergeable`
- **THEN** the heartbeat does not merge or close the pull request
- **AND** the next action asks the user for an explicit merge, close, or fix decision
