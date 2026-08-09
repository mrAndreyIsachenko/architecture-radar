# Proposal: Add Weekly Synthesis

## Problem

Architecture Radar and Opportunity Radar now produce useful daily or manual pull requests, but they do not yet provide a periodic synthesis layer. Reviewing individual PRs answers what changed in one run; it does not answer which patterns are strengthening, which topic families remain empty, which candidates recur, or which next experiment deserves focus.

Without a synthesis workflow, the repository can accumulate evidence while still leaving the user to manually reconstruct the bigger picture from reports, repository reviews, pattern files, opportunity files, and JSON state.

## Goals

- Add a separate weekly synthesis workflow that reads accumulated repository artifacts.
- Write synthesis reports under `weekly-reports/`.
- Keep weekly synthesis separate from daily Architecture Radar output and Opportunity Radar output.
- Avoid live discovery and new candidate selection in the weekly pass.
- Produce one focused next-week recommendation instead of multiple scattered build ideas.
- Validate weekly synthesis reports in CI.

## Non-Goals

- Do not replace daily Architecture Radar runs.
- Do not make Opportunity Radar scheduled.
- Do not auto-merge synthesis PRs.
- Do not use weekly synthesis to add new repository reviews, pattern files, opportunities, signals, or radar state entries.
- Do not contact people or use private/authenticated demand sources.

## Expected Impact

The workflow adds a lower-cost review layer over already-generated artifacts. It should help decide what to inspect next, what to stop reading about temporarily, and which experiment has the clearest evidence chain.
