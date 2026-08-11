#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
from pathlib import Path


ROOT = Path.cwd()
ARTIFACT_DIRS = ("reports", "repositories", "patterns")
E1 = "E1 source verified"
E2 = "E2 test verified"
E3 = "E3 maintainer stated"
BACKTICK_RE = re.compile(r"`([^`]+)`")


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def changed_artifact_files() -> list[Path]:
    names: set[str] = set()
    diff = run_git(["diff", "--name-only", "--diff-filter=ACMRT", "HEAD", "--", *ARTIFACT_DIRS])
    if diff.returncode == 0:
        names.update(diff.stdout.splitlines())

    untracked = run_git(["ls-files", "--others", "--exclude-standard", "--", *ARTIFACT_DIRS])
    if untracked.returncode == 0:
        names.update(untracked.stdout.splitlines())

    paths: list[Path] = []
    for name in sorted(names):
        if not name.endswith(".md"):
            continue
        path = ROOT / name
        if path.is_file():
            paths.append(path)
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
        return E2

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
        return E3

    return None


def looks_like_path(token: str) -> bool:
    token = token.strip()
    if not token or " " in token:
        return False
    basename = token.replace("\\", "/").rsplit("/", 1)[-1]
    return "/" in token or "\\" in token or "." in basename


def normalized_label_for_line(line: str) -> str | None:
    if E1 not in line:
        return None

    labels: set[str] = set()
    for token in BACKTICK_RE.findall(line):
        expected = evidence_label_for_path(token)
        if expected is not None:
            labels.add(expected)
        elif looks_like_path(token):
            labels.add(E1)

    if len(labels) == 1:
        label = next(iter(labels))
        if label != E1:
            return label
    return None


def normalize_text(text: str) -> tuple[str, int]:
    changed = 0
    lines: list[str] = []
    for line in text.splitlines(keepends=True):
        replacement = normalized_label_for_line(line)
        if replacement:
            line = line.replace(E1, replacement)
            changed += 1
        lines.append(line)
    return "".join(lines), changed


def normalize_file(path: Path) -> int:
    original = path.read_text(encoding="utf-8")
    normalized, changed = normalize_text(original)
    if changed:
        path.write_text(normalized, encoding="utf-8")
    return changed


def main() -> int:
    total = 0
    for path in changed_artifact_files():
        changed = normalize_file(path)
        if changed:
            total += changed
            print(f"normalized {changed} evidence label(s) in {path.relative_to(ROOT)}")

    if total == 0:
        print("no radar evidence labels needed normalization")
    else:
        print(f"normalized {total} radar evidence label(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
