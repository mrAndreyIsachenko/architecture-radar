#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE = ROOT / "tests" / "fixtures" / "agent-governance" / "negative_cases.json"
VALIDATOR_PATH = ROOT / "scripts" / "validate-agent-governance.py"


def load_validator() -> ModuleType:
    spec = importlib.util.spec_from_file_location("validate_agent_governance", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_fixture(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_fixture_shape(fixture: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if fixture.get("schema_version") != 1:
        errors.append("fixture schema_version must be 1")

    cases = fixture.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("fixture must contain a non-empty cases list")
        return errors

    for index, case in enumerate(cases):
        prefix = f"case[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{prefix} must be an object")
            continue
        if not isinstance(case.get("id"), str) or not case["id"].strip():
            errors.append(f"{prefix}.id must be a non-empty string")
        if not isinstance(case.get("body"), str):
            errors.append(f"{prefix}.body must be a string")
        if not isinstance(case.get("changed_files"), list) or not all(isinstance(path, str) for path in case.get("changed_files", [])):
            errors.append(f"{prefix}.changed_files must be a list of strings")
        if not isinstance(case.get("expected_errors"), list) or not all(isinstance(text, str) for text in case.get("expected_errors", [])):
            errors.append(f"{prefix}.expected_errors must be a list of strings")
        elif not case["expected_errors"]:
            errors.append(f"{prefix}.expected_errors must not be empty")
    return errors


def evaluate_cases(fixture: dict[str, Any], validator: ModuleType) -> list[str]:
    failures: list[str] = []
    for case in fixture["cases"]:
        errors = validator.validate_pr_body(case["body"])
        errors.extend(validator.validate_changed_files(case["changed_files"]))
        rendered = "\n".join(errors)

        if not errors:
            failures.append(f"{case['id']}: negative fixture unexpectedly passed")
            continue

        for expected in case["expected_errors"]:
            if expected not in rendered:
                failures.append(
                    f"{case['id']}: expected error substring {expected!r} not found in {rendered!r}"
                )
    return failures


def run_self_test(fixture_path: Path = DEFAULT_FIXTURE) -> list[str]:
    fixture = load_fixture(fixture_path)
    shape_errors = validate_fixture_shape(fixture)
    if shape_errors:
        return shape_errors
    validator = load_validator()
    return evaluate_cases(fixture, validator)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run negative self-tests for agent governance validation.")
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    args = parser.parse_args()

    failures = run_self_test(args.fixture)
    if failures:
        print("Agent governance negative self-test failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Agent governance negative self-test passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
