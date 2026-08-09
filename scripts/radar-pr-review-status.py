#!/usr/bin/env python3
"""Report whether Architecture Radar has a fresh PR or needs more waiting.

This helper exists for the local PR-review heartbeat. It deliberately checks
open pull requests before it ever reports "no work", and it uses the same
cadence anchor as the GitHub Actions workflow.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime, time, timezone
from pathlib import Path
from zoneinfo import ZoneInfo


DEFAULT_REPO = "mrAndreyIsachenko/architecture-radar"
DEFAULT_WORKFLOW = "architecture-radar.yml"
DEFAULT_TZ = "Europe/Moscow"
DEFAULT_ANCHOR = "2026-08-02"
DEFAULT_CADENCE_DAYS = 3
DEFAULT_SCHEDULE_HOUR_UTC = 5
RADAR_PR_TITLE_RE = re.compile(r"\bArchitecture Radar \d{4}-\d{2}-\d{2}\b")
RADAR_PR_BRANCH_RE = re.compile(r"^architecture-radar/\d{4}-\d{2}-\d{2}-")
ERROR_PATTERNS = (
    "##[error]",
    "Invalid workflow file",
    "Process completed with exit code",
    "Error:",
    "error:",
    "failed",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=os.environ.get("ARCHITECTURE_RADAR_REPOSITORY", DEFAULT_REPO))
    parser.add_argument("--workflow", default=os.environ.get("ARCHITECTURE_RADAR_WORKFLOW", DEFAULT_WORKFLOW))
    parser.add_argument("--timezone", default=os.environ.get("ARCHITECTURE_RADAR_TIMEZONE", DEFAULT_TZ))
    parser.add_argument("--now", help="Current time as ISO-8601. Defaults to real current UTC time.")
    parser.add_argument(
        "--cadence-anchor",
        default=os.environ.get("ARCHITECTURE_RADAR_CADENCE_ANCHOR", DEFAULT_ANCHOR),
    )
    parser.add_argument(
        "--cadence-days",
        type=int,
        default=int(os.environ.get("ARCHITECTURE_RADAR_CADENCE_DAYS", str(DEFAULT_CADENCE_DAYS))),
    )
    parser.add_argument(
        "--schedule-hour-utc",
        type=int,
        default=int(os.environ.get("ARCHITECTURE_RADAR_SCHEDULE_HOUR_UTC", str(DEFAULT_SCHEDULE_HOUR_UTC))),
    )
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--include-failed-log", action="store_true")
    return parser.parse_args()


def parse_datetime(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def current_time(value: str | None) -> datetime:
    if value:
        return parse_datetime(value)
    return datetime.now(timezone.utc)


def gh_cache_env() -> dict[str, str]:
    env = os.environ.copy()
    if "XDG_CACHE_HOME" not in env:
        tmpdir = Path(env.get("TMPDIR", "/tmp"))
        env["XDG_CACHE_HOME"] = str(tmpdir / "architecture-radar-gh-cache")
    return env


def run_gh(args: list[str], *, allow_failure: bool = False) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["gh", *args],
        check=False,
        capture_output=True,
        text=True,
        env=gh_cache_env(),
    )
    if result.returncode != 0 and not allow_failure:
        print(result.stderr.strip() or result.stdout.strip(), file=sys.stderr)
        raise SystemExit(result.returncode)
    return result


def load_json_from_gh(args: list[str]) -> object:
    result = run_gh(args)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"failed to parse gh JSON output: {exc}") from exc


def list_runs(repo: str, workflow: str, limit: int) -> list[dict[str, object]]:
    fields = (
        "databaseId,displayTitle,event,status,conclusion,createdAt,updatedAt,"
        "headBranch,url,workflowName"
    )
    data = load_json_from_gh(
        ["run", "list", "--repo", repo, "--workflow", workflow, "--limit", str(limit), "--json", fields]
    )
    if not isinstance(data, list):
        raise SystemExit("unexpected gh run list response")
    return data


def list_prs(repo: str, limit: int) -> list[dict[str, object]]:
    fields = (
        "number,title,url,headRefName,baseRefName,createdAt,updatedAt,"
        "isDraft,mergeable,statusCheckRollup"
    )
    data = load_json_from_gh(["pr", "list", "--repo", repo, "--state", "open", "--limit", str(limit), "--json", fields])
    if not isinstance(data, list):
        raise SystemExit("unexpected gh pr list response")
    return data


def is_radar_pr(pr: dict[str, object]) -> bool:
    title = str(pr.get("title") or "")
    head = str(pr.get("headRefName") or "")
    return bool(RADAR_PR_TITLE_RE.search(title) or RADAR_PR_BRANCH_RE.search(head))


def check_summary(check: dict[str, object]) -> dict[str, str]:
    return {
        "name": str(check.get("name") or check.get("context") or ""),
        "status": str(check.get("status") or ""),
        "conclusion": str(check.get("conclusion") or ""),
        "details_url": str(check.get("detailsUrl") or check.get("targetUrl") or ""),
        "workflow": str(check.get("workflowName") or ""),
    }


def summarize_pr(pr: dict[str, object]) -> dict[str, object]:
    checks = pr.get("statusCheckRollup") or []
    if not isinstance(checks, list):
        checks = []
    return {
        "number": pr.get("number"),
        "title": pr.get("title"),
        "url": pr.get("url"),
        "head": pr.get("headRefName"),
        "base": pr.get("baseRefName"),
        "created_at": pr.get("createdAt"),
        "updated_at": pr.get("updatedAt"),
        "is_draft": pr.get("isDraft"),
        "mergeable": pr.get("mergeable"),
        "checks": [check_summary(check) for check in checks if isinstance(check, dict)],
    }


def run_local_date(run: dict[str, object], tz: ZoneInfo) -> date | None:
    created_at = run.get("createdAt")
    if not isinstance(created_at, str):
        return None
    return parse_datetime(created_at).astimezone(tz).date()


def cadence_state(now: datetime, tz: ZoneInfo, anchor: date, cadence_days: int, schedule_hour_utc: int) -> dict[str, object]:
    if cadence_days <= 0:
        raise SystemExit("--cadence-days must be positive")
    today = now.astimezone(tz).date()
    days_since = (today - anchor).days
    should_run = days_since >= 0 and days_since % cadence_days == 0
    scheduled_at = datetime.combine(today, time(hour=schedule_hour_utc), tzinfo=timezone.utc)
    return {
        "run_date": today.isoformat(),
        "days_since_anchor": days_since,
        "should_run": should_run,
        "reason": "scheduled cadence matched" if should_run else f"scheduled run is outside the {cadence_days}-day cadence",
        "scheduled_at_utc": scheduled_at.isoformat().replace("+00:00", "Z"),
    }


def latest_completed_run(runs: list[dict[str, object]]) -> dict[str, object] | None:
    for run in runs:
        if run.get("status") == "completed":
            return run
    return None


def today_schedule_run(runs: list[dict[str, object]], tz: ZoneInfo, today: date) -> dict[str, object] | None:
    for run in runs:
        if run.get("event") == "schedule" and run_local_date(run, tz) == today:
            return run
    return None


def failed_log_excerpt(repo: str, run_id: object) -> list[str]:
    if not run_id:
        return []
    result = run_gh(["run", "view", str(run_id), "--repo", repo, "--log-failed"], allow_failure=True)
    if result.returncode != 0:
        return [result.stderr.strip() or "failed to fetch failed run log"]

    excerpt: list[str] = []
    seen: set[str] = set()
    for raw_line in result.stdout.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if any(pattern in line for pattern in ERROR_PATTERNS):
            normalized = re.sub(r"\s+", " ", line)
            if normalized not in seen:
                seen.add(normalized)
                excerpt.append(normalized)
        if len(excerpt) >= 12:
            break
    return excerpt


def build_status(args: argparse.Namespace) -> dict[str, object]:
    tz = ZoneInfo(args.timezone)
    now = current_time(args.now)
    anchor = date.fromisoformat(args.cadence_anchor)
    cadence = cadence_state(now, tz, anchor, args.cadence_days, args.schedule_hour_utc)
    today = date.fromisoformat(str(cadence["run_date"]))

    runs = list_runs(args.repo, args.workflow, args.limit)
    prs = list_prs(args.repo, args.limit)
    fresh_prs = [summarize_pr(pr) for pr in prs if is_radar_pr(pr)]
    latest_run = runs[0] if runs else None
    latest_completed = latest_completed_run(runs)
    todays_schedule = today_schedule_run(runs, tz, today)

    result: dict[str, object] = {
        "repo": args.repo,
        "workflow": args.workflow,
        "now_utc": now.isoformat().replace("+00:00", "Z"),
        "cadence": cadence,
        "latest_run": latest_run,
        "latest_completed_run": latest_completed,
        "fresh_prs": fresh_prs,
        "status": "unknown",
        "notification": "INFO",
        "message": "",
    }

    if fresh_prs:
        result["status"] = "fresh_pr"
        result["notification"] = "REVIEW"
        result["message"] = "Fresh Architecture Radar PR found; inspect its diff before reporting."
        return result

    scheduled_at = parse_datetime(str(cadence["scheduled_at_utc"]))
    if cadence["should_run"] and now < scheduled_at:
        result["status"] = "waiting"
        result["notification"] = "DONT_NOTIFY"
        result["message"] = "Today's cadence run is not due yet."
        return result

    if cadence["should_run"] and not todays_schedule:
        result["status"] = "waiting"
        result["notification"] = "DONT_NOTIFY"
        result["message"] = "Today's scheduled cadence run has not appeared yet; wait for GitHub Actions schedule delay."
        return result

    if todays_schedule and todays_schedule.get("status") != "completed":
        result["status"] = "waiting"
        result["notification"] = "DONT_NOTIFY"
        result["message"] = "Today's scheduled cadence run is still queued or in progress."
        return result

    if latest_completed and latest_completed.get("conclusion") == "failure":
        result["status"] = "failed_run"
        result["notification"] = "REPORT"
        result["message"] = "Latest completed Architecture Radar run failed."
        if args.include_failed_log:
            result["failed_log_excerpt"] = failed_log_excerpt(args.repo, latest_completed.get("databaseId"))
        return result

    result["status"] = "no_pr"
    result["notification"] = "INFO"
    result["message"] = "No fresh Architecture Radar PR to review."
    return result


def emit_markdown(status: dict[str, object]) -> None:
    notification = status["notification"]
    message = status["message"]
    latest_run = status.get("latest_run") or {}

    if notification == "DONT_NOTIFY":
        print(f"DONT_NOTIFY: {message}")
        return

    print(f"Status: {status['status']}")
    print(f"Message: {message}")
    print(f"Repository: {status['repo']}")

    if isinstance(latest_run, dict) and latest_run:
        print(
            "Latest run: "
            f"{latest_run.get('status')}/{latest_run.get('conclusion')} "
            f"{latest_run.get('event')} {latest_run.get('createdAt')} "
            f"{latest_run.get('url')}"
        )

    fresh_prs = status.get("fresh_prs") or []
    if isinstance(fresh_prs, list) and fresh_prs:
        print("Fresh PRs:")
        for pr in fresh_prs:
            if not isinstance(pr, dict):
                continue
            print(f"- #{pr.get('number')} {pr.get('title')} {pr.get('url')} head={pr.get('head')}")

    failed_log_excerpt = status.get("failed_log_excerpt") or []
    if isinstance(failed_log_excerpt, list) and failed_log_excerpt:
        print("Failure excerpt:")
        for line in failed_log_excerpt:
            print(f"- {line}")


def main() -> None:
    args = parse_args()
    status = build_status(args)
    if args.format == "json":
        print(json.dumps(status, indent=2, sort_keys=True))
    else:
        emit_markdown(status)


if __name__ == "__main__":
    main()
