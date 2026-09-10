## Why

Generated radar pull requests currently create commits with workflow-specific bot
identities such as `opportunity-radar-bot@users.noreply.github.com`. That makes
the commit history harder to attribute and does not match the repository owner's
preferred commit email.

## What Changes

- Configure Architecture Radar, Opportunity Radar, and Weekly Synthesis prepare
  scripts to use a shared generated-commit identity.
- Default the generated-commit author and committer email to
  `mr.andrey.isachenko@gmail.com`.
- Keep the identity overrideable through environment variables for future
  repository forks or automation changes.
- Add tests that prevent reintroducing bot noreply commit emails in generated
  workflow prepare scripts.

## Capabilities

### New Capabilities

### Modified Capabilities

- `generated-pr-validation`: generated radar pull requests use the repository
  owner's configured commit identity before publishing artifacts.

## Impact

- Affects `scripts/prepare-radar-run.sh`,
  `scripts/prepare-opportunity-radar-run.sh`, and
  `scripts/prepare-weekly-synthesis-run.sh`.
- Adds a unit test covering generated commit identity defaults.
- Does not add cryptographic GPG or SSH signing; it controls Git author and
  committer name/email.
