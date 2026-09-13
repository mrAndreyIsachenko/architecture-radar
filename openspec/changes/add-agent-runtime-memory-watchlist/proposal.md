## Why

Architecture Radar missed two high-signal AI infrastructure launches: the canonical DeepSeek Harness runtime and TencentDB Agent Memory. The current discovery rules mention agent runtimes and memory generally, but they do not force canonical source expansion when broad search finds secondary handbooks, forks, or vendor pages first.

## What Changes

- Add DeepSeek Harness and TencentDB Agent Memory as explicit Architecture Radar watchlist seeds.
- Extend architecture discovery seeds with AI runtime and agent-memory launch anchors.
- Require the Architecture Radar run to resolve secondary DeepSeek Harness or Tencent Agent Memory hits to their canonical source repositories before rejecting the topic.
- Keep the normal source evidence bar: watchlist inclusion forces accounting and source inspection, not automatic selection.
- Non-goal: this change does not add Opportunity Radar commercial scoring, generated reports, or repository reviews for these projects.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `architecture-radar`: Discovery must not miss canonical agent runtime and memory launch repositories when secondary docs, handbooks, forks, product pages, or regional/vendor aliases are encountered first.

## Impact

- `watchlist.yml`
- `docs/research-scope.md`
- `docs/agent-rules.md`
- Architecture Radar OpenSpec delta and validation artifacts
