#!/usr/bin/env python3
"""Extract a compact machine-readable summary from Opportunity Radar reports."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


DEFAULT_REPORT_DIR = Path("opportunity-reports")
LIST_MARKER_RE = re.compile(r"^\s*[-*]\s+(.+?)\s*$")
SIGNAL_COUNT_RE = re.compile(r"-\s+([^:]+):\s*(\d+)")
REVIEWED_SIGNALS_RE = re.compile(r"Reviewed public signals:\s*(\d+)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reports", nargs="*", type=Path, help="Opportunity report Markdown files to summarize.")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    return parser.parse_args()


def latest_report() -> Path:
    reports = sorted(DEFAULT_REPORT_DIR.glob("*.md"))
    if not reports:
        raise SystemExit("no opportunity-reports/*.md files found")
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


def parse_signal_counts(section_text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for line in section_text.splitlines():
        match = SIGNAL_COUNT_RE.match(line.strip())
        if match:
            counts[match.group(1).strip()] = int(match.group(2))
    return counts


def parse_reviewed_signals(text: str, ledger_rows: int) -> int:
    match = REVIEWED_SIGNALS_RE.search(text)
    if match:
        return int(match.group(1))
    return ledger_rows


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


def report_title(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def summarize_report_text(text: str, path: str | Path) -> dict[str, object]:
    sections = markdown_sections(text)
    ledger_rows = parse_table(sections.get("Signal Ledger", ""))
    build_readiness = parse_table(sections.get("Build Readiness", ""))
    money_readiness = parse_table(sections.get("Money Readiness", ""))
    structural_ranking = parse_table(sections.get("Structural Candidate Ranking", ""))
    structural_score_breakdown = parse_table(sections.get("Structural Score Breakdown", ""))

    return {
        "path": str(path),
        "title": report_title(text),
        "reviewed_signals": parse_reviewed_signals(text, len(ledger_rows)),
        "signal_counts": parse_signal_counts(sections.get("Signal Counts", "")),
        "ledger_rows": len(ledger_rows),
        "selected_opportunities": list_items(sections.get("Selected Opportunities", "")),
        "executive_summary": list_items(sections.get("Executive Summary", "")),
        "build_readiness": build_readiness,
        "money_readiness": money_readiness,
        "structural_ranking": structural_ranking,
        "structural_score_breakdown": structural_score_breakdown,
        "recommended_next_test": plain_text(sections.get("Recommended Next Test", "")),
        "evidence_gaps": list_items(sections.get("Evidence Gaps", "")),
    }


def summarize_report(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise SystemExit(f"opportunity report not found: {path}")

    return summarize_report_text(path.read_text(encoding="utf-8"), path)


def emit_markdown(summaries: list[dict[str, object]]) -> None:
    for index, summary in enumerate(summaries):
        if index:
            print()
        print(f"Report: {summary['path']}")
        if summary.get("title"):
            print(f"Title: {summary['title']}")
        print(f"Reviewed signals: {summary['reviewed_signals']} (ledger rows: {summary['ledger_rows']})")

        signal_counts = summary.get("signal_counts") or {}
        if isinstance(signal_counts, dict) and signal_counts:
            counts = ", ".join(f"{stage}={count}" for stage, count in signal_counts.items())
            print(f"Signal counts: {counts}")

        print_list("Selected opportunities", summary.get("selected_opportunities"))
        print_list("Executive summary", summary.get("executive_summary"))
        print_table_summary("Structural ranking", summary.get("structural_ranking"), ("Rank", "Opportunity", "Score", "Wedge"))
        print_table_summary(
            "Structural scores",
            summary.get("structural_score_breakdown"),
            ("Opportunity", "Total", "Fragmentation", "Manual pain", "Economic value"),
        )
        print_list("Evidence gaps", summary.get("evidence_gaps"))

        next_test = str(summary.get("recommended_next_test") or "").strip()
        if next_test:
            print("Recommended next test:")
            print(next_test)


def print_list(label: str, values: object) -> None:
    if not isinstance(values, list) or not values:
        return
    print(f"{label}:")
    for value in values:
        print(f"- {value}")


def print_table_summary(label: str, values: object, columns: tuple[str, ...]) -> None:
    if not isinstance(values, list) or not values:
        return
    print(f"{label}:")
    for row in values:
        if not isinstance(row, dict):
            continue
        parts = [str(row.get(column, "")).strip() for column in columns if str(row.get(column, "")).strip()]
        if parts:
            print(f"- {' | '.join(parts)}")


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
