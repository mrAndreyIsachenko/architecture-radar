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
        "Review Value": "\n".join(
            [
                "| Verdict | Score | Reason | Recommended action |",
                "|---|---:|---|---|",
                "| `useful-delta` | 4 | One reviewed repository adds a source-backed reusable mechanism. | `merge` |",
            ]
        ),
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
        "Validation Backlog Updates": "No validation backlog update required.",
    }

    body = ["# Architecture Radar Report: 2026-08-11", ""]
    for heading, content in sections.items():
        body.extend([f"## {heading}", "", content, ""])
    return "\n".join(body)


def write_research_scope(root: Path, families: list[str] | None = None) -> None:
    families = families or ["ai-llm-systems"]
    docs = root / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "research-scope.md").write_text(
        "## Topic Families\n\n" + "\n".join(f"- `{family}`" for family in families) + "\n",
        encoding="utf-8",
    )


def write_interests(root: Path, families: list[str] | None = None) -> None:
    families = families or ["ai-llm-systems"]
    lines = [
        "# Interests",
        "",
        "Use these top-level topic families for candidate accounting and per-topic selection:",
        "",
    ]
    lines.extend(f"- `{family}`: test family." for family in families)
    lines.extend(["", "## Current Priorities", "", "Test priorities."])
    (root / "interests.md").write_text("\n".join(lines), encoding="utf-8")


def write_family_playbook(root: Path, family: str, *, omit_heading: str | None = None) -> None:
    playbooks = root / "docs" / "family-playbooks"
    playbooks.mkdir(parents=True, exist_ok=True)
    headings = [
        "Family",
        "Mechanisms To Search",
        "Evidence Bar",
        "Selection Bias",
        "Rejection Triggers",
        "Validation Evidence",
        "Useful Search Seeds",
    ]
    body: list[str] = [f"# {family} Playbook", ""]
    for heading in headings:
        if heading == omit_heading:
            continue
        body.extend([f"## {heading}", "", f"`{family}`" if heading == "Family" else "Test content.", ""])
    (playbooks / f"{family}.md").write_text("\n".join(body), encoding="utf-8")


