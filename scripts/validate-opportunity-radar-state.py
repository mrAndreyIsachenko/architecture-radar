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
    "Build Readiness",
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
BUILD_READINESS_REQUIRED_COLUMNS = {
    "Opportunity",
    "Paid wedge",
    "Distribution channel",
    "Private data barrier",
    "OSS commoditization risk",
    "Product shape",
    "Pricing hypothesis",
    "Do not build until",
    "Build decision",
}

SELECTED_OPPORTUNITY_SECTIONS = {
    "Opportunity Summary",
    "Evidence",
    "Repeated Pain Or Demand Signal",
    "Likely User Or Buyer",
    "Current Workaround Or Money Signal",
    "Paid Wedge",
    "Distribution Channel",
    "Private Data Barrier",
    "OSS Commoditization Risk",
    "Product Shape",
    "Pricing Hypothesis",
    "Do Not Build Until",
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
STATE_ALLOWED_LABELS = ALLOWED_LABELS | {"M1", "M2", "M3", "M4", "I", "H"}
STATE_ARRAY_FIELDS = ("selected", "deferred", "watchlisted")
STATE_DISCOVERY_MODES = {"broad-discovery", "watchlist-directed", "mixed", "diagnostic"}
STATE_CONFIDENCE_VALUES = {"low", "medium-low", "medium", "medium-high", "high"}
STATE_MONEY_SIGNAL_VALUES = {"none-found", "weak", "medium", "strong"}
STATE_REACHABILITY_VALUES = {"low", "medium", "high"}
STATE_PRIVATE_DATA_BARRIER_VALUES = {
    "none",
    "public-only",
    "private-code-required",
    "private-data-required",
    "unclear",
}
STATE_OSS_COMMODITIZATION_RISK_VALUES = {"low", "medium", "high", "unclear"}
STATE_PRODUCT_SHAPE_VALUES = {
    "cli",
    "github-action",
    "browser-extension",
    "hosted-api",
    "report",
    "other",
    "unclear",
}
STATE_PRICING_HYPOTHESIS_VALUES = {"free", "team", "pro", "unclear"}
STATE_REQUIRED_COMPARISON_FIELDS = {
    "score",
    "confidence",
    "money_signal",
    "reachability",
    "evidence_count",
    "next_test",
    "paid_wedge",
    "distribution_channel",
    "private_data_barrier",
    "oss_commoditization_risk",
    "product_shape",
    "pricing_hypothesis",
    "do_not_build_until",
}
STATE_STAGE_VALUES = {"selected", "selected-for-test", "selected-for-build", "deferred", "watchlist", "watchlisted"}
UNCLEAR_TEXT_MARKERS = {
    "unclear",
    "unknown",
    "not clear",
    "not proven",
    "none found",
    "no paid",
    "no direct spend",
    "no budget",
    "tbd",
    "n/a",
}
PRIVATE_DATA_BLOCKING_VALUES = {"private-code-required", "private-data-required", "unclear"}
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


def clean_table_cell(value: str) -> str:
    return value.strip().strip("`").strip()


def validate_build_readiness_table(path: Path, section_text: str) -> None:
    if "None" in section_text or "No selected" in section_text:
        return

    lines = [line for line in section_text.splitlines() if line.startswith("|")]
    if len(lines) < 3:
        fail(f"{path.relative_to(ROOT)} Build Readiness must contain a markdown table with at least one row")

    header = [cell.strip() for cell in lines[0].strip().strip("|").split("|")]
    missing = BUILD_READINESS_REQUIRED_COLUMNS - set(header)
    if missing:
        fail(f"{path.relative_to(ROOT)} Build Readiness missing columns: {', '.join(sorted(missing))}")

    separator = [cell.strip() for cell in lines[1].strip().strip("|").split("|")]
    if len(separator) != len(header) or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in separator):
        fail(f"{path.relative_to(ROOT)} Build Readiness has an invalid markdown separator row")

    indexes = {name: header.index(name) for name in BUILD_READINESS_REQUIRED_COLUMNS}
    for row_index, row in enumerate(lines[2:], start=1):
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        if len(cells) != len(header):
            fail(f"{path.relative_to(ROOT)} Build Readiness row {row_index} has {len(cells)} cells, expected {len(header)}")

        paid_wedge = clean_table_cell(cells[indexes["Paid wedge"]])
        distribution_channel = clean_table_cell(cells[indexes["Distribution channel"]])
        private_data_barrier = clean_table_cell(cells[indexes["Private data barrier"]])
        oss_risk = clean_table_cell(cells[indexes["OSS commoditization risk"]])
        product_shape = clean_table_cell(cells[indexes["Product shape"]])
        pricing_hypothesis = clean_table_cell(cells[indexes["Pricing hypothesis"]])
        do_not_build_until = clean_table_cell(cells[indexes["Do not build until"]])
        build_decision = normalize_stage(clean_table_cell(cells[indexes["Build decision"]]))

        if len(paid_wedge) < 30:
            fail(f"{path.relative_to(ROOT)} Build Readiness row {row_index} paid wedge is too short")
        if len(distribution_channel) < 20:
            fail(f"{path.relative_to(ROOT)} Build Readiness row {row_index} distribution channel is too short")
        if len(do_not_build_until) < 30:
            fail(f"{path.relative_to(ROOT)} Build Readiness row {row_index} do not build until is too short")
        if private_data_barrier not in STATE_PRIVATE_DATA_BARRIER_VALUES:
            fail(
                f"{path.relative_to(ROOT)} Build Readiness row {row_index} private data barrier must be one of: "
                + ", ".join(sorted(STATE_PRIVATE_DATA_BARRIER_VALUES))
            )
        if oss_risk not in STATE_OSS_COMMODITIZATION_RISK_VALUES:
            fail(
                f"{path.relative_to(ROOT)} Build Readiness row {row_index} OSS commoditization risk must be one of: "
                + ", ".join(sorted(STATE_OSS_COMMODITIZATION_RISK_VALUES))
            )
        if product_shape not in STATE_PRODUCT_SHAPE_VALUES:
            fail(f"{path.relative_to(ROOT)} Build Readiness row {row_index} product shape must be one of: {', '.join(sorted(STATE_PRODUCT_SHAPE_VALUES))}")
        if pricing_hypothesis not in STATE_PRICING_HYPOTHESIS_VALUES:
            fail(
                f"{path.relative_to(ROOT)} Build Readiness row {row_index} pricing hypothesis must be one of: "
                + ", ".join(sorted(STATE_PRICING_HYPOTHESIS_VALUES))
            )
        if build_decision not in STATE_STAGE_VALUES:
            fail(f"{path.relative_to(ROOT)} Build Readiness row {row_index} has unsupported build decision: {build_decision}")
        if build_decision in {"selected", "selected-for-test", "selected-for-build"}:
            if is_unclear_text(paid_wedge):
                fail(f"{path.relative_to(ROOT)} Build Readiness row {row_index} cannot be selected with an unclear paid wedge")
            if private_data_barrier in PRIVATE_DATA_BLOCKING_VALUES:
                fail(
                    f"{path.relative_to(ROOT)} Build Readiness row {row_index} cannot be selected with private data barrier "
                    f"`{private_data_barrier}`"
                )


