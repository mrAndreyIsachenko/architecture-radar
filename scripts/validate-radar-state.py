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
    "source",
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
    "company",
    "product",
    "launch",
    "model",
    "dataset",
    "benchmark",
    "runtime",
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
    "watch-company",
    "watch-product",
    "watch-launch",
    "watch-model",
    "watch-dataset",
    "watch-benchmark",
    "watch-runtime",
}
WATCHLIST_NON_REPOSITORY_ARTIFACT_TYPES = {"company", "product", "launch"}
WATCHLIST_NON_REPOSITORY_REVIEW_MODES = {"watch-company", "watch-product", "watch-launch"}
REQUIRED_REPORT_SECTIONS = {
    "Prerequisites And State",
    "Candidate Counts",
    "Selected Repositories",
    "Executive Summary",
    "Review Value",
    "Detailed Reviews",
    "Extracted Or Updated Patterns",
    "Relevance To Explicit Problems In `interests.md`",
    "Candidate Ledger",
    "Recommended Next Action",
    "Notable Rejected Or Deferred Candidates",
    "Unresolved Evidence Gaps",
    "Validation Backlog Updates",
}
LEDGER_REQUIRED_COLUMNS = {
    "Repository",
    "URL",
    "Commit",
    "Discovery source",
    "Family",
    "Stage",
    "Decision",
}
REVIEW_VALUE_REQUIRED_COLUMNS = {
    "Verdict",
    "Score",
    "Reason",
    "Recommended action",
}
REVIEW_VALUE_VERDICTS = {
    "high-signal",
    "useful-delta",
    "no-candidate-cleared",
    "watchlist-only",
    "weak-signal",
    "stale-or-duplicate",
    "no-material-change",
    "needs-targeted-fix",
}
REVIEW_VALUE_LOW_VERDICTS = {
    "weak-signal",
    "stale-or-duplicate",
    "no-material-change",
    "needs-targeted-fix",
}
REVIEW_VALUE_ACTIONS = {"merge", "request-fix", "close", "watchlist"}
FAMILY_PLAYBOOKS = {
    "privacy-networking-vpn": "docs/family-playbooks/privacy-networking-vpn.md",
    "drones-robotics-autonomy": "docs/family-playbooks/drones-robotics-autonomy.md",
    "satellites-space-systems": "docs/family-playbooks/satellites-space-systems.md",
}
FAMILY_PLAYBOOK_REQUIRED_HEADINGS = {
    "Family",
    "Mechanisms To Search",
    "Evidence Bar",
    "Selection Bias",
    "Rejection Triggers",
    "Validation Evidence",
    "Useful Search Seeds",
}
BACKLOG_PATH = "experiments/failure-injection-backlog.yml"
BACKLOG_REQUIRED_FIELDS = {
    "id",
    "family",
    "source_report",
    "source_repository",
    "mechanism",
    "evidence_gap",
    "validation_type",
    "proposed_validation",
    "success_condition",
    "priority",
    "status",
    "created",
    "last_updated",
}
BACKLOG_VALIDATION_TYPES = {
    "runtime",
    "failure-injection",
    "restart-recovery",
    "reconnect-recovery",
    "replay",
    "sitl",
    "fleet",
    "operational",
}
BACKLOG_PRIORITIES = {"high", "medium", "low"}
BACKLOG_STATUSES = {"open", "planned", "running", "passed", "failed", "deferred", "closed"}
VALIDATION_BACKLOG_REQUIRED_COLUMNS = {
    "Backlog item",
    "Repository",
    "Family",
    "Validation type",
    "Reason",
    "Status",
}
NO_BACKLOG_UPDATE_RE = re.compile(r"\bno (?:validation )?backlog update (?:was )?required\b", re.IGNORECASE)
RUNTIME_VALIDATION_KEYWORDS = (
    "runtime validation",
    "failure-injection",
    "failure injection",
    "restart",
    "reconnect",
    "replay",
    "sitl",
    "fleet",
    "operational validation",
)


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
    base_ref = os.environ.get("ARCHITECTURE_RADAR_BASE_REF") or os.environ.get("GITHUB_BASE_REF")
    diff_range = ["HEAD"]

    if base_ref:
        remote_base = f"origin/{base_ref}"
        try:
            subprocess.run(
                ["git", "rev-parse", "--verify", remote_base],
                check=True,
                capture_output=True,
                text=True,
            )
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


