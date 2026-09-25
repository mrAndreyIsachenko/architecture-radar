import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/stage-radar-recovery.py"
spec = importlib.util.spec_from_file_location("stage_recovery", SCRIPT)
recovery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recovery)


class RecoveryTest(unittest.TestCase):
    def test_only_regular_allowlisted_files_are_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            root = base / "repo"
            for name in ("reports/2026-09-25.md", "radar.json", "experiments/failure-injection-backlog.yml", ".codex/auth.json", "reports/.secret.md", "reports/raw.log", "reports/nested/secret.md", "scripts/private.py", "opportunities.json"):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(name)
            outside = base / "credential"
            outside.write_text("not allowed")
            (root / "reports/linked.md").symlink_to(outside)
            (root / "patterns").symlink_to(root / "reports", target_is_directory=True)
            result = recovery.stage(root, base / "bundle", {"run_id": "123"})
            names = {item["path"] for item in result["files"]}
            self.assertEqual(names, {"reports/2026-09-25.md", "radar.json", "experiments/failure-injection-backlog.yml"})
            for item in result["files"]:
                contents = (base / "bundle/files" / item["path"]).read_bytes()
                self.assertEqual(hashlib.sha256(contents).hexdigest(), item["sha256"])
            self.assertEqual(json.loads((base / "bundle/manifest.json").read_text()), result)
            self.assertEqual(result["status"], "unvalidated-recovery")

    def test_empty_and_partial_output(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            root = base / "repo"
            root.mkdir()
            self.assertEqual(recovery.stage(root, base / "empty", {})["files"], [])
            (root / "radar.json").write_text('{"incomplete":')
            self.assertEqual(len(recovery.stage(root, base / "partial", {})["files"]), 1)

    def test_existing_or_internal_destination_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for destination in (root, root / "reports/bundle"):
                with self.assertRaises(ValueError):
                    recovery.stage(root, destination, {})

    def test_cli_requires_safe_provenance_and_does_not_dump_environment(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            root = base / "repo"
            root.mkdir()
            env = {**os.environ, "GITHUB_SHA": "a" * 40, "GITHUB_RUN_ID": "123", "GITHUB_RUN_ATTEMPT": "1", "ARCHITECTURE_RADAR_RUN_DATE": "2026-09-25", "OPENAI_API_KEY": "private-sentinel"}
            result = subprocess.run(["python3", str(SCRIPT), "--output", str(base / "bundle")], cwd=root, env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            manifest = (base / "bundle/manifest.json").read_text()
            self.assertNotIn("private-sentinel", manifest + result.stdout + result.stderr)
            env["GITHUB_RUN_ID"] = "private-sentinel"
            result = subprocess.run(["python3", str(SCRIPT), "--output", str(base / "invalid")], cwd=root, env=env, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((base / "invalid").exists())

    def test_workflow_failure_gate_does_not_hide_failure(self):
        workflow = (ROOT / ".github/workflows/architecture-radar.yml").read_text()
        self.assertIn("id: research", workflow)
        condition = "failure() && (steps.research.outcome == 'success' || steps.research.outcome == 'failure')"
        self.assertIn("if: " + condition, workflow)
        # Evaluate the restricted boolean expression for relevant step outcomes.
        for failed in (True, False):
            for outcome in ("success", "failure", "skipped", "cancelled", ""):
                expression = condition.replace("failure()", repr(failed)).replace("steps.research.outcome", repr(outcome)).replace("&&", "and").replace("||", "or")
                self.assertEqual(eval(expression, {"__builtins__": {}}), failed and outcome in {"success", "failure"})
        tail = workflow[workflow.index("      - name: Stage failed research output"):]
        self.assertIn("if: failure() && steps.recovery.outcome == 'success'", tail)
        self.assertIn("retention-days: 7", tail)
        self.assertIn("if-no-files-found: error", tail)
        self.assertNotIn("continue-on-error", workflow)
        self.assertLess(workflow.index("Validate radar artifacts"), workflow.index("Publish pull request"))
        self.assertNotIn("always()", workflow[workflow.index("      - name: Publish pull request"):workflow.index("      - name: Stage failed research output")])

    def test_agent_prompt_requires_full_validation(self):
        prompt = (ROOT / "scripts/run-codex-radar.sh").read_text()
        self.assertIn("canonical owner/repository identity", prompt)
        self.assertIn("python3 scripts/validate-radar-state.py", prompt)
        self.assertIn("Do not change validators or scripts to bypass failures", prompt)

    def test_smoke_lane_cannot_run_model_or_publish(self):
        workflow = (ROOT / ".github/workflows/architecture-radar.yml").read_text()
        production, smoke = workflow.split("  recovery-smoke:\n")
        self.assertIn("if: github.event_name != 'workflow_dispatch' || !inputs.recovery_smoke", production)
        self.assertIn("if: github.event_name == 'workflow_dispatch' && inputs.recovery_smoke", smoke)
        self.assertIn("permissions:\n      contents: read", smoke)
        self.assertIn("persist-credentials: false", smoke)
        self.assertIn("run: scripts/validate-radar-state.py", smoke)
        self.assertNotIn("secrets.", smoke)
        self.assertNotIn("run-codex", smoke)
        self.assertNotIn("publish-radar", smoke)
        # Hosted fixture must exercise exactly the production recovery steps.
        marker = "      - name: Stage failed research output"
        self.assertEqual(production[production.index(marker):].strip(), smoke[smoke.index(marker):].strip())

    def test_smoke_fixture_is_rejected_by_real_validator(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "reports").mkdir()
            fixture = ROOT / "tests/fixtures/recovery-invalid-report.md"
            (root / "reports/9999-12-31.md").write_bytes(fixture.read_bytes())
            validator_spec = importlib.util.spec_from_file_location("smoke_validator", ROOT / "scripts/validate-radar-state.py")
            validator = importlib.util.module_from_spec(validator_spec)
            validator_spec.loader.exec_module(validator)
            validator.ROOT = root
            with patch.object(validator, "report_files_to_validate", return_value=[root / "reports/9999-12-31.md"]):
                with self.assertRaises(SystemExit):
                    validator.validate_report_structure()


if __name__ == "__main__":
    unittest.main()
