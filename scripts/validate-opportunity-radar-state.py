#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path.cwd()
RUN_DATE = os.environ.get("OPPORTUNITY_RADAR_RUN_DATE")

REQUIRED_FILES = [
    "opportunity-interests.md",
    "opportunity-watchlist.yml",
    "opportunities.json",
    "docs/opportunity-agent-rules.md",
    "docs/opportunity-research-scope.md",
]

REQUIRED_DIRS = [
    "opportunity-reports",
    "opportunities",
    "signals",
]

REQUIRED_REPORT_SECTIONS = {
    "Prerequisites And State",
    "Signal Counts",
    "Selected Opportunities",
    "Executive Summary",
    "Signal Ledger",
    "Opportunity Reviews",
    "Recommended Next Test",
    "Rejected Or Deferred Signals",
    "Evidence Gaps",
}

LEDGER_REQUIRED_COLUMNS = {
    "Source",
    "URL",
    "Family",
    "Signal type",
    "Evidence label",
    "Decision",
    "Reason",
}

SELECTED_OPPORTUNITY_SECTIONS = {
    "Opportunity Summary",
    "Evidence",
    "Repeated Pain Or Demand Signal",
    "Likely User Or Buyer",
    "Current Workaround Or Money Signal",
    "Proposed Offer",
    "Success Threshold",
    "Falsification Threshold",
    "Evidence Gaps",
    "Decision",
}

MARKET_EVIDENCE_LABELS = {
    "M1 paid demand",
    "M2 repeated pain",
    "M3 competitor proof",
    "M4 workaround evidence",
}

ALLOWED_LABELS = MARKET_EVIDENCE_LABELS | {"I interpretation", "H hypothesis"}
WATCHLIST_ALLOWED_PRIORITIES = {"high", "medium", "low"}
WATCHLIST_ALLOWED_STATUSES = {"pending", "watch", "triaged", "reviewed", "deferred", "closed"}
WATCHLIST_ALLOWED_SIGNAL_TYPES = {
    "repeated-pain",
    "paid-demand",
    "competitor-proof",
    "workaround-economy",
    "integration-gap",
    "operational-risk",
    "infrastructure-shift",
    "incumbent-friction",
}
WATCHLIST_SCALAR_FIELDS = {"source", "url", "family", "signal_type", "priority", "status", "reason"}
WATCHLIST_LIST_FIELDS = {"search_terms"}


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


def markdown_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None

    for line in text.splitlines():
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            current = match.group(1)
            sections[current] = []
            continue
        if current is not None:
            sections[current].append(line)

    return {name: "\n".join(lines).strip() for name, lines in sections.items()}


def topic_families() -> set[str]:
    scope = require_path("docs/opportunity-research-scope.md").read_text(encoding="utf-8")
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
        fail("docs/opportunity-research-scope.md has no topic families")
    return families


