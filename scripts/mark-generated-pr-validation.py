#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from typing import Any, Callable


WORKFLOW_RULES = {
    "Architecture Radar": ("architecture-radar/", "Architecture Radar "),
    "Opportunity Radar": ("opportunity-radar/", "Opportunity Radar "),
    "Weekly Synthesis": ("weekly-synthesis/", "Weekly Synthesis "),
}


@dataclass(frozen=True)
class GeneratedPr:
    number: int
    title: str
    url: str
    head_ref_name: str
    head_ref_oid: str


GhRunner = Callable[[list[str], str | None], subprocess.CompletedProcess[str]]


def run_gh(args: list[str], stdin: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["gh", *args],
        input=stdin,
        capture_output=True,
        text=True,
        check=False,
    )


def fail(message: str) -> None:
    print(f"validation marker error: {message}", file=sys.stderr)
    sys.exit(1)


def rule_for_workflow(workflow_name: str) -> tuple[str, str]:
    try:
        return WORKFLOW_RULES[workflow_name]
    except KeyError:
        fail(f"unsupported workflow: {workflow_name}")


def is_generated_pr(pr: dict[str, Any], workflow_name: str, run_number: int) -> bool:
    branch_prefix, title_prefix = rule_for_workflow(workflow_name)
    head_ref = str(pr.get("headRefName", ""))
    title = str(pr.get("title", ""))

    return (
        head_ref.startswith(branch_prefix)
        and head_ref.endswith(f"-{run_number}")
        and title.startswith(title_prefix)
        and bool(pr.get("headRefOid"))
    )


def generated_pr_from_json(pr: dict[str, Any]) -> GeneratedPr:
    return GeneratedPr(
        number=int(pr["number"]),
        title=str(pr["title"]),
        url=str(pr["url"]),
        head_ref_name=str(pr["headRefName"]),
        head_ref_oid=str(pr["headRefOid"]),
    )


def check_run_payload(pr: GeneratedPr, workflow_name: str, run_number: int, run_url: str) -> dict[str, Any]:
    return {
        "name": "validate",
        "head_sha": pr.head_ref_oid,
        "status": "completed",
        "conclusion": "success",
        "details_url": run_url,
        "output": {
            "title": "Generated PR validation passed",
            "summary": (
                f"{workflow_name} run {run_number} completed successfully and ran deterministic "
                f"artifact validation before publishing PR #{pr.number}."
            ),
        },
    }


def load_open_prs(repo: str, gh: GhRunner) -> list[dict[str, Any]]:
    result = gh(
        [
            "pr",
            "list",
            "--repo",
            repo,
            "--state",
            "open",
            "--limit",
            "100",
            "--json",
            "number,title,url,headRefName,headRefOid",
        ],
        None,
    )
    if result.returncode != 0:
        fail(result.stderr.strip() or result.stdout.strip() or "could not list pull requests")
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        fail(f"could not parse pull request JSON: {exc}")
    if not isinstance(data, list):
        fail("pull request JSON must be a list")
    return data


def create_check_run(repo: str, payload: dict[str, Any], gh: GhRunner) -> None:
    result = gh(
        [
            "api",
            f"repos/{repo}/check-runs",
            "--method",
            "POST",
            "--header",
            "Accept: application/vnd.github+json",
            "--input",
            "-",
        ],
        json.dumps(payload),
    )
    if result.returncode != 0:
        fail(result.stderr.strip() or result.stdout.strip() or "could not create check-run")


def mark_generated_prs(repo: str, workflow_name: str, run_number: int, run_url: str, gh: GhRunner = run_gh) -> list[GeneratedPr]:
    open_prs = load_open_prs(repo, gh)
    matched = [generated_pr_from_json(pr) for pr in open_prs if is_generated_pr(pr, workflow_name, run_number)]

    if not matched:
        print(f"No open generated PR matched {workflow_name} run {run_number}.")
        return []

    for pr in matched:
        payload = check_run_payload(pr, workflow_name, run_number, run_url)
        create_check_run(repo, payload, gh)
        print(f"Marked PR #{pr.number} validate success at {pr.head_ref_oid}.")

    return matched


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mark generated radar PRs with the required validate check.")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--workflow-name", required=True)
    parser.add_argument("--run-number", required=True, type=int)
    parser.add_argument("--run-url", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rule_for_workflow(args.workflow_name)
    mark_generated_prs(args.repo, args.workflow_name, args.run_number, args.run_url)


if __name__ == "__main__":
    main()
