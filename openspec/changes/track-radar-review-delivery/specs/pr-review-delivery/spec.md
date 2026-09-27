## Purpose

Ensure generated radar reviews remain pending until their substantive analysis
has been delivered to the intended conversation for the exact reviewed revision.

## ADDED Requirements

### Requirement: Discovery Is Not Delivery

The checker SHALL track delivery independently of PR discovery, summary
generation, CI state, and unchanged metadata for both radar families.

#### Scenario: Unchanged PR without a delivery receipt
- **WHEN** a matching open PR has no confirmed receipt for its current head SHA
- **THEN** the checker includes it in pending content reviews on every check
- **AND** does not describe its review as already delivered

#### Scenario: CI blocks merge
- **WHEN** a pending PR has failed, missing, or approval-blocked validation
- **THEN** the checker still provides its content review with the concrete blocker
- **AND** validation state does not count as delivery evidence

### Requirement: Receipts Identify Revision And Destination

The checker SHALL scope receipts by repository, destination conversation, PR
number, and exact head commit. It MUST NOT infer delivery from PR age or timestamps.

#### Scenario: Receipt matches current revision
- **WHEN** a receipt matches all four identity fields
- **THEN** the repeated content review is suppressed for that destination only

#### Scenario: New commit or different destination
- **WHEN** the PR head changes or the checker targets another conversation
- **THEN** the prior receipt does not suppress the pending content review

#### Scenario: No trustworthy revision or destination
- **WHEN** the checker cannot establish the head SHA or delivery scope
- **THEN** it does not suppress the content review
- **AND** exposes the missing identity information

### Requirement: Delivery Acknowledgement Is Explicit And Evidence Referenced

A receipt SHALL be created only by an explicit acknowledgement identifying an
already visible substantive review, its destination, and reviewed commit. The
system MUST distinguish caller-attested delivery from platform-confirmed delivery.

#### Scenario: Summary printed but reply interrupted
- **WHEN** the helper prepares or prints a review without a later acknowledgement
- **THEN** no delivery receipt exists and the next check repeats the pending review

#### Scenario: Acknowledge delivered review
- **WHEN** the caller confirms a visible substantive review with its message or
  turn reference, repository, destination, PR number, and exact reviewed SHA
- **THEN** the system durably records the receipt with a timestamp
- **AND** repeated acknowledgement is idempotent

#### Scenario: Stale or incomplete acknowledgement
- **WHEN** acknowledgement refers to an older SHA or omits required identity
  or message evidence
- **THEN** it never marks the current different SHA delivered
- **AND** missing fields are rejected rather than guessed

### Requirement: Delivery State Fails Safely

Delivery state SHALL survive process restarts without entering tracked research
files. Missing or unreadable state MUST NOT silently suppress pending reviews.

#### Scenario: First run or lost state
- **WHEN** no receipt store exists
- **THEN** all matching open PR revisions are eligible for review
- **AND** no historical delivery is inferred or backfilled automatically

#### Scenario: Corrupt store or failed write
- **WHEN** state cannot be read or acknowledgement cannot be committed
- **THEN** the checker reports the storage error explicitly
- **AND** does not claim successful delivery or overwrite corrupt state silently

### Requirement: Content Deduplication Does Not Hide Operational State

Delivery receipts SHALL suppress only repeated content reviews, not workflow
failures, schedule waits, or concrete validation blockers.

#### Scenario: Both radar families have pending reviews
- **WHEN** both families have an unacknowledged revision
- **THEN** the checker includes both, regardless of which run finished last

#### Scenario: Delivered content and a failed run
- **WHEN** all current content reviews have receipts but a monitored run failed
- **THEN** the failure remains visible independently of the receipt store

#### Scenario: Delivered content and no new event
- **WHEN** all current revisions are acknowledged and no operational event needs reporting
- **THEN** the result explicitly says there is no pending content review
- **AND** it does not claim that no open PR exists
