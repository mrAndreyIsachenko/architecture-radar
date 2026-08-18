from __future__ import annotations

import importlib.util
import io
import json
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


LANGGRAPH_OPPORTUNITY = {
    "id": "langgraph-checkpoint-persistence-and-cost-diagnostics",
    "title": "LangGraph Checkpoint Persistence And Cost Diagnostics",
    "file": "opportunities/langgraph-checkpoint-persistence-and-cost-diagnostics.md",
    "stage": "watchlisted",
}


def complete_weekly_report(*, decisions: str | None = None, next_focus: str | None = None) -> str:
    sections = {
        "Week And Scope": "Synthesis for 2026-W33 from committed radar artifacts.",
        "Input Reports": "- `reports/2026-08-08.md`\n- `opportunity-reports/2026-08-09.md`",
        "Executive Synthesis": "Architecture evidence improved, while demand evidence remains early.",
        "Pattern Movement": "Evidence-carrying execution envelopes gained support.",
        "Topic Coverage": "AI and drones were represented; VPN demand remains thin.",
        "Repeated Candidates Or Signals": "LangGraph checkpoint pain repeated across reports.",
        "Decisions And Experiments": decisions or "Run one checkpoint-audit experiment before adding more builds.",
        "Evidence Gaps": "No direct procurement evidence was found for opportunity records.",
        "Next Week Focus": next_focus
        or "Focus on one LangGraph checkpoint audit CLI experiment tied to the existing opportunity record.",
    }

    body = ["# Weekly Synthesis: 2026-W33", ""]
    for heading, content in sections.items():
        body.extend([f"## {heading}", "", content, ""])
    return "\n".join(body)


def write_opportunities_state(
    root: Path,
    *,
    selected: list[dict[str, object]] | None = None,
    deferred: list[dict[str, object]] | None = None,
    watchlisted: list[dict[str, object]] | None = None,
) -> None:
    state = {
        "schema_version": 1,
        "generated_at": "2026-08-11",
        "selected": selected or [],
        "deferred": deferred or [],
        "watchlisted": watchlisted or [],
    }
    (root / "opportunities.json").write_text(json.dumps(state), encoding="utf-8")


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

    def test_weekly_report_rejects_absolute_runner_paths(self) -> None:
        bad_report = complete_weekly_report(
            next_focus=(
                "Reconcile [`repositories/example.md`]"
                "(/home/runner/work/architecture-radar/architecture-radar/repositories/example.md) "
                "before the next weekly report."
            )
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "weekly-reports" / "2026-W33.md"
            report.parent.mkdir()
            report.write_text(bad_report, encoding="utf-8")

            with patch.object(validator, "ROOT", root), patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
                validator.validate_weekly_report(report)

    def test_weekly_report_allows_repository_relative_links(self) -> None:
        report_text = complete_weekly_report(
            next_focus=(
                "Reconcile [`repositories/example.md`](repositories/example.md) "
                "with [`patterns/example.md`](patterns/example.md) before the next weekly report."
            )
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "weekly-reports" / "2026-W33.md"
            report.parent.mkdir()
            report.write_text(report_text, encoding="utf-8")

            with patch.object(validator, "ROOT", root):
                validator.validate_weekly_report(report)

    def test_weekly_report_rejects_active_watchlisted_opportunity_focus(self) -> None:
        bad_report = complete_weekly_report(
            decisions=(
                "Only the LangGraph line has enough evidence to justify active work, "
                "so keep it as the next opportunity experiment."
            ),
            next_focus=(
                "Build and run the LangGraph checkpoint audit path tied to "
                "`opportunities/langgraph-checkpoint-persistence-and-cost-diagnostics.md`."
            ),
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "weekly-reports" / "2026-W33.md"
            report.parent.mkdir()
            report.write_text(bad_report, encoding="utf-8")
            write_opportunities_state(root, watchlisted=[LANGGRAPH_OPPORTUNITY])

            with patch.object(validator, "ROOT", root), patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
                validator.validate_weekly_report(report)

    def test_weekly_report_allows_blocked_watchlisted_opportunity_mention(self) -> None:
        report_text = complete_weekly_report(
            decisions=(
                "LangGraph remains watchlisted; do not build until cross-company "
                "trace and storage evidence validates the paid wedge."
            ),
            next_focus=(
                "Use an architecture-only focus this week and keep LangGraph "
                "watchlisted pending validation before build work."
            ),
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "weekly-reports" / "2026-W33.md"
            report.parent.mkdir()
            report.write_text(report_text, encoding="utf-8")
            write_opportunities_state(root, watchlisted=[LANGGRAPH_OPPORTUNITY])

            with patch.object(validator, "ROOT", root):
                validator.validate_weekly_report(report)

    def test_weekly_report_allows_active_selected_opportunity_focus(self) -> None:
        report_text = complete_weekly_report(
            decisions="Run the LangGraph checkpoint audit as the selected opportunity experiment.",
            next_focus=(
                "Build and run the LangGraph checkpoint audit path tied to "
                "`opportunities/langgraph-checkpoint-persistence-and-cost-diagnostics.md`."
            ),
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "weekly-reports" / "2026-W33.md"
            report.parent.mkdir()
            report.write_text(report_text, encoding="utf-8")
            write_opportunities_state(root, selected=[{**LANGGRAPH_OPPORTUNITY, "stage": "selected"}])

            with patch.object(validator, "ROOT", root):
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
