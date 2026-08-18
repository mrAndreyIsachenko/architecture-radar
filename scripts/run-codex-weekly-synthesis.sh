#!/usr/bin/env bash
set -euo pipefail

run_date="${WEEKLY_SYNTHESIS_RUN_DATE:-}"
if [[ -z "$run_date" ]]; then
  run_date="$(TZ=Europe/Moscow date +%F)"
fi

week_id="${WEEKLY_SYNTHESIS_WEEK_ID:-}"
if [[ -z "$week_id" ]]; then
  week_id="$(python3 - "$run_date" <<'PY'
from datetime import date
import sys

run_date = date.fromisoformat(sys.argv[1])
iso_year, iso_week, _ = run_date.isocalendar()
print(f"{iso_year}-W{iso_week:02d}")
PY
)"
fi

prompt_file="${RUNNER_TEMP:-/tmp}/weekly-synthesis-prompt-${week_id}.md"
last_message="${RUNNER_TEMP:-/tmp}/weekly-synthesis-last-message-${week_id}.md"

{
  printf '# CI Run Context\n\n'
  printf 'Today is %s in Europe/Moscow.\n' "$run_date"
  printf 'The ISO week id is %s.\n\n' "$week_id"
  printf 'You are running inside GitHub Actions on an ephemeral Ubuntu runner for `mrAndreyIsachenko/architecture-radar`.\n\n'
  printf 'You are a weekly synthesis agent. Your job is to synthesize already committed Architecture Radar and Opportunity Radar artifacts.\n\n'
  printf 'Constraints:\n\n'
  printf -- '- Modify repository files only.\n'
  printf -- '- Write only `weekly-reports/%s.md`.\n' "$week_id"
  printf -- '- Do not modify `reports/`, `repositories/`, `patterns/`, `radar.json`, `opportunity-reports/`, `opportunities/`, `signals/`, or `opportunities.json`.\n'
  printf -- '- Do not create commits, push branches, edit git remotes, or open pull requests; the workflow wrapper handles publishing.\n'
  printf -- '- Do not perform live web search, GitHub search, external repository cloning, or new candidate discovery.\n'
  printf -- '- Do not read, print, persist, or exfiltrate CI secrets, environment tokens, Codex credentials, or GitHub credentials.\n'
  printf -- '- If there are not enough committed artifacts to synthesize, still create `weekly-reports/%s.md` as a diagnostic report explaining the missing inputs.\n' "$week_id"
  printf -- '- Before your final answer, run `scripts/validate-weekly-synthesis-state.py` and fix the report until it passes, or report the blocker explicitly.\n\n'
  printf 'Required output sections for `weekly-reports/%s.md`:\n\n' "$week_id"
  printf -- '- `## Week And Scope`\n'
  printf -- '- `## Input Reports`\n'
  printf -- '- `## Executive Synthesis`\n'
  printf -- '- `## Pattern Movement`\n'
  printf -- '- `## Topic Coverage`\n'
  printf -- '- `## Repeated Candidates Or Signals`\n'
  printf -- '- `## Decisions And Experiments`\n'
  printf -- '- `## Evidence Gaps`\n'
  printf -- '- `## Next Week Focus`\n\n'
  printf 'Read and synthesize these local files when present:\n\n'
  printf -- '- `interests.md`\n'
  printf -- '- `docs/research-scope.md`\n'
  printf -- '- `radar.json`\n'
  printf -- '- `reports/*.md`\n'
  printf -- '- `repositories/*.md`\n'
  printf -- '- `patterns/*.md`\n'
  printf -- '- `opportunity-interests.md`\n'
  printf -- '- `opportunity-reports/*.md`\n'
  printf -- '- `opportunities/*.md`\n'
  printf -- '- `opportunities.json`\n\n'
  printf 'Opportunity state rules:\n\n'
  printf -- '- Treat `opportunities.json.selected` as the only source of active Opportunity Radar experiments.\n'
  printf -- '- Do not recommend building, running, selling, or testing an opportunity from `opportunities.json.watchlisted` or `opportunities.json.deferred` as an active next-week experiment.\n'
  printf -- '- If `opportunities.json.selected` is empty, `## Decisions And Experiments` and `## Next Week Focus` must not contain an active Opportunity Radar build/run/sell/test recommendation.\n'
  printf -- '- Watchlisted and deferred opportunities may be mentioned only as blocked, deferred, watchlisted, or requiring the named `do_not_build_until` validation before build work.\n\n'
  printf 'Path and link rules:\n\n'
  printf -- '- When referencing repository artifacts, use repository-relative paths such as `repositories/example.md` or Markdown links whose target is `repositories/example.md`.\n'
  printf -- '- Do not emit absolute local, runner, or workspace paths such as `/home/runner/...`, `/workspace/...`, `/Users/...`, or `/tmp/...`.\n'
  printf -- '- Do not use the GitHub Actions checkout path in Markdown link targets.\n\n'
  printf 'Quality bar:\n\n'
  printf -- '- Distinguish facts from prior artifacts from your interpretation.\n'
  printf -- '- Identify which patterns gained support, which topic families are thin, and which repeated candidates or signals should be suppressed or revisited.\n'
  printf -- '- Recommend exactly one next-week focus unless the evidence says no action should be taken.\n'
  printf -- '- Tie the recommendation to existing report, pattern, repository, or opportunity file paths.\n'
  printf -- '- Keep the report concise; do not restate full daily reports.\n\n'
} > "$prompt_file"

codex --dangerously-bypass-approvals-and-sandbox exec \
  --cd "$PWD" \
  --model "${CODEX_MODEL:-gpt-5.4-mini}" \
  --ephemeral \
  --output-last-message "$last_message" \
  - < "$prompt_file"

echo "Codex final message:"
sed -n '1,160p' "$last_message"
