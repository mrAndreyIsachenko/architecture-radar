#!/usr/bin/env python3
"""Extract a compact machine-readable summary from Architecture Radar reports."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


DEFAULT_REPORT_DIR = Path("reports")
LIST_MARKER_RE = re.compile(r"^\s*[-*]\s+(.+?)\s*$")
TOTAL_CANDIDATES_RE = re.compile(r"Total candidates reaching at least `triaged`:\s*(\d+)")
STAGE_COUNT_RE = re.compile(r"-\s+`([^`]+)`:\s*(\d+)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reports", nargs="*", type=Path, help="Report Markdown files to summarize.")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    return parser.parse_args()


def latest_report() -> Path:
    reports = sorted(DEFAULT_REPORT_DIR.glob("*.md"))
    if not reports:
        raise SystemExit("no reports/*.md files found")
    return reports[-1]


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


def list_items(section_text: str) -> list[str]:
    items: list[str] = []
    for line in section_text.splitlines():
        match = LIST_MARKER_RE.match(line)
        if match:
            items.append(match.group(1).strip())
    return items


def plain_text(section_text: str) -> str:
    return "\n".join(line.rstrip() for line in section_text.splitlines()).strip()


def parse_candidate_counts(section_text: str) -> dict[str, object]:
    stage_counts: dict[str, int] = {}
    total: int | None = None

    for line in section_text.splitlines():
        stage_match = STAGE_COUNT_RE.match(line.strip())
        if stage_match:
            stage_counts[stage_match.group(1)] = int(stage_match.group(2))
            continue

        total_match = TOTAL_CANDIDATES_RE.search(line)
        if total_match:
            total = int(total_match.group(1))

    return {
        "total_triaged": total,
        "stage_counts": stage_counts,
    }


def parse_table(section_text: str) -> list[dict[str, str]]:
    lines = [line for line in section_text.splitlines() if line.startswith("|")]
    if len(lines) < 3:
        return []

    header = [cell.strip() for cell in lines[0].strip().strip("|").split("|")]
    rows: list[dict[str, str]] = []

    for line in lines[2:]:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != len(header):
            continue
        rows.append(dict(zip(header, cells)))

    return rows


def clean_markdown_code(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value.startswith("`") and value.endswith("`"):
        return value[1:-1].strip()
    return value


def parse_review_value(section_text: str) -> dict[str, object]:
    rows = parse_table(section_text)
    if not rows:
        return {}

    row = rows[0]
    score_text = clean_markdown_code(str(row.get("Score", "")))
    score: int | None = int(score_text) if re.fullmatch(r"\d+", score_text) else None
    return {
        "verdict": clean_markdown_code(str(row.get("Verdict", ""))),
        "score": score,
        "reason": str(row.get("Reason", "")).strip(),
        "recommended_action": clean_markdown_code(str(row.get("Recommended action", ""))),
    }


def report_title(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def summarize_report_text(text: str, path: str | Path) -> dict[str, object]:
    sections = markdown_sections(text)
    candidate_counts = parse_candidate_counts(sections.get("Candidate Counts", ""))
    ledger_rows = parse_table(sections.get("Candidate Ledger", ""))
    selected = list_items(sections.get("Selected Repositories", ""))
    patterns = list_items(sections.get("Extracted Or Updated Patterns", ""))
    executive_summary = list_items(sections.get("Executive Summary", ""))
    review_value = parse_review_value(sections.get("Review Value", ""))
    evidence_gaps = list_items(sections.get("Unresolved Evidence Gaps", ""))
    next_action = plain_text(sections.get("Recommended Next Action", ""))

    return {
        "path": str(path),
        "title": report_title(text),
        "candidate_count": candidate_counts["total_triaged"] or len(ledger_rows),
        "stage_counts": candidate_counts["stage_counts"],
        "ledger_rows": len(ledger_rows),
        "selected_repositories": selected,
        "updated_patterns": patterns,
        "executive_summary": executive_summary,
        "review_value": review_value,
        "evidence_gaps": evidence_gaps,
        "recommended_next_action": next_action,
    }


def summarize_report(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise SystemExit(f"report not found: {path}")

    return summarize_report_text(path.read_text(encoding="utf-8"), path)


def emit_markdown(summaries: list[dict[str, object]]) -> None:
    for index, summary in enumerate(summaries):
        if index:
            print()
        print(f"Report: {summary['path']}")
        if summary.get("title"):
            print(f"Title: {summary['title']}")
        print(f"Candidate count: {summary['candidate_count']} (ledger rows: {summary['ledger_rows']})")

        stage_counts = summary.get("stage_counts") or {}
        if isinstance(stage_counts, dict) and stage_counts:
            stages = ", ".join(f"{stage}={count}" for stage, count in stage_counts.items())
            print(f"Stages: {stages}")

        print_list("Selected repositories", summary.get("selected_repositories"))
        print_list("Updated patterns", summary.get("updated_patterns"))
        print_list("Executive summary", summary.get("executive_summary"))
        print_review_value(summary.get("review_value"))
        print_list("Evidence gaps", summary.get("evidence_gaps"))

        next_action = str(summary.get("recommended_next_action") or "").strip()
        if next_action:
            print("Recommended next action:")
            print(next_action)


def print_list(label: str, values: object) -> None:
    if not isinstance(values, list) or not values:
        return
    print(f"{label}:")
    for value in values:
        print(f"- {value}")


def print_review_value(value: object) -> None:
    if not isinstance(value, dict) or not value:
        return
    verdict = value.get("verdict")
    score = value.get("score")
    action = value.get("recommended_action")
    reason = value.get("reason")
    print(f"Review value: {verdict} score={score} action={action}")
    if reason:
        print(f"Review value reason: {reason}")


def main() -> None:
    args = parse_args()
    report_paths = args.reports or [latest_report()]
    summaries = [summarize_report(path) for path in report_paths]

    if args.format == "json":
        print(json.dumps({"reports": summaries}, indent=2, sort_keys=True))
    else:
        emit_markdown(summaries)


if __name__ == "__main__":
    main()
