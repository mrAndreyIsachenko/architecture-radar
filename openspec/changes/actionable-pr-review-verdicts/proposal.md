## Why

The PR-review heartbeat can now find Architecture Radar and Opportunity Radar pull requests, but successful summaries still tell the user to manually read the evidence before merging. That punts the review decision back to the user even when validation passed and the helper already extracted the relevant evidence gaps.

## What Changes

- Make successful generated PR review recommendations actionable.
- Replace generic `manually read...` next actions with concrete merge/close/fix guidance.
- Preserve the hard boundary that agents must not merge or close pull requests without explicit user authorization.
- Add regression coverage so generated review summaries do not reintroduce manual-read punt wording.

## Capabilities

### New Capabilities

### Modified Capabilities

- `pr-review-heartbeat`: Successful Architecture Radar and Opportunity Radar PR summaries must produce actionable review verdicts rather than delegating review back to the user.

## Impact

- Affects `scripts/summarize-radar-pr.py`, `scripts/summarize-opportunity-pr.py`, tests, local heartbeat documentation, and the current heartbeat automation prompt.
- Does not change generated research artifacts, radar schedules, PR publishing, or branch protection.
