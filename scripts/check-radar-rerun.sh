#!/usr/bin/env bash
set -euo pipefail

run_date="${ARCHITECTURE_RADAR_RUN_DATE:-${ARCHITECTURE_RADAR_DATE:-}}"
if [[ -z "$run_date" ]]; then
  run_date="$(TZ=Europe/Moscow date +%F)"
fi

force="${ARCHITECTURE_RADAR_FORCE_RESEARCH:-false}"
report_path="reports/${run_date}.md"
report_files=("$report_path")

for supplement in "reports/${run_date}"-supplement-*.md; do
  if [[ -e "$supplement" ]]; then
    report_files+=("$supplement")
  fi
done

is_true() {
  local value
  value="$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')"

  case "$value" in
    1|true|yes|y|on) return 0 ;;
    *) return 1 ;;
  esac
}

next_supplement_path() {
  local index=1
  local candidate

  while true; do
    candidate="reports/${run_date}-supplement-${index}.md"
    if [[ ! -e "$candidate" ]]; then
      printf '%s\n' "$candidate"
      return 0
    fi
    index=$((index + 1))
  done
}

write_outputs() {
  local should_run="$1"
  local reason="$2"
  local supplement_required="${3:-false}"
  local supplement_path="${4:-}"
  local changed_scope_files="${5:-}"

  if [[ -n "${GITHUB_OUTPUT:-}" ]]; then
    {
      echo "should_run=$should_run"
      echo "reason=$reason"
      echo "supplement_required=$supplement_required"
      echo "supplement_path=$supplement_path"
      echo "changed_scope_files=$changed_scope_files"
    } >> "$GITHUB_OUTPUT"
  fi

  if [[ -n "${GITHUB_ENV:-}" ]]; then
    {
      echo "ARCHITECTURE_RADAR_REPORT_EXISTS=$([[ -f "$report_path" ]] && echo true || echo false)"
      echo "ARCHITECTURE_RADAR_SUPPLEMENT_REQUIRED=$supplement_required"
      echo "ARCHITECTURE_RADAR_SUPPLEMENT_REPORT=$supplement_path"
      echo "ARCHITECTURE_RADAR_SCOPE_CHANGED_FILES=$changed_scope_files"
      echo "ARCHITECTURE_RADAR_RERUN_REASON=$reason"
    } >> "$GITHUB_ENV"
  fi

  echo "Architecture Radar rerun guard: should_run=$should_run, reason=$reason, supplement_required=$supplement_required, supplement_path=$supplement_path"
}

if [[ ! -f "$report_path" ]]; then
  write_outputs "true" "daily report is missing"
  exit 0
fi

if is_true "$force"; then
  write_outputs "true" "manual force_research requested" "true" "$(next_supplement_path)"
  exit 0
fi

latest_report_commit="$(git log -n 1 --format=%H -- "${report_files[@]}" 2>/dev/null || true)"
if [[ -z "$latest_report_commit" ]]; then
  write_outputs "true" "daily report exists but has no committed history" "true" "$(next_supplement_path)"
  exit 0
fi

changed_scope_files="$(
  git diff --name-only "${latest_report_commit}..HEAD" -- interests.md docs/agent-rules.md docs/research-scope.md watchlist.yml \
    | paste -sd ',' -
)"

if [[ -n "$changed_scope_files" ]]; then
  write_outputs "true" "research scope changed after existing daily report" "true" "$(next_supplement_path)" "$changed_scope_files"
  exit 0
fi

write_outputs "false" "daily report already exists and research scope is unchanged"
