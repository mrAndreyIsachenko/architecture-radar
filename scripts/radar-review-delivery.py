"""Local, caller-attested receipts; reading a review never acknowledges it."""
from __future__ import annotations

from contextlib import closing
from datetime import datetime, timezone
import fcntl
import os
from pathlib import Path
import re
import sqlite3


class DeliveryError(ValueError):
    pass


def default_path() -> Path:
    root = Path(os.environ.get("XDG_STATE_HOME") or Path.home() / ".local/state")
    return root / "architecture-radar/review-delivery.sqlite3"


def identity(repo: str, scope: str, number: int, sha: str) -> tuple:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
        raise DeliveryError("invalid repository; expected owner/repository")
    if not scope or scope.strip() != scope or any(ord(c) < 32 for c in scope):
        raise DeliveryError("delivery scope is required and must identify the destination thread")
    if type(number) is not int or number < 1:
        raise DeliveryError("positive PR number required")
    if not re.fullmatch(r"[a-f0-9]{40}", sha):
        raise DeliveryError("exact 40-character head SHA required")
    return repo.lower(), scope, number, sha


def validate_schema(connection):
    if connection.execute("PRAGMA user_version").fetchone()[0] != 1:
        raise DeliveryError("unsupported delivery state schema; state was not overwritten")
    columns = [row[1] for row in connection.execute("PRAGMA table_info(receipts)")]
    if columns != ["repo", "scope", "pr_number", "head_sha", "radar", "delivered_at", "message_ref", "evidence_type"]:
        raise DeliveryError("invalid delivery receipt schema")
    primary_key = [row[1] for row in sorted(connection.execute("PRAGMA table_info(receipts)"), key=lambda row: row[5]) if row[5]]
    if primary_key != ["repo", "scope", "pr_number", "head_sha"]:
        raise DeliveryError("invalid delivery receipt primary key")


def read_records(connection) -> dict[tuple, dict]:
    connection.row_factory = sqlite3.Row
    validate_schema(connection)
    result = {}
    for row in connection.execute("SELECT * FROM receipts"):
        record = dict(row)
        key = identity(record["repo"], record["scope"], record["pr_number"], record["head_sha"])
        validate_evidence(record["radar"], record["message_ref"])
        if record["evidence_type"] != "caller_attested":
            raise DeliveryError("unknown delivery evidence type")
        timestamp = datetime.fromisoformat(record["delivered_at"])
        if timestamp.tzinfo is None:
            raise DeliveryError("delivery timestamp requires a timezone")
        result[key] = record
    return result


def read_receipts(path: Path) -> dict[tuple, dict]:
    if not path.exists():
        return {}
    try:
        with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as connection:
            return read_records(connection)
    except (sqlite3.Error, OSError, ValueError, TypeError) as exc:
        raise DeliveryError(f"cannot read delivery state: {exc}") from exc


def validate_evidence(radar: str, message_ref: str):
    if radar not in {"architecture", "opportunity"}:
        raise DeliveryError("acknowledgement requires one radar family")
    if not message_ref or message_ref.strip() != message_ref or any(c.isspace() for c in message_ref):
        raise DeliveryError("message reference to an already visible substantive review required")
    if message_ref.lower() in {"none", "unknown", "pending", "todo", "stdout"}:
        raise DeliveryError("placeholder is not delivery evidence")


def acknowledge(path: Path, repo: str, scope: str, number: int, sha: str, radar: str, message_ref: str) -> dict:
    key = identity(repo, scope, number, sha)
    validate_evidence(radar, message_ref)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        # Serialize first creation too: an existing empty file is not a valid store.
        with path.with_suffix(path.suffix + ".lock").open("a+b") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            existed = path.exists()
            if existed:
                read_receipts(path)
            with closing(sqlite3.connect(path, timeout=10)) as connection:
                with connection:
                    connection.execute("BEGIN IMMEDIATE")
                    if not existed:
                        connection.execute("""CREATE TABLE receipts (
                            repo TEXT NOT NULL, scope TEXT NOT NULL, pr_number INTEGER NOT NULL,
                            head_sha TEXT NOT NULL, radar TEXT NOT NULL, delivered_at TEXT NOT NULL,
                            message_ref TEXT NOT NULL, evidence_type TEXT NOT NULL,
                            PRIMARY KEY (repo, scope, pr_number, head_sha))""")
                        connection.execute("PRAGMA user_version=1")
                    read_records(connection)
                    connection.execute("INSERT OR IGNORE INTO receipts VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                       (*key, radar, datetime.now(timezone.utc).isoformat(), message_ref, "caller_attested"))
        return read_receipts(path)[key]
    except (sqlite3.Error, OSError) as exc:
        raise DeliveryError(f"cannot acknowledge delivery: {exc}") from exc
