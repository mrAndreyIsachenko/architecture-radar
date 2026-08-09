from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "summarize-radar-pr.py"

spec = importlib.util.spec_from_file_location("summarize_radar_pr", SCRIPT)
summarizer = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(summarizer)


REPORT = """# Architecture Radar Report: 2026-08-11

## Candidate Counts

- `triaged`: 20
- `deeply-reviewed`: 1

Total candidates reaching at least `triaged`: 20.

## Selected Repositories

- `owner/repo` at `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`

## Executive Summary

- One useful finding.

## Extracted Or Updated Patterns

- Updated [Example](../patterns/example.md).

## Candidate Ledger

| Repository | URL | Commit | Discovery source | Family | Stage | Decision |
|---|---|---|---|---|---|---|
| `owner/repo` | https://github.com/owner/repo | `aaa` | search | `ai-llm-systems` | deeply-reviewed | selected |

## Recommended Next Action

Run one experiment.

## Unresolved Evidence Gaps

- Needs runtime validation.
"""


def pr_view() -> dict[str, object]:
    return {
        "number": 15,
        "title": "Architecture Radar 2026-08-11",
        "url": "https://github.com/example/pull/15",
        "headRefName": "architecture-radar/2026-08-11-42",
        "baseRefName": "main",
        "isDraft": False,
        "mergeable": "MERGEABLE",
        "statusCheckRollup": [
            {
                "name": "validate",
                "status": "COMPLETED",
                "conclusion": "SUCCESS",
                "detailsUrl": "https://github.com/example/actions/runs/1",
                "workflowName": "Radar Validation",
            }
        ],
        "files": [
            {"path": "reports/2026-08-11.md", "additions": 100, "deletions": 0, "changeType": "ADDED"},
            {"path": "repositories/owner-repo.md", "additions": 20, "deletions": 0, "changeType": "ADDED"},
            {"path": "patterns/example.md", "additions": 5, "deletions": 1, "changeType": "MODIFIED"},
            {"path": "radar.json", "additions": 10, "deletions": 2, "changeType": "MODIFIED"},
            {"path": "README.md", "additions": 1, "deletions": 0, "changeType": "MODIFIED"},
        ],
    }


class SummarizeRadarPrTest(unittest.TestCase):
    def test_changed_files_by_kind_groups_radar_artifacts(self) -> None:
        changed = summarizer.changed_files_by_kind(pr_view()["files"])

        self.assertEqual(changed["reports"], ["reports/2026-08-11.md"])
        self.assertEqual(changed["repositories"], ["repositories/owner-repo.md"])
        self.assertEqual(changed["patterns"], ["patterns/example.md"])
        self.assertEqual(changed["radar"], ["radar.json"])
        self.assertEqual(changed["readme"], ["README.md"])

    def test_summarize_pr_fetches_changed_report_from_head_branch(self) -> None:
        with (
            patch.object(summarizer, "pr_view", return_value=pr_view()),
            patch.object(summarizer, "fetch_file_text", return_value=REPORT) as fetch_file_text,
        ):
            summary = summarizer.summarize_pr("owner/repo", "15")

        fetch_file_text.assert_called_once_with("owner/repo", "architecture-radar/2026-08-11-42", "reports/2026-08-11.md")
        self.assertEqual(summary["number"], 15)
        self.assertEqual(summary["changed_files"]["reports"], ["reports/2026-08-11.md"])
        self.assertEqual(summary["reports"][0]["candidate_count"], 20)
        self.assertEqual(summary["reports"][0]["selected_repositories"], ["`owner/repo` at `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`"])

    def test_newest_open_radar_pr_selects_first_matching_pr(self) -> None:
        prs = [
            {"number": 1, "title": "Maintenance", "headRefName": "feature/x"},
            {"number": 2, "title": "Architecture Radar 2026-08-11", "headRefName": "architecture-radar/2026-08-11-42"},
        ]

        with patch.object(summarizer, "load_json_from_gh", return_value=prs):
            self.assertEqual(summarizer.newest_open_radar_pr("owner/repo"), "2")


if __name__ == "__main__":
    unittest.main()
