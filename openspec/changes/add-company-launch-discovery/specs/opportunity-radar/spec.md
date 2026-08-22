## ADDED Requirements

### Requirement: Opportunity Radar Accounts For Company Launch Signals

Opportunity Radar SHALL include public company-launch sources as discovery
seeds for priority topic families and SHALL classify them separately from
commercial demand proof.

#### Scenario: Company launch source is reviewed

- **WHEN** a normal or mixed Opportunity Radar run reviews launch, accelerator,
  portfolio, batch, demo-day, or product-launch sources
- **THEN** the report ledger records the company or product, source URL, topic
  family, signal type, source class, evidence label, decision, and reason

#### Scenario: Company launch lacks commercial proof

- **WHEN** a company-launch signal lacks independent evidence for buyer, paid
  wedge, recurring workflow, and permissionless validation path
- **THEN** the opportunity remains watchlisted or deferred
- **AND** the report SHALL NOT mark it selected-for-build based only on launch,
  accelerator, portfolio, or batch presence

#### Scenario: Company launch points to repositories

- **WHEN** a company-launch signal links to GitHub repositories, SDKs, runtimes,
  papers, docs, benchmarks, model hubs, or recipes
- **THEN** the report records those adjacent artifacts as follow-up sources
- **AND** Architecture Radar can use them as company-to-repository expansion
  candidates
