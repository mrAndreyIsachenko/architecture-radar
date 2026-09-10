from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREPARE_SCRIPTS = [
    ROOT / "scripts" / "prepare-radar-run.sh",
    ROOT / "scripts" / "prepare-opportunity-radar-run.sh",
    ROOT / "scripts" / "prepare-weekly-synthesis-run.sh",
]


class GeneratedCommitIdentityTest(unittest.TestCase):
    def test_prepare_scripts_default_to_personal_commit_email(self) -> None:
        for script in PREPARE_SCRIPTS:
            with self.subTest(script=script.name):
                text = script.read_text(encoding="utf-8")
                self.assertIn("RADAR_COMMIT_USER_NAME:-Andrey Isachenko", text)
                self.assertIn("RADAR_COMMIT_USER_EMAIL:-mr.andrey.isachenko@gmail.com", text)
                self.assertIn('git config user.name "$commit_user_name"', text)
                self.assertIn('git config user.email "$commit_user_email"', text)
                self.assertNotIn("@users.noreply.github.com", text)


if __name__ == "__main__":
    unittest.main()