def report_files_to_validate() -> list[Path]:
    paths: set[Path] = set()

    for path in changed_artifact_files():
        if path.parent == ROOT / "reports":
            paths.add(path)

    if RUN_DATE:
        paths.add(ROOT / "reports" / f"{RUN_DATE}.md")

    if SUPPLEMENT_REQUIRED in {"1", "true", "yes", "on"} and SUPPLEMENT_REPORT:
        paths.add(ROOT / SUPPLEMENT_REPORT)

    return sorted(path for path in paths if path.name.endswith(".md"))


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


def validate_candidate_ledger(path: Path, section_text: str) -> list[dict[str, str]]:
    lines = [line for line in section_text.splitlines() if line.startswith("|")]
    if len(lines) < 3:
        fail(f"{path.relative_to(ROOT)} Candidate Ledger must contain a markdown table with at least one row")

    header = [cell.strip() for cell in lines[0].strip().strip("|").split("|")]
    missing = LEDGER_REQUIRED_COLUMNS - set(header)
    if missing:
        fail(f"{path.relative_to(ROOT)} Candidate Ledger missing columns: {', '.join(sorted(missing))}")

    separator = [cell.strip() for cell in lines[1].strip().strip("|").split("|")]
    if len(separator) != len(header) or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in separator):
        fail(f"{path.relative_to(ROOT)} Candidate Ledger has an invalid markdown separator row")

    data_rows = lines[2:]
    rows: list[dict[str, str]] = []
    for row_index, row in enumerate(data_rows, start=1):
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        if len(cells) != len(header):
            fail(f"{path.relative_to(ROOT)} Candidate Ledger row {row_index} has {len(cells)} cells, expected {len(header)}")
        rows.append(dict(zip(header, cells)))

    return rows


def clean_markdown_code(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value.startswith("`") and value.endswith("`"):
        return value[1:-1].strip()
    return value


def validate_review_value(path: Path, section_text: str) -> None:
    lines = [line for line in section_text.splitlines() if line.startswith("|")]
    if len(lines) < 3:
        fail(f"{path.relative_to(ROOT)} Review Value must contain a markdown table with one row")

    header = [cell.strip() for cell in lines[0].strip().strip("|").split("|")]
    missing = REVIEW_VALUE_REQUIRED_COLUMNS - set(header)
    if missing:
        fail(f"{path.relative_to(ROOT)} Review Value missing columns: {', '.join(sorted(missing))}")

    separator = [cell.strip() for cell in lines[1].strip().strip("|").split("|")]
    if len(separator) != len(header) or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in separator):
        fail(f"{path.relative_to(ROOT)} Review Value has an invalid markdown separator row")

    data_rows = lines[2:]
    if len(data_rows) != 1:
        fail(f"{path.relative_to(ROOT)} Review Value must contain exactly one data row")

    cells = [cell.strip() for cell in data_rows[0].strip().strip("|").split("|")]
    if len(cells) != len(header):
        fail(f"{path.relative_to(ROOT)} Review Value row has {len(cells)} cells, expected {len(header)}")

    row = dict(zip(header, cells))
    verdict = clean_markdown_code(row["Verdict"])
    action = clean_markdown_code(row["Recommended action"])
    score_text = clean_markdown_code(row["Score"])
    reason = row["Reason"].strip()

    if verdict not in REVIEW_VALUE_VERDICTS:
        fail(f"{path.relative_to(ROOT)} Review Value has unsupported verdict: {verdict}")
    if action not in REVIEW_VALUE_ACTIONS:
        fail(f"{path.relative_to(ROOT)} Review Value has unsupported recommended action: {action}")
    if not re.fullmatch(r"\d+", score_text):
        fail(f"{path.relative_to(ROOT)} Review Value score must be an integer from 0 to 5")
    score = int(score_text)
    if score < 0 or score > 5:
        fail(f"{path.relative_to(ROOT)} Review Value score must be an integer from 0 to 5")
    if len(reason) < 30:
        fail(f"{path.relative_to(ROOT)} Review Value reason is too short")
    if verdict in REVIEW_VALUE_LOW_VERDICTS and action == "merge":
        fail(f"{path.relative_to(ROOT)} Review Value low-value verdict `{verdict}` cannot recommend merge")


