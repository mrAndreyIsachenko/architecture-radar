#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Sequence


ROOT = Path.cwd()

REQUIRED_PR_FIELDS = (
    "User request",
    "Scope confirmed",
    "Autonomous follow-up",
)

PLACEHOLDER_RE = re.compile(
    r"^\s*(?:todo|tbd|n/a|na|none|replace\s+this|fill\s+this|not\s+applicable|<!--.*-->)\s*$",
    re.IGNORECASE,
)

GENERATED_ARTIFACT_PREFIXES = (
    "reports/",
    "repositories/",
    "patterns/",
    "opportunity-reports/",
    "opportunities/",
    "signals/",
    "weekly-reports/",
)

GENERATED_ARTIFACT_FILES = {
    "radar.json",
    "opportunities.json",
}

GOVERNED_PREFIXES = (
    ".github/workflows/",
    ".github/ISSUE_TEMPLATE/",
    "scripts/",
    "tests/",
    ".codex/skills/",
    "openspec/specs/",
)

GOVERNED_FILES = {
    "AGENTS.md",
    ".github/pull_request_template.md",
    "openspec/config.yaml",
}

GOVERNED_DOCS = {
    "docs/agent-rules.md",
    "docs/opportunity-agent-rules.md",
    "docs/research-scope.md",
    "docs/opportunity-research-scope.md",
    "docs/github-actions.md",
    "docs/publication-checklist.md",
    "docs/release-checklist.md",
}


def normalize_path(path: str) -> str:
    return path.strip().replace("\\", "/")


def run_git(args: Sequence[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def git_ref_exists(ref: str) -> bool:
    result = run_git(["rev-parse", "--verify", "--quiet", ref])
    return result.returncode == 0


def changed_files(base_ref: str | None = None) -> list[str]:
    diff_range = ["HEAD"]
    if base_ref:
        remote_base = f"origin/{base_ref}"
        if git_ref_exists(remote_base):
            diff_range = [f"{remote_base}...HEAD"]
        elif git_ref_exists(base_ref):
            diff_range = [f"{base_ref}...HEAD"]

    diff = run_git(["diff", "--name-only", "--diff-filter=ACMRTD", *diff_range])
    paths = set(diff.stdout.splitlines()) if diff.returncode == 0 else set()

    untracked = run_git(["ls-files", "--others", "--exclude-standard"])
    if untracked.returncode == 0:
        paths.update(untracked.stdout.splitlines())

    return sorted(normalize_path(path) for path in paths if path.strip())


def pr_body_from_event(event_path: str | None = None) -> str | None:
    path = event_path or os.environ.get("GITHUB_EVENT_PATH")
    if not path:
        return None

    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None

    pull_request = payload.get("pull_request")
    if not isinstance(pull_request, dict):
        return None

    body = pull_request.get("body")
    return body if isinstance(body, str) else ""


def field_value(body: str, field: str) -> str | None:
    match = re.search(rf"(?im)^\s*{re.escape(field)}\s*:\s*(.*?)\s*$", body)
    if not match:
        return None
    return match.group(1).strip()


def has_non_placeholder_value(value: str | None) -> bool:
    if value is None:
        return False
    if PLACEHOLDER_RE.match(value):
        return False
    return bool(value.strip())


def validate_pr_body(body: str | None) -> list[str]:
    if body is None:
        return []

    errors: list[str] = []
    user_request = field_value(body, "User request")
    scope_confirmed = field_value(body, "Scope confirmed")
    autonomous_follow_up = field_value(body, "Autonomous follow-up")

    if not has_non_placeholder_value(user_request):
        errors.append("pull request body must contain `User request:` with a non-placeholder value")
    if (scope_confirmed or "").strip().lower() != "yes":
        errors.append("pull request body must contain `Scope confirmed: yes`")
    if (autonomous_follow_up or "").strip().lower() != "no":
        errors.append("pull request body must contain `Autonomous follow-up: no`")

    return errors


def is_generated_artifact(path: str) -> bool:
    path = normalize_path(path)
    return path in GENERATED_ARTIFACT_FILES or path.startswith(GENERATED_ARTIFACT_PREFIXES)


def is_openspec_evidence(path: str) -> bool:
    path = normalize_path(path)
    if not path.startswith("openspec/changes/"):
        return False
    return (
        path.endswith("/.openspec.yaml")
        or path.endswith("/proposal.md")
        or path.endswith("/design.md")
        or path.endswith("/tasks.md")
        or "/specs/" in path
    )


def is_governed_behavior(path: str) -> bool:
    path = normalize_path(path)
    if path in GOVERNED_FILES or path in GOVERNED_DOCS:
        return True
    return path.startswith(GOVERNED_PREFIXES)


def validate_changed_files(paths: Sequence[str]) -> list[str]:
    normalized = [normalize_path(path) for path in paths]
    governed = [path for path in normalized if is_governed_behavior(path)]
    if not governed:
        return []

    if all(is_generated_artifact(path) for path in normalized):
        return []

    evidence = [path for path in normalized if is_openspec_evidence(path)]
    if evidence:
        return []

    return [
        "governed behavior changes require OpenSpec evidence in the same pull request: "
        + ", ".join(governed[:8])
    ]


def validate_static_files(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    agents = root / "AGENTS.md"
    if not agents.is_file():
        errors.append("AGENTS.md is required")

    template = root / ".github" / "pull_request_template.md"
    if not template.is_file():
        errors.append(".github/pull_request_template.md is required")
    else:
        text = template.read_text(encoding="utf-8")
        for field in REQUIRED_PR_FIELDS:
            if f"{field}:" not in text:
                errors.append(f".github/pull_request_template.md must contain `{field}:`")

    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(validate_static_files())

    body = pr_body_from_event()
    errors.extend(validate_pr_body(body))

    base_ref = os.environ.get("GOVERNANCE_BASE_REF") or os.environ.get("GITHUB_BASE_REF")
    paths = changed_files(base_ref)
    errors.extend(validate_changed_files(paths))

    if errors:
        print("Agent governance validation failed:")
        for error in errors:
            print(f"- {error}")
        if paths:
            print("")
            print("Changed files:")
            for path in paths:
                print(f"- {path}")
        return 1

    print("Agent governance validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
