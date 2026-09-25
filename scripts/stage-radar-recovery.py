#!/usr/bin/env python3
"""Preserve research data only; never copy the runner workspace or raw logs."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path


PATTERNS = (
    "README.md", "radar.json", "reports/*.md", "repositories/*.md",
    "patterns/*.md", "experiments/failure-injection-backlog.yml",
)


def regular_source(root: Path, path: Path) -> bool:
    relative = path.relative_to(root)
    return (
        not any(part.startswith(".") for part in relative.parts)
        and not any(root.joinpath(*relative.parts[:i]).is_symlink() for i in range(1, len(relative.parts) + 1))
        and path.is_file()
        and path.resolve().is_relative_to(root.resolve())
    )


def stage(root: Path, destination: Path, metadata: dict[str, str]) -> dict:
    if destination.exists():
        raise ValueError("recovery destination already exists; use a fresh directory")
    if destination.resolve().is_relative_to(root.resolve()):
        raise ValueError("recovery destination must be outside the repository")
    destination.mkdir(parents=True)
    manifest = {"schema_version": 1, "status": "unvalidated-recovery", **metadata, "files": []}
    for pattern in PATTERNS:
        for source in sorted(root.glob(pattern)):
            if not regular_source(root, source):
                continue
            relative = source.relative_to(root)
            content = source.read_bytes()
            target = destination / "files" / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            manifest["files"].append({
                "path": relative.as_posix(), "bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
            })
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    fields = {
        "base_commit": ("GITHUB_SHA", r"[a-f0-9]{40}"),
        "run_id": ("GITHUB_RUN_ID", r"[0-9]+"),
        "run_attempt": ("GITHUB_RUN_ATTEMPT", r"[0-9]+"),
        "report_date": ("ARCHITECTURE_RADAR_RUN_DATE", r"[0-9]{4}-[0-9]{2}-[0-9]{2}"),
    }
    metadata = {}
    for key, (variable, pattern) in fields.items():
        value = os.environ.get(variable, "")
        if not re.fullmatch(pattern, value):
            raise SystemExit(f"missing or invalid recovery metadata: {variable}")
        metadata[key] = value
    manifest = stage(Path.cwd(), args.output, metadata)
    print(f"Staged {len(manifest['files'])} research files for recovery")


if __name__ == "__main__":
    main()
