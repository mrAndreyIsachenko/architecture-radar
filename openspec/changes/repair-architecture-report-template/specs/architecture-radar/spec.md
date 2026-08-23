## MODIFIED Requirements

### Requirement: Candidate Accounting Is Preserved

Generated reports SHALL include candidate counts, selected repositories, rejected or deferred candidates, evidence gaps, and one concrete next action. Scheduled Architecture Radar runs SHALL normalize the generated report to the canonical required section contract before validating artifacts.

#### Scenario: A report is validated

- **WHEN** `scripts/validate-radar-state.py` validates a changed report
- **THEN** required report sections and candidate-ledger columns must be present

#### Scenario: Generated report omits canonical sections

- **WHEN** the research agent produces a daily report with missing canonical Architecture Radar sections
- **THEN** the workflow repairs the report structure before validation by preserving existing content and adding explicit diagnostic placeholders for unrecoverable omissions

#### Scenario: Generated report omits the candidate ledger

- **WHEN** the research agent produces a daily report without a valid Candidate Ledger section
- **THEN** the workflow adds a diagnostic Candidate Ledger table with the required columns and marks the ledger as repair-generated
