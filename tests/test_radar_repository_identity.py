from contextlib import redirect_stderr
import io
import unittest

from test_repair_radar_report_structure import repairer
from test_validate_radar_state import validator


NAME = "Sri-Krishna-V/bumblebee"
URL = "https://github.com/" + NAME
RADAR = [{"repository": NAME, "URL": URL}]
BACKLOG = [{"id": "batch", "source_repository": NAME}]


def report(name="`bumblebee`", url=URL, backlog_name="`bumblebee`"):
    return f"""# Report

## Candidate Ledger

| URL | Repository | Decision | Family |
|---|---|---|---|
| {url} | {name} | selected | document-ai-ocr |

## Validation Backlog Updates

| Repository | Backlog item | Reason | Family | Validation type | Status |
|---|---|---|---|---|---|
| {backlog_name} | `batch` | bumblebee prose stays unchanged | document-ai-ocr | runtime | open |
"""


class RepositoryIdentityTest(unittest.TestCase):
    def test_strict_backlog_validation_fails_before_and_passes_after_repair(self):
        original = report(url="/tmp/architecture-radar-candidates/bumblebee")
        backlog = [{**BACKLOG[0], "family": "document-ai-ocr", "validation_type": "runtime", "status": "open"}]

        def validate(text):
            _, sections, _ = repairer.split_h2_sections(text)
            validator.validate_validation_backlog_updates(
                validator.ROOT / "reports/2026-09-25.md", sections["Validation Backlog Updates"],
                backlog_items={"batch": backlog[0]},
                ledger_rows=[row for _, _, row in repairer.table_rows(sections["Candidate Ledger"])],
                evidence_gaps="runtime evidence missing",
            )

        with self.assertRaises(SystemExit), redirect_stderr(io.StringIO()):
            validate(original)
        validate(repairer.repair_repository_identities(original, RADAR, backlog))
        conflict = [{**backlog[0], "source_repository": "other/bumblebee"}]
        with self.assertRaises(SystemExit), redirect_stderr(io.StringIO()):
            validate(repairer.repair_repository_identities(original, RADAR, conflict))

    def test_bare_name_repaired_in_both_tables_idempotently(self):
        original = report()
        fixed = repairer.repair_repository_identities(original, RADAR, BACKLOG)
        self.assertEqual(fixed.count(f"`{NAME}`"), 2)
        self.assertIn("bumblebee prose stays unchanged", fixed)
        self.assertEqual(fixed, repairer.repair_repository_identities(fixed, RADAR, BACKLOG))

    def test_plain_names_and_markdown_source_links(self):
        fixed = repairer.repair_repository_identities(report("bumblebee", f"[source]({URL})", "bumblebee"), RADAR, BACKLOG)
        self.assertIn(f"| {NAME} | `batch`", fixed)

    def test_canonical_ledger_and_bare_backlog(self):
        fixed = repairer.repair_repository_identities(report(NAME), RADAR, BACKLOG)
        self.assertIn(f"| `{NAME}` | `batch`", fixed)

    def test_clone_url_suffix_does_not_change_identity(self):
        radar = [{"repository": NAME, "URL": URL + ".git"}]
        fixed = repairer.repair_repository_identities(report(url=URL + ".git"), radar, BACKLOG)
        self.assertEqual(fixed.count(f"`{NAME}`"), 2)

    def test_incident_clone_path_requires_radar_source_and_backlog_agreement(self):
        original = report(url="/tmp/architecture-radar-candidates/bumblebee")
        radar = [{"repository": NAME, "URL": URL + ".git"}]
        fixed = repairer.repair_repository_identities(original, radar, BACKLOG)
        self.assertEqual(fixed.count(f"`{NAME}`"), 2)
        self.assertIn("/tmp/architecture-radar-candidates/bumblebee", fixed)
        self.assertEqual(original, repairer.repair_repository_identities(original, [], BACKLOG))

    def test_owner_conflict_with_clone_path_blocks_repair(self):
        original = report(name="other/bumblebee", url="/tmp/clone")
        self.assertEqual(original, repairer.repair_repository_identities(original, RADAR, BACKLOG))

    def test_explicit_owner_conflict_is_not_changed(self):
        original = report("other/bumblebee")
        self.assertEqual(original, repairer.repair_repository_identities(original, RADAR, BACKLOG))

    def test_backlog_conflict_does_not_partially_repair_ledger(self):
        original = report()
        for backlog in ([{"id": "batch", "source_repository": "other/bumblebee"}], [], BACKLOG * 2):
            with self.subTest(backlog=backlog):
                self.assertEqual(original, repairer.repair_repository_identities(original, RADAR, backlog))

    def test_explicit_backlog_cell_conflict_is_not_changed(self):
        original = report(backlog_name="other/bumblebee")
        self.assertEqual(original, repairer.repair_repository_identities(original, RADAR, BACKLOG))

    def test_same_name_owner_and_forge_collisions(self):
        for record in (
            {"repository": "other/bumblebee", "URL": "https://github.com/other/bumblebee"},
            {"repository": NAME, "URL": "https://gitee.com/" + NAME},
        ):
            with self.subTest(record=record):
                original = report()
                self.assertEqual(original, repairer.repair_repository_identities(original, RADAR + [record], BACKLOG))

    def test_missing_or_unsafe_source_evidence(self):
        for url in ("unavailable", "https://github.com.evil/" + NAME, "https://github.com/" + NAME + "/issues/1", "https://user@github.com/" + NAME):
            with self.subTest(url=url):
                original = report(url=url)
                self.assertEqual(original, repairer.repair_repository_identities(original, [], BACKLOG))

    def test_url_must_agree_with_radar_record_name(self):
        original = report()
        radar = [{"repository": NAME, "URL": "https://github.com/other/bumblebee"}]
        self.assertEqual(original, repairer.repair_repository_identities(original, radar, BACKLOG))

    def test_supported_forges_preserve_source(self):
        for host in ("gitee.com", "gitcode.com"):
            url = f"https://{host}/{NAME}"
            fixed = repairer.repair_repository_identities(report(url=url), [{"repository": NAME, "URL": url}], BACKLOG)
            self.assertIn(url, fixed)
            self.assertEqual(fixed.count(f"`{NAME}`"), 2)


if __name__ == "__main__":
    unittest.main()
