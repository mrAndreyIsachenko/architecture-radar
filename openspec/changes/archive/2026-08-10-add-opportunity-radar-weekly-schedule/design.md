## Context

Architecture Radar uses a daily wake-up plus a three-day cadence gate because
repository discovery can be expensive and still benefits from frequent checks.
Opportunity Radar researches public demand signals. Those signals are slower
moving and more repetitive, so a weekly schedule gives enough continuity without
burning tokens on low-signal reruns.

## Decision

Add a GitHub Actions schedule to `.github/workflows/opportunity-radar.yml`:

```yaml
schedule:
  - cron: "30 5 * * 2"
```

This runs Tuesday at `05:30 UTC`, which is `08:30 Europe/Moscow`.

Keep `workflow_dispatch` for manual event-driven runs. Do not add a cadence
gate for Opportunity Radar in this change; the schedule itself is already
weekly, and manual runs should remain deliberate.

Update setup doctor from "Opportunity Radar must be manual-only" to
"Opportunity Radar must support both weekly schedule and workflow_dispatch".

## Non-Goals

- Do not change Opportunity Radar research prompts.
- Do not change output schemas.
- Do not add a three-day cadence gate.
- Do not auto-merge generated Opportunity Radar PRs.
