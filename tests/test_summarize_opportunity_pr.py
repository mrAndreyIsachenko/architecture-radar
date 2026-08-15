from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "summarize-opportunity-pr.py"

spec = importlib.util.spec_from_file_location("summarize_opportunity_pr", SCRIPT)
summarizer = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(summarizer)


REPORT = """# Opportunity Radar Report 2026-08-11

## Prerequisites And State
- Reviewed public signals: 16.

## Signal Ledger
| Source | URL | Family | Signal type | Evidence label | Stage | Decision | Reason |
|---|---|---|---|---|---|---|---|
| LangGraph #7417 | https://github.com/langchain-ai/langgraph/issues/7417 | ai-llm-demand | operational-risk | `M2 repeated pain` | corroborated | corroborated | Duplicate work. |

## Selected Opportunities
- M1 paid demand: LangGraph Checkpoint Persistence And Cost Diagnostics.

## Build Readiness
| Opportunity | Paid wedge | Distribution channel | Private data barrier | OSS commoditization risk | Product shape | Pricing hypothesis | Do not build until | Build decision |
|---|---|---|---|---|---|---|---|---|
| LangGraph Checkpoint Persistence And Cost Diagnostics | Reduce engineering time. | Landing page. | public-only | medium | report | team | One paid pilot. | sell-before-build |

## Money Readiness
| Opportunity | Pain | Spend | Reachability | Timing | Buildability | Buyer | Existing spend | Paid experiment | Source classes | Stage |
|---|---|---|---|---|---|---|---|---|---|---|
| LangGraph Checkpoint Persistence And Cost Diagnostics | 5 | 3 | 4 | 4 | 4 | Agent platform teams. | Hiring. | Sell an audit. | github, docs, job | sell-before-build |

## Recommended Next Test
- Offer a paid LangGraph checkpoint audit first.

## Evidence Gaps
- Direct willingness to pay is not proven.
"""


def pr_view() -> dict[str, object]:
    return {
        "number": 50,
        "title": "Opportunity Radar 2026-08-11",
        "url": "https://github.com/example/pull/50",
        "headRefName": "opportunity-radar/2026-08-11-42",
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
            {"path": "opportunity-reports/2026-08-11.md", "additions": 100, "deletions": 0, "changeType": "ADDED"},
            {"path": "opportunities/langgraph-checkpoint-persistence-and-cost-diagnostics.md", "additions": 30, "deletions": 0, "changeType": "ADDED"},
            {"path": "signals/2026-08-11-langgraph-signals.md", "additions": 20, "deletions": 0, "changeType": "ADDED"},
            {"path": "opportunities.json", "additions": 10, "deletions": 2, "changeType": "MODIFIED"},
        ],
    }


class SummarizeOpportunityPrTest(unittest.TestCase):
    def test_changed_files_by_kind_groups_opportunity_artifacts(self) -> None:
        changed = summarizer.changed_files_by_kind(pr_view()["files"])

        self.assertEqual(changed["opportunity_reports"], ["opportunity-reports/2026-08-11.md"])
        self.assertEqual(
            changed["opportunities"],
            ["opportunities/langgraph-checkpoint-persistence-and-cost-diagnostics.md"],
        )
        self.assertEqual(changed["signals"], ["signals/2026-08-11-langgraph-signals.md"])
        self.assertEqual(changed["opportunities_state"], ["opportunities.json"])

    def test_summarize_pr_fetches_changed_opportunity_report_from_head_branch(self) -> None:
        with (
            patch.object(summarizer, "pr_view", return_value=pr_view()),
            patch.object(summarizer, "fetch_file_text", return_value=REPORT) as fetch_file_text,
        ):
            summary = summarizer.summarize_pr("owner/repo", "50")

        fetch_file_text.assert_called_once_with(
            "owner/repo",
            "opportunity-radar/2026-08-11-42",
            "opportunity-reports/2026-08-11.md",
        )
        self.assertEqual(summary["number"], 50)
        self.assertEqual(summary["radar"], "opportunity")
        self.assertEqual(summary["reports"][0]["reviewed_signals"], 16)
        self.assertEqual(summary["review_recommendation"]["decision"], "looks_mergeable")

    def test_newest_open_opportunity_pr_selects_first_matching_pr(self) -> None:
        prs = [
            {"number": 1, "title": "Maintenance", "headRefName": "feature/x"},
            {"number": 2, "title": "Opportunity Radar 2026-08-11", "headRefName": "opportunity-radar/2026-08-11-42"},
        ]

        with patch.object(summarizer, "load_json_from_gh", return_value=prs):
            self.assertEqual(summarizer.newest_open_opportunity_pr("owner/repo"), "2")


if __name__ == "__main__":
    unittest.main()
