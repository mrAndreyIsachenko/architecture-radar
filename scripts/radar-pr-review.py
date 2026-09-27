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
delivery = load_module("radar_review_delivery", ROOT / "scripts" / "radar-review-delivery.py")


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
    parser.add_argument("--delivery-state", type=Path, default=delivery.default_path())
    parser.add_argument("--delivery-scope", default=os.environ.get("CODEX_THREAD_ID", ""))
    parser.add_argument("--ack-delivered", type=int, metavar="PR", help="Attest an already visible substantive review, never helper stdout")
    parser.add_argument("--head-sha")
    parser.add_argument("--message-ref", help="Reference to the already delivered message or turn")
    args = parser.parse_args()
    if args.ack_delivered is not None:
        if not args.head_sha or not args.message_ref or not args.delivery_scope or args.radar == "all":
            parser.error("acknowledgement requires --head-sha, --message-ref, --delivery-scope (or CODEX_THREAD_ID), and one --radar")
    elif args.head_sha or args.message_ref:
        parser.error("--head-sha and --message-ref require --ack-delivered")
    return args


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
    scope = getattr(args, "delivery_scope", "")
    review: dict[str, object] = {
        "repo": args.repo,
        "status": status,
        "pr_overviews": [],
        "delivery_scope": scope,
        "pending_reviews": [],
        "delivered_reviews": [],
        "delivery_warnings": [],
        "review_errors": [],
        "validation_blockers": [],
    }
    receipts = {}
    if not scope:
        review["delivery_warnings"].append("No delivery scope: reviews cannot be suppressed or acknowledged.")
    else:
        try:
            receipts = delivery.read_receipts(getattr(args, "delivery_state", delivery.default_path()))
        except delivery.DeliveryError as exc:
            review["delivery_warnings"].append(str(exc))

    fresh_prs = status.get("fresh_prs") or []
    if not isinstance(fresh_prs, list):
        return review
    if not fresh_prs:
        review["operational_statuses"] = [profile.get("operational", profile) for profile in (status.get("radars") or [status])]
        return review

    for pr in fresh_prs:
        if not isinstance(pr, dict) or not pr.get("number"):
            continue
        radar = str(pr.get("radar") or "architecture")
        summarizer = opportunity_pr_summary_helper if radar == "opportunity" else pr_summary_helper
        try:
            overview = dict(summarizer.summarize_pr(args.repo, str(pr["number"])))
        except (SystemExit, ValueError) as exc:
            review["pending_reviews"].append({**pr, "delivery_status": "pending", "acknowledgeable": False})
            review["review_errors"].append(f"PR #{pr['number']}: {exc}; review remains pending")
            continue
        overview["radar"] = radar
        item = {"repo": args.repo, "scope": scope, "number": pr["number"], "radar": radar,
                "head_sha": overview.get("head_sha"), "url": overview.get("url")}
        receipt = None
        try:
            key = delivery.identity(args.repo, scope, int(pr["number"]), str(item["head_sha"] or ""))
            receipt = receipts.get(key)
        except delivery.DeliveryError as exc:
            review["delivery_warnings"].append(f"PR #{pr['number']}: {exc}")
        recommendation = overview.get("review_recommendation") or {}
        if recommendation.get("decision") in {"needs_manual_review", "needs_targeted_fix", "should_close"}:
            review["validation_blockers"].append({**item, **recommendation})
        if receipt:
            review["delivered_reviews"].append({**item, "delivery_status": "delivered", "receipt": receipt})
        else:
            review["pending_reviews"].append({**item, "delivery_status": "pending"})
            review["pr_overviews"].append(overview)

    # Receipt filtering changes content eligibility only, not run health.
    profiles = status.get("radars") or [status]
    operational = [profile.get("operational", profile) for profile in profiles]
    review["operational_statuses"] = operational
    if review["pending_reviews"]:
        outcome = ("pending_review", "REVIEW", "Substantive reviews are pending; unchanged PR metadata is not delivery evidence.")
    elif review["validation_blockers"] or review["delivery_warnings"]:
        outcome = ("attention_required", "REPORT", "No pending content review, but blockers or delivery-state warnings remain.")
    else:
        problem = next((op for kind in ("failed_run", "missed_schedule", "waiting") for op in operational if op.get("status") == kind), None)
        outcome = (problem["status"], problem["notification"], problem["message"]) if problem else (
            "no_pending_review", "INFO", "No pending content review; open PRs may still exist.")
    review["status"] = {**status, **dict(zip(("status", "notification", "message"), outcome))}
    return review


def emit_markdown(review: dict[str, object]) -> None:
    status = review.get("status")
    if not isinstance(status, dict):
        print("Status: unknown")
        return

    notification = status.get("notification")
    message = status.get("message")

    print(f"Delivery scope: {review.get('delivery_scope') or 'unavailable'}")
    for warning in review.get("delivery_warnings", []) + review.get("review_errors", []):
        print(f"Warning: {warning}")
    for item in review.get("pending_reviews", []):
        print(f"Pending content review: #{item['number']} SHA={item.get('head_sha') or 'unknown'}")
    for item in review.get("delivered_reviews", []):
        print(f"Delivered content review: #{item['number']} SHA={item['head_sha']} ({item['receipt']['message_ref']}; caller_attested)")
    for item in review.get("validation_blockers", []):
        print(f"PR #{item['number']} blocker: {item.get('reason')}; next action: {item.get('next_action')}")
    for op in review.get("operational_statuses", []):
        run = (op.get("latest_completed_run") if op.get("status") == "failed_run" else op.get("latest_run")) or {}
        print(f"Workflow {op.get('radar_label', '')}: {op.get('status')} {run.get('url', '')}")
        for line in op.get("failed_log_excerpt", []):
            print(f"- {line}")

    if notification == "DONT_NOTIFY":
        print(f"DONT_NOTIFY: {message}")
        return

    print(f"Status: {status.get('status')}")
    print(f"Message: {message}")

    radars = status.get("radars") or []
    if isinstance(radars, list) and radars:
        print("Radar discovery statuses (before delivery filtering):")
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
    if args.ack_delivered is not None:
        try:
            receipt = delivery.acknowledge(args.delivery_state, args.repo, args.delivery_scope,
                                           args.ack_delivered, args.head_sha, args.radar, args.message_ref)
        except delivery.DeliveryError as exc:
            raise SystemExit(str(exc)) from exc
        print(json.dumps({"delivery_status": "delivered", "receipt": receipt}, indent=2))
        return
    review = build_review(args)
    if args.format == "json":
        print(json.dumps(review, indent=2, sort_keys=True))
    else:
        emit_markdown(review)


if __name__ == "__main__":
    main()
