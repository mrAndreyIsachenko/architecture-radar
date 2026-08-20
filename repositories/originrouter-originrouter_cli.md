# originrouter/originrouter_cli

- Repository: https://github.com/originrouter/originrouter_cli
- Review date: 2026-08-20
- Current commit reviewed: `10fe64729a8d0f36e55d8875f8ddacc235fa20b0`
- Commit date: 2026-08-20T13:32:23+08:00
- Branch: `main`
- Previous commit reviewed: none
- Material changes since previous review: first review
- Decision: track

## Problem Fit

This repository informs `ai-llm-systems`, especially durable agent workflows, approval policy governance, and detached AI audit/review loops. The reusable mechanism is the local control plane around a collaboration state machine, not the surrounding product surface.

## Verified Flow

`SessionManager` boots with persistence, approval polling, and an AI audit planner -> `approvalPolicyStore` resolves policy bundles, history, rollbacks, and device/file references -> `PlanImplementVerifyCoordinator` enforces valid collaboration transitions and task phases -> `AiAuditQueryPlanner` creates a detached audit plan request -> `AiOperationReviewer` posts and polls the review sidecar -> tests cover approval polling, collaboration state transitions, policy validation, and durable replay.

- E1 source verified: `src/runtime/approvalPolicyStore.js` implements approval-policy lookup, revision history, rollback, bundle deployment, and reference resolution.
- E1 source verified: `src/runtime/aiAuditQueryPlanner.js` requests a planning payload from the audit service after refreshing the AI access token.
- E1 source verified: `src/runtime/aiOperationReviewer.js` submits operation analysis, polls for completion, and returns the review record when the sidecar completes.
- E1 source verified: `src/collaboration/planImplementVerifyCoordinator.js` encodes the collaboration state machine and the plan/implement/verify transitions.
- E1 source verified: `src/daemon/sessionManager.js` wires the collaboration runtime, approval polling, audit planner, and persistent session maps together.
- E2 test verified: `tests/approvalPolicy.test.js` checks canonical revisioning, validation, and policy evaluation behavior.
- E2 test verified: `tests/collaborationRuntime.test.js` verifies state transitions, duplicate message handling, and persistence across reopen.
- E2 test verified: `tests/collaborationReliability.test.js` verifies durable outbox delivery, fencing, and restart delivery semantics.
- E2 test verified: `tests/aiOperationAudit.test.js` verifies the detached AI audit review flow and the decision-source recording path.
- E2 test verified: `tests/sessionManagerApprovalPoll.test.js` verifies the approval poller lifecycle around a daemon session.

## Architecture

Principal components:

- Session manager and daemon boot logic.
- Revisioned approval-policy store with rollback and bundle deployment.
- Collaboration store/runtime and a plan/implement/verify coordinator.
- Detached AI audit query/review sidecars.
- Persistence and replay logic for sessions, outboxes, and approvals.

Most interesting mechanism: policy revisioning is not just a config file. The runtime stores, resolves, lists, and rolls back named approval-policy revisions and then binds those policies into a collaboration state machine that can move between planning, implementation, verification, blocked, failed, and cancelled states. The AI review sidecar stays detached from the deterministic path so the runtime can keep moving even when audit analysis is slow or unavailable.

Baseline comparison: a conventional agent tool wrapper would fire calls directly and stash a few logs. This repository separates approval policy, collaboration state, audit planning, and review polling into explicit subsystems with persistence and replay.

## Reuse Guidance

Reusable:

- Keep approval policy as a versioned artifact with a rollback path.
- Model agent work as a state machine with explicit transitions, not as a loose transcript.
- Run audit/review work in a detached sidecar so it cannot block the deterministic runtime.
- Store durable outbox or session state so restart delivery is possible.

Do not copy:

- Do not copy the product-specific relay, account, and auth plumbing without a narrower wrapper.
- Do not treat the external AI audit service as optional if the runtime depends on its results.
- Do not assume the collaboration state machine will generalize without simplifying the domain terms.

## Quality, Limits, And Adoption Conditions

Production-quality signals:

- The approval-policy store has validation, revision, deployment, and rollback coverage.
- Collaboration runtime tests cover duplicate detection and state persistence.
- Reliability tests cover durable delivery and restart behavior.
- The daemon/session boundary is explicit.

Experimental or incomplete for our needs:

- The system depends on external AI audit endpoints.
- Policy and collaboration semantics are tightly coupled to the product's terminology.
- Some runtime paths still need intended-backend validation in a real deployment.

Hidden costs and failure modes:

- Approval-policy history can drift if revisions are manually altered outside the store contract.
- Detached audit services can fail or time out without stopping the main runtime, which means the caller must decide how much the audit result matters.
- Collaboration state transitions must remain aligned with persistence semantics or restart recovery will become confusing.

Adoption experiment:

Run one session through planning, approval, implementation, and verification with a forced audit-service timeout, then confirm that the deterministic collaboration state still advances correctly and the audit result remains separated from core progress.

## Candidate Patterns

- `approval-revision store`
- `plan-implement-verify state machine`
- `detached AI audit sidecar`
