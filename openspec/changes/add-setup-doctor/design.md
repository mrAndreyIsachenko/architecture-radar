## Context

The repository has a mature public shell:

- MIT license.
- GitHub Community Profile at 100%.
- `v0.1.0` release.
- Branch protection on `main`.
- `validate` PR check.
- Scheduled Architecture Radar workflow.
- OpenSpec project state and Codex skills.

But these properties are partly local and partly remote. A user cloning or forking the repository needs a compact diagnostic view before running expensive model-backed research.

## Goals / Non-Goals

**Goals:**

- Provide one local command for setup readiness.
- Work without network access for local checks.
- Use `gh` when available for GitHub checks.
- Return non-zero when required checks fail.
- Distinguish required failures from warnings and informational checks.
- Keep output human-readable by default and machine-readable with `--json`.
- Keep the command diagnostic-only.

**Non-Goals:**

- Do not automatically fix GitHub repository settings.
- Do not read or print secret values.
- Do not require GitHub access for local-only checks.
- Do not validate generated radar research quality; that remains `validate-radar-state.py`.
- Do not run Codex or spend OpenAI tokens.

## Decisions

### Check Categories

The setup doctor should include:

- required local files and directories;
- `radar.json` structure;
- workflow files;
- OpenSpec files and `.codex/skills`;
- community files and license;
- release note artifacts;
- script/test presence;
- branch protection and required status checks when GitHub access is available;
- `OPENAI_API_KEY` secret presence via GitHub API metadata only;
- latest release/tag state when GitHub access is available.

### Severity Model

Use three severities:

- `pass`: check succeeded;
- `warn`: useful but not strictly required, or GitHub check unavailable;
- `fail`: required setup is missing or structurally invalid.

The command exits:

- `0` when there are no failures;
- `1` when one or more failures exist.

Warnings should not fail the command.

### GitHub Access

The doctor should derive the repository from `gh repo view --json nameWithOwner` unless `--repo OWNER/REPO` is provided.

If `gh` is missing, unauthenticated, or repository metadata is unavailable, remote checks should warn rather than fail. Local checks should still run. If metadata is available and it shows a required remote setting is absent, such as branch protection or `OPENAI_API_KEY`, the doctor should fail.

### JSON Output

`--json` should emit stable structured output:

```json
{
  "ok": true,
  "summary": {"pass": 1, "warn": 0, "fail": 0},
  "checks": [
    {
      "id": "required-file:README.md",
      "severity": "pass",
      "message": "found README.md",
      "details": {}
    }
  ]
}
```

## Risks / Trade-offs

- GitHub APIs differ by plan and repository settings; some remote checks may need to stay best-effort.
- Secret metadata can confirm names but not values; the doctor must not imply the key is valid.
- Branch protection APIs may return different shapes for legacy branch protection and rulesets. The first version should check conventional branch protection and warn when unavailable.
- A doctor can drift from docs; tests should cover classification and JSON output, while release/checklist docs should mention the command.
