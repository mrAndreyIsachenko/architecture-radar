from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType


def load_runner() -> ModuleType:
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "test-agent-governance-negative.py"
    spec = importlib.util.spec_from_file_location("agent_governance_negative_runner", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load test-agent-governance-negative.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


runner = load_runner()


class AgentGovernanceNegativeSelfTest(unittest.TestCase):
    def test_committed_negative_fixture_passes_self_test(self) -> None:
        self.assertEqual([], runner.run_self_test())

    def test_negative_fixture_that_unexpectedly_passes_is_failure(self) -> None:
        fixture = {
            "schema_version": 1,
            "cases": [
                {
                    "id": "bad-negative",
                    "body": "User request: Do the exact requested change.\nScope confirmed: yes\nAutonomous follow-up: no",
                    "changed_files": [
                        "scripts/run-codex-radar.sh",
                        "openspec/changes/example/proposal.md"
                    ],
                    "expected_errors": [
                        "should not appear"
                    ],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fixture.json"
            path.write_text(json.dumps(fixture), encoding="utf-8")
            failures = runner.run_self_test(path)

        self.assertIn("unexpectedly passed", "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
