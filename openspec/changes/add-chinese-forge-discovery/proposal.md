## Why

Architecture Radar currently treats GitHub as the primary source discovery surface, which can miss China-originated open-source work and repositories published first on regional forges. The immediate problem is discovery blind spots for drones, VPN/privacy networking, satellites, AI/LLM systems, and document AI projects whose public activity may be visible on Gitee, GitCode, or adjacent Chinese developer platforms before it appears on GitHub.

## What Changes

- Add Chinese forge and regional source discovery as an explicit Architecture Radar discovery path.
- Treat Gitee and GitCode as first-class candidate discovery surfaces when relevant to configured topic families.
- Treat Tencent CODING, Alibaba Codeup, Huawei CodeArts Repo, JiHu/GitLab China, launch pages, company pages, and product pages as secondary discovery evidence unless they expose inspectable source.
- Require mirror/upstream mapping when a candidate appears on both GitHub and a Chinese forge.
- Require stable revision evidence before source-level review; inaccessible, login-gated, or non-stable source views must remain triaged/deferred rather than selected.
- Preserve the existing evidence bar: non-GitHub discovery can find candidates, but selected reviews still need source-backed implementation evidence tied to `interests.md`.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `architecture-radar`: Discovery, candidate accounting, and source-level review rules expand beyond GitHub-only repository discovery to include Chinese forge and regional source-platform discovery with mirror, provenance, and access constraints.

## Impact

- `docs/agent-rules.md` discovery and candidate accounting guidance.
- `docs/research-scope.md` discovery surface notes and search seed calibration.
- `scripts/run-codex-radar.sh` prompt text passed to the research agent.
- `scripts/validate-radar-state.py` and tests if current validation assumes GitHub-only URLs, commit fields, or discovery-source wording.
- No change to Opportunity Radar behavior.