def changed_opportunity_files() -> list[Path]:
    names: set[str] = set()
    base_ref = os.environ.get("OPPORTUNITY_RADAR_BASE_REF") or os.environ.get("GITHUB_BASE_REF")
    diff_range = ["HEAD"]

    if base_ref:
        remote_base = f"origin/{base_ref}"
        try:
            subprocess.run(["git", "rev-parse", "--verify", remote_base], check=True, capture_output=True, text=True)
        except (OSError, subprocess.CalledProcessError):
            remote_base = base_ref
        diff_range = [f"{remote_base}...HEAD"]

    try:
        diff_result = subprocess.run(
            [
                "git",
                "diff",
                "--name-only",
                "--diff-filter=ACMRT",
                *diff_range,
                "--",
                "opportunity-reports",
                "opportunities",
                "signals",
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
                "opportunity-reports",
                "opportunities",
                "signals",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        untracked_result = None

    if untracked_result:
        names.update(untracked_result.stdout.splitlines())

    return sorted(ROOT / name for name in names if (ROOT / name).is_file())


def report_files_to_validate() -> list[Path]:
    paths: set[Path] = set()
    for path in changed_opportunity_files():
        if path.parent == ROOT / "opportunity-reports" and path.suffix == ".md":
            paths.add(path)
    if RUN_DATE:
        paths.add(ROOT / "opportunity-reports" / f"{RUN_DATE}.md")
    return sorted(paths)


def validate_label_text(path: Path, text: str) -> None:
    for line_number, line in enumerate(text.splitlines(), start=1):
        if "E1 source verified" in line or "E2 test verified" in line or "E3 maintainer stated" in line:
            fail(f"{path.relative_to(ROOT)}:{line_number} uses Architecture Radar evidence labels; use market-specific M labels")

        for match in re.findall(r"\b([MHI][0-9]? [A-Za-z -]+)", line):
            label = match.strip(" .,:;")
            if label.startswith(("M", "I ", "H ")) and label not in ALLOWED_LABELS:
                fail(f"{path.relative_to(ROOT)}:{line_number} has unsupported evidence label: {label}")


def validate_signal_ledger(path: Path, section_text: str) -> None:
    lines = [line for line in section_text.splitlines() if line.startswith("|")]
    if len(lines) < 3:
        fail(f"{path.relative_to(ROOT)} Signal Ledger must contain a markdown table with at least one row")

    header = [cell.strip() for cell in lines[0].strip().strip("|").split("|")]
    missing = LEDGER_REQUIRED_COLUMNS - set(header)
    if missing:
        fail(f"{path.relative_to(ROOT)} Signal Ledger missing columns: {', '.join(sorted(missing))}")

    separator = [cell.strip() for cell in lines[1].strip().strip("|").split("|")]
    if len(separator) != len(header) or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in separator):
        fail(f"{path.relative_to(ROOT)} Signal Ledger has an invalid markdown separator row")

    label_index = header.index("Evidence label")
    for row_index, row in enumerate(lines[2:], start=1):
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        if len(cells) != len(header):
            fail(f"{path.relative_to(ROOT)} Signal Ledger row {row_index} has {len(cells)} cells, expected {len(header)}")
        label = cells[label_index].strip("`")
        if label not in ALLOWED_LABELS:
            fail(f"{path.relative_to(ROOT)} Signal Ledger row {row_index} has unsupported evidence label: {label}")


def validate_report_structure() -> None:
    for path in report_files_to_validate():
        if not path.is_file():
            fail(f"missing opportunity report: {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            fail(f"opportunity report is empty: {path.relative_to(ROOT)}")

        validate_label_text(path, text)
        sections = markdown_sections(text)
        missing = REQUIRED_REPORT_SECTIONS - set(sections)
        if missing:
            fail(f"{path.relative_to(ROOT)} missing required report sections: {', '.join(sorted(missing))}")

        for section in REQUIRED_REPORT_SECTIONS:
            if not sections[section].strip():
                fail(f"{path.relative_to(ROOT)} section is empty: {section}")

        validate_signal_ledger(path, sections["Signal Ledger"])

        selected_text = sections["Selected Opportunities"] + "\n" + sections["Opportunity Reviews"]
        if "None" not in sections["Selected Opportunities"] and "No selected" not in sections["Selected Opportunities"]:
            if not any(label in selected_text for label in MARKET_EVIDENCE_LABELS):
                fail(f"{path.relative_to(ROOT)} selected opportunities must include at least one market evidence label")


def validate_selected_opportunity_files() -> None:
    for path in changed_opportunity_files():
        if path.parent != ROOT / "opportunities" or path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            fail(f"selected opportunity file is empty: {path.relative_to(ROOT)}")
        validate_label_text(path, text)

        sections = markdown_sections(text)
        missing = SELECTED_OPPORTUNITY_SECTIONS - set(sections)
        if missing:
            fail(f"{path.relative_to(ROOT)} missing required sections: {', '.join(sorted(missing))}")
        if not any(label in text for label in MARKET_EVIDENCE_LABELS):
            fail(f"{path.relative_to(ROOT)} must include at least one market evidence label")


def clean_yaml_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def validate_watchlist() -> None:
    path = require_path("opportunity-watchlist.yml")
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        fail("opportunity-watchlist.yml is empty")
    if "\t" in text:
        fail("opportunity-watchlist.yml must use spaces, not tabs")

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
            fail(f"opportunity-watchlist.yml:{line_number} expected top-level `entries:` before entries")

        if raw_line.startswith("  - "):
            if current is not None:
                entries.append(current)
            current = {}
            current_list_key = None
            payload = raw_line[4:]
            if ": " not in payload:
                fail(f"opportunity-watchlist.yml:{line_number} expected `key: value` after list marker")
            key, value = payload.split(": ", 1)
            if key not in WATCHLIST_SCALAR_FIELDS:
                fail(f"opportunity-watchlist.yml:{line_number} unsupported watchlist field: {key}")
            current[key] = clean_yaml_scalar(value)
            continue

        if current is None:
            fail(f"opportunity-watchlist.yml:{line_number} expected a watchlist entry")

        if raw_line.startswith("    ") and not raw_line.startswith("      "):
            payload = raw_line[4:]
            if payload.endswith(":"):
                key = payload[:-1]
                if key not in WATCHLIST_LIST_FIELDS:
                    fail(f"opportunity-watchlist.yml:{line_number} unsupported watchlist list field: {key}")
                current[key] = []
                current_list_key = key
                continue
            if ": " not in payload:
                fail(f"opportunity-watchlist.yml:{line_number} expected `key: value`")
            key, value = payload.split(": ", 1)
            if key not in WATCHLIST_SCALAR_FIELDS:
                fail(f"opportunity-watchlist.yml:{line_number} unsupported watchlist field: {key}")
            current[key] = clean_yaml_scalar(value)
            current_list_key = None
            continue

        if raw_line.startswith("      - "):
            if current_list_key is None:
                fail(f"opportunity-watchlist.yml:{line_number} list item without a list field")
            list_value = current.get(current_list_key)
            if not isinstance(list_value, list):
                fail(f"opportunity-watchlist.yml:{line_number} invalid list field: {current_list_key}")
            list_value.append(clean_yaml_scalar(raw_line[8:]))
            continue

        fail(f"opportunity-watchlist.yml:{line_number} unsupported indentation or syntax")

    if current is not None:
        entries.append(current)
    if not saw_entries:
        fail("opportunity-watchlist.yml is missing top-level `entries:`")
    if not entries:
        fail("opportunity-watchlist.yml must contain at least one entry")

    families = topic_families()
    required = {"source", "url", "family", "signal_type", "priority", "status", "reason"}

    for index, entry in enumerate(entries, start=1):
        missing = required - set(entry)
        if missing:
            fail(f"opportunity-watchlist.yml entry {index} missing required fields: {', '.join(sorted(missing))}")
        family = str(entry["family"])
        if family not in families:
            fail(f"opportunity-watchlist.yml entry {index} has unknown family: {family}")
        signal_type = str(entry["signal_type"])
        if signal_type not in WATCHLIST_ALLOWED_SIGNAL_TYPES:
            fail(f"opportunity-watchlist.yml entry {index} has unsupported signal_type: {signal_type}")
        priority = str(entry["priority"])
        if priority not in WATCHLIST_ALLOWED_PRIORITIES:
            fail(f"opportunity-watchlist.yml entry {index} has unsupported priority: {priority}")
        status = str(entry["status"])
        if status not in WATCHLIST_ALLOWED_STATUSES:
            fail(f"opportunity-watchlist.yml entry {index} has unsupported status: {status}")
        reason = str(entry["reason"]).strip()
        if len(reason) < 30:
            fail(f"opportunity-watchlist.yml entry {index} reason is too short")


def validate_state() -> None:
    data_path = require_path("opportunities.json")
    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"opportunities.json is not valid JSON: {exc}")

    if not isinstance(data, dict):
        fail("opportunities.json must be an object")
    if data.get("schema_version") != 1:
        fail("opportunities.json schema_version must be 1")
    if not isinstance(data.get("opportunities"), list):
        fail("opportunities.json opportunities must be a list")


def validate_workspace() -> None:
    for path in REQUIRED_FILES:
        require_path(path)
    for path in REQUIRED_DIRS:
        require_path(path, directory=True)

    if not require_path("opportunity-interests.md").read_text(encoding="utf-8").strip():
        fail("opportunity-interests.md is empty")

    if RUN_DATE:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", RUN_DATE):
            fail(f"invalid OPPORTUNITY_RADAR_RUN_DATE: {RUN_DATE}")
        report_path = ROOT / "opportunity-reports" / f"{RUN_DATE}.md"
        if not report_path.is_file():
            fail(f"missing opportunity report: {report_path}")
        if not report_path.read_text(encoding="utf-8").strip():
            fail(f"opportunity report is empty: {report_path}")


def main() -> None:
    validate_workspace()
    validate_state()
    validate_watchlist()
    validate_report_structure()
    validate_selected_opportunity_files()
    print("opportunity radar artifacts validated")


if __name__ == "__main__":
    main()
