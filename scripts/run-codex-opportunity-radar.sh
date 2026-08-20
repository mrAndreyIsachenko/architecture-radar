#!/usr/bin/env bash
set -euo pipefail

run_date="${OPPORTUNITY_RADAR_RUN_DATE:-}"
if [[ -z "$run_date" ]]; then
  run_date="$(TZ=Europe/Moscow date +%F)"
fi

prompt_file="${RUNNER_TEMP:-/tmp}/opportunity-radar-prompt-${run_date}.md"
last_message="${RUNNER_TEMP:-/tmp}/opportunity-radar-last-message-${run_date}.md"

{
  printf '# CI Run Context\n\n'
  printf 'Today is %s in Europe/Moscow.\n\n' "$run_date"
  printf 'You are running inside GitHub Actions on an ephemeral Ubuntu runner for `mrAndreyIsachenko/architecture-radar`.\n\n'
  printf 'Follow `docs/opportunity-agent-rules.md` as the operating prompt and `docs/opportunity-research-scope.md` as the domain configuration. Both are appended below, with these CI-specific constraints:\n\n'
  printf -- '- Modify repository files only. Do not create commits, push branches, edit git remotes, or open pull requests; the workflow wrapper handles publishing after you finish.\n'
  printf -- '- Write Opportunity Radar output only under `opportunity-reports/`, `opportunities/`, `signals/`, and `opportunities.json`.\n'
  printf -- '- Do not modify Architecture Radar artifacts under `reports/`, `repositories/`, `patterns/`, or `radar.json`.\n'
  printf -- '- Do not read, print, persist, or exfiltrate CI secrets, environment tokens, Codex credentials, or GitHub credentials.\n'
  printf -- '- Use public sources only. Do not contact people, send messages, scrape private/authenticated sources, or automate outreach.\n'
  printf -- '- Use live web/GitHub discovery for current public signal state.\n'
  printf -- '- Put scratch files under `/tmp/opportunity-radar-candidates`.\n'
  printf -- '- If a required prerequisite is missing, create `opportunity-reports/%s.md` as a diagnostic report and stop without synthetic opportunities.\n' "$run_date"
  printf -- '- Keep `opportunities.json` as schema_version 1 with array fields `selected`, `deferred`, and `watchlisted`; do not write a single `opportunities` object or map.\n'
  printf -- '- Include `discovery_mode`, `score`, `pain_score`, `spend_score`, `reachability_score`, `timing_score`, `buildability_score`, `confidence`, `money_signal`, `reachability`, `evidence_count`, `next_test`, `technology_shift`, `buyer`, `expensive_workflow`, `existing_spend`, `paid_experiment`, `source_classes`, `paid_wedge`, `distribution_channel`, `private_data_barrier`, `oss_commoditization_risk`, `product_shape`, `pricing_hypothesis`, and `do_not_build_until` in `opportunities.json` entries so selected, deferred, and watchlisted opportunities can be compared.\n'
  printf -- '- Also include structural fields in every `opportunities.json` entry: `structural_pattern`, `primitive_growth`, `fragmentation_summary`, `manual_workflow`, `objective_function`, `execution_ladder`, `economic_pain`, `timing_reason`, `competitors`, and `structural_scores`.\n'
  printf -- '- Also include commercial-filter fields in every `opportunities.json` entry: `fragmented_providers`, `multi_provider_user`, `boundary_workflow`, `build_vs_buy_reason`, `internal_build_likelihood`, `money_flow`, `recurrence`, `permissionless_validation`, `smallest_wedge`, and `intermediary_maturity`.\n'
  printf -- '- Compute `structural_scores.total` deterministically from integer 0-5 dimensions using weights: fragmentation 15%%, manual_pain 15%%, economic_value 20%%, objective_measurability 10%%, execution_potential 10%%, timing 10%%, competition_gap 10%%, prototype_feasibility 10%%.\n'
  printf -- '- Search explicitly for fragmentation/control-layer patterns: recent primitive or provider growth, fragmented choices, manual comparison or reconciliation, measurable objective functions, and a path from observe to recommend to choose to execute.\n'
  printf -- '- Search explicitly for cross-company glue patterns: customers using multiple independent providers, repeated boundary work, money already flowing through the providers, and a non-core buy-rather-than-build reason.\n'
  printf -- '- Account for every priority topic family listed in `opportunity-interests.md`: `ai-llm-demand`, `blockchain-demand`, `privacy-networking-demand`, `drones-robotics-demand`, and `document-ai-demand`. A family does not need a selected opportunity, but it must appear in `Topic Coverage` with reviewed signal count, best candidate or `None`, decision, and reason.\n'
  printf -- '- Treat opportunities already present in `opportunities.json.selected` as active experiments or backlog, not fresh discovery targets. Do not present an existing selected opportunity as the run main focus unless `Commercial Delta` records new commercial evidence such as a paid pilot, inbound request, procurement/RFP, direct buyer or spend evidence, or a new independent company/customer workflow. Extra GitHub issues alone are not enough.\n'
  printf -- '- Include a `## Topic Coverage` report section with a markdown table covering Family, Signals reviewed, Best candidate, Decision, and Reason.\n'
  printf -- '- Include a `## Commercial Delta` report section with a markdown table covering Opportunity, Previous stage, Current stage, Commercial delta, and Decision.\n'
  printf -- '- Include a `## Build Readiness` report section with a markdown table covering Opportunity, Paid wedge, Distribution channel, Private data barrier, OSS commoditization risk, Product shape, Pricing hypothesis, Do not build until, and Build decision.\n'
  printf -- '- Include a `## Money Readiness` report section with a markdown table covering Opportunity, Pain, Spend, Reachability, Timing, Buildability, Buyer, Existing spend, Paid experiment, Source classes, and Stage.\n'
  printf -- '- Include a `## Structural Candidate Ranking` report section with Rank, Opportunity, Ecosystem, Score, Why now, Manual workflow, and Wedge.\n'
  printf -- '- Include a `## Structural Score Breakdown` report section with Opportunity, Fragmentation, Manual pain, Economic value, Objective measurability, Execution potential, Timing, Competition gap, Prototype feasibility, and Total.\n'
  printf -- '- Include a `## Commercial Filter` report section with Opportunity, Fragmented providers, Multi-provider user, Boundary workflow, Build-vs-buy, Internal build likelihood, Money flow, Permissionless validation, Smallest wedge, and Decision.\n'
  printf -- '- Keep every `## Build Readiness` report row consistent with the matching `opportunities.json` entry by title or id; build decision and build-readiness fields must match state exactly after whitespace normalization.\n'
  printf -- '- Keep every `## Money Readiness` report row consistent with the matching `opportunities.json` entry by title or id; stage and money-readiness fields must match state exactly after whitespace normalization.\n'
  printf -- '- Keep every `## Structural Score Breakdown` report row consistent with the matching `opportunities.json` entry by title or id; `Total` must match deterministic weighted recomputation.\n'
  printf -- '- Keep every `## Commercial Filter` report row consistent with the matching `opportunities.json` entry by title or id; commercial-filter fields and decision must match state exactly after whitespace normalization.\n'
  printf -- '- Keep GitHub-only opportunities in `watchlisted`; GitHub issue evidence can prove pain but cannot by itself prove willingness to pay.\n'
  printf -- '- Keep opportunities in `watchlisted` when manual workflow, objective function, execution ladder, timing reason, or structural evidence is unclear.\n'
  printf -- '- Keep opportunities in `watchlisted` when multi-provider usage, boundary workflow, build-vs-buy reason, money flow, recurrence, permissionless validation, or smallest wedge is unclear.\n'
  printf -- '- Keep opportunities in `watchlisted` when `internal_build_likelihood` is `high`, when the smallest wedge is only a broad platform, or when validation requires hardware deployment first.\n'
  printf -- '- Do not put an opportunity under `selected` unless structural manual_pain, economic_value, objective_measurability, execution_potential, and timing are each >= 2.\n'
  printf -- '- Do not put an opportunity under `selected` unless `internal_build_likelihood` is `low` or `medium` and the buyer uses multiple providers.\n'
  printf -- '- Use `sell-before-build` when the next useful action is a paid/manual offer, audit, report, review, or sample transformation before implementation.\n'
  printf -- '- Do not mark an opportunity `selected-for-build` unless spend_score >= 3, reachability_score >= 3, timing_score >= 2, buildability_score >= 3, structural execution_potential >= 3, structural prototype_feasibility >= 3, internal_build_likelihood is `low`, paid_experiment is concrete, and at least three source classes support it.\n'
  printf -- '- If the run is anchored by `opportunity-watchlist.yml`, mark it `watchlist-directed` or `mixed` and do not describe selected opportunities as market-wide winners.\n'
  printf -- '- Prefer one focused money test for the week over multiple unrelated build artifacts.\n'
  printf -- '- Prefix important evidence bullets in every selected opportunity file with full market labels such as `M2 repeated pain:` or `M4 workaround evidence:`.\n'
  printf -- '- Ensure every Signal Ledger URL in `opportunity-reports/%s.md` appears in a date-prefixed signal note matching `signals/%s-*.md`.\n' "$run_date" "$run_date"
  printf -- '- Before your final answer, run `scripts/validate-opportunity-radar-state.py` and fix artifacts until it passes, or report the blocker explicitly.\n'
  printf -- '- The final answer should briefly summarize files changed and unresolved blockers; detailed analysis belongs in repository artifacts.\n\n'
  cat opportunity-interests.md
  printf '\n\n---\n\n'
  cat opportunity-watchlist.yml
  printf '\n\n---\n\n'
  cat docs/opportunity-research-scope.md
  printf '\n\n---\n\n'
  cat docs/opportunity-agent-rules.md
} > "$prompt_file"

codex --search --dangerously-bypass-approvals-and-sandbox exec \
  --cd "$PWD" \
  --model "${CODEX_MODEL:-gpt-5.4-mini}" \
  --ephemeral \
  --output-last-message "$last_message" \
  - < "$prompt_file"

echo "Codex final message:"
sed -n '1,160p' "$last_message"
