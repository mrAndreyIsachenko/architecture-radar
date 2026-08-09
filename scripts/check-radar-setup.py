#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable


REQUIRED_FILES = [
    "README.md",
    "QUICKSTART.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "LICENSE",
    "interests.md",
    "watchlist.yml",
    "opportunity-interests.md",
    "opportunity-watchlist.yml",
    "radar.json",
    "opportunities.json",
    "docs/agent-rules.md",
    "docs/research-scope.md",
    "docs/opportunity-agent-rules.md",
    "docs/opportunity-research-scope.md",
    "docs/publication-checklist.md",
    "docs/release-checklist.md",
    "docs/releases/v0.1.0.md",
    ".github/workflows/architecture-radar.yml",
    ".github/workflows/opportunity-radar.yml",
    ".github/workflows/radar-validation.yml",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/feature_request.md",
    ".github/ISSUE_TEMPLATE/research_quality.md",
    ".github/ISSUE_TEMPLATE/config.yml",
    "openspec/config.yaml",
    "openspec/specs/architecture-radar/spec.md",
    ".codex/skills/openspec-explore/SKILL.md",
    ".codex/skills/openspec-propose/SKILL.md",
    ".codex/skills/openspec-apply-change/SKILL.md",
    ".codex/skills/openspec-update-change/SKILL.md",
    ".codex/skills/openspec-sync-specs/SKILL.md",
    ".codex/skills/openspec-archive-change/SKILL.md",
    "scripts/validate-radar-state.py",
    "scripts/run-codex-radar.sh",
    "scripts/prepare-radar-run.sh",
    "scripts/prepare-opportunity-radar-run.sh",
    "scripts/publish-opportunity-radar-run.sh",
    "scripts/publish-radar-run.sh",
    "scripts/run-codex-opportunity-radar.sh",
    "scripts/check-radar-cadence.sh",
    "scripts/check-radar-rerun.sh",
    "scripts/radar-pr-review.py",
    "scripts/radar-pr-review-status.py",
    "scripts/summarize-radar-pr.py",
    "scripts/summarize-radar-report.py",
    "scripts/validate-opportunity-radar-state.py",
    "tests/test_check_radar_setup.py",
    "tests/test_radar_pr_review.py",
    "tests/test_radar_pr_review_status.py",
    "tests/test_summarize_radar_pr.py",
    "tests/test_summarize_radar_report.py",
    "tests/test_validate_opportunity_radar_state.py",
    "tests/test_validate_radar_state.py",
]

REQUIRED_DIRS = [
    "reports",
    "opportunity-reports",
    "repositories",
    "opportunities",
    "patterns",
    "signals",
    "examples",
    "openspec",
    "tests",
    ".codex/skills",
    ".github/ISSUE_TEMPLATE",
]

ARCHITECTURE_WORKFLOW_NEEDLES = [
    "name: Architecture Radar",
    "workflow_dispatch:",
    "schedule:",
    "contents: write",
    "pull-requests: write",
    "OPENAI_API_KEY",
]

VALIDATION_WORKFLOW_NEEDLES = [
    "name: Radar Validation",
    "pull_request:",
    "contents: read",
    "openspec validate --all --strict --no-interactive",
]

OPPORTUNITY_WORKFLOW_NEEDLES = [
    "name: Opportunity Radar",
    "workflow_dispatch:",
    "contents: write",
    "pull-requests: write",
    "OPENAI_API_KEY",
    "scripts/run-codex-opportunity-radar.sh",
    "scripts/validate-opportunity-radar-state.py",
    "scripts/publish-opportunity-radar-run.sh",
]

OPPORTUNITY_WORKFLOW_FORBIDDEN = ["schedule:"]

REQUIRED_RELEASE = "v0.1.0"
REQUIRED_SECRET = "OPENAI_API_KEY"
REQUIRED_BRANCH = "main"
REQUIRED_STATUS_CHECK = "validate"


