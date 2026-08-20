## Context

Weekly Synthesis runs inside GitHub Actions on an ephemeral checkout. The model
can see absolute filesystem paths when it reasons about local files, but those
paths are implementation details of the runner and are not useful in committed
Markdown.

## Goals / Non-Goals

**Goals:**

- Keep weekly report artifact links stable in GitHub by using repository-relative
  paths.
- Reject absolute runner, workspace, or user-machine paths in weekly reports.
- Preserve ordinary external HTTPS links if they are ever included.

**Non-Goals:**

- Rewriting historical reports.
- Changing daily Architecture Radar or Opportunity Radar output validation.
- Adding a Markdown link rewriter; generated reports should be fixed at source
  and rejected when invalid.

## Decisions

1. Add prompt guidance before generation.

   The weekly synthesis prompt now explicitly tells the model to use
   repo-relative paths such as `repositories/example.md` or Markdown links with
   repo-relative targets.

2. Validate the generated report text.

   The validator rejects absolute local paths and runner/workspace-specific
   substrings. This catches both Markdown link targets and plain-text absolute
   path mentions.

3. Scope validation to weekly reports.

   This change only guards `weekly-reports/*.md`; other artifact families have
   their own validators and can be tightened separately if needed.

## Risks / Trade-offs

- A legitimate absolute URL remains allowed because the check targets local
  filesystem and runner paths, not `https://` links.
- The validator intentionally rejects broad local absolute path prefixes like
  `/Users/`, `/home/`, and `/tmp/` in weekly reports because weekly synthesis is
  not supposed to cite machine-local artifacts.
