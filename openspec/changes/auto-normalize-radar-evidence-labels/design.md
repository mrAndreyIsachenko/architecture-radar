## Context

`scripts/validate-radar-state.py` already knows how to classify evidence paths:

- tests -> `E2 test verified`;
- README/docs/NEWS/CHANGELOG/release/ADR/spec paths -> `E3 maintainer stated`;
- implementation paths can remain `E1 source verified`.

The failure was not a validator gap. It was a model-output gap: the model
ignored the prompt rule and wrote an E1 label for a `spec/` evidence path.

## Decision

Add `scripts/normalize-radar-evidence-labels.py` and run it immediately after
`scripts/run-codex-radar.sh`.

The normalizer scans changed and untracked Markdown artifacts under:

- `reports/`;
- `repositories/`;
- `patterns/`.

For each line containing `E1 source verified`, it inspects backtick-quoted
tokens:

- path-like tokens classified as tests require `E2`;
- path-like tokens classified as docs/spec/release/ADR require `E3`;
- implementation-looking path tokens remain `E1`;
- non-path symbols do not affect normalization.

If every path-like evidence token on the line resolves to the same non-E1
label, the script replaces `E1 source verified` with that label.

If a line mixes implementation evidence with documentation/spec/test evidence,
the script leaves the line unchanged. `scripts/validate-radar-state.py` then
fails as before. This avoids hiding ambiguous claims by downgrading an entire
mixed-evidence sentence.

## Non-Goals

- Do not weaken `scripts/validate-radar-state.py`.
- Do not normalize `E2` or `E3` back to `E1`.
- Do not parse arbitrary Markdown semantics or split mixed-evidence bullets.
- Do not change Opportunity Radar evidence labels.
