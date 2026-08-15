## Context

The local heartbeat currently uses `scripts/radar-pr-review.py`, which delegates to `scripts/radar-pr-review-status.py` and `scripts/summarize-radar-pr.py`. That stack is Architecture Radar specific: it checks `architecture-radar.yml`, detects `Architecture Radar YYYY-MM-DD` PRs, applies a 3-day cadence guard, and summarizes `reports/`, `repositories/`, `patterns/`, and `radar.json`.

Opportunity Radar is already separate: it runs through `opportunity-radar.yml`, publishes PRs titled `Opportunity Radar YYYY-MM-DD`, and writes `opportunity-reports/`, `opportunities/`, `signals/`, and `opportunities.json`. The heartbeat should surface those PRs and failures without merging market artifacts into Architecture Radar summaries.

## Goals / Non-Goals

**Goals:**
- Make the default local heartbeat check both Architecture Radar and Opportunity Radar.
- Preserve Architecture Radar cadence semantics.
- Add Opportunity Radar weekly schedule awareness for Tuesday 05:30 UTC.
- Summarize Opportunity Radar PRs using opportunity-specific fields: reviewed signals, selected opportunities, watchlisted items, readiness tables, recommended next test, and evidence gaps.
- Keep JSON output machine-readable enough for the ChatGPT scheduled task to format a concise Russian message.

**Non-Goals:**
- Do not change either research workflow's schedule.
- Do not change generated research artifacts.
- Do not merge Opportunity Radar files into Architecture Radar state.
- Do not auto-merge or close PRs.

## Decisions

1. Add radar profiles to the status checker.

   The status helper will support `architecture`, `opportunity`, and `all` radar modes. Each profile owns its workflow file, title/branch PR patterns, user-facing label, schedule model, and no-work messages.

   Alternative considered: create a second `opportunity-pr-review-status.py`. That would duplicate run/PR/failure/cadence logic and make the heartbeat harder to keep consistent.

2. Keep profile-specific cadence logic.

   Architecture Radar keeps the existing 3-day anchor cadence. Opportunity Radar uses a weekly schedule: Tuesday at 05:30 UTC. Manual dispatch remains visible as the latest run, but schedule waiting applies only when the current local day is the configured weekly due day.

   Alternative considered: ignore Opportunity Radar schedule waiting. That would make the heartbeat claim "no work" during GitHub Actions schedule delay on Tuesdays.

3. Add an opportunity-specific PR summarizer.

   `summarize-radar-pr.py` remains Architecture Radar focused. A new opportunity summarizer will classify changed opportunity artifacts and summarize changed `opportunity-reports/*.md`.

   Alternative considered: overload the architecture report parser. The report schemas are different enough that a shared parser would either become brittle or produce vague field names.

4. Make the main heartbeat aggregate profile results.

   `scripts/radar-pr-review.py` will default to `--radar all`, call the status helper for both profiles, and summarize fresh PRs with the matching summarizer. A fresh PR in either profile should trigger review output. If no PR exists, failures should be reported before no-work results; waiting states should still emit `DONT_NOTIFY`.

## Risks / Trade-offs

- [Risk] Combined status output can be noisier than the old single-radar result. -> Mitigation: keep per-profile status blocks and concise markdown.
- [Risk] Opportunity report parsing may miss future section name changes. -> Mitigation: parse stable table/list sections and fall back to ledger row counts rather than failing.
- [Risk] Existing callers may expect Architecture-only behavior. -> Mitigation: keep `--radar architecture` available and keep status helper defaults compatible where practical.
