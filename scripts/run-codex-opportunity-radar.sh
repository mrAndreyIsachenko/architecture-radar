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
