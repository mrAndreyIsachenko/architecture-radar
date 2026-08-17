## Context

The scheduled Architecture Radar workflow already runs a deterministic normalization step before validation. Today that step only downgrades unambiguous evidence-label inflation. The 2026-08-17 run failed later in validation because the generated `Candidate Ledger` table did not expose the exact required `URL` header even though this is a common recoverable formatting drift.

## Goals / Non-Goals

**Goals:**

- Repair safe `Candidate Ledger` header aliases before strict validation.
- Preserve the hard validation contract for missing URL data.
- Keep the fix local to the existing normalization step and tests.

**Non-Goals:**

- Do not infer or synthesize repository URLs.
- Do not relax `scripts/validate-radar-state.py`.
- Do not change Architecture Radar discovery, selection, cadence, or publish permissions.

## Decisions

- Extend `scripts/normalize-radar-evidence-labels.py` instead of weakening the validator.
  - Rationale: the workflow already runs this script immediately before validation, so a safe structural repair can happen without changing publication boundaries.
  - Alternative rejected: let the validator accept aliases. That would blur the artifact contract and make downstream summarizers less predictable.
- Normalize only URL-like aliases to the canonical `URL` header.
  - Rationale: aliases such as `Repository URL`, `Repo URL`, `Link`, or `Source URL` preserve row shape and data; a truly absent URL column still fails.
  - Alternative rejected: insert a blank `URL` column. That would hide missing evidence and produce weaker reports.

## Risks / Trade-offs

- Alias list is incomplete -> Mitigation: keep validation failure explicit for unknown shapes and extend the normalizer only after observed failures.
- A non-URL `Link` column could be renamed -> Mitigation: only rename when the candidate ledger table otherwise has the required architecture-radar columns.
