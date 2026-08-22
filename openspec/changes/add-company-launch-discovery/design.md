## Context

Architecture Radar currently starts from repositories, model/runtime artifacts,
and related technical sources. Opportunity Radar starts from public pain signals
and explicit opportunity seeds. This works well for mature open-source projects,
but it misses early company-led signals where the first public artifact is a YC
profile, launch page, portfolio listing, product site, pricing page, or docs
rather than a GitHub repository with obvious topics.

Degla and RightNow/RunInfra show two distinct gaps:

- a company can be relevant to a priority family even when no source-level
  repository exists yet;
- a company launch can hide relevant repositories under a different company,
  product, or GitHub organization name.

## Goals / Non-Goals

**Goals:**

- Make company-launch sources explicit Opportunity Radar discovery seeds.
- Require Architecture Radar to expand company/product launches into related
  GitHub organizations and repositories when inspectable code exists.
- Support watchlist entries that are not repositories.
- Preserve the rule that launch/accelerator presence is a seed, not demand
  proof or source evidence.
- Add concrete watchlist entries for Degla and RightNow/RunInfra.

**Non-Goals:**

- Do not add scraping, authenticated source access, outreach, or sales
  automation.
- Do not treat YC, accelerator, or launch presence as `M1 paid demand`, `M2
  repeated pain`, or selected-for-build evidence by itself.
- Do not require Architecture Radar to deep-review companies without
  inspectable repositories.
- Do not change schedules, cadence, model selection, or publish permissions.

## Decisions

1. Add company-launch discovery to the existing scopes instead of creating a
   third radar mode.

   Rationale: this is an input-source gap, not a new output domain. Opportunity
   artifacts already support watchlisted opportunities, and Architecture Radar
   already supports adjacent artifacts and watch modes.

   Alternative considered: create a separate "Company Radar". That would add
   workflow and validation overhead before there is evidence that company-only
   tracking deserves its own artifact family.

2. Treat launch/company signals as discovery seeds unless independently
   corroborated.

   Rationale: accelerator acceptance and launch pages prove topical movement,
   not buyer pain or willingness to pay. Reports must label these as company,
   launch, product, or news source classes unless stronger evidence exists.

   Alternative considered: promote YC batch entries directly into selected
   opportunities. That would reintroduce the same over-selection failure the
   commercial filter was built to prevent.

3. Add company-to-repository expansion to Architecture Radar.

   Rationale: company names, product names, and GitHub organization names often
   diverge. A source-first search can miss repositories such as runtimes,
   kernels, SDKs, benchmarks, and demos if it only searches broad GitHub topics.

   Alternative considered: manually add every discovered repository to
   `watchlist.yml`. Manual watchlist entries remain useful, but the operating
   rule should force future runs to perform the expansion step.

4. Extend watchlist types conservatively.

   Rationale: `watch-company`, `watch-product`, and `watch-launch` should force
   ledger accounting without implying source-level review. `watch-runtime`
   remains the Architecture Radar path when a company expansion finds
   inspectable runtime code.

## Risks / Trade-offs

- More launch sources can increase noise -> require company-launch rows to stay
  watchlisted unless paid wedge, buyer, repeatability, and validation path are
  separately evidenced.
- Company pages can be marketing-heavy -> require the report to classify source
  class and evidence label explicitly.
- Company-to-repo mapping can be ambiguous -> require the ledger to record the
  mapping path and defer when ownership or relevance is unclear.
- Watchlists can bias discovery -> reports already track discovery mode; keep
  watchlist-directed runs from being presented as market-wide winners.
