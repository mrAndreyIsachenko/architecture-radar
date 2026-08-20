# wso2/labs-agentic-engineer

- Repository: https://github.com/wso2/labs-agentic-engineer
- Review date: 2026-08-20
- Current commit reviewed: `613e9ce58485f8bb5e120a62dd1994234caea9b0`
- Commit date: 2026-08-20T11:02:31+05:30
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `ai-llm-systems`, especially agentic workflow recovery and evidence-preserving authoring. The reusable mechanism is not the platform branding; it is the write-gated spec bundle and the deterministic projections that turn authored component files into derived machine views.

## Verified Flow

`parseSseStream` consumes a turn stream -> `FileBundle` applies anchored add/edit/remove operations -> `commit` runs YAML and artifact-specific gates (`checkComponentDesign`, `checkOpenapiSpec`, `checkWireframeLayout`) -> `parseTaskContextFile` extracts task frontmatter from `tasks/<issue>.md` -> `buildProjectDesign` folds the bundle into a project design -> `toCellDiagramProject` projects the design into a cell-diagram view -> tests verify the gates and derived views.

- E1 source verified: `packages/agent-stream/src/sse-client.ts` defines `parseSseStream` and `streamTurn` as a transport-only SSE fold that buffers frames across chunk boundaries and terminates on `[DONE]`.
- E1 source verified: `packages/agent-stream/src/bundle.ts` defines `FileBundle` with exact-once anchored edits, idempotent add/remove behavior, and write gates that reject invalid YAML or artifact-specific content without mutating the bundle.
- E1 source verified: `packages/agent-stream/src/component-design-schema.ts` defines `checkComponentDesign`, which rejects malformed `design.json` writes when JSON parsing, schema validation, name/directory matching, or the hard-coded buildpack rule fails.
- E1 source verified: `packages/agent-stream/src/task-context.ts` defines `parseTaskContextFile`, which reads the `tasks/<issue>.md` convention and degrades gracefully on malformed frontmatter.
- E1 source verified: `packages/design-projection/src/project-design.ts` defines `buildProjectDesign`, which deterministically folds the file bundle into a project model.
- E1 source verified: `packages/design-projection/src/cell-diagram.ts` defines `toCellDiagramProject`, which converts the derived project model into a renderer-facing cell-diagram structure.
- E2 test verified: `packages/agent-stream/test/change.test.ts` exercises bundle operations and exact-once edit behavior.
- E2 test verified: `packages/agent-stream/test/component-design-gate.test.ts` and `packages/agent-stream/test/openapi-spec-gate.test.ts` verify that invalid authored artifacts are rejected by the commit gate.
- E2 test verified: `packages/agent-stream/test/task-context.test.ts` verifies task-context parsing and malformed frontmatter recovery.
- E2 test verified: `packages/design-projection/test/project-design.test.ts` and `packages/design-projection/test/cell-diagram.test.ts` verify the deterministic projection chain.

## Architecture

Principal components:

- `FileBundle`: in-memory spec bundle with anchored replace semantics and path-level protection.
- Artifact gates: schema and syntax checks for authored files before a write is committed.
- SSE client: a wire parser that folds streamed turn events into a caller-owned execution loop.
- Task context parser: read-only convention parser for issue/task metadata.
- Design projection layer: deterministic projection from authored specs into reusable machine views.

Most interesting mechanism: the bundle treats a write as a gated transaction, not a text substitution. A candidate edit either anchors exactly once and passes all artifact gates, or the bundle remains byte-for-byte unchanged. The derived design views then fold the authoring state into stable projections that downstream tools can consume.

Baseline comparison: a conventional agent loop would rewrite files directly from the model response and rely on human review to catch corruption. This repository inserts parse-only gates and exact-once anchoring before any state change, then projects the accepted state into machine-readable views.

## Reuse Guidance

Reusable:

- Use anchored edits plus parse-only gates for any agent-authored spec bundle.
- Keep derived machine views separate from authored source files.
- Treat task metadata conventions as a read-only parser boundary.
- Preserve idempotency on repeated tool calls so retries do not wedge the loop.

Do not copy:

- Do not copy the hard-coded project file names or the platform-specific buildpack rule.
- Do not treat the in-memory bundle as a production persistence layer.
- Do not assume the exact file conventions will generalize without an adapter.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The bundle, schema gate, and derived projections all have dedicated tests.
- The SSE parser is factored so callers can own transport and authentication.
- Invalid authored content is rejected without corrupting the bundle.

Experimental or incomplete for our needs:

- The bundle is in-memory and file-convention dependent.
- The buildpack rule is hard-coded to the current platform assumption.
- The repository is broader than the file-gate mechanism alone.

Hidden costs and failure modes:

- Anchored edits require the caller to supply a unique snippet; short or ambiguous anchors can fail.
- Derived views can drift from the authored bundle if downstream consumers treat them as canonical.
- The current gating model assumes one writer owns the bundle.
- The hard-coded path conventions are a coupling point for future schema drift.

Adoption experiment:

Wrap one of our authored-spec workflows in a small bundle/gate adapter, then verify that an invalid spec write is rejected without mutating state and that the resulting projection stays deterministic across retries.

## Candidate Patterns

- `anchored spec bundle write gate`
- `deterministic design projection pipeline`
