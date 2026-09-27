from concurrent.futures import ThreadPoolExecutor
from contextlib import closing, redirect_stdout
import io
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from test_radar_pr_review import reviewer, args, ROOT
from test_summarize_radar_pr import summarizer as architecture, pr_view as architecture_view, REPORT as ARCH_REPORT
from test_summarize_opportunity_pr import summarizer as opportunity, pr_view as opportunity_view, REPORT as OPP_REPORT


delivery = reviewer.delivery
REPO = "owner/repo"
SHA = "a" * 40


class RevisionTest(unittest.TestCase):
    def test_both_summarizers_retry_moving_revision(self):
        for module, make_view, report in ((architecture, architecture_view, ARCH_REPORT), (opportunity, opportunity_view, OPP_REPORT)):
            before = make_view()
            after = {**before, "headRefOid": "b" * 40}
            with patch.object(module, "pr_view", side_effect=[before, after, after, after]), patch.object(module, "fetch_file_text", return_value=report) as fetch:
                result = module.summarize_pr(REPO, "15")
                self.assertEqual(result["head_sha"], "b" * 40)
                self.assertEqual([call.args[1] for call in fetch.call_args_list], [SHA, "b" * 40])

    def test_both_summarizers_reject_missing_sha_and_continuously_moving_files(self):
        for module, make_view, report in ((architecture, architecture_view, ARCH_REPORT), (opportunity, opportunity_view, OPP_REPORT)):
            view = make_view()
            with patch.object(module, "pr_view", return_value={**view, "headRefOid": None}), patch.object(module, "fetch_file_text") as fetch:
                with self.assertRaisesRegex(SystemExit, "SHA"):
                    module.summarize_pr(REPO, "15")
                fetch.assert_not_called()
            changed = {**view, "files": []}
            with patch.object(module, "pr_view", side_effect=[view, changed, view, changed]), patch.object(module, "fetch_file_text", return_value=report):
                with self.assertRaisesRegex(SystemExit, "changed during"):
                    module.summarize_pr(REPO, "15")


class DeliveryTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "state/receipts.sqlite3"

    def ack(self, number=91, sha=SHA, scope="thread-a", repo=REPO):
        return delivery.acknowledge(self.path, repo, scope, number, sha, "architecture", "turn:visible-review")

    def test_read_missing_does_not_create_state(self):
        self.assertEqual(delivery.read_receipts(self.path), {})
        self.assertFalse(self.path.parent.exists())

    def test_persistence_idempotence_and_identity_isolation(self):
        first = self.ack()
        self.assertEqual(first, self.ack())
        self.ack(sha="b" * 40)
        self.ack(scope="thread-b")
        self.ack(repo="other/repo")
        records = delivery.read_receipts(self.path)
        self.assertEqual(len(records), 4)
        self.assertEqual(records[(REPO, "thread-a", 91, SHA)]["message_ref"], "turn:visible-review")
        self.assertNotIn((REPO, "thread-a", 91, "c" * 40), records)

    def test_concurrent_acknowledgements_do_not_lose_records(self):
        with ThreadPoolExecutor(max_workers=6) as pool:
            list(pool.map(lambda number: self.ack(number=number), range(1, 13)))
        self.assertEqual(len(delivery.read_receipts(self.path)), 12)

    def test_concurrent_cli_processes_share_initialization_and_receipts(self):
        def acknowledge(number):
            return subprocess.run([sys.executable, str(ROOT / "scripts/radar-pr-review.py"),
                                   "--repo", REPO, "--delivery-state", str(self.path),
                                   "--delivery-scope", "thread-a", "--radar", "architecture",
                                   "--ack-delivered", str(number), "--head-sha", SHA,
                                   "--message-ref", "fixture:visible-turn"], capture_output=True, text=True)
        with ThreadPoolExecutor(max_workers=6) as pool:
            results = list(pool.map(acknowledge, range(1, 7)))
        for result in results:
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(delivery.read_receipts(self.path)), 6)

    def test_invalid_identity_and_evidence_rejected_before_write(self):
        for scope, number, sha, ref in (("", 91, SHA, "turn:x"), ("thread", 0, SHA, "turn:x"), ("thread", 91, "main", "turn:x"), ("thread", 91, SHA, ""), ("thread", 91, SHA, "stdout")):
            with self.assertRaises(delivery.DeliveryError):
                delivery.acknowledge(self.path, REPO, scope, number, sha, "architecture", ref)
        self.assertFalse(self.path.exists())

    def test_corrupt_or_unsupported_state_is_not_overwritten(self):
        self.path.parent.mkdir()
        self.path.write_bytes(b"not a database")
        for action in (lambda: delivery.read_receipts(self.path), self.ack):
            with self.assertRaises(delivery.DeliveryError):
                action()
            self.assertEqual(self.path.read_bytes(), b"not a database")
        self.path.unlink()
        with closing(sqlite3.connect(self.path)) as connection:
            connection.execute("PRAGMA user_version=99")
        with self.assertRaises(delivery.DeliveryError):
            self.ack()

    def test_failed_write_never_reports_success(self):
        self.path.parent.mkdir()
        self.path.mkdir()
        with self.assertRaises(delivery.DeliveryError):
            self.ack()

    def test_existing_empty_state_is_not_reinitialized(self):
        self.path.parent.mkdir()
        self.path.touch()
        with self.assertRaises(delivery.DeliveryError):
            self.ack()
        self.assertEqual(self.path.read_bytes(), b"")

    def test_corrupt_record_blocks_reads_and_further_writes(self):
        self.ack()
        with closing(sqlite3.connect(self.path)) as connection, connection:
            connection.execute("UPDATE receipts SET message_ref='stdout'")
        with self.assertRaises(delivery.DeliveryError):
            delivery.read_receipts(self.path)
        with self.assertRaises(delivery.DeliveryError):
            self.ack(number=92)
        with closing(sqlite3.connect(self.path)) as connection:
            self.assertEqual(connection.execute("SELECT count(*) FROM receipts").fetchone()[0], 1)

    def options(self):
        result = args()
        result.repo = REPO
        result.delivery_scope = "thread-a"
        result.delivery_state = self.path
        return result

    def review(self, *, sha=SHA, operational="no_pr", blocker=False, options=None):
        prs = [{"number": 91, "radar": "architecture", "head_sha": sha}, {"number": 92, "radar": "opportunity", "head_sha": SHA}]
        notification = {"failed_run": "REPORT", "waiting": "DONT_NOTIFY"}.get(operational, "INFO")
        op = {"status": operational, "notification": notification, "message": operational, "latest_run": {"url": "https://example/run"}}
        status = {"status": "fresh_pr", "notification": "REVIEW", "fresh_prs": prs, "radars": [{"operational": op}]}
        recommendation = {"decision": "needs_manual_review" if blocker else "looks_mergeable", "reason": "validation failed" if blocker else "passed", "next_action": "fix validation" if blocker else "merge"}
        with patch.object(reviewer.status_helper, "build_status", return_value=status), patch.object(reviewer.pr_summary_helper, "summarize_pr", return_value={"number": 91, "head_sha": sha, "reports": [], "review_recommendation": recommendation}), patch.object(reviewer.opportunity_pr_summary_helper, "summarize_pr", return_value={"number": 92, "head_sha": SHA, "reports": []}):
            return reviewer.build_review(options or self.options())

    def test_printing_or_interrupted_delivery_leaves_both_pending(self):
        self.assertEqual(len(self.review()["pending_reviews"]), 2)
        self.assertEqual(len(self.review()["pending_reviews"]), 2)
        self.assertFalse(self.path.exists())

    def test_receipt_suppresses_only_matching_revision_and_destination(self):
        self.ack()
        self.assertEqual([p["number"] for p in self.review()["pending_reviews"]], [92])
        self.assertEqual(len(self.review(sha="b" * 40)["pending_reviews"]), 2)
        options = self.options()
        options.delivery_scope = "thread-b"
        self.assertEqual(len(self.review(options=options)["pending_reviews"]), 2)

    def test_missing_scope_or_corrupt_state_replays_with_warning(self):
        self.ack()
        options = self.options()
        options.delivery_scope = ""
        review = self.review(options=options)
        self.assertEqual(len(review["pending_reviews"]), 2)
        self.assertTrue(review["delivery_warnings"])
        self.path.write_bytes(b"broken")
        review = self.review()
        self.assertEqual(len(review["pending_reviews"]), 2)
        self.assertTrue(review["delivery_warnings"])

    def test_receipts_do_not_hide_workflow_failure_or_ci_blocker(self):
        self.ack()
        delivery.acknowledge(self.path, REPO, "thread-a", 92, SHA, "opportunity", "turn:opp-review")
        self.assertEqual(self.review(operational="failed_run")["status"]["status"], "failed_run")
        review = self.review(blocker=True)
        self.assertEqual(review["status"]["status"], "attention_required")
        self.assertEqual(review["validation_blockers"][0]["number"], 91)
        self.assertEqual(self.review()["status"]["status"], "no_pending_review")

    def test_pending_content_survives_ci_blocker_and_failed_run(self):
        review = self.review(blocker=True, operational="failed_run")
        self.assertEqual(len(review["pending_reviews"]), 2)
        self.assertEqual(len(review["pr_overviews"]), 2)
        self.assertEqual(len(review["validation_blockers"]), 1)
        self.assertEqual(review["operational_statuses"][0]["status"], "failed_run")

    def test_schedule_wait_does_not_hide_pending_content(self):
        self.assertEqual(self.review(operational="waiting")["status"]["notification"], "REVIEW")
        self.ack()
        delivery.acknowledge(self.path, REPO, "thread-a", 92, SHA, "opportunity", "turn:opp-review")
        review = self.review(operational="waiting")
        self.assertEqual(review["status"]["notification"], "DONT_NOTIFY")
        self.assertEqual(len(review["delivered_reviews"]), 2)

    def test_failed_summary_stays_pending_and_does_not_skip_other_family(self):
        status = {"fresh_prs": [{"number": 91}, {"number": 92, "radar": "opportunity"}]}
        with patch.object(reviewer.status_helper, "build_status", return_value=status), patch.object(reviewer.pr_summary_helper, "summarize_pr", side_effect=SystemExit("moving head")), patch.object(reviewer.opportunity_pr_summary_helper, "summarize_pr", return_value={"number": 92, "head_sha": SHA}):
            review = reviewer.build_review(self.options())
        self.assertEqual(len(review["pending_reviews"]), 2)
        self.assertEqual(len(review["pr_overviews"]), 1)
        self.assertIn("moving head", review["review_errors"][0])

    def test_cli_acknowledgement_across_process_restart(self):
        command = [sys.executable, str(ROOT / "scripts/radar-pr-review.py"), "--repo", REPO,
                   "--delivery-state", str(self.path), "--delivery-scope", "thread-a",
                   "--radar", "architecture", "--ack-delivered", "91", "--head-sha", SHA,
                   "--message-ref", "turn:visible-review"]
        for _ in range(2):
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["receipt"]["evidence_type"], "caller_attested")
        self.assertEqual([p["number"] for p in self.review()["pending_reviews"]], [92])
        self.assertEqual(len(self.review(sha="b" * 40)["pending_reviews"]), 2)
        result = subprocess.run(command[:-2], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)

    def test_cli_rejects_incomplete_acknowledgements_without_touching_store(self):
        base = [sys.executable, str(ROOT / "scripts/radar-pr-review.py"), "--delivery-state", str(self.path)]
        for flags in (["--head-sha", SHA], ["--ack-delivered", "91"],
                      ["--ack-delivered", "91", "--head-sha", SHA, "--message-ref", "turn:x", "--delivery-scope", "thread-a"],
                      ["--ack-delivered", "91", "--head-sha", "main", "--message-ref", "turn:x", "--delivery-scope", "thread-a", "--radar", "architecture"]):
            with self.subTest(flags=flags):
                result = subprocess.run(base + flags, capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(self.path.exists())

    def test_end_to_end_prepared_visible_acknowledged_then_new_sha(self):
        status = {"fresh_prs": [{"number": 15, "radar": "architecture"}, {"number": 50, "radar": "opportunity"}]}
        current = {"sha": SHA}
        def view():
            return {**architecture_view(), "headRefOid": current["sha"]}
        with patch.object(reviewer.status_helper, "build_status", return_value=status), patch.object(reviewer.pr_summary_helper, "pr_view", side_effect=lambda *a: view()), patch.object(reviewer.pr_summary_helper, "fetch_file_text", return_value=ARCH_REPORT), patch.object(reviewer.opportunity_pr_summary_helper, "pr_view", return_value=opportunity_view()), patch.object(reviewer.opportunity_pr_summary_helper, "fetch_file_text", return_value=OPP_REPORT):
            first = reviewer.build_review(self.options())
            output = io.StringIO()
            with redirect_stdout(output):
                reviewer.emit_markdown(first)
            self.assertIn("Candidate count:", output.getvalue())
            self.assertIn("Reviewed signals:", output.getvalue())
            self.assertFalse(self.path.exists())
            self.assertEqual(len(reviewer.build_review(self.options())["pending_reviews"]), 2)
            # Fixture simulates an already visible prior reply, not actual chat transport.
            delivery.acknowledge(self.path, REPO, "thread-a", 15, SHA, "architecture", "fixture:visible-turn-1")
            delivery.acknowledge(self.path, REPO, "thread-a", 50, SHA, "opportunity", "fixture:visible-turn-1")
            self.assertEqual(reviewer.build_review(self.options())["pending_reviews"], [])
            current["sha"] = "b" * 40
            self.assertEqual([p["number"] for p in reviewer.build_review(self.options())["pending_reviews"]], [15])


if __name__ == "__main__":
    unittest.main()
