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
  printf 'Run guard state:\n\n'
  printf -- '- Existing daily report: `%s`.\n' "${ARCHITECTURE_RADAR_REPORT_EXISTS:-unknown}"
  printf -- '- Supplement required: `%s`.\n' "${ARCHITECTURE_RADAR_SUPPLEMENT_REQUIRED:-false}"
  printf -- '- Supplement report path: `%s`.\n' "${ARCHITECTURE_RADAR_SUPPLEMENT_REPORT:-}"
  printf -- '- Rerun reason: `%s`.\n' "${ARCHITECTURE_RADAR_RERUN_REASON:-not provided}"
  printf -- '- Scope files changed after existing report: `%s`.\n\n' "${ARCHITECTURE_RADAR_SCOPE_CHANGED_FILES:-}"
  printf 'Follow `docs/agent-rules.md` as the authoritative operating prompt and `docs/research-scope.md` as the domain configuration. Both are appended below, with these CI-specific constraints:\n\n'
  printf -- '- Modify repository files only. Do not create commits, push branches, edit git remotes, or open pull requests; the workflow wrapper handles publishing after you finish.\n'
  printf -- '- Do not read, print, persist, or exfiltrate CI secrets, environment tokens, Codex credentials, or GitHub credentials.\n'
  printf -- '- Put temporary external repository clones and scratch files under `/tmp/architecture-radar-candidates`.\n'
  printf -- '- Use live web/GitHub discovery for current repository state.\n'
  printf -- '- For company, product, launch, or runtime watchlist entries, perform company-to-repository expansion before deciding there is no inspectable source. Launch/company pages are discovery evidence only, not source-verified architecture evidence.\n'
  printf -- '- If a required prerequisite is missing, create `reports/%s.md` as a diagnostic report and stop without synthetic reviews, patterns, or radar entries.\n' "$run_date"
  printf -- '- If `Supplement required` is `true`, do not stop merely because `reports/%s.md` already exists. Create the supplement report at the provided supplement path and focus on changed or under-covered topic families.\n' "$run_date"
  printf -- '- The final answer should briefly summarize files changed and unresolved blockers; detailed analysis belongs in repository artifacts.\n\n'
  cat docs/research-scope.md
  printf '\n\n---\n\n'
  cat docs/agent-rules.md
} > "$prompt_file"

codex --search --dangerously-bypass-approvals-and-sandbox exec \
  --cd "$PWD" \
  --model "${CODEX_MODEL:-gpt-5.5}" \
  --ephemeral \
  --output-last-message "$last_message" \
  - < "$prompt_file"

echo "Codex final message:"
sed -n '1,160p' "$last_message"
