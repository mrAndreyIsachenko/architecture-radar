## Context

`scripts/radar-pr-review.py` delegates content summaries to `scripts/summarize-radar-pr.py` and `scripts/summarize-opportunity-pr.py`. Both summarizers already classify blocking conditions, validation status, draft state, mergeability, changed files, and report summaries. The current success path returns `looks_mergeable`, but the `next_action` still says to manually read the evidence.

## Decision

Keep the existing decision enum:

- `looks_mergeable`
- `needs_manual_review`

Change only the success-path `next_action` strings so they give a concrete user decision point:

- Architecture Radar: merge the PR; if the summarized evidence gaps are unacceptable, request a targeted fix for those gaps.
- Opportunity Radar: merge the PR; if the summarized paid wedge is too weak, request a targeted fix or close/watchlist the opportunity.

This keeps the agent inside governance boundaries: the helper gives a verdict, but it does not perform the merge.

## Rejected Alternatives

- Auto-merge generated radar PRs from the heartbeat. Rejected because repository governance explicitly requires user authorization before merge/close actions.
- Add a third decision enum such as `ready_to_merge`. Rejected because existing callers already consume `looks_mergeable`; the problem is the next action text, not the decision model.
- Ask the user to read the full reports. Rejected because the heartbeat summary already extracts the fields needed for first-pass review.

## Validation

Regression tests should assert that `looks_mergeable` recommendations do not contain `manually read` wording in either Architecture Radar or Opportunity Radar summarizers.
