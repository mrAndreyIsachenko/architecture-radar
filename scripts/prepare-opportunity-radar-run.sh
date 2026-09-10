#!/usr/bin/env bash
set -euo pipefail

if [[ -n "${OPPORTUNITY_RADAR_DATE:-}" ]]; then
  run_date="$OPPORTUNITY_RADAR_DATE"
else
  run_date="$(TZ=Europe/Moscow date +%F)"
fi

if [[ ! "$run_date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  echo "OPPORTUNITY_RADAR_DATE must be YYYY-MM-DD, got: $run_date" >&2
  exit 2
fi

branch="opportunity-radar/${run_date}-${GITHUB_RUN_NUMBER:-local}"

commit_user_name="${RADAR_COMMIT_USER_NAME:-Andrey Isachenko}"
commit_user_email="${RADAR_COMMIT_USER_EMAIL:-mr.andrey.isachenko@gmail.com}"

git config user.name "$commit_user_name"
git config user.email "$commit_user_email"
git checkout -B "$branch"

{
  echo "OPPORTUNITY_RADAR_RUN_DATE=$run_date"
  echo "OPPORTUNITY_RADAR_BRANCH=$branch"
} >> "${GITHUB_ENV:-/dev/null}"

echo "Prepared $branch for $run_date"
