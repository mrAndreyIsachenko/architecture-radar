## Why

The governance validator requires pull request bodies to include explicit
authorization metadata. Generated weekly, architecture, and opportunity radar
pull requests currently omit those fields, which creates an inconsistency
between the publisher scripts and the required validation gate.

## What Changes

Update every generated pull request publisher to include:

- `User request:`;
- `Scope confirmed: yes`;
- `Autonomous follow-up: no`;
- `OpenSpec change:` when applicable.

Also update tests and setup-doctor coverage so the regression is checked before
the publisher creates another PR.

## Capabilities

### Updated Capabilities

- `generated-pr-validation`: generated pull requests carry governance metadata.
- `weekly-synthesis`: weekly synthesis generated PRs carry governance metadata.

## Impact

- Updates architecture, opportunity, and weekly publisher scripts.
- Updates tests for publisher body requirements.
- Updates setup doctor workflow text checks.
- Archives this OpenSpec change in the same PR.