@dataclass(frozen=True)
class Check:
    id: str
    severity: str
    message: str
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "severity": self.severity,
            "message": self.message,
            "details": self.details,
        }


CommandRunner = Callable[[list[str], Path | None], subprocess.CompletedProcess[str]]
GhRunner = Callable[[list[str]], subprocess.CompletedProcess[str]]
Which = Callable[[str], str | None]


def make_check(
    check_id: str,
    severity: str,
    message: str,
    **details: Any,
) -> Check:
    if severity not in {"pass", "warn", "fail"}:
        raise ValueError(f"Unsupported severity: {severity}")
    return Check(check_id, severity, message, details)


def default_command_runner(
    args: list[str],
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        check=False,
    )


def default_gh_runner(args: list[str]) -> subprocess.CompletedProcess[str]:
    return default_command_runner(["gh", *args])


def load_json(text: str) -> Any:
    return json.loads(text)


def load_json_file(path: Path) -> tuple[Any | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except FileNotFoundError:
        return None, "file is missing"
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON: {exc}"


def check_required_paths(root: Path) -> list[Check]:
    checks: list[Check] = []
    for rel_path in REQUIRED_FILES:
        path = root / rel_path
        if path.is_file():
            checks.append(make_check(f"file:{rel_path}", "pass", f"found {rel_path}"))
        else:
            checks.append(
                make_check(
                    f"file:{rel_path}",
                    "fail",
                    f"missing {rel_path}; restore or create this required file",
                    remediation=f"Restore or create {rel_path}",
                )
            )

    for rel_path in REQUIRED_DIRS:
        path = root / rel_path
        if path.is_dir():
            checks.append(make_check(f"dir:{rel_path}", "pass", f"found {rel_path}"))
        else:
            checks.append(
                make_check(
                    f"dir:{rel_path}",
                    "fail",
                    f"missing {rel_path}; restore or create this required directory",
                    remediation=f"Restore or create {rel_path}",
                )
            )
    return checks


def check_radar_json(root: Path) -> list[Check]:
    path = root / "radar.json"
    data, error = load_json_file(path)
    if error:
        return [make_check("radar-json:parse", "fail", f"radar.json {error}; fix radar.json before running the workflow")]

    checks = [make_check("radar-json:parse", "pass", "radar.json parses")]
    if not isinstance(data, dict):
        checks.append(make_check("radar-json:shape", "fail", "radar.json must be an object; restore the expected schema"))
        return checks

    if "schema_version" in data:
        checks.append(make_check("radar-json:schema-version", "pass", "radar.json has schema_version"))
    else:
        checks.append(make_check("radar-json:schema-version", "fail", "radar.json is missing schema_version; restore the expected schema"))

    repositories = data.get("repositories")
    if isinstance(repositories, list):
        checks.append(make_check("radar-json:repositories", "pass", "radar.json has repositories list"))
    else:
        checks.append(make_check("radar-json:repositories", "fail", "radar.json repositories must be a list; restore the expected schema"))
    return checks


def check_opportunities_json(root: Path) -> list[Check]:
    path = root / "opportunities.json"
    data, error = load_json_file(path)
    if error:
        return [make_check("opportunities-json:parse", "fail", f"opportunities.json {error}; fix opportunities.json before running Opportunity Radar")]

    checks = [make_check("opportunities-json:parse", "pass", "opportunities.json parses")]
    if not isinstance(data, dict):
        checks.append(make_check("opportunities-json:shape", "fail", "opportunities.json must be an object; restore the expected schema"))
        return checks

    if data.get("schema_version") == 1:
        checks.append(make_check("opportunities-json:schema-version", "pass", "opportunities.json has schema_version 1"))
    else:
        checks.append(make_check("opportunities-json:schema-version", "fail", "opportunities.json schema_version must be 1"))

    for field in ("selected", "deferred", "watchlisted"):
        if isinstance(data.get(field), list):
            checks.append(make_check(f"opportunities-json:{field}", "pass", f"opportunities.json has {field} list"))
        else:
            checks.append(make_check(f"opportunities-json:{field}", "fail", f"opportunities.json {field} must be a list"))
    return checks


def check_workflow_text(root: Path) -> list[Check]:
    checks: list[Check] = []
    workflow_specs = [
        (
            "architecture-workflow",
            ".github/workflows/architecture-radar.yml",
            ARCHITECTURE_WORKFLOW_NEEDLES,
        ),
        (
            "validation-workflow",
            ".github/workflows/radar-validation.yml",
            VALIDATION_WORKFLOW_NEEDLES,
        ),
        (
            "opportunity-workflow",
            ".github/workflows/opportunity-radar.yml",
            OPPORTUNITY_WORKFLOW_NEEDLES,
        ),
    ]

    for check_prefix, rel_path, needles in workflow_specs:
        path = root / rel_path
        try:
            text = path.read_text(encoding="utf-8")
        except FileNotFoundError:
            checks.append(make_check(f"{check_prefix}:read", "fail", f"missing {rel_path}; restore the workflow file"))
            continue

        for needle in needles:
            if needle in text:
                checks.append(make_check(f"{check_prefix}:{needle}", "pass", f"{rel_path} contains {needle!r}"))
            else:
                checks.append(make_check(f"{check_prefix}:{needle}", "fail", f"{rel_path} is missing {needle!r}; update the workflow configuration"))

        if check_prefix == "opportunity-workflow":
            for forbidden in OPPORTUNITY_WORKFLOW_FORBIDDEN:
                if forbidden in text:
                    checks.append(make_check(f"{check_prefix}:no-{forbidden}", "fail", f"{rel_path} must remain manual-only and not contain {forbidden!r}"))
                else:
                    checks.append(make_check(f"{check_prefix}:no-{forbidden}", "pass", f"{rel_path} is manual-only with no {forbidden!r} trigger"))
    return checks


def check_open_spec_cli(
    root: Path,
    run_command: CommandRunner,
    which: Which,
) -> list[Check]:
    openspec_path = which("openspec")
    if not openspec_path:
        return [
            make_check(
                "openspec:cli",
                "warn",
                "openspec CLI is not installed; CI can still validate this if dependencies are installed there",
            )
        ]

    result = run_command(["openspec", "validate", "--all", "--strict", "--no-interactive"], root)
    if result.returncode == 0:
        return [
            make_check(
                "openspec:validate",
                "pass",
                "openspec validation passed",
                command="openspec validate --all --strict --no-interactive",
            )
        ]
    return [
        make_check(
            "openspec:validate",
            "fail",
            "openspec validation failed",
            command="openspec validate --all --strict --no-interactive",
            stderr=result.stderr.strip(),
            stdout=result.stdout.strip(),
        )
    ]


def local_checks(
    root: Path,
    run_command: CommandRunner = default_command_runner,
    which: Which = shutil.which,
) -> list[Check]:
    checks: list[Check] = []
    checks.extend(check_required_paths(root))
    checks.extend(check_radar_json(root))
    checks.extend(check_opportunities_json(root))
    checks.extend(check_workflow_text(root))
    checks.extend(check_open_spec_cli(root, run_command, which))
    return checks


def parse_gh_json(result: subprocess.CompletedProcess[str]) -> tuple[Any | None, str | None]:
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or f"gh exited with {result.returncode}"
        return None, message
    try:
        return load_json(result.stdout), None
    except json.JSONDecodeError as exc:
        return None, f"invalid gh JSON: {exc}"


def resolve_repo(repo: str | None, run_gh: GhRunner) -> tuple[str | None, Check]:
    if repo:
        return repo, make_check("github:repo", "pass", f"using repository {repo}", source="argument")

    result = run_gh(["repo", "view", "--json", "nameWithOwner"])
    data, error = parse_gh_json(result)
    if error:
        return None, make_check("github:repo", "warn", "could not resolve GitHub repository", error=error)

    name_with_owner = data.get("nameWithOwner") if isinstance(data, dict) else None
    if isinstance(name_with_owner, str) and "/" in name_with_owner:
        return name_with_owner, make_check("github:repo", "pass", f"resolved repository {name_with_owner}", source="gh repo view")

    return None, make_check("github:repo", "warn", "could not resolve GitHub repository from gh output")


def required_status_contexts(protection: dict[str, Any]) -> set[str]:
    status_checks = protection.get("required_status_checks")
    if not isinstance(status_checks, dict):
        return set()

    contexts = set()
    raw_contexts = status_checks.get("contexts")
    if isinstance(raw_contexts, list):
        contexts.update(context for context in raw_contexts if isinstance(context, str))

    raw_checks = status_checks.get("checks")
    if isinstance(raw_checks, list):
        for check in raw_checks:
            if isinstance(check, dict) and isinstance(check.get("context"), str):
                contexts.add(check["context"])
    return contexts


def github_checks(
    repo: str | None,
    run_gh: GhRunner = default_gh_runner,
    which: Which = shutil.which,
) -> list[Check]:
    checks: list[Check] = []
    if not which("gh"):
        return [
            make_check(
                "github:gh-cli",
                "warn",
                "gh CLI is not installed; remote repository checks were skipped",
            )
        ]

    auth = run_gh(["auth", "status"])
    if auth.returncode != 0:
        return [
            make_check(
                "github:auth",
                "warn",
                "gh is not authenticated; remote repository checks were skipped",
                stderr=auth.stderr.strip(),
            )
        ]
    checks.append(make_check("github:auth", "pass", "gh authentication is available"))

    resolved_repo, repo_check = resolve_repo(repo, run_gh)
    checks.append(repo_check)
    if not resolved_repo:
        return checks

    community = run_gh(["api", f"repos/{resolved_repo}/community/profile"])
    community_data, community_error = parse_gh_json(community)
    if community_error:
        checks.append(make_check("github:community-profile", "warn", "could not read GitHub community profile", error=community_error))
    elif isinstance(community_data, dict):
        health = community_data.get("health_percentage")
        severity = "pass" if isinstance(health, int) and health >= 100 else "warn"
        checks.append(
            make_check(
                "github:community-profile",
                severity,
                f"community profile health is {health}",
                health_percentage=health,
            )
        )

    secrets = run_gh(["secret", "list", "--repo", resolved_repo, "--json", "name"])
    secrets_data, secrets_error = parse_gh_json(secrets)
    if secrets_error:
        checks.append(make_check("github:secrets", "warn", "could not read repository secret metadata", error=secrets_error))
    elif isinstance(secrets_data, list):
        names = {item.get("name") for item in secrets_data if isinstance(item, dict)}
        if REQUIRED_SECRET in names:
            checks.append(make_check("github:secret:OPENAI_API_KEY", "pass", "OPENAI_API_KEY repository secret is configured"))
        else:
            checks.append(make_check("github:secret:OPENAI_API_KEY", "fail", "OPENAI_API_KEY repository secret is missing; add it under repository Actions secrets"))

    protection = run_gh(["api", f"repos/{resolved_repo}/branches/{REQUIRED_BRANCH}/protection"])
    protection_data, protection_error = parse_gh_json(protection)
    if protection_error:
        checks.append(
            make_check(
                "github:branch-protection",
                "fail",
                "main branch protection is not readable or not configured; protect main before relying on generated PRs",
                error=protection_error,
                remediation="Configure branch protection for main and require validate",
            )
        )
    elif isinstance(protection_data, dict):
        checks.append(make_check("github:branch-protection", "pass", "main branch protection is configured"))
        contexts = required_status_contexts(protection_data)
        if REQUIRED_STATUS_CHECK in contexts:
            checks.append(make_check("github:required-check:validate", "pass", "validate status check is required on main"))
        else:
            checks.append(
                make_check(
                    "github:required-check:validate",
                    "fail",
                    "main branch protection does not require validate; add validate as a required status check",
                    contexts=sorted(contexts),
                )
            )

    release = run_gh(["release", "view", REQUIRED_RELEASE, "--repo", resolved_repo, "--json", "tagName,isDraft,targetCommitish"])
    release_data, release_error = parse_gh_json(release)
    if release_error:
        checks.append(make_check("github:release:v0.1.0", "warn", "could not read v0.1.0 release", error=release_error))
    elif isinstance(release_data, dict):
        is_draft = release_data.get("isDraft")
        if release_data.get("tagName") == REQUIRED_RELEASE and is_draft is False:
            checks.append(make_check("github:release:v0.1.0", "pass", "v0.1.0 release exists and is published"))
        else:
            checks.append(make_check("github:release:v0.1.0", "warn", "v0.1.0 release exists but is not published as expected", release=release_data))

    for workflow in ("architecture-radar.yml", "opportunity-radar.yml", "radar-validation.yml"):
        result = run_gh(["workflow", "view", workflow, "--repo", resolved_repo])
        if result.returncode == 0:
            checks.append(make_check(f"github:workflow:{workflow}", "pass", f"{workflow} is visible on GitHub"))
        else:
            checks.append(
                make_check(
                    f"github:workflow:{workflow}",
                    "warn",
                    f"{workflow} is not visible through gh workflow view",
                    stderr=result.stderr.strip(),
                )
            )

    return checks


def run_checks(
    root: Path,
    repo: str | None = None,
    skip_github: bool = False,
    run_command: CommandRunner = default_command_runner,
    run_gh: GhRunner = default_gh_runner,
    which: Which = shutil.which,
) -> list[Check]:
    checks = local_checks(root, run_command=run_command, which=which)
    if skip_github:
        checks.append(make_check("github:skipped", "warn", "GitHub remote checks were skipped by --skip-github"))
    else:
        checks.extend(github_checks(repo=repo, run_gh=run_gh, which=which))
    return checks


def summarize(checks: list[Check]) -> dict[str, int]:
    return {
        "pass": sum(1 for check in checks if check.severity == "pass"),
        "warn": sum(1 for check in checks if check.severity == "warn"),
        "fail": sum(1 for check in checks if check.severity == "fail"),
    }


def payload(checks: list[Check]) -> dict[str, Any]:
    summary = summarize(checks)
    return {
        "ok": summary["fail"] == 0,
        "summary": summary,
        "checks": [check.to_dict() for check in checks],
    }


def exit_code(checks: list[Check]) -> int:
    return 1 if any(check.severity == "fail" for check in checks) else 0


def render_human(checks: list[Check]) -> str:
    lines = ["Architecture Radar setup doctor", ""]
    for check in checks:
        lines.append(f"{check.severity.upper():4} {check.id} - {check.message}")
    summary = summarize(checks)
    lines.extend(
        [
            "",
            f"Summary: {summary['pass']} pass, {summary['warn']} warn, {summary['fail']} fail",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check whether an Architecture Radar checkout is ready to run.")
    parser.add_argument("--root", default=".", help="Repository root to inspect. Defaults to the current directory.")
    parser.add_argument("--repo", help="GitHub repository in OWNER/REPO form. Defaults to gh repo view.")
    parser.add_argument("--skip-github", action="store_true", help="Skip remote GitHub checks.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    root = Path(args.root).resolve()
    checks = run_checks(root=root, repo=args.repo, skip_github=args.skip_github)
    if args.json:
        print(json.dumps(payload(checks), indent=2, sort_keys=True))
    else:
        print(render_human(checks))
    return exit_code(checks)


if __name__ == "__main__":
    raise SystemExit(main())
