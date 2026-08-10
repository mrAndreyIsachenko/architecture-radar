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
    "Money Readiness",
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
MONEY_READINESS_REQUIRED_COLUMNS = {
    "Opportunity",
    "Pain",
    "Spend",
    "Reachability",
    "Timing",
    "Buildability",
    "Buyer",
    "Existing spend",
    "Paid experiment",
    "Source classes",
    "Stage",
}

SELECTED_OPPORTUNITY_SECTIONS = {
    "Opportunity Summary",
    "Evidence",
    "Repeated Pain Or Demand Signal",
    "Likely User Or Buyer",
    "Current Workaround Or Money Signal",
    "Technology Shift",
    "Buyer",
    "Expensive Workflow",
    "Existing Spend",
    "Paid Experiment",
    "Money-First Scores",
    "Source Classes",
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
STATE_SOURCE_CLASS_VALUES = {
    "github",
    "forum",
    "social",
    "product",
    "pricing",
    "job",
    "procurement",
    "marketplace",
    "docs",
    "benchmark",
    "news",
    "other",
}
TECHNOLOGY_SHIFT_REQUIRED_FIELDS = {
    "what_changed",
    "when",
    "old_constraint",
    "new_capability",
    "cost_delta",
    "quality_delta",
    "latency_delta",
    "accessibility_delta",
    "affected_workflows",
}
MONEY_SCORE_FIELDS = {
    "pain_score",
    "spend_score",
    "reachability_score",
    "timing_score",
    "buildability_score",
}
STATE_REQUIRED_COMPARISON_FIELDS = {
    "score",
    "pain_score",
    "spend_score",
    "reachability_score",
    "timing_score",
    "buildability_score",
    "confidence",
    "money_signal",
    "reachability",
    "evidence_count",
    "next_test",
    "technology_shift",
    "buyer",
    "expensive_workflow",
    "existing_spend",
    "paid_experiment",
    "source_classes",
    "paid_wedge",
    "distribution_channel",
    "private_data_barrier",
    "oss_commoditization_risk",
    "product_shape",
    "pricing_hypothesis",
    "do_not_build_until",
}
STATE_STAGE_VALUES = {"selected", "selected-for-test", "sell-before-build", "selected-for-build", "deferred", "watchlist", "watchlisted"}
STATE_STAGE_VALUES_BY_ARRAY = {
    "selected": {"selected", "selected-for-test", "sell-before-build", "selected-for-build"},
    "deferred": {"deferred"},
    "watchlisted": {"watchlist", "watchlisted"},
}
BUILD_READINESS_STATE_FIELDS = {
    "Paid wedge": "paid_wedge",
    "Distribution channel": "distribution_channel",
    "Private data barrier": "private_data_barrier",
    "OSS commoditization risk": "oss_commoditization_risk",
    "Product shape": "product_shape",
    "Pricing hypothesis": "pricing_hypothesis",
    "Do not build until": "do_not_build_until",
}
MONEY_READINESS_STATE_FIELDS = {
    "Pain": "pain_score",
    "Spend": "spend_score",
    "Reachability": "reachability_score",
    "Timing": "timing_score",
    "Buildability": "buildability_score",
    "Buyer": "buyer",
    "Existing spend": "existing_spend",
    "Paid experiment": "paid_experiment",
    "Source classes": "source_classes",
}
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
URL_RE = re.compile(r"https?://[^\s\]\)>]+")


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


def signal_note_files_to_validate() -> list[Path]:
    paths: set[Path] = set()
    for path in changed_opportunity_files():
        if path.parent == ROOT / "signals" and path.suffix == ".md":
            paths.add(path)
    return sorted(paths)


def extract_urls(text: str) -> set[str]:
    return {match.group(0).rstrip(".,;:") for match in URL_RE.finditer(text)}


def field_value(text: str, field: str) -> str:
    match = re.search(rf"(?im)^\s*(?:[-*]\s*)?{re.escape(field)}\s*:\s*(.+?)\s*$", text)
    return match.group(1).strip().strip("`") if match else ""


def validate_label_text(path: Path, text: str) -> None:
    for line_number, line in enumerate(text.splitlines(), start=1):
        if "E1 source verified" in line or "E2 test verified" in line or "E3 maintainer stated" in line:
            fail(f"{path.relative_to(ROOT)}:{line_number} uses Architecture Radar evidence labels; use market-specific M labels")

        for match in re.findall(r"\b([MHI][0-9]? [A-Za-z -]+)", line):
            label = match.strip(" .,:;")
            if label.startswith(("M", "I ", "H ")) and label not in ALLOWED_LABELS:
                fail(f"{path.relative_to(ROOT)}:{line_number} has unsupported evidence label: {label}")


def validate_signal_ledger(path: Path, section_text: str) -> list[dict[str, str]]:
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
    rows: list[dict[str, str]] = []
    for row_index, row in enumerate(lines[2:], start=1):
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        if len(cells) != len(header):
            fail(f"{path.relative_to(ROOT)} Signal Ledger row {row_index} has {len(cells)} cells, expected {len(header)}")
        label = cells[label_index].strip("`")
        if label not in ALLOWED_LABELS:
            fail(f"{path.relative_to(ROOT)} Signal Ledger row {row_index} has unsupported evidence label: {label}")
        rows.append({column: cells[index] for index, column in enumerate(header)})

    return rows


def signal_note_paths_for_report(path: Path) -> list[Path]:
    return sorted((ROOT / "signals").glob(f"{path.stem}-*.md"))


def validate_signal_note_file(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        fail(f"signal note is empty: {path.relative_to(ROOT)}")

    validate_label_text(path, text)
    urls = extract_urls(text)
    if not urls:
        fail(f"{path.relative_to(ROOT)} signal note must include at least one source URL")

    lowered = text.lower()
    if "date range" not in lowered and not re.search(r"(?im)^\s*(?:[-*]\s*)?date\s*:", text):
        fail(f"{path.relative_to(ROOT)} signal note must include source date or date range")

    family = field_value(text, "Family")
    if not family:
        fail(f"{path.relative_to(ROOT)} signal note must include Family")
    if family not in topic_families():
        fail(f"{path.relative_to(ROOT)} signal note has unknown Family: {family}")

    signal_type = field_value(text, "Signal type")
    if not signal_type:
        fail(f"{path.relative_to(ROOT)} signal note must include Signal type")
    if signal_type not in WATCHLIST_ALLOWED_SIGNAL_TYPES:
        fail(f"{path.relative_to(ROOT)} signal note has unsupported Signal type: {signal_type}")

    labels = field_value(text, "Labels")
    if not labels:
        fail(f"{path.relative_to(ROOT)} signal note must include Labels")
    if not any(label in labels for label in ALLOWED_LABELS):
        fail(f"{path.relative_to(ROOT)} signal note Labels must include at least one market evidence label")

    notes = field_value(text, "Notes")
    if len(notes) < 30:
        fail(f"{path.relative_to(ROOT)} signal note Notes is too short")

    return urls


def validate_signal_notes() -> None:
    for path in signal_note_files_to_validate():
        validate_signal_note_file(path)


def validate_signal_note_coverage(path: Path, ledger_rows: list[dict[str, str]]) -> None:
    ledger_urls: set[str] = set()
    for row in ledger_rows:
        ledger_urls.update(extract_urls(row.get("URL", "")))
    if not ledger_urls:
        fail(f"{path.relative_to(ROOT)} Signal Ledger must include at least one URL")

    signal_note_paths = signal_note_paths_for_report(path)
    if not signal_note_paths:
        fail(f"{path.relative_to(ROOT)} Signal Ledger URLs must be covered by signals/{path.stem}-*.md notes")

    signal_urls: set[str] = set()
    for signal_path in signal_note_paths:
        signal_urls.update(validate_signal_note_file(signal_path))

    missing = sorted(ledger_urls - signal_urls)
    if missing:
        fail(
            f"{path.relative_to(ROOT)} Signal Ledger URLs missing from signals/{path.stem}-*.md notes: "
            + ", ".join(missing)
        )


def clean_table_cell(value: str) -> str:
    return value.strip().strip("`").strip()


def parse_int_cell(value: object, path: Path, row_index: str, column: str) -> int:
    text = clean_table_cell(str(value))
    if not re.fullmatch(r"\d+", text):
        fail(f"{path.relative_to(ROOT)} Money Readiness row {row_index} column `{column}` must be an integer")
    score = int(text)
    if not 0 <= score <= 5:
        fail(f"{path.relative_to(ROOT)} Money Readiness row {row_index} column `{column}` must be from 0 to 5")
    return score


def validate_money_score(value: object, context: str, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 5:
        fail(f"{context} {field} must be an integer from 0 to 5")
    return value


def split_source_classes(value: object) -> list[str]:
    if isinstance(value, list):
        raw_values = value
    else:
        text = clean_table_cell(str(value))
        text = text.replace("`", "")
        normalized_lines = []
        for line in text.splitlines():
            normalized_lines.append(re.sub(r"^\s*[-*]\s*", "", line).strip())
        text = ",".join(line for line in normalized_lines if line)
        raw_values = re.split(r"\s*,\s*|\s*;\s*", text) if text else []
    return [str(item).strip().lower() for item in raw_values if str(item).strip()]


def validate_source_classes(value: object, context: str) -> list[str]:
    source_classes = split_source_classes(value)
    if not source_classes:
        fail(f"{context} source_classes must contain at least one source class")
    duplicates = sorted({item for item in source_classes if source_classes.count(item) > 1})
    if duplicates:
        fail(f"{context} source_classes contains duplicates: {', '.join(duplicates)}")
    unsupported = sorted(set(source_classes) - STATE_SOURCE_CLASS_VALUES)
    if unsupported:
        fail(f"{context} source_classes has unsupported values: {', '.join(unsupported)}")
    return source_classes


def is_github_only(source_classes: list[str]) -> bool:
    return set(source_classes) == {"github"}


def validate_technology_shift(value: object, context: str) -> None:
    if not isinstance(value, dict):
        fail(f"{context} technology_shift must be an object")
    missing = TECHNOLOGY_SHIFT_REQUIRED_FIELDS - set(value)
    if missing:
        fail(f"{context} technology_shift missing fields: {', '.join(sorted(missing))}")

    for field in sorted(TECHNOLOGY_SHIFT_REQUIRED_FIELDS - {"affected_workflows"}):
        text = str(value.get(field, "")).strip()
        if len(text) < 3:
            fail(f"{context} technology_shift.{field} is too short")

    affected = value.get("affected_workflows")
    if not isinstance(affected, list) or not affected:
        fail(f"{context} technology_shift.affected_workflows must be a non-empty list")
    for index, workflow in enumerate(affected, start=1):
        if len(str(workflow).strip()) < 3:
            fail(f"{context} technology_shift.affected_workflows[{index}] is too short")


def normalize_report_text(value: object) -> str:
    text = clean_table_cell(str(value))
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def normalize_opportunity_key(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "", normalize_report_text(value))


def parse_build_readiness_table(path: Path, section_text: str) -> list[dict[str, str]]:
    if "None" in section_text or "No selected" in section_text:
        return []

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
    rows: list[dict[str, str]] = []
    for row_index, row in enumerate(lines[2:], start=1):
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        if len(cells) != len(header):
            fail(f"{path.relative_to(ROOT)} Build Readiness row {row_index} has {len(cells)} cells, expected {len(header)}")

        parsed = {column: clean_table_cell(cells[index]) for column, index in indexes.items()}
        parsed["_row_index"] = str(row_index)

        paid_wedge = parsed["Paid wedge"]
        distribution_channel = parsed["Distribution channel"]
        private_data_barrier = parsed["Private data barrier"]
        oss_risk = parsed["OSS commoditization risk"]
        product_shape = parsed["Product shape"]
        pricing_hypothesis = parsed["Pricing hypothesis"]
        do_not_build_until = parsed["Do not build until"]
        build_decision = normalize_stage(parsed["Build decision"])

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
        if build_decision in {"selected", "selected-for-test", "sell-before-build", "selected-for-build"}:
            if is_unclear_text(paid_wedge):
                fail(f"{path.relative_to(ROOT)} Build Readiness row {row_index} cannot be selected with an unclear paid wedge")
            if private_data_barrier in PRIVATE_DATA_BLOCKING_VALUES:
                fail(
                    f"{path.relative_to(ROOT)} Build Readiness row {row_index} cannot be selected with private data barrier "
                    f"`{private_data_barrier}`"
                )

        rows.append(parsed)

    return rows


def validate_build_readiness_table(path: Path, section_text: str) -> list[dict[str, str]]:
    return parse_build_readiness_table(path, section_text)


def parse_money_readiness_table(path: Path, section_text: str) -> list[dict[str, object]]:
    if "None" in section_text or "No selected" in section_text:
        return []

    lines = [line for line in section_text.splitlines() if line.startswith("|")]
    if len(lines) < 3:
        fail(f"{path.relative_to(ROOT)} Money Readiness must contain a markdown table with at least one row")

    header = [cell.strip() for cell in lines[0].strip().strip("|").split("|")]
    missing = MONEY_READINESS_REQUIRED_COLUMNS - set(header)
    if missing:
        fail(f"{path.relative_to(ROOT)} Money Readiness missing columns: {', '.join(sorted(missing))}")

    separator = [cell.strip() for cell in lines[1].strip().strip("|").split("|")]
    if len(separator) != len(header) or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in separator):
        fail(f"{path.relative_to(ROOT)} Money Readiness has an invalid markdown separator row")

    indexes = {name: header.index(name) for name in MONEY_READINESS_REQUIRED_COLUMNS}
    rows: list[dict[str, object]] = []
    for row_index, row in enumerate(lines[2:], start=1):
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        if len(cells) != len(header):
            fail(f"{path.relative_to(ROOT)} Money Readiness row {row_index} has {len(cells)} cells, expected {len(header)}")

        parsed: dict[str, object] = {column: clean_table_cell(cells[index]) for column, index in indexes.items()}
        parsed["_row_index"] = str(row_index)
        for column in ("Pain", "Spend", "Reachability", "Timing", "Buildability"):
            parsed[column] = parse_int_cell(parsed[column], path, str(row_index), column)

        buyer = str(parsed["Buyer"]).strip()
        existing_spend = str(parsed["Existing spend"]).strip()
        paid_experiment = str(parsed["Paid experiment"]).strip()
        if len(buyer) < 20:
            fail(f"{path.relative_to(ROOT)} Money Readiness row {row_index} buyer is too short")
        if len(existing_spend) < 20:
            fail(f"{path.relative_to(ROOT)} Money Readiness row {row_index} existing spend is too short")
        if len(paid_experiment) < 30:
            fail(f"{path.relative_to(ROOT)} Money Readiness row {row_index} paid experiment is too short")

        source_classes = validate_source_classes(parsed["Source classes"], f"{path.relative_to(ROOT)} Money Readiness row {row_index}")
        parsed["Source classes"] = source_classes

        stage = normalize_stage(parsed["Stage"])
        if stage not in STATE_STAGE_VALUES:
            fail(f"{path.relative_to(ROOT)} Money Readiness row {row_index} has unsupported stage: {stage}")
        if stage in {"selected", "selected-for-test", "sell-before-build", "selected-for-build"}:
            if int(parsed["Spend"]) < 2:
                fail(f"{path.relative_to(ROOT)} Money Readiness row {row_index} cannot be selected with spend below 2")
            if int(parsed["Reachability"]) < 2:
                fail(f"{path.relative_to(ROOT)} Money Readiness row {row_index} cannot be selected with reachability below 2")
            if len(source_classes) < 2 or is_github_only(source_classes):
                fail(f"{path.relative_to(ROOT)} Money Readiness row {row_index} cannot be selected with GitHub-only or single-class evidence")
        if stage == "selected-for-build":
            if int(parsed["Spend"]) < 3:
                fail(f"{path.relative_to(ROOT)} Money Readiness row {row_index} cannot be selected-for-build with spend below 3")
            if int(parsed["Reachability"]) < 3:
                fail(f"{path.relative_to(ROOT)} Money Readiness row {row_index} cannot be selected-for-build with reachability below 3")
            if int(parsed["Timing"]) < 2:
                fail(f"{path.relative_to(ROOT)} Money Readiness row {row_index} cannot be selected-for-build with timing below 2")
            if int(parsed["Buildability"]) < 3:
                fail(f"{path.relative_to(ROOT)} Money Readiness row {row_index} cannot be selected-for-build with buildability below 3")
            if len(source_classes) < 3:
                fail(f"{path.relative_to(ROOT)} Money Readiness row {row_index} cannot be selected-for-build with fewer than 3 source classes")
            if is_unclear_text(paid_experiment):
                fail(f"{path.relative_to(ROOT)} Money Readiness row {row_index} cannot be selected-for-build with an unclear paid experiment")

        rows.append(parsed)

    return rows


def validate_money_readiness_table(path: Path, section_text: str) -> list[dict[str, object]]:
    return parse_money_readiness_table(path, section_text)


def is_unclear_text(value: object) -> bool:
    text = str(value).strip().lower()
    if not text:
        return True
    return any(marker in text for marker in UNCLEAR_TEXT_MARKERS)


def normalize_stage(value: object) -> str:
    return str(value).strip().lower().replace("_", "-")


def read_opportunities_state() -> dict[str, object]:
    data_path = require_path("opportunities.json")
    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"opportunities.json is not valid JSON: {exc}")

    if not isinstance(data, dict):
        fail("opportunities.json must be an object")
    return data


def state_stage_for_entry(array_name: str, entry: dict[str, object]) -> str:
    stage = entry.get("stage")
    if stage is not None:
        return normalize_stage(stage)
    if array_name == "watchlisted":
        return "watchlist"
    return array_name


def build_state_entry_lookup(data: dict[str, object]) -> dict[str, tuple[str, int, dict[str, object]]]:
    lookup: dict[str, tuple[str, int, dict[str, object]]] = {}
    for array_name in STATE_ARRAY_FIELDS:
        entries = data.get(array_name, [])
        if not isinstance(entries, list):
            continue
        for index, entry in enumerate(entries, start=1):
            if not isinstance(entry, dict):
                continue
            keys = {
                normalize_opportunity_key(entry.get("id", "")),
                normalize_opportunity_key(entry.get("title", "")),
            }
            for key in keys:
                if not key:
                    continue
                previous = lookup.get(key)
                if previous is not None and previous[2] is not entry:
                    fail(f"opportunities.json has duplicate opportunity lookup key: {key}")
                lookup[key] = (array_name, index, entry)
    return lookup


def validate_build_readiness_state_consistency(
    path: Path,
    rows: list[dict[str, str]],
    state_entries: dict[str, tuple[str, int, dict[str, object]]],
) -> None:
    for row in rows:
        row_index = row["_row_index"]
        opportunity = row["Opportunity"]
        key = normalize_opportunity_key(opportunity)
        match = state_entries.get(key)
        if match is None:
            fail(f"{path.relative_to(ROOT)} Build Readiness row {row_index} opportunity is missing from opportunities.json: {opportunity}")

        array_name, state_index, entry = match
        actual_decision = normalize_stage(row["Build decision"])
        expected_decision = state_stage_for_entry(array_name, entry)
        if actual_decision != expected_decision:
            fail(
                f"{path.relative_to(ROOT)} Build Readiness row {row_index} decision `{actual_decision}` "
                f"does not match opportunities.json {array_name}[{state_index}] stage `{expected_decision}`"
            )

        for column, state_field in BUILD_READINESS_STATE_FIELDS.items():
            actual_value = normalize_report_text(row[column])
            expected_value = normalize_report_text(entry.get(state_field, ""))
            if actual_value != expected_value:
                fail(
                    f"{path.relative_to(ROOT)} Build Readiness row {row_index} column `{column}` "
                    f"does not match opportunities.json {array_name}[{state_index}].{state_field}"
                )


def validate_money_readiness_state_consistency(
    path: Path,
    rows: list[dict[str, object]],
    state_entries: dict[str, tuple[str, int, dict[str, object]]],
) -> None:
    for row in rows:
        row_index = str(row["_row_index"])
        opportunity = row["Opportunity"]
        key = normalize_opportunity_key(opportunity)
        match = state_entries.get(key)
        if match is None:
            fail(f"{path.relative_to(ROOT)} Money Readiness row {row_index} opportunity is missing from opportunities.json: {opportunity}")

        array_name, state_index, entry = match
        actual_stage = normalize_stage(row["Stage"])
        expected_stage = state_stage_for_entry(array_name, entry)
        if actual_stage != expected_stage:
            fail(
                f"{path.relative_to(ROOT)} Money Readiness row {row_index} stage `{actual_stage}` "
                f"does not match opportunities.json {array_name}[{state_index}] stage `{expected_stage}`"
            )

        for column, state_field in MONEY_READINESS_STATE_FIELDS.items():
            if column == "Source classes":
                actual_classes = split_source_classes(row[column])
                expected_classes = split_source_classes(entry.get(state_field, []))
                if actual_classes != expected_classes:
                    fail(
                        f"{path.relative_to(ROOT)} Money Readiness row {row_index} column `{column}` "
                        f"does not match opportunities.json {array_name}[{state_index}].{state_field}"
                    )
                continue

            actual_value = normalize_report_text(row[column])
            expected_value = normalize_report_text(entry.get(state_field, ""))
            if actual_value != expected_value:
                fail(
                    f"{path.relative_to(ROOT)} Money Readiness row {row_index} column `{column}` "
                    f"does not match opportunities.json {array_name}[{state_index}].{state_field}"
                )


def parse_money_scores_section(path_label: str, text: str) -> dict[str, int]:
    scores: dict[str, int] = {}
    for label, field in (
        ("Pain", "pain_score"),
        ("Spend", "spend_score"),
        ("Reachability", "reachability_score"),
        ("Timing", "timing_score"),
        ("Buildability", "buildability_score"),
    ):
        match = re.search(rf"(?im)^\s*(?:[-*]\s*)?{label}\s*:\s*(\d+)\s*$", text)
        if not match:
            fail(f"{path_label} Money-First Scores must include `{label}: N`")
        score = int(match.group(1))
        if not 0 <= score <= 5:
            fail(f"{path_label} Money-First Scores `{label}` must be from 0 to 5")
        scores[field] = score
    return scores


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

    source_classes = validate_source_classes(sections.get("Source Classes", ""), path_label) if sections.get("Source Classes") else []
    money_scores = parse_money_scores_section(path_label, sections["Money-First Scores"]) if "Money-First Scores" in sections else {}
    paid_experiment = sections.get("Paid Experiment", "")

    decision = sections.get("Decision", "")
    if "selected for test" in decision.lower() or "selected-for-test" in decision.lower() or "sell-before-build" in decision.lower():
        if is_unclear_text(sections.get("Paid Wedge", "")):
            fail(f"{path_label} cannot be selected with an unclear Paid Wedge")
        if private_data_barrier in PRIVATE_DATA_BLOCKING_VALUES:
            fail(f"{path_label} cannot be selected with Private Data Barrier `{private_data_barrier}`")
        if money_scores.get("spend_score", 0) < 2:
            fail(f"{path_label} cannot be selected with Spend score below 2")
        if money_scores.get("reachability_score", 0) < 2:
            fail(f"{path_label} cannot be selected with Reachability score below 2")
        if len(source_classes) < 2 or is_github_only(source_classes):
            fail(f"{path_label} cannot be selected with GitHub-only or single-class evidence")
        if is_unclear_text(paid_experiment):
            fail(f"{path_label} cannot be selected with an unclear Paid Experiment")
    if "selected for build" in decision.lower() or "selected-for-build" in decision.lower():
        if is_unclear_text(sections.get("Paid Wedge", "")):
            fail(f"{path_label} cannot be selected for build with an unclear Paid Wedge")
        if private_data_barrier in PRIVATE_DATA_BLOCKING_VALUES:
            fail(f"{path_label} cannot be selected for build with Private Data Barrier `{private_data_barrier}`")
        if money_scores.get("spend_score", 0) < 3:
            fail(f"{path_label} cannot be selected for build with Spend score below 3")
        if money_scores.get("reachability_score", 0) < 3:
            fail(f"{path_label} cannot be selected for build with Reachability score below 3")
        if money_scores.get("timing_score", 0) < 2:
            fail(f"{path_label} cannot be selected for build with Timing score below 2")
        if money_scores.get("buildability_score", 0) < 3:
            fail(f"{path_label} cannot be selected for build with Buildability score below 3")
        if len(source_classes) < 3:
            fail(f"{path_label} cannot be selected for build with fewer than 3 source classes")
        if is_unclear_text(paid_experiment):
            fail(f"{path_label} cannot be selected for build with an unclear Paid Experiment")


def validate_report_structure() -> None:
    state_entries = build_state_entry_lookup(read_opportunities_state())
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

        signal_ledger_rows = validate_signal_ledger(path, sections["Signal Ledger"])
        validate_signal_note_coverage(path, signal_ledger_rows)
        build_readiness_rows = validate_build_readiness_table(path, sections["Build Readiness"])
        validate_build_readiness_state_consistency(path, build_readiness_rows, state_entries)
        money_readiness_rows = validate_money_readiness_table(path, sections["Money Readiness"])
        validate_money_readiness_state_consistency(path, money_readiness_rows, state_entries)

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
    data = read_opportunities_state()

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
            context = f"opportunities.json {field}[{index}]"
            money_scores = {score_field: validate_money_score(entry[score_field], context, score_field) for score_field in MONEY_SCORE_FIELDS}
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
            validate_technology_shift(entry["technology_shift"], context)
            buyer = str(entry["buyer"]).strip()
            if len(buyer) < 20:
                fail(f"opportunities.json {field}[{index}] buyer is too short")
            expensive_workflow = str(entry["expensive_workflow"]).strip()
            if len(expensive_workflow) < 30:
                fail(f"opportunities.json {field}[{index}] expensive_workflow is too short")
            existing_spend = str(entry["existing_spend"]).strip()
            if len(existing_spend) < 20:
                fail(f"opportunities.json {field}[{index}] existing_spend is too short")
            paid_experiment = str(entry["paid_experiment"]).strip()
            if len(paid_experiment) < 30:
                fail(f"opportunities.json {field}[{index}] paid_experiment is too short")
            source_classes = validate_source_classes(entry["source_classes"], context)
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
            if stage is not None and normalize_stage(stage) not in STATE_STAGE_VALUES_BY_ARRAY[field]:
                fail(
                    f"opportunities.json {field}[{index}] stage `{normalize_stage(stage)}` "
                    f"does not match containing array `{field}`"
                )
            if field == "selected":
                if is_unclear_text(paid_wedge):
                    fail(f"opportunities.json selected[{index}] has unclear paid_wedge; keep it in watchlisted")
                if private_data_barrier in PRIVATE_DATA_BLOCKING_VALUES:
                    fail(f"opportunities.json selected[{index}] requires private data/code or has unclear barrier; keep it in watchlisted")
                if money_scores["spend_score"] < 2:
                    fail(f"opportunities.json selected[{index}] spend_score is below 2; keep it in watchlisted")
                if money_scores["reachability_score"] < 2:
                    fail(f"opportunities.json selected[{index}] reachability_score is below 2; keep it in watchlisted")
                if len(source_classes) < 2 or is_github_only(source_classes):
                    fail(f"opportunities.json selected[{index}] has GitHub-only or single-class evidence; keep it in watchlisted")
                if is_unclear_text(paid_experiment):
                    fail(f"opportunities.json selected[{index}] paid_experiment is unclear; keep it in watchlisted")
            if normalize_stage(stage) == "selected-for-build":
                if is_unclear_text(paid_wedge):
                    fail(f"opportunities.json {field}[{index}] cannot be selected-for-build with an unclear paid_wedge")
                if private_data_barrier in PRIVATE_DATA_BLOCKING_VALUES:
                    fail(f"opportunities.json {field}[{index}] cannot be selected-for-build with private_data_barrier `{private_data_barrier}`")
                if money_scores["spend_score"] < 3:
                    fail(f"opportunities.json {field}[{index}] cannot be selected-for-build with spend_score below 3")
                if money_scores["reachability_score"] < 3:
                    fail(f"opportunities.json {field}[{index}] cannot be selected-for-build with reachability_score below 3")
                if money_scores["timing_score"] < 2:
                    fail(f"opportunities.json {field}[{index}] cannot be selected-for-build with timing_score below 2")
                if money_scores["buildability_score"] < 3:
                    fail(f"opportunities.json {field}[{index}] cannot be selected-for-build with buildability_score below 3")
                if len(source_classes) < 3:
                    fail(f"opportunities.json {field}[{index}] cannot be selected-for-build with fewer than 3 source classes")
                if is_unclear_text(paid_experiment):
                    fail(f"opportunities.json {field}[{index}] cannot be selected-for-build with an unclear paid_experiment")

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
    validate_signal_notes()
    validate_selected_opportunity_files()
    print("opportunity radar artifacts validated")


if __name__ == "__main__":
    main()
