## 1. Rules And Prompt

- [x] 1.1 Update Opportunity Radar operating rules to make first transaction within seven days the primary objective.
- [x] 1.2 Update research scope with cashflow-first discovery sources and anti-bias rules.
- [x] 1.3 Update the CI prompt wrapper to require first-transaction sections, fields, and gates.

## 2. Schema And Validation

- [x] 2.1 Bump `opportunities.json` validation to schema version 2.
- [x] 2.2 Add cashflow-first required fields and money evidence classes to state validation.
- [x] 2.3 Add `Best Paths To First Transaction` report table validation.
- [x] 2.4 Enforce sell-before-build gates for money evidence, one-sentence offer, acquisition path, manual delivery, and time-to-transaction score.

## 3. State And Re-evaluation

- [x] 3.1 Migrate existing `opportunities.json` entries to schema version 2.
- [x] 3.2 Update existing opportunity files with cashflow-first fields and stages.
- [x] 3.3 Add a dry-run re-evaluation report comparing old vs new ranking and explaining stages.

## 4. Tests

- [x] 4.1 Add tests blocking GitHub issues plus adjacent enterprise pricing from sell-before-build.
- [x] 4.2 Add tests allowing paid repetitive manual workflow with reachable buyers to beat technical sophistication.
- [x] 4.3 Add tests proving `budget_adjacency` is stored separately and not treated as direct spend.
- [x] 4.4 Add tests blocking `time_to_transaction_score <= 2` from normal sell-before-build.
- [x] 4.5 Add tests blocking top-ranked commercial opportunities without one-sentence offer and acquisition path.
- [x] 4.6 Add a LangGraph-style regression without hardcoded special casing.

## 5. Verification

- [x] 5.1 Validate Opportunity Radar state and report artifacts.
- [x] 5.2 Validate the OpenSpec change.
- [x] 5.3 Run the relevant and full test suites.
