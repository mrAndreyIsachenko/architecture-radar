from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "summarize-radar-report.py"

spec = importlib.util.spec_from_file_location("summarize_radar_report", SCRIPT)
summarizer = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(summarizer)


REPORT = """# Architecture Radar Report: 2026-08-11

## Candidate Counts

Highest stage reached:

- `triaged`: 20
- `source-inspected`: 4
- `deeply-reviewed`: 2

Total candidates reaching at least `triaged`: 20.

## Selected Repositories

- `owner/alpha` at `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`
- `owner/beta` at `bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb`

## Executive Summary

- Alpha contributes one reusable mechanism.
- Beta contributes another reusable mechanism.

## Extracted Or Updated Patterns

- Updated [Example Pattern](../patterns/example-pattern.md).

## Candidate Ledger

| Repository | URL | Commit | Discovery source | Family | Stage | Decision |
|---|---|---|---|---|---|---|
| `owner/alpha` | https://github.com/owner/alpha | `aaa` | search | `ai-llm-systems` | deeply-reviewed | selected |
| `owner/beta` | https://github.com/owner/beta | `bbb` | watchlist | `blockchain-intelligence` | deeply-reviewed | selected |

## Recommended Next Action

Run one bounded experiment.

## Unresolved Evidence Gaps

- No local test suite was run.
- Runtime validation is still missing.
"""


class SummarizeRadarReportTest(unittest.TestCase):
    def test_parse_candidate_counts(self) -> None:
        counts = summarizer.parse_candidate_counts(
            "- `triaged`: 20\n- `deeply-reviewed`: 2\n\nTotal candidates reaching at least `triaged`: 20."
        )

        self.assertEqual(counts["total_triaged"], 20)
        self.assertEqual(counts["stage_counts"]["deeply-reviewed"], 2)

    def test_parse_candidate_ledger_table(self) -> None:
        rows = summarizer.parse_table(
            "| Repository | URL | Decision |\n"
            "|---|---|---|\n"
            "| `owner/repo` | https://github.com/owner/repo | selected |\n"
        )

        self.assertEqual(rows[0]["Repository"], "`owner/repo`")
        self.assertEqual(rows[0]["Decision"], "selected")

    def test_summarize_report_extracts_review_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "2026-08-11.md"
            path.write_text(REPORT, encoding="utf-8")

            summary = summarizer.summarize_report(path)

        self.assertEqual(summary["candidate_count"], 20)
        self.assertEqual(summary["ledger_rows"], 2)
        self.assertEqual(summary["stage_counts"]["source-inspected"], 4)
        self.assertEqual(len(summary["selected_repositories"]), 2)
        self.assertEqual(summary["updated_patterns"], ["Updated [Example Pattern](../patterns/example-pattern.md)."])
        self.assertEqual(summary["recommended_next_action"], "Run one bounded experiment.")
        self.assertEqual(len(summary["evidence_gaps"]), 2)


if __name__ == "__main__":
    unittest.main()
