#!/usr/bin/env python3
from __future__ import annotations

import os
import json
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

ACTIVE_OPPORTUNITY_SECTIONS = {
    "Decisions And Experiments",
    "Next Week Focus",
}

ACTIVE_OPPORTUNITY_LANGUAGE = re.compile(
    r"\b("
    r"active\s+(?:next[- ]week\s+)?(?:experiment|work|next[- ]step|focus)"
    r"|next[- ]week\s+(?:focus|experiment|work)"
    r"|next[- ]step\s+experiment"
    r"|selected[- ]for[- ]build"
    r"|paid\s+(?:pilot|audit|review|experiment)"
    r"|build(?:ing)?"
    r"|run(?:ning)?"
    r"|sell(?:ing)?"
    r"|ship(?:ping)?"
    r"|implement(?:ing)?"
    r"|prototype"
    r"|launch"
    r"|test(?:ing)?"
    r"|offer"
    r"|prioriti[sz]e"
    r"|execute"
    r")\b",
    re.IGNORECASE,
)

NON_ACTIVE_FRAMING = re.compile(
    r"\b("
    r"watchlisted"
    r"|watchlist"
    r"|deferred"
    r"|blocked"
    r"|not\s+selected"
    r"|not\s+ready"
    r"|do_not_build_until"
    r"|do\s+not\s+build"
    r"|do\s+not\s+recommend"
    r"|must\s+not"
    r"|should\s+not"
    r"|cannot\s+(?:be\s+)?(?:select|build|run|sell|test|ship|launch)"
    r"|can't\s+(?:be\s+)?(?:select|build|run|sell|test|ship|launch)"
    r"|no\s+active"
    r"|no\s+opportunit"
    r"|requires?\s+validation"
    r"|requiring\s+validation"
    r"|pending\s+validation"
    r"|before\s+build\s+work"
    r"|evidence\s+gap"
    r"|insufficient"
    r"|not\s+enough\s+evidence"
    r")\b",
    re.IGNORECASE,
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


def opportunity_state_path() -> Path:
    return ROOT / "opportunities.json"


def load_opportunity_state() -> dict[str, list[dict[str, object]]]:
    path = opportunity_state_path()
    if not path.is_file():
        return {"selected": [], "deferred": [], "watchlisted": []}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid opportunities.json: {exc}")

    state: dict[str, list[dict[str, object]]] = {}
    for bucket in ("selected", "deferred", "watchlisted"):
        entries = data.get(bucket, [])
        if not isinstance(entries, list):
            fail(f"opportunities.json field must be a list: {bucket}")
        state[bucket] = [entry for entry in entries if isinstance(entry, dict)]
    return state


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def opportunity_identifiers(entry: dict[str, object]) -> set[str]:
    identifiers: set[str] = set()
    for key in ("id", "title", "file"):
        value = entry.get(key)
        if isinstance(value, str) and value.strip():
            identifiers.add(value.lower())
            identifiers.add(slugify(value))
            if key == "file":
                identifiers.add(Path(value).stem.lower())

    return {identifier for identifier in identifiers if identifier}


def line_mentions_opportunity(line: str, entry: dict[str, object]) -> bool:
    lowered = line.lower()
    return any(identifier in lowered for identifier in opportunity_identifiers(entry))


def active_line_is_allowed(line: str) -> bool:
    return bool(NON_ACTIVE_FRAMING.search(line))


def validate_opportunity_state_alignment(path: Path, sections: dict[str, str]) -> None:
    state = load_opportunity_state()
    selected = state["selected"]
    non_selected = state["deferred"] + state["watchlisted"]

    for section_name in ACTIVE_OPPORTUNITY_SECTIONS:
        section_text = sections.get(section_name, "")
        for raw_line in section_text.splitlines():
            line = raw_line.strip()
            if not line or not ACTIVE_OPPORTUNITY_LANGUAGE.search(line):
                continue

            if not selected and "opportunit" in line.lower() and not active_line_is_allowed(line):
                fail(
                    f"{path.relative_to(ROOT)} {section_name} recommends active opportunity work "
                    "while opportunities.json.selected is empty"
                )

            for entry in non_selected:
                if line_mentions_opportunity(line, entry) and not active_line_is_allowed(line):
                    title = entry.get("title") or entry.get("id") or "<unknown>"
                    fail(
                        f"{path.relative_to(ROOT)} {section_name} recommends non-selected opportunity "
                        f"as active work: {title}"
                    )


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

    validate_opportunity_state_alignment(path, sections)


def validate_workspace() -> None:
    require_path("weekly-reports", directory=True)


def main() -> None:
    validate_workspace()
    for path in weekly_reports_to_validate():
        validate_weekly_report(path)
    print("weekly synthesis artifacts validated")


if __name__ == "__main__":
    main()
