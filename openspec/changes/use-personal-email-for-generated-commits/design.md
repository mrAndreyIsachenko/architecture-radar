## Context

The publish scripts commit generated artifacts after the prepare scripts create
the dated branch. Because the prepare scripts set local Git `user.name` and
`user.email`, that identity becomes both the author and committer for the
generated artifact commit.

## Goals / Non-Goals

**Goals:**

- Make generated artifact commits attributable to
  `Andrey Isachenko <mr.andrey.isachenko@gmail.com>` by default.
- Apply the same identity to Architecture Radar, Opportunity Radar, and Weekly
  Synthesis.
- Preserve a simple environment override for forks.

**Non-Goals:**

- Do not configure GPG or SSH commit signing in GitHub Actions.
- Do not change PR body governance metadata.
- Do not change generated PR validation marker behavior.

## Decisions

1. Use two shared environment variables in prepare scripts.

   `RADAR_COMMIT_USER_NAME` defaults to `Andrey Isachenko`.
   `RADAR_COMMIT_USER_EMAIL` defaults to `mr.andrey.isachenko@gmail.com`.
   The prepare scripts then run:

   ```bash
   git config user.name "$commit_user_name"
   git config user.email "$commit_user_email"
   ```

2. Keep the override generic rather than workflow-specific.

   A single override avoids three separate variable names and keeps forks easy:
   set one name/email pair and every generated workflow uses it.

3. Validate with a static unit test.

   The test reads the prepare scripts and rejects workflow-specific bot noreply
   emails. This catches the exact regression that produced the unattributed
   generated Opportunity Radar commit.

## Risks / Trade-offs

- [Risk] GitHub still shows commits as unsigned. -> Mitigation: this change is
  explicit about controlling author/committer identity only. Cryptographic
  signing would require a separate secret-backed signing setup.
- [Risk] Forks may not want the repository owner's email. -> Mitigation:
  `RADAR_COMMIT_USER_NAME` and `RADAR_COMMIT_USER_EMAIL` can override defaults.
