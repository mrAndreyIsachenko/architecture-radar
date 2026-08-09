#!/usr/bin/env python3
"""Summarize a fresh Architecture Radar pull request for local review."""

from __future__ import annotations

import argparse
import base64
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote


DEFAULT_REPO = "mrAndreyIsachenko/architecture-radar"
RADAR_PR_TITLE_RE = re.compile(r"\bArchitecture Radar \d{4}-\d{2}-\d{2}\b")
RADAR_PR_BRANCH_RE = re.compile(r"^architecture-radar/\d{4}-\d{2}-\d{2}-")
ROOT = Path(__file__).resolve().parents[1]
REPORT_SUMMARY_SCRIPT = ROOT / "scripts" / "summarize-radar-report.py"

spec = importlib.util.spec_from_file_location("summarize_radar_report", REPORT_SUMMARY_SCRIPT)
report_summary = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(report_summary)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pr", nargs="?", help="Pull request number or URL. Defaults to newest open radar PR.")
    parser.add_argument("--repo", default=os.environ.get("ARCHITECTURE_RADAR_REPOSITORY", DEFAULT_REPO))
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    return parser.parse_args()


def gh_cache_env() -> dict[str, str]:
    env = os.environ.copy()
    if "XDG_CACHE_HOME" not in env:
        tmpdir = Path(env.get("TMPDIR", "/tmp"))
        env["XDG_CACHE_HOME"] = str(tmpdir / "architecture-radar-gh-cache")
    return env


def run_gh(args: list[str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["gh", *args],
        check=False,
        capture_output=True,
        text=True,
        env=gh_cache_env(),
    )
    if result.returncode != 0:
        print(result.stderr.strip() or result.stdout.strip(), file=sys.stderr)
        raise SystemExit(result.returncode)
    return result


def load_json_from_gh(args: list[str]) -> object:
    result = run_gh(args)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"failed to parse gh JSON output: {exc}") from exc


def is_radar_pr(pr: dict[str, object]) -> bool:
    title = str(pr.get("title") or "")
    head = str(pr.get("headRefName") or "")
    return bool(RADAR_PR_TITLE_RE.search(title) or RADAR_PR_BRANCH_RE.search(head))


def newest_open_radar_pr(repo: str) -> str:
    data = load_json_from_gh(
        [
            "pr",
            "list",
            "--repo",
            repo,
            "--state",
            "open",
            "--limit",
            "20",
            "--json",
            "number,title,headRefName,updatedAt",
        ]
    )
    if not isinstance(data, list):
        raise SystemExit("unexpected gh pr list response")

    for pr in data:
        if isinstance(pr, dict) and is_radar_pr(pr):
            return str(pr["number"])
    raise SystemExit("no open Architecture Radar PR found")


def pr_view(repo: str, pr: str) -> dict[str, object]:
    fields = "number,title,url,headRefName,baseRefName,isDraft,mergeable,statusCheckRollup,files"
    data = load_json_from_gh(["pr", "view", pr, "--repo", repo, "--json", fields])
    if not isinstance(data, dict):
        raise SystemExit("unexpected gh pr view response")
    return data


def check_summary(check: dict[str, object]) -> dict[str, str]:
    return {
        "name": str(check.get("name") or check.get("context") or ""),
        "status": str(check.get("status") or ""),
        "conclusion": str(check.get("conclusion") or ""),
        "details_url": str(check.get("detailsUrl") or check.get("targetUrl") or ""),
        "workflow": str(check.get("workflowName") or ""),
    }


def changed_files_by_kind(files: list[dict[str, object]]) -> dict[str, list[str]]:
    kinds = {
        "reports": [],
        "repositories": [],
        "patterns": [],
        "radar": [],
        "readme": [],
        "other": [],
    }

    for file_info in files:
        path = str(file_info.get("path") or "")
        if path.startswith("reports/") and path.endswith(".md"):
            kinds["reports"].append(path)
        elif path.startswith("repositories/") and path.endswith(".md"):
            kinds["repositories"].append(path)
        elif path.startswith("patterns/") and path.endswith(".md"):
            kinds["patterns"].append(path)
        elif path == "radar.json":
            kinds["radar"].append(path)
        elif path == "README.md":
            kinds["readme"].append(path)
        else:
            kinds["other"].append(path)

    return kinds


def required_check_state(checks: list[dict[str, str]]) -> str:
    for check in checks:
        if check.get("name") == "validate" or check.get("workflow") == "Radar Validation":
            status = check.get("status", "").lower()
            conclusion = check.get("conclusion", "").lower()
            if status == "completed" and conclusion == "success":
                return "passed"
            if status == "completed" and conclusion:
                return "failed"
            return "pending"
    return "missing"