def is_unclear_text(value: object) -> bool:
    text = str(value).strip().lower()
    if not text:
        return True
    return any(marker in text for marker in UNCLEAR_TEXT_MARKERS)


def normalize_stage(value: object) -> str:
    return str(value).strip().lower().replace("_", "-")


def validate_opportunity_build_readiness(path_label: str, sections: dict[str, str]) -> None:
    for section in SELECTED_OPPORTUNITY_SECTIONS:
        if section in sections and not sections[section].strip():
            fail(f"{path_label} section is empty: {section}")

    product_shape = sections.get("Product Shape", "").strip().lower()
    if product_shape and product_shape not in STATE_PRODUCT_SHAPE_VALUES:
        fail(f"{path_label} Product Shape must be one of: {', '.join(sorted(STATE_PRODUCT_SHAPE_VALUES))}")

    pricing_hypothesis = sections.get("Pricing Hypothesis", "").strip().lower()
    if pricing_hypothesis and pricing_hypothesis not in STATE_PRICING_HYPOTHESIS_VALUES:
        fail(f"{path_label} Pricing Hypothesis must be one of: {', '.join(sorted(STATE_PRICING_HYPOTHESIS_VALUES))}")

    private_data_barrier = sections.get("Private Data Barrier", "").strip().lower()
    if private_data_barrier and private_data_barrier not in STATE_PRIVATE_DATA_BARRIER_VALUES:
        fail(f"{path_label} Private Data Barrier must be one of: {', '.join(sorted(STATE_PRIVATE_DATA_BARRIER_VALUES))}")

    oss_risk = sections.get("OSS Commoditization Risk", "").strip().lower()
    if oss_risk and oss_risk not in STATE_OSS_COMMODITIZATION_RISK_VALUES:
        fail(f"{path_label} OSS Commoditization Risk must be one of: {', '.join(sorted(STATE_OSS_COMMODITIZATION_RISK_VALUES))}")

    decision = sections.get("Decision", "")
    if "selected for build" in decision.lower() or "selected-for-build" in decision.lower():
        if is_unclear_text(sections.get("Paid Wedge", "")):
            fail(f"{path_label} cannot be selected for build with an unclear Paid Wedge")
        if private_data_barrier in PRIVATE_DATA_BLOCKING_VALUES:
            fail(f"{path_label} cannot be selected for build with Private Data Barrier `{private_data_barrier}`")


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
        validate_build_readiness_table(path, sections["Build Readiness"])

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
        validate_opportunity_build_readiness(str(path.relative_to(ROOT)), sections)
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

    has_entries = any(data.get(field) for field in STATE_ARRAY_FIELDS)
    discovery_mode = data.get("discovery_mode")
    if has_entries and discovery_mode not in STATE_DISCOVERY_MODES:
        fail("opportunities.json discovery_mode must be one of: " + ", ".join(sorted(STATE_DISCOVERY_MODES)))

    families = topic_families()
    for field in STATE_ARRAY_FIELDS:
        entries = data.get(field)
        if not isinstance(entries, list):
            fail(f"opportunities.json {field} must be a list")
        for index, entry in enumerate(entries, start=1):
            if not isinstance(entry, dict):
                fail(f"opportunities.json {field}[{index}] must be an object")
            entry_id = str(entry.get("id", "")).strip()
            if not entry_id:
                fail(f"opportunities.json {field}[{index}] is missing id")
            missing = STATE_REQUIRED_COMPARISON_FIELDS - set(entry)
            if missing:
                fail(f"opportunities.json {field}[{index}] missing comparison fields: {', '.join(sorted(missing))}")

            score = entry["score"]
            if not isinstance(score, int) or isinstance(score, bool) or not 0 <= score <= 10:
                fail(f"opportunities.json {field}[{index}] score must be an integer from 0 to 10")
            confidence = entry["confidence"]
            if confidence not in STATE_CONFIDENCE_VALUES:
                fail(f"opportunities.json {field}[{index}] confidence must be one of: {', '.join(sorted(STATE_CONFIDENCE_VALUES))}")
            money_signal = entry["money_signal"]
            if money_signal not in STATE_MONEY_SIGNAL_VALUES:
                fail(f"opportunities.json {field}[{index}] money_signal must be one of: {', '.join(sorted(STATE_MONEY_SIGNAL_VALUES))}")
            reachability = entry["reachability"]
            if reachability not in STATE_REACHABILITY_VALUES:
                fail(f"opportunities.json {field}[{index}] reachability must be one of: {', '.join(sorted(STATE_REACHABILITY_VALUES))}")
            evidence_count = entry["evidence_count"]
            if not isinstance(evidence_count, int) or isinstance(evidence_count, bool) or evidence_count < 0:
                fail(f"opportunities.json {field}[{index}] evidence_count must be a non-negative integer")
            next_test = str(entry["next_test"]).strip()
            if len(next_test) < 30:
                fail(f"opportunities.json {field}[{index}] next_test is too short")
            paid_wedge = str(entry["paid_wedge"]).strip()
            if len(paid_wedge) < 30:
                fail(f"opportunities.json {field}[{index}] paid_wedge is too short")
            distribution_channel = str(entry["distribution_channel"]).strip()
            if len(distribution_channel) < 20:
                fail(f"opportunities.json {field}[{index}] distribution_channel is too short")
            do_not_build_until = str(entry["do_not_build_until"]).strip()
            if len(do_not_build_until) < 30:
                fail(f"opportunities.json {field}[{index}] do_not_build_until is too short")

            private_data_barrier = entry["private_data_barrier"]
            if private_data_barrier not in STATE_PRIVATE_DATA_BARRIER_VALUES:
                fail(
                    f"opportunities.json {field}[{index}] private_data_barrier must be one of: "
                    + ", ".join(sorted(STATE_PRIVATE_DATA_BARRIER_VALUES))
                )
            oss_risk = entry["oss_commoditization_risk"]
            if oss_risk not in STATE_OSS_COMMODITIZATION_RISK_VALUES:
                fail(
                    f"opportunities.json {field}[{index}] oss_commoditization_risk must be one of: "
                    + ", ".join(sorted(STATE_OSS_COMMODITIZATION_RISK_VALUES))
                )
            product_shape = entry["product_shape"]
            if product_shape not in STATE_PRODUCT_SHAPE_VALUES:
                fail(f"opportunities.json {field}[{index}] product_shape must be one of: {', '.join(sorted(STATE_PRODUCT_SHAPE_VALUES))}")
            pricing_hypothesis = entry["pricing_hypothesis"]
            if pricing_hypothesis not in STATE_PRICING_HYPOTHESIS_VALUES:
                fail(
                    f"opportunities.json {field}[{index}] pricing_hypothesis must be one of: "
                    + ", ".join(sorted(STATE_PRICING_HYPOTHESIS_VALUES))
                )

            stage = entry.get("stage")
            if stage is not None and normalize_stage(stage) not in STATE_STAGE_VALUES:
                fail(f"opportunities.json {field}[{index}] has unsupported stage: {stage}")
            if field == "selected":
                if is_unclear_text(paid_wedge):
                    fail(f"opportunities.json selected[{index}] has unclear paid_wedge; keep it in watchlisted")
                if private_data_barrier in PRIVATE_DATA_BLOCKING_VALUES:
                    fail(f"opportunities.json selected[{index}] requires private data/code or has unclear barrier; keep it in watchlisted")
            if normalize_stage(stage) == "selected-for-build":
                if is_unclear_text(paid_wedge):
                    fail(f"opportunities.json {field}[{index}] cannot be selected-for-build with an unclear paid_wedge")
                if private_data_barrier in PRIVATE_DATA_BLOCKING_VALUES:
                    fail(f"opportunities.json {field}[{index}] cannot be selected-for-build with private_data_barrier `{private_data_barrier}`")

            family = entry.get("family")
            if family is not None and family not in families:
                fail(f"opportunities.json {field}[{index}] has unknown family: {family}")
            labels = entry.get("labels", [])
            if labels is not None:
                if not isinstance(labels, list):
                    fail(f"opportunities.json {field}[{index}] labels must be a list")
                for label in labels:
                    if label not in STATE_ALLOWED_LABELS:
                        fail(f"opportunities.json {field}[{index}] has unsupported label: {label}")


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
