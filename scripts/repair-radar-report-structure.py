#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
from collections import OrderedDict
from pathlib import Path


ROOT = Path.cwd()

REQUIRED_REPORT_SECTIONS = [
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
]

LEDGER_COLUMNS = [
    "Repository",
    "URL",
    "Commit",
    "Discovery source",
    "Family",
    "Stage",
    "Decision",
]


def heading_key(heading: str) -> str:
    normalized = heading.replace("`", "").replace("'", "")
    normalized = re.sub(r"[^a-zA-Z0-9]+", " ", normalized)
    return re.sub(r"\s+", " ", normalized).strip().casefold()


SECTION_ALIASES = {
    "run prerequisites": "Prerequisites And State",
    "run prerequisites and repository state": "Prerequisites And State",
    "prerequisites": "Prerequisites And State",
    "prerequisites and repository state": "Prerequisites And State",
    "repository state": "Prerequisites And State",
    "candidate counts by stage": "Candidate Counts",
    "candidate counts by topic": "Candidate Counts",
    "candidate counts by family": "Candidate Counts",
    "candidate accounting": "Candidate Counts",
    "selected repository": "Selected Repositories",
    "selections": "Selected Repositories",
    "selected": "Selected Repositories",
    "summary": "Executive Summary",
    "exec summary": "Executive Summary",
    "review value": "Review Value",
    "value verdict": "Review Value",
    "review verdict": "Review Value",
    "source backed analysis": "Detailed Reviews",
    "detailed analysis": "Detailed Reviews",
    "detailed source backed analysis": "Detailed Reviews",
    "deep reviews": "Detailed Reviews",
    "repository reviews": "Detailed Reviews",
    "patterns": "Extracted Or Updated Patterns",
    "extracted patterns": "Extracted Or Updated Patterns",
    "updated patterns": "Extracted Or Updated Patterns",
    "pattern updates": "Extracted Or Updated Patterns",
    "relevance": "Relevance To Explicit Problems In `interests.md`",
    "project relevance": "Relevance To Explicit Problems In `interests.md`",
    "relevance to current projects": "Relevance To Explicit Problems In `interests.md`",
    "relevance to our current projects": "Relevance To Explicit Problems In `interests.md`",
    "relevance to interests md": "Relevance To Explicit Problems In `interests.md`",
    "relevance to explicit problems in interests md": "Relevance To Explicit Problems In `interests.md`",
    "ledger": "Candidate Ledger",
    "candidate ledger table": "Candidate Ledger",
    "candidate list": "Candidate Ledger",
    "recommended action": "Recommended Next Action",
    "next action": "Recommended Next Action",
    "recommended next step": "Recommended Next Action",
    "next step": "Recommended Next Action",
    "notable rejected candidates": "Notable Rejected Or Deferred Candidates",
    "rejected candidates": "Notable Rejected Or Deferred Candidates",
    "rejected or deferred candidates": "Notable Rejected Or Deferred Candidates",
    "deferred candidates": "Notable Rejected Or Deferred Candidates",
    "rejection reasons": "Notable Rejected Or Deferred Candidates",
    "evidence gaps": "Unresolved Evidence Gaps",
    "unresolved gaps": "Unresolved Evidence Gaps",
    "quality concerns": "Unresolved Evidence Gaps",
    "evidence gaps and quality concerns": "Unresolved Evidence Gaps",
    "validation backlog": "Validation Backlog Updates",
    "validation backlog update": "Validation Backlog Updates",
    "validation backlog updates": "Validation Backlog Updates",
    "backlog updates": "Validation Backlog Updates",
    "failure injection backlog": "Validation Backlog Updates",
}

CANONICAL_BY_KEY = {heading_key(section): section for section in REQUIRED_REPORT_SECTIONS}
CANONICAL_BY_KEY.update({heading_key(alias): canonical for alias, canonical in SECTION_ALIASES.items()})


def split_h2_sections(text: str) -> tuple[str, OrderedDict[str, str], OrderedDict[str, str]]:
    preamble: list[str] = []
    canonical_sections: OrderedDict[str, list[str]] = OrderedDict()
    extra_sections: OrderedDict[str, list[str]] = OrderedDict()
    current_name: str | None = None
    current_target: OrderedDict[str, list[str]] | None = None
    seen_h2 = False

    for line in text.splitlines():
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            seen_h2 = True
            raw_name = match.group(1).strip()
            canonical_name = CANONICAL_BY_KEY.get(heading_key(raw_name))
            if canonical_name:
                current_name = canonical_name
                current_target = canonical_sections
            else:
                current_name = raw_name
                current_target = extra_sections
            current_target.setdefault(current_name, [])
            continue

        if not seen_h2:
            preamble.append(line)
            continue

        if current_name is not None and current_target is not None:
            current_target[current_name].append(line)

    canonical_text = OrderedDict((name, "\n".join(lines).strip()) for name, lines in canonical_sections.items())
    extra_text = OrderedDict((name, "\n".join(lines).strip()) for name, lines in extra_sections.items())
    return "\n".join(preamble).strip(), canonical_text, extra_text


def diagnostic_ledger() -> str:
    return "\n".join(
        [
            "| Repository | URL | Commit | Discovery source | Family | Stage | Decision |",
            "|---|---|---|---|---|---|---|",
            "| Repair-generated placeholder | unavailable | unknown | report-structure-repair | unknown | unknown | deferred: missing candidate ledger |",
        ]
    )


