#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path.cwd()
RUN_DATE = os.environ.get("ARCHITECTURE_RADAR_RUN_DATE")
SUPPLEMENT_REQUIRED = os.environ.get("ARCHITECTURE_RADAR_SUPPLEMENT_REQUIRED", "").lower()
SUPPLEMENT_REPORT = os.environ.get("ARCHITECTURE_RADAR_SUPPLEMENT_REPORT", "")


def fail(message: str) -> None:
    print(f"validation error: {message}", file=sys.stderr)
    sys.exit(1)


def require_path(path: str, *, directory: bool = False) -> Path:
    candidate = ROOT / path
    if directory:
        if not candidate.is_dir():
            fail(f"missing directory: {path}")
    elif not candidate.is_file():
        fail(f"missing file: {path}")
    return candidate


def changed_artifact_files() -> list[Path]:
    names: set[str] = set()

    try:
        diff_result = subprocess.run(
            [
                "git",
                "diff",
                "--name-only",
                "--diff-filter=ACMRT",
                "HEAD",
                "--",
                "reports",
                "repositories",
                "patterns",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return []

    names.update(diff_result.stdout.splitlines())

    try:
        untracked_result = subprocess.run(
            [
                "git",
                "ls-files",
                "--others",
                "--exclude-standard",
                "--",
                "reports",
                "repositories",
                "patterns",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        untracked_result = None

    if untracked_result:
        names.update(untracked_result.stdout.splitlines())

    paths: list[Path] = []
    for name in sorted(names):
        if not name.endswith(".md"):
            continue
        candidate = ROOT / name
        if candidate.is_file():
            paths.append(candidate)
    return paths


def evidence_label_for_path(path: str) -> str | None:
    normalized = path.replace("\\", "/").lower()
    basename = normalized.rsplit("/", 1)[-1]

    if (
        normalized.startswith(("test/", "tests/"))
        or "/test/" in normalized
        or "/tests/" in normalized
        or basename.startswith("test_")
        or "_test." in basename
        or basename.endswith("_test.go")
        or basename.endswith("test.cc")
        or basename.endswith("test.cpp")
        or basename.endswith("test.exs")
    ):
        return "E2 test verified"

    if (
        basename.startswith("readme")
        or normalized.startswith("docs/")
        or "/docs/" in normalized
        or basename.startswith("news")
        or basename.startswith("changelog")
        or basename.startswith("release")
        or normalized.startswith(("adr/", "adrs/", "spec/", "specs/"))
        or "/adr/" in normalized
        or "/adrs/" in normalized
        or "/spec/" in normalized
        or "/specs/" in normalized
    ):
        return "E3 maintainer stated"

    return None


def validate_evidence_labels() -> None:
    evidence_path = re.compile(r"`([^`]+)`")

    for path in changed_artifact_files():
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if "E1 source verified" not in line:
                continue
            for evidence in evidence_path.findall(line):
                expected = evidence_label_for_path(evidence)
                if expected:
                    relpath = path.relative_to(ROOT)
                    fail(
                        f"{relpath}:{line_number} labels `{evidence}` as E1; "
                        f"use `{expected}` for this evidence path"
                    )


require_path("interests.md")
require_path("radar.json")
require_path("reports", directory=True)
require_path("repositories", directory=True)
require_path("patterns", directory=True)
require_path("docs/architecture-radar-agent.md")

if not require_path("interests.md").read_text(encoding="utf-8").strip():
    fail("interests.md is empty")

try:
    radar = json.loads(require_path("radar.json").read_text(encoding="utf-8"))
except json.JSONDecodeError as exc:
    fail(f"radar.json is not valid JSON: {exc}")

if radar.get("schema_version") != 1:
    fail("radar.json schema_version must be 1")

if not isinstance(radar.get("repositories"), list):
    fail("radar.json repositories must be a list")

if RUN_DATE:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", RUN_DATE):
        fail(f"invalid ARCHITECTURE_RADAR_RUN_DATE: {RUN_DATE}")
    report_path = ROOT / "reports" / f"{RUN_DATE}.md"
    if not report_path.is_file():
        fail(f"missing daily report: {report_path}")
    if not report_path.read_text(encoding="utf-8").strip():
        fail(f"daily report is empty: {report_path}")

if SUPPLEMENT_REQUIRED in {"1", "true", "yes", "on"}:
    if not SUPPLEMENT_REPORT:
        fail("ARCHITECTURE_RADAR_SUPPLEMENT_REPORT is required when supplement is required")
    supplement_path = ROOT / SUPPLEMENT_REPORT
    if not supplement_path.is_file():
        fail(f"missing supplement report: {supplement_path}")
    if not supplement_path.read_text(encoding="utf-8").strip():
        fail(f"supplement report is empty: {supplement_path}")

validate_evidence_labels()

print("radar artifacts validated")
