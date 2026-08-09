# Contributing

Contributions are welcome when they make the radar more reliable, easier to adapt, or easier to review.

## Good Contributions

- Deterministic validation for model-generated research artifacts.
- Better first-run setup and documentation.
- Safer GitHub Actions boundaries.
- Tests for scripts and validators.
- Examples that show how to repoint the radar to a different research domain.
- Narrow fixes to evidence labeling, candidate accounting, PR review helpers, or cost controls.

## Before Opening A Pull Request

1. Start from a current `main`.
2. Keep changes focused.
3. Do not commit generated research artifacts unless your change is specifically about a radar run.
4. Do not include secrets, private repository names, API keys, or private project context.
5. Run the relevant checks locally.

Useful checks:

```bash
openspec validate --all --strict --no-interactive
python3 -m unittest discover -s tests
python3 -m py_compile scripts/*.py tests/*.py
bash -n scripts/*.sh
python3 scripts/check-radar-setup.py --skip-github
scripts/validate-opportunity-radar-state.py
scripts/validate-radar-state.py
git diff --check
```

## OpenSpec

Use OpenSpec for non-trivial behavior changes before implementation.

Start with an OpenSpec change when modifying:

- workflow behavior;
- validation rules;
- evidence taxonomies;
- artifact schemas;
- publishing boundaries;
- new radar modes;
- recurring automation semantics.

Generated radar reports, repository reviews, pattern updates, and routine research artifacts do not need OpenSpec changes.

The current OpenSpec root lives under `openspec/`.

The checked-in Codex integration lives under `.codex/skills/`. Restart Codex after pulling changes that update these skills.

## Pull Request Expectations

Explain:

- what changed;
- why it changed;
- whether it affects scheduled research runs;
- whether it changes generated artifacts, validation, or publication behavior;
- which checks were run.

For generated radar output, include the report date and link the relevant report, repository review, pattern, or `radar.json` entry.

## Research Artifact Quality

Generated reports and reviews should preserve the project's evidence discipline:

- `E1 source verified` only for implementation code;
- `E2 test verified` for tests or reproducible evaluation code;
- `E3 maintainer stated` for docs, README, changelog, issues, releases, and comments;
- `I interpretation` for architectural synthesis;
- `H hypothesis` for plausible but unverified claims.

Selecting zero repositories is acceptable when evidence is thin.

## Security And Credentials

Do not open public issues or PRs that expose secrets or security-sensitive details. Follow `SECURITY.md` for vulnerability reports.
