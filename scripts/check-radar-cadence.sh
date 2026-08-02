#!/usr/bin/env bash
set -euo pipefail

event_name="${GITHUB_EVENT_NAME:-local}"
anchor="${ARCHITECTURE_RADAR_CADENCE_ANCHOR:-2026-08-02}"
cadence_days="${ARCHITECTURE_RADAR_CADENCE_DAYS:-3}"
run_date="${ARCHITECTURE_RADAR_DATE:-}"

if [[ -z "$run_date" ]]; then
  run_date="$(TZ=Europe/Moscow date +%F)"
fi

if [[ ! "$cadence_days" =~ ^[1-9][0-9]*$ ]]; then
  echo "ARCHITECTURE_RADAR_CADENCE_DAYS must be a positive integer, got: $cadence_days" >&2
  exit 2
fi

days_since="$(
  python3 - "$anchor" "$run_date" <<'PY'
from datetime import date
import sys

try:
    anchor = date.fromisoformat(sys.argv[1])
    run_date = date.fromisoformat(sys.argv[2])
except ValueError as exc:
    raise SystemExit(f"invalid cadence date: {exc}")

print((run_date - anchor).days)
PY
)"

should_run="false"
reason="scheduled run is outside the ${cadence_days}-day cadence"

if [[ "$event_name" != "schedule" ]]; then
  should_run="true"
  reason="manual run"
elif (( days_since >= 0 && days_since % cadence_days == 0 )); then
  should_run="true"
  reason="scheduled cadence matched"
fi

if [[ -n "${GITHUB_OUTPUT:-}" ]]; then
  {
    echo "should_run=$should_run"
    echo "reason=$reason"
    echo "run_date=$run_date"
    echo "days_since_anchor=$days_since"
  } >> "$GITHUB_OUTPUT"
fi

echo "Architecture Radar cadence: should_run=$should_run, run_date=$run_date, days_since_anchor=$days_since, reason=$reason"
