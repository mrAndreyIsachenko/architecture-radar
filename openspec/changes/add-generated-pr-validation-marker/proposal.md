# Proposal: Add Generated PR Validation Marker

## Problem

Radar workflows publish pull requests with the repository `GITHUB_TOKEN`. GitHub does not run the normal `pull_request` validation workflow for pull requests created this way, so branch protection can remain blocked even when the generating workflow already ran deterministic validation before publishing.

The first Weekly Synthesis pull request showed this failure mode: the report was generated, validated, published, and then manually unblocked with an empty commit so the required `validate` check would attach.

## Goals

- Add a deterministic follow-up workflow for generated radar PRs.
- After a successful generator workflow, find the generated PR by branch prefix and source workflow run number.
- Create a GitHub Actions check-run named `validate` on the PR head SHA.
- Avoid changing generated artifacts just to trigger validation.
- Keep normal human-authored pull requests on the existing `pull_request` validation workflow.

## Non-Goals

- Do not weaken branch protection.
- Do not remove the existing `Radar Validation` workflow.
- Do not auto-merge generated PRs.
- Do not mark failed generator runs as validated.
- Do not validate arbitrary external contributor branches.

## Expected Impact

Generated Architecture Radar, Opportunity Radar, and Weekly Synthesis PRs should become mergeable after their source workflow succeeds, without requiring a manual empty commit.
