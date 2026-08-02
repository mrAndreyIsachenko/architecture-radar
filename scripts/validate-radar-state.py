#!/usr/bin/env python3
import json
import os
import re
import sys
from pathlib import Path


ROOT = Path.cwd()
RUN_DATE = os.environ.get("ARCHITECTURE_RADAR_RUN_DATE")


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


require_path("interests.md")
require_path("radar.json")
require_path("reports", directory=True)
require_path("repositories", directory=True)
require_path("patterns", directory=True)
require_path("docs/architecture-radar-agent.md")

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

print("radar artifacts validated")
