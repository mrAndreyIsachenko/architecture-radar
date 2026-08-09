#!/usr/bin/env python3
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path.cwd()
WEEK_ID = os.environ.get("WEEKLY_SYNTHESIS_WEEK_ID")

REQUIRED_REPORT_SECTIONS = {
    "Week And Scope",
    "Input Reports",
    "Executive Synthesis",
    "Pattern Movement",
    "Topic Coverage",
    "Repeated Candidates Or Signals",
    "Decisions And Experiments",
    "Evidence Gaps",
    "Next Week Focus",
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


def changed_weekly_files() -> list[Path]:
    names: set[str] = set()
    base_ref = os.environ.get("WEEKLY_SYNTHESIS_BASE_REF") or os.environ.get("GITHUB_BASE_REF")
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
            ["git", "diff", "--name-only", "--diff-filter=ACMRT", *diff_range, "--", "weekly-reports"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return []

    names.update(diff_result.stdout.splitlines())

    try:
        untracked_result = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard", "--", "weekly-reports"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        untracked_result = None

    if untracked_result:
        names.update(untracked_result.stdout.splitlines())

    return sorted(ROOT / name for name in names if name.endswith(".md") and (ROOT / name).is_file())


def weekly_reports_to_validate() -> list[Path]:
    paths: set[Path] = set(changed_weekly_files())
    if WEEK_ID:
        if not re.fullmatch(r"\d{4}-W\d{2}", WEEK_ID):
            fail(f"invalid WEEKLY_SYNTHESIS_WEEK_ID: {WEEK_ID}")
        paths.add(ROOT / "weekly-reports" / f"{WEEK_ID}.md")
    return sorted(paths)


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


def validate_weekly_report(path: Path) -> None:
    if not path.is_file():
        fail(f"missing weekly synthesis report: {path.relative_to(ROOT)}")

    text = path.read_text(encoding="utf-8")
    if not text.strip():
        fail(f"weekly synthesis report is empty: {path.relative_to(ROOT)}")

    sections = markdown_sections(text)
    missing = REQUIRED_REPORT_SECTIONS - set(sections)
    if missing:
        fail(f"{path.relative_to(ROOT)} missing required sections: {', '.join(sorted(missing))}")

    for section in REQUIRED_REPORT_SECTIONS:
        if not sections[section].strip():
            fail(f"{path.relative_to(ROOT)} section is empty: {section}")

    input_reports = sections["Input Reports"]
    if "reports/" not in input_reports and "opportunity-reports/" not in input_reports:
        fail(f"{path.relative_to(ROOT)} Input Reports must reference at least one report path")

    next_focus = sections["Next Week Focus"].strip()
    if len(next_focus) < 40:
        fail(f"{path.relative_to(ROOT)} Next Week Focus is too short")


def validate_workspace() -> None:
    require_path("weekly-reports", directory=True)


def main() -> None:
    validate_workspace()
    for path in weekly_reports_to_validate():
        validate_weekly_report(path)
    print("weekly synthesis artifacts validated")


if __name__ == "__main__":
    main()
