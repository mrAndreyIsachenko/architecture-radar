## MODIFIED Requirements

### Requirement: Candidate Accounting Is Preserved

Generated reports SHALL include candidate counts, selected repositories, rejected or deferred candidates, evidence gaps, and one concrete next action. The workflow SHALL normalize safe candidate-ledger URL column aliases before strict validation, but validation SHALL still fail when the ledger lacks URL data.

#### Scenario: A report is validated

- **WHEN** `scripts/validate-radar-state.py` validates a changed report
- **THEN** required report sections and candidate-ledger columns must be present

#### Scenario: Candidate ledger has a safe URL alias

- **WHEN** the pre-validation normalization step sees a `Candidate Ledger` table with a URL-like alias such as `Repository URL`
- **THEN** it rewrites that header to the canonical `URL` column before validation

#### Scenario: Candidate ledger lacks URL data

- **WHEN** the pre-validation normalization step sees a `Candidate Ledger` table without a URL-like column
- **THEN** it leaves the table unchanged so strict validation fails
