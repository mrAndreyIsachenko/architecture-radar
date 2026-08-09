## Why

Opportunity Radar reports now expose build-readiness metadata, and `opportunities.json` stores the same fields for structured comparison. Without a cross-check, a generated PR can still show one build decision in the report and a different decision or private-data boundary in the state file.

That creates review ambiguity: reviewers cannot tell which artifact is authoritative.

## What Changes

Validate that every `Build Readiness` table row in a newly generated or changed opportunity report corresponds to an entry in `opportunities.json`.

For matched rows, require the report to agree with state on:

- build decision / stage;
- paid wedge;
- distribution channel;
- private data barrier;
- OSS commoditization risk;
- product shape;
- pricing hypothesis;
- do-not-build-until condition.

Also validate that each `opportunities.json` entry's `stage` agrees with the array it is stored under.

## Capabilities

### Modified Capabilities

- `opportunity-radar`: report/state consistency for build-readiness decisions.

## Impact

- Updates Opportunity Radar operating rules.
- Updates Opportunity Radar state/report validator.
- Adds unit tests for report/state mismatch and array/stage mismatch.
