from __future__ import annotations

import importlib.util
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "radar-pr-review.py"

spec = importlib.util.spec_from_file_location("radar_pr_review", SCRIPT)
reviewer = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(reviewer)


def args() -> Namespace:
    return Namespace(
        repo="mrAndreyIsachenko/architecture-radar",
        radar="all",
        workflow=None,
        timezone="Europe/Moscow",
        now="2026-08-11T06:30:00Z",
        cadence_anchor="2026-08-02",
        cadence_days=3,
        schedule_hour_utc=5,
        schedule_minute_utc=0,
        limit=20,
        include_failed_log=True,
        format="json",
    )


class RadarPrReviewTest(unittest.TestCase):
    def test_build_review_returns_waiting_status_without_pr_overview(self) -> None:
        status = {
            "status": "waiting",
            "notification": "DONT_NOTIFY",
            "message": "Today's scheduled cadence run has not appeared yet.",
        }

        with patch.object(reviewer.status_helper, "build_status", return_value=status):
            review = reviewer.build_review(args())

        self.assertEqual(review["status"], status)
        self.assertEqual(review["pr_overviews"], [])

    def test_build_review_summarizes_every_fresh_pr(self) -> None:
        status = {
            "status": "fresh_pr",
            "notification": "REVIEW",
            "message": "Fresh Architecture Radar PR found.",
            "fresh_prs": [
                {"number": 21, "title": "Architecture Radar 2026-08-11"},
                {"number": 22, "title": "Architecture Radar 2026-08-11 supplement"},
            ],
        }
        summary = {"number": 21, "reports": []}

        with (
            patch.object(reviewer.status_helper, "build_status", return_value=status),
            patch.object(reviewer.pr_summary_helper, "summarize_pr", return_value=summary) as summarize_pr,
        ):
            review = reviewer.build_review(args())

        self.assertEqual(len(review["pr_overviews"]), 2)
        summarize_pr.assert_any_call("mrAndreyIsachenko/architecture-radar", "21")
        summarize_pr.assert_any_call("mrAndreyIsachenko/architecture-radar", "22")

    def test_build_review_routes_opportunity_pr_to_opportunity_summarizer(self) -> None:
        status = {
            "status": "fresh_pr",
            "notification": "REVIEW",
            "message": "Fresh generated radar PR found.",
            "fresh_prs": [
                {"number": 51, "title": "Opportunity Radar 2026-08-11", "radar": "opportunity"},
            ],
        }
        summary = {"number": 51, "radar": "opportunity", "reports": []}

        with (
            patch.object(reviewer.status_helper, "build_status", return_value=status),
            patch.object(reviewer.opportunity_pr_summary_helper, "summarize_pr", return_value=summary) as summarize_pr,
        ):
            review = reviewer.build_review(args())

        self.assertEqual(review["pr_overviews"], [summary])
        summarize_pr.assert_called_once_with("mrAndreyIsachenko/architecture-radar", "51")

    def test_status_args_maps_cli_options_for_status_helper(self) -> None:
        mapped = reviewer.status_args(args())

        self.assertEqual(mapped.repo, "mrAndreyIsachenko/architecture-radar")
        self.assertEqual(mapped.radar, "all")
        self.assertIsNone(mapped.workflow)
        self.assertTrue(mapped.include_failed_log)
        self.assertEqual(mapped.format, "json")


if __name__ == "__main__":
    unittest.main()
