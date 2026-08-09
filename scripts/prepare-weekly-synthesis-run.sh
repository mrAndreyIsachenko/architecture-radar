#!/usr/bin/env bash
set -euo pipefail

if [[ -n "${WEEKLY_SYNTHESIS_DATE:-}" ]]; then
  run_date="$WEEKLY_SYNTHESIS_DATE"
else
  run_date="$(TZ=Europe/Moscow date +%F)"
fi

if [[ ! "$run_date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  echo "WEEKLY_SYNTHESIS_DATE must be YYYY-MM-DD, got: $run_date" >&2
  exit 2
fi

week_id="$(python3 - "$run_date" <<'PY'
from datetime import date
import sys

run_date = date.fromisoformat(sys.argv[1])
iso_year, iso_week, _ = run_date.isocalendar()
print(f"{iso_year}-W{iso_week:02d}")
PY
)"

branch="weekly-synthesis/${week_id}-${GITHUB_RUN_NUMBER:-local}"

git config user.name "weekly-synthesis-bot"
git config user.email "weekly-synthesis-bot@users.noreply.github.com"
git checkout -B "$branch"

{
  echo "WEEKLY_SYNTHESIS_RUN_DATE=$run_date"
  echo "WEEKLY_SYNTHESIS_WEEK_ID=$week_id"
  echo "WEEKLY_SYNTHESIS_BRANCH=$branch"
} >> "${GITHUB_ENV:-/dev/null}"

echo "Prepared $branch for $week_id"
