from __future__ import annotations

import importlib.util
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-weekly-synthesis-state.py"

spec = importlib.util.spec_from_file_location("validate_weekly_synthesis_state", SCRIPT)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


def complete_weekly_report() -> str:
    sections = {
        "Week And Scope": "Synthesis for 2026-W33 from committed radar artifacts.",
        "Input Reports": "- `reports/2026-08-08.md`\n- `opportunity-reports/2026-08-09.md`",
        "Executive Synthesis": "Architecture evidence improved, while demand evidence remains early.",
        "Pattern Movement": "Evidence-carrying execution envelopes gained support.",
        "Topic Coverage": "AI and drones were represented; VPN demand remains thin.",
        "Repeated Candidates Or Signals": "LangGraph checkpoint pain repeated across reports.",
        "Decisions And Experiments": "Run one checkpoint-audit experiment before adding more builds.",
        "Evidence Gaps": "No direct procurement evidence was found for opportunity records.",
        "Next Week Focus": "Focus on one LangGraph checkpoint audit CLI experiment tied to the existing opportunity record.",
    }

    body = ["# Weekly Synthesis: 2026-W33", ""]
    for heading, content in sections.items():
        body.extend([f"## {heading}", "", content, ""])
    return "\n".join(body)


class ValidateWeeklySynthesisStateTest(unittest.TestCase):
    def test_markdown_sections_extracts_h2_sections(self) -> None:
        sections = validator.markdown_sections("intro\n\n## First\n\nalpha\n\n## Second\n\nbeta\n")

        self.assertEqual(sections["First"], "alpha")
        self.assertEqual(sections["Second"], "beta")

    def test_weekly_report_accepts_required_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "weekly-reports" / "2026-W33.md"
            report.parent.mkdir()
            report.write_text(complete_weekly_report(), encoding="utf-8")

            with patch.object(validator, "ROOT", root):
                validator.validate_weekly_report(report)

    def test_weekly_report_rejects_missing_input_report_path(self) -> None:
        bad_report = complete_weekly_report().replace("`reports/2026-08-08.md`", "`notes/2026-08-08.md`")
        bad_report = bad_report.replace("`opportunity-reports/2026-08-09.md`", "`notes/opportunity.md`")

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "weekly-reports" / "2026-W33.md"
            report.parent.mkdir()
            report.write_text(bad_report, encoding="utf-8")

            with patch.object(validator, "ROOT", root), patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
                validator.validate_weekly_report(report)

    def test_weekly_reports_to_validate_accepts_iso_week(self) -> None:
        with patch.object(validator, "WEEK_ID", "2026-W33"), patch.object(validator, "changed_weekly_files", return_value=[]):
            reports = validator.weekly_reports_to_validate()

        self.assertEqual([ROOT / "weekly-reports" / "2026-W33.md"], reports)

    def test_weekly_reports_to_validate_rejects_bad_week_id(self) -> None:
        with (
            patch.object(validator, "WEEK_ID", "2026-08-09"),
            patch.object(validator, "changed_weekly_files", return_value=[]),
            patch("sys.stderr", io.StringIO()),
            self.assertRaises(SystemExit),
        ):
            validator.weekly_reports_to_validate()


if __name__ == "__main__":
    unittest.main()
