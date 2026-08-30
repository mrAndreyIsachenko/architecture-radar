## Implementation

- [x] Update Architecture Radar PR success recommendations to use actionable merge/fix wording.
- [x] Update Opportunity Radar PR success recommendations to use actionable merge/fix/close/watchlist wording.
- [x] Update heartbeat documentation to state that manual reading is only for blockers or optional deeper audit.
- [x] Update the local heartbeat automation prompt to require actionable verdicts.

## Validation

- [x] Add regression tests that reject `manually read` punt wording on `looks_mergeable`.
- [x] Run focused PR summarizer tests.
- [x] Run full unit tests.
- [x] Run `openspec validate --all --strict --no-interactive`.
- [x] Run `git diff --check`.
