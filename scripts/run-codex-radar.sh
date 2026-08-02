#!/usr/bin/env bash
set -euo pipefail

run_date="${ARCHITECTURE_RADAR_RUN_DATE:-}"
if [[ -z "$run_date" ]]; then
  run_date="$(TZ=Europe/Moscow date +%F)"
fi

prompt_file="${RUNNER_TEMP:-/tmp}/architecture-radar-prompt-${run_date}.md"
last_message="${RUNNER_TEMP:-/tmp}/architecture-radar-last-message-${run_date}.md"

{
  printf '# CI Run Context\n\n'
  printf 'Today is %s in Europe/Moscow.\n\n' "$run_date"
  printf 'You are running inside GitHub Actions on an ephemeral Ubuntu runner for `mrAndreyIsachenko/architecture-radar`.\n\n'
  printf 'Follow `docs/architecture-radar-agent.md` as the authoritative operating prompt, with these CI-specific constraints:\n\n'
  printf -- '- Modify repository files only. Do not create commits, push branches, edit git remotes, or open pull requests; the workflow wrapper handles publishing after you finish.\n'
  printf -- '- Do not read, print, persist, or exfiltrate CI secrets, environment tokens, Codex credentials, or GitHub credentials.\n'
  printf -- '- Put temporary external repository clones and scratch files under `/tmp/architecture-radar-candidates`.\n'
  printf -- '- Use live web/GitHub discovery for current repository state.\n'
  printf -- '- If a required prerequisite is missing, create `reports/%s.md` as a diagnostic report and stop without synthetic reviews, patterns, or radar entries.\n' "$run_date"
  printf -- '- The final answer should briefly summarize files changed and unresolved blockers; detailed analysis belongs in repository artifacts.\n\n'
  cat docs/architecture-radar-agent.md
} > "$prompt_file"

codex --search --ask-for-approval never exec \
  --cd "$PWD" \
  --model "${CODEX_MODEL:-gpt-5.5}" \
  --sandbox workspace-write \
  --ephemeral \
  --output-last-message "$last_message" \
  - < "$prompt_file"

echo "Codex final message:"
sed -n '1,160p' "$last_message"
