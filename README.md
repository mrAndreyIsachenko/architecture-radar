# Architecture Radar

A scheduled research agent that reviews open-source projects and extracts reusable architectural mechanisms — and, more usefully, a worked example of **how to make a recurring agent produce output you can actually trust**.

The research output lives in `reports/`, `repositories/`, and `patterns/`. The part worth copying is everything around it: the evidence taxonomy, the mechanical checks that enforce it, and the privilege boundary between the model and the repository.

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

[`scripts/validate-radar-state.py`](scripts/validate-radar-state.py) catches that class deterministically. It scans every changed artifact for lines tagged `E1 source verified`, extracts the backtick-quoted evidence paths on those lines, and classifies each path by shape. A path under `tests/` or named `*_test.go` must be `E2`. A path under `docs/` or named `README*`, `CHANGELOG*`, or an ADR must be `E3`. Mislabel one and the run fails before anything is published.

No model grades another model here. It is path classification, and it runs in CI.

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
        ├── validate artifacts        [deterministic — fails the run on inflated evidence]
        │
        └── publish pull request      [deterministic — path allowlist, token scoped here only]
```

The model occupies exactly one step. Everything before it decides whether it should run; everything after it decides whether its output is allowed out.

## Layout

| Path | Role |
|---|---|
| `interests.md` | authoritative research priorities and open problems — findings must tie to these, not to inferred needs |
| `watchlist.yml` | explicit high-signal repositories or model/dataset/runtime artifacts that discovery must account for even when broad queries miss them |
| `docs/agent-rules.md` | the machine: discovery method, candidate accounting, selection thresholds, evidence discipline, quality bar — domain-independent |
| `docs/research-scope.md` | the domain: topic families, research areas, extraction granularity — replace this to repoint the radar |
| `reports/` | dated runs with full candidate ledgers, including what was rejected and why |
| `repositories/` | source-level reviews, each pinned to a full commit SHA |
| `patterns/` | mechanisms extracted where two or more independent projects converged |
| `radar.json` | structured metadata, schema-validated in CI |
| `scripts/` | the deterministic wrapper — guards, validation, publishing |

Reviews are pinned to commit SHAs because "project X does Y" decays. "Project X at `2adda68` does Y" stays checkable.

Rejections are recorded next to selections. A ledger showing 20 triaged, 8 deeply reviewed, 8 selected says considerably more about the quality bar than a list of 8 winners.

Patterns require independent convergence. One repository doing something interesting is an observation; two arriving at the same shape separately is a mechanism worth naming.

## What is enforced, and what is only asked

Worth stating precisely, since the distinction is the whole point.

**Enforced in CI** — evidence label consistency, required workspace files, `watchlist.yml` shape, `radar.json` schema, report presence and non-emptiness, the commit path allowlist, and the absence of a GitHub token during the agent step.

**Instructed in the prompt only** — pinning SHAs, honest candidate accounting, cost discipline, selecting zero, not reading CI credentials. Nothing mechanically stops the agent from ignoring these; pull request review is the backstop.

Two known limits, stated rather than papered over:

- the evidence check keys on the literal string `E1 source verified`, so a reworded label slips past it
- `codex login` writes credentials under `$CODEX_HOME` before the agent step, so the model can in principle read its own API credential — the mitigation is an ephemeral runner holding no repository access, not enforcement

Neither is a reason to distrust the output. Both are reasons to read the pull request.

## Running it

Repository setup:

- add an `OPENAI_API_KEY` repository secret
- allow GitHub Actions to write contents and create pull requests

The model defaults to `gpt-5.4-mini` to keep recurring cost bounded. Override recurring runs with the `ARCHITECTURE_RADAR_CODEX_MODEL` repository variable, or override a single run from the Actions tab — useful when one follow-up justifies a larger model.

Manual runs bypass the cadence gate but still respect the rerun guard, so a same-day rerun does nothing unless `interests.md`, `watchlist.yml`, or the operating prompt changed. The `force_research` input overrides that deliberately and writes `reports/YYYY-MM-DD-supplement-N.md`.

## Adapting it

The research domain is the least interesting part, and it is deliberately isolated in three files. To point this at something else, replace `interests.md` with your own unresolved problems, `watchlist.yml` with things broad discovery must not miss, and `docs/research-scope.md` with your own topic areas. Leave `docs/agent-rules.md` and `scripts/` untouched — that is the machine.

The parts worth keeping intact: the evidence taxonomy and its validator, the token and path boundary in the publish script, the input-diff rerun guard, and the rule that an empty result is a legitimate one.

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
