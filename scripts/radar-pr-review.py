#!/usr/bin/env python3
"""Single entrypoint for the local generated radar PR-review heartbeat."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
from argparse import Namespace
from pathlib import Path


DEFAULT_REPO = "mrAndreyIsachenko/architecture-radar"
DEFAULT_ARCHITECTURE_WORKFLOW = "architecture-radar.yml"
DEFAULT_TZ = "Europe/Moscow"
DEFAULT_ANCHOR = "2026-08-02"
DEFAULT_CADENCE_DAYS = 3
DEFAULT_SCHEDULE_HOUR_UTC = 5
DEFAULT_SCHEDULE_MINUTE_UTC = 0
ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


status_helper = load_module("radar_pr_review_status", ROOT / "scripts" / "radar-pr-review-status.py")
pr_summary_helper = load_module("summarize_radar_pr", ROOT / "scripts" / "summarize-radar-pr.py")
opportunity_pr_summary_helper = load_module(
    "summarize_opportunity_pr",
    ROOT / "scripts" / "summarize-opportunity-pr.py",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=os.environ.get("ARCHITECTURE_RADAR_REPOSITORY", DEFAULT_REPO))
    parser.add_argument(
        "--radar",
        choices=("all", "architecture", "opportunity"),
        default=os.environ.get("RADAR_PR_REVIEW_RADAR", "all"),
        help="Radar profile to check. Defaults to both Architecture and Opportunity Radar.",
    )
    parser.add_argument(
        "--workflow",
        default=os.environ.get("RADAR_PR_REVIEW_WORKFLOW"),
        help="Override workflow file for a single selected radar profile.",
    )
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
    parser.add_argument(
        "--schedule-minute-utc",
        type=int,
        default=int(os.environ.get("ARCHITECTURE_RADAR_SCHEDULE_MINUTE_UTC", str(DEFAULT_SCHEDULE_MINUTE_UTC))),
    )
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--include-failed-log", action="store_true")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    return parser.parse_args()


def status_args(args: argparse.Namespace) -> Namespace:
    return Namespace(
        repo=args.repo,
        radar=args.radar,
        workflow=args.workflow,
        timezone=args.timezone,
        now=args.now,
        cadence_anchor=args.cadence_anchor,
        cadence_days=args.cadence_days,
        schedule_hour_utc=args.schedule_hour_utc,
        schedule_minute_utc=args.schedule_minute_utc,
        limit=args.limit,
        format="json",
        include_failed_log=args.include_failed_log,
    )


def build_review(args: argparse.Namespace) -> dict[str, object]:
    status = status_helper.build_status(status_args(args))
    review: dict[str, object] = {
        "repo": args.repo,
        "status": status,
        "pr_overviews": [],
    }

    if status.get("status") != "fresh_pr":
        return review

    fresh_prs = status.get("fresh_prs") or []
    if not isinstance(fresh_prs, list):
        return review

    overviews = []
    for pr in fresh_prs:
        if not isinstance(pr, dict) or not pr.get("number"):
            continue
        radar = str(pr.get("radar") or "architecture")
        if radar == "opportunity":
            overviews.append(opportunity_pr_summary_helper.summarize_pr(args.repo, str(pr["number"])))
        else:
            overview = pr_summary_helper.summarize_pr(args.repo, str(pr["number"]))
            if isinstance(overview, dict):
                overview["radar"] = "architecture"
            overviews.append(overview)

    review["pr_overviews"] = overviews
    return review


def emit_markdown(review: dict[str, object]) -> None:
    status = review.get("status")
    if not isinstance(status, dict):
        print("Status: unknown")
        return

    notification = status.get("notification")
    message = status.get("message")

    if notification == "DONT_NOTIFY":
        print(f"DONT_NOTIFY: {message}")
        return

    print(f"Status: {status.get('status')}")
    print(f"Message: {message}")

    radars = status.get("radars") or []
    if isinstance(radars, list) and radars:
        print("Radar statuses:")
        for radar_status in radars:
            if isinstance(radar_status, dict):
                print(
                    "- "
                    f"{radar_status.get('radar_label')}: "
                    f"{radar_status.get('status')}/{radar_status.get('notification')} - "
                    f"{radar_status.get('message')}"
                )

    latest_run = status.get("latest_run") or {}
    if isinstance(latest_run, dict) and latest_run:
        print(
            "Latest run: "
            f"{latest_run.get('status')}/{latest_run.get('conclusion')} "
            f"{latest_run.get('event')} {latest_run.get('createdAt')} "
            f"{latest_run.get('url')}"
        )

    failed_log_excerpt = status.get("failed_log_excerpt") or []
    if isinstance(failed_log_excerpt, list) and failed_log_excerpt:
        print("Failure excerpt:")
        for line in failed_log_excerpt:
            print(f"- {line}")

    failed_runs = status.get("failed_runs") or []
    if isinstance(failed_runs, list) and failed_runs:
        for failed in failed_runs:
            if not isinstance(failed, dict):
                continue
            excerpt = failed.get("failed_log_excerpt") or []
            if isinstance(excerpt, list) and excerpt:
                print(f"Failure excerpt for {failed.get('radar_label')}:")
                for line in excerpt:
                    print(f"- {line}")

    overviews = review.get("pr_overviews") or []
    for overview in overviews:
        if not isinstance(overview, dict):
            continue
        print()
        if overview.get("radar") == "opportunity":
            opportunity_pr_summary_helper.emit_markdown(overview)
        else:
            pr_summary_helper.emit_markdown(overview)


def main() -> None:
    args = parse_args()
    review = build_review(args)
    if args.format == "json":
        print(json.dumps(review, indent=2, sort_keys=True))
    else:
        emit_markdown(review)


if __name__ == "__main__":
    main()
