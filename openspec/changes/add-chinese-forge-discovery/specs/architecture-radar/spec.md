## ADDED Requirements

### Requirement: Architecture Radar Uses Regional Source Forges
Architecture Radar SHALL include Chinese and regional source forges as explicit discovery surfaces when searching configured topic families.

#### Scenario: Broad discovery includes Chinese forge coverage
- **WHEN** an Architecture Radar run performs broad discovery for configured topic families
- **THEN** it includes Gitee and GitCode discovery queries when network access allows
- **AND** it records the platform name in the candidate ledger discovery source for every candidate found through those surfaces

#### Scenario: Secondary regional source page is discovered
- **WHEN** the run finds a Tencent CODING, Alibaba Codeup, Huawei CodeArts Repo, JiHu/GitLab China, company, product, launch, accelerator, paper, model-card, or documentation page
- **THEN** it treats that page as discovery evidence only unless it exposes inspectable repository source
- **AND** it performs source expansion to locate a stable repository before selecting the candidate for deep review

### Requirement: Regional Candidates Require Stable Source Evidence
Architecture Radar SHALL NOT select a regional-forge candidate for source-level review or deep review unless the candidate has inspectable source code and a stable reviewed revision.

#### Scenario: Regional source exposes a Git-compatible revision
- **WHEN** a candidate from Gitee, GitCode, or another regional forge exposes Git-compatible history
- **THEN** source-inspected and deeply-reviewed records use the full commit SHA, branch or tag, source URL, and review date

#### Scenario: Regional source lacks stable revision evidence
- **WHEN** a candidate page is login-gated, captcha-gated, mirror-only without a visible source revision, or otherwise cannot provide inspectable source and a stable revision
- **THEN** the candidate must remain rejected, inaccessible, or deferred
- **AND** it must not count as selected or deeply reviewed

### Requirement: Regional Mirrors Are Deduplicated
Architecture Radar SHALL deduplicate candidates that appear on both GitHub and a regional forge while preserving the mapping as discovery context.

#### Scenario: Candidate exists on GitHub and a Chinese forge
- **WHEN** the run discovers the same project on GitHub and on Gitee, GitCode, or another regional forge
- **THEN** it identifies the likely upstream or canonical repository when evidence allows
- **AND** it records the mirror or companion-source relationship in the candidate ledger or repository review
- **AND** it avoids reviewing the same source snapshot twice as separate repositories

#### Scenario: Upstream cannot be determined
- **WHEN** the run cannot determine whether GitHub or the regional forge is canonical
- **THEN** it records the ambiguity as an evidence gap
- **AND** it selects at most one source snapshot for review only if the reviewed snapshot still satisfies the normal evidence bar
