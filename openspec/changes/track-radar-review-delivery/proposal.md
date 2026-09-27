## Why

The heartbeat repeatedly returned status-only replies for PR #91 while treating
unchanged GitHub metadata as proof that its substantive review had already been
delivered. The helper lists open PRs as fresh but has no delivery receipt or
commit identity, so neither suppression nor successful delivery is auditable.

## What Changes

- Separate PR discovery, review preparation, and confirmed delivery for both
  Architecture Radar and Opportunity Radar.
- Key delivery receipts by repository, destination thread, PR number, and exact
  head SHA. Only a confirmed receipt suppresses a repeated content review.
- Add an explicit acknowledgement operation, requiring a reference to an
  already visible substantive review; reading or printing a summary never
  acknowledges delivery.
- Keep unacknowledged PRs eligible on every check, even if unchanged or blocked
  by CI. A new SHA requires a new review.
- Preserve workflow/validation alerts independently of content delivery, and
  expose missing or corrupt state without silently hiding pending reviews.
- Document the heartbeat integration and test interrupted delivery, retries,
  stale acknowledgements, multiple destinations, and both radar families.

Non-goals: changing research selection, fixing CI approval policy or synthetic
check verdicts, changing schedules/models, publishing recovered reports, automatic
merging, and introducing an external notification service.

## Capabilities

### New Capabilities

- `pr-review-delivery`: destination-scoped, revision-specific acknowledgement of
  delivered generated-radar reviews, independent of workflow status.

### Modified Capabilities

None. This complements the pending `pr-review-heartbeat` changes without
rewriting their verdict or research requirements.

## Impact

`scripts/radar-pr-review.py`, `scripts/radar-pr-review-status.py`, the two PR
summarizers, a focused delivery-state helper, tests, and `docs/github-actions.md`.
Runtime state stays outside tracked research and survives process restarts.
No new service, paid model call, or GitHub write is needed. The active heartbeat
must follow the acknowledgement protocol; the helper cannot prove chat delivery
from stdout alone.