def selected_ledger_rows(ledger_rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    selected: dict[tuple[str, str], dict[str, str]] = {}
    for row in ledger_rows:
        decision = clean_markdown_code(row.get("Decision", "")).lower()
        if "selected" not in decision:
            continue
        repository = clean_markdown_code(row.get("Repository", ""))
        family = clean_markdown_code(row.get("Family", ""))
        if repository and family:
            selected[(repository, family)] = row
    return selected


def section_has_runtime_validation_gap(section_text: str) -> bool:
    normalized = section_text.lower()
    return any(keyword in normalized for keyword in RUNTIME_VALIDATION_KEYWORDS)


def validate_validation_backlog_updates(
    path: Path,
    section_text: str,
    *,
    backlog_items: dict[str, dict[str, str]],
    ledger_rows: list[dict[str, str]],
    evidence_gaps: str,
) -> None:
    lines = [line for line in section_text.splitlines() if line.startswith("|")]
    has_runtime_gap = section_has_runtime_validation_gap(evidence_gaps)
    selected_rows = selected_ledger_rows(ledger_rows)

    if not lines:
        if not NO_BACKLOG_UPDATE_RE.search(section_text):
            fail(
                f"{path.relative_to(ROOT)} Validation Backlog Updates must contain a backlog table "
                "or state that no validation backlog update was required"
            )
        if has_runtime_gap and selected_rows:
            fail(f"{path.relative_to(ROOT)} records a runtime evidence gap but has no validation backlog item")
        return

    if len(lines) < 3:
        fail(f"{path.relative_to(ROOT)} Validation Backlog Updates must contain a markdown table with at least one row")

    header = [cell.strip() for cell in lines[0].strip().strip("|").split("|")]
    missing = VALIDATION_BACKLOG_REQUIRED_COLUMNS - set(header)
    if missing:
        fail(f"{path.relative_to(ROOT)} Validation Backlog Updates missing columns: {', '.join(sorted(missing))}")

    separator = [cell.strip() for cell in lines[1].strip().strip("|").split("|")]
    if len(separator) != len(header) or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in separator):
        fail(f"{path.relative_to(ROOT)} Validation Backlog Updates has an invalid markdown separator row")

    for row_index, row in enumerate(lines[2:], start=1):
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        if len(cells) != len(header):
            fail(
                f"{path.relative_to(ROOT)} Validation Backlog Updates row {row_index} "
                f"has {len(cells)} cells, expected {len(header)}"
            )
        row_data = dict(zip(header, cells))
        item_id = clean_markdown_code(row_data["Backlog item"])
        repository = clean_markdown_code(row_data["Repository"])
        family = clean_markdown_code(row_data["Family"])
        validation_type = clean_markdown_code(row_data["Validation type"])
        status = clean_markdown_code(row_data["Status"])

        item = backlog_items.get(item_id)
        if item is None:
            fail(f"{path.relative_to(ROOT)} references unknown validation backlog item: {item_id}")
        if item["source_repository"] != repository:
            fail(
                f"{path.relative_to(ROOT)} backlog item `{item_id}` repository mismatch: "
                f"{repository} != {item['source_repository']}"
            )
        if item["family"] != family:
            fail(f"{path.relative_to(ROOT)} backlog item `{item_id}` family mismatch: {family} != {item['family']}")
        if item["validation_type"] != validation_type:
            fail(
                f"{path.relative_to(ROOT)} backlog item `{item_id}` validation type mismatch: "
                f"{validation_type} != {item['validation_type']}"
            )
        if item["status"] != status:
            fail(f"{path.relative_to(ROOT)} backlog item `{item_id}` status mismatch: {status} != {item['status']}")
        if selected_rows and (repository, family) not in selected_rows:
            fail(f"{path.relative_to(ROOT)} backlog item `{item_id}` does not match a selected ledger row")