def has_valid_ledger_table(text: str) -> bool:
    lines = [line for line in text.splitlines() if line.startswith("|")]
    if len(lines) < 3:
        return False
    header = [cell.strip() for cell in lines[0].strip().strip("|").split("|")]
    if not set(LEDGER_COLUMNS).issubset(header):
        return False
    separator = [cell.strip() for cell in lines[1].strip().strip("|").split("|")]
    if len(separator) != len(header):
        return False
    return all(re.fullmatch(r":?-{3,}:?", cell) for cell in separator)


def quote_original(text: str) -> str:
    if not text.strip():
        return ""
    return "\n".join(f"> {line}" if line else ">" for line in text.splitlines())


def placeholder(section: str, missing_sections: set[str]) -> str:
    missing = ", ".join(sorted(missing_sections))
    if section == "Candidate Counts":
        return "\n".join(
            [
                "- `triaged`: unknown",
                "- `source-inspected`: unknown",
                "- `deeply reviewed`: unknown",
                f"- Repair-generated placeholder: the research agent omitted this section. Missing canonical sections: {missing}.",
            ]
        )
    if section == "Selected Repositories":
        return "- Repair-generated placeholder: selected repositories were not reported by the research agent."
    if section == "Executive Summary":
        return "Repair-generated placeholder: the research agent omitted the canonical executive summary section."
    if section == "Review Value":
        return "\n".join(
            [
                "| Verdict | Score | Reason | Recommended action |",
                "|---|---:|---|---|",
                "| `needs-targeted-fix` | 1 | Repair-generated placeholder because the original report omitted review value. | `request-fix` |",
            ]
        )
    if section == "Detailed Reviews":
        return "- Repair-generated placeholder: no canonical detailed review section was found."
    if section == "Extracted Or Updated Patterns":
        return "- Repair-generated placeholder: pattern changes were not reported under the canonical section."
    if section == "Relevance To Explicit Problems In `interests.md`":
        return "- Repair-generated placeholder: relevance to explicit `interests.md` problems was omitted."
    if section == "Recommended Next Action":
        return "Manually review this repaired report and close or rerun it if the missing sections contain material evidence gaps."
    if section == "Notable Rejected Or Deferred Candidates":
        return "- Repair-generated placeholder: rejected or deferred candidates were not reported under the canonical section."
    if section == "Unresolved Evidence Gaps":
        return f"- Repair-generated placeholder: original report was missing canonical sections: {missing}."
    if section == "Validation Backlog Updates":
        return "No validation backlog update required. Repair-generated placeholder; verify unresolved evidence gaps before merging."
    if section == "Prerequisites And State":
        return "- Repair-generated placeholder: prerequisites and repository state were omitted; verify workflow logs before merging."
    return "- Repair-generated placeholder: section omitted by the research agent."


def repair_report_text(text: str, report_name: str) -> str:
    if not text.strip():
        text = f"# Architecture Radar Report: {report_name}\n"

    preamble, canonical_sections, extra_sections = split_h2_sections(text)
    if not preamble:
        preamble = f"# Architecture Radar Report: {report_name}"

    missing_sections = {section for section in REQUIRED_REPORT_SECTIONS if not canonical_sections.get(section, "").strip()}
    output: list[str] = [preamble.strip(), ""]

    for section in REQUIRED_REPORT_SECTIONS:
        content = canonical_sections.get(section, "").strip()
        if section == "Candidate Ledger" and not has_valid_ledger_table(content):
            original = quote_original(content)
            content = diagnostic_ledger()
            content += "\n\nRepair-generated note: the original Candidate Ledger was missing or did not contain the required table."
            if original:
                content += "\n\nOriginal Candidate Ledger content:\n\n" + original
        elif not content:
            content = placeholder(section, missing_sections)

        output.extend([f"## {section}", "", content, ""])

    for section, content in extra_sections.items():
        if not content:
            continue
        output.extend([f"## {section}", "", content, ""])

    return "\n".join(output).rstrip() + "\n"


def target_paths(args: argparse.Namespace) -> list[Path]:
    if args.paths:
        return [ROOT / path for path in args.paths]

    paths: list[Path] = []
    run_date = os.environ.get("ARCHITECTURE_RADAR_RUN_DATE")
    if run_date:
        paths.append(ROOT / "reports" / f"{run_date}.md")

    supplement_required = os.environ.get("ARCHITECTURE_RADAR_SUPPLEMENT_REQUIRED", "").lower() in {"1", "true", "yes", "on"}
    supplement_report = os.environ.get("ARCHITECTURE_RADAR_SUPPLEMENT_REPORT", "")
    if supplement_required and supplement_report:
        paths.append(ROOT / supplement_report)

    return paths


def repair_path(path: Path) -> bool:
    original = path.read_text(encoding="utf-8") if path.is_file() else ""
    repaired = repair_report_text(original, path.stem)
    if repaired == original:
        print(f"report structure already canonical: {path.relative_to(ROOT)}")
        return False

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(repaired, encoding="utf-8")
    print(f"repaired report structure: {path.relative_to(ROOT)}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Repair Architecture Radar report headings before strict validation.")
    parser.add_argument("paths", nargs="*", help="Report paths to repair. Defaults to ARCHITECTURE_RADAR_RUN_DATE targets.")
    args = parser.parse_args()

    paths = target_paths(args)
    if not paths:
        print("no Architecture Radar report path selected for repair")
        return 0

    for path in paths:
        repair_path(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
