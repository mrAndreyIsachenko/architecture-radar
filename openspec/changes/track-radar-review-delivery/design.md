## Context

See proposal.md. `build_profile_status` labels every matching open PR `fresh_pr`
and returns early. `build_review` summarizes those PRs but has no receipt store.
PR listing and both summarizers currently omit `headRefOid`; report reads use
the mutable branch name. The heartbeat agent performs deduplication informally.

## Goals / Non-Goals

**Goals:** make pending versus delivered reviews explicit and testable, preserve
substantive analysis despite CI blockers, and avoid loss after interrupted replies.

**Non-goals:** exactly-once chat delivery, verifying chat transport from a shell
command, repairing independent approval-policy defects, or introducing a sender.

## Decisions

1. Keep discovery and delivery separate. Add `pending_reviews` and
   `delivered_reviews` with exact revision and destination identity. Preserve
   open-PR metadata independently; do not mutate GitHub to track local delivery.
   Age-based and updatedAt-based deduplication are rejected because neither
   proves a substantive response was delivered.
2. Fetch `headRefOid`, read report/state contents at that immutable SHA, and
   verify metadata/file-list consistency across a concurrent head update.
   Retry a bounded number of times or report a moving-head blocker; never
   associate mixed-revision analysis with a confirmed receipt.
3. Use a small standard-library SQLite receipt store with a versioned schema
   and a unique key `(repo, delivery_scope, pr_number, head_sha)`. Transactions
   prevent concurrent acknowledgements losing each other. A local POSIX advisory
   lock serializes initialization as well, distinguishing a new store from a
   pre-existing empty/corrupt file (macOS/Linux caller). Store radar family,
   delivered_at, message_ref, and `caller_attested` evidence type, not chat
   bodies or secrets. Default path: XDG_STATE_HOME or ~/.local/state, under
   architecture-radar; support `--delivery-state` for tests and isolated runs.
4. Resolve `--delivery-scope` from an explicit option or documented thread-ID
   environment variable when available. Without scope, show pending reviews
   and a warning but never suppress or acknowledge. Do not create receipt state
   while only reading summaries.
5. Add explicit `--ack-delivered PR --head-sha SHA --message-ref REF` using the
   same repository and scope options. The caller must first verify a substantive
   review is already visible in this conversation. A status-only message, plan,
   helper stdout, or intended future final response is not sufficient. This is
   an auditable caller attestation, not cryptographic proof of chat delivery.
   Acknowledging an older delivered revision leaves a newer head pending.
6. Document an executable heartbeat protocol: check receipts; verify any visible
   previous unacknowledged substantive reply and acknowledge its exact revision;
   run the helper; read changed content and send pending reviews. When a final
   response cannot be acknowledged afterward in the same turn, acknowledge it
   only on the next invocation after inspecting the visible thread record.
   No extra user confirmation per report is required. If delivery evidence
   cannot be retrieved, prefer a duplicate review over suppressing an unseen one.
7. Evaluate operational status even when open PRs exist. Receipts affect only
   content review eligibility; preserve current workflow and blocker reporting.
   Deduplication must not produce an all-clear for an unrelated failed run.

## Risks / Trade-offs

- No atomic transaction spans local storage and chat -> at-least-once review
  semantics; acknowledgement after visible delivery, never before.
- Lost state or moved machine can repeat old reviews -> conservative replay,
  explicit persistent path and scope, no speculative historical migration.
- Caller can provide false evidence -> require message reference and clear
  attestation semantics; do not promise the CLI verifies chat by itself.
- Active automation may retain the old prompt -> include adoption instructions
  and verify the caller protocol before claiming delivery is fixed end to end;
  do not silently rewrite scheduling or unrelated automation settings.
- Corruption or unavailable storage -> surface errors and leave reviews pending;
  acknowledgement failure cannot become successful delivery.

## Migration Plan

Implement in this one change after approval. Start with no receipts, retain both
radars, and test against temporary stores and mocked GitHub data. Use read-only
live checks for #91/#92 without marking them delivered automatically. Document
and verify the heartbeat protocol with a visible reply/receipt sequence; publishing
or updating the active automation requires the corresponding authorization.
Rollback removes delivery filtering; it never changes research artifacts or PRs.
