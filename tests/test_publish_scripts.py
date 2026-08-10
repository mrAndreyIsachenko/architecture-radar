from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PublishScriptsTest(unittest.TestCase):
    def test_publish_scripts_stage_allowlist_before_no_change_check(self) -> None:
        scripts = {
            "scripts/publish-radar-run.sh": "git add README.md interests.md radar.json reports repositories patterns",
            "scripts/publish-opportunity-radar-run.sh": "git add opportunity-interests.md opportunity-watchlist.yml opportunities.json opportunity-reports opportunities signals",
            "scripts/publish-weekly-synthesis-run.sh": "git add weekly-reports",
        }

        for rel_path, git_add in scripts.items():
            with self.subTest(script=rel_path):
                text = (ROOT / rel_path).read_text(encoding="utf-8")
                self.assertNotIn("git diff --quiet && git diff --cached --quiet", text)
                self.assertLess(text.index(git_add), text.index("git diff --cached --quiet"))

    def test_generated_pr_bodies_include_governance_fields(self) -> None:
        scripts = [
            "scripts/publish-radar-run.sh",
            "scripts/publish-opportunity-radar-run.sh",
            "scripts/publish-weekly-synthesis-run.sh",
        ]

        required_fields = [
            "## Agent Governance",
            "User request:",
            "Scope confirmed: yes",
            "Autonomous follow-up: no",
            "OpenSpec change: Not required; generated research artifact PR.",
        ]

        for rel_path in scripts:
            with self.subTest(script=rel_path):
                text = (ROOT / rel_path).read_text(encoding="utf-8")
                for field in required_fields:
                    self.assertIn(field, text)


if __name__ == "__main__":
    unittest.main()
