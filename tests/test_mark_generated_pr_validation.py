from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
import unittest
from pathlib import Path
from types import ModuleType
from typing import Any
from unittest.mock import patch


def load_marker() -> ModuleType:
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "mark-generated-pr-validation.py"
    spec = importlib.util.spec_from_file_location("mark_generated_pr_validation", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load mark-generated-pr-validation.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


marker = load_marker()


def completed(stdout: Any = "", stderr: str = "", returncode: int = 0) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(
        args=[],
        returncode=returncode,
        stdout=json.dumps(stdout) if not isinstance(stdout, str) else stdout,
        stderr=stderr,
    )


class GeneratedPrValidationMarkerTest(unittest.TestCase):
    def test_generated_pr_matching_uses_workflow_prefix_title_and_run_number(self) -> None:
        pr = {
            "number": 32,
            "title": "Weekly Synthesis 2026-W32",
            "url": "https://example.com/pr/32",
            "headRefName": "weekly-synthesis/2026-W32-2",
            "headRefOid": "abc123",
        }

        self.assertTrue(marker.is_generated_pr(pr, "Weekly Synthesis", 2))
        self.assertFalse(marker.is_generated_pr(pr, "Weekly Synthesis", 1))
        self.assertFalse(marker.is_generated_pr(pr, "Architecture Radar", 2))

    def test_check_run_payload_uses_required_validate_name(self) -> None:
        pr = marker.GeneratedPr(
            number=32,
            title="Weekly Synthesis 2026-W32",
            url="https://example.com/pr/32",
            head_ref_name="weekly-synthesis/2026-W32-2",
            head_ref_oid="abc123",
        )

        payload = marker.check_run_payload(pr, "Weekly Synthesis", 2, "https://example.com/run")

        self.assertEqual("validate", payload["name"])
        self.assertEqual("abc123", payload["head_sha"])
        self.assertEqual("completed", payload["status"])
        self.assertEqual("success", payload["conclusion"])
        self.assertEqual("https://example.com/run", payload["details_url"])

    def test_mark_generated_prs_creates_check_run_for_matching_pr(self) -> None:
        calls: list[tuple[list[str], str | None]] = []

        def fake_gh(args: list[str], stdin: str | None = None) -> subprocess.CompletedProcess[str]:
            calls.append((args, stdin))
            if args[:3] == ["pr", "list", "--repo"]:
                self.assertIn("100", args)
                return completed(
                    [
                        {
                            "number": 32,
                            "title": "Weekly Synthesis 2026-W32",
                            "url": "https://example.com/pr/32",
                            "headRefName": "weekly-synthesis/2026-W32-2",
                            "headRefOid": "abc123",
                        },
                        {
                            "number": 99,
                            "title": "Weekly Synthesis 2026-W31",
                            "url": "https://example.com/pr/99",
                            "headRefName": "weekly-synthesis/2026-W31-1",
                            "headRefOid": "def456",
                        },
                    ]
                )
            if args[:2] == ["api", "repos/example/radar/check-runs"]:
                return completed({"id": 123})
            return completed(stderr=f"unexpected args: {args}", returncode=1)

        with patch("sys.stdout", io.StringIO()):
            matched = marker.mark_generated_prs("example/radar", "Weekly Synthesis", 2, "https://example.com/run", gh=fake_gh)

        self.assertEqual([32], [pr.number for pr in matched])
        check_calls = [call for call in calls if call[0][:2] == ["api", "repos/example/radar/check-runs"]]
        self.assertEqual(1, len(check_calls))
        payload = json.loads(check_calls[0][1] or "{}")
        self.assertEqual("validate", payload["name"])
        self.assertEqual("abc123", payload["head_sha"])

    def test_mark_generated_prs_noops_when_no_pr_matches(self) -> None:
        def fake_gh(args: list[str], stdin: str | None = None) -> subprocess.CompletedProcess[str]:
            if args[:3] == ["pr", "list", "--repo"]:
                return completed([])
            return completed(stderr=f"unexpected args: {args}", returncode=1)

        with patch("sys.stdout", io.StringIO()):
            matched = marker.mark_generated_prs("example/radar", "Weekly Synthesis", 2, "https://example.com/run", gh=fake_gh)

        self.assertEqual([], matched)


if __name__ == "__main__":
    unittest.main()
