## ADDED Requirements

### Requirement: Architecture Radar Expands Company Launches To Repositories

Architecture Radar SHALL treat company, product, launch, and runtime watchlist
entries as discovery seeds and SHALL attempt to map them to inspectable GitHub
repositories before deciding whether source-level review is possible.

#### Scenario: Company seed maps to repositories

- **WHEN** a watchlist entry identifies a company, product, launch, or runtime
  artifact
- **THEN** the run attempts company-to-repository expansion through public
  company pages, product docs, GitHub organizations, papers, model hubs, runtime
  recipes, or linked code
- **AND** any resulting repository candidates are recorded in the candidate
  ledger with the discovery source and mapping evidence

#### Scenario: Company seed has no inspectable repository

- **WHEN** a company, product, or launch seed is relevant but no inspectable
  repository can be linked
- **THEN** the candidate is recorded as deferred, watch-company, watch-product,
  watch-launch, or inaccessible instead of being silently dropped
- **AND** no source-level architecture review is created for the company-only
  signal

#### Scenario: Launch signal is not architecture evidence

- **WHEN** a launch, accelerator, or portfolio page is the only evidence for a
  candidate
- **THEN** the run SHALL NOT present it as source-verified architecture evidence
  or a selected repository without inspectable source code