def validate_report_structure(backlog_items: dict[str, dict[str, str]] | None = None) -> None:
    backlog_items = backlog_items or {}
    for path in report_files_to_validate():
        if not path.is_file():
            fail(f"missing report: {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            fail(f"report is empty: {path.relative_to(ROOT)}")

        sections = markdown_sections(text)
        missing = REQUIRED_REPORT_SECTIONS - set(sections)
        if missing:
            fail(f"{path.relative_to(ROOT)} missing required report sections: {', '.join(sorted(missing))}")

        for section in REQUIRED_REPORT_SECTIONS:
            if not sections[section].strip():
                fail(f"{path.relative_to(ROOT)} section is empty: {section}")

        ledger_rows = validate_candidate_ledger(path, sections["Candidate Ledger"])
        validate_review_value(path, sections["Review Value"])
        validate_validation_backlog_updates(
            path,
            sections["Validation Backlog Updates"],
            backlog_items=backlog_items,
            ledger_rows=ledger_rows,
            evidence_gaps=sections["Unresolved Evidence Gaps"],
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


def interests_topic_families() -> set[str]:
    interests = require_path("interests.md").read_text(encoding="utf-8")
    families: set[str] = set()
    in_family_list = False

    for line in interests.splitlines():
        if line.startswith("Use these top-level topic families"):
            in_family_list = True
            continue
        if in_family_list and line.startswith("## "):
            break
        if not in_family_list:
            continue
        match = re.match(r"- `([^`]+)`:", line)
        if match:
            families.add(match.group(1))

    if not families:
        fail("interests.md has no topic families")
    return families


def validate_topic_family_consistency() -> None:
    scope_families = topic_families()
    interests_families = interests_topic_families()
    missing_from_interests = scope_families - interests_families
    missing_from_scope = interests_families - scope_families

    if missing_from_interests:
        fail(f"topic families missing from interests.md: {', '.join(sorted(missing_from_interests))}")
    if missing_from_scope:
        fail(f"topic families missing from docs/research-scope.md: {', '.join(sorted(missing_from_scope))}")


def validate_family_playbooks() -> None:
    require_path("docs/family-playbooks", directory=True)
    families = topic_families()

    for family, relpath in FAMILY_PLAYBOOKS.items():
        if family not in families:
            fail(f"family playbook `{relpath}` is configured for unknown family: {family}")
        path = require_path(relpath)
        sections = markdown_sections(path.read_text(encoding="utf-8"))
        missing = FAMILY_PLAYBOOK_REQUIRED_HEADINGS - set(sections)
        if missing:
            fail(f"{relpath} missing required headings: {', '.join(sorted(missing))}")
        if f"`{family}`" not in sections["Family"]:
            fail(f"{relpath} Family section must name `{family}`")


def parse_failure_backlog_yaml() -> list[dict[str, str]]:
    path = require_path(BACKLOG_PATH)
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        fail(f"{BACKLOG_PATH} is empty")
    if "\t" in text:
        fail(f"{BACKLOG_PATH} must use spaces, not tabs")

    saw_items = False
    explicit_empty = False
    items: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        if raw_line == "items: []":
            if saw_items:
                fail(f"{BACKLOG_PATH}:{line_number} duplicate top-level `items`")
            saw_items = True
            explicit_empty = True
            continue
        if raw_line == "items:":
            if saw_items:
                fail(f"{BACKLOG_PATH}:{line_number} duplicate top-level `items`")
            saw_items = True
            continue

        if not saw_items:
            fail(f"{BACKLOG_PATH}:{line_number} expected top-level `items:` before backlog entries")
        if explicit_empty:
            fail(f"{BACKLOG_PATH}:{line_number} cannot add entries after `items: []`")

        if raw_line.startswith("  - "):
            if current is not None:
                items.append(current)
            current = {}
            payload = raw_line[4:]
            if payload:
                if ": " not in payload:
                    fail(f"{BACKLOG_PATH}:{line_number} expected `key: value` after list marker")
                key, value = payload.split(": ", 1)
                if key not in BACKLOG_REQUIRED_FIELDS:
                    fail(f"{BACKLOG_PATH}:{line_number} unsupported backlog field: {key}")
                current[key] = clean_yaml_scalar(value)
            continue

        if raw_line.startswith("    "):
            if current is None:
                fail(f"{BACKLOG_PATH}:{line_number} expected a backlog entry")
            payload = raw_line[4:]
            if ": " not in payload:
                fail(f"{BACKLOG_PATH}:{line_number} expected `key: value`")
            key, value = payload.split(": ", 1)
            if key not in BACKLOG_REQUIRED_FIELDS:
                fail(f"{BACKLOG_PATH}:{line_number} unsupported backlog field: {key}")
            current[key] = clean_yaml_scalar(value)
            continue

        fail(f"{BACKLOG_PATH}:{line_number} unsupported indentation or syntax")

    if current is not None:
        items.append(current)
    if not saw_items:
        fail(f"{BACKLOG_PATH} is missing top-level `items:`")

    return items


def validate_failure_backlog() -> dict[str, dict[str, str]]:
    items = parse_failure_backlog_yaml()
    families = topic_families()
    by_id: dict[str, dict[str, str]] = {}

    for index, item in enumerate(items, start=1):
        missing = BACKLOG_REQUIRED_FIELDS - set(item)
        if missing:
            fail(f"{BACKLOG_PATH} item {index} missing required fields: {', '.join(sorted(missing))}")
        extra = set(item) - BACKLOG_REQUIRED_FIELDS
        if extra:
            fail(f"{BACKLOG_PATH} item {index} has unsupported fields: {', '.join(sorted(extra))}")

        item_id = item["id"]
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", item_id):
            fail(f"{BACKLOG_PATH} item {index} has invalid id: {item_id}")
        if item_id in by_id:
            fail(f"{BACKLOG_PATH} has duplicate item id: {item_id}")
        if item["family"] not in families:
            fail(f"{BACKLOG_PATH} item `{item_id}` has unknown family: {item['family']}")
        if not re.fullmatch(r"reports/\d{4}-\d{2}-\d{2}(?:-supplement-\d+)?\.md", item["source_report"]):
            fail(f"{BACKLOG_PATH} item `{item_id}` has invalid source_report: {item['source_report']}")
        if not re.fullmatch(r"[^/\s]+/[^/\s]+", item["source_repository"]):
            fail(f"{BACKLOG_PATH} item `{item_id}` has invalid source_repository: {item['source_repository']}")
        if item["validation_type"] not in BACKLOG_VALIDATION_TYPES:
            fail(f"{BACKLOG_PATH} item `{item_id}` has unsupported validation_type: {item['validation_type']}")
        if item["priority"] not in BACKLOG_PRIORITIES:
            fail(f"{BACKLOG_PATH} item `{item_id}` has unsupported priority: {item['priority']}")
        if item["status"] not in BACKLOG_STATUSES:
            fail(f"{BACKLOG_PATH} item `{item_id}` has unsupported status: {item['status']}")
        for date_field in ("created", "last_updated"):
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", item[date_field]):
                fail(f"{BACKLOG_PATH} item `{item_id}` has invalid {date_field}: {item[date_field]}")
        for text_field in ("mechanism", "evidence_gap", "proposed_validation", "success_condition"):
            if len(item[text_field].strip()) < 10:
                fail(f"{BACKLOG_PATH} item `{item_id}` {text_field} is too short")

        by_id[item_id] = item

    return by_id


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
    required = {"family", "artifact_type", "priority", "status", "review_mode", "reason"}

    for index, entry in enumerate(entries, start=1):
        missing = required - set(entry)
        if missing:
            fail(f"watchlist.yml entry {index} missing required fields: {', '.join(sorted(missing))}")
        repository = str(entry.get("repository", "")).strip()
        source = str(entry.get("source", "")).strip()
        if not repository and not source:
            fail(f"watchlist.yml entry {index} must include either repository or source")
        if repository and not re.fullmatch(r"[^/\s]+/[^/\s]+", repository):
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
        if not repository:
            if artifact_type not in WATCHLIST_NON_REPOSITORY_ARTIFACT_TYPES:
                fail(f"watchlist.yml entry {index} without repository must use a company, product, or launch artifact_type")
            if review_mode not in WATCHLIST_NON_REPOSITORY_REVIEW_MODES:
                fail(f"watchlist.yml entry {index} without repository must use watch-company, watch-product, or watch-launch")
        reason = str(entry["reason"]).strip()
        if len(reason) < 20:
            fail(f"watchlist.yml entry {index} reason is too short")


def validate_workspace() -> None:
    require_path("interests.md")
    require_path("watchlist.yml")
    require_path("radar.json")
    require_path("reports", directory=True)
    require_path("repositories", directory=True)
    require_path("patterns", directory=True)
    require_path("docs/family-playbooks", directory=True)
    require_path(BACKLOG_PATH)
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


def main() -> None:
    validate_workspace()
    validate_topic_family_consistency()
    validate_family_playbooks()
    backlog_items = validate_failure_backlog()
    validate_evidence_labels()
    validate_report_structure(backlog_items)
    validate_watchlist()

    print("radar artifacts validated")


if __name__ == "__main__":
    main()
