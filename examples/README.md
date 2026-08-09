# Examples

These examples show how to repoint Architecture Radar without changing the workflow wrapper.

Copy an example's files into the repository root:

| Example file | Root target |
|---|---|
| `interests.md` | `interests.md` |
| `research-scope.md` | `docs/research-scope.md` |
| `watchlist.yml` | `watchlist.yml` |

Then run the `Architecture Radar` workflow manually.

## Available Examples

- [`opportunity-demand-radar`](opportunity-demand-radar/) — tracks demand, pain points, emerging products, and commercial opportunities with evidence discipline.

## Adaptation Rule

Only replace the domain files. Keep these files unchanged unless you are intentionally changing how the agent operates:

- `docs/agent-rules.md`
- `.github/workflows/architecture-radar.yml`
- `scripts/`

That separation is what makes the radar reusable: the model can work on different research domains while the deterministic wrapper stays stable.
