## Why

Opportunity Radar reports already include a signal ledger, but `signals/` can remain too sparse or underspecified. A reviewer should be able to inspect the durable signal notes and find every public source URL used by the run without reconstructing the report manually.

The goal is not to force one file per URL. Grouped notes are acceptable when they enumerate every source URL and include enough metadata for later revision.

## What Changes

Require each changed Opportunity Radar report's Signal Ledger URLs to be covered by date-prefixed signal notes under `signals/`.

For every changed signal note, validate that it contains:

- at least one public URL;
- source date or date range;
- topic family;
- signal type;
- market evidence label;
- concise notes.

## Capabilities

### Modified Capabilities

- `opportunity-radar`: signal-note coverage and metadata validation.

## Impact

- Updates Opportunity Radar operating rules and workflow prompt.
- Updates Opportunity Radar artifact validator.
- Adds unit tests for signal note coverage and malformed signal notes.
