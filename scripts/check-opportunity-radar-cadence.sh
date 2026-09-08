#!/usr/bin/env bash
set -euo pipefail

event_name="${GITHUB_EVENT_NAME:-local}"
manual_date="${OPPORTUNITY_RADAR_DATE:-}"
timezone="${OPPORTUNITY_RADAR_TIMEZONE:-Europe/Moscow}"
catchup_days="${OPPORTUNITY_RADAR_CATCHUP_DAYS:-2}"
due_weekday="${OPPORTUNITY_RADAR_DUE_WEEKDAY:-2}"

date_state="$(
  python3 - "$manual_date" "$timezone" "$catchup_days" "$due_weekday" <<'PY'
from __future__ import annotations

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
import os
import sys

manual_date, timezone, catchup_days_raw, due_weekday_raw = sys.argv[1:5]

try:
    catchup_days = int(catchup_days_raw)
except ValueError as exc:
    raise SystemExit(f"OPPORTUNITY_RADAR_CATCHUP_DAYS must be an integer, got: {catchup_days_raw}") from exc

if catchup_days < 0:
    raise SystemExit(f"OPPORTUNITY_RADAR_CATCHUP_DAYS must be non-negative, got: {catchup_days}")

try:
    due_weekday = int(due_weekday_raw)
except ValueError as exc:
    raise SystemExit(f"OPPORTUNITY_RADAR_DUE_WEEKDAY must be an integer, got: {due_weekday_raw}") from exc

if due_weekday < 1 or due_weekday > 7:
    raise SystemExit(f"OPPORTUNITY_RADAR_DUE_WEEKDAY must be an ISO weekday from 1 to 7, got: {due_weekday}")

if manual_date:
    try:
        run_date = date.fromisoformat(manual_date)
    except ValueError as exc:
        raise SystemExit(f"OPPORTUNITY_RADAR_DATE must be YYYY-MM-DD, got: {manual_date}") from exc
    today = run_date
    target = run_date
    days_after_due = 0
    in_window = True
else:
    now_raw = os.environ.get("OPPORTUNITY_RADAR_NOW")
    if now_raw:
        if len(now_raw) == 10:
            today = date.fromisoformat(now_raw)
        else:
            normalized = now_raw[:-1] + "+00:00" if now_raw.endswith("Z") else now_raw
            today = datetime.fromisoformat(normalized).astimezone(ZoneInfo(timezone)).date()
    else:
        today = datetime.now(ZoneInfo(timezone)).date()

    target = today - timedelta(days=(today.isoweekday() - due_weekday) % 7)
    days_after_due = (today - target).days
    in_window = 0 <= days_after_due <= catchup_days
    run_date = target

print(f"today={today.isoformat()}")
print(f"run_date={run_date.isoformat()}")
print(f"target_date={target.isoformat()}")
print(f"days_after_due={days_after_due}")
print(f"in_window={'true' if in_window else 'false'}")
PY
)"

today=""
run_date=""
target_date=""
days_after_due=""
in_window="false"

while IFS='=' read -r key value; do
  case "$key" in
    today) today="$value" ;;
    run_date) run_date="$value" ;;
    target_date) target_date="$value" ;;
    days_after_due) days_after_due="$value" ;;
    in_window) in_window="$value" ;;
  esac
done <<< "$date_state"

if [[ -z "$run_date" || -z "$target_date" ]]; then
  echo "could not compute Opportunity Radar cadence date" >&2
  exit 2
fi

report_path="opportunity-reports/${run_date}.md"

remote_branch_exists() {
  if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    return 1
  fi
  if ! git remote get-url origin >/dev/null 2>&1; then
    return 1
  fi

  local refs
  refs="$(git ls-remote --heads origin "refs/heads/opportunity-radar/${run_date}-*" 2>/dev/null || true)"
  [[ -n "$refs" ]]
}

should_run="false"
reason="scheduled wake-up is outside the Opportunity Radar catch-up window"

if [[ "$event_name" != "schedule" ]]; then
  should_run="true"
  reason="manual run"
elif [[ "$in_window" != "true" ]]; then
  should_run="false"
  reason="scheduled wake-up is outside the Opportunity Radar catch-up window"
elif [[ -f "$report_path" ]]; then
  should_run="false"
  reason="weekly report already exists for ${run_date}"
elif remote_branch_exists; then
  should_run="false"
  reason="generated Opportunity Radar branch already exists for ${run_date}"
else
  should_run="true"
  reason="weekly Opportunity Radar report is missing for ${run_date}"
fi

if [[ -n "${GITHUB_OUTPUT:-}" ]]; then
  {
    echo "should_run=$should_run"
    echo "reason=$reason"
    echo "run_date=$run_date"
    echo "target_date=$target_date"
    echo "today=$today"
    echo "days_after_due=$days_after_due"
  } >> "$GITHUB_OUTPUT"
fi

if [[ -n "${GITHUB_ENV:-}" ]]; then
  {
    echo "OPPORTUNITY_RADAR_RUN_DATE=$run_date"
    echo "OPPORTUNITY_RADAR_DATE=$run_date"
    echo "OPPORTUNITY_RADAR_CADENCE_REASON=$reason"
  } >> "$GITHUB_ENV"
fi

echo "Opportunity Radar cadence: should_run=$should_run, run_date=$run_date, today=$today, days_after_due=$days_after_due, reason=$reason"