def review_recommendation(summary: dict[str, object]) -> dict[str, str]:
    checks = summary.get("checks") or []
    if not isinstance(checks, list):
        checks = []

    check_state = required_check_state([check for check in checks if isinstance(check, dict)])
    changed = summary.get("changed_files") or {}
    reports = summary.get("reports") or []
    is_draft = bool(summary.get("is_draft"))
    mergeable = str(summary.get("mergeable") or "")

    if check_state == "failed":
        return {
            "decision": "needs_manual_review",
            "reason": "required validation failed",
            "next_action": "inspect the failing Radar Validation check before reviewing content",
        }
    if check_state in {"pending", "missing"}:
        return {
            "decision": "needs_manual_review",
            "reason": f"required validation is {check_state}",
            "next_action": "wait for validation or inspect why the required check is missing",
        }
    if isinstance(changed, dict) and not changed.get("reports"):
        return {
            "decision": "needs_manual_review",
            "reason": "no changed report file was found in the PR",
            "next_action": "confirm whether this is an infrastructure PR rather than a radar report PR",
        }
    if not isinstance(reports, list) or not reports:
        return {
            "decision": "needs_manual_review",
            "reason": "changed reports could not be summarized",
            "next_action": "inspect the report files directly",
        }
    if is_draft:
        return {
            "decision": "needs_manual_review",
            "reason": "PR is still marked draft",
            "next_action": "mark ready for review after confirming the generated artifacts",
        }
    if mergeable not in {"MERGEABLE", "UNKNOWN"}:
        return {
            "decision": "needs_manual_review",
            "reason": f"GitHub mergeability is {mergeable or 'unknown'}",
            "next_action": "resolve mergeability before content review",
        }
    return {
        "decision": "looks_mergeable",
        "reason": "required validation passed and changed reports were summarized",
        "next_action": "manually read the report evidence and merge if the findings clear the quality bar",
    }


def fetch_file_text(repo: str, ref: str, path: str) -> str:
    encoded_path = quote(path, safe="/")
    encoded_ref = quote(ref, safe="")
    data = load_json_from_gh(["api", f"repos/{repo}/contents/{encoded_path}?ref={encoded_ref}"])
    if not isinstance(data, dict):
        raise SystemExit(f"unexpected GitHub contents response for {path}")
    if data.get("encoding") != "base64" or not isinstance(data.get("content"), str):
        raise SystemExit(f"cannot decode GitHub contents response for {path}")
    return base64.b64decode(data["content"]).decode("utf-8")


def summarize_pr(repo: str, pr: str | None) -> dict[str, object]:
    pr_ref = pr or newest_open_radar_pr(repo)
    view = pr_view(repo, pr_ref)
    files = view.get("files") or []
    if not isinstance(files, list):
        files = []

    checks = view.get("statusCheckRollup") or []
    if not isinstance(checks, list):
        checks = []

    changed = changed_files_by_kind([file_info for file_info in files if isinstance(file_info, dict)])
    head = str(view.get("headRefName") or "")
    report_summaries = []

    for path in changed["reports"]:
        text = fetch_file_text(repo, head, path)
        report_summaries.append(report_summary.summarize_report_text(text, path))

    summary = {
        "repo": repo,
        "number": view.get("number"),
        "title": view.get("title"),
        "url": view.get("url"),
        "head": head,
        "base": view.get("baseRefName"),
        "is_draft": view.get("isDraft"),
        "mergeable": view.get("mergeable"),
        "checks": [check_summary(check) for check in checks if isinstance(check, dict)],
        "changed_files": changed,
        "reports": report_summaries,
    }
    summary["review_recommendation"] = review_recommendation(summary)
    return summary


def emit_markdown(summary: dict[str, object]) -> None:
    print(f"PR: #{summary['number']} {summary['title']}")
    print(f"URL: {summary['url']}")
    print(f"Branch: {summary['head']} -> {summary['base']}")
    print(f"Draft: {summary['is_draft']}")
    print(f"Mergeable: {summary['mergeable']}")
    recommendation = summary.get("review_recommendation") or {}
    if isinstance(recommendation, dict) and recommendation:
        print(f"Review decision: {recommendation.get('decision')} - {recommendation.get('reason')}")
        print(f"Next action: {recommendation.get('next_action')}")

    checks = summary.get("checks") or []
    if isinstance(checks, list) and checks:
        print("Checks:")
        for check in checks:
            if isinstance(check, dict):
                print(f"- {check.get('workflow') or check.get('name')}: {check.get('status')}/{check.get('conclusion')} {check.get('details_url')}")

    changed = summary.get("changed_files") or {}
    if isinstance(changed, dict):
        print("Changed radar artifacts:")
        for kind in ("reports", "repositories", "patterns", "radar", "readme", "other"):
            values = changed.get(kind) or []
            if isinstance(values, list) and values:
                print(f"- {kind}: {', '.join(str(value) for value in values)}")

    reports = summary.get("reports") or []
    for report in reports:
        if not isinstance(report, dict):
            continue
        print()
        print(f"Report: {report.get('path')}")
        print(f"Candidate count: {report.get('candidate_count')} (ledger rows: {report.get('ledger_rows')})")
        print_list("Selected repositories", report.get("selected_repositories"))
        print_list("Updated patterns", report.get("updated_patterns"))
        print_list("Evidence gaps", report.get("evidence_gaps"))
        next_action = str(report.get("recommended_next_action") or "").strip()
        if next_action:
            print("Recommended next action:")
            print(next_action)


def print_list(label: str, values: object) -> None:
    if not isinstance(values, list) or not values:
        return
    print(f"{label}:")
    for value in values:
        print(f"- {value}")


def main() -> None:
    args = parse_args()
    summary = summarize_pr(args.repo, args.pr)
    if args.format == "json":
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        emit_markdown(summary)


if __name__ == "__main__":
    main()
