from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType
from typing import Any


def load_doctor() -> ModuleType:
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "check-radar-setup.py"
    spec = importlib.util.spec_from_file_location("check_radar_setup", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load check-radar-setup.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


doctor = load_doctor()


def completed(stdout: Any = "", stderr: str = "", returncode: int = 0) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args=[], returncode=returncode, stdout=json.dumps(stdout) if not isinstance(stdout, str) else stdout, stderr=stderr)


class SetupDoctorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        self.create_minimal_repo()

    def create_minimal_repo(self) -> None:
        for rel_path in doctor.REQUIRED_DIRS:
            (self.root / rel_path).mkdir(parents=True, exist_ok=True)

        content_by_path = {
            "radar.json": json.dumps({"schema_version": 1, "repositories": []}),
            "opportunities.json": json.dumps({"schema_version": 1, "selected": [], "deferred": [], "watchlisted": []}),
            ".github/workflows/architecture-radar.yml": "\n".join(
                [
                    "name: Architecture Radar",
                    "on:",
                    "  workflow_dispatch:",
                    "  schedule:",
                    "permissions:",
                    "  contents: write",
                    "  pull-requests: write",
                    "env:",
                    "  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}",
                ]
            ),
            ".github/workflows/radar-validation.yml": "\n".join(
                [
                    "name: Radar Validation",
                    "on:",
                    "  pull_request:",
                    "permissions:",
                    "  contents: read",
                    "jobs:",
                    "  validate:",
                    "    steps:",
                    "      - run: openspec validate --all --strict --no-interactive",
                ]
            ),
            ".github/workflows/generated-pr-validation.yml": "\n".join(
                [
                    "name: Generated PR Validation",
                    "on:",
                    "  workflow_run:",
                    "    workflows:",
                    "      - Architecture Radar",
                    "      - Opportunity Radar",
                    "      - Weekly Synthesis",
                    "permissions:",
                    "  checks: write",
                    "  pull-requests: read",
                    "steps:",
                    "  - run: scripts/mark-generated-pr-validation.py",
                ]
            ),
            ".github/workflows/opportunity-radar.yml": "\n".join(
                [
                    "name: Opportunity Radar",
                    "on:",
                    "  workflow_dispatch:",
                    "permissions:",
                    "  contents: write",
                    "  pull-requests: write",
                    "env:",
                    "  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}",
                    "steps:",
                    "  - run: scripts/run-codex-opportunity-radar.sh",
                    "  - run: scripts/validate-opportunity-radar-state.py",
                    "  - run: scripts/publish-opportunity-radar-run.sh",
                ]
            ),
            ".github/workflows/weekly-synthesis.yml": "\n".join(
                [
                    "name: Weekly Synthesis",
                    "on:",
                    "  workflow_dispatch:",
                    "  schedule:",
                    "permissions:",
                    "  contents: write",
                    "  pull-requests: write",
                    "env:",
                    "  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}",
                    "steps:",
                    "  - run: scripts/run-codex-weekly-synthesis.sh",
                    "  - run: scripts/validate-weekly-synthesis-state.py",
                    "  - run: scripts/publish-weekly-synthesis-run.sh",
                ]
            ),
        }
        for rel_path in doctor.REQUIRED_FILES:
            path = self.root / rel_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content_by_path.get(rel_path, f"# {rel_path}\n"), encoding="utf-8")

    def test_local_checks_pass_for_minimal_valid_tree(self) -> None:
        checks = doctor.local_checks(self.root, which=lambda name: None)
        failures = [check for check in checks if check.severity == "fail"]
        self.assertEqual([], failures)
        self.assertIn("warn", {check.severity for check in checks})

    def test_missing_required_file_is_failure(self) -> None:
        (self.root / "interests.md").unlink()
        checks = doctor.local_checks(self.root, which=lambda name: None)
        failures = [check.id for check in checks if check.severity == "fail"]
        self.assertIn("file:interests.md", failures)

    def test_invalid_radar_json_is_failure(self) -> None:
        (self.root / "radar.json").write_text("{nope", encoding="utf-8")
        checks = doctor.local_checks(self.root, which=lambda name: None)
        failures = [check.id for check in checks if check.severity == "fail"]
        self.assertIn("radar-json:parse", failures)

    def test_payload_and_exit_code_reflect_failures(self) -> None:
        checks = [
            doctor.Check("ok", "pass", "ok"),
            doctor.Check("warn", "warn", "warn"),
            doctor.Check("bad", "fail", "bad"),
        ]
        payload = doctor.payload(checks)
        self.assertFalse(payload["ok"])
        self.assertEqual({"pass": 1, "warn": 1, "fail": 1}, payload["summary"])
        self.assertEqual(1, doctor.exit_code(checks))

    def test_github_checks_pass_with_expected_remote_metadata(self) -> None:
        def run_gh(args: list[str]) -> subprocess.CompletedProcess[str]:
            if args == ["auth", "status"]:
                return completed("")
            if args == ["api", "repos/example/radar/community/profile"]:
                return completed({"health_percentage": 100})
            if args == ["secret", "list", "--repo", "example/radar", "--json", "name"]:
                return completed([{"name": "OPENAI_API_KEY"}])
            if args == ["api", "repos/example/radar/branches/main/protection"]:
                return completed({"required_status_checks": {"contexts": ["validate"]}})
            if args == ["release", "view", "v0.1.0", "--repo", "example/radar", "--json", "tagName,isDraft,targetCommitish"]:
                return completed({"tagName": "v0.1.0", "isDraft": False, "targetCommitish": "main"})
            if args in (
                ["workflow", "view", "architecture-radar.yml", "--repo", "example/radar"],
                ["workflow", "view", "generated-pr-validation.yml", "--repo", "example/radar"],
                ["workflow", "view", "opportunity-radar.yml", "--repo", "example/radar"],
                ["workflow", "view", "radar-validation.yml", "--repo", "example/radar"],
                ["workflow", "view", "weekly-synthesis.yml", "--repo", "example/radar"],
            ):
                return completed("")
            return completed(stderr=f"unexpected args: {args}", returncode=1)

        checks = doctor.github_checks("example/radar", run_gh=run_gh, which=lambda name: "/usr/bin/gh")
        failures = [check for check in checks if check.severity == "fail"]
        self.assertEqual([], failures)

    def test_github_checks_fail_when_secret_missing(self) -> None:
        def run_gh(args: list[str]) -> subprocess.CompletedProcess[str]:
            if args == ["auth", "status"]:
                return completed("")
            if args == ["api", "repos/example/radar/community/profile"]:
                return completed({"health_percentage": 100})
            if args == ["secret", "list", "--repo", "example/radar", "--json", "name"]:
                return completed([])
            if args == ["api", "repos/example/radar/branches/main/protection"]:
                return completed({"required_status_checks": {"contexts": ["validate"]}})
            if args == ["release", "view", "v0.1.0", "--repo", "example/radar", "--json", "tagName,isDraft,targetCommitish"]:
                return completed({"tagName": "v0.1.0", "isDraft": False, "targetCommitish": "main"})
            if args in (
                ["workflow", "view", "architecture-radar.yml", "--repo", "example/radar"],
                ["workflow", "view", "generated-pr-validation.yml", "--repo", "example/radar"],
                ["workflow", "view", "opportunity-radar.yml", "--repo", "example/radar"],
                ["workflow", "view", "radar-validation.yml", "--repo", "example/radar"],
                ["workflow", "view", "weekly-synthesis.yml", "--repo", "example/radar"],
            ):
                return completed("")
            return completed(stderr=f"unexpected args: {args}", returncode=1)

        checks = doctor.github_checks("example/radar", run_gh=run_gh, which=lambda name: "/usr/bin/gh")
        failures = [check.id for check in checks if check.severity == "fail"]
        self.assertIn("github:secret:OPENAI_API_KEY", failures)


if __name__ == "__main__":
    unittest.main()
