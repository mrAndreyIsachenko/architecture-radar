## Context

The current repository is optimized for Architecture Radar:

- `interests.md` describes engineering research priorities.
- `docs/agent-rules.md` assumes source-level GitHub repository inspection.
- `watchlist.yml` validates repository-like entries and adjacent model/dataset artifacts.
- `reports/`, `repositories/`, `patterns/`, and `radar.json` are organized around repository reviews and extracted architecture mechanisms.
- `scripts/validate-radar-state.py` enforces architecture report structure, watchlist shape, `radar.json`, and evidence label/path consistency.

Opportunity research should reuse the same operating principles but not the same data model. It cares less about commit SHAs and source trees, and more about evidence of demand, repeated pain, willingness to pay, current workarounds, competition, reachability, and a concrete testable offer.

## Goals / Non-Goals

**Goals:**

- Keep Architecture Radar behavior unchanged.
- Add a separate Opportunity/Demand Radar mode with distinct inputs and outputs.
- Use a market-specific evidence taxonomy.
- Preserve candidate/signal ledgers so rejected ideas remain visible.
- Require each selected opportunity to end in a small demand test.
- Make the mode runnable manually before considering any schedule.
- Validate opportunity artifacts deterministically where feasible.

**Non-Goals:**

- Do not build a sales automation or outreach spam system.
- Do not scrape private or authenticated sources in the first implementation.
- Do not add a database, web UI, CRM, billing, or lead pipeline.
- Do not mix opportunity records into `repositories/` or `radar.json`.
- Do not require OpenSpec for generated daily radar artifacts.

## Decisions

### Separate Mode And Artifacts

Opportunity Radar should have separate files:

```text
opportunity-interests.md
opportunity-watchlist.yml
opportunities.json
opportunity-reports/
opportunities/
signals/
docs/opportunity-agent-rules.md
docs/opportunity-research-scope.md
scripts/validate-opportunity-radar-state.py
.github/workflows/opportunity-radar.yml
```

This avoids forcing market signals into the repository-review schema and keeps the current Architecture Radar stable.

### Market-Specific Evidence Labels

Opportunity Radar should use labels calibrated for demand research:

```text
M1 paid demand
M2 repeated pain
M3 competitor proof
M4 workaround evidence
I interpretation
H hypothesis
```

These labels prevent the common failure where a model turns an interesting post into a confident claim that demand exists.

### Manual First, Scheduled Later

The first workflow should be `workflow_dispatch` only. Scheduling should wait until the mode has produced useful reports and validation catches common mistakes.

### Public Signals, Not Cold Outreach

The first implementation should discover public signals from sources such as GitHub issues/discussions, Hacker News, Reddit, Product Hunt, app reviews, job posts, public pricing pages, public forums, and search result snippets where allowed.

It should not contact people, send messages, or automate outbound sales.

### Testable Offer As Output

Each selected opportunity should produce one concrete test:

```text
observed demand signal -> evidence source -> repeated pain -> likely buyer/user -> testable offer -> success/failure threshold
```

## Risks / Trade-offs

- Public market signals are noisy; validation can enforce structure but not truth.
- Many sources have API, rate-limit, licensing, and terms-of-service constraints.
- Money evidence is harder to obtain than complaint evidence.
- A separate mode duplicates some workflow and validation code, but avoids corrupting the current Architecture Radar model.
- Running both radars on schedules can increase token spend; manual mode first keeps cost bounded.
