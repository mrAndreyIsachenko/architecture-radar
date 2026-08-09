from __future__ import annotations

import importlib.util
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "radar-pr-review-status.py"

spec = importlib.util.spec_from_file_location("radar_pr_review_status", SCRIPT)
radar = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(radar)


def args(now: str, *, include_failed_log: bool = False) -> Namespace:
    return Namespace(
        repo="mrAndreyIsachenko/architecture-radar",
        workflow="architecture-radar.yml",
        timezone="Europe/Moscow",
        now=now,
        cadence_anchor="2026-08-02",
        cadence_days=3,
        schedule_hour_utc=5,
        limit=20,
        format="json",
        include_failed_log=include_failed_log,
    )


def run(
    *,
    database_id: int = 1,
    created_at: str = "2026-08-09T05:47:08Z",
    event: str = "schedule",
    status: str = "completed",
    conclusion: str = "success",
) -> dict[str, object]:
    return {
        "databaseId": database_id,
        "displayTitle": "Architecture Radar",
        "event": event,
        "status": status,
        "conclusion": conclusion,
        "createdAt": created_at,
        "updatedAt": created_at,
        "headBranch": "main",
        "url": f"https://github.com/example/actions/runs/{database_id}",
        "workflowName": "Architecture Radar",
    }


def pr(*, title: str = "Architecture Radar 2026-08-11", head: str = "architecture-radar/2026-08-11-42") -> dict[str, object]:
    return {
        "number": 42,
        "title": title,
        "url": "https://github.com/example/pull/42",
        "headRefName": head,
        "baseRefName": "main",
        "createdAt": "2026-08-11T06:00:00Z",
        "updatedAt": "2026-08-11T06:00:00Z",
        "isDraft": False,
        "mergeable": "MERGEABLE",
        "statusCheckRollup": [
            {
                "name": "validate",
                "status": "COMPLETED",
                "conclusion": "SUCCESS",
                "detailsUrl": "https://github.com/example/actions/runs/99",
                "workflowName": "Radar Validation",
            }
        ],
    }


class RadarPrReviewStatusTest(unittest.TestCase):
    def build(
        self,
        now: str,
        *,
        runs: list[dict[str, object]] | None = None,
        prs: list[dict[str, object]] | None = None,
        include_failed_log: bool = False,
        failed_excerpt: list[str] | None = None,
    ) -> dict[str, object]:
        with (
            patch.object(radar, "list_runs", return_value=runs or []),
            patch.object(radar, "list_prs", return_value=prs or []),
            patch.object(radar, "failed_log_excerpt", return_value=failed_excerpt or []),
        ):
            return radar.build_status(args(now, include_failed_log=include_failed_log))

    def test_radar_pr_detection_accepts_title_or_branch(self) -> None:
        self.assertTrue(radar.is_radar_pr(pr(title="Architecture Radar 2026-08-11", head="feature/other")))
        self.assertTrue(radar.is_radar_pr(pr(title="Maintenance", head="architecture-radar/2026-08-11-42")))
        self.assertFalse(radar.is_radar_pr(pr(title="Maintenance", head="feature/other")))

    def test_fresh_pr_wins_before_schedule_waiting_logic(self) -> None:
        status = self.build("2026-08-11T06:30:00Z", runs=[], prs=[pr()])

        self.assertEqual(status["status"], "fresh_pr")
        self.assertEqual(status["notification"], "REVIEW")
        self.assertEqual(len(status["fresh_prs"]), 1)

    def test_waits_before_due_time_on_cadence_day(self) -> None:
        status = self.build("2026-08-11T04:30:00Z")

        self.assertEqual(status["status"], "waiting")
        self.assertEqual(status["notification"], "DONT_NOTIFY")
        self.assertIn("not due", status["message"])

    def test_waits_after_due_time_when_schedule_run_is_missing(self) -> None:
        status = self.build("2026-08-11T06:30:00Z")

        self.assertEqual(status["status"], "waiting")
        self.assertEqual(status["notification"], "DONT_NOTIFY")
        self.assertIn("has not appeared", status["message"])

    def test_waits_when_today_schedule_run_is_in_progress(self) -> None:
        status = self.build(
            "2026-08-11T06:30:00Z",
            runs=[run(database_id=11, created_at="2026-08-11T05:10:00Z", status="in_progress", conclusion="")],
        )

        self.assertEqual(status["status"], "waiting")
        self.assertEqual(status["notification"], "DONT_NOTIFY")
        self.assertIn("queued or in progress", status["message"])

    def test_failed_latest_completed_run_is_reported(self) -> None:
        status = self.build(
            "2026-08-09T10:00:00Z",
            runs=[run(database_id=9, created_at="2026-08-09T05:10:00Z", conclusion="failure")],
            include_failed_log=True,
            failed_excerpt=["Process completed with exit code 2."],
        )

        self.assertEqual(status["status"], "failed_run")
        self.assertEqual(status["notification"], "REPORT")
        self.assertEqual(status["failed_log_excerpt"], ["Process completed with exit code 2."])

    def test_no_pr_after_successful_non_cadence_run(self) -> None:
        status = self.build(
            "2026-08-09T10:00:00Z",
            runs=[run(database_id=9, created_at="2026-08-09T05:47:08Z", conclusion="success")],
        )

        self.assertEqual(status["status"], "no_pr")
        self.assertEqual(status["notification"], "INFO")


if __name__ == "__main__":
    unittest.main()
