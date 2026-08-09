from __future__ import annotations

import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate-opportunity-radar-state.py"

spec = importlib.util.spec_from_file_location("validate_opportunity_radar_state", SCRIPT)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


def complete_report(selected: bool = True) -> str:
    selected_text = "- Agent trace debugging for small teams, backed by `M2 repeated pain`."
    reviews = "The opportunity has repeated public issue evidence. `M2 repeated pain`."
    if not selected:
        selected_text = "None."
        reviews = "No selected opportunities."

    sections = {
        "Prerequisites And State": "- workspace verified",
        "Signal Counts": "- `triaged`: 1",
        "Selected Opportunities": selected_text,
        "Executive Summary": "One demand signal was reviewed.",
        "Signal Ledger": "\n".join(
            [
                "| Source | URL | Family | Signal type | Evidence label | Decision | Reason |",
                "|---|---|---|---|---|---|---|",
                "| GitHub issue | https://example.com/issue | `ai-llm-demand` | `repeated-pain` | `M2 repeated pain` | selected | Repeated agent debugging pain. |",
            ]
        ),
        "Opportunity Reviews": reviews,
        "Recommended Next Test": "Interview three teams and offer a trace-debugging report.",
        "Rejected Or Deferred Signals": "- None.",
        "Evidence Gaps": "- No paid demand yet.",
    }

    body = ["# Opportunity Radar Report: 2026-08-11", ""]
    for heading, content in sections.items():
        body.extend([f"## {heading}", "", content, ""])
    return "\n".join(body)


def complete_opportunity() -> str:
    sections = {
        "Opportunity Summary": "Trace-backed debugging reports for small agent teams.",
        "Evidence": "- `M2 repeated pain`: repeated public issues about debugging failed agent runs.",
        "Repeated Pain Or Demand Signal": "Teams repeatedly ask how to inspect failed agent runs.",
        "Likely User Or Buyer": "Engineering teams deploying multi-step LLM agents.",
        "Current Workaround Or Money Signal": "Teams use ad hoc logs and manual trace reading.",
        "Proposed Offer": "A manual trace audit report for one failed workflow.",
        "Success Threshold": "Three teams agree to share traces or pay for an audit.",
        "Falsification Threshold": "Teams decline because existing tools already solve it.",
        "Evidence Gaps": "No direct paid demand signal yet.",
        "Decision": "selected for manual test",
    }
    body = ["# Agent Trace Debugging Opportunity", ""]
    for heading, content in sections.items():
        body.extend([f"## {heading}", "", content, ""])
    return "\n".join(body)


class ValidateOpportunityRadarStateTest(unittest.TestCase):
    def test_markdown_sections_extracts_h2_sections(self) -> None:
        sections = validator.markdown_sections("intro\n\n## First\n\nalpha\n\n## Second\n\nbeta\n")

        self.assertEqual(sections["First"], "alpha")
        self.assertEqual(sections["Second"], "beta")

    def test_signal_ledger_accepts_required_columns_and_labels(self) -> None:
        ledger = "\n".join(
            [
                "| Source | URL | Family | Signal type | Evidence label | Decision | Reason |",
                "|---|---|---|---|---|---|---|",
                "| GitHub issue | https://example.com | `ai-llm-demand` | `repeated-pain` | `M2 repeated pain` | selected | Repeated pain. |",
            ]
        )

        validator.validate_signal_ledger(ROOT / "opportunity-reports" / "test.md", ledger)

    def test_signal_ledger_rejects_unsupported_label(self) -> None:
        ledger = "\n".join(
            [
                "| Source | URL | Family | Signal type | Evidence label | Decision | Reason |",
                "|---|---|---|---|---|---|---|",
                "| GitHub issue | https://example.com | `ai-llm-demand` | `repeated-pain` | `E3 maintainer stated` | selected | Wrong label. |",
            ]
        )

        with patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
            validator.validate_signal_ledger(ROOT / "opportunity-reports" / "test.md", ledger)

    def test_report_structure_accepts_complete_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "opportunity-reports" / "2026-08-11.md"
            report.parent.mkdir()
            report.write_text(complete_report(), encoding="utf-8")

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "report_files_to_validate", return_value=[report]),
            ):
                validator.validate_report_structure()

    def test_report_structure_rejects_selected_without_market_evidence(self) -> None:
        bad_report = complete_report().replace("`M2 repeated pain`", "`H hypothesis`")
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "opportunity-reports" / "2026-08-11.md"
            report.parent.mkdir()
            report.write_text(bad_report, encoding="utf-8")

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "report_files_to_validate", return_value=[report]),
                patch("sys.stderr", io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                validator.validate_report_structure()

    def test_label_text_rejects_architecture_evidence_labels(self) -> None:
        with patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
            validator.validate_label_text(ROOT / "opportunity-reports" / "test.md", "Claim uses `E1 source verified`.")

    def test_selected_opportunity_file_requires_contract_and_market_label(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            opportunity = root / "opportunities" / "trace-debugging.md"
            opportunity.parent.mkdir()
            opportunity.write_text(complete_opportunity(), encoding="utf-8")

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "changed_opportunity_files", return_value=[opportunity]),
            ):
                validator.validate_selected_opportunity_files()

    def test_state_schema_accepts_empty_opportunities_list(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "opportunities.json").write_text(json.dumps({"schema_version": 1, "opportunities": []}), encoding="utf-8")

            with patch.object(validator, "ROOT", root):
                validator.validate_state()

    def test_watchlist_accepts_expected_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "opportunity-research-scope.md").write_text(
                "## Topic Families\n\n- `ai-llm-demand`\n",
                encoding="utf-8",
            )
            (root / "opportunity-watchlist.yml").write_text(
                "\n".join(
                    [
                        "entries:",
                        "  - source: GitHub issue",
                        "    url: https://example.com",
                        "    family: ai-llm-demand",
                        "    signal_type: repeated-pain",
                        "    priority: medium",
                        "    status: watch",
                        "    reason: Repeated pain around debugging agent traces in public issues.",
                    ]
                ),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root):
                validator.validate_watchlist()


if __name__ == "__main__":
    unittest.main()
