## ADDED Requirements

### Requirement: Weekly Synthesis Respects Opportunity Selection State

Weekly synthesis SHALL use `opportunities.json.selected` as the only source of
active Opportunity Radar experiments, and SHALL NOT recommend deferred or
watchlisted opportunities as active next-week work.

#### Scenario: No selected opportunities exist

- **WHEN** `opportunities.json.selected` is empty
- **AND** a weekly synthesis report is produced
- **THEN** the report does not recommend building, running, selling, or testing
  any Opportunity Radar entry as an active next-week experiment
- **AND** deferred or watchlisted opportunities may only be mentioned as blocked,
  watchlisted, deferred, or requiring validation

#### Scenario: Watchlisted opportunity is referenced

- **WHEN** a weekly synthesis report references an opportunity from
  `opportunities.json.watchlisted`
- **THEN** the reference is framed as not selected for active work
- **AND** the report names the missing validation or `do_not_build_until`
  condition before any build work

#### Scenario: Selected opportunity is referenced

- **WHEN** a weekly synthesis report recommends an active Opportunity Radar
  experiment
- **THEN** the referenced opportunity exists in `opportunities.json.selected`
