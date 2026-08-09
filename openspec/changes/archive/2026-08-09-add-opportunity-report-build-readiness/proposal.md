## Why

Opportunity Radar now records build-readiness fields in `opportunities.json` and opportunity records, but a reviewer opening only the daily PR report still has to inspect secondary artifacts to see the paid wedge, distribution channel, private-data boundary, OSS commoditization risk, product shape, pricing hypothesis, and do-not-build-until condition.

That weakens the PR review loop. The report is the first artifact reviewers read, so it should expose the same build gate directly.

## What Changes

Require `opportunity-reports/YYYY-MM-DD.md` to include a `## Build Readiness` section.

The section must contain a markdown table with:

- opportunity;
- paid wedge;
- distribution channel;
- private data barrier;
- OSS commoditization risk;
- product shape;
- pricing hypothesis;
- do not build until;
- build decision.

The deterministic validator will reject reports whose build-readiness table is missing, malformed, uses unsupported enum values, or marks an opportunity selected/selected-for-build while the paid wedge is unclear or the private-data boundary blocks public validation.

## Capabilities

### Modified Capabilities

- `opportunity-radar`: report-level build-readiness visibility and validation.

## Impact

- Updates Opportunity Radar operating prompt and workflow wrapper.
- Updates Opportunity Radar report validation.
- Updates unit tests and OpenSpec.
