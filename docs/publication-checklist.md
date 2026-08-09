# Publication Checklist

Use this checklist before actively promoting a public fork of Architecture Radar.

The goal is to make the repository understandable, reusable, and safe to run by someone who does not know the original project context.

## Required Before Promotion

- Confirm the repository has a license matching the intended reuse model. This repository uses the MIT License.
- Set a concise repository description in GitHub settings.
- Add GitHub topics that match the reusable mechanics, not only the current research domain.
- Keep `README.md` understandable in the first screen: what it is, why it exists, what can be copied, and where to start.
- Keep `QUICKSTART.md` current with the actual workflow inputs, required secrets, default model, and branch protection recommendations.
- Run the `validate` check on the default branch.
- Confirm `main` branch protection requires the `validate` status check.
- Confirm generated radar PRs are not auto-merged.

## Suggested GitHub Metadata

Repository description:

```text
Evidence-backed scheduled research agent that turns recurring AI research into validated GitHub pull requests.
```

Suggested topics:

- `ai-agents`
- `llm`
- `research-agent`
- `github-actions`
- `open-source-intelligence`
- `evidence`
- `provenance`
- `knowledge-graph`
- `architecture`
- `automation`
- `codex`

Add domain topics only when they are central to the public fork. For this repository, candidates include:

- `blockchain`
- `ocr`
- `document-ai`
- `vpn`
- `drones`
- `robotics`

## Trust Claims To Avoid

Do not claim that the radar:

- proves that generated research is correct;
- eliminates the need for human review;
- prevents all prompt or evidence mistakes;
- provides investment, security, legal, or safety advice;
- safely handles private data by default.

The stronger and more accurate claim is:

```text
The repository turns model-generated research into reviewable pull requests with deterministic structural and evidence-label checks.
```

## What Makes The Project Interesting Externally

- It treats recurring model output as a pull request, not as a notification.
- It separates model work from publishing authority.
- It validates evidence labels with deterministic code.
- It records rejected candidates, not only selected winners.
- It treats "no useful finding" as a valid outcome.
- It includes cadence and rerun guards to control recurring cost.

## Public Demo Criteria

Before sharing a run as an example, verify that it includes:

- a dated report in `reports/`;
- candidate counts and a candidate ledger;
- selected repositories or an explicit zero-selection decision;
- evidence labels attached to important claims;
- repository reviews pinned to commit SHAs when deep reviews exist;
- pattern updates only when there is enough convergence or relevance;
- a clear rejection reason for notable candidates;
- one concrete next action.

## Cost And Privacy Notes

Public users should understand that recurring research agents can spend tokens quickly when they read source code. Keep model defaults conservative, document how to override the model per run, and explain when the rerun guard skips work.

Do not publish private project context in `interests.md` unless the repository and OpenAI project are configured for that data.

## Organic Interest Loop

After the basics are in place:

1. Publish one high-quality example PR and link to it from the README.
2. Add one small example scope under `examples/` for a different use case.
3. Share a short post focused on the mechanism, not the topic: "scheduled research agents should open validated PRs."
4. Watch GitHub traffic, stars, forks, issues, and inbound clones separately. Clone spikes without views often mean CI or bot traffic, not real adoption.
5. Improve the first-run experience before adding more features.
