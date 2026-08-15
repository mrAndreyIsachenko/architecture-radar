## Why

The local PR-review heartbeat currently reports only Architecture Radar runs and PRs, so business-idea output from Opportunity Radar is invisible unless it is checked manually. This creates a misleading no-work result on days when an Opportunity Radar PR exists or has failed.

## What Changes

- Extend the local PR-review checker to monitor both Architecture Radar and Opportunity Radar.
- Report fresh Opportunity Radar PRs with opportunity-specific summaries instead of architecture repository summaries.
- Preserve existing Architecture Radar cadence handling and `DONT_NOTIFY` behavior.
- Add tests for Opportunity Radar PR detection, weekly schedule waiting, failure reporting, and summary output.
- Update docs so the heartbeat instructions cover both technical radar and business-opportunity radar.

## Capabilities

### New Capabilities
- `pr-review-heartbeat`: Local heartbeat behavior for generated radar PR review across Architecture Radar and Opportunity Radar workflows.

### Modified Capabilities

## Impact

- Affects `scripts/radar-pr-review-status.py`, `scripts/radar-pr-review.py`, and related tests.
- May add an opportunity-specific PR/report summarizer.
- Affects README or GitHub Actions docs describing the local heartbeat usage.
- Does not change generated Architecture Radar or Opportunity Radar research artifacts.
- Does not change workflow schedules or publish behavior.
