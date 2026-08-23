## Context

`scripts/validate-radar-state.py` validates generated Architecture Radar reports by exact H2 section names. The agent prompt says what a report should contain, but does not provide an exact machine-readable section contract near the CI instructions. When the model writes alternate section names, the workflow fails in `Validate radar artifacts` before `scripts/publish-radar-run.sh` can publish a PR.

## Decision

Add a deterministic repair script that runs after the research agent and evidence-label normalization, before `scripts/validate-radar-state.py`.

The repair step will:

- target `reports/$ARCHITECTURE_RADAR_RUN_DATE.md` and the supplement report when one is required;
- parse H2 sections using the same section extraction contract as validation;
- preserve existing content under canonical sections;
- map common alternate headings to canonical section names;
- append missing required sections with explicit diagnostic placeholder content;
- create a minimally valid diagnostic Candidate Ledger table only when the ledger section is missing;
- keep placeholders visible so reviewers can close or fix a low-quality run rather than accepting synthetic evidence.

The workflow prompt will also list the exact H2 headings and Candidate Ledger columns. This reduces repair frequency and makes the contract visible to the model.

## Non-Goals

- Do not infer candidate counts, selected repositories, evidence quality, or pattern changes from unrelated prose.
- Do not repair repository review files, pattern files, or `radar.json`.
- Do not weaken `scripts/validate-radar-state.py` section requirements.

## Risks

- A repaired report can pass structural validation while still being low-quality. The placeholder text must explicitly mark gaps as repair-generated so PR review can reject it.
- If the model emits a report with no useful candidate data at all, the repaired PR is diagnostic rather than a valid research result.
