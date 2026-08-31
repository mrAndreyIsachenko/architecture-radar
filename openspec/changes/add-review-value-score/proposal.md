## Why

Generated radar pull requests can pass validation while still adding little value: repeated topics, weak market evidence, or no material architecture delta. The PR review helper needs a deterministic value layer so "valid Markdown" is not treated as equivalent to "useful radar output".

## What Changes

- Require Architecture Radar and Opportunity Radar reports to include a `Review Value` section.
- Make the section expose a review verdict, score, reason, and recommended PR action.
- Validate that new reports include a non-empty, supported value verdict.
- Teach report summarizers and PR summarizers to parse the value verdict and turn it into actionable `merge`, `fix`, or `close/watchlist` guidance.
- Keep the value layer deterministic; the code does not re-run research or independently judge repository/source quality.

## Capabilities

### New Capabilities

### Modified Capabilities

- `architecture-radar`: generated architecture reports expose a review value verdict that downstream review tooling can parse.
- `opportunity-radar`: generated opportunity reports expose a review value verdict that downstream review tooling can parse.

## Impact

- Affected docs: `docs/agent-rules.md`, `docs/opportunity-agent-rules.md`, `docs/github-actions.md`.
- Affected scripts: report summarizers, PR summarizers, and radar state validators.
- Affected tests: summarizer and validator unit tests.
- No new external dependencies or credentials.
