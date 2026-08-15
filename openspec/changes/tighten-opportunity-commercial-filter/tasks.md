## 1. Rules And Prompt

- [x] 1.1 Update Opportunity Radar rules with cross-company glue and build-vs-buy filtering.
- [x] 1.2 Update opportunity research scope with commercial-filter search criteria, negative signals, and scoring guidance.
- [x] 1.3 Update the GitHub Actions prompt wrapper with commercial-filter field and report-section requirements.

## 2. Validation And State

- [x] 2.1 Add commercial-filter fields and internal-build likelihood validation to `scripts/validate-opportunity-radar-state.py`.
- [x] 2.2 Add report validation for `Commercial Filter` rows and state consistency.
- [x] 2.3 Add selected opportunity file validation for commercial-filter sections and anti-platform wedge checks.
- [x] 2.4 Migrate existing `opportunities.json` entries and opportunity files with conservative commercial-filter metadata.

## 3. Documentation And Tests

- [x] 3.1 Update README or GitHub Actions docs for the stricter Opportunity Radar commercial filter.
- [x] 3.2 Update Opportunity Radar summarizer output for commercial-filter rows.
- [x] 3.3 Add tests for internal-build likelihood, unclear multi-provider usage, missing money flow, and platform-shaped wedges.
- [x] 3.4 Run focused tests, full tests, and OpenSpec validation.
