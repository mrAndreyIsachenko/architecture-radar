## ADDED Requirements

### Requirement: Opportunity Radar Accounts For Priority Topic Families

Opportunity Radar SHALL account for every priority topic family listed in `opportunity-interests.md` during normal opportunity reports without requiring weak families to produce selected opportunities.

#### Scenario: Normal report records family coverage

- **WHEN** Opportunity Radar creates a normal non-diagnostic report
- **THEN** the report includes a `Topic Coverage` section
- **AND** the section contains every priority family listed in `opportunity-interests.md`
- **AND** each family row records reviewed signal count, best candidate or `None`, decision, and reason

#### Scenario: Priority family has no strong candidate

- **WHEN** a priority family has no selected, deferred, or watchlisted candidate in a run
- **THEN** the report keeps the family in `Topic Coverage`
- **AND** the reason explains whether the family had no fresh signals, weak evidence, duplicate evidence, or insufficient commercial support

#### Scenario: Watchlist is configured

- **WHEN** Opportunity Radar validates `opportunity-watchlist.yml`
- **THEN** the watchlist contains at least one entry for every priority family listed in `opportunity-interests.md`

### Requirement: Opportunity Radar Requires Commercial Delta For Repeated Focus

Opportunity Radar SHALL distinguish carried-forward selected opportunities from fresh opportunity focus and SHALL require new commercial evidence before presenting an already-selected opportunity as the run's main selected focus.

#### Scenario: Existing selected opportunity is carried forward

- **WHEN** an opportunity was already present in `opportunities.json.selected` before the run
- **AND** the report does not record new commercial evidence for it
- **THEN** the report may keep it as carried forward
- **AND** the report must not present it as the main fresh selected opportunity or recommended new focus

#### Scenario: Existing selected opportunity is promoted again

- **WHEN** an opportunity was already present in `opportunities.json.selected` before the run
- **AND** the report presents it as main focus, recommended next test, promoted, selected, or sell-before-build for the current run
- **THEN** the `Commercial Delta` section records new commercial evidence such as paid pilot, inbound request, procurement/RFP, direct buyer or spend evidence, or a new independent company/customer workflow

#### Scenario: GitHub-only delta is present

- **WHEN** a repeated selected opportunity only adds new GitHub issues, stars, discussions, or releases
- **THEN** that evidence is not sufficient commercial delta by itself
- **AND** the report treats the opportunity as carried forward or watchlisted unless other commercial evidence is present
