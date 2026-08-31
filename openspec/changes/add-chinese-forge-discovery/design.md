## Context

See `proposal.md` for motivation. The current Architecture Radar rules already support watchlists, company-to-repository expansion, topic-family playbooks, cooldowns, evidence labels, and source-level review gates. This change widens discovery surfaces without changing the artifact model or weakening the source-evidence requirements.

## Goals / Non-Goals

**Goals:**

- Make Gitee and GitCode explicit discovery sources for Architecture Radar runs.
- Preserve a clear path from regional discovery evidence to a stable source snapshot.
- Prevent duplicate reviews when the same project exists on GitHub and a regional forge.
- Keep regional launch/company/platform pages useful as discovery clues without treating them as source evidence.

**Non-Goals:**

- Do not add a new radar family or separate China Radar mode.
- Do not add credentials, scraping, captcha bypass, or private source access.
- Do not require Opportunity Radar changes.
- Do not require a new candidate ledger schema unless implementation discovers a hard validator assumption that blocks regional URLs.

## Decisions

### Treat Gitee and GitCode as first-class discovery surfaces

Gitee and GitCode should be named in `docs/agent-rules.md`, `docs/research-scope.md`, and the Architecture Radar prompt because they are repository-oriented enough to support source expansion and commit-pinned review.

Alternative considered: add only generic "non-GitHub forges" wording. That is too vague for the agent and would not address the observed blind spot around China-originated projects.

### Treat enterprise/devops platforms as secondary discovery evidence

Tencent CODING, Alibaba Codeup, Huawei CodeArts Repo, JiHu/GitLab China, company pages, launch pages, product pages, papers, and docs should trigger source expansion, but they should not be accepted as source evidence unless a public source tree and stable revision are inspectable.

Alternative considered: force all of these into the same discovery tier. That would inflate the candidate ledger with inaccessible or product-only pages and make review quality worse.

### Store platform evidence in existing fields first

The existing candidate ledger already has `URL`, `discovery source`, `decision`, and rejection/deferral reason fields. The implementation should use those fields for platform names, mirror mappings, and access gaps before changing schemas.

Alternative considered: add new ledger columns such as `forge`, `canonical_url`, and `mirror_url`. That can be added later if reports show repeated ambiguity, but it increases validation and report churn before the need is proven.

### Stable revision remains the selection gate

Regional candidates can be discovered and triaged from web pages, but source-inspected and deeply-reviewed candidates still need inspectable source and a stable commit SHA or equivalent Git-compatible revision. Login-gated, captcha-gated, or non-stable views should be rejected, inaccessible, or deferred.

Alternative considered: allow non-GitHub candidates to be selected with weaker revision evidence. That would break the radar's core property: claims are tied to stable source snapshots.

### Prefer canonical source when mirrors exist

When GitHub and a Chinese forge expose the same project, the agent should identify canonical/upstream evidence when possible, record the relationship, and review only one source snapshot.

Alternative considered: review each forge URL independently. That would create duplicate radar entries and distort coverage metrics.

## Risks / Trade-offs

- Regional forge search results may be sparse or inconsistent -> require explicit ledger deferral rather than forcing selections.
- Some platforms may require login, captcha, or regional network access -> record as inaccessible; do not add credentials or bypass steps.
- Mirror direction may be ambiguous -> record ambiguity and choose at most one stable snapshot if the source evidence still clears the bar.
- More discovery surfaces can increase token and search cost -> keep source inspection targeted and stop early when source stability is missing.
- Non-English source/docs can increase misinterpretation risk -> rely on source tree, commit history, tests, and machine-translatable documentation only as E3 maintainer evidence.

## Migration Plan

1. Update Architecture Radar operating docs and prompt text to name the new discovery surfaces and source-stability rules.
2. Run validators and tests to catch schema assumptions.
3. Let the next scheduled Architecture Radar run prove whether the new surfaces produce useful candidates or only deferred ledger rows.

Rollback is straightforward: revert the docs/prompt changes and remove the OpenSpec change if the additional sources create noise without useful candidates.

## Open Questions

- Whether dedicated ledger columns for `source_platform`, `canonical_url`, and `mirror_url` are worth adding after one or two live runs.
