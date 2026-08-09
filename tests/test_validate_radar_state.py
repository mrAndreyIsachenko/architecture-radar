from __future__ import annotations

import importlib.util
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-radar-state.py"

spec = importlib.util.spec_from_file_location("validate_radar_state", SCRIPT)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


def complete_report() -> str:
    sections = {
        "Prerequisites And State": "- workspace verified",
        "Candidate Counts": "- `triaged`: 1",
        "Selected Repositories": "- `owner/repo` at `0123456789abcdef`",
        "Executive Summary": "One useful mechanism was reviewed.",
        "Detailed Reviews": "- [owner/repo](../repositories/owner-repo.md)",
        "Extracted Or Updated Patterns": "- None.",
        "Relevance To Explicit Problems In `interests.md`": "- `ai-llm-systems`: context construction.",
        "Candidate Ledger": "\n".join(
            [
                "| Repository | URL | Commit | Discovery source | Family | Stage | Decision |",
                "|---|---|---|---|---|---|---|",
                "| `owner/repo` | https://github.com/owner/repo | `0123456789abcdef` | test | `ai-llm-systems` | triaged | selected |",
            ]
        ),
        "Recommended Next Action": "Run one bounded experiment.",
        "Notable Rejected Or Deferred Candidates": "- None.",
        "Unresolved Evidence Gaps": "- No local test suite was run.",
    }

    body = ["# Architecture Radar Report: 2026-08-11", ""]
    for heading, content in sections.items():
        body.extend([f"## {heading}", "", content, ""])
    return "\n".join(body)


class ValidateRadarStateTest(unittest.TestCase):
    def test_markdown_sections_extracts_h2_sections(self) -> None:
        sections = validator.markdown_sections("intro\n\n## First\n\nalpha\n\n## Second\n\nbeta\n")

        self.assertEqual(sections["First"], "alpha")
        self.assertEqual(sections["Second"], "beta")

    def test_candidate_ledger_accepts_required_columns(self) -> None:
        ledger = "\n".join(
            [
                "| Repository | URL | Commit | Discovery source | Family | Stage | Decision |",
                "|---|---|---|---|---|---|---|",
                "| `owner/repo` | https://github.com/owner/repo | `abc` | search | `ai-llm-systems` | triaged | selected |",
            ]
        )

        validator.validate_candidate_ledger(ROOT / "reports" / "test.md", ledger)

    def test_candidate_ledger_rejects_missing_required_columns(self) -> None:
        ledger = "\n".join(
            [
                "| Repository | URL | Commit | Stage | Decision |",
                "|---|---|---|---|---|",
                "| `owner/repo` | https://github.com/owner/repo | `abc` | triaged | selected |",
            ]
        )

        with patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
            validator.validate_candidate_ledger(ROOT / "reports" / "test.md", ledger)

    def test_report_structure_accepts_complete_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "reports" / "2026-08-11.md"
            report.parent.mkdir()
            report.write_text(complete_report(), encoding="utf-8")

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "report_files_to_validate", return_value=[report]),
            ):
                validator.validate_report_structure()

    def test_report_structure_rejects_missing_required_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "reports" / "2026-08-11.md"
            report.parent.mkdir()
            report.write_text(complete_report().replace("## Candidate Ledger", "## Ledger"), encoding="utf-8")

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "report_files_to_validate", return_value=[report]),
                patch("sys.stderr", io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                validator.validate_report_structure()


if __name__ == "__main__":
    unittest.main()
