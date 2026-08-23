from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from types import ModuleType
from unittest.mock import patch


def load_repairer() -> ModuleType:
    script = Path(__file__).resolve().parents[1] / "scripts" / "repair-radar-report-structure.py"
    spec = importlib.util.spec_from_file_location("repair_radar_report_structure", script)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load repair-radar-report-structure.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


repairer = load_repairer()


class RepairRadarReportStructureTest(unittest.TestCase):
    def test_repair_maps_common_alias_headings_to_canonical_sections(self) -> None:
        original = "\n".join(
            [
                "# Architecture Radar Report: 2026-08-23",
                "",
                "## Run Prerequisites And Repository State",
                "",
                "- workspace ok",
                "",
                "## Candidate Counts By Stage",
                "",
                "- `triaged`: 20",
                "",
                "## Ledger",
                "",
                "| Repository | URL | Commit | Discovery source | Family | Stage | Decision |",
                "|---|---|---|---|---|---|---|",
                "| `owner/repo` | https://github.com/owner/repo | `abc` | search | `ai-llm-systems` | triaged | selected |",
                "",
                "## Evidence Gaps",
                "",
                "- no local tests",
            ]
        )

        repaired = repairer.repair_report_text(original, "2026-08-23")

        self.assertIn("## Prerequisites And State\n\n- workspace ok", repaired)
        self.assertIn("## Candidate Counts\n\n- `triaged`: 20", repaired)
        self.assertIn("## Candidate Ledger\n\n| Repository | URL | Commit | Discovery source | Family | Stage | Decision |", repaired)
        self.assertIn("## Unresolved Evidence Gaps\n\n- no local tests", repaired)
        for section in repairer.REQUIRED_REPORT_SECTIONS:
            self.assertIn(f"## {section}", repaired)

    def test_repair_inserts_diagnostic_candidate_ledger_when_missing(self) -> None:
        repaired = repairer.repair_report_text(
            "\n".join(
                [
                    "# Architecture Radar Report: 2026-08-23",
                    "",
                    "## Candidate Ledger",
                    "",
                    "The agent summarized candidates in prose only.",
                ]
            ),
            "2026-08-23",
        )

        self.assertIn("| Repository | URL | Commit | Discovery source | Family | Stage | Decision |", repaired)
        self.assertIn("Repair-generated placeholder", repaired)
        self.assertIn("> The agent summarized candidates in prose only.", repaired)

    def test_repair_path_creates_missing_report_as_diagnostic(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            report = root / "reports" / "2026-08-23.md"

            with patch.object(repairer, "ROOT", root):
                changed = repairer.repair_path(report)

            self.assertTrue(changed)
            text = report.read_text(encoding="utf-8")
            self.assertIn("# Architecture Radar Report: 2026-08-23", text)
            self.assertIn("## Candidate Ledger", text)
            self.assertIn("deferred: missing candidate ledger", text)


if __name__ == "__main__":
    unittest.main()
