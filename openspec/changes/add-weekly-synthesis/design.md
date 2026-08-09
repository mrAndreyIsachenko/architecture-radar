# Design: Weekly Synthesis

## Workflow Shape

Add `.github/workflows/weekly-synthesis.yml` with:

- a weekly schedule;
- `workflow_dispatch` for manual runs;
- model override input;
- a deterministic prepare step;
- one Codex synthesis step;
- deterministic validation;
- deterministic publish step with a narrow allowlist.

The workflow writes only to `weekly-reports/`.

## Inputs

The synthesis prompt instructs the agent to read:

- `interests.md`;
- `docs/research-scope.md`;
- `reports/`;
- `repositories/`;
- `patterns/`;
- `radar.json`;
- `opportunity-interests.md`;
- `opportunity-reports/`;
- `opportunities/`;
- `opportunities.json`.

The workflow does not need live web search. It should synthesize committed repository artifacts only.

## Output Format

Reports are written as `weekly-reports/YYYY-Www.md` and contain:

- week and scope;
- input reports;
- executive synthesis;
- pattern movement;
- topic coverage;
- repeated candidates or signals;
- decisions and experiments;
- evidence gaps;
- next week focus.

## Validation

Add `scripts/validate-weekly-synthesis-state.py` and unit tests. The validator checks that changed weekly reports contain the required sections and a basic input-report reference.

The main validation workflow runs the weekly validator on every PR.

## Publishing Boundary

The publish step stages only `weekly-reports/`. The model step receives OpenAI credentials but no GitHub token; the publish step receives GitHub credentials but no OpenAI key.

## Cost

Weekly synthesis should be cheaper than discovery. It reads existing artifacts and defaults to the same mini model family as other recurring workflows. It should not clone external repositories or use live discovery.
