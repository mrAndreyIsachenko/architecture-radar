## Context

See proposal.md for the incident. The existing report repair step already
normalizes table headings and validation types. The strict validator compares
backlog `source_repository` with report table identities and selected ledger
rows. The agent wrapper currently checks neither of these before its final
message. No recovery upload follows a failed validation step.

The failing run used base commit `e8e7441cb82e03ef52f71133615d38aa4ef40a70`.
Its downloaded log contains repeated patch output including the failing row.
Completeness of every changed file has not yet been established. The local
checkout is an older merged research branch; implementation must be reconciled
with current main without discarding user changes.

## Goals / Non-Goals

**Goals:** repair recoverable presentation aliases deterministically, preserve
strict reference checks, and make failed output recoverable without another
model call.

**Non-goals:** fuzzy repository matching, automatic owner/forge migrations,
relabeling weak evidence, mass historical rewrites, changing the model or budget,
and fixing the separate bot-approval/synthetic-check incident.

## Decisions

1. Extend the existing report repair boundary, not the strict validator's equality
   rule. Parse structured tables and source URLs using existing helpers and URL
   parsing. Build canonical references from radar state, selected ledger URLs,
   and backlog IDs. Only replace bare names with agreement across available
   references; explicit owner conflicts, unknown hosts, and ambiguous mirrors
   remain unresolved. Restrict edits to the current report's identity cells.
   Do not infer identity from display labels or globally replace prose.
2. Keep report and ledger repair atomic for a given candidate, so fixing the
   backlog table does not merely expose a new selected-ledger mismatch. Do not
   overwrite the canonical backlog or radar identity to fit a report typo.
3. Add canonical-identity and full-validator instructions to the research prompt.
   Prompt instructions are not enforcement: the independent workflow validation
   remains the publication gate. No automatic paid repair loop is added.
4. Stage a recovery bundle from an explicit artifact allowlist into a dedicated
   temporary directory. Include generated Markdown/JSON and the failure-injection
   backlog plus minimal provenance; reject symlinks, non-regular files, unsafe
   paths, and unrelated extensions. Never upload the workspace, CODEX_HOME,
   environment dump, or raw model logs. Upload after failure of an executed
   research step or its downstream steps, with seven-day retention. A recovery
   upload failure must be visible without hiding the original failure.
5. Recover this incident in a temporary checkout at the recorded base. Treat
   log patches as untrusted data: inspect allowlisted paths, do not execute
   embedded commands, and never blindly apply a mixed code/artifact patch.
   Record completeness per file; apply only observed data changes, then the
   deterministic identity repair. Keep publication subject to validation and
   the user's separate push/PR authorization.

## Risks / Trade-offs

Hosted acceptance uses an explicit `recovery_smoke` workflow-dispatch boolean,
default false. This mode skips the production job and runs a bounded read-only
job without secrets or Codex. It copies an invalid report fixture, invokes the
real validator, and executes identical recovery steps. A publication sentinel
must be skipped, the run must remain failed, and the artifact must download and
match its manifest. Scheduled research never enters this mode.

- Short names can collide across owners or forges -> require corroborating
  references and leave conflicts for strict validation to reject.
- Fixing only the first validation error can hide later failures -> run the
  complete validator on recovered output and add an end-to-end fixture.
- File allowlists cannot prove generated text contains no secret -> retain the
  agent's no-secret rule, exclude raw logs and credentials by construction, and
  test file/path boundaries; do not claim content-level secret detection.
- Logs can be incomplete -> report missing files explicitly; no invented output
  and no unapproved paid regeneration.
- A local passing test is not proof of GitHub upload behavior -> keep live
  acceptance pending until the authorized workflow exercise completes.

## Migration Plan

Implement and test on the current main baseline in one change. Restore and
validate the existing incident output locally without spending API credits.
Publish implementation only after user authorization, then exercise a bounded
no-model validation-failure fixture in GitHub Actions to prove recovery upload
and unchanged failure status. Verify the next real research run separately.
Rollback reverts the repair/upload changes; strict validation remains intact.
