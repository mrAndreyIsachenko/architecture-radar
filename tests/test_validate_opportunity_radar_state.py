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
        "Paid Wedge": "Teams pay to reduce engineering time spent reconstructing failed agent runs.",
        "Distribution Channel": "A CLI installed from GitHub or PyPI and run locally against exported traces.",
        "Private Data Barrier": "public-only",
        "OSS Commoditization Risk": "medium",
        "Product Shape": "cli",
        "Pricing Hypothesis": "team",
        "Do Not Build Until": "Three teams agree to run the audit on real traces or one team asks for a paid follow-up.",
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

    def test_selected_opportunity_file_rejects_build_selection_with_unclear_wedge(self) -> None:
        text = complete_opportunity().replace(
            "Teams pay to reduce engineering time spent reconstructing failed agent runs.",
            "unclear",
        ).replace("selected for manual test", "selected for build")
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            opportunity = root / "opportunities" / "trace-debugging.md"
            opportunity.parent.mkdir()
            opportunity.write_text(text, encoding="utf-8")

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "changed_opportunity_files", return_value=[opportunity]),
                patch("sys.stderr", io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                validator.validate_selected_opportunity_files()

    def test_state_schema_accepts_empty_state_arrays(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "opportunity-research-scope.md").write_text(
                "## Topic Families\n\n- `ai-llm-demand`\n",
                encoding="utf-8",
            )
            (root / "opportunities.json").write_text(
                json.dumps({"schema_version": 1, "selected": [], "deferred": [], "watchlisted": []}),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root):
                validator.validate_state()

    def test_state_schema_accepts_selected_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "opportunity-research-scope.md").write_text(
                "## Topic Families\n\n- `ai-llm-demand`\n",
                encoding="utf-8",
            )
            (root / "opportunities.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "discovery_mode": "watchlist-directed",
                        "selected": [
                            {
                                "id": "agent-trace-debugging",
                                "family": "ai-llm-demand",
                                "stage": "selected-for-test",
                                "score": 7,
                                "confidence": "medium",
                                "money_signal": "weak",
                                "reachability": "high",
                                "evidence_count": 3,
                                "next_test": "Offer a manual trace debugging report to three agent teams.",
                                "paid_wedge": "Teams pay to reduce engineering time spent reconstructing failed agent runs.",
                                "distribution_channel": "A CLI installed from GitHub or PyPI and run locally against exported traces.",
                                "private_data_barrier": "public-only",
                                "oss_commoditization_risk": "medium",
                                "product_shape": "cli",
                                "pricing_hypothesis": "team",
                                "do_not_build_until": "Three teams agree to run the audit on real traces or one asks for a paid follow-up.",
                                "labels": ["M2", "M4"],
                            }
                        ],
                        "deferred": [],
                        "watchlisted": [],
                    }
                ),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root):
                validator.validate_state()

    def test_state_schema_rejects_selected_with_unclear_paid_wedge(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "opportunity-research-scope.md").write_text(
                "## Topic Families\n\n- `ai-llm-demand`\n",
                encoding="utf-8",
            )
            (root / "opportunities.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "discovery_mode": "watchlist-directed",
                        "selected": [
                            {
                                "id": "agent-trace-debugging",
                                "family": "ai-llm-demand",
                                "stage": "selected-for-test",
                                "score": 7,
                                "confidence": "medium",
                                "money_signal": "weak",
                                "reachability": "high",
                                "evidence_count": 3,
                                "next_test": "Offer a manual trace debugging report to three agent teams.",
                                "paid_wedge": "unclear",
                                "distribution_channel": "A CLI installed from GitHub or PyPI and run locally.",
                                "private_data_barrier": "public-only",
                                "oss_commoditization_risk": "medium",
                                "product_shape": "cli",
                                "pricing_hypothesis": "team",
                                "do_not_build_until": "Three teams agree to run the audit on real traces.",
                                "labels": ["M2", "M4"],
                            }
                        ],
                        "deferred": [],
                        "watchlisted": [],
                    }
                ),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root), patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
                validator.validate_state()

    def test_state_schema_allows_unclear_paid_wedge_on_watchlist(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "opportunity-research-scope.md").write_text(
                "## Topic Families\n\n- `ai-llm-demand`\n",
                encoding="utf-8",
            )
            (root / "opportunities.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "discovery_mode": "watchlist-directed",
                        "selected": [],
                        "deferred": [],
                        "watchlisted": [
                            {
                                "id": "agent-trace-debugging",
                                "family": "ai-llm-demand",
                                "stage": "watchlist",
                                "score": 5,
                                "confidence": "medium-low",
                                "money_signal": "none-found",
                                "reachability": "medium",
                                "evidence_count": 3,
                                "next_test": "Find direct evidence that teams pay for trace debugging.",
                                "paid_wedge": "unclear; no direct budget evidence yet",
                                "distribution_channel": "Likely local CLI or report, but the buying path is unproven.",
                                "private_data_barrier": "unclear",
                                "oss_commoditization_risk": "high",
                                "product_shape": "unclear",
                                "pricing_hypothesis": "unclear",
                                "do_not_build_until": "A team asks for a paid report or shares a budget-backed workflow.",
                                "labels": ["M2"],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root):
                validator.validate_state()

    def test_state_schema_rejects_missing_comparison_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs = root / "docs"
            docs.mkdir()
            (docs / "opportunity-research-scope.md").write_text(
                "## Topic Families\n\n- `ai-llm-demand`\n",
                encoding="utf-8",
            )
            (root / "opportunities.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "discovery_mode": "watchlist-directed",
                        "selected": [
                            {
                                "id": "agent-trace-debugging",
                                "family": "ai-llm-demand",
                                "status": "selected",
                                "labels": ["M2", "M4"],
                            }
                        ],
                        "deferred": [],
                        "watchlisted": [],
                    }
                ),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root), patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
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
