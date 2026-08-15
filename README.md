# Architecture Radar

[![Architecture Radar](https://github.com/mrAndreyIsachenko/architecture-radar/actions/workflows/architecture-radar.yml/badge.svg)](https://github.com/mrAndreyIsachenko/architecture-radar/actions/workflows/architecture-radar.yml)
[![Radar Validation](https://github.com/mrAndreyIsachenko/architecture-radar/actions/workflows/radar-validation.yml/badge.svg)](https://github.com/mrAndreyIsachenko/architecture-radar/actions/workflows/radar-validation.yml)
[![License](https://img.shields.io/github/license/mrAndreyIsachenko/architecture-radar)](LICENSE)

A reference implementation for running a scheduled AI research agent that produces **evidence-backed pull requests** instead of disposable digests.

Use it to build a radar for open-source architecture, market signals, security research, model releases, protocol ecosystems, or any recurring investigation where plausible-but-unsupported output is worse than no output.

The core idea: let the model research and write, but let deterministic GitHub Actions decide whether the result is structurally valid, evidence-labeled, reviewable, and safe to publish.

The current radar reviews open-source repositories related to AI/LLM systems, document AI/OCR, blockchain intelligence, VPN/privacy networking, and drones/autonomy. The reusable part is not the topic list. It is the operating system around the research agent.

The repository also includes a separate **Opportunity Radar** mode for money-first, evidence-backed demand research. It writes to `opportunity-reports/`, `opportunities/`, `signals/`, and `opportunities.json`, not to the architecture-review artifacts.

## Quick Start

See [`QUICKSTART.md`](QUICKSTART.md) for the shortest path from fork to first scheduled PR.

At a high level:

1. Fork or clone this repository.
2. Run `python3 scripts/check-radar-setup.py --skip-github` to verify the local checkout.
3. Add an `OPENAI_API_KEY` repository secret.
4. Allow GitHub Actions to write contents and create pull requests.
5. Run `python3 scripts/check-radar-setup.py` with `gh` authenticated to verify the remote setup.
6. Replace `interests.md`, `docs/research-scope.md`, and `watchlist.yml` with your own research scope.
7. Run the `Architecture Radar` workflow manually.
8. Review the generated PR before merging.

## What You Can Copy

- A GitHub Actions wrapper for scheduled AI research that opens pull requests instead of writing to `main`.
- An evidence taxonomy that separates source-verified facts, test-verified behavior, maintainer claims, interpretation, and hypotheses.
- Deterministic validation that catches common evidence-label inflation before a PR is published.
- A privilege boundary where the model gets API credentials but no GitHub token, while publishing happens in a separate allowlisted step.
- Cadence and rerun guards that avoid spending tokens when the research inputs have not changed.
- Local PR-review helpers for turning a generated radar PR into a short review notification.
- Example scopes under [`examples/`](examples/) showing how to reuse the same workflow for other research domains.
- A weekly scheduled Opportunity Radar workflow for testing demand and first-money paths without mixing it into Architecture Radar state, with manual dispatch for event-driven checks.

## Example Output

Real generated pull requests from this repository:

| Mode | Pull request | Generated artifacts |
|---|---|---|
| Architecture Radar | [PR #9, Architecture Radar 2026-08-08](https://github.com/mrAndreyIsachenko/architecture-radar/pull/9) | [`reports/2026-08-08.md`](reports/2026-08-08.md), [`reports/2026-08-08-supplement-1.md`](reports/2026-08-08-supplement-1.md), [Reorg-Safe Materialization Windows](patterns/reorg-safe-materialization-windows.md), and [Deferred Image Materialization](patterns/deferred-image-materialization.md) |
| Opportunity Radar | [PR #27, Opportunity Radar 2026-08-09](https://github.com/mrAndreyIsachenko/architecture-radar/pull/27) | [`opportunity-reports/2026-08-09.md`](opportunity-reports/2026-08-09.md), three opportunity records under [`opportunities/`](opportunities/), and normalized signal notes under [`signals/`](signals/) |
| Weekly Synthesis | [PR #32, Weekly Synthesis 2026-W32](https://github.com/mrAndreyIsachenko/architecture-radar/pull/32) | [`weekly-reports/2026-W32.md`](weekly-reports/2026-W32.md), combining committed Architecture Radar and Opportunity Radar evidence without fresh discovery |

The useful part is the review shape, not the specific topics: selected candidates or opportunities, rejected candidates, evidence gaps, pattern updates, and one concrete next action all arrive in a PR that CI can reject.

## The problem this is built against

A research agent on a schedule fails in a specific way. It rarely crashes. It returns something plausible.

Left alone, it will:

- call a claim from a project's README "source verified"
- select a repository because it needs to select something
- restate last week's findings so the diff looks like progress
- spend tokens on days when nothing has changed

None of these produce an error. All of them produce a report that reads fine and is worth nothing. Each mechanism below exists to make one of them fail loudly instead.

## Four mechanisms

### 1. An evidence taxonomy, mechanically enforced

Every significant claim carries a label stating how it was established:

| Label | Meaning |
|---|---|
| `E1 source verified` | confirmed in implementation code at the reviewed commit |
| `E2 test verified` | confirmed by a test expressing the behavior |
| `E3 maintainer stated` | claimed in docs, ADR, issue, release note, or maintainer comment |
| `I interpretation` | architectural reading derived from evidence |
| `H hypothesis` | plausible, not sufficiently verified |

Facts, claims, interpretations, and guesses stay in separate categories instead of collapsing into one confident voice.

The predictable failure is label inflation — the model reads a README, and `E1` makes a better-sounding report than `E3`.

[`scripts/normalize-radar-evidence-labels.py`](scripts/normalize-radar-evidence-labels.py) fixes the unambiguous cases deterministically before validation. If the model writes `E1 source verified` for a test path, the line becomes `E2 test verified`; if it writes `E1` for `README*`, `docs/`, `CHANGELOG*`, release, ADR, or `spec/` evidence, the line becomes `E3 maintainer stated`.

[`scripts/validate-radar-state.py`](scripts/validate-radar-state.py) remains the hard gate. It scans every changed artifact for remaining lines tagged `E1 source verified`, extracts the backtick-quoted evidence paths on those lines, and classifies each path by shape. Ambiguous mixed-evidence lines still fail before anything is published.

No model grades another model here. It is path classification, and it runs in CI.

The scheduled research workflow validates artifacts before it can publish a PR. The separate `Radar Validation` workflow runs the same deterministic checks on pull requests without Codex, OpenAI credentials, or repository write permissions.

### 2. The agent cannot publish

The research step runs with `--dangerously-bypass-approvals-and-sandbox`, so it has full reign over the runner filesystem. It has no route to the repository.

Three independent boundaries:

- checkout uses `persist-credentials: false`, leaving no git credentials in the working tree
- the agent step receives **no** `GH_TOKEN` — only the later publish step gets one
- [`scripts/publish-radar-run.sh`](scripts/publish-radar-run.sh) stages an explicit allowlist:

  ```
  git add README.md interests.md radar.json reports repositories patterns
  ```

That last line is the one that matters. Note what is absent from it: `scripts/`, `.github/`, and `docs/`. Even with full local write access, the agent cannot get a change to the wrapper, the workflow, or **its own operating rules** into a commit — those writes are silently dropped. The blast radius is bounded by what the deterministic wrapper is willing to stage, not by what the agent was told not to touch.

Everything produced arrives as a pull request. Nothing reaches `main` unreviewed.

### 3. Re-run on scope change, not on a timer

Two guards decide whether to spend tokens at all, both before the expensive step.

[`check-radar-cadence.sh`](scripts/check-radar-cadence.sh) — the workflow wakes daily, but research fires every third day, computed against a fixed anchor date. A daily cron with a cheap gate is easier to reason about than a cron expression encoding the real cadence.

[`check-radar-rerun.sh`](scripts/check-radar-rerun.sh) — the more interesting one. When today's report already exists, it finds the commit that last touched it and diffs `interests.md`, `watchlist.yml`, `docs/agent-rules.md`, and `docs/research-scope.md` from that commit to `HEAD`:

- nothing changed → skip, spend nothing
- priorities or the operating prompt changed → run a **supplement**, scoped to the families the change affected

The agent's output is treated as a cached artifact keyed on its own inputs. Change the question or change the instructions and the cache invalidates. Change neither, and re-running only pays to reword yesterday.

### 4. Selecting nothing is a valid outcome

From the operating prompt: *select zero repositories when no candidate clears the quality bar.*

This is the hardest rule to hold, because it cuts against everything a model is inclined to do. An empty run looks like failure, so the default behavior is to promote the best of a weak field and describe it in language implying it was strong.

The rule is stated in [`docs/agent-rules.md`](docs/agent-rules.md) and backed by the fact that a padded selection still has to survive the evidence check — inflating a weak candidate means labeling documentation as source-verified, which fails the build.

Every recommendation must close this chain or it does not ship:

```
problem in interests.md → observed mechanism → source evidence → proposed experiment
```

## How a run works

```
 cron (daily, 05:00 UTC)
        │
        ├── cadence gate ──────────── not a cadence day ─────────────► stop (free)
        │
        ├── rerun guard ───────────── report exists, scope unchanged ─► stop (free)
        │                             scope changed ──► supplement mode
        │
        ├── prepare dated branch      [deterministic]
        │
        ├── research agent            [model — no GH token, unsandboxed]
        │      reads  interests.md + watchlist.yml
        │             docs/agent-rules.md + docs/research-scope.md
        │      writes reports/ repositories/ patterns/ radar.json
        │
        ├── normalize evidence labels [deterministic — downgrades unambiguous E1 over-labeling]
        │
        ├── validate artifacts        [deterministic — fails the run on remaining inflated evidence]
        │
        └── publish pull request      [deterministic — path allowlist, token scoped here only]
```

The model occupies exactly one step. Everything before it decides whether it should run; everything after it decides whether its output is allowed out.

Generated PRs have one extra validation detail: GitHub does not automatically run `pull_request` workflows for pull requests created by a workflow with `GITHUB_TOKEN`. After a generated workflow succeeds, `Generated PR Validation` marks the generated PR head with the required `validate` check that corresponds to the deterministic validation already run before publishing.

## Layout

| Path | Role |
|---|---|
| `.codex/skills/` | OpenSpec-generated Codex skills for explore/propose/apply/archive workflows |
| `QUICKSTART.md` | fork-to-first-PR setup guide |
| `interests.md` | authoritative research priorities and open problems — findings must tie to these, not to inferred needs |
| `opportunity-interests.md` | authoritative priorities for Opportunity Radar demand research |
| `watchlist.yml` | explicit high-signal repositories or model/dataset/runtime artifacts that discovery must account for even when broad queries miss them |
| `opportunity-watchlist.yml` | public demand-signal sources Opportunity Radar should account for |
| `docs/agent-rules.md` | the machine: discovery method, candidate accounting, selection thresholds, evidence discipline, quality bar — domain-independent |
| `docs/research-scope.md` | the domain: topic families, research areas, extraction granularity — replace this to repoint the radar |
| `docs/opportunity-agent-rules.md` | operating rules for market-signal and demand research |
| `docs/opportunity-research-scope.md` | topic families, signal types, and evidence labels for Opportunity Radar |
| `docs/publication-checklist.md` | public-release hygiene: license, metadata, topics, branch protection, demo quality |
| `docs/release-checklist.md` | release readiness checks for public releases |
| `docs/releases/` | release-note drafts |
| `examples/` | reusable domain templates, including opportunity and demand research |
| `openspec/` | specs and proposed changes for non-trivial behavior changes |
| `opportunity-reports/` | dated Opportunity Radar runs with signal ledgers |
| `opportunities/` | selected opportunity records ending in testable offers |
| `reports/` | dated runs with full candidate ledgers, including what was rejected and why |
| `repositories/` | source-level reviews, each pinned to a full commit SHA |
| `patterns/` | mechanisms extracted where two or more independent projects converged |
| `signals/` | normalized public signal notes worth revisiting |
| `weekly-reports/` | weekly synthesis across accumulated Architecture Radar and Opportunity Radar artifacts |
| `opportunities.json` | structured Opportunity Radar state |
| `radar.json` | structured metadata, schema-validated in CI |
| `scripts/` | the deterministic wrapper — guards, validation, publishing |

Reviews are pinned to commit SHAs because "project X does Y" decays. "Project X at `2adda68` does Y" stays checkable.

Rejections are recorded next to selections. A ledger showing 20 triaged, 8 deeply reviewed, 8 selected says considerably more about the quality bar than a list of 8 winners.

Patterns require independent convergence. One repository doing something interesting is an observation; two arriving at the same shape separately is a mechanism worth naming.

## What is enforced, and what is only asked

Worth stating precisely, since the distinction is the whole point.

**Enforced in CI** — evidence label consistency, required workspace files, `watchlist.yml` shape, `radar.json` schema, report presence and required sections, candidate-ledger table shape, script syntax, PR-review helper unit tests, changed-file whitespace, the commit path allowlist, generated PR validation markers, and the absence of a GitHub token during the agent step.

**Instructed in the prompt only** — pinning SHAs, honest candidate accounting, cost discipline, selecting zero, not reading CI credentials. Nothing mechanically stops the agent from ignoring these; pull request review is the backstop.

Two known limits, stated rather than papered over:

- the evidence check keys on the literal string `E1 source verified`, so a reworded label slips past it
- `codex login` writes credentials under `$CODEX_HOME` before the agent step, so the model can in principle read its own API credential — the mitigation is an ephemeral runner holding no repository access, not enforcement

Neither is a reason to distrust the output. Both are reasons to read the pull request.

## Running it

Repository setup:

- add an `OPENAI_API_KEY` repository secret
- allow GitHub Actions to write contents and create pull requests

Before spending tokens on a workflow run, check the setup locally:

```bash
python3 scripts/check-radar-setup.py --skip-github
```

Then authenticate `gh` and check the GitHub-side configuration:

```bash
python3 scripts/check-radar-setup.py
```

The model defaults to `gpt-5.4-mini` to keep recurring cost bounded. Override recurring runs with the `ARCHITECTURE_RADAR_CODEX_MODEL` repository variable, or override a single run from the Actions tab — useful when one follow-up justifies a larger model.

Manual runs bypass the cadence gate but still respect the rerun guard, so a same-day rerun does nothing unless `interests.md`, `watchlist.yml`, or the operating prompt changed. The `force_research` input overrides that deliberately and writes `reports/YYYY-MM-DD-supplement-N.md`.

Opportunity Radar runs weekly on Tuesday at 05:30 UTC, which is 08:30 Europe/Moscow. It now uses money-first selection: GitHub-only pain stays watchlisted, `sell-before-build` is a valid outcome, and build recommendations require spend, reachability, timing, buildability, source-class diversity, and a concrete paid experiment. Run it manually from `Actions -> Opportunity Radar -> Run workflow` after notable demand signals or when validating a specific opportunity hypothesis.

Weekly Synthesis runs separately from discovery. It reads committed radar artifacts and writes `weekly-reports/YYYY-Www.md` with pattern movement, topic coverage, repeated candidates or signals, evidence gaps, and one next-week focus. Run it from `Actions -> Weekly Synthesis -> Run workflow`, or let the weekly schedule open a synthesis PR.

## Reviewing PRs

The local PR-review heartbeat should use the repository helper before deciding whether to notify:

```bash
python3 scripts/radar-pr-review.py --format markdown --include-failed-log
```

By default it checks both `Architecture Radar YYYY-MM-DD` and `Opportunity Radar YYYY-MM-DD` pull requests before reporting no work. It mirrors the Architecture Radar 3-day cadence, waits through the Opportunity Radar Tuesday schedule delay, includes failed-run excerpts, summarizes fresh PRs from GitHub metadata plus changed report files, and emits a `looks_mergeable` or `needs_manual_review` recommendation. Use `--radar architecture` or `--radar opportunity` to limit the check.

Lower-level helpers are still available when needed. After checking out a radar PR branch, summarize the generated report without hand-parsing Markdown:

```bash
python3 scripts/summarize-radar-report.py reports/YYYY-MM-DD.md --format markdown
```

Or summarize an open radar PR directly from GitHub metadata and changed report files:

```bash
python3 scripts/summarize-radar-pr.py PR_NUMBER --format markdown
```

For an Opportunity Radar PR:

```bash
python3 scripts/summarize-opportunity-pr.py PR_NUMBER --format markdown
```

Weekly synthesis PRs are intentionally small: review the single report under `weekly-reports/` and check whether the next-week focus follows from existing evidence rather than fresh discovery.

## Planning Changes

Non-trivial behavior changes use OpenSpec before implementation. This applies to workflow behavior, validators, evidence taxonomies, artifact schemas, publishing boundaries, new radar modes, and recurring automation semantics.

Generated radar artifacts do not need OpenSpec changes.

OpenSpec's Codex integration lives under `.codex/skills/`. Restart Codex after pulling changes that add or update those skills.

```bash
openspec validate --all --strict --no-interactive
```

## Adapting it

The research domain is the least interesting part, and it is deliberately isolated in three files. To point this at something else, replace `interests.md` with your own unresolved problems, `watchlist.yml` with things broad discovery must not miss, and `docs/research-scope.md` with your own topic areas. Leave `docs/agent-rules.md` and `scripts/` untouched — that is the machine.

The parts worth keeping intact: the evidence taxonomy and its validator, the token and path boundary in the publish script, the input-diff rerun guard, and the rule that an empty result is a legitimate one.

For a concrete non-architecture adaptation, see [`examples/opportunity-demand-radar/`](examples/opportunity-demand-radar/). For public-release hygiene, see [`docs/publication-checklist.md`](docs/publication-checklist.md).

## Current themes

Mechanisms extracted so far, each backed by two or more independent implementations:

- **[Evidence-carrying execution envelopes](patterns/evidence-carrying-execution-envelopes.md)** — checkpoint, lineage-event, and source-episode envelopes preserving producer and schema identity, parent-child causality, recovery state, and links from derived claims back to source evidence.
- **[Reorg-safe materialization windows](patterns/reorg-safe-materialization-windows.md)** — provisional/finalized block splits with explicit rollback and catchup paths, keeping blockchain indexes recoverable after chain reorganizations.
- **[Deferred image materialization](patterns/deferred-image-materialization.md)** — lowres-first document parsing that promotes expensive page images or crops only after structural decisions prove they are needed.

## Operating principles

- Treat `interests.md` as authoritative.
- Prefer verified source evidence over README summaries.
- Pin every repository review to a full commit SHA.
- Select zero repositories when no candidate clears the quality bar.
- Extract narrow reusable mechanisms, not product recommendations.
- Update this README only when the cumulative radar materially changes.

## License

MIT. See [`LICENSE`](LICENSE).
