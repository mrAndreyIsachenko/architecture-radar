from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check-opportunity-radar-cadence.sh"


def parse_output_file(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        result[key] = value
    return result


class OpportunityRadarCadenceTest(unittest.TestCase):
    def run_gate(
        self,
        root: Path,
        *,
        event_name: str = "schedule",
        now: str = "2026-09-08",
        report_date: str = "",
        catchup_days: str = "2",
    ) -> tuple[subprocess.CompletedProcess[str], dict[str, str], dict[str, str]]:
        output_path = root / "github-output"
        env_path = root / "github-env"
        env = os.environ.copy()
        env.update(
            {
                "GITHUB_EVENT_NAME": event_name,
                "GITHUB_OUTPUT": str(output_path),
                "GITHUB_ENV": str(env_path),
                "OPPORTUNITY_RADAR_NOW": now,
                "OPPORTUNITY_RADAR_DATE": report_date,
                "OPPORTUNITY_RADAR_CATCHUP_DAYS": catchup_days,
            }
        )
        completed = subprocess.run(
            [str(SCRIPT)],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        return completed, parse_output_file(output_path), parse_output_file(env_path)

    def test_scheduled_tuesday_runs_when_report_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "opportunity-reports").mkdir()

            completed, outputs, env = self.run_gate(root, now="2026-09-08")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(outputs["should_run"], "true")
        self.assertEqual(outputs["run_date"], "2026-09-08")
        self.assertEqual(env["OPPORTUNITY_RADAR_RUN_DATE"], "2026-09-08")

    def test_scheduled_wednesday_catches_up_tuesday_due_date(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "opportunity-reports").mkdir()

            completed, outputs, env = self.run_gate(root, now="2026-09-09")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(outputs["should_run"], "true")
        self.assertEqual(outputs["run_date"], "2026-09-08")
        self.assertEqual(env["OPPORTUNITY_RADAR_DATE"], "2026-09-08")

    def test_scheduled_monday_skips_outside_catchup_window(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "opportunity-reports").mkdir()

            completed, outputs, _ = self.run_gate(root, now="2026-09-14")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(outputs["should_run"], "false")
        self.assertIn("outside", outputs["reason"])

    def test_existing_due_report_skips_scheduled_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            reports = root / "opportunity-reports"
            reports.mkdir()
            (reports / "2026-09-08.md").write_text("# report\n", encoding="utf-8")

            completed, outputs, _ = self.run_gate(root, now="2026-09-09")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(outputs["should_run"], "false")
        self.assertIn("already exists", outputs["reason"])

    def test_manual_dispatch_always_runs_supplied_date(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "opportunity-reports").mkdir()

            completed, outputs, env = self.run_gate(
                root,
                event_name="workflow_dispatch",
                now="2026-09-14",
                report_date="2026-09-13",
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(outputs["should_run"], "true")
        self.assertEqual(outputs["run_date"], "2026-09-13")
        self.assertEqual(env["OPPORTUNITY_RADAR_RUN_DATE"], "2026-09-13")


if __name__ == "__main__":
    unittest.main()
