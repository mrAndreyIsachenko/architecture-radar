# Release Checklist

Use this checklist before cutting a public release.

## Current Candidate

First release:

```text
v0.1.0
```

Release intent:

```text
Make Architecture Radar reusable as a reference implementation for scheduled, evidence-backed research agents that publish validated pull requests.
```

## Preconditions

- `main` is protected.
- `validate` is required on `main`.
- GitHub Community Profile is complete.
- Repository license is MIT.
- Repository description and topics are set.
- `README.md` explains the project without relying on private context.
- `QUICKSTART.md` can take a new user from fork to first generated PR.
- At least one real generated PR is linked from the README as example output.
- No secrets or private project details are present in public docs, examples, reports, or templates.
- Generated radar PRs are not auto-merged.

## Checks

Run locally before tagging:

```bash
openspec validate --all --strict --no-interactive
python3 -m unittest discover -s tests
python3 -m py_compile scripts/*.py tests/*.py
bash -n scripts/*.sh
python3 scripts/check-radar-setup.py --skip-github
scripts/validate-opportunity-radar-state.py
scripts/validate-radar-state.py
scripts/validate-weekly-synthesis-state.py
git diff --check
```

Run the GitHub-side setup doctor before tagging:

```bash
python3 scripts/check-radar-setup.py
```

Confirm the default branch check is green:

```bash
gh run list --repo mrAndreyIsachenko/architecture-radar --workflow radar-validation.yml --branch main --limit 1
```

Confirm community profile state:

```bash
gh api repos/mrAndreyIsachenko/architecture-radar/community/profile
```

## Release Notes

Use [`docs/releases/v0.1.0.md`](releases/v0.1.0.md) as the draft release notes.

## Release Command

After the release PR is merged and `main` is green:

```bash
gh release create v0.1.0 \
  --repo mrAndreyIsachenko/architecture-radar \
  --target main \
  --title "v0.1.0 - Evidence-backed scheduled research PRs" \
  --notes-file docs/releases/v0.1.0.md \
  --draft
```

## Post-Release

- Link the release from a short announcement.
- Watch views, stars, forks, issues, and non-bot clone patterns.
- Prefer improving first-run setup over adding new radar features.
- Keep example outputs current when the workflow changes materially.
