from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from types import ModuleType


def load_validator() -> ModuleType:
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "validate-agent-governance.py"
    spec = importlib.util.spec_from_file_location("validate_agent_governance", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load validate-agent-governance.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validator = load_validator()


class AgentGovernanceValidationTest(unittest.TestCase):
    def test_pr_body_with_explicit_authorization_passes(self) -> None:
        body = "\n".join(
            [
                "User request: Implement agent governance guardrails in PR #44.",
                "Scope confirmed: yes",
                "Autonomous follow-up: no",
            ]
        )
        self.assertEqual([], validator.validate_pr_body(body))

    def test_pr_body_missing_user_request_fails(self) -> None:
        body = "\n".join(
            [
                "Scope confirmed: yes",
                "Autonomous follow-up: no",
            ]
        )
        errors = validator.validate_pr_body(body)
        self.assertIn("User request", "\n".join(errors))

    def test_pr_body_placeholder_user_request_fails(self) -> None:
        body = "\n".join(
            [
                "User request: TODO",
                "Scope confirmed: yes",
                "Autonomous follow-up: no",
            ]
        )
        errors = validator.validate_pr_body(body)
        self.assertIn("non-placeholder", "\n".join(errors))

    def test_pr_body_autonomous_follow_up_must_be_no(self) -> None:
        body = "\n".join(
            [
                "User request: Continue in PR #44.",
                "Scope confirmed: yes",
                "Autonomous follow-up: yes",
            ]
        )
        errors = validator.validate_pr_body(body)
        self.assertIn("Autonomous follow-up: no", "\n".join(errors))

    def test_governed_change_requires_openspec_evidence(self) -> None:
        errors = validator.validate_changed_files(["scripts/run-codex-radar.sh"])
        self.assertIn("OpenSpec evidence", "\n".join(errors))

    def test_governed_change_accepts_active_openspec_evidence(self) -> None:
        errors = validator.validate_changed_files(
            [
                "scripts/run-codex-radar.sh",
                "openspec/changes/add-agent-governance-guardrails/proposal.md",
            ]
        )
        self.assertEqual([], errors)

    def test_governed_change_accepts_archived_openspec_evidence(self) -> None:
        errors = validator.validate_changed_files(
            [
                ".github/workflows/radar-validation.yml",
                "openspec/changes/archive/2026-08-09-add-agent-governance-guardrails/specs/agent-governance/spec.md",
            ]
        )
        self.assertEqual([], errors)

    def test_generated_artifacts_do_not_need_openspec_evidence(self) -> None:
        errors = validator.validate_changed_files(
            [
                "reports/2026-08-09.md",
                "repositories/example.md",
                "patterns/evidence-provenance.md",
                "radar.json",
            ]
        )
        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