def write_backlog(root: Path, text: str) -> None:
    experiments = root / "experiments"
    experiments.mkdir(exist_ok=True)
    (experiments / "failure-injection-backlog.yml").write_text(text, encoding="utf-8")


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

    def test_report_structure_rejects_missing_review_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "reports" / "2026-08-11.md"
            report.parent.mkdir()
            report.write_text(complete_report().replace("## Review Value", "## Value"), encoding="utf-8")

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "report_files_to_validate", return_value=[report]),
                patch("sys.stderr", io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                validator.validate_report_structure()

    def test_report_structure_rejects_low_value_merge(self) -> None:
        report_text = complete_report().replace("`useful-delta` | 4", "`stale-or-duplicate` | 1")
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "reports" / "2026-08-11.md"
            report.parent.mkdir()
            report.write_text(report_text, encoding="utf-8")

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "report_files_to_validate", return_value=[report]),
                patch("sys.stderr", io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                validator.validate_report_structure()

    def test_report_structure_rejects_runtime_gap_without_backlog_item(self) -> None:
        report_text = complete_report().replace(
            "No validation backlog update required.",
            "No validation backlog update required.",
        ).replace("- No local test suite was run.", "- Needs runtime validation after restart.")
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "reports" / "2026-08-11.md"
            report.parent.mkdir()
            report.write_text(report_text, encoding="utf-8")

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "report_files_to_validate", return_value=[report]),
                patch("sys.stderr", io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                validator.validate_report_structure({})

    def test_report_structure_accepts_validation_backlog_reference(self) -> None:
        backlog_items = {
            "owner-repo-runtime-restart": {
                "id": "owner-repo-runtime-restart",
                "family": "ai-llm-systems",
                "source_report": "reports/2026-08-11.md",
                "source_repository": "owner/repo",
                "mechanism": "Runtime restart recovery",
                "evidence_gap": "Restart behavior is not validated.",
                "validation_type": "restart-recovery",
                "proposed_validation": "Run a restart recovery scenario.",
                "success_condition": "State recovers after restart.",
                "priority": "high",
                "status": "open",
                "created": "2026-08-11",
                "last_updated": "2026-08-11",
            }
        }
        report_text = complete_report().replace(
            "- No local test suite was run.",
            "- Needs restart recovery validation.",
        ).replace(
            "No validation backlog update required.",
            "\n".join(
                [
                    "| Backlog item | Repository | Family | Validation type | Reason | Status |",
                    "|---|---|---|---|---|---|",
                    "| `owner-repo-runtime-restart` | `owner/repo` | `ai-llm-systems` | `restart-recovery` | Needs restart recovery validation. | `open` |",
                ]
            ),
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "reports" / "2026-08-11.md"
            report.parent.mkdir()
            report.write_text(report_text, encoding="utf-8")

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "report_files_to_validate", return_value=[report]),
            ):
                validator.validate_report_structure(backlog_items)

    def test_report_structure_rejects_mismatched_backlog_reference(self) -> None:
        backlog_items = {
            "owner-repo-runtime-restart": {
                "id": "owner-repo-runtime-restart",
                "family": "ai-llm-systems",
                "source_report": "reports/2026-08-11.md",
                "source_repository": "other/repo",
                "mechanism": "Runtime restart recovery",
                "evidence_gap": "Restart behavior is not validated.",
                "validation_type": "restart-recovery",
                "proposed_validation": "Run a restart recovery scenario.",
                "success_condition": "State recovers after restart.",
                "priority": "high",
                "status": "open",
                "created": "2026-08-11",
                "last_updated": "2026-08-11",
            }
        }
        report_text = complete_report().replace(
            "No validation backlog update required.",
            "\n".join(
                [
                    "| Backlog item | Repository | Family | Validation type | Reason | Status |",
                    "|---|---|---|---|---|---|",
                    "| `owner-repo-runtime-restart` | `owner/repo` | `ai-llm-systems` | `restart-recovery` | Needs restart recovery validation. | `open` |",
                ]
            ),
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "reports" / "2026-08-11.md"
            report.parent.mkdir()
            report.write_text(report_text, encoding="utf-8")

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "report_files_to_validate", return_value=[report]),
                patch("sys.stderr", io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                validator.validate_report_structure(backlog_items)

    def test_failure_backlog_accepts_valid_item(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_research_scope(root)
            write_backlog(
                root,
                "\n".join(
                    [
                        "items:",
                        "  - id: owner-repo-runtime-restart",
                        "    family: ai-llm-systems",
                        "    source_report: reports/2026-08-11.md",
                        "    source_repository: owner/repo",
                        "    mechanism: Runtime restart recovery",
                        "    evidence_gap: Restart behavior is not validated.",
                        "    validation_type: restart-recovery",
                        "    proposed_validation: Run a restart recovery scenario.",
                        "    success_condition: State recovers after restart.",
                        "    priority: high",
                        "    status: open",
                        "    created: 2026-08-11",
                        "    last_updated: 2026-08-11",
                    ]
                ),
            )

            with patch.object(validator, "ROOT", root):
                items = validator.validate_failure_backlog()

        self.assertIn("owner-repo-runtime-restart", items)

    def test_failure_backlog_rejects_bad_validation_type(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_research_scope(root)
            write_backlog(
                root,
                "\n".join(
                    [
                        "items:",
                        "  - id: owner-repo-runtime-restart",
                        "    family: ai-llm-systems",
                        "    source_report: reports/2026-08-11.md",
                        "    source_repository: owner/repo",
                        "    mechanism: Runtime restart recovery",
                        "    evidence_gap: Restart behavior is not validated.",
                        "    validation_type: vague",
                        "    proposed_validation: Run a restart recovery scenario.",
                        "    success_condition: State recovers after restart.",
                        "    priority: high",
                        "    status: open",
                        "    created: 2026-08-11",
                        "    last_updated: 2026-08-11",
                    ]
                ),
            )

            with patch.object(validator, "ROOT", root), patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
                validator.validate_failure_backlog()

    def test_topic_family_consistency_accepts_matching_lists(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            families = ["ai-llm-systems", "satellites-space-systems"]
            write_research_scope(root, families)
            write_interests(root, families)

            with patch.object(validator, "ROOT", root):
                validator.validate_topic_family_consistency()

    def test_family_playbooks_reject_missing_required_heading(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            families = list(validator.FAMILY_PLAYBOOKS)
            write_research_scope(root, families)
            for family in families:
                write_family_playbook(
                    root,
                    family,
                    omit_heading="Evidence Bar" if family == "privacy-networking-vpn" else None,
                )

            with patch.object(validator, "ROOT", root), patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
                validator.validate_family_playbooks()

    def test_watchlist_accepts_company_seed_without_repository(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_research_scope(root)
            (root / "watchlist.yml").write_text(
                "\n".join(
                    [
                        "entries:",
                        "  - source: YC RightNow / RunInfra profile",
                        "    url: https://www.ycombinator.com/companies/rightnow",
                        "    family: ai-llm-systems",
                        "    artifact_type: company",
                        "    priority: high",
                        "    status: watch",
                        "    review_mode: watch-company",
                        "    reason: Company-launch seed for expanding to related runtime repositories without treating the launch as source evidence.",
                    ]
                ),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root):
                validator.validate_watchlist()

    def test_watchlist_rejects_non_repository_seed_with_source_review_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_research_scope(root)
            (root / "watchlist.yml").write_text(
                "\n".join(
                    [
                        "entries:",
                        "  - source: YC RightNow / RunInfra profile",
                        "    url: https://www.ycombinator.com/companies/rightnow",
                        "    family: ai-llm-systems",
                        "    artifact_type: company",
                        "    priority: high",
                        "    status: watch",
                        "    review_mode: deep-review",
                        "    reason: Company-launch seed for expanding to related runtime repositories without treating the launch as source evidence.",
                    ]
                ),
                encoding="utf-8",
            )

            with patch.object(validator, "ROOT", root), patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit):
                validator.validate_watchlist()


if __name__ == "__main__":
    unittest.main()
