## Context

See `proposal.md` for motivation. Current generated PR review already checks validation status, report presence, draft state, and mergeability. It also extracts compact report summaries, but it does not distinguish a report with a useful new signal from a report that is only structurally valid.

## Goals / Non-Goals

**Goals:**

- Add a deterministic value verdict to generated reports.
- Keep the verdict easy to parse from Markdown.
- Let PR summaries recommend merge, targeted fix, or close/watchlist without telling the user to manually re-read the whole report.
- Preserve existing validation as the first gate: failed validation still blocks content review.

**Non-Goals:**

- Do not add a second model call or semantic reviewer.
- Do not recompute architecture novelty or business demand from raw sources.
- Do not update historical reports only to backfill the new section.
- Do not merge or close PRs automatically.

## Decisions

1. Use a single-row Markdown table in `Review Value`.

   The table is compact, existing parsers already support tables, and it gives stable columns:

   `Verdict`, `Score`, `Reason`, `Recommended action`.

   `Score` is a 0-5 integer. It is not a 0-10 ranking, because downstream PR
   helpers display it as `<score>/5` and validators reject larger values.

   Alternative considered: free-form bullets. Rejected because they are harder to validate consistently.

2. Use small enumerations for verdict and action.

   Verdicts are shared across radar types where possible:

   - `high-signal`
   - `useful-delta`
   - `watchlist-only`
   - `weak-signal`
   - `stale-or-duplicate`
   - `no-material-change`
   - `needs-targeted-fix`

   Actions are:

   - `merge`
   - `request-fix`
   - `close`
   - `watchlist`

   Alternative considered: free-form action text only. Rejected because the PR helper needs deterministic behavior.

3. Treat report-declared value as advisory after validation.

   Validators confirm the section is present and coherent. PR summarizers convert `request-fix`, `close`, and `watchlist` into non-merge recommendations. They do not override failed checks, missing report files, draft PRs, or non-mergeable states.

4. Do not require old reports to have `Review Value`.

   The validators already focus on changed/generated reports. Historical artifacts remain useful and should not churn.

5. Repair accidental 0-10 review value scores before validation.

   The workflow prompt must ask for a 0-5 score, but the repair step also
   normalizes a single-row `Review Value` score from 6-10 onto the 0-5 scale
   before strict validation. Values outside 0-10 still fail validation because
   they indicate an unrecognized report format rather than a common scale
   mistake.

## Risks / Trade-offs

- [Risk] The research agent can overstate value in the new section. -> Mitigation: the section must give a concrete reason and action; later changes can add stricter cross-checks against candidate counts, topic repetition, and evidence gaps.
- [Risk] `looks_mergeable` may still mean "merge a weak but honest watchlist update." -> Mitigation: `watchlist` and `close` actions are surfaced distinctly and do not return `looks_mergeable`.
- [Risk] Existing generated PRs created before this change may fail if they are still open. -> Mitigation: this is acceptable for future workflow correctness; users can regenerate those PRs after the rule lands.
