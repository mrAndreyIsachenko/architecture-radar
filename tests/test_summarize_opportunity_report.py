from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "summarize-opportunity-report.py"

spec = importlib.util.spec_from_file_location("summarize_opportunity_report", SCRIPT)
summarizer = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(summarizer)


REPORT = """# Opportunity Radar Report 2026-08-11

## Prerequisites And State
- Reviewed public signals: 16.
- Selected opportunities: 1 sell-before-build, 0 selected-for-build, 2 watchlisted.

## Signal Counts
- Discovered: 16
- Triaged: 16
- Corroborated: 10
- Sell-before-build: 1
- Watchlisted: 2

## Selected Opportunities
- M1 paid demand: LangGraph Checkpoint Persistence And Cost Diagnostics.

## Executive Summary
- The strongest near-term money path is a paid checkpoint audit.

## Signal Ledger
| Source | URL | Family | Signal type | Evidence label | Stage | Decision | Reason |
|---|---|---|---|---|---|---|---|
| LangGraph #7417 | https://github.com/langchain-ai/langgraph/issues/7417 | ai-llm-demand | operational-risk | `M2 repeated pain` | corroborated | corroborated | Duplicate work. |

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
- Success threshold: one paid pilot.

## Evidence Gaps
- LangGraph still lacks direct proof that teams will pay.
"""


class SummarizeOpportunityReportTest(unittest.TestCase):
    def test_summarize_report_text_extracts_opportunity_fields(self) -> None:
        summary = summarizer.summarize_report_text(REPORT, "opportunity-reports/2026-08-11.md")

        self.assertEqual(summary["reviewed_signals"], 16)
        self.assertEqual(summary["ledger_rows"], 1)
        self.assertEqual(summary["signal_counts"]["Triaged"], 16)
        self.assertEqual(
            summary["selected_opportunities"],
            ["M1 paid demand: LangGraph Checkpoint Persistence And Cost Diagnostics."],
        )
        self.assertEqual(summary["build_readiness"][0]["Build decision"], "sell-before-build")
        self.assertEqual(summary["money_readiness"][0]["Stage"], "sell-before-build")
        self.assertIn("paid LangGraph checkpoint audit", summary["recommended_next_test"])
        self.assertEqual(summary["evidence_gaps"], ["LangGraph still lacks direct proof that teams will pay."])


if __name__ == "__main__":
    unittest.main()
