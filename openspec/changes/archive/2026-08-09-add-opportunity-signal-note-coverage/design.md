## Context

The report ledger is the review table. `signals/` is the durable evidence scratchpad. If the two are not connected, future review has to trust that the ledger was copied correctly.

## Decision

For a report `opportunity-reports/YYYY-MM-DD.md`, the validator will gather signal notes matching `signals/YYYY-MM-DD-*.md`.

The report passes only when every URL in its `Signal Ledger` appears in those signal notes. A grouped note can satisfy multiple ledger rows by listing every URL.

Each changed signal note must include these lightweight fields in markdown text:

- `Sources` with at least one `http` or `https` URL;
- `Date` or `Date range`;
- `Family`;
- `Signal type`;
- `Labels`;
- `Notes`.

Labels must use Opportunity Radar market evidence labels, not Architecture Radar E-labels.

## Non-Goals

- Do not rewrite historical signal notes.
- Do not require exactly one signal file per ledger row.
- Do not require YAML front matter or a new structured file format.
- Do not validate that the source date is semantically correct.
