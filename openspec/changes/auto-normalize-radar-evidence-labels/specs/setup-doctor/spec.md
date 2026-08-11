## ADDED Requirements

### Requirement: Setup Doctor Checks Radar Evidence Normalization

Setup Doctor SHALL verify that the Architecture Radar workflow includes the deterministic evidence-label normalization step.

#### Scenario: Architecture workflow is configured

- **WHEN** local setup checks inspect `.github/workflows/architecture-radar.yml`
- **THEN** the workflow contains `scripts/normalize-radar-evidence-labels.py`

#### Scenario: Normalizer script is required

- **WHEN** local setup checks inspect the repository files
- **THEN** `scripts/normalize-radar-evidence-labels.py` exists
