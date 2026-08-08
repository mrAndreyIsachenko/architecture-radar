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
WATCHLIST_SCALAR_FIELDS = {
    "repository",
    "url",
    "family",
    "artifact_type",
    "priority",
    "status",
    "review_mode",
    "reason",
}
WATCHLIST_LIST_FIELDS = {"external_artifacts", "search_terms"}
WATCHLIST_ALLOWED_ARTIFACT_TYPES = {
    "repository",
    "model",
    "dataset",
    "benchmark",
    "runtime-adapter",
    "paper",
    "recipe",
}
WATCHLIST_ALLOWED_PRIORITIES = {"high", "medium", "low"}
WATCHLIST_ALLOWED_STATUSES = {"pending", "watch", "triaged", "reviewed", "deferred", "closed"}
WATCHLIST_ALLOWED_REVIEW_MODES = {
    "deep-review",
    "source-inspect",
    "triage-only",
    "watch-model",
    "watch-dataset",
    "watch-benchmark",
    "watch-runtime",
}


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


def clean_yaml_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def topic_families() -> set[str]:
    scope = require_path("docs/research-scope.md").read_text(encoding="utf-8")
    families: set[str] = set()
    in_section = False

    for line in scope.splitlines():
        if line.startswith("## "):
            in_section = line == "## Topic Families"
            continue
        if not in_section:
            continue
        match = re.match(r"- `([^`]+)`", line)
        if match:
            families.add(match.group(1))

    if not families:
        fail("docs/research-scope.md has no topic families")
    return families


def validate_watchlist() -> None:
    path = require_path("watchlist.yml")
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        fail("watchlist.yml is empty")
    if "\t" in text:
        fail("watchlist.yml must use spaces, not tabs")

    entries: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    current_list_key: str | None = None
    saw_entries = False

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line == "entries:":
            saw_entries = True
            current_list_key = None
            continue

        if not saw_entries:
            fail(f"watchlist.yml:{line_number} expected top-level `entries:` before entries")

        if raw_line.startswith("  - "):
            if current is not None:
                entries.append(current)
            current = {}
            current_list_key = None
            payload = raw_line[4:]
            if ": " not in payload:
                fail(f"watchlist.yml:{line_number} expected `key: value` after list marker")
            key, value = payload.split(": ", 1)
            if key not in WATCHLIST_SCALAR_FIELDS:
                fail(f"watchlist.yml:{line_number} unsupported watchlist field: {key}")
            current[key] = clean_yaml_scalar(value)
            continue

        if current is None:
            fail(f"watchlist.yml:{line_number} expected a watchlist entry")

        if raw_line.startswith("    ") and not raw_line.startswith("      "):
            payload = raw_line[4:]
            if payload.endswith(":"):
                key = payload[:-1]
                if key not in WATCHLIST_LIST_FIELDS:
                    fail(f"watchlist.yml:{line_number} unsupported watchlist list field: {key}")
                current[key] = []
                current_list_key = key
                continue
            if ": " not in payload:
                fail(f"watchlist.yml:{line_number} expected `key: value`")
            key, value = payload.split(": ", 1)
            if key not in WATCHLIST_SCALAR_FIELDS:
                fail(f"watchlist.yml:{line_number} unsupported watchlist field: {key}")
            current[key] = clean_yaml_scalar(value)
            current_list_key = None
            continue

        if raw_line.startswith("      - "):
            if current_list_key is None:
                fail(f"watchlist.yml:{line_number} list item without a list field")
            list_value = current.get(current_list_key)
            if not isinstance(list_value, list):
                fail(f"watchlist.yml:{line_number} invalid list field: {current_list_key}")
            list_value.append(clean_yaml_scalar(raw_line[8:]))
            continue

        fail(f"watchlist.yml:{line_number} unsupported indentation or syntax")

    if current is not None:
        entries.append(current)
    if not saw_entries:
        fail("watchlist.yml is missing top-level `entries:`")
    if not entries:
        fail("watchlist.yml must contain at least one entry")

    families = topic_families()
    required = {"repository", "family", "artifact_type", "priority", "status", "review_mode", "reason"}

    for index, entry in enumerate(entries, start=1):
        missing = required - set(entry)
        if missing:
            fail(f"watchlist.yml entry {index} missing required fields: {', '.join(sorted(missing))}")
        repository = str(entry["repository"])
        if not re.fullmatch(r"[^/\s]+/[^/\s]+", repository):
            fail(f"watchlist.yml entry {index} has invalid repository: {repository}")
        family = str(entry["family"])
        if family not in families:
            fail(f"watchlist.yml entry {index} has unknown family: {family}")
        artifact_type = str(entry["artifact_type"])
        if artifact_type not in WATCHLIST_ALLOWED_ARTIFACT_TYPES:
            fail(f"watchlist.yml entry {index} has unsupported artifact_type: {artifact_type}")
        priority = str(entry["priority"])
        if priority not in WATCHLIST_ALLOWED_PRIORITIES:
            fail(f"watchlist.yml entry {index} has unsupported priority: {priority}")
        status = str(entry["status"])
        if status not in WATCHLIST_ALLOWED_STATUSES:
            fail(f"watchlist.yml entry {index} has unsupported status: {status}")
        review_mode = str(entry["review_mode"])
        if review_mode not in WATCHLIST_ALLOWED_REVIEW_MODES:
            fail(f"watchlist.yml entry {index} has unsupported review_mode: {review_mode}")
        reason = str(entry["reason"]).strip()
        if len(reason) < 20:
            fail(f"watchlist.yml entry {index} reason is too short")


require_path("interests.md")
require_path("watchlist.yml")
require_path("radar.json")
require_path("reports", directory=True)
require_path("repositories", directory=True)
require_path("patterns", directory=True)
require_path("docs/agent-rules.md")
require_path("docs/research-scope.md")

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
validate_watchlist()

print("radar artifacts validated")
